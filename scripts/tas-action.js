const TAS_ADDR = "https://tas-improv-exec-engine-qg76fti.herokuapp.com";
// const TAS_ADDR = 'https://8j9mjzo7.tunnelto.dev';

function* makeRangeIterator(content = []) {
    let current = 0;

    while (true) {
        let retry = yield content[current];
        if (retry) continue;
        current++;
    }
}

function fetchData(url, payload) {
    let options = {
        method: "post",
        contentType: "application/json",
        payload: JSON.stringify({ file: payload }),
        muteHttpExceptions: true,
        headers: {
            "Keep-Alive": "timeout=30, max=1000",
        },
    };

    return UrlFetchApp.fetch(url, options);
}

function isSuccess(code) {
    return !(code < 200.0 || code >= 300.0);
}

function setStore(store, column, success, dataset) {
    const data = Utilities.parseCsv(dataset)[1];
    store[column] = { success, data };
}

function getStore(store, column) {
    return store[column];
}

function getAllStore(store) {
    return store;
}

function streamAllRecords() {
    const url = TAS_ADDR + "/upload";
    const sheet = SpreadsheetApp.getActiveSpreadsheet();
    const table = sheet.getDataRange();

    const [head, ...body] = table.getValues();
    const iter = makeRangeIterator(body);

    const store = {};

    let retry = false;
    let retries = 3;
    let count = body.length - 1;
    let columnNum = 1;

    while (true) {
        const payload = iter.next(retry).value;
        const response = fetchData(url, [head, payload]);
        const success = isSuccess(response.getResponseCode());

        if (!success) {
            if (retries <= 0) {
                setStore(store, columnNum, success, [head, payload]);
                columnNum++;
                retries = 3;
                retry = false;
                continue;
            }
            if (!retry) {
                retry = true;
            }
            retries--;
            continue;
        }

        setStore(store, columnNum, success, response.getContentText());
        retry = false;
        retries = 3;

        Logger.log(getStore(store, columnNum));

        if (count <= 0) {
            break;
        }
        count--;
        columnNum++;
    }

    const _content = [head];
    for (let key of Object.keys(getAllStore(store))) {
        const { data, success } = getStore(store, key);
        _content.push(data);
    }

    Logger.log(_content);
    table.setValues(_content);
}

function uploadAllRecords() {
    const url = TAS_ADDR + "/upload";
    const sheet = SpreadsheetApp.getActiveSpreadsheet();
    const table = sheet.getDataRange();

    const response = fetchData(url, table.getValues());
    const records = Utilities.parseCsv(response.getContentText());

    Logger.log(records);
    table.setValues(records);
}

function uploadSelectedRange() {
    const url = TAS_ADDR + "/upload";
    const sheet = SpreadsheetApp.getActiveSpreadsheet();

    const header = sheet.getRange("A1:AD1");
    const range = sheet.getActiveSheet().getActiveRange();
    const table = header.getValues().concat(range.getValues());

    const response = fetchData(url, table);

    const [_, records] = Utilities.parseCsv(response.getContentText());

    Logger.log(records);
    range.setValues([records]);
}

function onOpen() {
    let ui = SpreadsheetApp.getUi();
    ui.createMenu("TAS Actions").addItem("Test All", "uploadAllRecords").addItem("Test Selected Range", "uploadSelectedRange").addItem("Stream All", "streamAllRecords").addToUi();
}
