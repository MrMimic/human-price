import pandas as pd
import requests
import numpy as np

page = requests.get("https://en.wikipedia.org/wiki/Prices_of_chemical_elements").text
chemicals_price = pd.read_html(page, flavor="bs4")[0]
print(chemicals_price.head())

page = requests.get("https://en.wikipedia.org/wiki/Composition_of_the_human_body").text
human_composition = pd.read_html(page, flavor="bs4")[1]

print(list(human_composition["Fraction of mass[11][12][13][14][15][16]"]))


POIDS = 49.9
print()
FINAL_TOT = 0

for n, k in zip(list(chemicals_price["Name"]["Name"]), list(chemicals_price["Price[5]"]["USD/L[c]"])):
    fraction = human_composition.loc[human_composition['Element'] == n, 'Fraction of mass[11][12][13][14][15][16]']

    # If this element is found in the body
    if len(list(fraction)) > 0 and list(fraction)[0] is not np.nan:
        fraction = fraction.values[0]
        
        # Numeric fraction
        try:
            fraction = float(fraction)
        except:
            unit = float(fraction.split("×")[0])
            exposant = fraction.split("×")[1].replace("10", "").replace("−", "-")
            fraction = float(f"{unit}E{exposant}")

        # Numeric price
        try:
            price = float(k)
        except:
            k = [float(x) for x in k.split("–")]
            price = np.mean(k)

        total = price * fraction * POIDS
        FINAL_TOT = FINAL_TOT + total

        print(f"{n}\t{price}$/k * fraction: {fraction} * {POIDS} = {total}$")

print(f"FINAL: {round(FINAL_TOT, 2)}$")