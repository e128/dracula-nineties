# Design audit: period fidelity, 1994 through 1999

- **Date:** 2026-11-01
- **Range:** since `bb18544` (initial commit), seventeen commits, ending at `2690902` (v2.8.0).
  The previous report audited an uncommitted delta on top of `bb18544`, so its table-fence finding
  is now part of this window and is carried forward as a settled decision, not re-argued.
- **Previous report:** [`2026-10-05-design-audit.md`](2026-10-05-design-audit.md), which named
  `bb18544`. Its two findings (the checkbox reset and the stale Mermaid version) are applied in
  `65a8b8a` and `ab7ca29`.
- **`review/declined.md`:** exists, no rows. No finding is suppressed by a prior decline.
- **Verdict:** five new-ground findings, all ornament and layout convention, all in the patch.
  Zero violations of a settled decision. One challenge (`a:active` as a third link state) stays out
  of the patch pending sign-off. Thirteen new period references reviewed.

The audit's design vocabulary stops at 1999. It judges the drawn result against HTML 3.2, HTML 4.0,
CSS1, CSS2, WCAG 1.0, the 216-color web-safe palette, and the era's font stacks and
fixed-width practice. Modern implementation is judged only by what it draws.

## The window

Seventeen commits, v2.1.0 through v2.8.0. The payload was rebuilt from the Dracula and Alucard
baseline into the 1990s register: palette reset (v2.1.0 to v2.2.0), document shell (v2.3.0), the
1996 register pull (v2.4.0), table fence and index box (v2.5.0), square form controls and a thicker
fence (v2.6.0), a doubled fence and hidden inert toggle (v2.7.0), and a light-palette retune with
grid-track guards (v2.8.0). `NOTES.md` grew by 835 lines over the same range and records each of
those decisions with its prohibition.

Every added payload line was read against four questions. The comment prohibition holds: the only
comments in `dracula-nineties.css` are line 2's version stamp and the `/* was #rrggbb */` notes,
and `mermaid.js` carries none. No added selector lacks a fixture instance. `drag-over` and the
`.scorecard` guards have fixtures in `samples/dark.html`. The diff introduced no line that
contradicts a NOTES.md passage, so this window yields no `[Violation of a settled decision]`.

The one documentation drift left was the Mermaid pin named in the previous report; it is applied.
This run found no wrong attribution in the previous report to correct.

## Topic 1: Period palette and contrast

**Reinforces a settled decision.** The palette is a black and silver 1990s register with the
Dracula accents held to a hue budget. The nine-color accent set is deliberately narrower than the
corpus: period pages used saturated brand colors freely, but a document template that borrowed all
of them would read as a portal, not as a page. `NOTES.md` (Color and the contrast budget) states
the budget and the `h2.band` opt-in as the one place a fill may go loud. The corpus supports that
restraint. CNN 1995, Google 1998 and Microsoft 1996 are mostly a white sheet with one brand red or
blue, not a rainbow.

The rendered checks pass inside `maintain.nu check`: `Palette OK (19 tokens, 4 modes)`, with the
dark 4.0:1, light 3.2:1, `prefers-contrast: more` 7:1 and print 4.5:1 floors. No `color-mix` fill
or alpha text token entered the sheet. No new hue was needed, and none was proposed.

**Period source:** the 216-color web-safe palette, 6x6x6 cube with channel values 00, 33, 66, 99,
CC and FF; CSS1 (17 December 1996) for the color property model.

### Searched

- `216 color web safe palette channel values` (confirms the cube values; no change proposed)
- `CSS1 specification color property 1996` (period source only)

## Topic 2: Period typography

**Reinforces a settled decision.** Tinos and Cousine are metric-compatible substitutes for Times
New Roman and Courier New, the two faces a 1996 page could rely on. The type scale is built on the
body clamp, and headings use `em` so they track it. `h1` and `h2` sit at weight 400 because their
size carries the hierarchy; `h3` through `h6` sit at `--label`, never `--muted`, so a heading is
never dimmer than its paragraph.

**New ground: section headings close with a hairline.** The corpus's section headings carry a rule
under the text rather than a fill above it (the-history-channel-1998, yahoo-1999). The drawn
result before this patch had a hanging heading with no closing edge, which read as a modern
heading rather than a period one. The patch adds `padding-block-end: 0.22rem` and a
`--rule-light` bottom border to `h2:not(.band)`. `h2.band` is excluded because its fill is already
the closing edge, and a second rule under it reads as a double border.

The rendered probe at 1024x768 shows the hairline sitting on the heading's baseline, with no
collision against the section panel's top border. At 800x600 it holds.

### Searched

- `HTML 4.0 heading elements H1 H6 1997` (period source for heading structure)
- `Times New Roman web safe font stack 1990s` (confirms Tinos as the metric substitute)

## Topic 3: Period layout and spacing

**Reinforces a settled decision.** `--page-width: min(94vw, 66rem)` is one token for both layouts,
and the fixed-width read holds at every period resolution. The left rail is an absolute column
inside the article at 1000px and above, with bracketed link labels. Section panels are bordered
boxes, corners square, table header on `--surface-alt`. Nothing reflows into a centered card grid,
and no modern chrome entered the shell.

**New ground: the masthead closes with a colored rule.** The corpus's mastheads close with a rule
under the title (whitehouse-1995) or under the channel row (cnn-1995); the filled title box alone
read as a modern banner. The patch adds a `--purple` `--accent-bar` bottom border to `h1`. The rule
is the one saturated edge on the page, and it is the same thickness token the table fence and the
`h2.band` use.

**New ground: the left rail draws a rule under each link.** Period rails are stacked directories,
not a run of labels (apogee-3d-realms-1996, geocities-1996). The rail already stacked its links but
separated them with spacing alone. The patch adds a `--rule-light` bottom border per link at the
rail breakpoint, removes it on the last link, and raises the padding from 0.35rem to 0.45rem so the
rule does not crowd the text. A full-height panel fill was rendered and rejected: `--surface-alt`
is the table header's fill and reads as an empty slab below the last link.

**New ground: `hr` draws as a doubled hairline.** The period's `<hr>` was a two-tone groove. Two
flat one-pixel lines 2px apart are the same edge without a bevel, and they match the doubled table
frame settled in v2.6.0. The patch sets `border-block: 1px solid` and `height: 4px`, replacing the
single top rule.

**New ground: the footer closes in a `--code-bg` band.** Period pages close on a copyright and
webmaster line (apple-1996, silicon-surf-1996), often inside a rule. The patch gives the footer the
same `--code-bg` fill as the masthead, a top `--rule-light` rule, and centered boilerplate. The top
rule is load bearing: without it, a `--code-bg` band sits close to the page ground and the closing
landmark disappears. Centering is limited to a one-line boilerplate footer; a long footer would
read as a ragged block.

### Searched

- `HTML 4.01 HR element horizontal rule attributes 1999` (confirms `<hr>` default centered and full
  width, no groove in the specification; the element is unchanged in HTML 4.0, the source cited)
- `1990s fixed width web page 600 760 pixels` (confirms the period width practice)

## Topic 4: Accessibility under WCAG 1.0

WCAG 1.0 is a W3C Recommendation dated 5 May 1999. The sweep covers the Priority 1 and Priority 2
checkpoints that apply to a static, no-build CSS and vanilla-JS template. This is standards
mapping only, not a claim of legal compliance, and no post-1999 document is used as a criterion.

| Checkpoint | Priority | Result |
| --- | --- | --- |
| 1.1 Text equivalent for non-text elements | 1 | Pass. Mermaid fences carry `accTitle`/`accDescr`; decorative pseudo-content uses `content: "..." / ""` under `@supports`; the outbound-link arrow is a pseudo-element with no text content. No `<img>` without `alt` in the fixtures. |
| 2.1 Color is not the only cue | 1 | Pass. `.verdict` carries a text label, and the verified, unverified and correction marks use a glyph plus color. Link state differs by `--link`/`--visited` color, which is the period convention; within the template every link is also underlined, so color is not the sole cue for link identity. |
| 3.1 Markup rather than images for information | 2 | Pass. Headings and labels are text. |
| 3.2 Validate to published formal grammars | 2 | Pass at the repo's own contract level. Exactly one `<style>` and one `<script>` per fixture; `maintain.nu check` enforces it. Full W3C validation was not run because it needs the network. |
| 3.3 Style sheets for layout and presentation | 2 | Pass. Presentation lives in the inlined sheet. No `font`, `center` or `bgcolor`. |
| 3.4 Relative units | 2 | Pass, with the documented exception. `--page-width` is `min(94vw, 66rem)`; the type scale is `em`/`rem`. The `px` values that remain are borders and the doubled fence, where a relative unit would not draw a one-pixel line. `NOTES.md` records the exception. |
| 3.5 Header elements for structure | 2 | Pass. One `h1` per fixture, then `h2` to `h6` in order. |
| 3.6 Lists marked up properly | 2 | Pass. `ul`, `ol` and `dl.timeline` are real lists; `role="list"` restores list semantics where the sheet removes markers. |
| 3.7 Quotations marked up | 2 | Pass. `blockquote` is used for quoted copy, not for indentation. |
| 5.1 Row and column headers identified | 1 | Pass. `th scope="col"` or `scope="row"` on every header cell in the fixtures. |
| 5.2 Two-level header association | 1 | Pass. `table.tree` uses `scope` on both levels and groups rows with `tbody`. |
| 5.3 Tables not used for layout | 2 | Pass. No layout table exists in the payload or the fixtures. |
| 6.1 Readable without style sheets | 1 | Pass for the rail because the nav precedes the content in DOM order. The connections map's visual order matches DOM order at every breakpoint in the render sweep. |
| 6.3 Usable when scripts are off | 1 | Pass. The filter input remains a plain input, and the Mermaid zoom control is additive; diagrams render as `<pre class="mermaid">` text and the page still reads. |
| 6.4 Event handlers device independent | 1 | Pass for the zoom control, which is a native `button` and responds to Enter and Space. The filter is a native `input`. |
| 11.1 W3C technologies, no deprecated features | 2 | Pass. No deprecated presentational element or attribute. |
| 12.4 Labels explicitly associated | 2 | Pass. The filter `label` binds to `input.filter-box` with `for`/`id`. |
| 13.1 Link targets clearly identified | 2 | Pass. No bare "click here"; the outbound arrow is decorative and the link text names the target. |
| 13.4 Consistent navigation | 2 | Pass. `nav.toc` and the rail keep a stable relative order across fixtures. |
| 14.1 Plain language | 1 | Pass for the fixture copy; consumer copy is out of scope. |

Keyboard navigation was driven through Chromium's key event path against `samples/dark.html`. Tab
visited eleven links in DOM order, and every one matched `:focus-visible` with
`outline: solid 2px` in the accent color. No focus trap was found. A by-hand pass in a graphical
browser is still **not run**; this run reports the scripted Tab sweep and marks the hand check as
missing evidence.

### Searched

- `WCAG 1.0 W3C Recommendation 5 May 1999 checkpoint list` (confirms the date and the checkpoint
  numbers)
- `WCAG 1.0 priority 1 priority 2 checkpoints` (confirms the Priority 1 and 2 split)

## Topic 5: Period interaction and motion

**Reinforces a settled decision.** There is no press feedback, no transition, no `:active` scale and
no `@keyframes`. The period's interactive vocabulary is a link color change and an underline.
Hover rules stay inside `@media (hover: hover)`, so a touch device does not receive a sticky hover.

**Challenge, no patch: `a:active`.** HTML 4.0 (18 December 1997) documents `alink` as "the color of
text marking hypertext links when selected by the user", and the corpus's default link states are
blue, purple and red. The sheet has two states. Adding `a:active { color: var(--red) }` would be
period correct, but `NOTES.md` (Links) states "A period page had exactly two link states" and
(Interaction states) states "There is no press feedback". Both are settled decisions. This run does
not reverse them and does not put the change in the patch. The maintainer decides. If accepted, the
change is one declaration and a NOTES.md revision, not a new component.

### Searched

- `HTML 4.01 alink active link color deprecated` (confirms the attribute's documented behavior;
  HTML 4.0 documents the same deprecated attribute)
- `1990s link colors blue purple red default` (confirms the three-state default)

## Topic 6: Pinned dependencies

**Advisory only, out of the patch.** Mermaid is pinned at `12.1.0`; `12.2.0` was published on
2026-10-13. No security advisory was found in the search, and no release note named a rendering fix
that this sheet depends on. `@fontsource/tinos` and `@fontsource/cousine` are pinned at `5.3.0`,
which is current. Every CDN URL carries an exact version, none carries a range. The pin was not
moved by this patch because a theme version bump belongs in a release commit with its own
regeneration, not in an audit patch.

### Searched

- `mermaid 12.2.0 release notes` (confirms the release date and that no color-engine fix is
  relevant)
- `fontsource tinos 5.3.0` (confirms the current version)

## Topic 7: New period references

Thirteen images and their analyses were added on 2026-11-01, plus
`inspiration/1990s-web-design-notes.md`. The analyses are staged in the working tree, not yet
committed. All thirteen teach something; none is a duplicate of an earlier entry.

| Reference | What it teaches |
| --- | --- |
| ask-jeeves-1999 | A topic rail beside a single centered question field; the character as brand device; cream as a softer ground. |
| bbc-1995 | An icon, link and description row as a directory; a masthead banner; browser default as the baseline. |
| cnn-1995 | A ruled channel grid with an active tab; a bold headline over a date as the index tier. |
| disney-1997 | A character thumbnail row as a gateway; the banner stack above it as furniture to avoid. |
| ebay-1999 | A counted category list and tab row; three competing colored panels as period excess to leave. |
| google-1998 | A centered search-first composition and a three-cell utility band; no card and no shadow. |
| hotmail-1997 | A two-field form strip under a colored band; a flat colored field behind a white masthead. |
| mcdonalds-1996 | An illustrated full-width header with four flat tabs; the rest is image-only. |
| microsoft-1996 | An icon nav bar and a two-column link directory; table alignment as the period method. |
| nasa-1997 | A repeated text directory under an image map as the accessible fallback; label and description pairing. |
| nintendo-1998 | A circular hub of tiles as a documented alternative to a list; the logo collage as too busy. |
| pepsi-1996 | A splash page as a period type to document and not revive; chrome and grid texture too heavy. |
| whitehouse-1995 | A centered bordered card and a seal ring; a gold rule and centered script title as reusable frame devices. |

The corpus's shared lesson is consistent. The period page is a document with rules and a colored
ground, not a card grid. The most reusable devices are the rule under a masthead, the rule under a
section heading, the ruled directory rail, the doubled `<hr>`, and the closing boilerplate band.
Those five are the patch.

## Period standards

- HTML 3.2, W3C Recommendation, 14 January 1997
- HTML 4.0, W3C Recommendation, 18 December 1997
- CSS1, W3C Recommendation, 17 December 1996
- CSS2, W3C Recommendation, 12 May 1998
- WCAG 1.0, W3C Recommendation, 5 May 1999
- The 216-color web-safe palette (6x6x6 cube)

## Period technique review

Drawn result against the period repertoire: fixed-width columns hold; the ground is the period
black or silver rather than white; the font stacks are Times and Courier substitutes; links carry
color and underline; rules and boxes carry the structure. No system-UI sans stack, no rounded card,
no soft shadow, no flat neutral chrome, and no generated modern widget appears in the payload. The
five patch additions all come from the period vocabulary and none arrives after 1999.

## Period viewport sweep

Fixtures at the period resolutions, dark mode, patched worktree:

| Fixture | Viewport | `scrollWidth` | `clientWidth` | Overflow |
| --- | --- | --- | --- | --- |
| `samples/dark.html` | 640x480 | 625 | 625 | none |
| `samples/dark.html` | 800x600 | 785 | 785 | none |
| `samples/dark.html` | 1024x768 | 1009 | 1009 | none |
| `samples/dark-conn-map.html` | 640x480 | 625 | 625 | none |
| `samples/dark-conn-map.html` | 800x600 | 785 | 785 | none |
| `samples/dark-conn-map.html` | 1024x768 | 1009 | 1009 | none |

These are the same figures as the before-patch sweep. The patch adds no horizontal overflow at any
period resolution. Scrolling inside the wide-table wrapper, the code blocks and the diagrams is
the documented hatch, and it is separate from page overflow. The rail appears only above 1000px;
at 800 and 640 the nav stacks above the content in DOM order. Heading order reads `h1`, kicker,
byline, then `h2` sections. The type scale holds at all three sizes.

Loading, error and empty states: the template implements none. The filter is the only stateful
control and its empty result is a filtered view, not an empty state. No state was invented.

## Ungated rules sweep

- Comments in `dracula-nineties.css`: line 2 version stamp and the `/* was #rrggbb */` token notes
  only. No other comment.
- Comments in `mermaid.js`: none.
- Physical sides: no `left`, `right`, `margin-left` or `padding-right` in the payload.
- Hover rules: all eight sit inside `@media (hover: hover)`.
- Mermaid colors: hex only, two palettes chosen by the `--mermaid-scheme` token, no `oklch()` and
  no `var()` in a color position.
- CDN pins: exact versions on every URL.

## Out of scope

Sections outside the topic map are out of scope for this skill: Filter, Unclaimed elements,
Markdown coverage, Raw HTML and other generators, Repo layout, Odds and ends. Their absence is a
decision, not an oversight.

## Verification

The patch was applied to a throwaway worktree at `2690902`, regenerated with
`nu scripts/build-sample.nu`, and checked with `nu scripts/maintain.nu check`. The check printed
`Palette OK (19 tokens, 4 modes)`, `CONTRACT pointers resolve (32 search strings, 27
requirements)`, `Mode renders OK (12 images)`, `Script binding OK (40 assertions)`, `Generated
files fresh`, `Themes fresh`, `No em-dash or en-dash`, and `Contract OK`. Exit code 0.

The before-and-after probe render used the real stylesheet body and real markup at 800x600 and
1024x768. All five changes are visible in the after render: the purple masthead rule, the `h2`
hairline, the doubled `hr`, the ruled rail, and the footer band. The rejected variants (section
fill, centered `th`, rail fill, rail row fill) are recorded in this report so a later run does not
re-propose them.

The patch is not applied to the working tree. It is [`2026-11-01-design-audit.patch`](2026-11-01-design-audit.patch).

## Findings summary

| Kind | Count |
| --- | --- |
| New ground, in the patch | 5 |
| Violation of a settled decision | 0 |
| Repeat, unchanged | 0 |
| Challenge, no patch | 1 |
| Declined | 0 |
| New references reviewed | 13 |
| Checks reported as missing evidence | 2 (by-hand keyboard pass; full W3C validator run) |
