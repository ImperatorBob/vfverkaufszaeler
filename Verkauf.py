import streamlit as st
import pandas as pd
from datetime import datetime
import os

EXCEL_PATH = "data.xlsx"
DATE_STR = datetime.now().strftime("%d.%m.%Y")

# Initialisiere Excel-Datei
if not os.path.exists(EXCEL_PATH):
    df = pd.DataFrame(columns=["Datum", "Tagesziel", "Verkäufe", "Restmenge"])
    df.to_excel(EXCEL_PATH, index=False)

# Lade Daten
df = pd.read_excel(EXCEL_PATH)
row = df[df["Datum"] == DATE_STR]

if row.empty:
    ziel = 50  # Defaultwert
    sales = 0
    rest = ziel
    df = pd.concat([df, pd.DataFrame([[DATE_STR, ziel, sales, rest]], columns=df.columns)], ignore_index=True)
    df.to_excel(EXCEL_PATH, index=False)
else:
    ziel = int(row["Tagesziel"].values[0])
    sales = int(row["Verkäufe"].values[0])
    rest = int(row["Restmenge"].values[0])

# UI
st.title("🎯 Tagesziel-Tracker")
st.write(f"📅 Datum: {DATE_STR}")

ziel_input = st.number_input("Tagesziel setzen", value=ziel, min_value=0)
if ziel_input != ziel:
    df.loc[df["Datum"] == DATE_STR, "Tagesziel"] = ziel_input
    df.loc[df["Datum"] == DATE_STR, "Restmenge"] = ziel_input - sales
    df.to_excel(EXCEL_PATH, index=False)
    st.experimental_rerun()

st.metric("Verkäufe", sales)
st.metric("Restmenge", max(ziel_input - sales, 0))

if st.button("Verkauf +1"):
    sales += 1
    rest = max(ziel_input - sales, 0)
    df.loc[df["Datum"] == DATE_STR, "Verkäufe"] = sales
    df.loc[df["Datum"] == DATE_STR, "Restmenge"] = rest
    df.to_excel(EXCEL_PATH, index=False)
    st.experimental_rerun()
