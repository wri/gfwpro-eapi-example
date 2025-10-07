"""Demonstration: prepare upload, upload file, create list, poll analysis."""

import os
import sys
import time
import requests
from rich import print

BASE = os.environ.get('GFWPRO_BASE_URL', 'https://pro.globalforestwatch.org/api/v1')
if BASE.startswith('//'):
  BASE = f'http:{BASE}'
BASE = BASE.rstrip('/')
TOKEN = os.environ.get('GFWPRO_API_TOKEN')
EMAIL = os.environ.get('USER_EMAIL', 'demo@example.com')
CSV_PATH = os.environ.get('CSV_PATH', 'sample_data/example.csv')
COMMODITY = os.environ.get('COMMODITY', 'Cocoa Generic')
ANALYSIS = os.environ.get('ANALYSIS', 'FCD')
HEADERS = {'x-api-key': TOKEN, 'Accept': 'application/json'}

def postWithRedirect(api_url, headers, data):
    response = requests.post(api_url, headers=headers, data=data, allow_redirects=False)
    if response.status_code in (301, 302):
        new_url = response.headers.get("Location")
    response = requests.post(new_url, headers=headers, data=data, allow_redirects=False)
    return response

def prepare_upload() -> dict:
  res = postWithRedirect(f'{BASE}/prepare_upload', data={'userEmail': EMAIL, 'fileType': 'csv'}, headers=HEADERS)
  res.raise_for_status()
  return res.json()


def upload_file(upload_info: dict):
  with open(CSV_PATH, 'rb') as fh:
    data = fh.read()
  res = requests.put(upload_info['uploadUrl'], data=data, headers={'Content-Type': 'text/csv'})
  res.raise_for_status()


def create_list(upload_id: str) -> str:
  body = {'uploadId': upload_id, 'listName': f'client_demo_{int(time.time())}', 'commodity': COMMODITY, 'analysisIDs': ANALYSIS}
  res = postWithRedirect(f'{BASE}/list/upload_new', data=body, headers=HEADERS)
  res.raise_for_status()
  return res.json()['listId']


def poll_status(list_id: str):
  while True:
    res = requests.get(f'{BASE}/list/{list_id}/analysis/{ANALYSIS}/status', headers=HEADERS)
    res.raise_for_status()
    data = res.json()
    status_value = str(data.get('status', '')).lower()
    print('Status:', data.get('status'))
    if status_value in {'complete', 'completed', 'failed', 'error'}:
      return data
    time.sleep(10)


def download_results(list_id: str, analysis_id: str, result_url: str):
  res = requests.get(result_url)
  res.raise_for_status()
  filename = f'{list_id}_{analysis_id}.zip'
  with open(filename, 'wb') as fh:
    fh.write(res.content)
  print('Saved results to', filename)


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

  print('[bold]4. Poll analysis status[/bold]')
  status = poll_status(list_id)
  status_value = str(status.get('status', '')).lower()
  if status_value in {'complete', 'completed'}:
    result_url = status.get('resultUrl')
    if not result_url:
      print('[red]Analysis completed but resultUrl not provided. Use generate endpoint to refresh downloads.[/red]')
      sys.exit(1)
    download_results(list_id, ANALYSIS, result_url)
  else:
    print('[red]Analysis did not complete successfully[/red]', status)
    sys.exit(1)


if __name__ == '__main__':
  main()
