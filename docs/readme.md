# TAS Documentation

## Setting Apps Script

Steps:

* Open the Google Sheets application
* Click the `Tools` Menu, and
* Click the `Script editor`
* Copy the contents within [tas-action](../scripts/tas-action.js)

    *Note: AppsScript is a superset of Javascript but most use the .gs extension*

### Tas Actions

* Test All

    Test all reads all the records within the file and send this records to the tas server.

    The rows with avaliable repo url would be evaluated and the result of the testcase would be popluated.

    After all the tests are completed the existing file would be updated in-place.

* Test Selected Range

    This runs the update actions for a single selected range.

    *NOTE: if multiple rangeList are selected this actions would fail.*
