# Lessons Learned & Codebase Utilities

This page documents system tools, environmental setups, and engineering decisions.

## 🛠️ Codebase Tooling
1. **`tools/dir-tree.sh`**: Prints the directory structure while ignoring generated folders like `_site`, `docs`, and `node_modules`.
2. **`tools/diff.sh`**: Utility script utilizing Diffmerge to check configurations across testing, development, and production paths.
3. **`tools/assert-url.js`**: Node.js script that replaces relative image pathways in markdown files with raw GitHub master paths to prevent broken links on rendering.

## 🚀 Environment Configurations
1. **Jekyll Static Site Generation**: Managed via `codex.yaml` which defines setup scripts to configure Ruby, Bundler, and Jekyll.
2. **ST_BarcodeMap Compilation**:
   - Compiling `ST_BarcodeMap` locally requires Boost 1.73.0, HDF5 1.10.7, and Zlib 1.2.11.
   - **Lesson Learned**: System makefiles do not natively support Conda path resolution. The makefile was customized to map `INCLUDE_DIRS` and `LIBRARY_DIRS` to `$CONDA_PREFIX` paths.
   - **Alternative**: Building via GitHub Actions workflow is faster and avoids local library conflicts.

## 🔑 Git Authentication Wrapper Bypass
- **Problem**: The IDE injects a dummy `GITHUB_TOKEN` which shadows local authentication keys (e.g. `gh auth`).
- **Solution**: Bypass the shadow token by running push commands with:
  ```bash
  env -u GITHUB_TOKEN git push origin main
  ```

## 🎨 UI & Responsive Layout Optimization
1. **Light Theme Glassmorphism**:
   - Background image scaling can make text hard to read if the frosted-glass background is too opaque.
   - Decreasing `--glass-bg` to `rgba(254, 253, 250, 0.45)` and `--bg-overlay` to `rgba(254, 253, 250, 0.5)` maximizes background visibility while maintaining accessibility and readability when combined with a `backdrop-filter: blur(16px)` layer.
2. **Mobile Ribbon Blockage**:
   - Elements like `#forkongithub` absolute-positioned ribbons can overlay the main nav bar on mobile devices.
   - Resolution: Hide these elements entirely on viewports under 800px.
3. **Vanilla JS Touch Swipes**:
   - Custom sliders without external frameworks (like FlexSlider or Swiper) require manual tracking of `touchstart` and `touchend` events.
   - Event listeners must be registered with `{ passive: true }` to maintain smooth scrolling performance.

