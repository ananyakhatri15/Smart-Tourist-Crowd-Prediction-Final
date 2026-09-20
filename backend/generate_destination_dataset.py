import pandas as pd
import numpy as np
# Load files
conditions = pd.read_csv("backend/dataset.csv")
destinations = pd.read_csv("backend/destinaion_data.csv")


# Find minimum and maximum visitor numbers
min_log = np.log1p(destinations["annual_visitors"]).min()
max_log = np.log1p(destinations["annual_visitors"]).max()


def destination_score(visitors):

    log_visitors = np.log1p(visitors)

    score = (
        (log_visitors - min_log)
        / (max_log - min_log)
    ) * 60

    return score


# Calculate crowd index
def get_crowd_score(row):

    score = destination_score(row["annual_visitors"])

    # Day effect
    if row["day"] == "Sunday":
        score += 20

    elif row["day"] in ["Saturday", "Friday"]:
        score += 10

    # Holiday effect
    if row["holiday"] == "Yes":
        score += 10

    # Festival/event effect
    if row["festival"] == "Yes":
        score += 15

    # Rain effect
    if row["weather"] == "Rainy":
        score -= 10

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    return round(score, 2)


# Convert score into crowd category
def get_crowd_category(score):

    if score >= 70:
      return "High"

    elif score >= 40:
      return "Medium"

    else:
     return "Low"


# Create dataset
rows = []

for _, destination in destinations.iterrows():

    for _, condition in conditions.iterrows():

        row = {
            "destination": destination["destination"],
            "annual_visitors": destination["annual_visitors"],
            "day": condition["day"],
            "weather": condition["weather"],
            "holiday": condition["holiday"],
            "festival": condition["festival"]
        }

        score = get_crowd_score(row)

        row["crowd_score"] = score
        row["crowd"] = get_crowd_category(score)

        rows.append(row)


# Create dataframe
new_data = pd.DataFrame(rows)


# Save dataset
new_data.to_csv(
    "backend/destination_dataset.csv",
    index=False
)


print("Destination dataset created successfully!")
print("Total rows:", len(new_data))
print()
print(new_data.head(10))