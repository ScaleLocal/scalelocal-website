# Home Services / Trades Template — ScaleLocal

## Niche Coverage
Plumbing, HVAC, Electrical, Roofing, Sealcoating, Tree Service, Landscaping, Painting, General Contractors, Cleaning Services

## Design Philosophy
**Bold. Trustworthy. Action-Oriented.**
This isn't a brochure — it's a conversion machine with personality. Every scroll should feel intentional. Every section earns the next.

## Tech Stack
- Single-file HTML with embedded CSS + JS (no external dependencies except fonts + CDN libs)
- Three.js for hero background particle/mesh effects
- GSAP (GreenSock) for scroll-triggered animations
- Intersection Observer API for reveal-on-scroll
- CSS custom properties for easy theming
- CSS Grid + Flexbox for layouts
- Smooth scroll with momentum
- Responsive: mobile-first with 768px and 1200px breakpoints

## Color System (Configurable via CSS Variables)
- `--primary`: Brand primary (e.g., #1A1A1A for dark trades, #0047AB for clean/professional)
- `--accent`: CTA/highlight color (e.g., #FCB514 gold, #FF6B35 orange)
- `--accent-secondary`: Supporting accent
- `--surface`: Background surfaces
- `--text`: Body copy
- `--text-light`: Secondary text
- `--gradient-start` / `--gradient-end`: Hero gradient overlay

## Page Structure

### 1. HERO (Full viewport, immersive)
- **Background**: Three.js animated mesh/particle system OR full-bleed video with dark overlay
- **Content**: Badge → H1 with animated text reveal → Subhead → Dual CTA buttons
- **Trust strip**: Animated counter bar (years, projects, rating) with number count-up on scroll
- **Scroll indicator**: Animated chevron bounce at bottom
- **Mobile**: Simplified particles, stacked CTAs

### 2. SERVICES SHOWCASE (Interactive cards)
- **Layout**: Asymmetric grid (not boring 3x2)
- **Cards**: Hover → 3D tilt effect (vanilla JS tilt), icon morphs, gradient border reveal
- **Each card**: Number badge, icon, title, description, "Learn More" with arrow animation
- **Mobile**: Horizontal scroll carousel with snap points

### 3. WHY CHOOSE US (Split layout with parallax)
- **Left**: Large parallax image with floating badge overlays (ratings, certifications)
- **Right**: Staggered feature list with icon + title + description
- **Animation**: Each feature slides in from right on scroll
- **Background**: Subtle diagonal stripe pattern

### 4. PROCESS TIMELINE (Horizontal scroll on desktop)
- **Desktop**: Horizontal scrolling timeline with connected nodes
- **Each step**: Number, icon, title, description
- **Animation**: Line draws between nodes as you scroll, nodes pulse on activation
- **Mobile**: Vertical timeline with alternating sides

### 5. REVIEWS / SOCIAL PROOF (Carousel with depth)
- **Layout**: 3D perspective carousel showing 3 cards (center card elevated)
- **Each review**: Stars, quote, name, service type, Google/Yelp badge
- **Auto-rotate** with pause on hover
- **Background**: Gradient mesh or subtle pattern

### 6. SERVICE AREA MAP (Interactive)
- **Embedded map** with custom styling (dark mode map)
- **Surrounding**: List of towns served with hover highlighting
- **Badge overlay**: "Proudly Serving [X] Communities"

### 7. CTA BAND (Conversion section)
- **Full-width**: Dark gradient background
- **Content**: Bold headline, subtext, phone number with click-to-call
- **Animation**: Subtle background particle drift
- **Phone number**: Large, bold, gold/accent colored

### 8. FOOTER (Premium feel)
- **Multi-column**: Logo + about, Quick links, Services, Contact info
- **Bottom bar**: Copyright, powered by ScaleLocal, social links
- **Subtle animation**: Links have underline slide effect

## Animations & Effects Catalog
1. **Scroll reveal**: Elements fade-up with stagger (GSAP ScrollTrigger)
2. **3D card tilt**: Mousemove-based perspective transform on service cards
3. **Counter animation**: Numbers count up when section enters viewport
4. **Text split reveal**: Hero text animates letter-by-letter or word-by-word
5. **Parallax layers**: Background images move at different scroll speeds
6. **Magnetic buttons**: CTAs subtly follow cursor on hover
7. **Gradient border**: Cards get animated gradient border on hover
8. **Line draw**: SVG path animation for timeline connector
9. **Smooth scroll**: CSS scroll-behavior + JS for anchor navigation
10. **Loading screen**: Brief branded loading animation on first visit

## Responsive Strategy
- **Desktop (1200px+)**: Full experience, all animations, 3D effects
- **Tablet (768-1199px)**: Simplified grid, reduced parallax, touch-friendly
- **Mobile (<768px)**: Stacked layout, no 3D tilt, simplified hero, swipe carousels

## Performance Targets
- First Contentful Paint: <1.5s
- Largest Contentful Paint: <2.5s
- Three.js loaded async, doesn't block render
- GSAP loaded from CDN with defer
- Images lazy-loaded with blur-up placeholders
- All fonts preloaded

## Placeholder System
All content uses {{VARIABLE}} placeholders for easy find-and-replace:
- {{BUSINESS_NAME}}, {{PHONE}}, {{EMAIL}}, {{ADDRESS}}
- {{CITY}}, {{STATE}}, {{SERVICE_AREA}}
- {{TAGLINE}}, {{HERO_HEADLINE}}, {{HERO_SUBHEAD}}
- {{SERVICE_1_TITLE}}, {{SERVICE_1_DESC}}, etc.
- {{REVIEW_1_TEXT}}, {{REVIEW_1_NAME}}, etc.
- {{YEARS_EXPERIENCE}}, {{PROJECTS_COMPLETED}}, {{GOOGLE_RATING}}
