import os
import pyodbc
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog

# ----------------------- Configuration -----------------------
DEFAULT_DB = "Blood.accdb"  # default file name to try in current folder
# -------------------------------------------------------------
def connect(self, db_path=None):
    if db_path:
        self.db_path = db_path

    # --- AUTO-CREATE DB FILE IF MISSING ---
    if not os.path.exists(self.db_path):
        try:
            # Make an empty .accdb file
            with open(self.db_path, "wb") as f:
                f.write(b"")  
        except Exception as e:
            return False, f"Failed to create database file: {e}"

    conn_str = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        rf"DBQ={os.path.abspath(self.db_path)};"
    )
    try:
        self.conn = pyodbc.connect(conn_str, autocommit=False)
        self.cursor = self.conn.cursor()
        self._ensure_tables()
        return True, ""
    except Exception as e:
        return False, str(e)

class DatabaseManager:
    def __init__(self, db_path=None):
        self.db_path = db_path or DEFAULT_DB
        self.conn = None
        self.cursor = None

    def connect(self, db_path=None):
        if db_path:
            self.db_path = db_path
        if not os.path.exists(self.db_path):
            # Will still try to connect (user may want to create tables later)
            pass

        conn_str = (
            r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
            rf"DBQ={os.path.abspath(self.db_path)};"
        )
        try:
            self.conn = pyodbc.connect(conn_str, autocommit=False)
            self.cursor = self.conn.cursor()
            self._ensure_tables()
            return True, ""
        except Exception as e:
            return False, str(e)

    def close(self):
        try:
            if self.conn:
                self.conn.close()
        except:
            pass

    def _ensure_tables(self):
        # Create tables if they don't exist (simple checks)
        # NOTE: Access is case-insensitive for identifiers.
        # Table creation SQL — Access supports CREATE TABLE with basic types.
        existing_tables = {row.table_name.upper() for row in self.cursor.tables(tableType='TABLE')}
        # Donors
        if "DONORS" not in existing_tables:
            self.cursor.execute("""
                CREATE TABLE Donors (
                    DonorID AUTOINCREMENT PRIMARY KEY,
                    Name TEXT(255),
                    Contact TEXT(255),
                    Age INTEGER,
                    BloodType TEXT(10),
                    UnitsDonated INTEGER
                )
            """)
        # Patients
        if "PATIENTS" not in existing_tables:
            self.cursor.execute("""
                CREATE TABLE Patients (
                    PatientID AUTOINCREMENT PRIMARY KEY,
                    Name TEXT(255),
                    Contact TEXT(255),
                    Age INTEGER,
                    BloodType TEXT(10),
                    UnitsNeeded INTEGER
                )
            """)
        # BloodStock
        if "BLOODSTOCK" not in existing_tables:
            self.cursor.execute("""
                CREATE TABLE BloodStock (
                    BloodType TEXT(10) PRIMARY KEY,
                    Units INTEGER
                )
            """)
            # initialize stock rows
            for bt in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]:
                self.cursor.execute("INSERT INTO BloodStock (BloodType, Units) VALUES (?, ?)", (bt, 0))
        else:
            # ensure all blood types rows are present
            present = set()
            self.cursor.execute("SELECT BloodType FROM BloodStock")
            for r in self.cursor.fetchall():
                present.add(r[0])
            for bt in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]:
                if bt not in present:
                    self.cursor.execute("INSERT INTO BloodStock (BloodType, Units) VALUES (?, ?)", (bt, 0))

        # History
        if "HISTORY" not in existing_tables:
            self.cursor.execute("""
                CREATE TABLE History (
                    ID AUTOINCREMENT PRIMARY KEY,
                    EntityID INTEGER,
                    EntityType TEXT(50),
                    Name TEXT(255),
                    BloodType TEXT(10),
                    Units INTEGER,
                    Action TEXT(50),
                    EventDate DATETIME
                )
            """)
        self.conn.commit()

    # ---------- Database operations ----------
    def add_donor(self, name, contact, age, blood_type, units):
        self.cursor.execute(
            "INSERT INTO Donors (Name, Contact, Age, BloodType, UnitsDonated) VALUES (?, ?, ?, ?, ?)",
            (name, contact, age, blood_type, units)
        )
        # fetch last inserted autonumber
        donor_id = self.cursor.execute("SELECT @@IDENTITY").fetchone()[0]
        self._update_stock(blood_type, units, "add")
        self._log_history(donor_id, "Donor", name, blood_type, units, "Donated")
        self.conn.commit()
        return donor_id

    def add_patient(self, name, contact, age, blood_type, units_needed):
        self.cursor.execute(
            "INSERT INTO Patients (Name, Contact, Age, BloodType, UnitsNeeded) VALUES (?, ?, ?, ?, ?)",
            (name, contact, age, blood_type, units_needed)
        )
        patient_id = self.cursor.execute("SELECT @@IDENTITY").fetchone()[0]
        if blood_type and units_needed and units_needed > 0:
            self._update_stock(blood_type, units_needed, "subtract")
            self._log_history(patient_id, "Patient", name, blood_type, units_needed, "Needed")
        self.conn.commit()
        return patient_id

    def _update_stock(self, blood_type, units, action):
        # fetch current
        row = self.cursor.execute("SELECT Units FROM BloodStock WHERE BloodType=?", (blood_type,)).fetchone()
        if not row:
            # create row if missing
            current = 0
            self.cursor.execute("INSERT INTO BloodStock (BloodType, Units) VALUES (?, ?)", (blood_type, 0))
        else:
            current = row[0] or 0
        if action == "add":
            new_val = current + units
        else:
            new_val = current - units
            if new_val < 0:
                new_val = 0  # prevent negative stock
        self.cursor.execute("UPDATE BloodStock SET Units=? WHERE BloodType=?", (new_val, blood_type))

    def _log_history(self, entity_id, entity_type, name, blood_type, units, action):
        import datetime
        now = datetime.datetime.now()
        self.cursor.execute("""
            INSERT INTO History (EntityID, EntityType, Name, BloodType, Units, Action, EventDate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (entity_id, entity_type, name, blood_type, units, action, now))

    def fetch_all(self, table):
        self.cursor.execute(f"SELECT * FROM {table}")
        cols = [col[0] for col in self.cursor.description]
        rows = self.cursor.fetchall()
        return cols, rows

    def fetch_stock(self):
        self.cursor.execute("SELECT BloodType, Units FROM BloodStock ORDER BY BloodType")
        return self.cursor.fetchall()


class BloodApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blood Management System")
        self.geometry("900x600")

        self.db = DatabaseManager()
        ok, err = self.db.connect(self._find_default_db())
        if not ok:
            # prompt user to choose DB file
            messagebox.showwarning("DB Connection", f"Couldn't open default DB: {err}\nPlease select your .accdb file.")
            self._choose_db_file()
        else:
            messagebox.showinfo("DB Connected", f"Connected to database: {os.path.abspath(self.db.db_path)}")

        self._create_ui()
        self._refresh_all_views()

    def _find_default_db(self):
        # try current directory for DEFAULT_DB
        cwd = os.getcwd()
        path = os.path.join(cwd, DEFAULT_DB)
        if os.path.exists(path):
            return path
        return DEFAULT_DB  # attempt anyway; user may choose file later

    def _choose_db_file(self):
        f = filedialog.askopenfilename(title="Select Access DB (.accdb/.mdb)", filetypes=[("Access DB", "*.accdb *.mdb"), ("All files", "*.*")])
        if not f:
            messagebox.showerror("No DB", "No database selected. Exiting.")
            self.destroy()
            return
        ok, err = self.db.connect(f)
        if not ok:
            messagebox.showerror("Connection Error", f"Failed to connect: {err}")
            self.destroy()
            return
        messagebox.showinfo("Connected", f"Connected to: {f}")

    def _create_ui(self):
        # Menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        filem = tk.Menu(menubar, tearoff=False)
        filem.add_command(label="Select Database...", command=self._choose_db_file)
        filem.add_separator()
        filem.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filem)

        # Toolbar frame
        toolbar = ttk.Frame(self)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=4, pady=4)

        ttk.Button(toolbar, text="Add Donor", command=self._open_add_donor).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Add Patient", command=self._open_add_patient).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Refresh", command=self._refresh_all_views).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Select DB", command=self._choose_db_file).pack(side=tk.LEFT, padx=4)

        # Notebook for views
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Donors tab
        self.tab_donors = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_donors, text="Donors")
        self._setup_tree(self.tab_donors, "Donors")

        # Patients tab
        self.tab_patients = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_patients, text="Patients")
        self._setup_tree(self.tab_patients, "Patients")

        # Blood Stock tab
        self.tab_stock = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_stock, text="Blood Stock")
        self._setup_stock_view(self.tab_stock)

        # History tab
        self.tab_history = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_history, text="History")
        self._setup_tree(self.tab_history, "History")

    def _setup_tree(self, parent, table_name):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(frame, show="headings")
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)

        # store reference
        setattr(self, f"tree_{table_name.lower()}", tree)

        # right-click menu for copy/export could be added later

    def _setup_stock_view(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        cols = ("Blood Type", "Units")
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor=tk.CENTER, width=120)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)
        self.tree_bloodstock = tree

    # ---------- Add Donor / Patient dialogs ----------
    def _open_add_donor(self):
        dlg = tk.Toplevel(self)
        dlg.title("Add Donor")
        dlg.geometry("350x320")
        dlg.transient(self)
        dlg.grab_set()

        frm = ttk.Frame(dlg, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="Name:").pack(anchor=tk.W)
        ent_name = ttk.Entry(frm)
        ent_name.pack(fill=tk.X)

        ttk.Label(frm, text="Contact:").pack(anchor=tk.W, pady=(8,0))
        ent_contact = ttk.Entry(frm)
        ent_contact.pack(fill=tk.X)

        ttk.Label(frm, text="Age:").pack(anchor=tk.W, pady=(8,0))
        ent_age = ttk.Entry(frm)
        ent_age.pack(fill=tk.X)

        ttk.Label(frm, text="Blood Type:").pack(anchor=tk.W, pady=(8,0))
        cb_bt = ttk.Combobox(frm, values=["A+","A-","B+","B-","AB+","AB-","O+","O-"])
        cb_bt.pack(fill=tk.X)

        ttk.Label(frm, text="Units Donated:").pack(anchor=tk.W, pady=(8,0))
        ent_units = ttk.Entry(frm)
        ent_units.pack(fill=tk.X)

        def submit():
            try:
                name = ent_name.get().strip()
                contact = ent_contact.get().strip()
                age = int(ent_age.get().strip())
                bt = cb_bt.get().strip()
                units = int(ent_units.get().strip())
            except Exception as e:
                messagebox.showerror("Input error", "Check your inputs. Age and Units must be numbers.")
                return
            if not name or not bt:
                messagebox.showerror("Missing", "Name and Blood Type are required.")
                return
            try:
                self.db.add_donor(name, contact, age, bt, units)
                messagebox.showinfo("Success", "Donor added.")
                dlg.destroy()
                self._refresh_all_views()
            except Exception as ex:
                messagebox.showerror("DB error", str(ex))

        ttk.Button(frm, text="Add Donor", command=submit).pack(pady=12)

    def _open_add_patient(self):
        dlg = tk.Toplevel(self)
        dlg.title("Add Patient")
        dlg.geometry("350x360")
        dlg.transient(self)
        dlg.grab_set()

        frm = ttk.Frame(dlg, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="Name:").pack(anchor=tk.W)
        ent_name = ttk.Entry(frm)
        ent_name.pack(fill=tk.X)

        ttk.Label(frm, text="Contact:").pack(anchor=tk.W, pady=(8,0))
        ent_contact = ttk.Entry(frm)
        ent_contact.pack(fill=tk.X)

        ttk.Label(frm, text="Age:").pack(anchor=tk.W, pady=(8,0))
        ent_age = ttk.Entry(frm)
        ent_age.pack(fill=tk.X)

        ttk.Label(frm, text="Needs Blood?").pack(anchor=tk.W, pady=(8,0))
        needs_var = tk.StringVar(value="no")
        rb_yes = ttk.Radiobutton(frm, text="Yes", variable=needs_var, value="yes")
        rb_no = ttk.Radiobutton(frm, text="No", variable=needs_var, value="no")
        rb_yes.pack(anchor=tk.W)
        rb_no.pack(anchor=tk.W)

        ttk.Label(frm, text="Blood Type (if needed):").pack(anchor=tk.W, pady=(8,0))
        cb_bt = ttk.Combobox(frm, values=["A+","A-","B+","B-","AB+","AB-","O+","O-"])
        cb_bt.pack(fill=tk.X)

        ttk.Label(frm, text="Units Needed:").pack(anchor=tk.W, pady=(8,0))
        ent_units = ttk.Entry(frm)
        ent_units.pack(fill=tk.X)

        def submit():
            try:
                name = ent_name.get().strip()
                contact = ent_contact.get().strip()
                age = int(ent_age.get().strip())
                needs = needs_var.get()
                bt = cb_bt.get().strip() if needs == "yes" else "N/A"
                units = int(ent_units.get().strip()) if needs == "yes" else 0
            except Exception as e:
                messagebox.showerror("Input error", "Check your inputs. Age and Units must be numbers.")
                return
            if not name:
                messagebox.showerror("Missing", "Name is required.")
                return
            try:
                self.db.add_patient(name, contact, age, bt if bt else "N/A", units)
                messagebox.showinfo("Success", "Patient added.")
                dlg.destroy()
                self._refresh_all_views()
            except Exception as ex:
                messagebox.showerror("DB error", str(ex))

        ttk.Button(frm, text="Add Patient", command=submit).pack(pady=12)

    # ---------- Refresh / Populate views ----------
    def _refresh_all_views(self):
        try:
            self._populate_table("Donors", getattr(self, "tree_donors"))
            self._populate_table("Patients", getattr(self, "tree_patients"))
            self._populate_table("History", getattr(self, "tree_history"))
            self._populate_stock()
        except Exception as e:
            # if DB disconnected, ignore until user chooses DB
            print("Refresh error:", e)

    def _populate_table(self, table_name, tree_widget):
        cols, rows = self.db.fetch_all(table_name)
        # clear tree columns
        tree_widget.delete(*tree_widget.get_children())
        tree_widget["columns"] = cols
        for c in cols:
            tree_widget.heading(c, text=c)
            tree_widget.column(c, anchor=tk.W, width=110)

        for r in rows:
            # row is pyodbc.Row — convert to tuple
            vals = []
            for i in range(len(r)):
                v = r[i]
                # convert datetime to string if needed
                if hasattr(v, "isoformat"):
                    v = str(v)
                vals.append("" if v is None else str(v))
            tree_widget.insert("", tk.END, values=vals)

    def _populate_stock(self):
        tree = self.tree_bloodstock
        tree.delete(*tree.get_children())
        try:
            rows = self.db.fetch_stock()
            for r in rows:
                tree.insert("", tk.END, values=(r[0], r[1]))
        except Exception as e:
            print("Stock fetch err:", e)

    def on_closing(self):
        try:
            self.db.close()
        except:
            pass
        self.destroy()


if __name__ == "__main__":
    app = BloodApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
