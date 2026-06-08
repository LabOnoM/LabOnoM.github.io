/**
 * BSGOU Modernized Client-Side Logic
 * Vanilla JavaScript (Zero Dependencies, Zero jQuery)
 */

document.addEventListener("DOMContentLoaded", () => {
  // ==========================================
  // 1. Theme Switcher (Light / Dark Mode)
  // ==========================================
  const themeToggleBtn = document.getElementById("theme-toggle-btn");
  
  const applyTheme = (theme) => {
    if (theme === "dark") {
      document.body.classList.add("dark-theme");
      if (themeToggleBtn) themeToggleBtn.innerHTML = "&#9789;"; // Moon icon
    } else {
      document.body.classList.remove("dark-theme");
      if (themeToggleBtn) themeToggleBtn.innerHTML = "&#9788;"; // Sun icon
    }
    localStorage.setItem("bsgou-theme", theme);
  };

  const savedTheme = localStorage.getItem("bsgou-theme");
  const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  if (savedTheme === "dark" || (!savedTheme && systemDark)) {
    applyTheme("dark");
  } else {
    applyTheme("light");
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", () => {
      const isDark = document.body.classList.contains("dark-theme");
      applyTheme(isDark ? "light" : "dark");
    });
  }

  // ==========================================
  // 2. Responsive mobile navigation toggle
  // ==========================================
  const menuToggleBtn = document.getElementById("menu-toggle-btn");
  const navigation = document.getElementById("navigation");

  if (menuToggleBtn && navigation) {
    menuToggleBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      navigation.classList.toggle("nav-open");
    });

    document.addEventListener("click", () => {
      navigation.classList.remove("nav-open");
    });

    navigation.querySelectorAll("#menu a").forEach((link) => {
      link.addEventListener("click", () => {
        navigation.classList.remove("nav-open");
      });
    });
  }

  // ==========================================
  // 3. Scroll spy - active menu navigation link
  // ==========================================
  const sections = document.querySelectorAll("header, section");
  const navLinks = document.querySelectorAll("#menu a");

  window.addEventListener("scroll", () => {
    let currentId = "home";
    const scrollPos = window.scrollY + 100; // offset for sticky navbar

    sections.forEach((section) => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
        currentId = section.getAttribute("id") || "home";
      }
    });

    navLinks.forEach((link) => {
      link.classList.remove("active");
      const href = link.getAttribute("href");
      if (href === `#${currentId}` || (currentId === "home" && href === "#home")) {
        link.classList.add("active");
      }
    });
  });

  // ==========================================
  // 4. Vanilla Slider / Carousel
  // ==========================================
  const initSlider = (sliderEl) => {
    const slidesContainer = sliderEl.querySelector(".slides");
    const slides = sliderEl.querySelectorAll(".slides > li");
    if (!slidesContainer || slides.length === 0) return;

    let currentIndex = 0;
    const slideCount = slides.length;
    let intervalId = null;

    const goToSlide = (index) => {
      currentIndex = (index + slideCount) % slideCount;
      slidesContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
    };

    const startAutoSlide = () => {
      intervalId = setInterval(() => {
        goToSlide(currentIndex + 1);
      }, 6000);
    };

    const stopAutoSlide = () => {
      if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
      }
    };

    startAutoSlide();

    sliderEl.addEventListener("mouseenter", stopAutoSlide);
    sliderEl.addEventListener("mouseleave", startAutoSlide);
  };

  document.querySelectorAll(".flexslider").forEach(initSlider);

  // ==========================================
  // 5. Works Gallery Category Filtering
  // ==========================================
  const filterButtons = document.querySelectorAll("#filterOptions li a");
  const galleryItems = document.querySelectorAll(".ourHolder .gallery-item");

  filterButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();

      document.querySelectorAll("#filterOptions li").forEach((li) => {
        li.classList.remove("active");
      });
      button.parentElement.classList.add("active");

      const filterClass = button.getAttribute("class");

      galleryItems.forEach((item) => {
        const itemType = item.getAttribute("data-type");
        if (filterClass === "all" || itemType === filterClass) {
          item.style.display = "block";
        } else {
          item.style.display = "none";
        }
      });
    });
  });

  // ==========================================
  // 6. Native dialog modal overlays
  // ==========================================
  const dialog = document.getElementById("gallery-dialog");
  const dialogCloseBtn = document.getElementById("dialog-close-btn");
  const dialogTitle = document.getElementById("dialog-title");
  const dialogDesc = document.getElementById("dialog-desc");
  const dialogMedia = document.getElementById("dialog-media-container");
  const dialogCta = document.getElementById("dialog-cta-btn");

  galleryItems.forEach((item) => {
    item.addEventListener("click", () => {
      const title = item.getAttribute("data-title");
      const desc = item.getAttribute("data-desc");
      const url = item.getAttribute("data-url");
      const mediaType = item.getAttribute("data-media-type");

      if (dialog && dialogTitle && dialogDesc && dialogMedia && dialogCta) {
        dialogTitle.textContent = title;
        dialogDesc.textContent = desc;
        dialogCta.href = url;

        if (mediaType === "video") {
          dialogMedia.style.display = "block";
          dialogMedia.innerHTML = `<iframe src="${url}" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
        } else {
          dialogMedia.style.display = "none";
          dialogMedia.innerHTML = "";
        }

        dialog.showModal();
      }
    });
  });

  if (dialogCloseBtn && dialog) {
    const closeDialog = () => {
      dialog.close();
      if (dialogMedia) dialogMedia.innerHTML = "";
    };

    dialogCloseBtn.addEventListener("click", closeDialog);

    dialog.addEventListener("click", (e) => {
      if (e.target === dialog) {
        closeDialog();
      }
    });
  }
});
