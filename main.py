import os

import pandas as pd
from flask import Flask, render_template, request
from flask.helpers import url_for
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


app = Flask(__name__)


def get_favicon_path():
    return url_for("static", filename="favicon.ico")


@app.route("/", methods=["GET", "POST"])
def root_index():

    try:
        weight = float(request.form["weight_slider"])
    except KeyError:
        weight = 75
    data = get_data(weight=weight)
    total_value = data["worth"].sum()
    chemicals = data.to_dict('records')

    # Create HTML context
    context = {
        "favicon_path": get_favicon_path(),
        "total": round(total_value, 2),
        "weight": int(weight),
        "chemicals": chemicals}
    # Return render template + context
    html_template = render_template("index.html", **context)

    return html_template


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
