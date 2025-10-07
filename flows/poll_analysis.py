"""Poll analysis status until completion."""

import os
import time
import requests
from rich import print

BASE = os.environ.get('GFWPRO_BASE_URL', 'https://pro.globalforestwatch.org/api/v1').rstrip('/')
TOKEN = os.environ.get('GFWPRO_API_TOKEN')
LIST_ID = os.environ.get('LIST_ID')
ANALYSIS_ID = os.environ.get('ANALYSIS_ID', 'FCD')
HEADERS = {'x-api-key': TOKEN}


def poll_status(list_id: str, analysis_id: str):
  while True:
    res = requests.get(f'{BASE}/list/{list_id}/analysis/{analysis_id}/status', headers=HEADERS)
    res.raise_for_status()
    data = res.json()
    status_value = str(data.get('status', '')).lower()
    print('Status:', data.get('status'))
    if status_value in {'complete', 'completed', 'failed', 'error'}:
      return data
    time.sleep(int(os.environ.get('POLL_INTERVAL', '10')))


def main():
  if not TOKEN:
    raise RuntimeError('Set GFWPRO_API_TOKEN')
  if not LIST_ID:
    raise RuntimeError('Set LIST_ID environment variable')

  result = poll_status(LIST_ID, ANALYSIS_ID)
  status_value = str(result.get('status', '')).lower()
  if status_value in {'complete', 'completed'}:
    print('[green]Analysis complete[/green]')
    result_url = result.get('resultUrl')
    if not result_url:
      raise RuntimeError('Analysis completed but no resultUrl returned. Re-run generate endpoint.')
    res = requests.get(result_url)
    res.raise_for_status()
    filename = f'{LIST_ID}_{ANALYSIS_ID}.zip'
    with open(filename, 'wb') as fh:
      fh.write(res.content)
    print('Saved results to', filename)
  else:
    print('[red]Analysis failed[/red]', result)


if __name__ == '__main__':
  main()
