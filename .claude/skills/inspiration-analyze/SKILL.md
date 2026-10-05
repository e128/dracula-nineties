---
name: inspiration-analyze
description: Write a per-image analysis file beside every screenshot in inspiration/. Each image gets a sibling .txt holding the same four marked sections in the same order (PALETTE, LAYOUT, META, RELEVANCE) plus a header block, with role colors sampled from the pixels. Use when the user says "analyze the inspiration images", "analyze inspiration", "write the reference analyses", "document the inspiration folder", or invokes /inspiration-analyze.
---

# Analyze the inspiration screenshots

`inspiration/` holds reference screenshots of 1990s and early-2000s pages. This skill writes the
sibling `.txt` analysis for each image: what it looks like, how it is laid out, what it reads as
overall, and whether it teaches this template anything.

Read [AGENTS.md](../../../AGENTS.md) "Inspiration analysis" first. The template below is that
section made runnable, and this file never adds a rule of its own.

This skill writes only into `inspiration/`. It never edits `dracula-nineties.css`, `mermaid.js`,
or anything under `samples/`.

## Step 1: take inventory

```
ls inspiration/*.png
ls inspiration/*.txt
```

A `.png` with a `.txt` beside it is done and is skipped unless `--force` was asked for. Report
which images you skip, every run, so a stale skip is visible.

## Step 2: measurements

Per image, before anything else:

```
magick identify -format "%f %wx%h\n" inspiration/<name>.png
magick inspiration/<name>.png -colors 12 -format %c histogram:info:- | sort -rn | head
```

The first gives `dimensions`. The second gives the dominant colors, but it is dominated by the
background and by anti-aliasing, so crop the regions that carry an accent before trusting it:

```
magick inspiration/<name>.png -crop 300x60+X+Y +repage -colors 8 -format %c histogram:info:- | sort -rn
```

Sample the pixels that carry a role (ground, text, link, accent, chrome). A value read off the
image by eye is a guess; the histogram is the measurement.

## Step 3: look at the image

Read the image with the image-reading tool, at full size. Everything in `[LAYOUT]` and `[META]`
comes from actually looking at it: column structure, what sits in the nav, how many levels the
hierarchy has, where the whitespace is, what carries the visual weight.

## Step 4: write the file

Same stem, same directory, `.txt`. Fill the template exactly. No em-dash and no en-dash; these
files are tracked, so the repo prose gate scans them.

```
<name>.png
site: <who published it, domain where known>
period: <year or year range, from the filename or the page itself>
dimensions: <width>x<height>
sampled: <YYYY-MM-DD, today>

[PALETTE]
ground    #rrggbb  role: page bg   <short hue note>
surface   #rrggbb  role: surface   <short hue note>
text      #rrggbb  role: body      <short hue note>
link      #rrggbb  role: link      <short hue note>
accent    #rrggbb  role: accent    <short hue note>
matte     #rrggbb  role: backdrop  <short hue note>

[LAYOUT]
<two to four full sentences: column structure, widths, what is in each region>

[META]
<two to four full sentences: the holistic read of the design, not a summary of the above>

[RELEVANCE]
<one line: what it contributes to this template, or that it contributes nothing>
```

Role names are not fixed to the six above. Use the roles the page actually has (for example
`badge`, `panel`, `edge`, `chrome`, `frame`) and drop roles with no counterpart. Keep the column
alignment: name, hex, `role: <role>`, description.

`[RELEVANCE]` is the one section that looks at this repo. It answers a single question: does this
page teach a decision the template has not already made? "Nothing transferable" is a complete
and useful answer, and is the honest one for a page whose look this repo deliberately avoids.

## Step 5: check

```
nu scripts/maintain.nu check
```

It must print `Contract OK`. It also scans the new `.txt` files, so a dash character or a broken
file shows up here rather than later. `nu scripts/maintain.nu check` needs the fixtures to be
current; if it complains about staleness, that is unrelated to this skill and means the payload
was edited without regenerating.
