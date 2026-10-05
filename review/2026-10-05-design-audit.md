# Design audit: period fidelity, 1994 through 1999

- **Date:** 2026-10-05
- **Range:** since `bb18544` (initial commit), nine commits that touched the payload, plus an
  uncommitted table-fence delta in the working tree.
- **Previous report:** none. No `review/*-design-audit.md` existed, so this run reports against
  `NOTES.md` alone and the window is the last ten commits that touched the payload.
- **`review/declined.md`:** exists, no rows. No finding is suppressed by a prior decline.
- **Verdict:** one violation of a settled decision (a hidden control the reset repainted) and one
  documentation drift, both in the patch. One dependency recommendation stays out of the patch.

The audit's design vocabulary stops at 1999: HTML 3.2, HTML 4.0/4.01, CSS1, CSS2, WCAG 1.0, the
216-color web-safe palette, and the era's font stacks and fixed-width layout practice. The cap is
on convention, not implementation, so an `oklch()` ground, a logical property or a cascade layer is
judged only by what it draws.

## The window

Nine payload commits, all inside one day. The record is frozen, so nothing here is "the field moved
past a decision": the two findings are payload drift and a stale count.

- v2.1.0 through v2.3.0 reset the palette to the 1990s register and landed the 1996 document shell.
- v2.4.0 pulled the payload back to the 1996 register; v2.5.0 fenced the tables and boxed the index.
- v2.6.0 squared the form controls and thickened the table fence.
- **Uncommitted delta:** the table frame moved from `border-collapse: collapse` at 2px to
  `border-collapse: separate` with `border-spacing: 2px`, giving the period doubled line.
  `NOTES.md` (Tables) records it and `.github/script-probe.py` asserts it
  (`table-borders-separate`, `table-fence-thin`), so it is a settled decision carried out, not drift.
  `nu scripts/maintain.nu check` prints `Contract OK` on the working tree.

## Topic 1: Period palette and contrast

**Reinforces a settled decision.** The `:root` block stays the only color source, and the eleven
`palette-check.py` checks pass inside `maintain.nu check`: the dark 4.0:1 floor, light 3.2:1,
`prefers-contrast: more` 7:1 and print 4.5:1 all hold, the sRGB gamut gate passes on every parsed
token, and the data ramp stays four period categoricals. The 216-color web-safe palette is the
period yardstick for the light `--surface` `#c0c0c0` (the X11 `silver`, also a Netscape default
ground) and the light ramp. No drift.

A `color-mix` row hover, an upstream `#282a36` ground and a re-saturated accent each shipped and
went back out; `NOTES.md` (Color and the contrast budget) holds the prohibitions, and this run
found the payload obeying them.

## Topic 2: Period typography

**Reinforces a settled decision.** The body face stays Times New Roman via the pinned Tinos clone
and the code face Courier New via Cousine, both at `@fontsource/*@5.3.0`. Headings stay `em` at
weights 400 (`h1`/`h2`) and 700 (`h3`-`h6`), the two stops a 1996 desktop had, and `h5`/`h6` stay at
`--label`, not `--muted`, so no heading renders dimmer than the paragraph it introduces. `text-wrap`
and `hyphens` are absent, which is the period's own wrapping. Italics fall on the eight recorded
rules, with `h2` italic and `h3` upright. No drift.

## Topic 3: Period layout and spacing

**Reinforces a settled decision.** `--page-width: min(94vw, 66rem)` remains the single width token
shared by both layouts. The fixed-width practice of the period holds: the plain `<nav>` becomes the
left rail above 1000px, square corners throughout (`--radius` is `0`), and the table fence is now
the period doubled line (a table border and a cell border 2px apart) rather than a thicker single
rule. `NOTES.md` (Tables) records that decision and its two prohibitions. No drift.

## Topic 4: Accessibility under WCAG 1.0

WCAG 1.0 (W3C Recommendation, 5 May 1999) is the only accessibility document this run cites. WCAG
2.x, WCAG 3.0, ISO/IEC 40500 and EN 301 549 each post-date the period and are not used as criteria.

### Violation of a settled decision: the inert margin toggle is visible and focusable

**New ground, and a violation, so it is in the patch.** `NOTES.md` (Keyboard and assistive
technology) states the sidenote `input.margin-toggle` "is inert by design, and its `display: none`
rules must stay". The sheet declares `input.margin-toggle { display: none; }`, but the form-control
reset added later declares `input[type="checkbox"], input[type="radio"] { display: inline-grid; … }`
at the same specificity (`0,1,1`) and later in source order. The reset therefore wins, and the
hidden control is repainted as a visible 16x16 square.

Rendered evidence (`samples/dark.html`):

| | `input.margin-toggle` elements | Visible | In the tab order |
| --- | --- | --- | --- |
| HEAD, before the patch | 5 | 5 | 5 |
| HEAD, after the patch | 5 | 0 | 0 |

A `Tab` sweep reaches three of them between the `nav.toc` links and the first content link, so the
defect costs a reader four dead focus stops on top of the stray checkboxes on the page. The fix
excludes the class from the reset (`input[type="checkbox"]:not(.margin-toggle)`), which keeps the
hide rule where the sidenote logic lives and needs no specificity bump. `NOTES.md` gains the
decision and its prohibition.

### The WCAG 1.0 Priority 1 and 2 sweep

| Checkpoint | Priority | Result |
| --- | --- | --- |
| 1.1 Text equivalent for non-text elements | 1 | Pass. Every decorative `::before`/`::after` glyph carries the `content: "…" / ""` twin behind `@supports`; `accTitle`/`accDescr` are a `CONTRACT.md` § 2 consumer obligation; the `.icon-chip` glyph is `aria-hidden`. |
| 2.1 Color is not the only cue | 1 | Pass. `.verdict`/`.verified`/`.unverified`/`.correction` spell their state in text. |
| 3.1 Markup over images for information | 2 | Pass. No image-based headings; all headings are text. |
| 3.2 Valid to published grammars | 2 | Pass. `nu scripts/maintain.nu check` holds exactly one `<style>` and one `<script>` per fixture and the markup parses; `<html lang="en">` is present. |
| 3.3 Style sheets for presentation | 2 | Pass. Both layout and the table fence live in the inlined sheet. The `align` attribute appears only in generated pipe tables; see the note below. |
| 3.4 Relative units | 2 | Pass. `--page-width` and the type scale are `rem`/`em`/`vw`; the recorded exception is the `.num`/`[align="right"]` right-alignment, not a unit. |
| 3.5 Header elements convey structure | 2 | Pass. The fixture opens `h1 h2 h3 h4 h5 h6` in order. |
| 3.6 Proper list markup | 2 | Pass. `ul`/`ol`/`dl.timeline`; `.nav-list`/`.icon-list` carry `role="list"` per `CONTRACT.md` § 2. |
| 3.7 Mark up quotations | 2 | Pass. `blockquote` and `cite` are used for quoted copy; none for indentation. |
| 5.1 Data tables identify headers | 1 | Pass. Every `th` in the fixture carries `scope="col"` (18 instances). |
| 5.2 Two-level header association | 1 | Pass. `table.tree` associates the depth header through markup, not presentation. |
| 5.3 No layout tables | 2 | Pass. No fixture uses a table for layout; `table.bar-chart` is data. |
| 6.1 Readable without style sheets | 1 | Pass. DOM order is visual order; `body.conn-map` no longer reorders with `order`, and both sections read top to bottom unstyled. |
| 6.3 Usable with scripts off | 1 | Pass. The zoom control is absent without script and the diagram source stays readable; `filter.js` degrades to a plain input. |
| 6.4 Input-device-independent handlers | 1 | Pass. Zoom is a real `<button>` (keyboard and pointer); the filter is a native input; the overlay is a native `<dialog>` closed by `Escape`. |
| 11.1 Avoid deprecated features | 2 | Pass with a recorded deviation. No `font`, `center`, `applet`, `frame` or `bgcolor`. The `align` attribute on generated pipe-table cells is deprecated in HTML 4.01, and it is a deliberate support decision (`NOTES.md`, Markdown coverage). |
| 12.4 Explicit label association | 2 | Pass. The filter `label` binds to `input.filter-box` by `for`. |
| 13.1 Identify each link's target | 2 | Pass. No bare "click here"; the sheet carries no outbound-link glyph at all. |
| 13.4 Consistent navigation | 2 | Pass. `nav.toc` and the nav groups keep a stable relative order. |

Manually driven in headless Chromium on `samples/dark.html`, `800x600`: `Tab` and `Shift+Tab`
traverse the toc, the controls and the content in DOM order; `Enter` opens `details.deep` and
`Escape` closes the zoom `<dialog>`; `Space` collapses the `details`; the focus ring is a visible
2px outline on the filter box.

Not applicable to this static template, with reason: 1.2-1.4 and 9.1 (no image maps or multimedia),
4.x (no language changes), 6.2 and 6.5 (no applets), 7.x (no motion to flicker), 10.x (no
standalone `select`-driven form), 12.1-12.3 (no frames), 13.2-13.3 (no sitemap or search engine).
Priority 3 candidates tracked separately, not scored as conformance: 5.5 (summary rows), 9.5
(header grouping), 10.5 (adjacent link separation).

## Topic 5: Period interaction and motion

**Reinforces a settled decision.** Every hover rule sits inside `@media (hover: hover)` (nine rules,
one block), so no affordance sticks on a tap. The sheet declares no `transition`, no `@keyframes`
and no `:active` scale, which is the period's static behaviour. The decorative overlay close mark
`✕` carries its alt-text twin. No drift.

## Topic 6: Pinned dependencies

**New ground, recommendation only, out of the patch.** Every CDN reference is pinned to an exact
version: `@fontsource/cousine@5.3.0`, `@fontsource/tinos@5.3.0`, and
`mermaid@12.0.0/dist/mermaid.esm.min.mjs`. Mermaid **12.1.0** shipped on 2026-10-02, three days
before this run, with ELK feedback-edge orientation, a shared path-based edge-label resolver that
separates overlapping ELK edge labels, and `packet` bit-order support. The edge-label work touches
this template's own `CONTRACT.md` § 2 note that a label outside its viewBox stays unreachable, so it
is worth evaluating.

The patch does not carry the bump: a runtime dependency change needs its own render and its own
verification across the twelve diagram types, and the repo pins deliberately. Recorded here as a
recommendation for the maintainer to schedule, not as an unapplied fix.

## Topic 7: New period references

Seven references were added since the last payload commit (`52013f5`): `active-worlds-1998`,
`dell-1996`, `las-vegas-1998`, `loreal-cosmetics-1998`, `lycos-1998`, `playstation-1998`,
`the-history-channel-1998`. Each has its sibling `.txt` with the four fixed sections, so no entry is
missing its analysis.

All seven `[RELEVANCE]` lines read "nothing transferable" or "nothing new", and each names an
existing repo decision rather than new period ground:

- `active-worlds-1998`: the bracketed `nav > a` form the repo already draws.
- `dell-1996`: the "bar heads a row" motif, already on the grouped lists and tables.
- `las-vegas-1998`: the `nav-list`/recent-group form and the fenced table.
- `loreal-cosmetics-1998`: an image-led layout far from a text template.
- `lycos-1998`: the `nav-group`/`.toc-label` motif and the fenced table.
- `playstation-1998`: reinforces `h2.band` (yellow heading on red) and the tab list.
- `the-history-channel-1998`: reinforces `.icon-list`/`.edge-list` and the heading rule.

**No new ground.** The corpus adds reinforcement, not a new decision to adopt.

## Period viewport sweep

Rendered with mermaid hydrated (`networkidle`), because a raw `<pre class="mermaid">` source text is
wide until Mermaid renders and would read as transient overflow that is not real.

| Fixture | 640x480 | 800x600 | 1024x768 |
| --- | --- | --- | --- |
| `samples/dark.html` | sw 640 / cw 640 | 800 / 800 | 1024 / 1024 |
| `samples/dark-conn-map.html` | 640 / 640 | 800 / 800 | 1024 / 1024 |
| `samples/dark-timeline.html` | 640 / 640 | 800 / 800 | 1024 / 1024 |
| `samples/dark-charts.html` | 640 / 640 | 800 / 800 | 1024 / 1024 |
| `samples/light.html` | 640 / 640 | 800 / 800 | 1024 / 1024 |

No page-level horizontal scrolling at any period resolution. The fixed-width layout holds at each
size, and the heading order and type scale read as settled. The template implements no loading,
error or empty state, so that check is not applicable; it is reported rather than invented.

## Standards mapping

| Document | Date | Use in this run |
| --- | --- | --- |
| HTML 3.2 | 14 January 1997 | Period grammar context |
| HTML 4.0 / 4.01 | 18 December 1997 / 24 December 1999 | Deprecated-feature check (11.1), `align` deviation |
| CSS1 | 17 December 1996 | Period presentation model |
| CSS2 | 12 May 1998 | Period layout and the doubled table frame |
| WCAG 1.0 | 5 May 1999 | The accessibility sweep above |
| Web-safe palette | 216 colors | Light `--surface` `#c0c0c0` and the light data ramp |

This is a standards mapping, not a claim of legal compliance.

## Out of scope

`NOTES.md` sections outside the topic map (Filter, Unclaimed elements, Markdown coverage, Raw HTML
and other generators, Repo layout, Odds and ends) were not audited by topic. That is a scoping
decision, not an oversight. The stale-count fix below did read Markdown coverage and Document shell
before it was written, as the skill requires for a section outside its topic's map.

## Prose rules that no check enforces

- No em-dash or en-dash anywhere: `maintain.nu check` passes the dash gate over `git ls-files`, and
  this report's own lines are dash-free.
- No comment in an inlined file: `dracula-nineties.css` carries only the line-2 version stamp and the
  `/* was #rrggbb */` notes; `mermaid.js` carries none (its only `//` is inside the CDN URL).
- No physical sides outside the documented float fallback; no deprecated markup in the payload.

## Finding outside the patch: stale reference count

`NOTES.md` stated "42 references" twice (Document shell, at line 196, and Links, at line 503). The
corpus now holds 49, because commit `52013f5` added seven. `AGENTS.md` already dropped its own "42
files" and `README.md` its "two Claude Code skills" earlier in this session; `NOTES.md` was the
remaining instance. The patch removes the frozen number rather than asserting a new one, so the
qualitative claim ("about 20 carry a left link rail") survives without a brittle denominator.

## Patch

`review/2026-10-05-design-audit.patch` (source files only, against `HEAD`):

- `dracula-nineties.css`: `input[type="checkbox"]` in the reset becomes
  `input[type="checkbox"]:not(.margin-toggle)`, so the inert margin toggle stays `display: none`.
- `NOTES.md`: a Form controls bullet records the decision and its prohibition; the two stale
  reference counts drop the frozen number.

**Verification verdict: Verified.** Applied in a throwaway worktree
(`git worktree add --detach /tmp/da-verify HEAD`), the patch applied clean, `nu
scripts/build-sample.nu` regenerated every fixture, and `nu scripts/maintain.nu check` printed
`Contract OK` (19 palette tokens, 12 mode renders, 38 script-probe assertions, no dashes). The probe
render after the patch shows zero visible margin-toggle controls at 640x480, 800x600 and 1024x768,
with no page overflow.

## Applied

The maintainer applied both patch findings and took the Topic 6 recommendation on 2026-10-05.

- The two source edits are in the tree: the checkbox reset excludes `.margin-toggle`, and the two
  stale reference counts drop the frozen number.
- The Mermaid pin moved from `12.0.0` to `12.1.0` in `mermaid.js`. Verified by render: no console
  error on `dark.html`, `dark-charts.html` or `dark-conn-map.html`, the palette reaches the
  diagram nodes, no page overflow at 800px, and `maintain.nu check` prints `Contract OK`.
- A new `.github/script-probe.py` assertion, `control-margin-toggle-hidden`, gates the fix. It was
  mutate-tested: reverting the CSS and regenerating the fixture makes it fail, restoring it makes
  it pass. The binding half now reports 39 assertions.

## Searched

- Topic 4: "WCAG 1.0 W3C Recommendation 5 May 1999 checkpoint 1.1 priority 1 guidelines list".
- Topic 6: "mermaid latest version release 12 changelog npm".

Topics 1, 2, 3, 5 and 7 rest on the frozen period record and the repo's own gates, so no search was
run for them.
