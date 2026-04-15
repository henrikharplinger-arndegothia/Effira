const puppeteer = require('puppeteer-core');
const path = require('path');

const HTML_FILE = path.resolve(__dirname, 'Boardmeeting April.html');
const PDF_OUT  = path.resolve(__dirname, 'Boardmeeting April.pdf');
const CHROME   = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

// 16:9 at 96dpi → 1280×720px
const WIDTH_PX  = 1280;
const HEIGHT_PX = 720;

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 2 });
  await page.goto('file://' + HTML_FILE, { waitUntil: 'networkidle0' });

  // Count slides
  const slideCount = await page.evaluate(() =>
    document.querySelectorAll('.slide').length
  );
  console.log(`Found ${slideCount} slides`);

  // Inject print CSS: stack all slides as full-height pages
  await page.addStyleTag({ content: `
    @page { size: ${WIDTH_PX}px ${HEIGHT_PX}px; margin: 0; }
    * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    body { overflow: visible !important; height: auto !important; }
    .deck { height: auto !important; }
    .slide {
      position: relative !important;
      opacity: 1 !important;
      pointer-events: auto !important;
      display: block !important;
      width: 100vw !important;
      height: 100vh !important;
      page-break-after: always !important;
      break-after: page !important;
    }
    .slide-inner { height: 100vh !important; }
    .arrow-nav, .brand-logo { display: none !important; }
  `});

  await page.pdf({
    path: PDF_OUT,
    width:  WIDTH_PX  + 'px',
    height: HEIGHT_PX + 'px',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });

  await browser.close();
  console.log('PDF saved to:', PDF_OUT);
})();
