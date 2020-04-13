#!/usr/bin/python3

import random
import matplotlib.pyplot as plt


NUM_TRIALS = 100000


def simulate_dmg(dmg, armor=5, shots=1):
  max_dmg = dmg * 2
  results = [0] * max_dmg * shots

  for _ in range(NUM_TRIALS):
    dealt_dmg = 0
    for _ in range(shots):
      dealt_dmg += max(0, random.randint(0, dmg) + random.randint(0, dmg) - armor)
    results[dealt_dmg] += 1

  plot_results(results, "dmg: {}, armor: {}, total: {:.2f}".format(dmg, armor, calc_total(results)))


def plot_results(results, label=""):
  plt.plot(range(len(results)), results, label=label)
  

def calc_total(results):
  return sum([index * count * 1.0 / NUM_TRIALS for index, count in enumerate(results)])


def main():
  simulate_dmg(int((3*12+22)), 15)
  simulate_dmg(int(30), 10, 2)

  plt.ylim(0, NUM_TRIALS * .04)
  plt.xlim(0, 80)

  plt.legend()
  plt.show()


if __name__ == "__main__":
  main()
