import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import os

class HospitalManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Apply ttk theme for attractive UI
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 12), padding=10, background="#4CAF50", foreground="white")
        style.map("TButton", background=[("active", "#45a049")])
        style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

        # File paths for CSV
        self.patients_file = "patients.csv"
        self.appointments_file = "appointments.csv"

        # Initialize CSV files if not exist
        if not os.path.exists(self.patients_file):
            pd.DataFrame(columns=["ID", "Name", "Age", "Gender", "Issue"]).to_csv(self.patients_file, index=False)
        if not os.path.exists(self.appointments_file):
            pd.DataFrame(columns=["ID", "Patient_ID", "Doctor", "Time", "Status"]).to_csv(self.appointments_file, index=False)

        # Main Frame
        self.main_frame = ttk.Frame(root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(self.main_frame, text="Hospital Management System", font=("Helvetica", 18, "bold")).pack(pady=10)

        # Buttons for actions
        ttk.Button(self.main_frame, text="Add Patient", command=self.add_patient_window).pack(pady=10, fill="x")
        ttk.Button(self.main_frame, text="Book Appointment", command=self.book_appointment_window).pack(pady=10, fill="x")
        ttk.Button(self.main_frame, text="View Patients", command=self.view_patients).pack(pady=10, fill="x")
        ttk.Button(self.main_frame, text="View Appointments", command=self.view_appointments).pack(pady=10, fill="x")
        ttk.Button(self.main_frame, text="Search Records", command=self.search_window).pack(pady=10, fill="x")
        ttk.Button(self.main_frame, text="Exit", command=root.quit).pack(pady=10, fill="x")

    def add_patient_window(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("Add Patient")
        add_win.geometry("400x300")
        add_win.configure(bg="#f0f0f0")

        ttk.Label(add_win, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(add_win)
        name_entry.pack()

        ttk.Label(add_win, text="Age:").pack(pady=5)
        age_entry = ttk.Entry(add_win)
        age_entry.pack()

        ttk.Label(add_win, text="Gender:").pack(pady=5)
        gender_entry = ttk.Entry(add_win)
        gender_entry.pack()

        ttk.Label(add_win, text="Health Issue:").pack(pady=5)
        issue_entry = ttk.Entry(add_win)
        issue_entry.pack()

        def save_patient():
            name, age, gender, issue = name_entry.get(), age_entry.get(), gender_entry.get(), issue_entry.get()
            if not all([name, age, gender, issue]):
                messagebox.showerror("Error", "All fields are required!")
                return
            try:
                age = int(age)
            except ValueError:
                messagebox.showerror("Error", "Age must be a number!")
                return

            df = pd.read_csv(self.patients_file)
            new_id = len(df) + 1
            new_row = pd.DataFrame({"ID": [new_id], "Name": [name], "Age": [age], "Gender": [gender], "Issue": [issue]})
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(self.patients_file, index=False)
            messagebox.showinfo("Success", "Patient added!")
            add_win.destroy()

        ttk.Button(add_win, text="Save", command=save_patient).pack(pady=20)

    def book_appointment_window(self):
        book_win = tk.Toplevel(self.root)
        book_win.title("Book Appointment")
        book_win.geometry("400x300")
        book_win.configure(bg="#f0f0f0")

        ttk.Label(book_win, text="Patient ID:").pack(pady=5)
        pid_entry = ttk.Entry(book_win)
        pid_entry.pack()

        ttk.Label(book_win, text="Doctor Name:").pack(pady=5)
        doctor_entry = ttk.Entry(book_win)
        doctor_entry.pack()

        ttk.Label(book_win, text="Appointment Time (YYYY-MM-DD HH:MM):").pack(pady=5)
        time_entry = ttk.Entry(book_win)
        time_entry.pack()

        def save_appointment():
            pid, doctor, ap_time = pid_entry.get(), doctor_entry.get(), time_entry.get()
            if not all([pid, doctor, ap_time]):
                messagebox.showerror("Error", "All fields are required!")
                return
            try:
                pid = int(pid)
                datetime.strptime(ap_time, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Error", "Invalid Patient ID or Time format!")
                return

            # Check if patient exists
            df_p = pd.read_csv(self.patients_file)
            if pid not in df_p["ID"].values:
                messagebox.showerror("Error", "Patient ID not found!")
                return

            df = pd.read_csv(self.appointments_file)
            new_id = len(df) + 1
            new_row = pd.DataFrame({"ID": [new_id], "Patient_ID": [pid], "Doctor": [doctor], "Time": [ap_time], "Status": ["Scheduled"]})
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(self.appointments_file, index=False)
            messagebox.showinfo("Success", "Appointment booked!")
            book_win.destroy()

        ttk.Button(book_win, text="Book", command=save_appointment).pack(pady=20)

    def view_patients(self):
        view_win = tk.Toplevel(self.root)
        view_win.title("View Patients")
        view_win.geometry("600x400")

        df = pd.read_csv(self.patients_file)
        tree = ttk.Treeview(view_win, columns=list(df.columns), show="headings")
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        for _, row in df.iterrows():
            tree.insert("", "end", values=tuple(row))
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(view_win, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def view_appointments(self):
        view_win = tk.Toplevel(self.root)
        view_win.title("View Appointments")
        view_win.geometry("600x400")

        df = pd.read_csv(self.appointments_file)
        tree = ttk.Treeview(view_win, columns=list(df.columns), show="headings")
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        for _, row in df.iterrows():
            tree.insert("", "end", values=tuple(row))
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(view_win, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def search_window(self):
        search_win = tk.Toplevel(self.root)
        search_win.title("Search Records")
        search_win.geometry("400x200")
        search_win.configure(bg="#f0f0f0")

        ttk.Label(search_win, text="Search by Patient Name:").pack(pady=5)
        search_entry = ttk.Entry(search_win)
        search_entry.pack()

        def perform_search():
            query = search_entry.get().strip().lower()
            if not query:
                messagebox.showerror("Error", "Enter a name to search!")
                return

            df_p = pd.read_csv(self.patients_file)
            results_p = df_p[df_p["Name"].str.lower().str.contains(query)]

            df_a = pd.read_csv(self.appointments_file)
            results_a = df_a[df_a["Patient_ID"].isin(results_p["ID"])]

            # Display results
            result_win = tk.Toplevel(search_win)
            result_win.title("Search Results")
            result_win.geometry("600x400")

            ttk.Label(result_win, text="Patients:").pack(pady=5)
            tree_p = ttk.Treeview(result_win, columns=list(df_p.columns), show="headings")
            for col in df_p.columns:
                tree_p.heading(col, text=col)
            for _, row in results_p.iterrows():
                tree_p.insert("", "end", values=tuple(row))
            tree_p.pack(fill="x", padx=10, pady=5)

            ttk.Label(result_win, text="Appointments:").pack(pady=5)
            tree_a = ttk.Treeview(result_win, columns=list(df_a.columns), show="headings")
            for col in df_a.columns:
                tree_a.heading(col, text=col)
            for _, row in results_a.iterrows():
                tree_a.insert("", "end", values=tuple(row))
            tree_a.pack(fill="x", padx=10, pady=5)

        ttk.Button(search_win, text="Search", command=perform_search).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementSystem(root)
    root.mainloop()