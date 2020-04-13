#!/usr/bin/python3

import argparse
import random


def simulate_damage(dmg, armor):
  return max(0, random.randint(0, dmg * 2) - armor)


def simulate(dmg, burst, effectiveness, armor, modifier, sims=10000):
  total_dmg = 0.0
  for _ in range(sims):
    for _ in range(burst):
      total_dmg += simulate_damage(int(dmg * modifier), int(armor * effectiveness))

  return total_dmg / sims


def main():
  parser = argparse.ArgumentParser(description='Simulate weapon {DAMAGE} against {ARMOR}')
  parser.add_argument('-s', '--simulations', metavar='SIMS', default=10000, type=int, help='Number of simulations to run. Default 10000.')
  parser.add_argument('scenarios', metavar='DAMAGEx{BURST}#{EFFECTIVENESS}', nargs='+', help='Listed damage value. Format: DAMAGE#EFFECTIVENESS, or DAMAGExBURST#EFFECTIVENESS')
  parser.add_argument('armor', metavar='ARMOR#{MODIFIER}', help='Listed armor value. Format: ARMOR#MODIFIER')
  args = parser.parse_args()

  it = iter(args.scenarios)
  try:
    armor = args.armor
    modifier = 1.0
    if '#' in armor:
      armor, modifier = armor.split('#')
      modifier = float(modifier)
    armor = int(armor)

    for scenario in it:
      damage = scenario
      effectiveness = 1.0

      if '#' in damage:
        damage, effectiveness = damage.split('#')
        effectiveness = float(effectiveness)

      if 'x' in damage:
        damage, burst = map(int, damage.split('x'))
      else:
        damage = int(damage)
        burst = 1

      effective_scenario = "" 
      if '#' in args.armor:
        effective_damage = str(int(damage * modifier))
        effective_scenario += "({})".format(effective_damage)

      effective_scenario += str(damage)

      if 'x' in scenario:
        effective_scenario += "x{}".format(burst)
      if '#' in scenario:
        effective_scenario += "#{}".format(effectiveness)

      result = simulate(damage, burst, effectiveness, armor, modifier, args.simulations)

      effective_armor = str(armor)
      if '#' in scenario:
        effective_armor = "({})".format(int(effectiveness * armor)) + effective_armor

      print("{:5.2f} - {} simulations, {:14} damage against {:>7} armor".format(result, args.simulations, effective_scenario, effective_armor))

  except StopIteration:
    print("Missing {{ARMOR}} value for {{DAMAGE}} value: {}".format(args.scenarios[-1]))


if __name__ == "__main__":
  main()
