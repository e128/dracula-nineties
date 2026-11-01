# 1990s Web Design: Research Notes

Reference notes gathered on 2026-11-01 while adding thirteen period screenshots to this folder.
The images are third-party captures of public home pages, kept as design references. The source
for each file is listed under Provenance below.

## Sources

- Web Design Museum, "Web Design in the 90s" exhibition and year galleries, https://www.webdesignmuseum.org/exhibitions/web-design-in-the-90s
- Web Design Museum, individual gallery entries, https://www.webdesignmuseum.org/gallery
- Version Museum, website history exhibits, https://www.versionmuseum.com/
- Jennifer Niederst, Web Design in a Nutshell, O'Reilly, 1999. Chapters on tables, frames, animated GIFs and the Web Palette.
- "Web Design Hints and Tips", irt.org, March 1999, https://www.irt.org/articles/js152/
- Jakob Nielsen, "Why Frames Suck (Most of the Time)", Nielsen Norman Group, December 1996, https://www.nngroup.com/articles/why-frames-suck-most-of-the-time/
- HubSpot, "A Look Back at 30+ Years of Website Design", https://blog.hubspot.com/marketing/look-back-20-years-website-design
- W3C specifications used as the period record: CSS1 (17 December 1996), HTML 3.2 (14 January 1997), HTML 4.0 (18 December 1997), CSS2 (12 May 1998), WCAG 1.0 (5 May 1999), HTML 4.01 (24 December 1999).

## Timeline

**1991 to 1993: hypertext, not design.** Pages are text, headings and links. Tim Berners-Lee's
first site is a document with no layout, and early academic sites follow it. The browser supplies
every visual property: Times body text, blue unvisited links, grey page ground, a rule under
headings. There is no stylesheet and no image.

**1994 to 1995: the home page appears.** Companies put a single page online and treat it as a
sign. Layout arrives through images: a logo, an image map, a row of buttons. Netscape's default
grey becomes the accidental national background. Pages are built for 640x480 and often left
aligned, because centering costs markup and does nothing on a fixed monitor.

**1996: the table becomes a layout engine.** HTML tables are used with `cellpadding`,
`cellspacing`, `border=0` and transparent spacer GIFs to build columns, gutters and fixed widths.
Animated GIFs, hit counters, guestbooks, tiled backgrounds, `marquee`, `blink`, MIDI files and
Java applets appear. Macromedia Flash ships in 1996 and Shockwave is already in use, so home
pages begin to gate themselves behind plugins. The 216-color web-safe palette is the working
constraint on 256-color displays.

**1997 to 1998: brands build portals.** Nested tables reach their peak. Home pages become dense
directories of channels, promotions and partner logos. Framesets are common despite the known
usability cost. Splash pages, chrome bevels, lens flares and dark textured grounds mark the
multimedia era. HTML 3.2 and HTML 4.0 standardize what designers already do, while CSS1 support
is partial and inconsistent.

**1999: density and commerce.** Table layouts still dominate. Portals and marketplaces compress
search, categories, promotions and trust badges into one screen. CSS2 exists on paper but is not
a dependable layout tool, so the fixed-width table remains the production method. E-commerce
adds another density layer: prices, counts, guarantees and partner badges.

## Visual vocabulary

- **Fixed width.** The page is a pixel-width table, commonly 600 or 760 pixels, with a left or
  center alignment. Nothing reflows. Horizontal scrolling is a failure.
- **Nested tables.** Rows, columns, gutters and colored panels are table cells. Spacer GIFs hold
  empty space open. Borders become visible rules when a page wants structure.
- **Colored grounds.** A `bgcolor` or a tiled GIF fills the page. Common choices are black,
  navy, steel blue, cream or a textured grey. A white content column on a colored ground is a
  standard composition.
- **System type.** Times New Roman, Georgia, Arial, Helvetica, Verdana, Trebuchet MS and Courier.
  Sizes come from `font size` or `FONT` tags, not a scale. Headings are often bold body text.
- **Default link colors.** Unvisited blue `#0000EE`, visited purple `#551A8B`, active red. Links
  are always underlined. Color is the only state cue.
- **Bevel chrome.** Buttons and panels use light top-left and dark bottom-right borders to fake
  depth. Gradients are made from repeated one-pixel GIFs or image slices.
- **Image navigation.** Image maps, icon bars, tab images, circular hubs and logo collages. A
  text link list below the image map is the accessibility fallback and also the search engine
  fallback.
- **Motion.** Animated GIFs, scrolling status bar text, marquees, blinking text, MIDI soundtracks,
  Java applets and Flash. Motion is usually decorative, and often the loudest element on a page.
- **Social proof.** Hit counters, guestbooks, award badges, "best viewed with" logos and "under
  construction" signs. These are content in their own right, not footer decoration.
- **Splash pages.** A first screen with one image and an Enter link, often requiring Shockwave or
  Flash. The site is behind the splash, not on it.
- **Palette discipline by constraint.** The web-safe palette is a 6x6x6 cube with channel values
  00, 33, 66, 99, CC and FF, for 216 colors that do not dither on 256-color displays. Saturated
  primaries are common because they survive the constraint.

## Why it looked that way

- **Dial-up.** A 14.4 or 28.8 kbps modem makes image weight the first design constraint. Every
  decorative GIF is a download the visitor waits for.
- **Display.** 640x480 is the common target, 800x600 is rising, and 256 colors is the assumed
  depth. A page that needs more fails for a large share of the audience.
- **Browser wars.** Netscape and Internet Explorer render differently and add proprietary tags.
  Designers test in both and accept the lowest common result.
- **No usable CSS.** CSS1 arrives in December 1996, but support through 1999 is partial. Tables
  and presentational HTML are the reliable layout tools, so the period look is a side effect of
  the available engine.
- **No web fonts.** Face choice is limited to what the operating system already has. Font stacks
  and image-rendered wordmarks carry brand.
- **Frames.** A frameset keeps navigation in one pane and content in another. It breaks the page
  model: bookmarks, links, printing, Back and search indexing all suffer. Nielsen documents the
  cost in 1996; designers use frames anyway.

## Post-1999 idioms to keep out

The audit cap in AGENTS.md stops at 1999, so these are the tells of a later default rather than
period technique:

- Rounded cards, soft drop shadows and flat neutral chrome.
- A fluid responsive grid as the default composition.
- A system-UI sans stack as the body face.
- Icon-only navigation with no text label.
- Generous whitespace as the primary hierarchy device, with no rule or bevel.
- Hover or focus styling that replaces the visible default link color.

## Provenance

All thirteen images were downloaded from Web Design Museum gallery entries on 2026-11-01. The
museum page for each file names the archived capture it reproduces. These are reference copies,
not original artwork owned by this repo.

| File | Site | Period | Museum entry |
| --- | --- | --- | --- |
| google-1998.png | google.com | 1998 | https://www.webdesignmuseum.org/gallery/google-1998 |
| cnn-1995.png | cnn.com | 1995 | https://www.webdesignmuseum.org/gallery/cnn-com-1995 |
| microsoft-1996.png | microsoft.com | 1996 | https://www.webdesignmuseum.org/gallery/microsoft-1996 |
| whitehouse-1995.png | whitehouse.gov | 1995 | https://www.webdesignmuseum.org/gallery/the-white-house-1995 |
| nasa-1997.png | nasa.gov | 1997 | https://www.webdesignmuseum.org/gallery/nasa-1997 |
| disney-1997.png | disney.com | 1997 | https://www.webdesignmuseum.org/gallery/disney-1997 |
| hotmail-1997.png | hotmail.com | 1997 | https://www.webdesignmuseum.org/gallery/hotmail-1997 |
| ebay-1999.png | ebay.com | 1999 | https://www.webdesignmuseum.org/gallery/ebay-in-1999 |
| bbc-1995.png | bbcnc.org.uk | 1995 | https://www.webdesignmuseum.org/gallery/bbc-1995 |
| mcdonalds-1996.png | mcdonalds.com | 1996 | https://www.webdesignmuseum.org/gallery/mcdonald-s-1996 |
| pepsi-1996.png | pepsi.com | 1996 | https://www.webdesignmuseum.org/gallery/pepsi-1996 |
| nintendo-1998.png | nintendo.com | 1998 | https://www.webdesignmuseum.org/gallery/nintendo-1998 |
| ask-jeeves-1999.png | askjeeves.com | 1999 | https://www.webdesignmuseum.org/gallery/ask-jeeves-1999 |
