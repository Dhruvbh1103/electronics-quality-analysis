import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")

df = pd.read_csv(
    "../data/processed/cleaned_quality_data.csv"
)

os.makedirs(
    "../images",
    exist_ok=True
)

# Overall defect distribution

plt.figure(figsize=(7, 5))

sns.countplot(
    data=df,
    x="Defect",
    hue="Defect",
    palette=["#2E86C1", "#E74C3C"],
    legend=False
)

plt.title(
    "Defective vs Non-Defective Units"
)

plt.xlabel("Defect")
plt.ylabel("Number of Units")

plt.xticks(
    [0, 1],
    ["Non-Defective", "Defective"]
)

plt.tight_layout()

plt.savefig(
    "../images/defect_distribution.png",
    dpi=300
)

plt.show()


# Defect rate by production line

line_analysis = (
    df.groupby("Production_Line")
    .agg(
        Total_Units=("Unit_ID", "count"),
        Defective_Units=("Defect", "sum"),
        Defect_Rate=("Defect", "mean")
    )
    .reset_index()
)

line_analysis["Defect_Rate"] *= 100

print("\nDefect Rate by Production Line")
print(line_analysis)


plt.figure(figsize=(9, 5))

sns.barplot(
    data=line_analysis,
    x="Production_Line",
    y="Defect_Rate",
    hue="Production_Line",
    palette="Reds",
    legend=False
)

plt.title(
    "Defect Rate by Production Line"
)

plt.xlabel("Production Line")
plt.ylabel("Defect Rate (%)")

plt.tight_layout()

plt.savefig(
    "../images/defect_rate_by_line.png",
    dpi=300
)

plt.show()


# Defect rate by component

component_analysis = (
    df.groupby("Component_Type")
    .agg(
        Total_Units=("Unit_ID", "count"),
        Defective_Units=("Defect", "sum"),
        Defect_Rate=("Defect", "mean")
    )
    .reset_index()
)

component_analysis["Defect_Rate"] *= 100

print("\nDefect Rate by Component")
print(component_analysis)


plt.figure(figsize=(10, 6))

sns.barplot(
    data=component_analysis.sort_values(
        "Defect_Rate",
        ascending=False
    ),
    x="Component_Type",
    y="Defect_Rate",
    hue="Component_Type",
    palette="Oranges",
    legend=False
)

plt.title(
    "Defect Rate by Component Type"
)

plt.xlabel("Component Type")
plt.ylabel("Defect Rate (%)")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "../images/defect_rate_by_component.png",
    dpi=300
)

plt.show()


# Defect types

defect_type_counts = (
    df[df["Defect"] == 1]["Defect_Type"]
    .value_counts()
)

plt.figure(figsize=(9, 6))

sns.barplot(
    x=defect_type_counts.values,
    y=defect_type_counts.index,
    hue=defect_type_counts.index,
    palette="viridis",
    legend=False
)

plt.title(
    "Distribution of Defect Types"
)

plt.xlabel("Number of Defects")
plt.ylabel("Defect Type")

plt.tight_layout()

plt.savefig(
    "../images/defect_types.png",
    dpi=300
)

plt.show()


# Temperature vs defect

plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="Defect",
    y="Temperature",
    hue="Defect",
    palette=["#2E86C1", "#E74C3C"],
    legend=False
)

plt.title(
    "Temperature by Defect Status"
)

plt.xlabel("Defect")
plt.ylabel("Temperature")

plt.xticks(
    [0, 1],
    ["Non-Defective", "Defective"]
)

plt.tight_layout()

plt.savefig(
    "../images/temperature_vs_defect.png",
    dpi=300
)

plt.show()


# Inspection score

plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="Defect",
    y="Inspection_Score",
    hue="Defect",
    palette=["#2E86C1", "#E74C3C"],
    legend=False
)

plt.title(
    "Inspection Score by Defect Status"
)

plt.xlabel("Defect")
plt.ylabel("Inspection Score")

plt.xticks(
    [0, 1],
    ["Non-Defective", "Defective"]
)

plt.tight_layout()

plt.savefig(
    "../images/inspection_score_vs_defect.png",
    dpi=300
)

plt.show()


# Shift analysis

shift_analysis = (
    df.groupby("Shift")
    .agg(
        Total_Units=("Unit_ID", "count"),
        Defective_Units=("Defect", "sum"),
        Defect_Rate=("Defect", "mean")
    )
    .reset_index()
)

shift_analysis["Defect_Rate"] *= 100

print("\nDefect Rate by Shift")
print(shift_analysis)


plt.figure(figsize=(8, 5))

sns.barplot(
    data=shift_analysis,
    x="Shift",
    y="Defect_Rate",
    hue="Shift",
    palette="Blues",
    legend=False
)

plt.title(
    "Defect Rate by Production Shift"
)

plt.xlabel("Shift")
plt.ylabel("Defect Rate (%)")

plt.tight_layout()

plt.savefig(
    "../images/defect_rate_by_shift.png",
    dpi=300
)

plt.show()


# Correlation matrix

numeric_df = df.select_dtypes(
    include=["int64", "float64"]
)

plt.figure(figsize=(12, 8))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title(
    "Manufacturing Variable Correlation Matrix"
)

plt.tight_layout()

plt.savefig(
    "../images/correlation_matrix.png",
    dpi=300
)

plt.show()


# Summary

print("\n==============================")
print("EDA SUMMARY")
print("==============================")

print(
    "Total Units:",
    len(df)
)

print(
    "Defective Units:",
    df["Defect"].sum()
)

print(
    "Overall Defect Rate:",
    round(
        df["Defect"].mean() * 100,
        2
    ),
    "%"
)

print(
    "Average Inspection Score:",
    round(
        df["Inspection_Score"].mean(),
        2
    )
)

print(
    "Total Downtime:",
    round(
        df["Downtime"].sum(),
        2
    )
)
