import os

import numpy as np
import pandas as pd
import requests
from flask import Flask


def convert_scientific_notation(x: str) -> float:
    """Convert strange scientific notation from Wikipedia into floats.

    Args:
        x (str): tThe value to be casted as a float.

    Returns:
        float: The casted value.
    """
    try:
        x = float(x)
    except ValueError:
        # The 'x' is not a real ASCII x.
        unit = float(x.split("×")[0])
        # Neither is the "-"
        exposant = x.split("×")[1].replace("10", "").replace("−", "-")
        x = float(f"{unit}E{exposant}")
    return x


def average_range(x: str) -> float:
    """Wikipedia sometimes give a str as a price, sometimes a range.

    Args:
        x (str): tThe value to be casted as a float.

    Returns:
        float: The averaged value.
    """
    x = x.replace(" ", "")
    try:
        x = float(x)
    except ValueError:
        x = [convert_scientific_notation(i) for i in x.split("–")]
        x = np.mean(x)
    return x


def get_chemical_prices() -> pd.DataFrame:
    """Create a dataframe of chemical price/kg in US dollars.

    Returns:
        pd.DataFrame: The created Pandas dataframe.
    """
    # Get the data on wikipedia
    wiki_chemical_price_page = requests.get(
        "https://en.wikipedia.org/wiki/Prices_of_chemical_elements").text
    chemicals_price = pd.read_html(wiki_chemical_price_page, flavor="bs4")[0]
    # Select columns of interest
    chemicals_price = chemicals_price[["Z", "Symbol", "Name", "Price[5]"]]
    chemicals_price = pd.DataFrame(np.array(chemicals_price.values), columns=[
                                   "Z", "symbol", "name", "price/kg", "price/L"]).drop(["price/L"], axis=1)
    # Remove not traded chemicals
    chemicals_price = chemicals_price[chemicals_price["price/kg"]
                                      != "Not traded."]
    # Cast values to numbers
    chemicals_price["Z"] = chemicals_price["Z"].apply(lambda x: int(x))
    return chemicals_price


def get_body_composition() -> pd.DataFrame:
    """Get the human body composition on WIkipedia.

    Returns:
        pd.DataFrame: The created Pandas dataframe.
    """
    # Get the data on Wikipedia
    page = requests.get(
        "https://en.wikipedia.org/wiki/Composition_of_the_human_body").text
    human_composition = pd.read_html(page, flavor="bs4")[1]
    # Split needed information
    human_composition = human_composition[[
        "Element", "Fraction of mass[11][12][13][14][15][16]"]]
    human_composition = pd.DataFrame(
        np.array(human_composition.values), columns=["name", "fraction"])
    human_composition.dropna(inplace=True)
    # COnvert data into numbers
    human_composition["fraction"] = human_composition["fraction"].apply(
        convert_scientific_notation)
    return human_composition


def get_data(weight: float = 70) -> pd.DataFrame:
    """Calls Wikipedia for body composition and chemical prices.
    Merge all information into a single DF, format it, cast dtypers and returns.

    Args:
        weight (float): The weight of the studied body (kg).
    Returns:
        pd.DataFrame: The created DataFrame
    """
    # Get sub dataframes
    chemicals_price = get_chemical_prices()
    human_composition = get_body_composition()
    # Merge them, sort and cast
    global_df = pd.merge(
        human_composition, chemicals_price, how="left").dropna()
    global_df["Z"] = global_df["Z"].apply(lambda x: int(x))
    global_df["price/kg"] = global_df["price/kg"].apply(average_range)
    global_df = global_df.sort_values(by="Z")
    # Apply weight coefficient
    global_df["weight (kg)"] = global_df["fraction"] * weight
    global_df["value (U$D)"] = global_df["weight (kg)"] * global_df["price/kg"]
    return global_df.sort_values(by="weight (kg)", ascending=False)


app = Flask(__name__)


@app.route("/")
def root_index():
    data = get_data(weight=75)
    total_value = data["value (U$D)"].sum()
    return data.to_dict()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))