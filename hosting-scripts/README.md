# Python script leaseweb_gsheet.py
This script fetches invoice details from your Leaseweb account and creates Google sheet.

Before use it:
* Install [python module gspread and configure Google authentification keys](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
* Create google_sheet_secret.json with Google auth keys
* Get API key of your Leaseweb account
* Create config.py with api keys:
```
lw_accounts = {
    "lw_us" : {'x-lsw-auth': "LEASEWEB_API_KEY", 'Accept': "application/json"},
    "lw_eu" : {'x-lsw-auth': "LEASEWEB_API_KEY", 'Accept': "application/json"},
}
```
In this example we have two API keys for US and EU accounts
* Run script providing region EU for Europe or US for USA, and invoice number:
```
python3 leaseweb_gsheet.py -r eu -i 91181824
```
