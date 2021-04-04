import os
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from utilities import average_range, get_body_composition, get_chemical_prices


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
    global_df = pd.merge(human_composition, chemicals_price,
                         how="left").dropna()
    global_df["Z"] = global_df["Z"].apply(lambda x: int(x))
    global_df["price_per_kg"] = global_df["price/kg"].apply(average_range)
    global_df = global_df.sort_values(by="Z")
    # Apply weight coefficient
    global_df["mass"] = global_df["fraction"] * weight
    global_df["worth"] = global_df["mass"] * global_df["price_per_kg"]
    return global_df.sort_values(by="worth", ascending=False)


def format_chemical(chemicals: List[Dict[str, Any]],
                    element: str) -> Dict[str, str]:
    """Extract the element from a list of dicts and format it for template rendering.

    Args:
        chemicals (List[Dict[str, Any]]): The list of chemicals.
        element (str): The searched chemical.

    Returns:
        Dict[str, str]: The formated dict representing the wished element.
    """
    chemical = next(chemical for chemical in chemicals
                    if chemical["name"] == element)
    chemical["worth"] = round(chemical["worth"], 2)
    return chemical


def compute_other_worths(chemicals: List[Dict[str, Any]]) -> float:
    """Compute the worth of all chemicals, except those that are on the picture.

    Args:
        chemicals (List[Dict[str, Any]]): The complete list of chemicals.

    Returns:
        float: The summed values of other components.
    """
    excluded = ["Oxygen", "Hydrogen", "Nitrogen", "Carbon"]
    values = [
        chemical["worth"] for chemical in chemicals
        if chemical["name"] not in excluded
    ]
    summed_values = float(round(np.sum(values), 2))  # type: ignore
    return summed_values


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def root_index():

    try:
        weight = float(request.form["weight_slider"])
    except KeyError:
        weight = 75
    data = get_data(weight=weight)
    total_value = data["worth"].sum()
    chemicals = data.to_dict('records')

    # Get principal elements
    oxygen = format_chemical(chemicals, "Oxygen")
    carbon = format_chemical(chemicals, "Carbon")
    hydrogen = format_chemical(chemicals, "Hydrogen")
    nitrogen = format_chemical(chemicals, "Nitrogen")

    others_worth = compute_other_worths(chemicals)

    # Create HTML context
    context = {
        "total": round(total_value, 2),
        "weight": int(weight),
        "chemicals": chemicals,
        "oxygen": oxygen,
        "carbon": carbon,
        "hydrogen": hydrogen,
        "nitrogen": nitrogen,
        "others_worth": others_worth
    }
    # Return render template + context
    html_template = render_template("index.html", **context)

    return html_template


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
