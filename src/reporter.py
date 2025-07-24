import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.utils.dataframe import dataframe_to_rows
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

def export_to_excel(summary_df: pd.DataFrame, charts_dir="../charts/", out_path="../output/final_report.xlsx"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
        # Export data
        summary_df.to_excel(writer, index=False, sheet_name="Summary")
        writer.save()
    
    # Reload to embed images
    wb = load_workbook(out_path)
    ws = wb["Summary"]

    # Embed charts
    chart_files = ["sales_over_time.png", "top_products_bar.png"]
    for i, chart_file in enumerate(chart_files):
        img_path = os.path.join(charts_dir, chart_file)
        if os.path.exists(img_path):
            img = XLImage(img_path)
            img.width = 600
            img.height = 300
            ws.add_image(img, f"B{35 + i*20}")  # Adjust position as needed

    wb.save(out_path)
    print(f"✅ Excel report saved to {out_path}")

def export_to_pdf(charts_dir="../charts/", out_path="../output/final_report.pdf"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    chart_files = ["sales_over_time.png", "top_products_bar.png"]
    with PdfPages(out_path) as pdf:
        for file in chart_files:
            path = os.path.join(charts_dir, file)
            if os.path.exists(path):
                img = plt.imread(path)
                plt.figure(figsize=(8, 5))
                plt.imshow(img)
                plt.axis('off')
                pdf.savefig()
                plt.close()

    print(f"✅ PDF report saved to {out_path}")