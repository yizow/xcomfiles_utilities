#!/usr/bin/python3

"""
Parses items_XCOMFILES.rul for items that train throwing
"""

import yaml


def evaluate_throwing(item):
  name = item.get('type')
  if not name:
    return None

  mode = item.get('experienceTrainingMode')
  if mode:
    if mode in [7, 8, 9, 10, 11, 15, 18]:
      return '{}: {}'.format(mode, name)
    else:
      if mode != 0:
        return None

  categories = item.get('categories')
  if categories:
    if 'STR_GRENADES' in item['categories']:
      return name

  if item.get('arcingShot'):
    return name

  maxRange = item.get('maxRange')
  if maxRange and maxRange <= 10 and maxRange >= 2:
    return name

  return None


def main():
  with open('items_XCOMFILES.rul', 'r') as f:
    items = yaml.load(f)

    for item in items['items']:
      result = evaluate_throwing(item)

      if result:
        print(result)

if __name__ == "__main__":
  main()
