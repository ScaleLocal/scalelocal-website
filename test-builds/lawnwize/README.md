# LawnWize Website

A self-contained, five-page static website for LawnWize — lawn care and grounds maintenance in Livingston County, Michigan.

## Viewing the Site Locally

No server or build step needed. Unzip the folder anywhere and double-click `index.html`. Every page works straight from your computer; the only things loaded from the internet are the Google Fonts (Playfair Display and Inter) and the Google Map on the contact page. Without internet, the site still renders fully using system fonts.

## Folder Structure

```
lawnwize/
├── index.html        Homepage (hero carousel, services, about preview, gallery preview)
├── services.html     All four service lines with full sub-service detail
├── about.html        Story, core standards, team, service area
├── gallery.html      Photo gallery
├── contact.html      Estimate request form, contact info, hours, service-area map
├── 404.html          Not-found page
├── css/site.css      All styling (one file, responsive)
├── js/site.js        Hero carousel, mobile nav, estimate form (vanilla JS, no frameworks)
└── images/           All photos, logo, favicon
```

## Updating Content

- **Copy / text:** open the relevant `.html` file in any text editor and edit the text between the tags. Phone number, hours, and service area appear in the utility bar (top) and footer of every page — update all six pages if those change.
- **Photos:** replace files in `images/` keeping the same filenames (`hero-1.jpg` through `hero-4.jpg` for the homepage carousel, `gallery-01.jpg` onward for the gallery, `service-*.jpg` for the four service images). Recommended sizes: heroes ~1920px wide, gallery ~1100px wide.
- **Logo:** `images/logo-lawnwize.svg` is the standalone logo file. The header and footer logos are drawn inline inside each HTML file (search for `aria-label="LawnWize"`).
- **Estimate form:** the contact form currently opens a pre-filled email to info@lawnwize.com in the visitor's mail app. To connect a real form provider (Formspree, Basin, Netlify Forms, or a CRM), see the comment block inside `contact.html` above the form, and remove the form handler section in `js/site.js`.
- **Contact launcher:** the floating button in the bottom-right corner (on every page) opens a panel with three actions: text, free estimate, and call. It is fully static — no live chat, no third-party scripts. Edit the panel text by searching any `.html` file for `lw-launcher`.

## Hosting

Any static host works — the whole site is plain HTML/CSS/JS:

- **Netlify:** drag the unzipped folder onto https://app.netlify.com/drop — live in under a minute.
- **GitHub Pages:** push the folder to a repository and enable Pages in repo settings.
- **Traditional shared hosting:** upload the folder contents to your web root (e.g. `public_html/`) via FTP or your host's file manager.

## What's Not Included (By Design)

This is a clean handoff build. The following were intentionally left out and can be added whenever you're ready:

- No