import numpy as np
import pandas as pd
import os

np.random.seed(42)

N = 10000

dates = pd.date_range(
    start="2025-01-01",
    end="2025-12-31",
    periods=N
)

production_lines = np.random.choice(
    ["Line A", "Line B", "Line C", "Line D"],
    N
)

component_types = np.random.choice(
    ["PCB", "Sensor", "IC", "Capacitor", "Connector"],
    N
)

shifts = np.random.choice(
    ["Morning", "Evening", "Night"],
    N,
    p=[0.40, 0.35, 0.25]
)

temperature = np.random.normal(30, 5, N)
humidity = np.random.normal(50, 10, N)
voltage = np.random.normal(5.0, 0.35, N)
current = np.random.normal(2.0, 0.25, N)

machine_age = np.random.randint(1, 15, N)

inspection_score = np.clip(
    np.random.normal(85, 8, N),
    40,
    100
)

downtime = np.random.exponential(15, N)

probability = (
    0.03
    + 0.025 * (temperature > 35)
    + 0.02 * (humidity > 65)
    + 0.025 * (voltage > 5.4)
    + 0.03 * (inspection_score < 75)
    + 0.015 * (machine_age > 10)
    + 0.015 * (downtime > 30)
    + 0.01 * (shifts == "Night")
)

probability = np.clip(
    probability,
    0.01,
    0.70
)

defect = np.random.binomial(
    1,
    probability
)

defect_types = []

for d in defect:

    if d == 1:

        defect_types.append(
            np.random.choice(
                [
                    "Soldering",
                    "Component Failure",
                    "Assembly",
                    "Electrical",
                    "Other"
                ],
                p=[0.30, 0.25, 0.20, 0.15, 0.10]
            )
        )

    else:

        defect_types.append("No Defect")


df = pd.DataFrame({

    "Unit_ID": [
        f"UNIT-{i:05d}"
        for i in range(1, N + 1)
    ],

    "Production_Date": dates,

    "Production_Line": production_lines,

    "Component_Type": component_types,

    "Temperature": temperature.round(2),

    "Humidity": humidity.round(2),

    "Voltage": voltage.round(2),

    "Current": current.round(2),

    "Machine_Age": machine_age,

    "Inspection_Score": inspection_score.round(2),

    "Shift": shifts,

    "Defect_Type": defect_types,

    "Defect": defect,

    "Downtime": downtime.round(2)
})


missing_columns = [
    "Temperature",
    "Humidity",
    "Voltage",
    "Inspection_Score"
]

for column in missing_columns:

    indices = np.random.choice(
        df.index,
        size=int(N * 0.01),
        replace=False
    )

    df.loc[
        indices,
        column
    ] = np.nan


duplicates = df.sample(
    20,
    random_state=42
)

df = pd.concat(
    [df, duplicates],
    ignore_index=True
)

os.makedirs(
    "../data/raw",
    exist_ok=True
)

df.to_csv(
    "../data/raw/manufacturing_quality.csv",
    index=False
)

print("Dataset generated successfully.")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print(
    "Saved to: data/raw/manufacturing_quality.csv"
)
