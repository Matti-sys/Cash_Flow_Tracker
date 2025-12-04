#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# =========================================================
# DATEN LADEN / SPEICHERN
# =========================================================
def lade_daten():
    try:
        with open("data.json", "r") as f:
            daten = json.load(f)
            print(f"{len(daten)} Transaktionen geladen.")
            return daten
    except FileNotFoundError:
        print("Keine vorherigen Daten gefunden. Neue Liste wird erstellt.")
        with open("data.json", "w") as f:
            json.dump([], f)
        return []

def speichere_daten():
    with open("data.json", "w") as f:
        json.dump(transaktionen, f, indent=4)
    print(f"{len(transaktionen)} Transaktionen gespeichert.")

# =========================================================
# TRANSAKTIONEN HINZUFÜGEN
# =========================================================
def transaktion_hinzufuegen(betrag, kategorie, beschreibung, geplant=False, datum=None, typ="Einnahme"):
    if typ == "Ausgabe":
        betrag = -abs(betrag)
    elif typ == "Einnahme":
        betrag = abs(betrag)

    if datum:
        datum_obj = datetime.strptime(datum, "%Y-%m-%d").date()
    else:
        datum_obj = datetime.today().date()

    transaktion = {
        "betrag": betrag,
        "kategorie": kategorie,
        "beschreibung": beschreibung,
        "datum": datum_obj.strftime("%Y-%m-%d"),
        "geplant": geplant,
        "typ": typ
    }
    transaktionen.append(transaktion)
    print("Transaktion wurde hinzugefügt!")

# =========================================================
# KONTOSTAND BERECHNEN
# =========================================================
def kontostand_berechnen(inkl_planung=False):
    heute = datetime.today().date()
    saldo = 0.0
    for t in transaktionen:
        t_datum = datetime.strptime(t["datum"], "%Y-%m-%d").date()
        if inkl_planung:
            saldo += t["betrag"]
        else:
            if (not t["geplant"]) or (t["geplant"] and t_datum <= heute):
                saldo += t["betrag"]

    if not inkl_planung and saldo < 0:
        print(f"Aktueller Kontostand: {saldo:.2f} € -> Houston we have a problem")
    elif inkl_planung:
        print(f"Voraussichtliches Saldo (inkl. geplanter Transaktionen): {saldo:.2f} €")
    else:
        print(f"Aktueller Kontostand: {saldo:.2f} €")
    return saldo

# =========================================================
# TRANSAKTIONEN ANZEIGEN
# =========================================================
def alle_transaktionen_anzeigen():
    print("\n--- ALLE TRANSAKTIONEN ---")
    for t in transaktionen:
        status = "geplant" if t["geplant"] else "ausgeführt"
        print(f"{t['datum']} | {t['betrag']:.2f} € | {t['kategorie']} | {t['beschreibung']} | {status}")
    print("--------------------------")

def nach_kategorie_filtern(kategorie):
    print(f"\n--- TRANSAKTIONEN IN KATEGORIE '{kategorie}' ---")
    for t in transaktionen:
        if t["kategorie"].lower() == kategorie.lower():
            status = "geplant" if t["geplant"] else "ausgeführt"
            print(f"{t['datum']} | {t['betrag']:.2f} € | {t['beschreibung']} | {status}")
    print("--------------------------")

def transaktionen_suchen():
    suchbegriff = input("Suchbegriff: ").lower()
    print(f"\n--- SUCHERGEBNIS ---")
    for t in transaktionen:
        if (suchbegriff in t["beschreibung"].lower()) or (suchbegriff in t["kategorie"].lower()):
            status = "geplant" if t["geplant"] else "ausgeführt"
            print(f"{t['datum']} | {t['betrag']:.2f} € | {t['kategorie']} | {t['beschreibung']} | {status}")
    print("--------------------------")

def exportiere_csv():
    import csv
    with open("transaktionen.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Datum","Betrag (€)","Kategorie","Beschreibung","Geplant","Typ"])
        for t in transaktionen:
            writer.writerow([t["datum"], t["betrag"], t["kategorie"], t["beschreibung"], t["geplant"], t["typ"]])
    print("CSV-Datei 'transaktionen.csv' erstellt.")

# =========================================================
# SALDO DIAGRAMM
# =========================================================
def diagramm_saldo():
    if not transaktionen:
        print("Keine Transaktionen vorhanden.")
        return

    daten_sortiert = sorted(transaktionen, key=lambda x: datetime.strptime(x["datum"], "%Y-%m-%d"))
    start_datum = datetime.strptime(daten_sortiert[0]["datum"], "%Y-%m-%d").date()
    ende_datum = max(datetime.today().date(), max(datetime.strptime(t["datum"], "%Y-%m-%d").date() for t in daten_sortiert))

    datum_liste = []
    saldo_liste = []
    aktueller_saldo = 0.0
    datum = start_datum
    while datum <= ende_datum + timedelta(days=30):
        tages_transaktionen = [t for t in transaktionen if datetime.strptime(t["datum"], "%Y-%m-%d").date() == datum]
        for t in tages_transaktionen:
            aktueller_saldo += t["betrag"]
        datum_liste.append(datum)
        saldo_liste.append(aktueller_saldo)
        datum += timedelta(days=1)

    plt.figure(figsize=(12,6))
    plt.plot(datum_liste, saldo_liste, marker='o', linestyle='-')
    plt.title("Kontostand Verlauf (inkl. geplanter Transaktionen)")
    plt.xlabel("Datum")
    plt.ylabel("Saldo (€)")
    plt.grid(True)
    plt.axhline(0, color='red', linestyle='--')
    plt.fill_between(datum_liste, saldo_liste, 0, where=[s<0 for s in saldo_liste], color='red', alpha=0.2)
    plt.show()

# =========================================================
# MENÜ
# =========================================================
def menu():
    print("""
====================================
          CASH FLOW TRACKER
====================================
Benutzeranleitung:
1. Einnahmen sofort = positive Werte (Saldo wird aktualisiert)
2. Ausgaben sofort = negative Werte (Saldo wird aktualisiert)
3. Geplante Einnahmen/Ausgaben = werden noch nicht im Saldo berücksichtigt
4. Datum im Format YYYY-MM-DD
5. Daten werden automatisch in 'data.json' gespeichert
====================================
""")
    while True:
        print("\nWähle eine Option:")
        print("1. Einnahme sofort")
        print("2. Ausgabe sofort")
        print("3. Geplante Einnahme")
        print("4. Geplante Ausgabe")
        print("5. Alle Transaktionen anzeigen")
        print("6. Nach Kategorie filtern")
        print("7. Kontostand anzeigen")
        print("8. Voraussichtliches Saldo anzeigen")
        print("9. Transaktionen suchen")
        print("10. CSV exportieren")
        print("11. Saldo Diagramm anzeigen")
        print("12. Speichern & Beenden")

        auswahl = input("Deine Auswahl: ")

        if auswahl in ["1","2","3","4"]:
            betrag = float(input("Betrag: "))
            kategorie = input("Kategorie: ")
            beschreibung = input("Beschreibung: ")
            datum_eingabe = input("Datum (YYYY-MM-DD) oder Enter für heute: ")
            geplant = auswahl in ["3","4"]
            typ = "Ausgabe" if auswahl in ["2","4"] else "Einnahme"
            transaktion_hinzufuegen(betrag, kategorie, beschreibung, geplant, datum_eingabe if datum_eingabe else None, typ)

        elif auswahl == "5":
            alle_transaktionen_anzeigen()
        elif auswahl == "6":
            kategorie = input("Kategorie zum Filtern: ")
            nach_kategorie_filtern(kategorie)
        elif auswahl == "7":
            kontostand_berechnen()
        elif auswahl == "8":
            kontostand_berechnen(inkl_planung=True)
        elif auswahl == "9":
            transaktionen_suchen()
        elif auswahl == "10":
            exportiere_csv()
        elif auswahl == "11":
            diagramm_saldo()
        elif auswahl == "12":
            speichere_daten()
            print("Programm beendet. Auf Wiedersehen!")
            break
        else:
            print("Ungültige Eingabe. Bitte erneut wählen.")

# =========================================================
# START DES PROGRAMMS
# =========================================================
transaktionen = lade_daten()
menu()


# In[ ]:




