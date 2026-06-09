# UI Refactor Plan: Index.html Modernization

## Overview
This document records the strategic modernization of the BSGOU public landing page (`index.html`). The refactor aligns with BSGOU's [[values]] of "Open Innovation" and "Global Inclusivity" by ensuring a performant, accessible, and lightweight digital presence.

## Historical Context & Chat Sessions
Following a deep review of the codebase, project [[timeline]], and chat sessions (Session ID: `65057ccc`), it was identified that the original `index.html` relied on outdated, heavy jQuery dependencies (`v1.8.2`) and legacy plugins (`flexslider`, `quicksand`, `fancybox`, `sticky`, `tinynav`, `anchorScroll`).

The community decided to:
1. Strip all jQuery dependencies.
2. Replace legacy plugins with native HTML5/CSS3 and lightweight Vanilla JS.
3. Prioritize a **Dynamic Theme Switcher** featuring both a clean, professional **Light Theme** (default) and a sleek **Dark Theme**, controlled by an accessible toggle button and `localStorage`.
4. Implement a clean, sliding responsive **vanilla JS carousel** for the hero section.

## Goals & Technical Specs
- **Accessibility & SEO**: Fix viewport scaling issues, implement semantic HTML tags (`<header>`, `<main>`, `<dialog>`), and add appropriate meta tags/alt attributes.
- **Performance**: Drastically reduce page weight by relying on CSS Grid, Flexbox, and CSS-based animations (`transition`, `scroll-behavior: smooth`).
- **Resilience**: Ensure the new `custom.js` is thoroughly checked to prevent any dead-end logic loops or memory leaks from orphaned event listeners.
- **Multilingual Support**: Enhance the existing `switchLanguage(lang)` function to persist user preferences via `localStorage`, fulfilling the goal of global outreach.

## Integration with BSGOU Mission
This UI refactor directly supports the [[overview|BSGOU Mission]] by providing an accessible ecosystem dashboard. A modern, fast website ensures that global researchers and students can easily access protocols, blog posts, and tools without experiencing browser lag or accessibility barriers.

## Modernization Execution Highlights
- **Touch Swipes**: Native touch gesture support added via `touchstart` and `touchend` event handlers to ensure seamless mobile swiping.
- **Light Theme Transparency**: Re-engineered `--glass-bg` and `--bg-overlay` variables to utilize lower opacity (`0.45` and `0.5` respectively) to showcase the background image clearly while preserving legibility via back-drop blur filters.

## Related Links
- [[readme]]: Main project context.
- [[lessons-learned]]: For details on bypassing IDE git credentials, Jekyll environments, and UI layout optimization lessons.
