import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading

from reader import load_and_merge_excels
from cleaner import clean_data
from analyzer import summarize_sales
from plotter import plot_sales_over_time, plot_top_products_bar
from reporter import export_to_excel, export_to_pdf
# from emailer import send_email_report  # Placeholder for optional email module

class ReportApp:
    def __init__(self, master):
        self.master = master
        master.title("Excel Reporting Automation")
        master.geometry("500x300")

        self.folder_path = tk.StringVar()
        self.email_address = tk.StringVar()

        # Folder selection
        tk.Label(master, text="Select Excel Data Folder:").pack(pady=5)
        tk.Entry(master, textvariable=self.folder_path, width=60).pack()
        tk.Button(master, text="Browse", command=self.browse_folder).pack(pady=5)

        # Email input
        tk.Label(master, text="Enter Email (optional):").pack(pady=5)
        tk.Entry(master, textvariable=self.email_address, width=60).pack()

        # Generate button
        tk.Button(master, text="Generate Report", command=self.run_report_threaded).pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(master, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        self.status_label = tk.Label(master, text="", fg="blue")
        self.status_label.pack()

    def browse_folder(self):
        selected = filedialog.askdirectory()
        if selected:
            self.folder_path.set(selected)

    def run_report_threaded(self):
        t = threading.Thread(target=self.generate_report)
        t.start()

    def generate_report(self):
        try:
            self.set_status("Starting report generation...")
            self.progress["value"] = 0
            self.master.update_idletasks()

            data_dir = self.folder_path.get()
            if not os.path.exists(data_dir):
                raise Exception("Invalid folder path.")

            df_raw = load_and_merge_excels(data_dir)
            self.set_progress(20, "Cleaning data...")
            df_clean = clean_data(df_raw)

            self.set_progress(40, "Analyzing summary...")
            df_summary = summarize_sales(df_clean)

            self.set_progress(60, "Generating charts...")
            plot_sales_over_time(df_summary)
            plot_top_products_bar(df_summary)

            self.set_progress(80, "Exporting to Excel & PDF...")
            export_to_excel(df_summary)
            export_to_pdf()

            email = self.email_address.get().strip()
            if email:
                self.set_progress(90, f"Sending to {email}... (placeholder)")
                # send_email_report(email, attachments=["output/final_report.xlsx", "output/final_report.pdf"])
                print(f"[Simulated] Email sent to {email}")

            self.set_progress(100, "Done.")
            messagebox.showinfo("Success", "Report generated successfully!")

        except Exception as e:
            self.set_status("Error during report generation.")
            messagebox.showerror("Error", str(e))

    def set_progress(self, val, message=""):
        self.progress["value"] = val
        self.set_status(message)
        self.master.update_idletasks()

    def set_status(self, msg):
        self.status_label.config(text=msg)