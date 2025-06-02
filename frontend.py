# frontend.py  – GUI that launches generatorV2.exe (or generatorV2.py)
import os, sys, subprocess, threading, queue
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog, scrolledtext, messagebox, simpledialog

# ───────────────────────── PATHS & MODES ──────────────────────────────
BASE_DIR = Path(sys.argv[0]).resolve().parent      # folder of this script / EXE
FROZEN   = getattr(sys, "frozen", False)           # True after PyInstaller
SCRAPER  = BASE_DIR / ("generatorV2.exe" if FROZEN else "generatorV2.py")
ENV_PATH = BASE_DIR / ".env"                       # stores the API key
# ────────────────────────── ISO-2 country list ─────────────────────────
COUNTRIES = [
    # (code, name)  — FULL list, alphabetically
    ("AF","Afghanistan"),("AX","Åland Islands"),("AL","Albania"),("DZ","Algeria"),
    ("AS","American Samoa"),("AD","Andorra"),("AO","Angola"),("AI","Anguilla"),
    ("AQ","Antarctica"),("AG","Antigua and Barbuda"),("AR","Argentina"),
    ("AM","Armenia"),("AW","Aruba"),("AU","Australia"),("AT","Austria"),
    ("AZ","Azerbaijan"),("BS","Bahamas"),("BH","Bahrain"),("BD","Bangladesh"),
    ("BB","Barbados"),("BY","Belarus"),("BE","Belgium"),("BZ","Belize"),
    ("BJ","Benin"),("BM","Bermuda"),("BT","Bhutan"),("BO","Bolivia"),
    ("BQ","Caribbean Netherlands"),("BA","Bosnia & Herzegovina"),("BW","Botswana"),
    ("BV","Bouvet Island"),("BR","Brazil"),("IO","British Indian Ocean Territory"),
    ("BN","Brunei"),("BG","Bulgaria"),("BF","Burkina Faso"),("BI","Burundi"),
    ("KH","Cambodia"),("CM","Cameroon"),("CA","Canada"),("CV","Cabo Verde"),
    ("KY","Cayman Islands"),("CF","Central African Republic"),("TD","Chad"),
    ("CL","Chile"),("CN","China"),("CX","Christmas Island"),("CC","Cocos (Keeling) Islands"),
    ("CO","Colombia"),("KM","Comoros"),("CG","Congo – Brazzaville"),
    ("CD","Congo – Kinshasa"),("CK","Cook Islands"),("CR","Costa Rica"),
    ("CI","Côte d’Ivoire"),("HR","Croatia"),("CU","Cuba"),("CW","Curaçao"),
    ("CY","Cyprus"),("CZ","Czechia"),("DK","Denmark"),("DJ","Djibouti"),
    ("DM","Dominica"),("DO","Dominican Republic"),("EC","Ecuador"),("EG","Egypt"),
    ("SV","El Salvador"),("GQ","Equatorial Guinea"),("ER","Eritrea"),("EE","Estonia"),
    ("SZ","Eswatini"),("ET","Ethiopia"),("FK","Falkland Islands"),("FO","Faroe Islands"),
    ("FJ","Fiji"),("FI","Finland"),("FR","France"),("GF","French Guiana"),
    ("PF","French Polynesia"),("TF","French Southern Territories"),("GA","Gabon"),
    ("GM","Gambia"),("GE","Georgia"),("DE","Germany"),("GH","Ghana"),("GI","Gibraltar"),
    ("GR","Greece"),("GL","Greenland"),("GD","Grenada"),("GP","Guadeloupe"),
    ("GU","Guam"),("GT","Guatemala"),("GG","Guernsey"),("GN","Guinea"),
    ("GW","Guinea-Bissau"),("GY","Guyana"),("HT","Haiti"),("HM","Heard & McDonald Islands"),
    ("VA","Vatican City"),("HN","Honduras"),("HK","Hong Kong SAR"),("HU","Hungary"),
    ("IS","Iceland"),("IN","India"),("ID","Indonesia"),("IR","Iran"),("IQ","Iraq"),
    ("IE","Ireland"),("IM","Isle of Man"),("IL","Israel"),("IT","Italy"),("JM","Jamaica"),
    ("JP","Japan"),("JE","Jersey"),("JO","Jordan"),("KZ","Kazakhstan"),("KE","Kenya"),
    ("KI","Kiribati"),("KP","North Korea"),("KR","South Korea"),("KW","Kuwait"),
    ("KG","Kyrgyzstan"),("LA","Laos"),("LV","Latvia"),("LB","Lebanon"),("LS","Lesotho"),
    ("LR","Liberia"),("LY","Libya"),("LI","Liechtenstein"),("LT","Lithuania"),
    ("LU","Luxembourg"),("MO","Macao SAR"),("MG","Madagascar"),("MW","Malawi"),
    ("MY","Malaysia"),("MV","Maldives"),("ML","Mali"),("MT","Malta"),("MH","Marshall Islands"),
    ("MQ","Martinique"),("MR","Mauritania"),("MU","Mauritius"),("YT","Mayotte"),
    ("MX","Mexico"),("FM","Micronesia"),("MD","Moldova"),("MC","Monaco"),("MN","Mongolia"),
    ("ME","Montenegro"),("MS","Montserrat"),("MA","Morocco"),("MZ","Mozambique"),
    ("MM","Myanmar"),("NA","Namibia"),("NR","Nauru"),("NP","Nepal"),("NL","Netherlands"),
    ("NC","New Caledonia"),("NZ","New Zealand"),("NI","Nicaragua"),("NE","Niger"),
    ("NG","Nigeria"),("NU","Niue"),("NF","Norfolk Island"),("MK","North Macedonia"),
    ("MP","Northern Mariana Islands"),("NO","Norway"),("OM","Oman"),("PK","Pakistan"),
    ("PW","Palau"),("PS","Palestinian Territories"),("PA","Panama"),("PG","Papua New Guinea"),
    ("PY","Paraguay"),("PE","Peru"),("PH","Philippines"),("PN","Pitcairn Islands"),
    ("PL","Poland"),("PT","Portugal"),("PR","Puerto Rico"),("QA","Qatar"),("RE","Réunion"),
    ("RO","Romania"),("RU","Russia"),("RW","Rwanda"),("BL","St Barthélemy"),
    ("SH","St Helena"),("KN","St Kitts & Nevis"),("LC","St Lucia"),
    ("MF","St Martin"),("PM","St Pierre & Miquelon"),("VC","St Vincent & Grenadines"),
    ("WS","Samoa"),("SM","San Marino"),("ST","São Tomé & Príncipe"),("SA","Saudi Arabia"),
    ("SN","Senegal"),("RS","Serbia"),("SC","Seychelles"),("SL","Sierra Leone"),
    ("SG","Singapore"),("SX","Sint Maarten"),("SK","Slovakia"),("SI","Slovenia"),
    ("SB","Solomon Islands"),("SO","Somalia"),("ZA","South Africa"),("GS","South Georgia & SSI"),
    ("SS","South Sudan"),("ES","Spain"),("LK","Sri Lanka"),("SD","Sudan"),
    ("SR","Suriname"),("SJ","Svalbard & Jan Mayen"),("SE","Sweden"),("CH","Switzerland"),
    ("SY","Syria"),("TW","Taiwan"),("TJ","Tajikistan"),("TZ","Tanzania"),
    ("TH","Thailand"),("TL","Timor-Leste"),("TG","Togo"),("TK","Tokelau"),
    ("TO","Tonga"),("TT","Trinidad & Tobago"),("TN","Tunisia"),("TR","Türkiye"),
    ("TM","Turkmenistan"),("TC","Turks & Caicos Islands"),("TV","Tuvalu"),
    ("UG","Uganda"),("UA","Ukraine"),("AE","United Arab Emirates"),("GB","United Kingdom"),
    ("US","United States"),("UM","U.S. Outlying Islands"),("UY","Uruguay"),
    ("UZ","Uzbekistan"),("VU","Vanuatu"),("VE","Venezuela"),("VN","Vietnam"),
    ("VG","British Virgin Islands"),("VI","U.S. Virgin Islands"),("WF","Wallis & Futuna"),
    ("EH","Western Sahara"),("YE","Yemen"),("ZM","Zambia"),("ZW","Zimbabwe")
]

# ───────────────────── .env HELPERS ────────────────────────────────────
def read_env_key() -> str:
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            if line.split("=",1)[0].strip() == "OPENAI_API_KEY":
                return line.split("=",1)[1].strip()
    return ""

def write_env_key(key: str):
    ENV_PATH.write_text(f"OPENAI_API_KEY={key}\n")

def ensure_api_key() -> bool:
    key = os.environ.get("OPENAI_API_KEY") or read_env_key()
    if key:
        os.environ["OPENAI_API_KEY"] = key
        return True
    key = simpledialog.askstring(
        "OpenAI API Key",
        "Paste your OpenAI API key (starts with ‘sk-’).\n"
        "It will be stored in a local .env file for next time.",
        show="*"
    )
    if key and key.strip():
        key = key.strip()
        os.environ["OPENAI_API_KEY"] = key
        write_env_key(key)
        return True
    messagebox.showerror("Missing key", "An OpenAI API key is required.")
    return False

# ───────────────────── TKINTER GUI SETUP ───────────────────────────────
root = Tk(); root.title("University Contact Scraper")
frm  = ttk.Frame(root, padding=10); frm.grid(sticky="nsew")
root.columnconfigure(0, weight=1); root.rowconfigure(0, weight=1)

# --- Country dropdown --------------------------------------------------
country_var = StringVar()
ttk.Label(frm, text="Country*").grid(row=0, column=0, sticky="w", pady=2)
country_cbx = ttk.Combobox(
    frm, textvariable=country_var, state="readonly", width=35,
    values=[f"{code} — {name}" for code, name in COUNTRIES]
)
country_cbx.grid(row=0, column=1, columnspan=2, sticky="ew", pady=2)

# --- Other input fields ------------------------------------------------
limit_var, outfile_var, probes_var = StringVar(), StringVar(), StringVar()
outfile_modified = [False]

def default_outfile(*_):
    sel = country_var.get().split()
    if sel and not outfile_modified[0]:
        outfile_var.set(f"contacts_{sel[0]}.xlsx")
country_cbx.bind("<<ComboboxSelected>>", default_outfile)

def browse_out():
    fn = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files","*.xlsx"),("CSV files","*.csv"),("All files","*.*")]
    )
    if fn:
        outfile_modified[0] = True
        outfile_var.set(fn)

def add_row(r, label, var, hint="", browse=False):
    ttk.Label(frm, text=label).grid(row=r, column=0, sticky="w", pady=2)
    ent = ttk.Entry(frm, textvariable=var, width=35)
    ent.grid(row=r, column=1, sticky="ew", pady=2)
    if browse:
        ttk.Button(frm, text="Browse…", command=browse_out)\
            .grid(row=r, column=2, padx=4)
    elif hint:
        ttk.Label(frm, text=hint).grid(row=r, column=2, sticky="w", padx=4)

add_row(1, "Limit",   limit_var,  "(default 200)")
add_row(2, "Outfile", outfile_var, "", browse=True)
add_row(3, "Probes",  probes_var, "(default 15)")

# --- Output box & run button ------------------------------------------
output_box = scrolledtext.ScrolledText(frm, width=100, height=25, wrap="none")
output_box.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=(4,0))
frm.rowconfigure(5, weight=1); frm.columnconfigure(1, weight=1)

run_btn = ttk.Button(frm, text="Run"); run_btn.grid(
    row=4, column=0, columnspan=3, pady=(6,4))

# ───────────────────── RUN BUTTON CALLBACK ─────────────────────────────
def run_script():
    sel = country_var.get().strip()
    if not sel:
        messagebox.showerror("Missing country", "Please pick a country."); return
    if not ensure_api_key(): return
    code = sel.split()[0]

    if not SCRAPER.exists():
        messagebox.showerror("Error", f"{SCRAPER} not found"); return

    # Build command for subprocess
    cmd = [str(SCRAPER), code] if FROZEN else [sys.executable, str(SCRAPER), code]
    if limit_var.get().strip():   cmd += ["--limit",  limit_var.get().strip()]
    if outfile_var.get().strip(): cmd += ["--outfile", outfile_var.get().strip()]
    if probes_var.get().strip():  cmd += ["--probes", probes_var.get().strip()]

    # Clear UI & disable button
    output_box.delete(1.0, END); run_btn.config(state=DISABLED)

    # Threaded reader to keep GUI responsive
    q = queue.Queue()

    def reader():
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1, universal_newlines=True
        )
        for line in proc.stdout:
            q.put(line)
        proc.wait(); q.put(f"\n[exit code {proc.returncode}]\n"); q.put(None)

    threading.Thread(target=reader, daemon=True).start()
    poll_queue(q)

def poll_queue(q):
    try:
        while True:
            txt = q.get_nowait()
            if txt is None:
                run_btn.config(state=NORMAL)
                return
            output_box.insert(END, txt); output_box.see(END)
    except queue.Empty:
        pass
    root.after(100, poll_queue, q)

run_btn.config(command=run_script)

root.mainloop()