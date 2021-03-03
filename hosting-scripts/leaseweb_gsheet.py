#!/usr/bin/env python3

import requests
import argparse
import gspread
import config
from oauth2client.service_account import ServiceAccountCredentials as Account


def api_request(url, headers, params=None):
    """
    HTTP Request to api
    """
    try:
        conn = requests.get(url=url, headers=headers, params=params)
        conn.raise_for_status()
    except requests.exceptions.HTTPError as http_error:
        raise SystemExit(http_error)
    except requests.exceptions.RequestException as req_error:
        raise SystemExit(req_error)
    except Exception as error:
        raise SystemExit(error)
    else:
        return conn.json()


def main(url, auth_key):
    hosts = []
    for item in api_request(url, auth_key)['lineItems']:
        print(item)
        host = {
            'ContractId': item['contractId'],
            'Product': item['product'],
            'Quantity': item['quantity'],
            'UnitAmount': item['unitAmount'],
            'TotalAmount': item['totalAmount'],
            'Reference': item['reference'] if 'reference' in item else '',
            'EquipmentId': item['equipmentId'] if (item['contractId'] != config.lw_contract) else '',
        }
        hosts.append(host)
    return hosts


# Google sheet
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = Account.from_json_keyfile_name('google_sheet_secret.json', scope)
client = gspread.authorize(creds)


def update_google_table(parameter_list):
    # Google doc
    spreadsheet = client.open("Leaseweb EU invoices")
    # Создание вкладки worksheet с номером инвойса
    worksheet = spreadsheet.add_worksheet(title=invoice, rows="300", cols="10")
    worksheet = spreadsheet.worksheet(invoice)  # Вкладка Billing
    # На вход функции передается list элементами которого являются dict
    # Формирование заголовка таблицы
    header = [
        'ContractId',
        'Product',
        'Quantity',
        'UnitAmount',
        'TotalAmount',
        'Reference',
        'EquipmentId',
    ]
    worksheet.update('A1', [header])
    start_cell = 'A2'
    end_cell = 'G' + str(len(parameter_list) + 1)
    cell_range = worksheet.range('{}:{}'.format(start_cell, end_cell))
    simplyfied_data = []
    for row in parameter_list:
        for column in header:
            simplyfied_data.append(row[column])

    for i, cell in enumerate(cell_range):
        cell.value = simplyfied_data[i]

    worksheet.update_cells(cell_range)


if __name__ == "__main__":
    url = 'https://api.leaseweb.com/invoices/v1/invoices/'

    parser = argparse.ArgumentParser(
        prog='leaseweb_invoice_gsheet.py',
        usage='%(prog)s -r [eu|us] -i invoice_number',
        description='Get invoice from Leaseweb API and create Google Sheet'
    )
    parser.add_argument(
        '-r',
        nargs='?',
        default=None,
        choices=['eu', 'us'],
        help='Region: EU, US',
        required=True
    )
    parser.add_argument('-i', help='Invoice number', required=True)
    args = parser.parse_args()

    region = vars(args)['r']
    invoice = vars(args)['i']

    if region == 'eu':
        update_google_table(main(url + invoice, config.lw_accounts['lw_eu']))
    else:
        update_google_table(main(url + invoice, config.lw_accounts['lw_us']))
