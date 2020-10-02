# Python script leaseweb_invoice.py
Before use it:
* Install [python module gspread and configure Google authentification](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
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
