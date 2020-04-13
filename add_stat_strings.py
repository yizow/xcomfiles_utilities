#!/usr/bin/python3

import argparse


SOLDIER_STRING = 'type: STR_SOLDIER\n'
AI_STRING = 'type: STR_MUGGLE_AI\n'
DOG_STRING = 'type: STR_DOG\n'
RAT_STRING = 'type: STR_RAT\n'
VALID_SOLDIER = [SOLDIER_STRING, ]


CURRENT_STATS_STRING = 'currentStats:\n'
SOLDIER_END_STRING = 'tags: '
SOLDIER_NAME_STRING = 'name: '


# format:
# save_file_stat_name : (targeted_min_value, max_value, abbreviation)
# if value is None, check is ignored
SOLDIER_STATS = {
    'firing': (None, 90, 'F'),
    'reactions': (50, 60, 'R'),
    'throwing': (55, None, 'T'),
    'melee': (65, 90, 'M'),
    'bravery': (50, None, 'B'),
    }
STAT_ORDER = 'FRBMT'

MAX_STAT_STRING = '.'
MIN_STAT_STRING = '*'
SEPARATOR_STAT_STRING = '-'


def valid_soldier_type(soldier):
  return any(soldier_type in soldier for soldier_type in VALID_SOLDIER)


def read_soldier(original):
  soldier_lines = []
  processing_current_stats = False

  min_flags = ''
  max_flags = ''

  while True:
    line = original.readline()
    soldier_lines.append(line)

    if CURRENT_STATS_STRING in line:
      processing_current_stats = True
      processed_stats = 0

    if processing_current_stats:
      if any(stat in line for stat in SOLDIER_STATS.keys()):
        processed_stats += 1
        stat, value = line.strip().split(': ')
        value = int(value)

        min_value, max_value, abbreviation = SOLDIER_STATS[stat]

        if min_value is not None:
          if value < min_value:
            min_flags += abbreviation
        if max_value is not None:
          if value >= max_value:
            max_flags += abbreviation

      if processed_stats == len(SOLDIER_STATS):
        processing_current_stats = False

        min_flags = ''.join(sorted(min_flags, key = STAT_ORDER.index))
        max_flags = ''.join(sorted(max_flags, key = STAT_ORDER.index))

    if SOLDIER_END_STRING in line:
      break

  return soldier_lines, min_flags, max_flags


def write_soldier(soldier_lines, min_flags, max_flags, modified):
  for line in soldier_lines:
    if SOLDIER_NAME_STRING in line:
      line = line.replace('"', '')
      prefix = ''
      if len(max_flags) > 0:
        prefix += MAX_STAT_STRING + max_flags
      if len(min_flags) > 0:
        prefix += MIN_STAT_STRING + min_flags
      if len(prefix) > 0:
        prefix += SEPARATOR_STAT_STRING
      
      orignal_name = line.split(SOLDIER_NAME_STRING)[-1].split(SEPARATOR_STAT_STRING)[-1]
      line = line.split(SOLDIER_NAME_STRING)[0] + SOLDIER_NAME_STRING + '"' + prefix + orignal_name[:-1] + '"' + orignal_name[-1]

    modified.write(line)


def process_soldier(original, modified):
  write_soldier(*read_soldier(original), modified)


def modify_save(filename):
  with open(filename, 'r', encoding='utf8') as original, open(filename+'.modified', 'w', encoding='utf8') as modified:
    line = original.readline()
    soldier_count = 0

    while line:
      modified.write(line)
      if valid_soldier_type(line):
        soldier_count += 1
        process_soldier(original, modified)

      line = original.readline()

  print('Found {} soldiers'.format(soldier_count))


def main():
  parser = argparse.ArgumentParser(description='Add stat strings to solider names in save')
  parser.add_argument('save_file', metavar='FILE', help='Save filename')
  args = parser.parse_args()

  modify_save(args.save_file)


if __name__ == "__main__":
  main()
