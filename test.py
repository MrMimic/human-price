import pandas as pd
import requests

page = requests.get("https://en.wikipedia.org/wiki/Prices_of_chemical_elements").text
chemicals_price = pd.read_html(page, flavor="bs4")[0]
print(chemicals_price.head())

page = requests.get("https://en.wikipedia.org/wiki/Composition_of_the_human_body").text
human_composition = pd.read_html(page, flavor="bs4")[1]

print(list(human_composition["Fraction of mass[11][12][13][14][15][16]"]))

for n, k, l in zip(list(chemicals_price["Name"]["Name"]), list(chemicals_price["Price[5]"]["USD/kg"]), list(chemicals_price["Price[5]"]["USD/L[c]"])):
    print(f"{n}\t{k} / {l}")
    print(human_composition.loc[human_composition['Element'] == n, 'Fraction of mass[11][12][13][14][15][16]'])
    print()
