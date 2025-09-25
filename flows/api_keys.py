"""Manage API keys (requires internal access)."""

import os
import requests
from rich import print

BASE = os.environ.get('GFWPRO_BASE_URL', 'https://pro-qa.globalforestwatch.org/api/v1').rstrip('/')
TOKEN = os.environ.get('GFWPRO_API_TOKEN')
ORG_ID = os.environ.get('ORG_ID')
USER_ID = os.environ.get('USER_ID')
HEADERS = {'x-api-key': TOKEN}


def list_keys():
  res = requests.get(f'{BASE}/../api-keys/{ORG_ID}', headers=HEADERS)
  res.raise_for_status()
  return res.json()


def create_key():
  res = requests.post(f'{BASE}/../api-keys', json={'organizationId': int(ORG_ID), 'userId': int(USER_ID)}, headers=HEADERS)
  res.raise_for_status()
  return res.json()


def delete_key(token_id: str):
  res = requests.delete(f'{BASE}/../api-keys/{ORG_ID}/{token_id}', headers=HEADERS)
  res.raise_for_status()


def main():
  if not TOKEN:
    raise RuntimeError('Set GFWPRO_API_TOKEN')
  if not ORG_ID:
    raise RuntimeError('Set ORG_ID')

  print('[bold]Existing keys[/bold]')
  keys = list_keys()
  print(keys)

  if USER_ID:
    new_key = create_key()
    print('[green]Created key[/green]', new_key)

  if os.environ.get('DELETE_TOKEN_ID'):
    delete_key(os.environ['DELETE_TOKEN_ID'])
    print('Deleted token', os.environ['DELETE_TOKEN_ID'])


if __name__ == '__main__':
  main()
