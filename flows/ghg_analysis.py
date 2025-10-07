"""GHG analysis workflow using requests."""

import os
import time
import requests
from rich import print

BASE = os.environ.get('GFWPRO_BASE_URL', 'https://pro.globalforestwatch.org/api/v1').rstrip('/')
TOKEN = os.environ.get('GFWPRO_API_TOKEN')
EMAIL = os.environ.get('USER_EMAIL', 'demo@example.com')
CSV_PATH = os.environ.get('CSV_PATH', 'sample_data/example.csv')
COMMODITY = os.environ.get('COMMODITY', 'Cocoa Generic')
YIELD = float(os.environ.get('GHG_YIELD', '0.5'))
HEADERS = {'x-api-key': TOKEN}


def prepare_upload() -> dict:
  res = requests.post(f'{BASE}/prepare_upload', json={'userEmail': EMAIL, 'fileType': 'csv'}, headers=HEADERS)
  res.raise_for_status()
  return res.json()


def upload_file(upload_info: dict):
  with open(CSV_PATH, 'rb') as fh:
    data = fh.read()
  res = requests.put(upload_info['uploadUrl'], data=data, headers={'Content-Type': 'text/csv'})
  res.raise_for_status()


def create_list(upload_id: str) -> str:
  body = {'uploadId': upload_id, 'listName': f'ghg_demo_{int(time.time())}', 'commodity': COMMODITY, 'analysisIDs': 'GHG'}
  res = requests.post(f'{BASE}/list/upload_new', json=body, headers=HEADERS)
  res.raise_for_status()
  return res.json()['listId']


def trigger_ghg(list_id: str):
  payload = {'yield': YIELD, 'baselineYear': 2020, 'userEmail': EMAIL}
  res = requests.post(f'{BASE}/list/{list_id}/analysis/GHG/analyze', json=payload, headers=HEADERS)
  res.raise_for_status()


def main():
  if not TOKEN:
    raise RuntimeError('Set GFWPRO_API_TOKEN environment variable.')

  info = prepare_upload()
  upload_file(info)
  list_id = create_list(info['uploadId'])
  print('List ID:', list_id)
  trigger_ghg(list_id)
  print('Triggered GHG analysis. Poll /list/{list_id}/analysis/GHG/status')


if __name__ == '__main__':
  main()
