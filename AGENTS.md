# AGENTS.md — Maquiadora Sue Website

## Project Type
Static HTML/CSS website for a makeup artist (Maquiadora Sue). No build tools, no package manager, no tests.

## Structure
- `site_maquiadora_sue.html` — Full institutional site (portfolio, testimonials, sections)
- `biosite.html` — Link-in-bio page (WhatsApp CTA, social links)
- `shared.css` — Shared styles (variables, typography, buttons, utilities)
- `site.css` — Site-specific styles
- `biosite.css` — Biosite-specific styles
- `fontawesome.css` + `fonts/` — Self-hosted FontAwesome (biosite only)
- Image assets: `.webp` files for portfolio and profile

## Key Facts
- **Language:** Portuguese (Brazil)
- **Domain:** maquiadorasue.com.br
- **WhatsApp:** +55-21-99542-1808 (all CTAs link here)
- **Fonts:** Lato + Playfair Display (Google Fonts)
- **Icons:** FontAwesome 6.4.0 (CDN in site, self-hosted in biosite)
- **Lightbox:** Custom vanilla JS in site_maquiadora_sue.html (keyboard navigation, mobile swipe)

## CSS Variables
```css
--gold-accent: #D4AF37;
--text-dark: #1C1C1C;
--bg-luxury: #FDFBF9;
```

## Workflow
- Open HTML files directly in browser (no server required)
- Test responsive behavior at 992px breakpoint (mobile menu toggle)
- Test lightbox: click portfolio image → arrow keys/ESC to navigate/close
- Test WhatsApp links open in new tab

## Gotchas
- `biosite.html` uses self-hosted FontAwesome; `site_maquiadora_sue.html` uses CDN version
- Image filenames contain underscores (e.g., `Nova_Foto_Perfil.webp`) — use exact filenames in code
- Both files share `shared.css` but have separate page-specific CSS
- Lightbox JS is inline in `site_maquiadora_sue.html` (lines 277-347)
