# CLAUDE (CSS and Styling Component Context)

This package contains stylesheets and UI design variables for the BSGOU public website.

## 1. UI Styling Constraints & Specs

- **Dual-Theme Mechanics**:
  - Class `.dark-theme` is applied to the `<body>` element to override CSS properties.
  - Maintain HSL-derived color tokens for primary backgrounds, text, and accent colors.
- **Glassmorphism Design Tokens**:
  - Background overlay should have high transparency showing hero backgrounds.
  - Always enforce `backdrop-filter: blur(16px)` and `-webkit-backdrop-filter: blur(16px)` for text readability.
  - Enforce glass border values exactly as specified in `SPEC.md`.
- **Responsive Mobile Offsets**:
  - Fork ribbon `#forkongithub` **must be hidden** on screens narrower than `800px`.
  - Grid layout: card columns set to `repeat(auto-fit, minmax(280px, 1fr))` with `16px` gaps.
- **Slider Touch Swipe**:
  - Swiping threshold is set to `50px` for transitioning slides (Left/Right swipe).
  - Touch event listeners in JS must be registered with `{ passive: true }`.

---

## 2. Local Files & Customization

- **style.css**: Core customized styles, theme overrides, grid alignments, and glassmorphic overlays.
- **bootstrap.min.css**: Upstream library styles; do not edit directly.
- **flexslider.css**: Carousel slider styling.

---

## 3. Styling Standards

- **No Tailwind CSS**: Use Vanilla CSS for custom styles to maintain layout consistency.
- **Micro-Animations**: Use smooth animations (`transition: transform 0.3s ease, box-shadow 0.3s ease`) on interactive card hover states.
