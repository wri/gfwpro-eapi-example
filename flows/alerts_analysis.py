#!/usr/bin/env python3
"""Alerts analysis workflow with graceful error handling."""

import os
import time
import requests
from rich import print

try:
  from .http_utils import post_with_redirect
except ImportError:  # pragma: no cover
  from http_utils import post_with_redirect

BASE = os.environ.get('GFWPRO_BASE_URL', 'https://pro.globalforestwatch.org/api/v1').rstrip('/')
TOKEN = os.environ.get('GFWPRO_API_TOKEN')
EMAIL = os.environ.get('USER_EMAIL', 'demo@example.com')
CSV_PATH = os.environ.get('CSV_PATH', 'sample_data/example.csv')
START_DATE = os.environ.get('ALERT_START_DATE', '01-01-2024')
END_DATE = os.environ.get('ALERT_END_DATE', '12-31-2024')
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
  try:
    res = post_with_redirect(
      f'{BASE}/list/{list_id}/analysis/Alerts/generate',
      json=payload,
      headers=HEADERS,
    )
    res.raise_for_status()
    print('✅ Alerts generation triggered successfully')
    return True
  except Exception as e:
    print(f'⚠️  Alerts generation failed: {e}')
    print('This may be due to missing microservices (e.g., port 3336 service not running)')
    print('The list was created successfully, but alerts generation requires additional services.')
    return False


def main():
  if not TOKEN:
    raise RuntimeError('Set GFWPRO_API_TOKEN environment variable.')

  print('[bold]1. Prepare upload[/bold]')
  info = prepare_upload()

  print('[bold]2. Upload CSV[/bold]')
  upload_file(info)

  print('[bold]3. Create list[/bold]')
  list_id = create_list(info['uploadId'])
  print('List ID:', list_id)
  
  print('[bold]4. Trigger alerts generation[/bold]')
  success = trigger_alerts(list_id)
  
  if success:
    print('✅ Alerts analysis workflow completed successfully!')
    print(f'Poll status with: LIST_ID={list_id} ANALYSIS_ID=Alerts python flows/poll_analysis.py')
  else:
    print('⚠️  Alerts analysis workflow completed with warnings')
    print('The list was created but alerts generation failed due to missing services')
    print(f'You can still check the list with: LIST_ID={list_id} python flows/check_status.py')


if __name__ == '__main__':
  main()
