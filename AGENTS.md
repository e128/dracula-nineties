# AGENTS.md: Dracula-Nineties template

Instructions for any agent that works in this repo, whichever harness runs it. These instructions
override default behavior.

**This file is the whole contract for agent behavior here, and the only instruction file in the
repo.** Everything it asks for is a shell command, a file path, or a decision rule. A harness may
wrap a flow below behind a command, a skill or a slash command of its own. Such a wrapper adds an
entry point. **It never adds, relaxes or overrides a rule stated here.** If one appears to, this
file wins. The wrappers that exist, and the rules that bind them, are listed under
[Harness entry points](#harness-entry-points) near the end. Nothing outside this file is required
reading, and **a second instruction file beside this one is a regression**: see that section.

## Read [NOTES.md](NOTES.md) first

**Before you change `dracula-nineties.css` or `mermaid.js`, read [NOTES.md](NOTES.md).** It holds
the reasoning that used to live in those files as comments. It records every current decision,
every rejected alternative, and every prohibition this repo already paid for.

**NOTES.md states decisions, not measurements.** Every number behind an entry was measured in
Chromium, and those measurements live in git history and in the gates. `.github/palette-check.py`
and `.github/render-modes.py` enforce the color and mode claims, so a number that matters is a
check rather than a paragraph. **Do not add measurement narration back to NOTES.md**, and do not
write a version history into it: `CONTRACT.md` § 3 owns per-release deltas and `git blame` owns
the rest.

This is not optional background. Several changes in this repo's history were correct on paper,
shipped, and then went back out: a monospace table stack, a `color-mix` row-hover fill, and two dead
`themeVariable` declarations. Every "do not" in NOTES.md is one of those. The file exists so that
nobody covers the same ground twice.

You may want to fix something that looks wrong: a heading heavier than its parent, or an inert
`themeVariable`. **NOTES.md probably records it already.** Check NOTES.md before you touch the CSS.
If you still disagree, re-measure and say so directly. Do not reverse a documented decision in
silence.

When you make a new decision worth keeping, add it to NOTES.md as a decision plus its
prohibition. Do not add it to the stylesheet, and do not append it as a story about what changed.

## Writing rules

**No em-dash and no en-dash anywhere in this repo.** Not in prose, not in a heading, not in a
table cell, not in a code comment, not in a runtime `print` string, not in fixture copy, and not
in a commit message or a PR body. The two characters are U+2014 EM DASH and U+2013 EN DASH, and
the count is zero. This paragraph names them by codepoint rather than printing them, because the
gate below scans every tracked file and would otherwise fail on the rule that states it.

Use whatever the sentence actually needs instead:

- A period, when the two halves are two sentences. This is right most of the time.
- A comma or a conjunction, when the second half qualifies the first.
- A colon, when the second half names or expands the first.
- Parentheses, when a pair of dashes was fencing an aside.
- A plain hyphen `-`, for compound words, numeric ranges (`200-900`, `h1`-`h6`), and aligned
  key-to-description lines where a colon would break the column.

`nu scripts/maintain.nu check` and the `contract` workflow both fail on any occurrence, and
`nu scripts/maintain.nu bump` refuses to stamp a version while one is present, so this is gated
rather than trusted. The commit-subject convention is `feat: vX.Y.Z - <summary>` with a hyphen.
Commits in history keep the old em-dash form. No rewrite changes them.

The rule exists because 186 em-dashes across 22 files read as one voice tic rather than as
punctuation, and because a gate is the only thing that keeps a prose rule alive in a repo where
most edits are made by an agent.

## NEVER write comments in files that get inlined into HTML

Every generated HTML file carries a verbatim copy of `dracula-nineties.css` and `mermaid.js`. A
comment here is not written once. Every page a consumer renders carries a copy of it, forever.

**Rules:**

- **Do not add comments to `dracula-nineties.css` or `mermaid.js`.** No block comments, no
  end-of-line comments, and no single line that explains a magic number.
- The same rule covers any future file that a consumer inlines instead of links. If a consumer
  copies the file into output, the file carries no comments.
- `mermaid-palette.json` already has `_comment` keys. Do not add more.
- **Two exceptions exist. A machine reads both. Do not remove them:**
  - **Line 2 of `dracula-nineties.css`** must be a comment that holds the template version, in the
    form `/* Dracula-Nineties vMAJOR.MINOR.PATCH */`. `scripts/build-sample.nu` parses it out of
    `lines | get 1` to stamp `tokens.css`, and `scripts/maintain.nu bump` rewrites it. If you remove it,
    regeneration dies with `index too large (empty content)`. That failure is *silent* when you
    pipe the output, and it leaves stale fixtures that look correct.
  - **The `/* was #rrggbb */` notes on the `:root` tokens that are exact upstream hexes.** Check 3
    of `.github/palette-check.py` parses them, and the check fails when a stated hex disagrees with
    its `oklch()`. If you delete a note, you disable that gate in silence. Match the exact format
    when you add a token. The notes cover every token with a real sRGB hex behind it (the Dracula
    and Alucard accents, the grounds, the data ramp); `--purple-bright`, the rule tokens and the
    alpha or relative forms carry none, because no single hex states them. See NOTES.md, Color and
    the contrast budget.
- The Nushell scripts (`scripts/build-sample.nu`, `scripts/maintain.nu`), `README.md`, `backlog.md`
  and `AGENTS.md` are **not** inlined. Comment those files as normal.

**Put the reasoning in one of these places instead**, in order of preference:

1. **[NOTES.md](NOTES.md)**, the durable home for the reason a declaration looks the way it
   does. It holds measurements, rejected alternatives, and settled decisions. A future agent
   reads this file instead of the comments.
2. **The commit message**, for the story of a single change.
3. **`backlog.md`**, for open decisions and deferred work.
4. **`README.md`**, for anything a consumer needs to know.

Never delete a load-bearing explanation. Move it to NOTES.md.

## Regeneration and the contract

- `scripts/build-sample.nu` generates `samples/dark.html`, `samples/dark-conn-map.html` and `tokens.css`. Never edit
  them by hand. Change `dracula-nineties.css`, `mermaid.js` or `scripts/build-sample.nu`, then regenerate.
- Run `nu scripts/maintain.nu check` after every change. It mirrors CI: file presence, the palette
  hex-against-oklch gate, exactly one `<style>` and one `<script>` per fixture, and a staleness
  check that proves regeneration changes nothing. It must print `Contract OK`.
- The first line of `dracula-nineties.css` must be exactly `  <style>`. The last line must be
  exactly `  </style>`. Consumers slice the body out with `sed '1d;$d'`. This is a contract.
- `dracula-nineties.css` carries its own `<style>` wrapper, and `mermaid.js` carries its own
  `<script>` wrapper. Do not add a second wrapper.
- **Never cite a line number into a generated file.** Any document that points at
  `samples/`, `tokens.css` or any other generated artifact points at a **string to search for**,
  never at a line. A fixture is rewritten on every payload edit, so a line number rots on a change
  that has nothing to do with what it names. `CONTRACT.md` § 2 carried 22 such references and every
  one of them was wrong, undetected, for twelve releases. The form is
  ``(in `samples/dark.html`, search `class="tag-dot"`)`` and `nu scripts/maintain.nu check` parses
  and resolves every one of them.
- **A gate that cannot reach its subject does not get written.** Say so in `NOTES.md` and leave the
  obligation in prose. A check that skips the only instance it could test reports green about a
  question it never asked, which is worse than the honest gap. This is why the `quadrantChart`
  label length is prose and the `.step-node` accent is gated.

## A tag claims that the contract held. Verify the claim, never assume it

Consumers pin to a tag through a git submodule. A tag on a commit that CI never checked hands
every consumer a payload that nothing verified. The fixtures and `tokens.css` are generated, so
a stale or broken one looks completely normal.

**Only a pull request can satisfy a required status check.** `main` requires the `contract`
check (`strict: true`, `enforce_admins: false`, no review requirement). The check runs *after* a
push, so a direct `git push origin main` can never satisfy it. GitHub accepts the push and
records `Bypassed rule violations`. Two separate pushes, one for the commit and one for the tag,
do not fix this. Only a merged pull request does. **Never commit straight to `main`.**

The flow, start to finish. Run it as written, whatever else your harness offers on top of it:

```
git switch -c fix/whatever                  # never work on main
nu scripts/maintain.nu bump 1.11.0          # stamps the CSS + README
git add -A && git commit -m 'fix: v1.11.0 - <summary>'
git push -u origin fix/whatever
gh pr create --fill && gh pr checks --watch # `contract` must pass here
gh pr merge --squash                        # the merge is what the check gates
git switch main && git pull
nu scripts/maintain.nu release 1.11.0       # verifies, then tags
```

`nu scripts/maintain.nu release <version>` does **not** push a branch. It refuses a dirty tree. It
refuses a version that the stylesheet does not carry. It refuses a tag that already exists. It
refuses a `HEAD` that is not already `origin/main`, and that last refusal is what proves the
commit arrived through the gate instead of around it. It then polls the check runs for that
exact SHA, and it writes the tag only when every check named in `REQUIRED_CHECKS` concludes
`success`. A missing required check counts as a failure, because a commit that CI never saw is
the thing this gate exists to refuse. The tag is **annotated**, so `git tag -v` has an object to
read.

**A release also publishes three assets**, and a tag without them is an incomplete release: the
Rider plugin zip, the VS Code vsix, and the themes zip. `scripts/create-themes.nu` builds them.
Check an existing release with `gh release view v<version>` before assuming it shipped whole.

**Only the required checks gate the tag. The rest are advisory.** GitHub attaches a check run
for every workflow that a commit fires, including the workflows GitHub generates itself.
`pages-build-deployment` alone contributes `build`, `deploy` and `report-build-status`. None of
them say anything about the payload. A gate on *every* check once held a tag for a full timeout
because a Pages deploy stalled on GitHub's side, and then refused the tag outright, because a
non-success conclusion stays attached to that SHA. `REQUIRED_CHECKS` near the top of
`scripts/maintain.nu` is the list. Keep it in step with the required checks configured on `main`,
and add to that list rather than widen the gate back to every check.

**Rules that have no exception:**

- **Never run `git push origin main v1.x.0`.** One command pushes the commit and the tag
  together, so the tag claims that the contract held before anything checked it.
- **Never tag a commit that is not `origin/main`,** and never tag a commit where a required
  check is absent. Absent is not passing.
- **Never use `--no-verify`, and never force-push a tag that you already pushed.** A moved tag
  changes what every pinned consumer resolves to, and it does so in silence.
- **If a push reports `Bypassed rule violations`, stop and say so in that same message.** The
  report means that something overrode the protection instead of satisfying it. Do not bury it,
  and do not continue to the tag. Offer to revert.

A release faces outward and is hard to reverse. Confirm before you tag or push, unless the
request was explicitly to release.

## Constraints that shape every decision

- **No build step.** Consumers inline two files verbatim. Anything that needs compilation,
  bundling, or a preprocessor is out of scope.
- **Output renders locally, and often offline.** A CDN dependency must degrade well: the webfont
  falls back to a system serif and the text still renders. Mermaid is the existing exception,
  and it fails hard offline.
- **Mermaid colors must be hex, never `oklch()`.** Its color engine (khroma) throws
  "Unsupported color format" on an `oklch()` string and aborts init, so no diagram renders. It never
  resolves a `var()` either, so `mermaid.js` carries **two** hex palettes and picks one at init by
  reading the `--mermaid-scheme` token off `:root`. Read the token, never `matchMedia`: the
  forced-light sample pages rewrite an `@media` condition, which the cascade sees and `matchMedia`
  does not. `mermaid-palette.json` holds both sets as `init` and `initLight`, and
  `.github/palette-check.py` keeps both honest against the oklch source.
- Pin every CDN dependency to an exact version, never to a range.

## Verify a rendered claim by rendering it

**A layout or contrast claim about this stylesheet is not verified until a browser has drawn it.**
The repo already drives headless Chromium in `.github/render-modes.py`, and Playwright is the
convention for anything more interactive. Three plausible fixes once seemed correct from arithmetic
alone. All three were wrong. SVG ink outside a root `<svg>` does not create scrollable overflow for
any CSS ancestor. No `overflow` value recovers it. The zoom overlay does not fix an escaping
viewBox at narrow widths. It scales the overrun with the diagram. Alpha compositing must use
gamma-encoded sRGB, not linear. Otherwise, a contrast ratio reads several tenths too bright.

**When a claim rests on a mitigation, test the mitigation too, not just the defect.**

**A behavioural claim about `mermaid.js` or `filter.js` is not verified until the script has run.**
`.github/script-probe.py` drives both of them in the real fixture through the same headless Chrome.
Add an assertion there when you change either file, and mutate the change to confirm the assertion
fails without it. Every other check in this repo reads the payload. This is the only check that runs it. The probe exists because the fixture shipped an inert `input.filter-box` for six releases and a diagram nobody could click for several more. Other checks missed both defects.

**Re-price a decline before you repeat it.** Three entries sat in `backlog.md` for releases on
costs that were simply wrong: a jsdom dependency the repo did not need, a resize listener a media
query replaces, and an `!important` that two real `themeVariables` made unnecessary. A recorded
decline is a cost estimate with a date on it, not a verdict.

## Design Audit Evidence

Every design audit reports on period fidelity: whether the drawn design still matches the standards
of 1994 through 1999, and whether the payload has drifted from a decision NOTES.md records. For each
check, report measured results, limits, and missing inputs. Never report an unrun check as a pass.
**The audit's design vocabulary stops at 1999.** Judge the design against the period record: HTML
3.2 (14 January 1997), HTML 4.0 (18 December 1997) and HTML 4.01 (24 December 1999), CSS1 (17
December 1996), CSS2 (12 May 1998), WCAG 1.0 (5 May 1999), the 216-color web-safe palette, and the
era's font stacks and fixed-width layout practice. Do not import a post-1999 standard as the
yardstick.

The cap is on design convention, not on CSS implementation. The payload renders in a modern browser
and may use a modern property to reach a period result; NOTES.md records those decisions. An audit
does not propose replacing them, and does not propose a modern design idiom. Update this file and
the skill only through a separate maintainer-authorized change.

### Period Fidelity

- Render representative fixtures at the period's canonical resolutions: 640x480, 800x600 and
  1024x768. Measure page-level horizontal overflow with `scrollWidth` and `clientWidth`, and
  identify any overflow inside a documented scroll hatch. Check flex and grid stacking against
  DOM order.
- Check the settled fixed-width layout (NOTES.md, Width and measure), the type scale and the
  heading decisions at each resolution. Report the visual result, not the arithmetic.
- Review the `inspiration/` entries added since the previous audit. A new reference is the one
  input that can introduce a design consideration the earlier runs did not weigh. Name each added
  entry and what it teaches the template, or say it teaches nothing.
- Report the period standards the run checked against, with each document and its date.
- Test each implemented loading, error, and empty state. Confirm that critical actions remain
  reachable. If a state does not exist, report it as not applicable and do not invent one.

### Accessibility Checks

Run a WCAG 1.0 sweep, the period's accessibility standard (W3C Recommendation, 5 May 1999). Check
the [W3C TR record](https://www.w3.org/TR/) for the Recommendation date and its checkpoint list.
Report the Priority 1 and Priority 2 checkpoints that apply to a static, no-build CSS and
vanilla-JS template, and mark a checkpoint that needs absent content not applicable with a reason.
Do not import WCAG 2.x, WCAG 3.0, ISO/IEC 40500, EN 301 549, or any later document as a criterion:
each post-dates the period. Report standards mapping only. Do not claim legal compliance.

Do not send non-public content to an external service without user authorization.

Test keyboard navigation by hand. Check Tab, Shift+Tab, Enter, Space, and Escape where relevant.
Confirm visible focus for each interactive element in each appearance mode. Automated results, when
available, supplement the manual checks, the palette gate, and the rendered contrast checks.

### Period Technique Review

Check the drawn result against the period repertoire: fixed-width columns, web-safe or
dithered-safe grounds, the era font stacks (Georgia, Verdana, Trebuchet MS, Courier, Times),
visible link states, and rule or bevel ornament in the period vocabulary. Look for a modern default
that arrived after 1999 and changes the look: a system-UI sans stack, flat neutral chrome, or a
generated modern widget. Record each as a candidate and check NOTES.md before proposing an addition.

## Inspiration analysis

`inspiration/` holds reference screenshots of period pages, and each image gets a sibling `.txt`
beside it with the same stem. Every file carries a header block and four marked sections in a
fixed order: `[PALETTE]`, `[LAYOUT]`, `[META]`, `[RELEVANCE]`. The point of the fixed order is
that the files stay comparable, so do not reorder, rename or drop a section.

The header block carries `site`, `period`, `dimensions` and `sampled` (the date the analysis was
written, `YYYY-MM-DD`). `[PALETTE]` lists role colors as `name  #rrggbb  role: <role>  <short hue
description>`, sampled from the pixels rather than guessed. `[LAYOUT]` and `[META]` run two to
four full sentences each, and `[META]` is the holistic read of the design rather than a summary
of the other two. `[RELEVANCE]` is one line on what the page contributes to this template, or
that it contributes nothing.

Per image, the flow is shell plus model work:

    magick identify -format "%f %wx%h\n" inspiration/<name>.png            # dimensions
    magick inspiration/<name>.png -colors 12 -format %c histogram:info:-   # role colors
    # then read the image and write the four sections

**These files are tracked, so the no-dash rule and every other prose rule apply to them.** A
re-run skips an image that already has a `.txt`; `--force` overwrites it, because a silent skip
leaves a stale file that still looks current. Say which images were skipped.

## Harness entry points

**Every rule in this file reaches every harness through this one file, and nothing in this section
adds a rule.** A harness that ships wrappers, config or skills gets them listed here, so that an
agent which opens `.claude/` can tell an entry point from a rule. **These names exist for
orientation only. Delete `.claude/` and this repo still works exactly as written above.**

### Claude Code

Claude Code reads `AGENTS.md` directly from v2.1.277 on, with no `CLAUDE.md` beside it. Three
skills live in `.claude/skills/`, and they are available to Claude Code only. Each one packages a
flow that this file states in full as plain shell, so a harness without skills loses an entry
point and no capability.

| Skill | Wraps | Invoked by |
| --- | --- | --- |
| [`release`](.claude/skills/release/SKILL.md) | Release flow and three published assets | "release", "cut", "tag", or version |
| [`design-audit`](.claude/skills/design-audit/SKILL.md) | Audits payload changes against NOTES.md and the design standards of 1994 through 1999 (HTML 3.2, HTML 4.0, CSS1, CSS2, WCAG 1.0, the web-safe palette). Reviews new `inspiration/` references, renders changed components, and writes a dated report with unapplied patch to `review/`. Never edits the payload | "design audit", "period fidelity", "review the references", `/design-audit` |
| [`inspiration-analyze`](.claude/skills/inspiration-analyze/SKILL.md) | Writes the per-image `.txt` analysis beside each `inspiration/` screenshot, in the fixed four-section template above | "analyze inspiration", "analyze the reference pages", `/inspiration-analyze` |

**None of these skills is required to do the work.** `release` is the order in which to call
`scripts/maintain.nu`, and every one of those commands appears above. `design-audit` produces a
report a person reads, and `review/` holds the prior ones as precedent whatever wrote them.

### Rules that bind a harness, its skills and its config

- **A skill, or any bundled design skill, is not authority over a settled decision.** *Style
  decisions that are already settled* is the authority. A skill's finding does not reverse an entry
  there: report it to a person and let them decide.
- **A skill may only wrap a flow this file states in full, and may not restate it as its own.** Do
  not let a rule come to rest only inside a skill: a harness without skills must lose an entry
  point, never a rule. If a skill's instructions and this file disagree, this file is right and the
  skill is a bug.
- **No skill edits `dracula-nineties.css` or `mermaid.js` without a render.** *Verify a rendered claim
  by rendering it* applies to skill-driven edits exactly as it does to direct ones.
- **`.claude/settings.json` configures the status line and nothing about the payload.** Do not put
  repo policy there. Policy goes in this file, where every harness can read it.
- **A second instruction file beside this one is a regression.** Claude Code's default
  `claude-md-or-agents-md` setting loads a `CLAUDE.md` and then **skips `AGENTS.md` altogether**, so
  a pointer file does not accompany this contract, it replaces it. Do not add one, do not leave a
  stale one, and do not symlink one.

## Style decisions that are already settled

Do not "fix" these decisions. Each one is deliberate, and this repo re-litigated each one at
least once. [NOTES.md](NOTES.md) holds the failed alternatives for each.

- **Headings use `em`**, so they track the body clamp instead of the fixed root.
- **`h1` and `h2` sit at weight 400.** They are large enough to carry it. Nothing at text size
  may be lighter than body copy.
- **`h3` through `h6` sit at `--label`.** Not `--muted`, which would render a heading dimmer
  than the paragraph it introduces.
- **Page width is one token.** `--page-width` in `:root` serves both layouts, so the two layouts
  cannot drift. A change there is a layout change for every consumer page.
