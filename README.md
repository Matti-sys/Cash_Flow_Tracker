# Cash Flow Tracker

Ein Python-Projekt zur Verwaltung persönlicher Einnahmen und Ausgaben.  
Das Programm ermöglicht das Hinzufügen von Einnahmen und Ausgaben, das Anzeigen aller Transaktionen,  
das Filtern nach Kategorien sowie das automatische Speichern in einer JSON-Datei.

## 📌 Funktionen

- Einnahme hinzufügen  
- Ausgabe hinzufügen  
- Alle Transaktionen anzeigen  
- Nach Kategorien filtern  
- Gesamtsaldo berechnen  
- Geplante Transaktionen berücksichtigen  
- Daten beim Start laden und automatisch speichern  

## 📁 Projektstruktur

Cash_Flow_Tracker/
├── Cash_Flow_Projekt.py
├── data.json
└── README.md

r
Code kopieren

## ▶️ Ausführen des Programms

Im Terminal / Konsole:

python Cash_Flow_Projekt.py

shell
Code kopieren

## 📝 Beispiel einer Transaktion

{
"datum": "2025-01-01",
"betrag": -12.50,
"kategorie": "Essen",
"beschreibung": "Sandwich",
"geplant": false,
"typ": "Ausgabe"
}

markdown
Code kopieren

## ⚙️ Voraussetzungen

- Python 3.x  
- Keine zusätzlichen Bibliotheken erforderlich (nur Standardbibliothek)  
- Optional: `matplotlib` für Diagramme (falls Diagrammfunktion genutzt wird)

## 💡 Hinweise

- Einnahmen haben positive Beträge  
- Ausgaben haben negative Beträge  
- Geplante Transaktionen werden im Saldo erst berücksichtigt, wenn das Datum erreicht ist  
- Beim ersten Start sollte `data.json` die leere Liste `[]` enthalten
