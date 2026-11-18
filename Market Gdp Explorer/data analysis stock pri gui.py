#python
import os
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

import pandas as pd
import plotly.express as px


# ==========================================
# MARKET AND GDP DASHBOARD
# ==========================================

APP_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Stock CSV files and their column names
STOCK_DATA = {
    "Banking": {
        "SBI Bank": {
            "file": "SBIBANK.csv",
            "date": "DateTime",
            "price": "SBINEQN",
            "separator": ","
        },
        "HDFC Bank": {
            "file": "HDFCBANK.csv",
            "date": "Date",
            "price": "EQN",
            "separator": "\t"
        }
    },

    "Automobile": {
        "Maruti Suzuki": {
            "file": "MARUTISUZUKI.csv",
            "date": "DateTime",
            "price": "MARUTIEQN",
            "separator": ","
        },
        "Tata Motors": {
            "file": "TATAMOTORS.csv",
            "date": "DateTime",
            "price": "TMCVEQN",
            "separator": ","
        }
    },

    "IT Companies": {
        "Infosys": {
            "file": "INFOSYS.csv",
            "date": "DateTime",
            "price": "INFYEQN",
            "separator": "\t"
        },
        "TCS": {
            "file": "TCS.csv",
            "date": "DateTime",
            "price": "TCSEQN",
            "separator": ","
        }
    }
}


# GDP values from your original screenshot.
# Confirm the year, currency and data source before presenting them.
GDP_DATA = {
    "India": 6000000000000,
    "China": 21550000000000,
    "Japan": 4340000000000,
    "Bangladesh": 506360000000,
    "Pakistan": 450130000000
}


# ==========================================
# APPLICATION WINDOW
# ==========================================

root = tk.Tk()
root.title("Market & GDP Explorer")
root.geometry("1050x700")
root.minsize(850, 600)
root.configure(bg="#f1f5f9")


# ==========================================
# STYLING
# ==========================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    rowheight=28,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold")
)


# ==========================================
# HEADER
# ==========================================

header = tk.Frame(
    root,
    bg="#172554",
    height=90
)

header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="MARKET & GDP EXPLORER",
    font=("Arial", 22, "bold"),
    fg="white",
    bg="#172554"
).pack(anchor="w", padx=25, pady=(15, 2))

tk.Label(
    header,
    text="Banking | Automobile | IT Companies | Asian GDP",
    font=("Arial", 11),
    fg="#cbd5e1",
    bg="#172554"
).pack(anchor="w", padx=27)


# ==========================================
# MAIN LAYOUT
# ==========================================

main_frame = tk.Frame(
    root,
    bg="#f1f5f9"
)

main_frame.pack(fill="both", expand=True)


# ==========================================
# SIDEBAR
# ==========================================

sidebar = tk.Frame(
    main_frame,
    bg="#111827",
    width=220
)

sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)


tk.Label(
    sidebar,
    text="DASHBOARD MENU",
    font=("Arial", 11, "bold"),
    fg="#94a3b8",
    bg="#111827"
).pack(anchor="w", padx=18, pady=(25, 15))


# ==========================================
# CONTENT AREA
# ==========================================

content = tk.Frame(
    main_frame,
    bg="#f1f5f9"
)

content.pack(
    side="left",
    fill="both",
    expand=True,
    padx=22,
    pady=22
)


def clear_content():
    """Remove existing widgets from the main content area."""
    for widget in content.winfo_children():
        widget.destroy()


def create_title(title, subtitle):
    """Display a page heading."""
    tk.Label(
        content,
        text=title,
        font=("Arial", 22, "bold"),
        fg="#0f172a",
        bg="#f1f5f9"
    ).pack(anchor="w")

    tk.Label(
        content,
        text=subtitle,
        font=("Arial", 10),
        fg="#64748b",
        bg="#f1f5f9"
    ).pack(anchor="w", pady=(4, 18))


def create_card(parent, title, description, command):
    """Create a clickable dashboard card."""
    card = tk.Frame(
        parent,
        bg="white",
        highlightbackground="#cbd5e1",
        highlightthickness=1,
        cursor="hand2"
    )

    tk.Label(
        card,
        text=title,
        font=("Arial", 15, "bold"),
        fg="#1e293b",
        bg="white"
    ).pack(anchor="w", padx=15, pady=(16, 7))

    tk.Label(
        card,
        text=description,
        font=("Arial", 10),
        fg="#64748b",
        bg="white",
        justify="left",
        wraplength=280
    ).pack(anchor="w", padx=15, pady=(0, 16))

    card.bind("<Button-1>", lambda event: command())

    for child in card.winfo_children():
        child.bind("<Button-1>", lambda event: command())

    return card


# ==========================================
# OVERVIEW PAGE
# ==========================================

def show_home():
    clear_content()

    create_title(
        "Dashboard Overview",
        "Choose a sector to explore stock prices and GDP data."
    )

    grid = tk.Frame(content, bg="#f1f5f9")
    grid.pack(fill="x")

    cards = [
        (
            "BANKING",
            "SBI Bank and HDFC Bank\nInteractive stock charts",
            lambda: show_sector("Banking")
        ),
        (
            "AUTOMOBILE",
            "Maruti Suzuki and Tata Motors\nInteractive stock charts",
            lambda: show_sector("Automobile")
        ),
        (
            "IT COMPANIES",
            "Infosys and TCS\nInteractive stock charts",
            lambda: show_sector("IT Companies")
        ),
        (
            "ASIAN GDP",
            "India, China, Japan,\nBangladesh and Pakistan",
            show_gdp
        )
    ]

    for index, (title, description, command) in enumerate(cards):
        card = create_card(
            grid,
            title,
            description,
            command
        )

        card.grid(
            row=index // 2,
            column=index % 2,
            sticky="nsew",
            padx=7,
            pady=7
        )

        grid.grid_columnconfigure(index % 2, weight=1)

    information = tk.Frame(
        content,
        bg="white",
        highlightbackground="#cbd5e1",
        highlightthickness=1
    )

    information.pack(
        fill="both",
        expand=True,
        padx=7,
        pady=(15, 0)
    )

    tk.Label(
        information,
        text="Project Information",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="#0f172a"
    ).pack(anchor="w", padx=18, pady=(16, 10))

    details = [
        "• Four separate dashboard sections.",
        "• Stock prices loaded from your CSV datasets.",
        "• Interactive Plotly charts with zoom and hover details.",
        "• Asian GDP comparison using your original values.",
        "• Simple desktop GUI built with Python Tkinter."
    ]

    for detail in details:
        tk.Label(
            information,
            text=detail,
            font=("Arial", 10),
            bg="white",
            fg="#475569"
        ).pack(anchor="w", padx=20, pady=5)


# ==========================================
# STOCK CSV LOADER
# ==========================================

def load_stock_data(company, settings):
    """
    Load a company's CSV data.

    The code first tries the separator specified for the dataset,
    then checks common alternatives.
    """

    file_path = os.path.join(
        APP_FOLDER,
        settings["file"]
    )

    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"CSV file not found:\n\n{settings['file']}\n\n"
            f"Place it in this folder:\n{APP_FOLDER}"
        )

    separators = list(dict.fromkeys([
        settings["separator"],
        ",",
        "\t",
        ";"
    ]))

    df = None

    for separator in separators:
        try:
            candidate = pd.read_csv(
                file_path,
                sep=separator,
                engine="python"
            )

            if len(candidate.columns) > 1:
                df = candidate
                break

        except Exception:
            continue

    if df is None:
        raise ValueError(
            f"Could not read {settings['file']}."
        )

    # Remove accidental spaces in CSV column headers.
    df.columns = df.columns.astype(str).str.strip()

    date_column = settings["date"]
    price_column = settings["price"]

    # Case-insensitive column matching.
    column_lookup = {
        column.lower(): column
        for column in df.columns
    }

    if date_column not in df.columns:
        date_column = column_lookup.get(
            date_column.lower()
        )

    if price_column not in df.columns:
        price_column = column_lookup.get(
            price_column.lower()
        )

    if date_column is None or price_column is None:
        raise ValueError(
            f"Required columns were not found in "
            f"{settings['file']}.\n\n"
            f"Available columns:\n{', '.join(df.columns)}\n\n"
            f"Expected date column: {settings['date']}\n"
            f"Expected price column: {settings['price']}"
        )

    result = df[[date_column, price_column]].copy()

    result.columns = ["Date", "Price"]

    result["Date"] = pd.to_datetime(
        result["Date"],
        errors="coerce"
    )

    result["Price"] = pd.to_numeric(
        result["Price"]
        .astype(str)
        .str.replace(",", "", regex=False),
        errors="coerce"
    )

    result = result.dropna(
        subset=["Date", "Price"]
    ).sort_values("Date")

    if result.empty:
        raise ValueError(
            f"No valid date and price data found in "
            f"{settings['file']}."
        )

    return result


# ==========================================
# STOCK CHART
# ==========================================

def show_stock_chart(company, settings):
    try:
        df = load_stock_data(company, settings)

        fig = px.line(
            df,
            x="Date",
            y="Price",
            title=f"{company} Stock Price Analysis",
            labels={
                "Date": "Date",
                "Price": "Stock Price"
            },
            hover_data={
                "Date": "|%d %b %Y"
            }
        )

        fig.update_layout(
            template="plotly_white",
            title_x=0.5,
            hovermode="x unified",
            font=dict(family="Arial", size=13),
            xaxis_title="Date",
            yaxis_title="Stock Price"
        )

        fig.update_traces(
            line=dict(width=2),
            hovertemplate=(
                "Date: %{x}<br>"
                "Price: %{y:,.2f}"
                "<extra></extra>"
            )
        )

        output_file = os.path.join(
            APP_FOLDER,
            company.lower().replace(" ", "_") + "_chart.html"
        )

        fig.write_html(
            output_file,
            include_plotlyjs=True
        )

        webbrowser.open(
            "file:///" + os.path.abspath(output_file).replace("\\", "/")
        )

    except Exception as error:
        messagebox.showerror(
            "Chart Error",
            str(error)
        )


# ==========================================
# SECTOR PAGE
# ==========================================

def show_sector(sector):
    clear_content()

    create_title(
        sector + " Dashboard",
        "Select a company and open its interactive stock-price chart."
    )

    companies = STOCK_DATA[sector]

    selector_frame = tk.Frame(
        content,
        bg="white",
        highlightbackground="#cbd5e1",
        highlightthickness=1
    )

    selector_frame.pack(fill="x", pady=(0, 15))

    tk.Label(
        selector_frame,
        text="Select Company:",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#334155"
    ).pack(side="left", padx=18, pady=20)

    selected_company = tk.StringVar(
        value=list(companies.keys())[0]
    )

    company_dropdown = ttk.Combobox(
        selector_frame,
        textvariable=selected_company,
        values=list(companies.keys()),
        state="readonly",
        width=25,
        font=("Arial", 11)
    )

    company_dropdown.pack(
        side="left",
        padx=5,
        pady=15
    )

    details_frame = tk.Frame(
        content,
        bg="white",
        highlightbackground="#cbd5e1",
        highlightthickness=1
    )

    details_frame.pack(
        fill="both",
        expand=True
    )

    tk.Label(
        details_frame,
        text="Company Analysis",
        font=("Arial", 15, "bold"),
        bg="white",
        fg="#0f172a"
    ).pack(anchor="w", padx=20, pady=(20, 12))

    company_info = tk.Label(
        details_frame,
        text="",
        font=("Arial", 11),
        bg="white",
        fg="#475569",
        justify="left",
        anchor="w"
    )

    company_info.pack(
        anchor="w",
        padx=20,
        pady=5
    )

    def update_company_info(*args):
        company = selected_company.get()
        settings = companies[company]

        company_info.config(
            text=(
                f"Company: {company}\n\n"
                f"Dataset: {settings['file']}\n\n"
                f"Date column: {settings['date']}\n\n"
                f"Price column: {settings['price']}"
            )
        )

    company_dropdown.bind(
        "<<ComboboxSelected>>",
        update_company_info
    )

    update_company_info()

    tk.Button(
        details_frame,
        text="OPEN INTERACTIVE CHART",
        command=lambda: show_stock_chart(
            selected_company.get(),
            companies[selected_company.get()]
        ),
        font=("Arial", 11, "bold"),
        bg="#2563eb",
        fg="white",
        activebackground="#1d4ed8",
        activeforeground="white",
        relief="flat",
        padx=20,
        pady=12,
        cursor="hand2"
    ).pack(anchor="w", padx=20, pady=25)

    tk.Label(
        details_frame,
        text="The interactive chart opens in your default web browser.",
        font=("Arial", 10),
        bg="white",
        fg="#64748b"
    ).pack(anchor="w", padx=20, pady=(0, 15))


# ==========================================
# ASIAN GDP DASHBOARD
# ==========================================

def show_gdp():
    clear_content()

    create_title(
        "Asian GDP Dashboard",
        "Compare the GDP values entered in your original Python project."
    )

    panel = tk.Frame(
        content,
        bg="white",
        highlightbackground="#cbd5e1",
        highlightthickness=1
    )

    panel.pack(fill="both", expand=True)

    tk.Label(
        panel,
        text="GDP Comparison",
        font=("Arial", 15, "bold"),
        bg="white",
        fg="#0f172a"
    ).pack(anchor="w", padx=20, pady=(18, 8))

    tk.Label(
        panel,
        text=(
            "The following values are taken from your screenshot. "
            "Confirm their year, currency and source before reporting them."
        ),
        font=("Arial", 10),
        bg="white",
        fg="#64748b",
        wraplength=650,
        justify="left"
    ).pack(anchor="w", padx=20, pady=(0, 12))

    table = ttk.Treeview(
        panel,
        columns=("Country", "GDP"),
        show="headings",
        height=5
    )

    table.heading("Country", text="Country")
    table.heading("GDP", text="GDP Value")

    table.column("Country", width=200)
    table.column("GDP", width=300)

    for country, value in GDP_DATA.items():
        table.insert(
            "",
            "end",
            values=(country, f"{value:,}")
        )

    table.pack(
        fill="x",
        padx=20,
        pady=10
    )

    def open_gdp_chart():
        df = pd.DataFrame({
            "Country": list(GDP_DATA.keys()),
            "GDP": list(GDP_DATA.values())
        })

        fig = px.pie(
            df,
            names="Country",
            values="GDP",
            title="Asian Countries GDP Comparison",
            hole=0.3
        )

        fig.update_layout(
            template="plotly_white",
            title_x=0.5
        )

        output_file = os.path.join(
            APP_FOLDER,
            "asian_countries_gdp_chart.html"
        )

        fig.write_html(
            output_file,
            include_plotlyjs=True
        )

        webbrowser.open(
            "file:///" + os.path.abspath(output_file).replace("\\", "/")
        )

    tk.Button(
        panel,
        text="OPEN GDP CHART",
        command=open_gdp_chart,
        font=("Arial", 11, "bold"),
        bg="#2563eb",
        fg="white",
        activebackground="#1d4ed8",
        activeforeground="white",
        relief="flat",
        padx=20,
        pady=12,
        cursor="hand2"
    ).pack(anchor="w", padx=20, pady=20)


# ==========================================
# NAVIGATION BUTTONS
# ==========================================

navigation = [
    ("⌂  Overview", show_home),
    ("Banking", lambda: show_sector("Banking")),
    ("Automobile", lambda: show_sector("Automobile")),
    ("IT Companies", lambda: show_sector("IT Companies")),
    ("Asian GDP", show_gdp)
]

for label, command in navigation:
    tk.Button(
        sidebar,
        text=label,
        command=command,
        font=("Arial", 11),
        bg="#111827",
        fg="white",
        activebackground="#334155",
        activeforeground="white",
        relief="flat",
        anchor="w",
        padx=18,
        pady=14,
        cursor="hand2"
    ).pack(fill="x", padx=6, pady=3)


# ==========================================
# STATUS BAR
# ==========================================

status_bar = tk.Label(
    root,
    text="Ready | Select a dashboard section from the sidebar.",
    font=("Arial", 9),
    bg="#e2e8f0",
    fg="#334155",
    anchor="w",
    padx=12,
    pady=7
)

status_bar.pack(fill="x", side="bottom")


# ==========================================
# START APPLICATION
# ==========================================

show_home()

root.mainloop()
