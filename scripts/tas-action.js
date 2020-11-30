 const TAS_ADDR = 'https://tas-feat-server-na6izd3flr0gvw.herokuapp.com'
// const TAS_ADDR = 'https://kj2ifn9s.tunnelto.dev'


// uploadAllRecords uploads all the spreadsheet records to the tas server.
function uploadAllRecords() {
  let sheet = SpreadsheetApp.getActiveSpreadsheet();
  let headers = sheet.getRange('A1:X1');
  let table = sheet.getDataRange();

  let blob = Utilities.newBlob(JSON.stringify(table.getValues()), 'text/csv', 'demo.csv');
  let formData = {
    'file': table.getValues(),
  }

  let options = {
    'method': 'post',
    'contentType': 'application/json',
    'payload': JSON.stringify(formData),
  }

  let response = UrlFetchApp.fetch(TAS_ADDR + '/upload', options);
  let parsedResponse = Utilities.parseCsv(response.getContentText())

  Logger.log(parsedResponse);
  table.setValues(parsedResponse);
}

function uploadSelectedRange() {
  let sheet = SpreadsheetApp.getActiveSpreadsheet();
  let header = sheet.getRange('A1:X1')
  let range = sheet.getActiveSheet().getActiveRange()

  let table = header.getValues().concat(range.getValues())

  let formData = {
    'file': table,
  }

  let options = {
    'method': 'post',
    'contentType': 'application/json',
    'payload': JSON.stringify(formData)
  }

  let response = UrlFetchApp.fetch(TAS_ADDR + '/upload', options);
  let [_, records] = Utilities.parseCsv(response.getContentText())

  Logger.log(records)
  range.setValues([records])
}

// function uplaodSelectedRangeList() {
// }


function onOpen() {
  let ui = SpreadsheetApp.getUi();

  ui.createMenu('TAS Actions')
    .addItem('Test All', 'uploadAllRecords')
    .addItem('Test Selected Range', 'uploadSelectedRange')
    .addToUi();
}
