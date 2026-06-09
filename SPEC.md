# UI and Styling Design Specification

This document provides the official technical specifications for the styling, layouts, theme mechanics, and interaction behaviors of the BSGOU website.

---

## 1. Theme and Color System

The website implements a dual-theme styling system (Light and Dark) that toggles via class application on the `<body>` element (`.dark-theme`).

### 1.1. Default Light Theme
Derived from color schemes in the reference visual assets (`124112083.jpeg`), using a warm, ivory, and soft earth palette.
- **Primary Background (`--bg-primary`):** `#fefdfa`
- **Secondary Background (`--bg-secondary`):** `#faf6f0`
- **Primary Text (`--text-primary`):** `#2d2520` (Dark slate brown)
- **Secondary Text (`--text-secondary`):** `#61564f`
- **Pink Accent (`--accent-pink` / `--accent-pink-hover`):** `#e06b5a` / `#c55343`
- **Blue Accent (`--accent-blue` / `--accent-blue-hover`):** `#4a8ab7` / `#396e94`
- **Background Image (`--bg-image`):** `url('../img/quote.jpg')`
- **Icon Filter (`--icon-filter`):** `contrast(1.2) saturate(1.2) brightness(0.9)` (Heightened contrast for accessibility on light background)

### 1.2. Dark Theme Override
Inspired by visual colors from the reference asset (`2.jpg`), using a cool steel, slate-blue, and vibrant neon accents.
- **Primary Background (`--bg-primary`):** `#1e262c`
- **Secondary Background (`--bg-secondary`):** `#12181d`
- **Primary Text (`--text-primary`):** `#f0f4f8`
- **Secondary Text (`--text-secondary`):** `#8b9aa6`
- **Pink Accent (`--accent-pink` / `--accent-pink-hover`):** `#f472b6` / `#ec4899`
- **Blue Accent (`--accent-blue` / `--accent-blue-hover`):** `#06b6d4` / `#0891b2`
- **Background Image (`--bg-image`):** `url('../img/quote copy.jpg')`
- **Icon Filter (`--icon-filter`):** `none`

---

## 2. Glassmorphism Mechanics

Both themes utilize a glassmorphic visual system for card elements, sticky headers, and layout sections. The goal is to provide a premium feel with high transparency showing the underlying background image while maintaining content contrast.

- **Glass Background (`--glass-bg`):**
  - **Light Theme:** `rgba(254, 253, 250, 0.45)` (Higher transparency)
  - **Dark Theme:** `rgba(18, 24, 29, 0.72)`
- **Glass Border (`--glass-border`):**
  - **Light Theme:** `rgba(180, 160, 140, 0.15)`
  - **Dark Theme:** `rgba(255, 255, 255, 0.08)`
- **Overlay Background (`--bg-overlay`):**
  - **Light Theme:** `rgba(254, 253, 250, 0.5)` (Lower opacity to maximize visibility of hero/quote backgrounds)
  - **Dark Theme:** `rgba(18, 24, 29, 0.85)`
- **Backdrop Blur:** A standard `backdrop-filter: blur(16px)` / `-webkit-backdrop-filter: blur(16px)` is applied to all glass elements to ensure text readability.

---

## 3. Core Values Grid Layout

The `.services` list layout has been optimized for tighter arrangement and improved visual balance.
- **Grid Configuration:** `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))`
- **Gap:** `16px`
- **Card Padding:** `20px`
- **Grid Item Spacing:** `gap: 16px` (Flex gap between icon and title/description)
- **Transition:** A smooth `transform 0.3s ease` and `box-shadow 0.3s ease` is applied to card hover states.

---

## 4. Mobile Layout & Responsive Offsets

- **Ribbon Blocking Fix:** The GitHub fork link ribbon (`#forkongithub`) is suppressed (`display: none`) on screens narrower than `800px` to prevent blocking the header navigation menu.
- **Header Structure:** The sticky header offset is calculated dynamically or handled via padding to ensure no content is obscured on smaller viewports.

---

## 5. Interaction Mechanics & Slider Swipe

The landing page slider implements custom touch swipe gestures for mobile accessibility.
- **Swipe Threshold:** `50px`
- **Gestures:**
  - **Right Swipe:** Translates to `goToSlide(currentIndex - 1)` (Previous) and resets the auto-slide timer.
  - **Left Swipe:** Translates to `goToSlide(currentIndex + 1)` (Next) and resets the auto-slide timer.
- **Listeners:** Added with `{ passive: true }` to avoid scroll performance degradation.
