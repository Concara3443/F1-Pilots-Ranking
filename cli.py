"""
This file is an alternative version that performs pilot comparison in the command line (CMD), 
without external dependencies or other tabs.
"""
import math
import random
from glicko import Glicko2

class Pilot:
    def __init__(self, name):
        self.name = name
        self.rating = 1500
        self.rd = 350
        self.volatility = 0.06

pilots = [
    Pilot("Lewis Hamilton"),
    Pilot("Max Verstappen"),
    Pilot("Charles Leclerc"),
    Pilot("Valtteri Bottas"),
    Pilot("Sergio Perez"),
    Pilot("Lando Norris"),
    Pilot("Daniel Ricciardo"),
    Pilot("Carlos Sainz"),
    Pilot("Pierre Gasly"),
    Pilot("Esteban Ocon"),
    Pilot("Fernando Alonso"),
    Pilot("Yuki Tsunoda"),
    Pilot("George Russell"),
    Pilot("Alexander Albon"),
    Pilot("Logan Sargeant"),
    Pilot("Oscar Piastri"),
    Pilot("Kevin Magnussen"),
    Pilot("Nico Hülkenberg"),
    Pilot("Lance Stroll"),
    Pilot("Zhou Guanyu")
]

def get_pilot_by_name(name):
    for pilot in pilots:
        if pilot.name == name:
            return pilot
    return None

def compare_pilots(pilot1, pilot2):
    choice = input(f"Which pilot do you prefer? (1: {pilot1.name}, 2: {pilot2.name}): ")
    if choice == '1':
        return pilot1, pilot2, False
    elif choice == '2':
        return pilot2, pilot1, False
    else:
        return pilot1, pilot2, True

def main():
    glicko = Glicko2()
    duels = set()
    for _ in range(len(pilots) * 2):  # Perform multiple comparisons
        while True:
            pilot1, pilot2 = random.sample(pilots, 2)
            duel = tuple(sorted([pilot1.name, pilot2.name]))
            if duel not in duels:
                duels.add(duel)
                break
        preferred, not_preferred, drawn = compare_pilots(pilot1, pilot2)
        preferred_rating = glicko.create_rating(preferred.rating, preferred.rd, preferred.volatility)
        not_preferred_rating = glicko.create_rating(not_preferred.rating, not_preferred.rd, not_preferred.volatility)
        new_ratings = glicko.rate_1vs1(preferred_rating, not_preferred_rating, drawn)
        preferred.rating, preferred.rd, preferred.volatility = new_ratings[0].mu, new_ratings[0].phi, new_ratings[0].sigma
        not_preferred.rating, not_preferred.rd, not_preferred.volatility = new_ratings[1].mu, new_ratings[1].phi, new_ratings[1].sigma

    sorted_pilots = sorted(pilots, key=lambda p: p.rating, reverse=True)
    print("Pilots ranked from best to worst:")
    for pilot in sorted_pilots:
        print(f"{pilot.name}: {pilot.rating:.2f}")

if __name__ == "__main__":
    main()