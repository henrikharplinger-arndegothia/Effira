const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720 });

  const filePath = 'file://' + path.resolve(__dirname, 'Boardmeeting April.html');
  await page.goto(filePath, { waitUntil: 'networkidle0' });

  // Count slides
  const slideCount = await page.evaluate(() => document.querySelectorAll('.slide').length);
  console.log(`Found ${slideCount} slides`);

  const { PDFDocument } = require('pdf-lib');
  const pages = [];

  for (let i = 0; i < slideCount; i++) {
    await page.evaluate((idx) => {
      const slides = document.querySelectorAll('.slide');
      slides.forEach(s => s.classList.remove('active'));
      slides[idx].classList.add('active');
      // update body class
      const inner = slides[idx].querySelector('.slide-inner');
      document.body.className = '';
      if (inner.classList.contains('dark')) document.body.classList.add('slide-dark');
      else if (inner.classList.contains('accent')) document.body.classList.add('slide-accent');
      else document.body.classList.add('slide-light');
    }, i);

    await new Promise(r => setTimeout(r, 150));

    const pdfBytes = await page.pdf({
      width: '1280px',
      height: '720px',
      printBackground: true,
    });
    pages.push(pdfBytes);
    process.stdout.write(`\rProcessed slide ${i + 1}/${slideCount}`);
  }

  console.log('\nMerging pages...');
  const merged = await PDFDocument.create();
  for (const pdfBytes of pages) {
    const doc = await PDFDocument.load(pdfBytes);
    const [copiedPage] = await merged.copyPages(doc, [0]);
    merged.addPage(copiedPage);
  }

  const fs = require('fs');
  fs.writeFileSync(path.resolve(__dirname, 'Boardmeeting April.pdf'), await merged.save());
  console.log('Done! Boardmeeting April.pdf updated.');

  await browser.close();
})();
