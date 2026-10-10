#!/usr/bin/env python3
"""Fail if any hex projection of the palette drifts from the oklch source.

dracula-nineties.css :root is the single source of truth. Two projections carry the
same colors as hex, because Mermaid's color engine (khroma) throws "Unsupported
color format" on oklch() and renders no diagram at all:

  mermaid-palette.json  - the declared hex palette, keyed by themeVariables name
  mermaid.js            - the same values inline (consumers inline it, no build)

contract-check.yml already pins mermaid.js to mermaid-palette.json. This closes
the remaining edge: mermaid-palette.json back to the CSS it claims to project.
It is what makes the "from" fields load-bearing rather than decorative.

Paths resolve from this script's location, so cwd does not matter (scripts/maintain.nu
calls it by absolute path). Exit 1 on any drift.

ponytail: stdlib-only Oklab -> sRGB, no colour-science dependency for 18 values.
"""
import json
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def oklch_to_linear_raw(L, C, h):
    """oklch() -> linear sRGB, unclamped, so a channel outside 0..1 stays visible."""
    a = C * math.cos(math.radians(h))
    b = C * math.sin(math.radians(h))
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def oklch_to_linear(L, C, h):
    """oklch() -> clamped linear sRGB. Clamping here is the gamut clip a browser does."""
    return tuple(min(1.0, max(0.0, v)) for v in oklch_to_linear_raw(L, C, h))


def max_chroma(L, h, eps=1e-4):
    """The largest chroma at this lightness and hue that still lands inside sRGB.

    Bisection, because there is no closed form: the sRGB boundary in Oklab is the
    surface where one of the three channels hits 0 or 1, and which channel that is
    depends on the hue. 40 halvings of 0..0.5 resolve it far finer than the three
    decimals a token is written to.
    """
    lo, hi = 0.0, 0.5
    for _ in range(40):
        mid = (lo + hi) / 2
        if all(-eps <= v <= 1 + eps for v in oklch_to_linear_raw(L, mid, h)):
            lo = mid
        else:
            hi = mid
    return lo


def oklch_to_hex(L, C, h):
    """oklch() -> #rrggbb, gamut-mapped, matching how a browser renders it.

    Chroma is reduced to the sRGB ceiling before conversion, rather than clipped
    per-channel afterward, because that is what a browser's own CSS Color 4 gamut
    mapping does: hold L and h, pull C in to the boundary. A P3-reaching token (see
    P3_WIDENED) has no exact sRGB hex, but every hex-only consumer (Mermaid, the
    editor themes `--dump` feeds) is sRGB regardless, so this is the nearest
    same-hue-and-lightness color they can actually show, not a hue-shifted guess.
    Every token that already fits in sRGB is untouched: this only ever pulls
    chroma in, never out.
    """

    def encode(x):
        return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055

    C = min(C, max_chroma(L, h))
    return "#%02x%02x%02x" % tuple(round(encode(v) * 255) for v in oklch_to_linear(L, C, h))


def contrast(one, two):
    """WCAG 2.x contrast ratio between two oklch triples, on the clipped values."""

    def relative_luminance(lch):
        r, g, b = oklch_to_linear(*lch)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    a, b = relative_luminance(one), relative_luminance(two)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


stylesheet = (ROOT / "dracula-nineties.css").read_text()

# Only the :root block defines the palette. Scanning the whole stylesheet would let a
# --x: oklch(...) declared inside a component rule join the palette set and quietly
# widen the membership checks below, so a stale hex could start passing. Non-greedy up
# to a closing brace on its own line, and the first match is the real :root, and the
# @media one is a single inline line that never reaches this shape.
root = re.search(r":root \{(.*?)\n\s*\}", stylesheet, re.S)
if not root:
    sys.exit("Could not find the :root block in dracula-nineties.css.")
css = root.group(1)

triples = {
    name: (float(L), float(C), float(h))
    for name, L, C, h in re.findall(
        r"--([\w-]+):\s*oklch\(([\d.]+) ([\d.]+) ([\d.]+)\)", css
    )
}
palette = {name: oklch_to_hex(*lch) for name, lch in triples.items()}
if len(palette) < 18:
    sys.exit(f"Only parsed {len(palette)} oklch tokens from :root, expected 18.")

# The light palette is the base :root overlaid with the light block's overrides, which
# is how the cascade resolves it. mermaid.js carries both hex sets because khroma cannot
# read a var() or an oklch(), and picks one at init from the --mermaid-scheme token.
# Computed ahead of --dump (below) so the editor/terminal themes can render a real light
# variant instead of only ever seeing the dark one.
light_block = re.search(
    r"@media \(prefers-color-scheme: light\) \{\s*:root \{(.*?)\n\s*\}", stylesheet, re.S
)
if not light_block:
    sys.exit("Could not find the light :root block in dracula-nineties.css.")
light_triples = dict(triples)
light_triples.update({
    name: (float(L), float(C), float(h))
    for name, L, C, h in re.findall(
        r"--([\w-]+):\s*oklch\(([\d.]+) ([\d.]+) ([\d.]+)\)", light_block.group(1)
    )
})
light_palette = {name: oklch_to_hex(*lch) for name, lch in light_triples.items()}

# --dump is the generator side of the same parse: scripts/create-themes.nu needs the palette
# as data, and re-deriving oklch -> sRGB in Nushell would mean a second implementation
# of the matrix above, free to drift from the one CI checks. This comment used to say
# Nushell had no trig builtins. It does, since `math sin` and `math cos` both work, checked
# on 0.114.1, so the reason is one implementation, not a missing primitive.
# `bright` is the L + 0.07 rule the Ghostty ANSI slots already document; it lives
# here because it needs oklch, not because it is palette policy. The ceiling is
# 0.99, not 1.0: --on-surface sits at L 0.977, so an unclamped bump lands on
# #fffff9, a white with nothing above it. 0.99 keeps ANSI 15 at #fcfcf6. Dark and light
# get their own ceiling-checked bump off their own lightness, not one borrowed from the
# other: a light-mode token already sitting above 0.92 needs the same clamp dark tokens do.
if "--dump" in sys.argv:
    json.dump(
        {
            "dark": {
                name: {"hex": hexval, "bright": oklch_to_hex(min(0.99, triples[name][0] + 0.07), *triples[name][1:])}
                for name, hexval in palette.items()
            },
            "light": {
                name: {"hex": hexval, "bright": oklch_to_hex(min(0.99, light_triples[name][0] + 0.07), *light_triples[name][1:])}
                for name, hexval in light_palette.items()
            },
        },
        sys.stdout,
    )
    sys.exit(0)

pal = json.loads((ROOT / "mermaid-palette.json").read_text())
fail = 0

# 1. Every init hex is exactly the conversion of the variable it names, in both
#    palettes. initLight names the same tokens and resolves them through the light
#    block, so a light-only token edit cannot slip past by looking right in dark.
for section, source in (("init", palette), ("initLight", light_palette)):
    if section not in pal:
        print(f"DRIFT: mermaid-palette.json has no {section} section")
        fail = 1
        continue
    keys = [k for k in pal[section] if k != "_comment"]
    if len(keys) < 20:
        sys.exit(f"{section} has only {len(keys)} keys, refusing to pass vacuously.")
    for key in keys:
        entry = pal[section][key]
        want = source.get(entry["from"].lstrip("-"))
        if want is None:
            print(f"DRIFT: {section}.{key} names {entry['from']}, which is not in :root")
            fail = 1
        elif entry["hex"] != want:
            print(f"DRIFT: {section}.{key} is {entry['hex']}, {entry['from']} computes to {want}")
            fail = 1
    if set(keys) != set(k for k in pal["init"] if k != "_comment"):
        print(f"DRIFT: {section} and init cover different themeVariables keys")
        fail = 1

# 2. Each classdef fill is exactly the variable its `from` field names, and that is
#    what makes `from` load-bearing here too. stroke/color are shared across every
#    role rather than named, so those get a membership check.
#
#    Both sets are checked, each against its own palette. `classdef` shipped alone and
#    dark-only for four releases, so a generator that emitted its hex onto a page a
#    reader could see in light mode painted dark-ramp fills at the 1.69 to 2.15:1 the
#    --data-* light values were added to fix everywhere else. `classdefLight` is that
#    projection, and the role sets are pinned equal so a role added to one set cannot
#    stay missing from the other.
#    Each set names the token its `color` field projects, because that field is text
#    painted on the fill and the two sets answer it in opposite directions: the dark
#    ramp is pale so the letter is --surface, the light ramp is mid-tone so the letter
#    is --on-surface. That pair is measured, not asserted, which is what caught the
#    light set at 3.45 to 3.53:1 had it reused --surface.
CLASSDEF = (
    ("classdef", palette, triples, "surface"),
    ("classdefLight", light_palette, light_triples, "surface"),
)
for section, source, lch_for, text_token in CLASSDEF:
    if section not in pal:
        print(f"DRIFT: mermaid-palette.json has no {section} section")
        fail = 1
        continue
    for role, entry in pal[section].items():
        if role == "_comment":
            continue
        want = source.get(entry["from"].lstrip("-"))
        if entry["fill"] != want:
            print(f"DRIFT: {section}.{role} fill is {entry['fill']}, {entry['from']} computes to {want}")
            fail = 1
        for found in (entry["stroke"], entry["color"]):
            if found not in source.values():
                print(f"DRIFT: {section}.{role} hex {found} is not a dracula-nineties.css palette color")
                fail = 1
        if entry["color"] != source[text_token]:
            print(
                f"DRIFT: {section}.{role} color is {entry['color']}, but this set paints "
                f"--{text_token} ({source[text_token]}) on its fill"
            )
            fail = 1
        elif want is not None:
            got = contrast(lch_for[text_token], lch_for[entry["from"].lstrip("-")])
            if got + 0.005 < 4.5:
                print(
                    f"CONTRAST: {section}.{role} paints --{text_token} on its "
                    f"{entry['from']} fill at {got:.2f}:1, below 4.5"
                )
                fail = 1
    if {r for r in pal[section] if r != "_comment"} != {
        r for r in pal["classdef"] if r != "_comment"
    }:
        print(f"DRIFT: {section} and classdef cover different node roles")
        fail = 1

# 3. The `/* was #xxxxxx */` provenance comments are read by whoever hand-edits
#    the stylesheet, so they have to stay true too. `.get`, not `[name]`: a token
#    this file cannot parse (alpha slash syntax, say) must report as drift rather
#    than crash with a KeyError that says nothing about which check failed.
for name, stated in re.findall(
    r"--([\w-]+):\s*oklch\([^)]*\);\s*/\* was (#[0-9a-f]{6})", css
):
    if palette.get(name) != stated:
        print(f"DRIFT: --{name} comment says {stated}, its oklch computes to {palette.get(name)}")
        fail = 1

# 4. contract-check.yml maps every palette key onto mermaid.js; this is the
#    reverse: a hex inline in mermaid.js that is no longer a palette color at all
#    (a hand-added themeVariable, a stale value under a renamed key).
known = set(palette.values()) | set(light_palette.values())
for found in sorted(set(re.findall(r"#[0-9a-f]{6}", (ROOT / "mermaid.js").read_text()))):
    if found not in known:
        print(f"DRIFT: mermaid.js hex {found} is not a dracula-nineties.css palette color")
        fail = 1

# 5. Every mode has to hold its own contrast floor. The stylesheet ships four
#    palettes now (the default, `prefers-contrast: more`, `prefers-color-scheme:
#    light` and print) and the ratios behind each one were measured by hand and
#    written into NOTES.md. A measurement in prose is not a gate: a later edit to
#    one lightness value strands text at a ratio nobody re-derives. This check
#    re-derives all of them on every run.
#
#    A mode block only restates what it changes, so each palette is the default
#    overlaid with that block's overrides, which is also how the cascade resolves
#    it. Text tokens are checked against all THREE backgrounds a reader meets:
#    --code-bg carries the default palette's floor, and --surface-alt is the
#    row-hover fill, which NOTES.md names as one of the grounds a token has to
#    clear and which this check did not look at for two releases. It is the
#    hardest of the three in light mode, where --muted, --orange and --pink all
#    measured 4.44 to 4.47 on it while passing on the other two, so a `strong` or
#    an outbound arrow inside a hovered row was under 4.5 with nothing saying so.
#    Rule tokens are checked against --surface and --surface-alt, not --code-bg:
#    --rule-light fences a table cell and outlines a checkbox, and a checkbox sits
#    on --surface-alt (a table header cell is filled --surface-alt too), which is
#    the harder of the two in light mode. A rule is never drawn inside a code fill,
#    so --code-bg is not a ground for this role. 1.4.11 asks 3:1 of a non-text
#    boundary.
#
#    DATA stays on --surface and --code-bg. A diagram is not drawn inside a table
#    row, so the hover fill is not a ground a category fill ever lands on.
#
#    DATA is the diagram-category ramp, and it is a non-text boundary like a rule
#    rather than text: a pie slice or a classDef fill has to be tellable from the
#    card it sits on. It is checked against BOTH grounds because a diagram is drawn
#    on --code-bg while a bare SVG lands on --surface. Through v1.24.0 this ramp had
#    no light or print override and measured 1.69 to 2.15:1 there, which NOTES.md
#    recorded and accepted. v1.25.0 gave it both, so the floor is now gated.
TEXT = ["on-surface", "label", "muted", "link", "visited", "orange", "red", "purple", "purple-bright", "pink", "green"]
RULES = ["rule-light"]
DATA = ["data-1", "data-2", "data-3", "data-4"]
MODES = {
    # name: (media condition, text floor, non-text boundary floor)
    #
    # Every mode that paints text carries the body floor, 4.5:1, except high
    # contrast, which carries 7.0. Default and light were priced down in turn
    # (4.0, then 3.2) to carry a token the palette has since been re-derived
    # around, so neither is a floor any more. Print stays 4.5 because paper has no
    # identity to preserve. The boundary floor for a rule or a data ramp stays 3.0.
    "default": (None, 4.5, 3.0),
    "prefers-contrast: more": ("@media (prefers-contrast: more)", 7.0, 3.0),
    "prefers-color-scheme: light": ("@media (prefers-color-scheme: light)", 4.5, 3.0),
    "print": ("@media print", 4.5, 3.0),
}
# Empty since v2.2.0. The two entries here existed only because the dracula
# baseline forced Comment and Red under 3.0 on the Current Line fill; the 1990s
# reset lifted both, so the default floor carries them and no pair needs naming.
# Keep the table: a future baseline that forces a pair names it here rather than
# lowering a whole mode.
FLOOR_OVERRIDE = {}
resolved = {}
for mode, (condition, text_floor, rule_floor) in MODES.items():
    triples_for_mode = dict(triples)
    if condition is not None:
        block = re.search(
            re.escape(condition) + r" \{\s*:root \{(.*?)\n\s*\}", stylesheet, re.S
        )
        if not block:
            print(f"DRIFT: no `{condition}` block with a :root of its own")
            fail = 1
            continue
        overrides = {
            name: (float(L), float(C), float(h))
            for name, L, C, h in re.findall(
                r"--([\w-]+):\s*oklch\(([\d.]+) ([\d.]+) ([\d.]+)\)", block.group(1)
            )
        }
        if not overrides:
            print(f"DRIFT: the `{condition}` block redefines no oklch token")
            fail = 1
            continue
        triples_for_mode.update(overrides)
    resolved[mode] = triples_for_mode
    # --on-surface goes to `oklch(1 0 0)` in high contrast, which the triple regex
    # reads fine, and print writes `oklch(0.200 0 0)`. Both parse. A token that
    # stops parsing drops back to its default value rather than vanishing, so a
    # weakened override cannot pass by becoming unreadable.
    for role, floor in ((TEXT, text_floor), (RULES, rule_floor), (DATA, rule_floor)):
        for name in role:
            fg = triples_for_mode[name]
            if role is RULES:
                grounds = ["surface", "surface-alt"]
            elif role is DATA:
                grounds = ["surface", "code-bg"]
            else:
                grounds = ["surface", "code-bg", "surface-alt"]
            for ground in grounds:
                got = contrast(fg, triples_for_mode[ground])
                limit = FLOOR_OVERRIDE.get((mode, name), floor)
                if got + 0.005 < limit:
                    print(
                        f"CONTRAST: {mode} --{name} is {got:.2f}:1 on --{ground}, "
                        f"below the {limit} floor for this mode"
                    )
                    fail = 1

# 6. --mermaid-scheme is the whole mechanism that lets a diagram follow the palette,
#    and deleting it fails silently: mermaid.js reads an empty string, decides "not
#    light", and renders a dark diagram on a light page while every other check stays
#    green. That is the exact defect this token was added to fix, so it is gated
#    rather than trusted. The token is not an oklch() value, so nothing else here sees
#    it, and the JS side is checked by name because a renamed token is the same bug.
mermaid_js = (ROOT / "mermaid.js").read_text()
for where, want, block_text in (
    (":root", "dark", css),
    ("the light :root block", "light", light_block.group(1)),
):
    if not re.search(r"--mermaid-scheme:\s*" + want + r"\s*;", block_text):
        print(f"DRIFT: {where} does not declare --mermaid-scheme: {want}")
        fail = 1
if "--mermaid-scheme" not in mermaid_js:
    print("DRIFT: mermaid.js never reads --mermaid-scheme, so a diagram cannot follow the palette")
    fail = 1
if "prefers-color-scheme" in mermaid_js:
    print("DRIFT: mermaid.js reads prefers-color-scheme, which reports the host, not the "
          "cascade, so the forced-light sample pages would render a dark diagram. Read "
          "--mermaid-scheme off the computed style instead")
    fail = 1

#    mermaid.js decides whether a `pre` is a scrollable region from the same width the
#    stylesheet gives it `overflow-x: auto`, and the two carry that number separately.
#    A breakpoint moved on one side alone puts the tab stop where nothing scrolls, or
#    takes it away from where something does, and neither shows up in a render of the
#    other side. So the literal is pinned in both files.
SCROLL_BREAKPOINT = "(max-width: 600px)"
if f"@media {SCROLL_BREAKPOINT}" not in stylesheet:
    print(f"DRIFT: dracula-nineties.css has no `@media {SCROLL_BREAKPOINT}` block, which is "
          f"where pre.mermaid gets its scroll axis")
    fail = 1
#    The match is against the matchMedia call, not the file: mermaid.js names the same
#    breakpoint in the comment beside it, and a bare substring check passed on that
#    comment while the live query said 700px. Caught by mutating it.
if f"matchMedia('{SCROLL_BREAKPOINT}')" not in mermaid_js:
    print(f"DRIFT: mermaid.js does not call matchMedia('{SCROLL_BREAKPOINT}'), so the "
          f"diagram region no longer tracks the width at which pre.mermaid can scroll")
    fail = 1

# 7. Every declared chroma has to be reachable in sRGB, in every mode. A value above
#    the ceiling is not an error the browser reports: it clips per channel and paints
#    something else, so the stylesheet documents a color it never renders and every
#    check above still passes, because they all measure the clipped result. The
#    high-contrast block shipped three of these. --red was `oklch(0.895 0.142 21.457)`
#    where the ceiling at that lightness and hue is 0.055, so the declared chroma was
#    259% of what sRGB can hold, and Chrome painted `oklch(0.842 0.087 20.795)`: 0.053
#    of lightness and 0.055 of chroma gone, ΔE_ok 0.077 from the stated value. --pink
#    also drifted 4.9 degrees of hue, which is the part that makes this more than
#    bookkeeping.
#
#    The trap this closes is directional. An editor reading C 0.142 sees chroma to
#    spare and raises L for more contrast, but the ceiling *shrinks* as L climbs
#    (0.159 at L 0.74 against 0.052 at L 0.90 on that hue), so the color washes out
#    faster than the numbers in front of them predict. Checked in all four modes, on
#    every token the triple regex parses, not just the ones with a contrast floor.
#
#    The 0.0005 slack is one unit in the third decimal a token is written to. Sitting
#    exactly on the boundary passes, and it is still a bad place to sit: a later
#    lightness nudge tips it out. Aim for the fraction of maximum chroma the dark
#    token holds, which is the method the --data-* ramp already documents.
#
#    Every token is now an exact sRGB hex from the upstream baseline, so the sRGB
#    ceiling is the only ruler and the P3 widening this check used to carry is gone.
#    The trap it closes is unchanged: a declared chroma over the ceiling renders as
#    a browser clip, not an error, and every check above measures the clipped result.
for mode, triples_for_mode in resolved.items():
    for name, (L, C, h) in sorted(triples_for_mode.items()):
        ceiling = max_chroma(L, h)
        if C > ceiling + 0.0005:
            print(
                f"GAMUT: {mode} --{name} declares chroma {C:.3f} at L {L:.3f} hue {h:g}, "
                f"where sRGB holds {ceiling:.3f} ({C / ceiling * 100:.0f}% of the ceiling). "
                f"The browser clips it to {oklch_to_hex(L, C, h)} instead."
            )
            fail = 1

# 8. An accent used as a BACKGROUND is a pair no check above ever looks at. Check 5
#    only ever puts a token in the foreground, on --surface, --code-bg or
#    --surface-alt. Three components invert that: `.verdict-*`, `.step-node` and
#    `h2.band` all paint --surface TEXT on an accent fill. Nothing gated either of the
#    first two, and the gap
#    is not theoretical: the first draft of the .tag-dot fixture painted --surface on a
#    --data-* fill at a ratio a reader would have copied, caught by hand that time.
#    `.step-node` takes its fill from an --icon-color custom property, so the same
#    mistake is one property away.
#
#    The Dracula baseline makes --surface legible on every --data-* member in every
#    mode, so the ramp is no longer out of bounds for .step-node and the permitted set
#    below includes it. A .tag-dot still paints currentColor on an empty element, and
#    an .icon-chip still paints its glyph on a --code-bg fill, neither of which is a
#    full-strength accent under real text. Only a full-strength fill under real text is
#    the problem, and that pair is what this check measures.
#
#    Print is skipped for `.verdict-*` and `h2.band`, because the print block replaces
#    the fill with `background: none` plus a currentColor ring and recolors the text, so
#    the pair this check describes does not exist on paper. `.step-node` has no print
#    override, so it is checked there like everywhere else.
INVERTED = {
    ".verdict-*": ("surface", ["green", "orange", "red", "muted"], {"print"}),
    "h2.band": ("surface", ["purple"], {"print"}),
    ".step-node": ("surface", ["orange", "link", "purple", "green",
                               "data-1", "data-2", "data-3", "data-4"], set()),
}
for mode, triples_for_mode in resolved.items():
    floor = MODES[mode][1]
    for component, (text, grounds, skip) in INVERTED.items():
        if mode in skip:
            continue
        for ground in grounds:
            got = contrast(triples_for_mode[text], triples_for_mode[ground])
            if got + 0.005 < floor:
                print(
                    f"CONTRAST: {mode} {component} puts --{text} text on a --{ground} "
                    f"fill at {got:.2f}:1, below the {floor} floor for this mode"
                )
                fail = 1

# 9. --highlight is written with relative color syntax, and the triple regex above
#     cannot see it: `--highlight: oklch(from var(--orange) l c h / 0.30)` sat outside
#     checks 5 and 7 entirely. It is a background, so check 5's foreground pairs never
#     covered the `mark` text painted on it, and check 7 never saw the chroma.
#
#     --purple-bright used to be relative here too, but the exact #bd93f9 has no
#     headroom: any lightness bump off it leaves sRGB, so all four modes now state it
#     as a literal and it rides checks 5 and 7 like any other accent.
#
#     Only the one form survives, and a second relative form may return, so this
#     resolves the general shape rather than the single instance. A form it cannot
#     parse fails loudly below instead of being silently skipped, which is the failure
#     mode this check exists to remove.
RELATIVE = re.compile(
    r"--([\w-]+):\s*oklch\(from var\(--([\w-]+)\) "
    r"(?:calc\(l ([+-]) ([\d.]+)\)|l) c h(?: / ([\d.]+))?\)"
)


def relative_decls(text):
    out = {}
    for name, base, sign, delta, alpha in RELATIVE.findall(text):
        shift = 0.0 if not delta else (float(delta) if sign == "+" else -float(delta))
        out[name] = (base, shift, float(alpha) if alpha else 1.0)
    return out


def encode(x):
    return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055


def decode(x):
    return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4


def over(fg, bg, alpha):
    """Alpha-composite two oklch triples, in the gamma-encoded space a browser uses.

    Compositing the linear values instead reads several tenths of a ratio too bright,
    which is enough to turn a failing pair into a passing one. Checks 9 and 11 both
    depend on the gamma-encoded space, so it has to match what the browser does rather
    than an assumption about it.
    """
    f, b = oklch_to_linear(*fg), oklch_to_linear(*bg)
    return tuple(decode(encode(x) * alpha + encode(y) * (1 - alpha)) for x, y in zip(f, b))


def relative_luminance_lin(lin):
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast_lin(one, two):
    a, b = relative_luminance_lin(one), relative_luminance_lin(two)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


base_relative = relative_decls(css)
declared_relative = set(base_relative)
for mode, (condition, text_floor, rule_floor) in MODES.items():
    triples_for_mode = resolved.get(mode)
    if triples_for_mode is None:
        continue
    block = css
    if condition is not None:
        found = re.search(
            re.escape(condition) + r" \{\s*:root \{(.*?)\n\s*\}", stylesheet, re.S
        )
        block = found.group(1) if found else ""
    rel = dict(base_relative)
    rel.update(relative_decls(block))
    declared_relative |= set(rel)
    for name, (base, shift, alpha) in rel.items():
        # A mode may override the relative form with a literal, which print does for
        # --purple-bright and which prefers-contrast: more now has to do as well. Check
        # 7 already owns the gamut for a literal, because the triple regex sees it; the
        # contrast floor is checked here either way, since --purple-bright is in no
        # role list above and would otherwise be measured in two modes out of four.
        literal = name in triples_for_mode
        L, C, h = triples_for_mode[name] if literal else triples_for_mode[base]
        resolved_lch = (L, C, h) if literal else (L + shift, C, h)
        origin = f"--{name}" if literal else f"--{name} (from --{base})"
        if alpha == 1.0:
            for ground in ("surface", "code-bg", "surface-alt"):
                got = contrast(resolved_lch, triples_for_mode[ground])
                if got + 0.005 < text_floor:
                    print(
                        f"CONTRAST: {mode} {origin} is {got:.2f}:1 on "
                        f"--{ground}, below the {text_floor} floor for this mode"
                    )
                    fail = 1
            if not literal:
                ceiling = max_chroma(resolved_lch[0], resolved_lch[2])
                if C > ceiling + 0.0005:
                    print(
                        f"GAMUT: {mode} {origin} declares chroma {C:.3f} at "
                        f"L {resolved_lch[0]:.3f}, where the ceiling holds {ceiling:.3f}"
                    )
                    fail = 1
        else:
            # An alpha wash is a background, and --on-surface is what `mark` pins on
            # top of it. The floor is 4.5 in every mode, including prefers-contrast:
            # more, because the alpha caps what the composite can reach and NOTES.md
            # already records that trade: a lower alpha would make the highlight
            # harder to see, which is the one thing the element exists to do.
            for ground in ("surface", "code-bg"):
                composite = over(resolved_lch, triples_for_mode[ground], alpha)
                got = contrast_lin(oklch_to_linear(*triples_for_mode["on-surface"]), composite)
                if got + 0.005 < 4.5:
                    print(
                        f"CONTRAST: {mode} --on-surface on --{name} ({alpha:g} alpha of "
                        f"--{base}) over --{ground} is {got:.2f}:1, below 4.5"
                    )
                    fail = 1

#     A token that stops matching RELATIVE stops being checked, and a check that
#     silently covers nothing is worse than no check. Both names are pinned.
for name in ("purple-bright", "highlight"):
    if name not in declared_relative and name not in triples:
        print(
            f"DRIFT: --{name} is neither an oklch() triple nor a relative color this "
            f"file can parse, so nothing measures it in any mode"
        )
        fail = 1

# 10. A pie slice label is the one place a themeVariable lands ON another
#     themeVariable, so check 5 cannot see it: it measures every token against
#     --surface, --code-bg and --surface-alt, and a slice is none of those. Mermaid
#     draws `.slice { fill: pieSectionTextColor }` over `.pieCircle { fill: pieN }`,
#     and its stock single `textColor` cannot serve both palettes, because the fills
#     are pale in dark mode and mid-tone in light. Measured before this check existed:
#     a dark-mode slice label was #f8f8f2 on a pale fill at 1.81:1 flat.
#
#     `pieOpacity` is pinned to '1' in the same breath. Mermaid defaults it to 0.7, and
#     a slice composited at 0.7 measured 2.15 to 2.22:1 against the light card even
#     after the --data-* ramp cleared 3.2:1 flat, so the opacity is what the ramp's own
#     floor depends on. It is not a color, so nothing else in this file or in
#     contract-check.yml would notice it going back to the default.
for section, source, lch_for in (
    ("init", palette, triples),
    ("initLight", light_palette, light_triples),
):
    label = pal.get(section, {}).get("pieSectionTextColor")
    if label is None:
        print(f"DRIFT: {section} declares no pieSectionTextColor, so a slice label falls "
              f"back to mermaid's single textColor, which one palette always fails")
        fail = 1
        continue
    text = lch_for[label["from"].lstrip("-")]
    for i in (1, 2, 3, 4):
        slice_from = pal[section][f"pie{i}"]["from"].lstrip("-")
        got = contrast(text, lch_for[slice_from])
        if got + 0.005 < 4.5:
            print(
                f"CONTRAST: {section} pieSectionTextColor ({label['from']}) on a pie{i} "
                f"slice (--{slice_from}) is {got:.2f}:1, below 4.5"
            )
            fail = 1
#     Mermaid bakes its hex at init and print is a media query with no re-render, so a
#     diagram themed for a dark page keeps painting its own colours while @media print
#     turns --surface white. Everything the diagram draws on the page ground rather than
#     on a node fill then went white on white, about 1.0:1 on paper. The fix is to give
#     the diagram back the ground it was themed for, so --diagram-ground in the print
#     block has to BE the default --surface: a drift between them repaints the ground in
#     a colour the SVG was never themed against, and nothing else here reads printed
#     output. `print-color-adjust: exact` is what makes it survive Chrome's default
#     "background graphics off", verified against a PDF rendered with backgrounds
#     suppressed, so it is pinned too.
print_ground = relative_decls("")  # placeholder, kept so the shape below reads plainly
frozen = re.search(r"@media print \{.*?\n      pre\.mermaid \{(.*?)\n      \}", stylesheet, re.S)
if not frozen:
    print("DRIFT: the @media print block has no `pre.mermaid` rule, so a dark-themed "
          "diagram prints its own colors against white paper")
    fail = 1
else:
    got = {
        name: (float(L), float(C), float(h))
        for name, L, C, h in re.findall(
            r"--([\w-]+):\s*oklch\(([\d.]+) ([\d.]+) ([\d.]+)\)", frozen.group(1)
        )
    }
    # Every token any pre.mermaid or .mermaid-overlay rule resolves through. A token used
    # there but not frozen resolves to the paper palette instead, which is how the packet
    # title and the byte labels first came out dark on the dark ground.
    for name in ("surface", "on-surface", "code-bg", "purple", "muted"):
        if name not in got:
            print(f"DRIFT: @media print pre.mermaid does not freeze --{name}, so it resolves "
                  f"to the paper palette inside a diagram themed against the default one")
            fail = 1
        elif got[name] != triples[name]:
            print(f"DRIFT: @media print pre.mermaid freezes --{name} at {got[name]}, but the "
                  f"SVG is themed against the default {triples[name]}")
            fail = 1
for pin in ("print-color-adjust: exact", "-webkit-print-color-adjust: exact",
            "background: var(--surface); padding: var(--space-3) 0"):
    if pin not in stylesheet:
        print(f"DRIFT: dracula-nineties.css no longer carries `{pin}` on pre.mermaid in print, so the "
              f"diagram loses its ground in print")
        fail = 1
if "@media print and (prefers-color-scheme: light) {" not in stylesheet:
    print("DRIFT: no `@media print and (prefers-color-scheme: light)` block, so a "
          "light-themed diagram gets a dark ground it was never themed for")
    fail = 1

# 11. The bar chart puts a --data-* member somewhere no check above looks: it is an
#     alpha wash of --data-1 painted UNDER the number in the same
#     cell, so the pair is --on-surface over that wash over --surface or over the
#     row-hover fill, and the alpha decides whether it clears the text floor. That is the
#     same shape as the --highlight wash check 9 measures for a :root token, except this
#     wash is written inside a rule, so no token exists for the regex to find.
#
#     The alpha is read out of the rule rather than restated here, so nudging it is what
#     fails this check instead of silently moving a text pair under the floor.
bar = re.search(
    r"table\.bar-chart td\.bar \{ --bar-tint: oklch\(from var\(--data-1\) l c h / ([\d.]+)\)",
    stylesheet,
)
if not bar:
    print("DRIFT: table.bar-chart td.bar no longer declares --bar-tint as an alpha of "
          "--data-1, so nothing measures the number that sits on the band")
    fail = 1
else:
    bar_alpha = float(bar.group(1))
    for mode, triples_for_mode in resolved.items():
        for ground in ("surface", "surface-alt"):
            for name in DATA:
                composite = over(triples_for_mode[name], triples_for_mode[ground], bar_alpha)
                got = contrast_lin(oklch_to_linear(*triples_for_mode["on-surface"]), composite)
                if got + 0.005 < 4.5:
                    print(
                        f"CONTRAST: {mode} --on-surface on a bar band ({bar_alpha:g} alpha "
                        f"of --{name}) over --{ground} is {got:.2f}:1, below 4.5"
                    )
                    fail = 1

#     The band paints through a background image, which Chrome drops when it prints
#     (verified by render). The print pin gives it back. Forced colors drops it outright
#     and cannot get it back, which costs the band and no number, so nothing is pinned
#     for that mode. `.tag-dot::before` rides the same print pin for the same reason.
pin = "table.bar-chart td.bar, .tag-dot::before { print-color-adjust: exact;"
if pin not in stylesheet:
    print(f"DRIFT: dracula-nineties.css no longer carries `{pin}`, so a bar band and a "
          f"legend dot print blank")
    fail = 1

if not re.search(r"pieOpacity:\s*'1'", mermaid_js):
    print("DRIFT: mermaid.js does not pin pieOpacity to '1'. Mermaid's 0.7 default "
          "composites every slice toward the card and drops it under the 3:1 floor "
          "the --data-* ramp is gated to")
    fail = 1

print("Palette drift." if fail else f"Palette OK ({len(palette)} tokens, 4 modes).")
sys.exit(fail)
