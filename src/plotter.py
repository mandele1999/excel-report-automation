import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_sales_over_time(df: pd.DataFrame, out_dir="../charts/"):
    os.makedirs(out_dir, exist_ok=True)

    top_products = df.groupby("product")["sales"].sum().sort_values(ascending=False).head(5).index.tolist()
    df_top = df[df['product'].isin(top_products)]

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_top, x="date", y="sales", hue="product", marker="o")
    plt.title("Sales Over Time (Top Products)")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.legend(title="Product")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "sales_over_time.png"))
    plt.close()

def plot_top_products_bar(df: pd.DataFrame, out_dir="../charts/"):
    os.makedirs(out_dir, exist_ok=True)

    top_sales = (
        df.groupby("product")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_sales.values, y=top_sales.index, palette="Blues_d")
    plt.title("Top Products by Total Sales")
    plt.xlabel("Total Sales")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "top_products_bar.png"))
    plt.close()