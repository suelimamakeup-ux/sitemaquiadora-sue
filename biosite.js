/**
 * Biosite - Alternância de Idiomas Dinâmica (sem redirecionar)
 * Suporte a: Português (PT), Inglês (EN), Espanhol (ES)
 */
(function() {
  'use strict';

  const translations = {
    pt: {
      htmlLang: 'pt-BR',
      pageTitle: 'Maquiadora Sue | Link na Bio',
      profileRole: 'Por Sue Lima • Makeup & Hair Artist',
      profileBio: 'Maquiagem e penteado de alta durabilidade para <strong>noivas</strong>, <strong>debutantes</strong>, <strong>shooting</strong>, <strong>produções sociais</strong> e <strong>audiovisual</strong> pelo mundo.',
      jornadaTitle: 'Trajetória & Autoridade',
      jornadaText: 'Com formação internacional na prestigiada escola <strong>Make Up For Ever em Nova York</strong>, especializei-me em técnicas de alta durabilidade, estudando com os maiores nomes do mercado. Integrei também por mais de 5 anos a equipe de caracterização da <strong>Fox Sports</strong> na TV.',
      badges: [
        'MUFE Nova York',
        '5+ Anos Fox Sports',
        'Pele Resistente',
        'Atendimento Exclusivo'
      ],
      linkWhatsapp: 'Conversar no WhatsApp • Orçamentos',
      linkSite: 'Site Oficial & Portfólio Completo',
      linkExp: 'A Experiência Noiva Sue Lima',
      linkDebutantes: 'Debutantes & Produção Social',
      linkFaq: 'Dúvidas Frequentes (FAQ)',
      siteUrl: 'site_maquiadora_sue.html',
      siteUrlExp: 'site_maquiadora_sue.html#experiencia',
      siteUrlServ: 'site_maquiadora_sue.html#servicos',
      siteUrlFaq: 'site_maquiadora_sue.html#faq',
      waMessage: 'Olá Sue! Vim pelo seu link da bio e gostaria de solicitar um orçamento para o meu evento.',
      waFooterMessage: 'Olá Sue! Vim pelo seu link da bio e gostaria de tirar algumas dúvidas.'
    },
    en: {
      htmlLang: 'en',
      pageTitle: 'Maquiadora Sue | Link in Bio',
      profileRole: 'By Sue Lima • Makeup & Hair Artist',
      profileBio: 'Long-lasting makeup and hair styling for <strong>brides</strong>, <strong>debutantes</strong>, <strong>shootings</strong>, <strong>social productions</strong> and <strong>audiovisual</strong> worldwide.',
      jornadaTitle: 'Trajectory & Authority',
      jornadaText: 'With international education at the prestigious <strong>Make Up For Ever Academy in New York</strong>, I specialized in high-durability techniques, learning from leading industry artists. I also spent over 5 years on the <strong>Fox Sports</strong> characterization & makeup TV team.',
      badges: [
        'MUFE New York',
        '5+ Years Fox Sports',
        'Long-Wear Skin',
        'Exclusive Service'
      ],
      linkWhatsapp: 'Chat on WhatsApp • Inquiries',
      linkSite: 'Official Website & Full Portfolio',
      linkExp: 'The Bridal Experience Sue Lima',
      linkDebutantes: 'Debutantes & Social Production',
      linkFaq: 'Frequently Asked Questions (FAQ)',
      siteUrl: 'site_maquiadora_sue_en.html',
      siteUrlExp: 'site_maquiadora_sue_en.html#experiencia',
      siteUrlServ: 'site_maquiadora_sue_en.html#servicos',
      siteUrlFaq: 'site_maquiadora_sue_en.html#faq',
      waMessage: 'Hello Sue! I visited your link in bio and would like to request an inquiry for my event.',
      waFooterMessage: 'Hello Sue! I visited your link in bio and would like to ask some questions.'
    },
    es: {
      htmlLang: 'es',
      pageTitle: 'Maquiadora Sue | Enlace en Bio',
      profileRole: 'Por Sue Lima • Makeup & Hair Artist',
      profileBio: 'Maquillaje y peinado de alta durabilidad para <strong>novias</strong>, <strong>quinceañeras</strong>, <strong>shooting</strong>, <strong>producciones sociales</strong> y <strong>audiovisual</strong> por el mundo.',
      jornadaTitle: 'Trayectoria y Autoridad',
      jornadaText: 'Con formación internacional en la prestigiosa escuela <strong>Make Up For Ever en Nueva York</strong>, me especialicé en técnicas de alta durabilidad. También integré durante más de 5 años el equipo de caracterización y maquillaje de <strong>Fox Sports</strong> en televisión.',
      badges: [
        'MUFE Nueva York',
        '5+ Años Fox Sports',
        'Piel Resistente',
        'Atención Exclusiva'
      ],
      linkWhatsapp: 'Chatear en WhatsApp • Presupuestos',
      linkSite: 'Sitio Oficial y Portafolio Completo',
      linkExp: 'La Experiencia Novia Sue Lima',
      linkDebutantes: 'Quinceañeras y Eventos Sociales',
      linkFaq: 'Preguntas Frecuentes (FAQ)',
      siteUrl: 'site_maquiadora_sue_es.html',
      siteUrlExp: 'site_maquiadora_sue_es.html#experiencia',
      siteUrlServ: 'site_maquiadora_sue_es.html#servicos',
      siteUrlFaq: 'site_maquiadora_sue_es.html#faq',
      waMessage: '¡Hola Sue! Visité tu enlace en bio y me gustaría solicitar un presupuesto para mi evento.',
      waFooterMessage: '¡Hola Sue! Visité tu enlace en bio y me gustaría consultar algunas dudas.'
    }
  };

  function setLanguage(lang) {
    const data = translations[lang];
    if (!data) return;

    document.documentElement.lang = data.htmlLang;
    document.title = data.pageTitle;

    // Profile
    const roleEl = document.querySelector('.profile-role');
    if (roleEl) roleEl.innerHTML = data.profileRole;

    const bioEl = document.querySelector('.profile-bio');
    if (bioEl) bioEl.innerHTML = data.profileBio;

    // Jornada
    const jornadaTitleEl = document.getElementById('jornada-title');
    if (jornadaTitleEl) {
      jornadaTitleEl.innerHTML = `<i class="fa-solid fa-star" aria-hidden="true"></i> ${data.jornadaTitle}`;
    }

    const jornadaTextEl = document.querySelector('.jornada-card > p');
    if (jornadaTextEl) {
      jornadaTextEl.innerHTML = data.jornadaText;
    }

    // Badges
    const badgeElements = document.querySelectorAll('.bio-badges .bio-badge');
    if (badgeElements.length === 4) {
      const badgeIcons = [
        '<i class="fa-solid fa-crown" aria-hidden="true"></i> ',
        '<i class="fa-solid fa-star" aria-hidden="true"></i> ',
        '<i class="fa-solid fa-wand-magic" aria-hidden="true"></i> ',
        '<i class="fa-solid fa-heart" aria-hidden="true"></i> '
      ];
      badgeElements.forEach((badge, index) => {
        badge.innerHTML = badgeIcons[index] + data.badges[index];
      });
    }

    // Links text & URLs
    const waLink = document.querySelector('.btn-link.featured');
    if (waLink) {
      waLink.href = `https://wa.me/5521995421808?text=${encodeURIComponent(data.waMessage)}`;
      const textSpan = waLink.querySelector('.link-text');
      if (textSpan) textSpan.textContent = data.linkWhatsapp;
    }

    const siteLink = document.querySelector('.btn-link[data-link="site"]');
    if (siteLink) {
      siteLink.href = data.siteUrl;
      const textSpan = siteLink.querySelector('.link-text');
      if (textSpan) textSpan.textContent = data.linkSite;
    }

    const expLink = document.querySelector('.btn-link[data-link="experiencia"]');
    if (expLink) {
      expLink.href = data.siteUrlExp;
      const textSpan = expLink.querySelector('.link-text');
      if (textSpan) textSpan.textContent = data.linkExp;
    }

    const servLink = document.querySelector('.btn-link[data-link="servicos"]');
    if (servLink) {
      servLink.href = data.siteUrlServ;
      const textSpan = servLink.querySelector('.link-text');
      if (textSpan) textSpan.textContent = data.linkDebutantes;
    }

    const faqLink = document.querySelector('.btn-link[data-link="faq"]');
    if (faqLink) {
      faqLink.href = data.siteUrlFaq;
      const textSpan = faqLink.querySelector('.link-text');
      if (textSpan) textSpan.textContent = data.linkFaq;
    }

    // Footer WhatsApp link
    const footerWa = document.querySelector('.social-icons a[data-social="whatsapp"]');
    if (footerWa) {
      footerWa.href = `https://wa.me/5521995421808?text=${encodeURIComponent(data.waFooterMessage)}`;
    }

    // Update active class on buttons
    document.querySelectorAll('.lang-option').forEach(btn => {
      if (btn.getAttribute('data-lang') === lang) {
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
      } else {
        btn.classList.remove('active');
        btn.setAttribute('aria-pressed', 'false');
      }
    });

    try {
      localStorage.setItem('sue_biosite_lang', lang);
    } catch (e) {}
  }

  document.addEventListener('DOMContentLoaded', function() {
    const langButtons = document.querySelectorAll('.lang-option');
    langButtons.forEach(btn => {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        const selectedLang = this.getAttribute('data-lang');
        if (selectedLang) {
          setLanguage(selectedLang);
        }
      });
    });

    let savedLang = 'pt';
    try {
      savedLang = localStorage.getItem('sue_biosite_lang') || 'pt';
    } catch (e) {}

    if (savedLang && savedLang !== 'pt' && translations[savedLang]) {
      setLanguage(savedLang);
    }
  });
})();
