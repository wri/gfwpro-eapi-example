"""List management helpers: enumerate lists, fetch details, delete list."""

import os
import requests
from rich import print

BASE = os.environ.get('GFWPRO_BASE_URL', 'https://pro-qa.globalforestwatch.org/api/v1').rstrip('/')
TOKEN = os.environ.get('GFWPRO_API_TOKEN')
HEADERS = {'x-api-key': TOKEN}


def list_all(page_size: int = 50, page_num: int = 0):
  res = requests.get(f'{BASE}/list', params={'pageSize': page_size, 'pageNum': page_num}, headers=HEADERS)
  res.raise_for_status()
  return res.json()


def get_list(list_id: str):
  res = requests.get(f'{BASE}/list/{list_id}', headers=HEADERS)
  res.raise_for_status()
  return res.json()


def delete_list(list_id: str, user_email: str):
  res = requests.post(f'{BASE}/list/{list_id}/delete', json={'userEmail': user_email}, headers=HEADERS)
  res.raise_for_status()
  return res.json()


def main():
  if not TOKEN:
    raise RuntimeError('Set GFWPRO_API_TOKEN')

  data = list_all()
  print('[bold]Lists:[/bold]')
  for item in data.get('lists', []):
    print(item['listId'], item.get('listName'), item.get('status'))

  if data.get('lists'):
    first = data['lists'][0]['listId']
    print('\n[bold]Details for[/bold]', first)
    print(get_list(first))

    if os.environ.get('DELETE_LIST') == '1':
      user_email = os.environ.get('USER_EMAIL', 'demo@example.com')
      print(delete_list(first, user_email))


if __name__ == '__main__':
  main()
