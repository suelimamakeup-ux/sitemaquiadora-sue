const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
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

  // 3. Scroll suave até "A Profissional"
  console.log('Cena 3: A Profissional');
  await page.locator('#sobre').scrollIntoViewIfNeeded();
  await page.waitForTimeout(2500);

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

  // 15. Scroll até CTA Final
  console.log('Cena 10: CTA Final');
  await page.locator('.action-banner').scrollIntoViewIfNeeded();
  await page.waitForTimeout(2000);

  // 16. Hover no botão final
  await page.hover('.action-banner .btn-luxury-cta');
  await page.waitForTimeout(1500);

  // 17. Mostra WhatsApp flutuante
  console.log('Cena 11: WhatsApp Float');
  await page.hover('.whatsapp-float');
  await page.waitForTimeout(1500);

  // 18. Scroll até o footer
  console.log('Cena 12: Footer');
  await page.locator('footer').scrollIntoViewIfNeeded();
  await page.waitForTimeout(2000);

  // 19. Volta ao topo
  console.log('Cena 13: Volta ao topo');
  await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'smooth' }));
  await page.waitForTimeout(2000);

  // 20. Demonstração do menu mobile
  console.log('Cena 14: Menu Mobile');
  await page.setViewportSize({ width: 375, height: 812 });
  await page.waitForTimeout(1000);
  await page.click('.nav-toggle');
  await page.waitForTimeout(1500);
  await page.click('.nav-toggle');
  await page.waitForTimeout(1000);

  // 21. Volta para desktop
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.waitForTimeout(1000);

  console.log('Gravação concluída!');
  console.log('Use OBS Studio para gravar a janela do navegador.');

  await browser.close();
})();
