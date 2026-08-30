(function() {
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

  const pTrack = document.querySelector('.portfolio-grid');
  const pPrevBtn = document.querySelector('.portfolio-carousel-btn.prev');
  const pNextBtn = document.querySelector('.portfolio-carousel-btn.next');
  if (pTrack && pPrevBtn && pNextBtn) {
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
    });
  });

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add('visible');
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.section-header, .step-card, .pillar-card, .portfolio-item, .credentials-content, .hero-text, .testimonial-card').forEach(el => {
    el.classList.add('reveal');
    revealObserver.observe(el);
  });
})();
