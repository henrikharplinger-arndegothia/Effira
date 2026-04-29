// ── SETUP ──────────────────────────────────────────────────────────────────
// 1. Gå till script.google.com → Nytt projekt
// 2. Klistra in hela den här filen
// 3. Klicka Distribuera → Ny distribution → Webbapp
//    - Kör som: Jag (ditt Google-konto)
//    - Vem har åtkomst: Alla
// 4. Godkänn behörigheter
// 5. Kopiera URL:en och klistra in i lead-dashboard.html som SCRIPT_URL
// ───────────────────────────────────────────────────────────────────────────

const SHEET_NAME = 'Leads';

function doGet(e) {
  try {
    const sheet = getOrCreateSheet();
    const data = sheet.getDataRange().getValues();
    const result = {};
    for (let i = 1; i < data.length; i++) {
      const key = data[i][0] + '_' + data[i][1];
      result[key] = { status: data[i][3], notes: data[i][4] };
    }
    return json(result);
  } catch (err) {
    return json({ error: err.message });
  }
}

function doPost(e) {
  try {
    const p = JSON.parse(e.postData.contents);
    const sheet = getOrCreateSheet();
    const data = sheet.getDataRange().getValues();
    const key = p.channel + '_' + p.rank;

    for (let i = 1; i < data.length; i++) {
      if (data[i][0] + '_' + data[i][1] === key) {
        sheet.getRange(i + 1, 3, 1, 4).setValues([[p.name, p.status, p.notes || '', new Date()]]);
        return json({ ok: true });
      }
    }

    sheet.appendRow([p.channel, p.rank, p.name, p.status, p.notes || '', new Date()]);
    return json({ ok: true });
  } catch (err) {
    return json({ error: err.message });
  }
}

function getOrCreateSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow(['channel', 'rank', 'name', 'status', 'notes', 'updated']);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function json(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
