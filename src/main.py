from reader import load_and_merge_excels
from cleaner import clean_data
from analyzer import summarize_sales
from plotter import plot_sales_over_time, plot_top_products_bar
from reporter import export_to_excel, export_to_pdf

if __name__ == "__main__":
    df_raw = load_and_merge_excels("../data/")
    df_clean = clean_data(df_raw)
    df_summary = summarize_sales(df_clean)
    
    plot_sales_over_time(df_summary)
    plot_top_products_bar(df_summary)

    export_to_excel(df_summary)
    export_to_pdf()
    print("✅ All tasks completed successfully!")
    print("Check the 'output' directory for the final report and charts.")