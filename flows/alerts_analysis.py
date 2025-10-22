"""Alerts analysis workflow using requests."""

import os
import time
import requests
from rich import print
from .http_utils import post_with_redirect


BASE = os.environ.get('GFWPRO_BASE_URL', 'https://pro.globalforestwatch.org/api/v1').rstrip('/')
TOKEN = os.environ.get('GFWPRO_API_TOKEN')
EMAIL = os.environ.get('USER_EMAIL', 'demo@example.com')
CSV_PATH = os.environ.get('CSV_PATH', 'sample_data/example.csv')
START_DATE = os.environ.get('ALERT_START_DATE', '2024-01-01')
END_DATE = os.environ.get('ALERT_END_DATE', '2024-12-31')
HEADERS = {'x-api-key': TOKEN}


def prepare_upload() -> dict:
  res = post_with_redirect(
    f'{BASE}/prepare_upload',
    json={'userEmail': EMAIL, 'fileType': 'csv'},
    headers=HEADERS,
  )
  res.raise_for_status()
  return res.json()


def upload_file(upload_info: dict):
  with open(CSV_PATH, 'rb') as fh:
    data = fh.read()
  res = requests.put(upload_info['uploadUrl'], data=data, headers={'Content-Type': 'text/csv'})
  res.raise_for_status()


def create_list(upload_id: str) -> str:
  body = {'uploadId': upload_id, 'listName': f'alerts_demo_{int(time.time())}', 'commodity': 'Cocoa Generic', 'analysisIDs': 'Alerts'}
  res = post_with_redirect(
    f'{BASE}/list/upload_new',
    json=body,
    headers=HEADERS,
  )
  res.raise_for_status()
  return res.json()['listId']


def trigger_alerts(list_id: str):
  payload = {'startDate': START_DATE, 'endDate': END_DATE, 'userEmail': EMAIL}
  res = post_with_redirect(
    f'{BASE}/list/{list_id}/analysis/Alerts/generate',
    json=payload,
    headers=HEADERS,
  )
  res.raise_for_status()


def main():
  if not TOKEN:
    raise RuntimeError('Set GFWPRO_API_TOKEN environment variable.')

  info = prepare_upload()
  upload_file(info)
  list_id = create_list(info['uploadId'])
  print('List ID:', list_id)
  trigger_alerts(list_id)
  print('Triggered Alerts generation. Poll /list/{list_id}/analysis/Alerts/status')


if __name__ == '__main__':
  main()
