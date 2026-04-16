# Template Spec: Salon / Spa / Beauty / Medspa

## Template Identity
- **Name:** Velvet Rose Salon & Spa Template
- **Niche:** Salons, Spas, Beauty Studios, Medspas
- **File:** `templates/salon-spa/index.html`
- **Preview:** `scalelocal.net/test-builds/temp/salons/`
- **Vibe:** Luxury, warmth, aspiration -- opposite energy from the Home Services template

## Design Philosophy
Sexy. Elegant. Aspirational. Every scroll should feel like stepping into a high-end spa. Warm tones, flowing animations, and premium imagery designed to make someone want to book immediately.

## Color Palette
- Primary: Deep charcoal `#2D2226`
- Accent: Rose gold `#C4956A`
- Rose: `#D4A0A0`
- Blush: `#F5E6E0`
- Cream: `#FAF6F3`
- Deep Plum: `#4A2D3F` (promo backgrounds)
- Surface Dark: `#1A1115` (dark sections)

## Typography
- Headings: Cormorant Garamond (serif, elegant, italic accents)
- Body: Montserrat (clean sans-serif, light weight)

## Tech Stack
- Single-file HTML, all CSS/JS embedded
- GSAP + ScrollTrigger for scroll animations
- Lenis for smooth scroll
- Custom cursor with magnetic hover effects
- Canvas particle system (cursor-reactive)
- Animated gradient mesh background
- Loading sequence with character reveal + wipe transition
- Scroll progress bar
- No Three.js, no external frameworks

## Sections (in order)
1. Loading Screen (character-by-character logo reveal, progress bar, wipe transition)
2. Navigation (glassmorphism on scroll, mobile slide-out)
3. Hero (full-viewport, parallax bg, character-level text reveal, trust strip with counters)
4. Marquee Strip (scrolling service categories)
5. Services Menu (tabbed: Hair/Skin/Nails/Body, animated category switching, 3D card tilt on hover)
6. Photo Break: Aspirational Quote (parallax image, serif italic quote)
7. About / Experience (image + floating card + accent box, feature list with hover icons)
8. Gallery (masonry grid, hover zoom, lightbox on click)
9. Photo Break: Stats (animated counters for reviews, artists, services)
10. Team / Artists (image cards with grayscale-to-color hover, overlay booking links)
11. Reviews (featured quote slider with auto-rotate, dot navigation)
12. Promo / Special Offer (deep plum bg, animated radial gradients, urgency badge)
13. Packages / Membership (3-tier pricing with monthly/annual toggle, featured card)
14. Gift Cards (3 preset amounts + custom input, glassmorphism cards)
15. Client Portal (feature list + mockup dashboard showing upcoming/past appointments, login modal)
16. Comparison Chart (Velvet Rose vs. Others, animated row reveals)
17. Contact / Booking (info + hours + form, form with accent border)
18. Map (grayscale filtered Google Maps embed with overlay card)
19. Instagram Strip (6 images, hover overlay with icon)
20. Footer (4-column with social links prominent)
21. Booking Modal (multi-step: service select, date picker, time slots, confirmation)
22. Portal Login Modal

## Placeholder Variables
Use `{{VARIABLE_NAME}}` format. Key variables:
- `{{BUSINESS_NAME}}`, `{{PHONE}}`, `{{EMAIL}}`, `{{ADDRESS}}`
- `{{CITY}}`, `{{STATE}}`, `{{BOOKING_URL}}`
- `{{TAGLINE}}`, `{{HERO_HEADLINE}}`, `{{HERO_SUBHEAD}}`
- `{{SERVICE_CATEGORY_1-4}}` with items, prices, durations
- `{{STYLIST_1-4_NAME}}`, `{{STYLIST_1-4_TITLE}}`
- `{{REVIEW_1-5_TEXT}}`, `{{REVIEW_1-5_NAME}}`
- `{{PROMO_HEADLINE}}`, `{{PROMO_DETAILS}}`
- `{{PACKAGE_1-3_NAME}}`, `{{PACKAGE_1-3_PRICE}}`, `{{PACKAGE_1-3_FEATURES}}`
- `{{INSTAGRAM_URL}}`, `{{FACEBOOK_URL}}`

Sample business used: "Velvet Rose Salon & Spa" in Beverly Hills, CA.

## Interactive Features
- Service tabs with animated category switching
- Monthly/annual package pricing toggle
- Multi-step booking modal (service > date > time > confirmation)
- Gift card purchase with custom amount
- Client portal login modal
- Gallery lightbox
- Reviews auto-rotating slider
- Custom cursor with magnetic button effects
- Back to top button

## Responsive Breakpoints
- Desktop: 1200px+ (full animations, cursor, particle system, multi-column)
- Tablet: 768px-1199px (simplified grid, no custom cursor)
- Mobile: <768px (stacked, swipe-friendly, large tap targets, no particles)

## Performance
- GSAP loaded async/defer
- Lenis loaded async/defer
- Images lazy-loaded
- Particles reduced on mobile (50 desktop, 20 mobile)
- Custom cursor hidden on mobile
- will-change hints on animated elements

## Deployment Paths
- Source: `templates/salon-spa/index.html`
- Preview: `test-builds/temp/salons/index.html`
- Also at: `test-builds/temp/beauty/index.html`
- Workspace: `Templates/Website_Templates/salon-spa/index.html`
