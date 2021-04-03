import os

import pandas as pd
from flask import Flask
from utilities import average_range, get_chemical_prices, get_body_composition


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
    output = {"total": total_value, "data": data.to_dict()}
    return output


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
