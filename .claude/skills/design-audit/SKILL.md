---
name: design-audit
description: Periodic period-fidelity review for the Dracula-Nineties template. Audits payload changes against NOTES.md and the design standards of 1994 through 1999 (HTML 3.2, HTML 4.0, CSS1, CSS2, WCAG 1.0, the web-safe palette, and the era's font stacks and fixed-width layout practice). Reviews the inspiration/ references added since the last run, renders new or changed components, and writes a dated report and unapplied patch to review/. Never edits the payload. Use for design audits, period-fidelity reviews, reference reviews, and refresh reviews.
---

# Design audit: period fidelity, 1994 through 1999

This is a research-and-report skill, not an implementation skill. It never edits
`dracula-nineties.css`, `mermaid.js`, or any generated file in the working tree. It never runs
`scripts/maintain.nu bump` or opens a PR. It produces two files under `review/` for the
maintainer to read and decide on. Manual invocation only: nothing schedules this.

**Why this exists:** the maintainer is not strong in CSS and layout, and wants a periodic
check that this repo's hand-tuned decisions still match the design standard the template
deliberately recreates, backed by real sources rather than a model's unstated priors.

## The cap: what this audit may and may not know

**This audit judges the design against 1994 through 1999, and against nothing later.** The
template recreates the look of period pages, so a convention that arrived after 1999 is not
an improvement to propose when it changes how the page looks. The audit's design vocabulary
stops at 1999.

**The cap is on design convention, not on CSS implementation.** The payload renders in a
modern browser and may use a modern property to reach a period result. Logical properties,
an `oklch()` ground, or a cascade layer are implementation, and NOTES.md records those
decisions. The audit does not propose replacing them. It asks only whether the drawn result
reads as 1994 to 1999. **Do not gut a modern implementation detail that NOTES.md settled, and
do not propose a modern design idiom.**

**Out of scope, so no run re-raises any of it:** Core Web Vitals and field-performance
measurement, the Baseline feature tiers, mobile-first and responsive layout as a design goal,
target-size minima, `prefers-reduced-motion` and other post-1999 media features as design
requirements, dark mode as an operating-system preference, and every post-1999 accessibility
and standards document. The period yardsticks are listed under *Period standards* below.

**Two kinds of finding come out of a run, and the second one matters more.** The period
record is frozen: HTML 3.2, CSS1 and the rest do not change, so "the field moved past a
settled decision" almost never happens. The payload drifting away from a decision NOTES.md
already records is common and fast, because most edits here are made by an agent that did not
read NOTES.md first. A newly added `inspiration/` reference is the third source, and the only
one that can introduce new period ground. Step 2, Step 4 and Topic 7 exist for the drift and
reference kinds.

## Step 1: load the decision set, the last audit, and the corpus

Four reads, in this order, before anything else.

1. **`AGENTS.md`, whole.** Short, and every constraint the patch must obey lives there. Its
   *Design Audit Evidence* section states what this audit reports.
2. **`NOTES.md`, the `## Contents` table only.** That table names every section and what
   each one covers. Read it whole so nothing in the file is invisible to this run. Read
   individual sections in Step 3, scoped by the topic map, not up front. If a finding
   turns out to touch a section outside its topic's map, read that section before writing
   the finding up. Never write a finding against a section this run has not read.
3. **The newest `review/*-design-audit.md`, if one exists,** plus `review/declined.md`.
   `ls review/*-design-audit.md | sort | tail -1` gives the file. **Read its header for the
   commit SHA it audited, not just its date.** Step 2 needs the SHA.
4. **The `inspiration/` inventory.** `ls inspiration/*.png` and `ls inspiration/*.txt`. Note
   the newest entries by commit, because Topic 7 reviews the ones added since the last audit.

Do not rely on partial recall from a prior turn in this conversation. Re-read the files
fresh, since they may have changed since any memory of them was formed.

### What the previous audit is for

A periodic skill that starts blind every time reports the same list every time, and the
maintainer stops reading it by the third run. The previous report changes this run in four
ways:

- **It anchors the window on a commit, not on a date.** See Step 2.
- **It classifies repeats.** A finding already in the last report, with nothing new behind
  it, is marked `Repeat, unchanged since YYYY-MM-DD` in one line. Do not re-argue it, do
  not re-cite it, and do not put it in the patch again.
- **It respects declines.** `review/declined.md` is the ledger of findings the maintainer
  looked at and said no to. NOTES.md records prohibitions this repo paid for in reverted
  commits. It does not record "the audit proposed X and the maintainer declined". Without
  the ledger, the same rejected proposal returns every quarter.
- **Its own claims are re-checkable, and one of them was wrong.** See Step 2, last part.

`review/declined.md` is a single markdown table: `| Date | Topic | Finding | Reason |`. **The
file exists and may hold no rows.** An empty ledger is a real state and it means no finding
has been declined yet, not that the ledger is missing. **This skill only ever appends to it,
and only when the maintainer declines a finding in conversation.** A run never writes to it
on its own, and never removes a row.

A finding that appears in the ledger is out of scope unless a source added after the decline
backs it: a new `inspiration/` reference, or a period document the earlier run did not cite.
If one does, it is a challenge under Step 5, not an ordinary finding, and the report must
quote the ledger row alongside the NOTES.md passage.

## Step 2: audit the delta before reading the period record

**Do this before Step 3.** The topics ask what the drawn design is. This step asks what this
repo changed, and it is where the findings are.

### The window is a commit range

```bash
PREV=<the SHA named in the previous report's header>
git log --oneline "$PREV..HEAD"
git diff --stat "$PREV..HEAD"
git diff "$PREV..HEAD" -- dracula-nineties.css mermaid.js filter.js NOTES.md scripts/ .github/ 'themes/**/*.in'
git diff --name-only "$PREV..HEAD" -- inspiration/
```

If the previous report names no SHA, fall back to the tag for the version it says it read
(`git rev-list -n1 v1.44.0`), and say in the header which fallback was used. If no previous
report exists at all, the range is the last ten commits that touched the payload.

**The header states the range and the commit count, not only a date:** "since `7e67221`
(v1.44.0), six commits". A one-day window with six commits is a large delta. A two-month
window with no payload commit is nothing, and the run should say so in one line and spend
its effort on Topic 7 and on Step 4 instead.

### Every added payload line gets four questions

Read the diff, not a summary of it. For each added or changed line in `dracula-nineties.css`,
`mermaid.js`, `filter.js`, or a `themes/**/*.in` slot-map template:

1. **Does NOTES.md document it?** AGENTS.md: "When you make a new decision worth keeping,
   add it to NOTES.md as a decision plus its prohibition." A new component with no NOTES.md
   entry is a finding on its own, and the patch adds the entry.
2. **Does it obey AGENTS.md?** The comment prohibition first, since nothing gates it.
3. **Does it obey a decision NOTES.md already records?** This is the high-yield question.
   Run the Step 4 sweep against the new lines specifically, not only against the sheet as a
   whole.
4. **Does anything render it?** A selector with no fixture instance is drawn by no gate in
   this repo. NOTES.md, Print, states the principle: "A styled class with no instance is an
   untested class."

Classify these the same way Step 3 classifies topic findings, with one addition:
**`[Violation of a settled decision]`** for a payload line that contradicts a NOTES.md
passage. That is not a challenge and it never goes under the challenge heading: the decision
still stands and the code broke it, which is the opposite direction. It goes in the patch
like any other bug, and the report quotes the NOTES.md passage it broke.

### Re-check the previous report's own non-repeat claims

Any claim in the previous report that named a file, a selector, or an owner is checkable.
Check the ones this run's delta touches. On 2026-09-07 the report attributed two
`font-family: var(--sans)` declarations to a consumer's generator. The declarations already
appeared in `dracula-nineties.css`, shipped in v1.45.0 a day earlier. Under the repeat rule alone,
a wrong verdict stays wrong forever because the next run is told not to re-argue it. Correct it
in the new report and say which report it corrects.

## Step 3: run one topic at a time

Seven topics. Each is a period-fidelity question, scoped to the NOTES.md sections it owns.
The map is fixed so that coverage is stable run to run, and so the maintainer can tell which
sections an audit never looked at.

| # | Topic | Covers | NOTES.md sections |
| --- | --- | --- | --- |
| 1 | Period palette and contrast | web-safe grounds, dithered-safe values, the link and accent convention, the WCAG 1.0 contrast checkpoint | Color and the contrast budget, Appearance modes, Print, Mermaid, Editor themes |
| 2 | Period typography | era font stacks, the period type scale, italics and emphasis | Fonts, Type scale, Italics, Paragraphs and section rhythm |
| 3 | Period layout and spacing | fixed-width columns, the 640x480 and 800x600 targets, rule and spacer rhythm | Width and measure, Tables, Lists, Connections-map layout, Cascade layer |
| 4 | Accessibility under WCAG 1.0 | the Priority 1 and 2 checkpoints, keyboard reach, text equivalents | Keyboard and assistive technology, Direction, zoom and growth, Links |
| 5 | Period interaction and motion | link and rollover states, the period's limited motion vocabulary | Interaction states, Form follows role |
| 6 | Pinned dependencies | whether the pinned CDN versions have shipped fixes worth taking | Fonts, Mermaid |
| 7 | New period references | the `inspiration/` entries added since the last audit, and what each one teaches | reads `inspiration/*.txt`, no NOTES.md section |

Sections outside the map (Filter, Unclaimed elements, Markdown coverage, Raw HTML and
other generators, Repo layout, Odds and ends) are out of scope for this skill. Say so in one
line in the report so their absence reads as a decision rather than an oversight.

For each topic:

1. **Read the period record first.** The yardstick is the period document, not current
   practice. For a color question, read the web-safe palette table and NOTES.md; for type,
   the era stacks; for layout, the fixed-width practice of the period. Use WebSearch only to
   confirm a period fact (a release date, a document's contents, a browser's support), and
   cite the period document with its date. Two to four sources per topic is enough. Record
   title and URL for every source cited in the report, and list every query run under
   `### Searched` for that topic even when it returned nothing. The next run reads that
   list to avoid re-treading ground. **Scale this to the window.** When Step 2 found a
   short range and the previous report's datings are all inside their own citation
   windows, one query per topic is enough and the repeats carry forward uncited.
2. **Cite the period document and its date.** A rendering or fidelity claim is checkable
   only when it names the period source: "HTML 4.0, 18 December 1997" or "the 216-color
   web-safe palette". Do not cite a post-1999 source as the yardstick.
3. **Compare against the actual stylesheet**, not against the audit's memory of it. Read
   the relevant part of `dracula-nineties.css` and the mapped `NOTES.md` sections.
4. **Classify each candidate finding:**
   - **New ground.** NOTES.md has no decision here at all. No conflict, propose freely.
   - **Reinforces a settled decision.** The drawn result still matches what NOTES.md chose.
     Say so. A confirmed decision is worth reporting because it shows the repo has not
     drifted.
   - **Repeat.** Already in the previous report, nothing new behind it. One line.
   - **Declined.** In `review/declined.md`, no post-decline source. Drop it silently.
   - **Violation of a settled decision.** The payload contradicts NOTES.md. See Step 2.
   - **Challenges a settled decision.** The drawn result now disagrees with a NOTES.md
     entry. This is the case that needs care, see Step 5.

### Render the component, do not reason about the cascade

AGENTS.md: "A layout or contrast claim about this stylesheet is not verified until a browser
has drawn it." That applies to this skill's findings and to this skill's fixes.

**Any finding or fix touching a component that Step 2 found new or changed gets a probe
render.** Playwright is installed locally and `.github/render-modes.py` shows how the repo
finds Chrome. Build a throwaway page in the scratchpad that carries the **real** stylesheet
body (`dracula-nineties.css` with its first and last lines stripped, which are the `<style>`
wrapper) plus real markup for the component, then measure it:

- **800x600**, the period's working resolution, for the resting geometry.
- **640x480**, the period's floor, for the narrow case.
- **1024x768**, the period's upper end.
- **`dir="rtl"`**, for regressions in the repo's logical-property decision (NOTES.md,
  Direction). Read `borderLeftWidth` against `borderRightWidth`, not the declaration.
- **`emulate_media(media="print")`**, for the Print overrides. Read the computed value on the
  element the declaration actually targets **and** on the element the author probably meant.

Measure the same page again after the patch and put both numbers in the report. A claim with
a before-and-after pair is checkable a year later. "Fixed" is not.

**A slot-map finding gets a probe of its own kind, not a Chromium render.** Editor themes,
Light and dark parity: "Verify against the generated `.icls`, not the template: placeholders
hide which hex actually lands." Run `scripts/create-themes.nu` and `.github/palette-check.py
--dump` in the scratchpad, and quote the resolved hex per slot, before and after any patch
touching a `themes/**/*.in` file.

**A fix is not verified until the probe shows it.** On 2026-09-08 the first version of a
narrow-width column override was inert: the override sat in a media block above the rule it
meant to beat, a media query adds no specificity, and the base rule won on source order. The
arithmetic was right and the rendering was wrong. NOTES.md records the same trap twice
already, for the `.scorecard` container query and for the `@media (hover: hover)` position.

### Fixed period viewport sweep

Run this sweep on every audit. Render `samples/dark.html` and `samples/dark-conn-map.html` at
the period's canonical resolutions:

- 640x480, the period floor.
- 800x600, the period default.
- 1024x768, the period upper end.

Record fixture, viewport, `document.documentElement.scrollWidth`,
`document.documentElement.clientWidth`, and any intentional overflow. Check page-level
horizontal scrolling at every size. Inspect flex and grid stacking against DOM order. Separate
page overflow from scrolling inside documented table, code, math, and diagram hatches.

Confirm the settled fixed-width layout (NOTES.md, Width and measure) holds at each size.
Check visual hierarchy, heading order, and typography at each resolution, against the settled
type scale and heading decisions in NOTES.md. Test every loading, error, and empty state that
the fixtures implement, and confirm that critical actions remain reachable in each state. If
the template has no such state, report that fact. Do not invent states or controls. Add the
results under `## Period viewport sweep` in the report. This is a fidelity and readability
check at period resolutions, not a post-1999 responsive-design review.

### Topic 4 in particular: the WCAG 1.0 sweep

The rest of this skill asks whether the drawn design matches the period. Topic 4 asks a
narrower, harder question every run: **does this repo fail a WCAG 1.0 checkpoint, right now,
whatever NOTES.md decided.** WCAG 1.0 (W3C Recommendation, 5 May 1999) is the period's
accessibility standard, and it is the only accessibility document this audit cites. A
violation is not a style opinion. It goes in the patch like any other bug, unless the fix
contradicts a settled decision. In that case, make it a Step 5 challenge instead of an
ordinary finding.

**First, find the standard.** Confirm the WCAG 1.0 Recommendation date and its checkpoint
list from the W3C TR record. Do not import WCAG 2.x, WCAG 3.0, ISO/IEC 40500, EN 301 549, or
any later accessibility document as a criterion: each post-dates the period and this audit
does not use it. Report standards mapping only. Do not claim legal compliance.

**Second, run the Priority 1 and Priority 2 checkpoints that apply to a static, no-build CSS
and vanilla-JS template.** The table is fixed so coverage is stable from run to run and shows
what has not been checked. This template has one filter input, no audio or video, no
authentication flow, and no multi-step form process. Mark a checkpoint that requires absent
content `Not applicable` with a brief reason. Do not drop a checkpoint from the table just
because it is not applicable.

| Checkpoint | Priority | Check against |
| --- | --- | --- |
| 1.1 Provide a text equivalent for every non-text element | 1 | `alt` text on `img`, `accTitle`/`accDescr` on mermaid fences, SVG `title`, decorative pseudo-element `content: "…" / ""` |
| 2.1 Ensure all information conveyed with color is also available without color | 1 | `.verdict`, `.verified`/`.unverified`/`.correction`: color never the only cue |
| 3.1 Use markup rather than images to convey information where a markup language exists | 2 | Headings and labels are text, not image-based headings |
| 3.2 Create documents that validate to published formal grammars | 2 | Exactly one `<style>` and one `<script>` per fixture (the repo's own contract), and the markup parses |
| 3.3 Use style sheets to control layout and presentation | 2 | Presentation is in the inlined stylesheet, not presentational markup |
| 3.4 Use relative rather than absolute units in markup attributes and style sheet values | 2 | `--page-width` and the type scale. Check the exception NOTES.md records rather than re-litigating it |
| 3.5 Use header elements to convey document structure | 2 | The `h1` to `h6` hierarchy |
| 3.6 Mark up lists and list items properly | 2 | `ul`, `ol`, and `dl.timeline` |
| 3.7 Mark up quotations | 2 | `blockquote` and `q` where copy is quoted, not for indentation |
| 5.1 For data tables, identify row and column headers | 1 | `th` scope, table structure |
| 5.2 For data tables with two or more logical levels of headers, associate data and header cells | 1 | `table.tree` header association |
| 5.3 Do not use tables for layout unless the table makes sense when linearized | 2 | The repo uses no layout table; confirm |
| 6.1 Organize documents so they may be read without style sheets | 1 | DOM order vs visual order, especially `body.conn-map`'s flex reorder |
| 6.3 Ensure pages are usable when scripts are off or unsupported | 1 | The zoom control and the filter degrade to readable content |
| 6.4 For scripts, ensure event handlers are input device independent | 1 | Mermaid zoom button and filter input: keyboard operable |
| 11.1 Use W3C technologies and avoid deprecated features | 2 | No `font`, `center`, `bgcolor`, or other deprecated markup |
| 12.4 Associate labels explicitly with their controls | 2 | The filter `label` binds to `input.filter-box` |
| 13.1 Clearly identify the target of each link | 2 | No bare "click here". The outbound-link arrow carries alt text |
| 13.4 Use navigation mechanisms in a consistent manner | 2 | `nav.toc` and the nav groups keep a stable relative order |
| 14.1 Use the clearest and simplest language appropriate | 1 | Fixture prose is plain and direct |

**Not applicable for this template, stated once:** 1.2 to 1.5 (no image maps, no multimedia
beyond alt text), 4.x (single-language prose by convention; flag mixed-language fixtures
without language markup), 6.2 and 6.5 (the only dynamic content is the filter result count,
checked under 6.3), 7.x (no blinking, flashing, or moving content), 9.x (no image maps), 10.x
(no spawned windows, no side-by-side text tables), 12.1 to 12.3 (no frames), and 13.2 to 13.3
(metadata and site maps are out of scope for a single-document template).

**Priority 3 candidates, tracked separately, not as failures:** 5.5 (table summaries), 9.5
(keyboard shortcuts to important links), and 10.5 (printable characters between adjacent
links, which the `nav:not(.toc) > a` bracket pseudo-elements already provide).

**Classify every row, do not skip one silently:**

- **Pass.** State the evidence briefly. A passing sweep is worth reporting. This follows the
  reasoning for a `[Reinforces]` finding elsewhere in this skill.
- **Accepted gap.** NOTES.md already states, in prose, that this repo knowingly does not
  meet it (the 400% sideways-scroll line under Direction, zoom and growth is exactly this
  shape). Quote the passage. Confirm it describes current behavior. If behavior has changed,
  state whether the gap closed or remains open.
- **Violation.** Fails the checkpoint and NOTES.md never said so. This is the case Topic 4
  exists to catch. State the failure concretely (a selector, a missing attribute, a
  reproducible interaction), and put a mechanical fix in the patch if one exists, exactly
  like any other Topic 4 finding. If the only fix available would reverse a NOTES.md
  decision, this becomes a Step 5 challenge instead, same rule as everywhere else in this
  skill. If the only fix available is a design judgment rather than a mechanical one, say
  so in the row and leave it out of the patch, with the reason stated.
- **Not applicable.** For a checkpoint, state the absent feature and reason in its row. Keep
  the explicit out-of-scope summary for checkpoints outside the fixed table.

Report this sweep under its own `## WCAG 1.0 sweep` heading in the audit report, as a table
with one row per Priority 1 and 2 checkpoint above. Use (Checkpoint, Priority, Status,
Evidence) columns. Topic 4's ordinary findings still cover everything this sweep does not,
including the Priority 3 candidates and any markup-structure shift.

### Manual accessibility checks

Do not send local or private fixture content to an external service. If automated contrast
results are available, treat them as a supplement to Topic 1's palette gate and the rendered
contrast checks, not as a replacement.

Test keyboard navigation by hand in each appearance mode. Use Tab and Shift+Tab to visit
each interactive element. Use Enter, Space, and Escape where the control supports them.
Confirm every element has a visible focus indicator, and confirm that keyboard use keeps
critical actions reachable. Report these results under `## Accessibility and keyboard checks`.
Automated checks, when used, do not prove conformance.

### Topic 6 in particular

`AGENTS.md` mandates an exact pin, never a range, for every CDN dependency. Read the pinned
versions out of the files rather than from memory:

```bash
rg -o '[a-z0-9@/-]+@[0-9.]+' dracula-nineties.css mermaid.js | sort -u
```

For each, report the current release (`npm view <pkg> version time.modified`), whether
anything between the two is a rendering or security fix, and whether the upgrade is worth
taking. **Do not put a Mermaid bump in the patch:** `nu scripts/maintain.nu mermaid <version>`
is the supported path and it touches generated files. Name the command in the report and stop
that part there.

**Also check provenance, not only freshness.** Every jsDelivr URL in the two files above
loads through a mechanism with no `integrity` attribute available to it: `@font-face src:
url()` has no SRI hook in any browser, and a bare-specifier ESM `import` of a remote URL has
no `integrity` hook either, current npm-package or import-map metadata aside. State this
plainly rather than proposing an `integrity=` attribute that cannot attach to either
construct. What is checkable:
- The URL pins an exact version (already covered by the exact-pin row in Step 4's table,
  cross-reference rather than re-run).
- jsDelivr serves the npm-published tarball unmodified at a versioned path, so the actual
  supply-chain question is whether the **npm package itself** has a provenance attestation
  (`npm view <pkg> dist.attestations` or the npm registry's provenance badge), not whether
  the CDN edge is trusted.
- Whether self-hosting the four font files or Mermaid bundle is worth the tradeoff NOTES.md
  already weighed. Read that passage before proposing self-hosting again. If NOTES.md already
  declined it, mark it `[Repeat]` or match `review/declined.md`. Do not call it new ground.

### Topic 7 in particular: new period references

The `inspiration/` corpus is the period ground this template draws on. Each run reviews the
entries added since the previous audit, because a new reference is the one input that can
introduce a design consideration the earlier runs never weighed. This is the part of the
audit that keeps the period vocabulary growing instead of frozen at the first run.

```bash
PREV=<the previous report's SHA, or the most recent inspiration/ commit>
git diff --name-only "$PREV..HEAD" -- inspiration/
```

When the previous report names no SHA, the floor is the most recent commit that touched
`inspiration/` (`git log -n1 --format=%H -- inspiration/`). Say which floor was used. If no
entry was added in the window, say so in one line under `## New period references` and move
on.

For each added `.png` and its sibling `.txt` (written by the `inspiration-analyze` skill):

1. **Read the `.txt`** (`[PALETTE]`, `[LAYOUT]`, `[META]`, `[RELEVANCE]`), then look at the
   image itself. The `.txt` is the analysis; the image is the evidence.
2. **Ask what it teaches this template**, per its `[RELEVANCE]` line, and whether the drawn
   result already carries that cue or could. A reference that reinforces a settled decision
   is a `[Reinforces]` finding. A cue the payload lacks is `[New ground]`, and the report
   cites the reference by filename and the period document it sits in.
3. **Do not propose a post-1999 reading of it.** A 1998 page is evidence about 1998, not a
   licence to import a later convention.
4. **A `.png` with no sibling `.txt` is a finding of its own**: its analysis is missing, and
   `inspiration-analyze` is the skill that writes it. Name the command in the report. This
   skill only reads the corpus and never writes an analysis `.txt`.

Report under `## New period references`, one block per added entry, and list the added names.

### Period standards

Check this section on every audit. Report the period document each finding cites, and its
date. These documents are historical and frozen, so the check is that a citation points at
the period document, not that a status changes. **Do not import a post-1999 standard as the
yardstick.**

| Area | Period source to cite | Report |
| --- | --- | --- |
| HTML 3.2 | W3C Recommendation, 14 January 1997 | Which HTML 3.2 constructs the markup uses |
| HTML 4.0 and 4.01 | W3C Recommendation, 18 December 1997 and 24 December 1999 | Whether the markup validates to the period grammar |
| CSS1 | W3C Recommendation, 17 December 1996 | Which CSS1 properties the design relies on |
| CSS2 | W3C Recommendation, 12 May 1998 | Which CSS2 properties are used, and whether the drawn result is expressible in period CSS |
| WCAG 1.0 | W3C Recommendation, 5 May 1999 | The Priority 1 and 2 sweep above |
| Web-safe palette | the 216-color web-safe table | Whether the ground and accent roles map to web-safe values or a documented dithered-safe equivalent |
| Period browser references | Netscape Navigator 3 and 4, Internet Explorer 3, 4 and 5 | The browser an idiom targeted, named only when it explains a decision |

Report this under `## Period standards`. Add `### Searched` with every query, source title,
URL, and access date. State that the audit maps technical criteria only. Do not claim that a
template complies with any law.

### Period technique review

Check the drawn result against the period repertoire. Report one row per technique under
`## Period technique review`, with the technique, whether the drawn result uses it, and the
reason when it does not. A post-period idiom found in the rendering is a candidate fidelity
finding, checked against NOTES.md first.

| Period technique | What to check |
| --- | --- |
| Fixed-width page column | `--page-width` produces a centered fixed column (NOTES.md, Width and measure) |
| Web-safe or dithered-safe grounds | Grounds map to web-safe values or a documented equivalent |
| Era font stacks | Georgia, Verdana, Trebuchet MS, Courier, Times: a stack of the period, not a system-UI default |
| Visible link states | link, visited, hover, and active states, in the period underline and color convention |
| Table-free layout | The page lays out in CSS, not a layout table (a settled decision) |
| Rule and bevel ornament | 1px rules, doubled frames, or a bevel in the period vocabulary, not large radii or soft shadows |
| No post-period visual idiom | No large `border-radius`, no softened shadow, no eased hover transition with no period analogue |

Also look for a modern default that arrived after 1999 and changes the look: a system-UI sans
stack, flat neutral chrome, or a generated modern widget. Record each as a candidate and
check NOTES.md before proposing anything. Report queries and sources under `### Searched`
for the relevant topics. Recheck these rows on every audit, including rows the drawn result
does not exercise.

### Step 3 report format

The report has one section for each of the seven topics, followed by `## Period standards`,
`## Period technique review`, `## Period viewport sweep`, `## Accessibility and keyboard
checks`, `## WCAG 1.0 sweep`, and `## New period references`. Include every relevant Priority
1 and 2 checkpoint from the current WCAG 1.0 record. Mark absent features not applicable with
a reason. Add `### Searched` under each research topic and include every query and source used
for the standards and technique review.

## Step 4: the ungated-rules sweep

**Why this exists.** AGENTS.md: "a gate is the only thing that keeps a prose rule alive in a
repo where most edits are made by an agent." Several rules in AGENTS.md and NOTES.md have no
gate behind them, so `nu scripts/maintain.nu check` prints `Contract OK` while the payload
breaks them. A five-line block comment inside `@media print` shipped in v1.41.0 and reached
every consumer page for four releases while three design audits read past it. This table is
fixed so that cannot happen a fourth time.

Run every row. The commands are starting points, not the whole check: read the hits.

| Rule | Source | Check | 
| --- | --- | --- |
| No comment in `dracula-nineties.css` or `mermaid.js`. **Both exceptions are CSS-only** (line 2's version stamp, the `/* was #rrggbb */` notes), so `mermaid.js` must have zero comments | AGENTS.md | `rg -n '/\*' dracula-nineties.css \| rg -v 'was #'` returns line 2 only. Then `rg -n -e '/\*' -e '^\s*//' mermaid.js` returns nothing |
| Every `var(--x)` resolves to a declared token or has a fallback | NOTES.md, Progressive disclosure | Set difference. Match `--x:` anywhere because component tokens count. Exclude references with fallback commas. Six references outside `:root` resolve on `HEAD`, and all six are deliberate |
| Sides are logical, never physical | NOTES.md, Direction, zoom and growth | `rg -n 'border-left\|border-right\|padding-left\|padding-right\|margin-left\|margin-right' dracula-nineties.css` returns nothing, except a deliberate physical fallback stated in NOTES.md (the sidenote `float`) |
| Every `:hover` rule sits inside `@media (hover: hover)` | NOTES.md, Interaction states | Every line number from `rg -n ':hover' dracula-nineties.css` falls inside that block's range. A selector pairing `:hover` with `:focus-visible` in one rule is the usual way this breaks |
| Decorative pseudo-element content has an alt-text twin | NOTES.md, Links | Check each string-valued `::before` and `::after`. The twin must follow its base declaration |
| A selector not represented in a fixture has a documented reason or remains a candidate, not presumed unused | NOTES.md, Print, and Fixtures are coverage | Compare class selectors against `scripts/build-sample.nu` and NOTES.md exceptions. Do not remove selectors only because fixtures did not exercise them |
| Mermaid colors are hex, never `oklch()` and never `var()` | AGENTS.md | `rg -n 'oklch\|var(' mermaid.js` returns nothing in a color position |
| Exact CDN pin, never a range | AGENTS.md | No `^`, `~` or `latest` in a jsDelivr URL |
| Never cite a line number into a generated file | AGENTS.md | `maintain.nu check` gates search-string pointers. Confirm each new document pointer uses this form |
| New composite grounds outside palette-check coverage have a NOTES.md entry | AGENTS.md | Add a gate or document grounds not covered by `--surface`, `--code-bg`, or `--surface-alt` |

Status per row is `Pass`, `Violation` or `Not reachable this run` (say why). Report it under
its own `## Ungated-rules sweep` heading.

### A finding a gate could catch should become a gate

The first two rows of that table are mechanically decidable in a few lines of Nushell, and
they caught two real defects on the 2026-09-08 run. **This skill may put a `maintain.nu`
gate in the patch**, and should when a row is cheap to mechanize: `scripts/` is a source
file, the patch already touches source files, and Step 7 regenerates and runs `check` in a
worktree so a broken gate fails there rather than in the maintainer's tree.

Two limits on that:

- **A gate that cannot reach its subject does not get written.** AGENTS.md is explicit, and
  it is why the `quadrantChart` label rule is prose. Prefer an honest NOTES.md paragraph over
  a check that reports green about a question it never asked.
- **A gate that would fail on `HEAD` goes in the patch together with the fix it demands**, or
  it does not go in at all. A patch that adds a red check is a patch nobody can apply.

## Step 5: settled decisions can be challenged, but only loudly

NOTES.md exists because several past changes were correct on paper, shipped, and had to be
reverted. This skill is allowed to propose reopening a settled decision, but never
quietly. Every such finding in the report must:

- Quote the exact NOTES.md passage being challenged, with its section heading.
- State what changed since that passage was written (a new `inspiration/` reference, or a
  period document the earlier run did not cite) with a cited source and a date.
- Sit under a `## Challenges a settled decision` heading, separate from ordinary findings.
- Carry the line: `Requires maintainer sign-off before this touches NOTES.md or the
  stylesheet.`

**A challenged finding never enters the patch.** Not in this run and not in any run. Step 8
ends the invocation, so sign-off cannot happen inside a run that raised the challenge, and
a patch drafted "in case" is a patch nobody agreed to. If the maintainer signs off later,
that is a separate ask in a separate turn, and they ask for the change directly through the
normal contract flow.

**Do not confuse a challenge with a violation.** A challenge says the decision may be wrong
now. A violation says the code broke a decision that still stands. A violation goes in the patch. A challenge never does.

Findings that do not challenge a settled decision go into the draft patch.

## Step 6: write the two artifacts

Get today's date once (`date +%F`) and reuse it for both filenames. Do not call `date` separately for each file. A run that crosses midnight could produce mismatched pairs. A
second run on the same day overwrites the first: that is intended, one audit per day is
the unit.

- `review/YYYY-MM-DD-design-audit.md`: the report. A header naming **the commit range and
  commit count** from Step 2 and the previous report it read, the Step 2 delta findings, one
  section per topic, findings classified per Step 3, `### Searched` per topic, sources cited
  inline with dates, the `## Period standards` report, the `## Period technique review`, the
  period viewport sweep, the accessibility and keyboard checks, the current WCAG 1.0 sweep,
  the new period references, the ungated-rules sweep, the challenged-decisions section (if
  any) clearly separated per Step 5, one line naming the out-of-scope NOTES.md sections, and
  the Step 7 verification result.
- `review/YYYY-MM-DD-design-audit.patch`: a unified diff against `HEAD` covering only the
  non-challenging findings the maintainer would plausibly want. A draft to review, not
  something to apply automatically. **If there are no such findings, do not write an empty
  patch file.** Say "no patch: nothing to propose" in the report instead.

The report and patch never edit `AGENTS.md` or this skill. Report audit-process gaps separately.

The patch must obey every constraint in AGENTS.md: no comments added to
`dracula-nineties.css` or `mermaid.js`, no em-dash or en-dash anywhere, hex-only in
`mermaid.js`, the `<style>` and `<script>` wrapper contract intact. Step 7 proves that
mechanically rather than trusting it.

**The patch touches source files only.** It never changes `samples/*.html` or `tokens.css`.
The generator creates those files. Step 7 regenerates them in a throwaway worktree to test the
patch. If the maintainer accepts it, they regenerate through the normal contract flow.

`NOTES.md` and `scripts/` are source files and the patch may touch both. Step 2 findings about
undocumented components require a NOTES.md entry. Step 4 findings that a short script can check require a gate.

**The easiest way to author the patch is a second worktree.** Edit there, regenerate there,
run `check` there, then `git diff HEAD -- <source files only>` out of it. That keeps the real
tree clean, which is this skill's hardest rule, and it means the diff you emit is the diff
you already tested. Remove both worktrees when done.

Create `review/` if it does not exist. Do not touch any other file in the working tree.

## Step 7: verify the patch mechanically, or say it is unverified

AGENTS.md: "a gate is the only thing that keeps a prose rule alive in a repo where most
edits are made by an agent." A patch this skill only *claims* obeys the contract is worth
less than no patch, because the maintainer pays to discover otherwise.

Skip this step only when Step 6 wrote no patch.

```bash
D=$(date +%F)
git worktree add --detach /tmp/design-audit-verify HEAD
git -C /tmp/design-audit-verify apply "$PWD/review/$D-design-audit.patch"
nu /tmp/design-audit-verify/scripts/build-sample.nu     # regenerate INSIDE the worktree
nu /tmp/design-audit-verify/scripts/maintain.nu check   # must print "Contract OK"
git worktree remove --force /tmp/design-audit-verify
```

Four things about that sequence, each of which has one way to get wrong:

- **The worktree is at `HEAD`, so the patch must apply to `HEAD`.** Generate the diff
  against `HEAD`, not against a dirty working tree.
- **`build-sample.nu` runs before `check`, not after.** `check` regenerates internally and
  fails on `STALE` if the fixtures do not match the sources. A patch that changes the CSS
  and no fixtures always trips that. Regenerating first is what makes the staleness gate
  say something real: it now proves the patch survives regeneration.
- **Everything happens in the worktree.** The real tree keeps its generated files
  untouched, which is the rule Step 6 states.
- **`git worktree remove` runs even when `check` fails.** Do not leave the worktree behind.

Then run the two scans `check` cannot do for you.

The first covers this skill's own output files, which the dash gate misses because it
reads `git ls-files` and these are not tracked yet:

```bash
rg -c -e '\u{2014}' -e '\u{2013}' review/$D-design-audit.*   # must find nothing
```

The second covers the rule with no gate behind it. **`maintain.nu check` does not detect a
comment added to `dracula-nineties.css` or `mermaid.js`.** A patch that adds one passes
`Contract OK` and ships a comment into every page every consumer ever renders, which is the
single hardest prohibition in AGENTS.md. Read every added line of the patch yourself:

```bash
rg -n '^\+' review/$D-design-audit.patch | rg -e '/\*' -e '\*/' -e '//'   # must find nothing
```

That regex over-matches (a `//` inside a URL trips it, and a `#` comment added to a Nushell
script is permitted), so read the hits rather than trusting the count. Zero hits passes. Any
hit needs an eye on it.

Third, **re-run the probe render from Step 3 against the patched stylesheet** and record the
after numbers beside the before ones. `Contract OK` says the contract holds. It says nothing
about whether the fix took effect.

Record the outcome in the report as one of exactly three verdicts:

- `Verified: patch applies to HEAD and Contract OK after regeneration.`
- `FAILED: <the shortest decisive line of output>.` Fix the patch and re-verify, or drop
  the offending finding to the report body and say why.
- `Unverified: <reason>.` Use this only for a missing local dependency, `check` runs
  `render-modes.py`, which needs a local Chromium. A missing browser is an environment
  gap, not a bad patch, and calling it a failure is a false report. Never write
  `Verified` for a run where `check` did not conclude.

## Step 8: Report Back, Then Stop

End by telling the maintainer where the files landed, the verification verdict, and one
line of counts: findings total, how many are violations of a settled decision, how many are
new, how many are repeats, how many challenge a settled decision, how many added
`inspiration/` references this run reviewed, and how many evidence checks were unavailable.
Stop there.

Applying the patch, updating NOTES.md, appending to `review/declined.md`, bumping a CDN
pin, or cutting a release are separate asks with their own flow (see the `release` skill
and AGENTS.md's regeneration section). This skill does not chain into any of them.

## Rules with no exception

- **Never edit `dracula-nineties.css`, `mermaid.js`, `filter.js`, `samples/*.html` or
  `tokens.css` in the working tree.** The only place this skill applies a change is a
  throwaway worktree it removes in the same step.
- **A challenged decision never enters the patch.** See Step 5. A violated decision always
  does.
- **Never write `Verified` for a `check` that did not conclude.** Unverified is a real
  verdict and it is the honest one.
- **Never write to `review/declined.md` unprompted, and never remove a row from it.** It
  is the record of what the maintainer already decided.
- **Never claim a design is period-correct without a render that shows it.** Arithmetic has
  been wrong here four times on record.
