#!/usr/bin/env python3

# http://10.0.1.3:2283
# pip install wheel requests
# Note: you might need to run "pip install halo tabulate tqdm" if these dependencies are missing on your machine

# admin API Key
# KejK6k3fy4yiY8yAyvCmf6HDQYU70GXVtWcjvN8bzE

#owner's key
# IufgTVAPysasnNzeHoyoLVi7TH6wOCLmVSpMVdXLrUY

# protocol and port
# http://10.0.1.3:2283

import argparse
import json
import requests

from datetime import datetime
from halo import Halo
from tabulate import tabulate
from tqdm import tqdm
from urllib.parse import urlparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Fetch file report and delete orphaned media assets from Immich.')
    parser.add_argument('--apikey', help='Immich API key for authentication')
    parser.add_argument('--immichaddress', help='Full address for Immich, including protocol and port')
    parser.add_argument('--no_prompt', action='store_true', help='Delete orphaned media assets without confirmation')
    args = parser.parse_args()
    return args

def filter_entities(response_json, entity_type):
    return [
        {'pathValue': entity['pathValue'], 'entityId': entity['entityId'], 'entityType': entity['entityType']}
        for entity in response_json.get('orphans', []) if entity.get('entityType') == entity_type
    ]

def main():
    args = parse_arguments()
    owner_api_key = "IufgTVAPysasnNzeHoyoLVi7TH6wOCLmVSpMVdXLrUY"
    try:
        if args.apikey:
            api_key = args.apikey
        else:
            api_key = input('Enter the Immich API key: ')

        if args.immichaddress:
            immich_server = args.immichaddress
        else:
            immich_server = input('Enter the full web address for Immich, including protocol and port: ')
        immich_parsed_url = urlparse(immich_server)
        base_url = f'{immich_parsed_url.scheme}://{immich_parsed_url.netloc}'
        api_url = f'{base_url}/api'
        file_report_url = api_url + '/audit/file-report'
        headers = {'x-api-key': api_key}

        print()
        spinner = Halo(text='Retrieving list of orphaned media assets...', spinner='dots')
        spinner.start()

        try:
            response = requests.get(file_report_url, headers=headers)
            response.raise_for_status()
            spinner.succeed('Success!')
        except requests.exceptions.RequestException as e:
            spinner.fail(f'Failed to fetch assets: {str(e)}')

        person_assets = filter_entities(response.json(), 'person')
        orphan_media_assets = filter_entities(response.json(), 'asset')

        num_entries = len(orphan_media_assets)

        if num_entries == 0:
            print('No orphaned media assets found; exiting.')
            return

        else:
            if not args.no_prompt:
                table_data = []
                for asset in orphan_media_assets:
                    table_data.append([asset['pathValue'], asset['entityId']])
                print(tabulate(table_data, headers=['Path Value', 'Entity ID'], tablefmt='pretty'))
                print()

                if person_assets:
                    print('Found orphaned person assets! Please run the "RECOGNIZE FACES > ALL" job in Immich after running this tool to correct this.')
                    print()

                if num_entries > 0:
                    summary = f'There {"is" if num_entries == 1 else "are"} {num_entries} orphaned media asset{"s" if num_entries != 1 else ""}. Would you like to delete {"them" if num_entries != 1 else "it"} from Immich? (yes/no): '
                    user_input = input(summary).lower()
                    print()

                    if user_input not in ('y', 'yes'):
                        print('Exiting without making any changes.')
                        return

# https://immich.app/docs/api/delete-assets
            with tqdm(total=num_entries, desc="Deleting orphaned media assets", unit="asset") as progress_bar:
                for asset in orphan_media_assets:
                    entity_id = asset['entityId']
                    asset_url = f'{api_url}/asset'
                    delete_payload = json.dumps({'force': True, 'ids': [entity_id]})
                    headers = {'Content-Type': 'application/json', 'x-api-key': owner_api_key}
                    response = requests.delete(asset_url, headers=headers, data=delete_payload)
                    response.raise_for_status()
                    progress_bar.set_postfix_str(entity_id)
                    progress_bar.update(1)
            print()
            print('Orphaned media assets deleted successfully!')
    except Exception as e:
        print()
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()
