require('dotenv').config();
const express = require('express');
const OpenAI = require('openai');
const cors = require('cors');
const path = require('path');
const https = require('https');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.dirname(__filename)));
app.get('/', (req, res) => res.sendFile(path.join(path.dirname(__filename), 'agent.html')));

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// ── Savings lookup (same data as the JSON file) ──
const SAVINGS = {"SE4":{"BV":{"hus 1":{"nej":{"2023":2800,"2024":2310},"sol":{"2023":4770,"2024":4360},"elbil":{"2023":3096,"2024":2483},"sol+elbil":{"2023":5066,"2024":4533}},"hus 2":{"nej":{"2023":3878,"2024":3054},"sol":{"2023":5848,"2024":5104},"elbil":{"2023":4316,"2024":3310},"sol+elbil":{"2023":6286,"2024":5360}},"hus 3":{"nej":{"2023":5169,"2024":4425},"sol":{"2023":7139,"2024":6475},"elbil":{"2023":5681,"2024":4723},"sol+elbil":{"2023":7651,"2024":6773}},"hus 4":{"nej":{"2023":7255,"2024":6421},"sol":{"2023":9225,"2024":8471},"elbil":{"2023":7989,"2024":6850},"sol+elbil":{"2023":9959,"2024":8900}}},"LV":{"hus 1":{"nej":{"2023":3686,"2024":2873},"sol":{"2023":5656,"2024":4923},"elbil":{"2023":4050,"2024":3086},"sol+elbil":{"2023":6020,"2024":5135}},"hus 2":{"nej":{"2023":4724,"2024":3786},"sol":{"2023":6694,"2024":5836},"elbil":{"2023":5218,"2024":4074},"sol+elbil":{"2023":7188,"2024":6124}},"hus 3":{"nej":{"2023":6918,"2024":6235},"sol":{"2023":8888,"2024":8285},"elbil":{"2023":7522,"2024":6587},"sol+elbil":{"2023":9492,"2024":8637}},"hus 4":{"nej":{"2023":8655,"2024":8422},"sol":{"2023":10625,"2024":10472},"elbil":{"2023":9397,"2024":8855},"sol+elbil":{"2023":11367,"2024":10905}}},"FL":{"hus 1":{"nej":{"2023":4610,"2024":3607},"sol":{"2023":6580,"2024":5657},"elbil":{"2023":5004,"2024":3837},"sol+elbil":{"2023":6974,"2024":5887}},"hus 2":{"nej":{"2023":6602,"2024":5658},"sol":{"2023":8572,"2024":7707},"elbil":{"2023":7132,"2024":5967},"sol+elbil":{"2023":9102,"2024":8017}},"hus 3":{"nej":{"2023":9130,"2024":7962},"sol":{"2023":11100,"2024":10012},"elbil":{"2023":9792,"2024":8348},"sol+elbil":{"2023":11762,"2024":10398}},"hus 4":{"nej":{"2023":10243,"2024":9551},"sol":{"2023":12213,"2024":11601},"elbil":{"2023":12994,"2024":11431},"sol+elbil":{"2023":14964,"2024":13481}}}},"SE3":{"BV":{"hus 1":{"nej":{"2023":2176,"2024":2259},"sol":{"2023":3773,"2024":3897},"elbil":{"2023":2383,"2024":2487},"sol+elbil":{"2023":3980,"2024":4126}},"hus 2":{"nej":{"2023":3002,"2024":2801},"sol":{"2023":4599,"2024":4440},"elbil":{"2023":3309,"2024":3082},"sol+elbil":{"2023":4906,"2024":4720}},"hus 3":{"nej":{"2023":4030,"2024":3915},"sol":{"2023":5627,"2024":5553},"elbil":{"2023":4389,"2024":4229},"sol+elbil":{"2023":5986,"2024":5867}},"hus 4":{"nej":{"2023":5651,"2024":5379},"sol":{"2023":7248,"2024":7018},"elbil":{"2023":6165,"2024":5758},"sol+elbil":{"2023":7762,"2024":7397}}},"LV":{"hus 1":{"nej":{"2023":2875,"2024":2613},"sol":{"2023":4472,"2024":4251},"elbil":{"2023":3130,"2024":2848},"sol+elbil":{"2023":4726,"2024":4487}},"hus 2":{"nej":{"2023":3673,"2024":3347},"sol":{"2023":5270,"2024":4986},"elbil":{"2023":4019,"2024":3642},"sol+elbil":{"2023":5616,"2024":5280}},"hus 3":{"nej":{"2023":5426,"2024":5321},"sol":{"2023":7023,"2024":6959},"elbil":{"2023":5849,"2024":5660},"sol+elbil":{"2023":7446,"2024":7299}},"hus 4":{"nej":{"2023":6795,"2024":7076},"sol":{"2023":8392,"2024":8714},"elbil":{"2023":7314,"2024":7472},"sol+elbil":{"2023":8911,"2024":9111}}},"FL":{"hus 1":{"nej":{"2023":3620,"2024":3119},"sol":{"2023":5217,"2024":4758},"elbil":{"2023":3896,"2024":3347},"sol+elbil":{"2023":5493,"2024":4985}},"hus 2":{"nej":{"2023":5197,"2024":4746},"sol":{"2023":6794,"2024":6385},"elbil":{"2023":5568,"2024":5026},"sol+elbil":{"2023":7165,"2024":6665}},"hus 3":{"nej":{"2023":7216,"2024":6546},"sol":{"2023":8813,"2024":8184},"elbil":{"2023":7679,"2024":6868},"sol+elbil":{"2023":9276,"2024":8506}},"hus 4":{"nej":{"2023":8233,"2024":7988},"sol":{"2023":9830,"2024":9627},"elbil":{"2023":10159,"2024":8944},"sol+elbil":{"2023":11756,"2024":10582}}}},"SE2":{"BV":{"hus 1":{"nej":{"2023":1886,"2024":2005},"sol":{"2023":3212,"2024":3356},"elbil":{"2023":2093,"2024":2234},"sol+elbil":{"2023":3419,"2024":3584}},"hus 2":{"nej":{"2023":2616,"2024":2485},"sol":{"2023":3942,"2024":3835},"elbil":{"2023":2923,"2024":2765},"sol+elbil":{"2023":4249,"2024":4116}},"hus 3":{"nej":{"2023":3477,"2024":3408},"sol":{"2023":4803,"2024":4759},"elbil":{"2023":3836,"2024":3722},"sol+elbil":{"2023":5161,"2024":5072}},"hus 4":{"nej":{"2023":4883,"2024":4641},"sol":{"2023":6209,"2024":5991},"elbil":{"2023":5397,"2024":5020},"sol+elbil":{"2023":6723,"2024":6370}}},"LV":{"hus 1":{"nej":{"2023":2480,"2024":2296},"sol":{"2023":3806,"2024":3647},"elbil":{"2023":2734,"2024":2532},"sol+elbil":{"2023":4060,"2024":3882}},"hus 2":{"nej":{"2023":3182,"2024":2936},"sol":{"2023":4507,"2024":4286},"elbil":{"2023":3527,"2024":3230},"sol+elbil":{"2023":4853,"2024":4580}},"hus 3":{"nej":{"2023":4643,"2024":4561},"sol":{"2023":5969,"2024":5911},"elbil":{"2023":5066,"2024":4901},"sol+elbil":{"2023":6392,"2024":6251}},"hus 4":{"nej":{"2023":5807,"2024":6020},"sol":{"2023":7133,"2024":7371},"elbil":{"2023":6327,"2024":6417},"sol+elbil":{"2023":7653,"2024":7768}}},"FL":{"hus 1":{"nej":{"2023":3093,"2024":2697},"sol":{"2023":4419,"2024":4048},"elbil":{"2023":3369,"2024":2925},"sol+elbil":{"2023":4695,"2024":4275}},"hus 2":{"nej":{"2023":4425,"2024":4050},"sol":{"2023":5751,"2024":5400},"elbil":{"2023":4796,"2024":4330},"sol+elbil":{"2023":6122,"2024":5680}},"hus 3":{"nej":{"2023":6110,"2024":5533},"sol":{"2023":7436,"2024":6883},"elbil":{"2023":6573,"2024":5855},"sol+elbil":{"2023":7899,"2024":7205}},"hus 4":{"nej":{"2023":6807,"2024":6616},"sol":{"2023":8133,"2024":7967},"elbil":{"2023":8733,"2024":7572},"sol+elbil":{"2023":10059,"2024":8922}}}},"SE1":{"BV":{"hus 1":{"nej":{"2023":1886,"2024":2005},"sol":{"2023":3134,"2024":3276},"elbil":{"2023":2093,"2024":2234},"sol+elbil":{"2023":3341,"2024":3505}},"hus 2":{"nej":{"2023":2616,"2024":2485},"sol":{"2023":3864,"2024":3755},"elbil":{"2023":2923,"2024":2765},"sol+elbil":{"2023":4170,"2024":4036}},"hus 3":{"nej":{"2023":3477,"2024":3408},"sol":{"2023":4725,"2024":4679},"elbil":{"2023":3835,"2024":3722},"sol+elbil":{"2023":5083,"2024":4993}},"hus 4":{"nej":{"2023":4882,"2024":4640},"sol":{"2023":6130,"2024":5911},"elbil":{"2023":5396,"2024":5019},"sol+elbil":{"2023":6644,"2024":6290}}},"LV":{"hus 1":{"nej":{"2023":2479,"2024":2296},"sol":{"2023":3727,"2024":3567},"elbil":{"2023":2734,"2024":2532},"sol+elbil":{"2023":3982,"2024":3802}},"hus 2":{"nej":{"2023":3181,"2024":2935},"sol":{"2023":4429,"2024":4206},"elbil":{"2023":3527,"2024":3230},"sol+elbil":{"2023":4775,"2024":4501}},"hus 3":{"nej":{"2023":4642,"2024":4561},"sol":{"2023":5890,"2024":5832},"elbil":{"2023":5065,"2024":4900},"sol+elbil":{"2023":6313,"2024":6171}},"hus 4":{"nej":{"2023":5807,"2024":6020},"sol":{"2023":7055,"2024":7291},"elbil":{"2023":6326,"2024":6417},"sol+elbil":{"2023":7574,"2024":7687}}},"FL":{"hus 1":{"nej":{"2023":3093,"2024":2697},"sol":{"2023":4341,"2024":3968},"elbil":{"2023":3369,"2024":2925},"sol+elbil":{"2023":4617,"2024":4195}},"hus 2":{"nej":{"2023":4425,"2024":4050},"sol":{"2023":5672,"2024":5320},"elbil":{"2023":4796,"2024":4330},"sol+elbil":{"2023":6043,"2024":5600}},"hus 3":{"nej":{"2023":6109,"2024":5532},"sol":{"2023":7357,"2024":6803},"elbil":{"2023":6572,"2024":5854},"sol+elbil":{"2023":7820,"2024":7125}},"hus 4":{"nej":{"2023":6806,"2024":6616},"sol":{"2023":8054,"2024":7887},"elbil":{"2023":8732,"2024":7571},"sol+elbil":{"2023":9980,"2024":8842}}}}};

// ── City → elområde mapping ──
const CITY_TO_REGION = {
  // SE1 — Norrland nord
  luleå:'SE1', kiruna:'SE1', gällivare:'SE1', boden:'SE1', piteå:'SE1', älvsbyn:'SE1', haparanda:'SE1', kalix:'SE1', arvidsjaur:'SE1',
  // SE2 — Norrland syd / Mellansverige nord
  umeå:'SE2', sundsvall:'SE2', härnösand:'SE2', kramfors:'SE2', örnsköldsvik:'SE2', östersund:'SE2', ånge:'SE2', hudiksvall:'SE2', söderhamn:'SE2', bollnäs:'SE2', ljusdal:'SE2', skellefteå:'SE2',
  // SE3 — Mellansverige (störst, inkl Stockholm & Göteborg)
  stockholm:'SE3', göteborg:'SE3', uppsala:'SE3', västerås:'SE3', örebro:'SE3', linköping:'SE3', norrköping:'SE3', jönköping:'SE3', karlstad:'SE3', eskilstuna:'SE3', gävle:'SE3', borås:'SE3', södertälje:'SE3', halmstad:'SE3', växjö:'SE3', falun:'SE3', borlänge:'SE3', sandviken:'SE3', motala:'SE3', nyköping:'SE3', trollhättan:'SE3', skövde:'SE3', lidköping:'SE3', varberg:'SE3', kungsbacka:'SE3', mölndal:'SE3',
  // SE4 — Sydsverige
  malmö:'SE4', helsingborg:'SE4', lund:'SE4', kristianstad:'SE4', karlskrona:'SE4', kalmar:'SE4', ystad:'SE4', trelleborg:'SE4', landskrona:'SE4', ängelholm:'SE4', eslöv:'SE4', vänersborg:'SE4', uddevalla:'SE4',
};

function cityToRegion(city) {
  if (!city) return null;
  const key = city.toLowerCase().trim();
  return CITY_TO_REGION[key] || null;
}

// Map latitude to elområde (approximate — based on transmission grid boundaries)
function latToRegion(lat) {
  if (lat >= 63.5) return 'SE1';
  if (lat >= 60.0) return 'SE2';
  if (lat >= 56.3) return 'SE3';
  return 'SE4';
}

// Geocode any Swedish address/city string via Nominatim (OpenStreetMap, free)
function geocode(query) {
  return new Promise((resolve) => {
    const q = encodeURIComponent(query + ', Sverige');
    const url = `https://nominatim.openstreetmap.org/search?q=${q}&countrycodes=se&format=json&limit=1&accept-language=sv`;
    const req = https.get(url, { headers: { 'User-Agent': 'Effira-Besparingskalkylator/1.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const results = JSON.parse(data);
          if (results.length) {
            const { lat, lon, display_name } = results[0];
            resolve({ lat: parseFloat(lat), lon: parseFloat(lon), display_name });
          } else {
            resolve(null);
          }
        } catch { resolve(null); }
      });
    });
    req.on('error', () => resolve(null));
    req.setTimeout(4000, () => { req.destroy(); resolve(null); });
  });
}

const KWH_PROFILES = {
  BV: [{id:'hus 1',kwh:6600,max:7700},{id:'hus 2',kwh:8800,max:10700},{id:'hus 3',kwh:12600,max:15050},{id:'hus 4',kwh:17500,max:99999}],
  LV: [{id:'hus 1',kwh:9000,max:10100},{id:'hus 2',kwh:11200,max:14525},{id:'hus 3',kwh:17850,max:20175},{id:'hus 4',kwh:22500,max:99999}],
  FL: [{id:'hus 1',kwh:12000,max:14800},{id:'hus 2',kwh:17600,max:21400},{id:'hus 3',kwh:25200,max:28850},{id:'hus 4',kwh:32500,max:99999}]
};

// ── Calculation function ──
async function calculateSavings({ system, region, city, kwh, hustyp, sol, elbil }) {
  // Resolve region: direct > city map > geocode
  if (!region && city) {
    region = cityToRegion(city);
    if (!region) {
      const geo = await geocode(city);
      if (geo) region = latToRegion(geo.lat);
    }
  }
  // Map kWh to house profile
  let hus = hustyp;
  if (!hus && kwh && system && KWH_PROFILES[system]) {
    const profiles = KWH_PROFILES[system];
    let best = profiles[0], bestDist = Math.abs(kwh - best.kwh);
    for (const p of profiles) {
      const d = Math.abs(kwh - p.kwh);
      if (d < bestDist) { bestDist = d; best = p; }
    }
    hus = best.id;
  }
  if (!hus || !region) return null;

  const scenario = sol && elbil ? 'sol+elbil' : sol ? 'sol' : elbil ? 'elbil' : 'nej';

  // Unknown system: calculate across all three, return min-max span with wider band
  if (!system) {
    const systems = ['BV', 'LV', 'FL'];
    const values = systems.map(s => {
      const d = SAVINGS[region]?.[s]?.[hus]?.[scenario];
      return d ? (d['2023'] + d['2024']) / 2 : null;
    }).filter(Boolean);
    if (!values.length) return null;
    const avg = Math.round(values.reduce((a,b) => a+b, 0) / values.length / 500) * 500;
    const low = Math.round(Math.min(...values) * 0.85 / 500) * 500;
    const high = Math.round(Math.max(...values) * 1.15 / 500) * 500;
    return { avg, low, high, hus, scenario, systemUnknown: true };
  }

  const data = SAVINGS[region]?.[system]?.[hus]?.[scenario];
  if (!data) return null;

  const avg = Math.round((data['2023'] + data['2024']) / 2 / 500) * 500;
  const low = Math.round(avg * 0.85 / 500) * 500;
  const high = Math.round(avg * 1.15 / 500) * 500;

  // Calculate component breakdown for explanation
  const breakdown = {};
  const baseData = SAVINGS[region]?.[system]?.[hus]?.['nej'];
  if (baseData) {
    breakdown.opti = Math.round((baseData['2023'] + baseData['2024']) / 2 / 500) * 500;
  }
  if (elbil) {
    const withoutElbilScenario = sol ? 'sol' : 'nej';
    const withoutElbilData = SAVINGS[region]?.[system]?.[hus]?.[withoutElbilScenario];
    if (withoutElbilData) {
      const withoutElbilAvg = (withoutElbilData['2023'] + withoutElbilData['2024']) / 2;
      breakdown.elbil = Math.round((avg - withoutElbilAvg) / 500) * 500;
    }
  }
  if (sol) {
    const withoutSolScenario = elbil ? 'elbil' : 'nej';
    const withoutSolData = SAVINGS[region]?.[system]?.[hus]?.[withoutSolScenario];
    if (withoutSolData) {
      const withoutSolAvg = (withoutSolData['2023'] + withoutSolData['2024']) / 2;
      breakdown.sol = Math.round((avg - withoutSolAvg) / 500) * 500;
    }
  }

  return { avg, low, high, hus, scenario, breakdown, year2023: data['2023'], year2024: data['2024'] };
}

// ── System prompt ──
const SYSTEM_PROMPT = `Du är en vänlig och kunnig energirådgivare som hjälper villaägare räkna ut vad de kan spara med Effiras produkt OPTi — ett styrsystem som optimerar uppvärmning mot elpriset.

Ditt mål: samla in tillräckligt med information för att kunna räkna ut en besparing, sedan presentera resultatet på ett tydligt och engagerande sätt.

## Produktkunskap — OPTi

**Vad OPTi gör:** Tar över styrlagret i värmepumpen och förskjuter uppvärmning och varmvattenproduktion till timmar då elen är billig (typiskt 30 min–2 timmar). Kunden behöver inte göra något — det sker automatiskt.

**Komfortgaranti:** OPTi agerar bara när den lagrade termiska massan redan räcker för att hålla inomhustemperaturen. Temperaturen varierar max ±1°C i Komfortläge, ±2°C i Prisläge. Om systemet tappar kommunikation återgår värmepumpen automatiskt till normal drift.

**Kompatibilitet:** Fungerar med ~95% av alla vattenburna värmepumpar — NIBE, Bosch, IVT, Thermia, Mitsubishi m.fl. Kräver bergvärme, luft/vatten eller frånluft. Fungerar EJ med luft/luft.

**Installation:** Utförs av en Effira-tekniker, ingår i tjänsten. Ingen ombyggnad. Påverkar inte tillverkargarantin.

**Ekonomi:**
- Installationskostnad: ~1 000 kr
- Återbetalningstid: 8–14 månader
- 10× billigare än hembatteri för motsvarande optimeringsnytta
- Solceller: ökar egenanvändning av solel med +35–45% (~2 500 kr/år extra)

**Elavtal:** Fungerar med alla avtal. Maximal besparing kräver kvartsprisavtal (timpris/spotpris). Fast pris ger lägre besparing.

**App:** Effira-appen visar daglig besparing, inställningar och komfortstyrning.

**Produkter:** OPTi Flex (flexibel betalning) och OPTi Standard (abonnemang).

**Om kunden frågar om pris/kostnad:** Hänvisa till effiraenergy.com eller erbjud att koppla dem med en rådgivare — du har inte exakta abonnemangspriser att ge.

**Om kunden frågar om deras specifika värmepumpsmärke:** Om det är NIBE, Bosch, IVT, Thermia eller Mitsubishi — bekräfta att det troligen fungerar. Annars: "Med ~95% täckning är det stor chans att det fungerar — vår tekniker bekräftar vid installation."

Du behöver samla in:
1. Uppvärmningssystem: BV (bergvärme), LV (luft/vatten-värmepump) eller FL (frånluftsvärmepump)
2. Plats — fråga "Var bor du?" och ta emot vad som helst. När kunden svarar: anropa resolve_location med exakt vad de angav. Bekräfta resultatet naturligt, t.ex. "Sandgången 12 — det är Mölndal, bra!" eller "Göteborg, perfekt." Visa ALDRIG "SE1/SE2/SE3/SE4" för kunden. Om orten inte hittas, fråga "Är det i norra, mellersta eller södra Sverige?"
3. Årsförbrukning el i kWh — om de inte vet, fråga efter hustyp/storlek i stället
4. Solceller: ja eller nej
5. Elbil: ja eller nej

OPTi stöder INTE dessa system — avbryt och förklara snällt om kunden nämner något av dessa:
- Luft/luft-värmepump (kallas även "split", "AC-pump" eller "luftpump") — vanligaste misstaget
- Direktel (el-element, golvvärme utan värmepump)
- Fjärrvärme
- Ved/pellets/olja

Om kunden har ett system som inte stöds: berätta det direkt, förklara kort vilka system OPTi fungerar med, och fråga om de har ett sådant eller funderar på byte. Ställ INGA fler frågor om elområde eller förbrukning — det är irrelevant om systemet inte stöds.

Regler:
- Ställ en fråga i taget — håll det naturligt och enkelt
- När du frågar om uppvärmningssystem, lista alltid de tre som stöds: "OPTi fungerar med bergvärme, luft/vatten-värmepump och frånluftsvärmepump — vilket har du?"
- Om kunden svarar "vet inte", "osäker", "ingen aning" eller liknande: säg DIREKT "Inga problem — OPTi kräver att värmen fördelas via radiatorer eller golvvärme (inte fläktar). Vi går vidare och jag räknar ett spann som täcker alla system." Gå sedan omedelbart vidare till nästa fråga. Fråga ALDRIG om systemtypen igen — inte ens en gång till.
- Om användaren nämner flera saker på en gång, extrahera allt och fråga om resten
- Om de inte vet kWh, förklara kort var de hittar det (elräkning/app) och erbjud hustyp som alternativ
- Hustyp är ENBART internt — visa aldrig "hus 1/2/3/4" för kunden. Fråga istället om kvm eller beskriv storleken i vanliga termer ("litet", "stort" etc.). Mappa internt: litet ~100-130 kvm → hus 1, mellanhus ~150-170 kvm → hus 2, stort ~200-220 kvm → hus 3, mycket stort ~250+ kvm → hus 4
- Visa aldrig interna koder (BV/LV/FL/SE1 etc.) för kunden — använd vanliga ord: "bergvärme", "luft/vatten-värmepump", "Norrland" etc.
- Var positiv och ge känslan av ett rådgivande samtal, inte ett formulär
- Använd svenska hela tiden
- Håll svar korta — max 2-3 meningar per tur
- Elbilsbesparing: OPTi styr INTE elbilsladdning. När du presenterar resultatet för en kund med elbil ska du alltid: (1) nämna hur mycket av besparingen som kommer från elbilen (finns i breakdown.elbil i resultatet), (2) förklara att den besparingen förutsätter att kunden laddar när elpriset är lågt — t.ex. nattetid eller när solcellerna producerar. Exempel: "Av de X kr/år kommer ungefär Y kr från elbilen — det förutsätter att du laddar när elpriset är lågt, till exempel nattetid. Det styr du själv, OPTi hjälper dig med resten."

Flöde — följ exakt denna ordning:
1. Samla in: system, plats, kWh eller storlek, solceller, elbil
2. När du har tillräckligt — fråga "Vad är din e-postadress? Då skickar vi kalkylen dit." E-post är primärt — vi behöver den för att skicka beräkningen.
   - Ger de e-post direkt → spara med capture_lead, fråga ALLTID därefter: "Vill du att en av våra rådgivare ringer upp dig? Lämna i så fall ditt telefonnummer." Detta är obligatoriskt — hoppa inte över det.
   - Ger de telefonnummer istället → spara numret, fråga direkt: "Tack! Vi behöver också din e-post för att skicka kalkylen — vad är den?"
   - Ger de både på en gång → perfekt, spara allt, gå vidare
   - Vägrar ge e-post → respektera, gå vidare ändå utan att fråga igen
3. Anropa capture_lead med allt du fått, sedan calculate_savings.
4. Presentera resultatet naturligt. Avsluta med: "Vill du ha en exaktare kalkyl anpassad till ditt hus?"
5. Om de vill ha mer → fråga efter det som saknas (namn, telefon eller e-post). Anropa capture_lead igen.

Regler för lead capture:
- Ta emot vilket format som helst — adress, stad, postnummer, telefon med eller utan landskod
- Spara allt kunden ger frivilligt via capture_lead — mer data är alltid bättre
- Tvinga aldrig fram specifikt format
- Spara aldrig persondata bara i konversationen — anropa alltid capture_lead`;

// ── Lead storage (in-memory for demo, replace with DB/HubSpot) ──
const leads = [];

function saveLead({ email, name, phone, result, source }) {
  const existing = leads.find(l => l.email === email);
  if (existing) {
    if (name) existing.name = name;
    if (phone) existing.phone = phone;
    if (result) existing.result = result;
    existing.updatedAt = new Date().toISOString();
    console.log('[LEAD updated]', existing);
    return existing;
  }
  const lead = { email, name, phone, result, source, createdAt: new Date().toISOString() };
  leads.push(lead);
  console.log('[LEAD captured]', lead);
  return lead;
}

// ── Tool definition ──
const TOOLS = [
{
  type: 'function',
  function: {
    name: 'resolve_location',
    description: 'Slår upp en adress, postnummer eller stad och returnerar ort + elområde. Anropa direkt när kunden anger var de bor — bekräfta sedan resultatet till kunden innan du går vidare.',
    parameters: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Exakt vad kunden angav — adress, postnummer, stad' }
      },
      required: ['query']
    }
  }
},
{
  type: 'function',
  function: {
    name: 'capture_lead',
    description: 'Sparar kontaktuppgifter från kunden. Anropa med e-post innan calculate_savings, och igen med namn+telefon om kunden vill ha exaktare kalkyl.',
    parameters: {
      type: 'object',
      properties: {
        email: { type: 'string', description: 'Kundens e-postadress' },
        name:  { type: 'string', description: 'Kundens namn (om angivet)' },
        phone: { type: 'string', description: 'Kundens telefonnummer (om angivet)' },
        location_raw: { type: 'string', description: 'Exakt vad kunden angav — gatuadress, postnummer, stad, vad som helst' },
        wants_followup: { type: 'boolean', description: 'Kunden vill ha personlig uppföljning/exaktare kalkyl' }
      }
    }
  }
},
{
  type: 'function',
  function: {
    name: 'calculate_savings',
    description: 'Beräknar uppskattad årlig besparing med OPTi baserat på kundens uppgifter',
    parameters: {
      type: 'object',
      properties: {
        system: { type: 'string', enum: ['BV', 'LV', 'FL'], description: 'Uppvärmningssystem' },
        region: { type: 'string', enum: ['SE1', 'SE2', 'SE3', 'SE4'], description: 'Elområde — härled från stad via intern mappning' },
        city: { type: 'string', description: 'Kundens stad — från resolve_location-resultatet' },
        kwh: { type: 'number', description: 'Årsförbrukning el i kWh (om känd)' },
        hustyp: { type: 'string', enum: ['hus 1', 'hus 2', 'hus 3', 'hus 4'], description: 'Hustyp (om kWh inte är känt)' },
        sol: { type: 'boolean', description: 'Har solceller' },
        elbil: { type: 'boolean', description: 'Har elbil' }
      },
      required: ['region']
    }
  }
}];

// ── Quick reply detection ──
function detectQuickReplies(text) {
  if (!text) return null;
  const t = text.toLowerCase();
  if (t.includes('bergvärme') && t.includes('luft/vatten')) {
    return ['Bergvärme', 'Luft/vatten', 'Frånluft', 'Vet inte'];
  }
  if ((t.includes('solcell') || t.includes('solpanel')) && (t.includes('ja') || t.includes('nej') || t.includes('har du'))) {
    return ['Ja', 'Nej'];
  }
  if (t.includes('elbil') && (t.includes('ja') || t.includes('nej') || t.includes('har du'))) {
    return ['Ja', 'Nej'];
  }
  if (t.includes('norra') && t.includes('mellersta') && t.includes('södra')) {
    return ['Norra Sverige', 'Mellersta Sverige', 'Södra Sverige'];
  }
  return null;
}

// ── Chat endpoint ──
app.post('/chat', async (req, res) => {
  const { messages } = req.body;

  try {
    let currentMessages = [...messages];
    let allToolMessages = [];
    let savingsResult = null;

    // Allow up to 3 tool calls in one turn (e.g. capture_lead then calculate_savings)
    let response = await openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [{ role: 'system', content: SYSTEM_PROMPT }, ...currentMessages],
      tools: TOOLS,
      tool_choice: 'auto',
      temperature: 0.7,
    });

    let msg = response.choices[0].message;

    while (msg.tool_calls?.length) {
      allToolMessages.push(msg);
      const toolResults = [];

      for (const call of msg.tool_calls) {
        const args = JSON.parse(call.function.arguments);
        let result;

        if (call.function.name === 'resolve_location') {
          const geo = await geocode(args.query);
          let resolvedRegion = null, resolvedCity = null;
          if (geo) {
            resolvedRegion = latToRegion(geo.lat);
            // Extract city from display_name (first meaningful part)
            const parts = geo.display_name.split(',').map(s => s.trim());
            resolvedCity = parts[1] || parts[0]; // usually municipality or city
          } else {
            // Fallback: try city map
            resolvedRegion = cityToRegion(args.query);
          }
          toolResults.push({ role: 'tool', tool_call_id: call.id, content: JSON.stringify({
            city: resolvedCity,
            region: resolvedRegion,
            display: geo?.display_name || null,
            found: !!resolvedRegion
          })});
        } else if (call.function.name === 'capture_lead') {
          result = saveLead({ ...args, source: 'agent-v2' });
          toolResults.push({ role: 'tool', tool_call_id: call.id, content: JSON.stringify({ ok: true }) });
        } else if (call.function.name === 'calculate_savings') {
          result = await calculateSavings(args);
          savingsResult = result;
          toolResults.push({ role: 'tool', tool_call_id: call.id, content: JSON.stringify(result) });
        }
      }

      allToolMessages.push(...toolResults);

      // Continue conversation with tool results
      response = await openai.chat.completions.create({
        model: 'gpt-4o',
        messages: [
          { role: 'system', content: SYSTEM_PROMPT },
          ...currentMessages,
          ...allToolMessages,
        ],
        tools: TOOLS,
        tool_choice: 'auto',
        temperature: 0.7,
      });

      msg = response.choices[0].message;
    }

    res.json({ reply: msg.content, result: savingsResult, quickReplies: detectQuickReplies(msg.content) });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
});

// ── Leads endpoint (for Effira to review) ──
app.get('/leads', (req, res) => {
  res.json({ count: leads.length, leads });
});

// ── Feedback endpoint ──
app.post('/feedback', (req, res) => {
  const { feedback, inputs, result } = req.body;
  console.log('[FEEDBACK]', new Date().toISOString(), feedback, inputs, result);
  // TODO: persist to file/DB
  res.json({ ok: true });
});

// ── Global error handling — keep server alive ──
process.on('uncaughtException', (err) => {
  console.error('[uncaughtException]', err);
});
process.on('unhandledRejection', (reason) => {
  console.error('[unhandledRejection]', reason);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Effira agent running at http://localhost:${PORT}`));
