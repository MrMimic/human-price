import os

import pandas as pd
import requests
from flask import Flask


def get_data() -> pd.DataFrame:
    page = requests.get("https://en.wikipedia.org/wiki/Prices_of_chemical_elements").text
    chemicals_price = pd.read_html(page, flavor="bs4")[0]
    for n, k, l in zip(list(chemicals_price["Name"]), list(chemicals_price["Price[5]"]["USD/kg"]), list(chemicals_price["Price[5]"]["USD/L[c]"])):
        print(n, k, l)
    page = requests.get("https://en.wikipedia.org/wiki/Composition_of_the_human_body").text
    human_composition = pd.read_html(page, flavor="bs4")[1]


app = Flask(__name__)


@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
