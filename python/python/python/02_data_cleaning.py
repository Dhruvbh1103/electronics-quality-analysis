import pandas as pd
import os

df = pd.read_csv(
    "../data/raw/manufacturing_quality.csv"
)

print("Original Shape:", df.shape)

df["Production_Date"] = pd.to_datetime(
    df["Production_Date"],
    errors="coerce"
)

df = df.drop_duplicates()

numerical_columns = [
    "Temperature",
    "Humidity",
    "Voltage",
    "Current",
    "Machine_Age",
    "Inspection_Score",
    "Downtime"
]

for column in numerical_columns:

    df[column] = df[column].fillna(
        df[column].median()
    )

categorical_columns = [
    "Production_Line",
    "Component_Type",
    "Shift",
    "Defect_Type"
]

for column in categorical_columns:

    df[column] = df[column].fillna(
        df[column].mode()[0]
    )

for column in categorical_columns:

    df[column] = (
        df[column]
        .astype(str)
        .str.strip()
    )

df["Defect"] = df["Defect"].astype(int)

os.makedirs(
    "../data/processed",
    exist_ok=True
)

df.to_csv(
    "../data/processed/cleaned_quality_data.csv",
    index=False
)

print("Cleaning completed.")
print("Final Shape:", df.shape)

print(
    "Remaining Missing Values:",
    df.isnull().sum().sum()
)

print(
    "Duplicate Rows:",
    df.duplicated().sum()
)

print(
    "Defect Rate:",
    round(
        df["Defect"].mean() * 100,
        2
    ),
    "%"
)
