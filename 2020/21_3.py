import os
import re


def read_data() -> list:
    with open(os.path.join(os.path.dirname(__file__), '21.py'), "r") as f:
        c = f.read()
        data = c[c.rindex("🎅") + 1: c.rindex("⛄")].rstrip()
    return [line.strip() for line in data.strip().split('\n')]


# Problem input
foods = read_data()
foods = """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""".strip().split("\n")
# Part 1

# Finding all allergens
allergens = []
[allergens.extend(x.split(" (contains ")[1][:-1].split(", ")) for x in foods]
allergens = list(set(allergens))

# Defining a dictionary of potential ingredients that contain the allergen
potentials = {}
for item in allergens:
    potentials[item] = []
    for line in foods:
        if re.findall(item, line):
            potentials[item].append(line.split(' (')[0].split(' '))

# Finding the ingredients for each allergen that are common in every line
for key in list(potentials.keys()):
    potentials[key] = [set(x) for x in potentials[key]]
    potentials[key] = list(potentials[key][0].intersection(*potentials[key][1:]))

# Finding and narrowing down each allergen to the ingredient
knowns = {}
while potentials != {}:
    for key, val in list(potentials.items()):
        if len(potentials[key]) == 1:
            knowns[key] = val
            potentials.pop(key)
            [potentials[x].remove(val[0]) for x, y in potentials.items() if val[0] in y]

known_ingredients = []
[known_ingredients.append(x[0]) for x in list(knowns.values())]

# Finding all the ingredients mentioned in the input file
ingredients = []
for item in foods:
    if re.search('\(', item):
        ingredients.extend(item.split(' (')[0].split(' '))
    else:
        ingredients.extend(item.split(' '))

print('Part 1 answer:', len([x for x in ingredients if x not in known_ingredients]))

# Part 2

print('Part 2 answer: ', ','.join([val[0] for key, val in sorted(knowns.items())]))
