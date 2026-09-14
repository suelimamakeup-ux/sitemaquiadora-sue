(function() {
  // Header Glassmorphism on Scroll
  const header = document.querySelector('header');
  if (header) {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }

  // Mobile Menu Toggle
  const navToggle = document.querySelector('.nav-toggle');
  const navMenu = document.getElementById('nav-menu');
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', function() {
      const isOpen = navMenu.classList.toggle('open');
      this.setAttribute('aria-expanded', isOpen);
    });
    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Lightbox & Filter
  const allPortfolioItems = Array.from(document.querySelectorAll('.portfolio-item'));
  let visibleItems = allPortfolioItems.filter(item => !item.classList.contains('hidden'));

  const lightbox = document.getElementById('lightbox');
  const lbImg = document.getElementById('lightbox-img');
  const lightboxClose = document.querySelector('.lightbox-close');
  const lightboxPrev = document.querySelector('.lightbox-prev');
  const lightboxNext = document.querySelector('.lightbox-next');
  let currentIndex = 0;
  let lastFocusedElement = null;

  function openLightbox(index) {
    currentIndex = index;
    const currentItem = visibleItems[index];
    lastFocusedElement = currentItem;
    const img = currentItem.querySelector('img');
    lbImg.src = img.src;
    lbImg.alt = img.alt;
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
    lightboxClose.focus();
  }

  function closeLightbox() {
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
    if (lastFocusedElement) {
      lastFocusedElement.focus();
    }
  }

  function navigate(dir) {
    currentIndex = (currentIndex + dir + visibleItems.length) % visibleItems.length;
    const currentItem = visibleItems[currentIndex];
    const img = currentItem.querySelector('img');
    lbImg.src = img.src;
    lbImg.alt = img.alt;
  }

  function trapFocus(e) {
    if (!lightbox.classList.contains('open')) return;
    const focusableElements = [lightboxClose, lightboxPrev, lightboxNext];
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    }
  }

  const portfolioGrid = document.querySelector('.portfolio-grid');
  if (portfolioGrid) {
    portfolioGrid.addEventListener('click', e => {
      const item = e.target.closest('.portfolio-item');
      if (item && !item.classList.contains('hidden')) {
        const idx = visibleItems.indexOf(item);
        if (idx !== -1) openLightbox(idx);
      }
    });
    portfolioGrid.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        const item = e.target.closest('.portfolio-item');
        if (item && !item.classList.contains('hidden')) {
          e.preventDefault();
          const idx = visibleItems.indexOf(item);
          if (idx !== -1) openLightbox(idx);
        }
      }
    });
  }

  // Portfolio Carousel & Progress Bar
  const pTrack = document.querySelector('.portfolio-grid');
  const pPrevBtn = document.querySelector('.portfolio-carousel-btn.prev');
  const pNextBtn = document.querySelector('.portfolio-carousel-btn.next');
  let progressBarFill = null;

  if (pTrack) {
    // Cria barra de progresso automaticamente se não existir no DOM
    const carouselWrapper = document.querySelector('.portfolio-carousel-wrapper');
    if (carouselWrapper && !carouselWrapper.querySelector('.portfolio-progress-bar')) {
      const pBar = document.createElement('div');
      pBar.className = 'portfolio-progress-bar';
      pBar.setAttribute('aria-hidden', 'true');
      progressBarFill = document.createElement('div');
      progressBarFill.className = 'portfolio-progress-fill';
      pBar.appendChild(progressBarFill);
      carouselWrapper.appendChild(pBar);
    }

    const updatePortfolioProgress = () => {
      if (!progressBarFill) return;
      const maxScroll = pTrack.scrollWidth - pTrack.clientWidth;
      if (maxScroll <= 0) {
        progressBarFill.style.width = '100%';
        progressBarFill.style.transform = 'translateX(0)';
      } else {
        const progress = Math.min(1, Math.max(0, pTrack.scrollLeft / maxScroll));
        const visibleRatio = Math.max(0.15, pTrack.clientWidth / pTrack.scrollWidth);
        progressBarFill.style.width = `${visibleRatio * 100}%`;
        const moveRange = 100 - (visibleRatio * 100);
        progressBarFill.style.transform = `translateX(${progress * (pTrack.clientWidth - (pTrack.clientWidth * visibleRatio))}px)`;
      }
    };

    pTrack.addEventListener('scroll', updatePortfolioProgress, { passive: true });
    window.addEventListener('resize', updatePortfolioProgress, { passive: true });
    setTimeout(updatePortfolioProgress, 100);

    if (pPrevBtn && pNextBtn) {
      pPrevBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const firstItem = pTrack.querySelector('.portfolio-item:not(.hidden)');
        if (firstItem) {
          const itemWidth = firstItem.offsetWidth + 20;
          pTrack.scrollBy({ left: -itemWidth, behavior: 'smooth' });
        }
      });
      pNextBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const firstItem = pTrack.querySelector('.portfolio-item:not(.hidden)');
        if (firstItem) {
          const itemWidth = firstItem.offsetWidth + 20;
          pTrack.scrollBy({ left: itemWidth, behavior: 'smooth' });
        }
      });
    }
  }

  lightboxClose?.addEventListener('click', closeLightbox);
  lightboxPrev?.addEventListener('click', () => navigate(-1));
  lightboxNext?.addEventListener('click', () => navigate(1));
  lightbox?.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });
  document.addEventListener('keydown', e => {
    if (!lightbox.classList.contains('open')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') navigate(-1);
    if (e.key === 'ArrowRight') navigate(1);
    trapFocus(e);
  });

  const filterBtns = document.querySelectorAll('.filter-btn');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filterValue = btn.getAttribute('data-filter');

      allPortfolioItems.forEach(item => {
        if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
          item.classList.remove('hidden');
        } else {
          item.classList.add('hidden');
        }
      });

      visibleItems = allPortfolioItems.filter(item => !item.classList.contains('hidden'));
      if (pTrack) {
        pTrack.scrollTo({ left: 0, behavior: 'smooth' });
        setTimeout(() => {
          const evt = new Event('scroll');
          pTrack.dispatchEvent(evt);
        }, 150);
      }
    });
  });

  // FAQ Accordion
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    if (!question) return;
    question.addEventListener('click', () => {
      const isActive = item.classList.contains('active');
      faqItems.forEach(otherItem => {
        if (otherItem !== item) {
          otherItem.classList.remove('active');
          const otherQ = otherItem.querySelector('.faq-question');
          if (otherQ) otherQ.setAttribute('aria-expanded', 'false');
        }
      });
      item.classList.toggle('active');
      question.setAttribute('aria-expanded', !isActive);
    });
  });

  // Scroll Spy
  const navLinks = document.querySelectorAll('.nav-menu a');
  const sections = document.querySelectorAll('main section[id]');
  if (navLinks.length && sections.length) {
    const spyObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          navLinks.forEach(link => {
            if (link.getAttribute('href') === `#${id}`) {
              link.setAttribute('aria-current', 'page');
            } else if (link.getAttribute('href')?.startsWith('#')) {
              link.removeAttribute('aria-current');
            }
          });
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });

    sections.forEach(sec => spyObserver.observe(sec));
  }

  // Staggered Reveal Animations (Details Vault style)
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  // Agrupa cards em containers para aplicar delays progressivos
  const containerGroups = [
    '.experience-timeline',
    '.pillars-grid',
    '.testimonials-grid',
    '.credentials-badges'
  ];

  containerGroups.forEach(groupSelector => {
    const group = document.querySelector(groupSelector);
    if (group) {
      const children = Array.from(group.children);
      children.forEach((child, index) => {
        child.classList.add('reveal', `reveal-delay-${Math.min(5, (index % 5) + 1)}`);
        revealObserver.observe(child);
      });
    }
  });

  document.querySelectorAll('.section-header, .credentials-content, .hero-text, .hero-image-frame, .credentials-image, .faq-item').forEach(el => {
    el.classList.add('reveal');
    revealObserver.observe(el);
  });
})();
