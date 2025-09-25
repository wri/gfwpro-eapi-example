"""Poll analysis status until completion."""

import os
import time
import requests
from rich import print

BASE = os.environ.get('GFWPRO_BASE_URL', 'https://pro-qa.globalforestwatch.org/api/v1').rstrip('/')
TOKEN = os.environ.get('GFWPRO_API_TOKEN')
LIST_ID = os.environ.get('LIST_ID')
ANALYSIS_ID = os.environ.get('ANALYSIS_ID', 'FCD')
HEADERS = {'x-api-key': TOKEN}


def poll_status(list_id: str, analysis_id: str):
  while True:
    res = requests.get(f'{BASE}/list/{list_id}/analysis/{analysis_id}/status', headers=HEADERS)
    res.raise_for_status()
    data = res.json()
    print('Status:', data['status'])
    if data['status'] in {'COMPLETE', 'FAILED'}:
      return data
    time.sleep(int(os.environ.get('POLL_INTERVAL', '10')))


def main():
  if not TOKEN:
    raise RuntimeError('Set GFWPRO_API_TOKEN')
  if not LIST_ID:
    raise RuntimeError('Set LIST_ID environment variable')

  result = poll_status(LIST_ID, ANALYSIS_ID)
  if result['status'] == 'COMPLETE':
    print('[green]Analysis complete[/green]')
    res = requests.get(f'{BASE}/list/{LIST_ID}/download', headers=HEADERS)
    res.raise_for_status()
    filename = f'{LIST_ID}_{ANALYSIS_ID}.zip'
    with open(filename, 'wb') as fh:
      fh.write(res.content)
    print('Saved results to', filename)
  else:
    print('[red]Analysis failed[/red]', result)


if __name__ == '__main__':
  main()
