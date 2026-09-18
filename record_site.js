const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const videoDir = path.join(__dirname, '.temp_video');
  if (!fs.existsSync(videoDir)) {
    fs.mkdirSync(videoDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
    recordVideo: {
      dir: videoDir,
      size: { width: 1920, height: 1080 }
    }
  });
  const page = await context.newPage();

  const sitePath = path.join(__dirname, 'site_maquiadora_sue.html');
  await page.goto(`file:///${sitePath.replace(/\\/g, '/')}`);
  await page.waitForTimeout(2000);

  // 1. Hero - Página carrega
  console.log('Cena 1: Hero');
  await page.waitForTimeout(3000);

  // 2. Hover no botão CTA
  console.log('Cena 2: Botão CTA');
  await page.hover('.btn-luxury-cta');
  await page.waitForTimeout(1500);

  // 3. Scroll suave até "A Profissional" e marcos de autoridade
  console.log('Cena 3: A Profissional e Credenciais');
  await page.locator('#sobre').scrollIntoViewIfNeeded();
  await page.waitForTimeout(1500);
  const badges = await page.locator('.badge-item').all();
  for (let i = 0; i < badges.length; i++) {
    await badges[i].hover();
    await page.waitForTimeout(800);
  }
  await page.waitForTimeout(1000);

  // 4. Scroll até "A Experiência"
  console.log('Cena 4: A Experiência');
  await page.locator('#experiencia').scrollIntoViewIfNeeded();
  await page.waitForTimeout(2000);

  // 5. Mostra cada card de etapa
  const stepCards = await page.locator('.step-card').all();
  for (let i = 0; i < stepCards.length; i++) {
    await stepCards[i].scrollIntoViewIfNeeded();
    await page.waitForTimeout(1500);
  }

  // 6. Scroll até "Especialidades"
  console.log('Cena 5: Especialidades');
  await page.locator('#servicos').scrollIntoViewIfNeeded();
  await page.waitForTimeout(2000);

  // 7. Mostra cada pillar card
  const pillarCards = await page.locator('.pillar-card').all();
  for (let i = 0; i < pillarCards.length; i++) {
    await pillarCards[i].scrollIntoViewIfNeeded();
    await page.waitForTimeout(1500);
  }

  // 8. Hover no botão "Conhecer Pacotes"
  console.log('Cena 6: Botão WhatsApp');
  await page.hover('.btn-pillar');
  await page.waitForTimeout(1000);

  // 9. Scroll até Portfólio
  console.log('Cena 7: Portfólio');
  await page.locator('.portfolio-section').scrollIntoViewIfNeeded();
  await page.waitForTimeout(2000);

  // 10. Abre o lightbox
  console.log('Cena 8: Lightbox');
  await page.locator('.portfolio-item').first().click();
  await page.waitForTimeout(1500);

  // 11. Navega no lightbox
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(1000);
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(1000);
  await page.keyboard.press('ArrowLeft');
  await page.waitForTimeout(1000);

  // 12. Fecha o lightbox
  await page.keyboard.press('Escape');
  await page.waitForTimeout(1000);

  // 13. Scroll até Depoimentos
  console.log('Cena 9: Depoimentos');
  await page.locator('.testimonials-section').scrollIntoViewIfNeeded();
  await page.waitForTimeout(2500);

  // 14. Mostra cada depoimento
  const testimonials = await page.locator('.testimonial-card').all();
  for (let i = 0; i < testimonials.length; i++) {
    await testimonials[i].scrollIntoViewIfNeeded();
    await page.waitForTimeout(1500);
  }

  // 15. Scroll até Perguntas Frequentes (FAQ)
  console.log('Cena 10: FAQ Accordion');
  await page.locator('#faq').scrollIntoViewIfNeeded();
  await page.waitForTimeout(1500);
  const faqQuestions = await page.locator('.faq-question').all();
  if (faqQuestions.length > 0) {
    await faqQuestions[0].click();
    await page.waitForTimeout(2000);
    if (faqQuestions.length > 1) {
      await faqQuestions[1].click();
      await page.waitForTimeout(2000);
    }
  }

  // 16. Scroll até CTA Final
  console.log('Cena 11: CTA Final');
  await page.locator('.action-banner').scrollIntoViewIfNeeded();
  await page.waitForTimeout(2000);

  // 17. Hover no botão final
  await page.hover('.action-banner .btn-luxury-cta');
  await page.waitForTimeout(1500);

  // 18. Mostra WhatsApp flutuante com tooltip
  console.log('Cena 12: WhatsApp Float com Tooltip');
  await page.hover('.whatsapp-float');
  await page.waitForTimeout(2000);

  // 19. Scroll até o footer
  console.log('Cena 13: Footer');
  await page.locator('footer').scrollIntoViewIfNeeded();
  await page.waitForTimeout(2000);

  // 20. Volta ao topo e mostra seletor de idioma minimalista
  console.log('Cena 14: Volta ao topo e Seletor de Idioma');
  await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'smooth' }));
  await page.waitForTimeout(1500);
  await page.hover('.lang-switch');
  await page.waitForTimeout(1500);

  // 21. Demonstração do menu mobile
  console.log('Cena 15: Menu Mobile');
  await page.setViewportSize({ width: 375, height: 812 });
  await page.waitForTimeout(1000);
  await page.click('.nav-toggle');
  await page.waitForTimeout(1500);
  await page.click('.nav-toggle');
  await page.waitForTimeout(1000);

  // 22. Demonstração do Biosite (Link na Bio)
  console.log('Cena 16: Biosite (Instagram)');
  await page.setViewportSize({ width: 400, height: 850 });
  const biositePath = path.join(__dirname, 'biosite.html');
  await page.goto(`file:///${biositePath.replace(/\\/g, '/')}`);
  await page.waitForTimeout(2500);
  await page.hover('.btn-link.featured');
  await page.waitForTimeout(2000);
  await page.evaluate(() => window.scrollTo({ top: 300, behavior: 'smooth' }));
  await page.waitForTimeout(2500);

  console.log('Gravação e demonstração concluídas com sucesso!');

  // Salva o caminho do vídeo antes de fechar a página
  const videoPath = await page.video().path();
  await page.close();
  await context.close();
  await browser.close();

  const finalVideoPath = path.join(__dirname, 'demo_maquiadora_sue.mp4');
  if (fs.existsSync(finalVideoPath)) {
    try { fs.unlinkSync(finalVideoPath); } catch (e) {}
  }
  
  if (fs.existsSync(videoPath)) {
    fs.copyFileSync(videoPath, finalVideoPath);
    console.log(`Novo vídeo de demonstração salvo em: ${finalVideoPath}`);
    try {
      fs.rmSync(videoDir, { recursive: true, force: true });
    } catch (e) {}
  }
})();
