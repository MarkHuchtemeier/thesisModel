# Bachelorarbeit Einlagenmodellierung

## Ziel
Analyse von Bankeinlagen in Abhängigkeit von makroökonomischen Faktoren. Diese Anleitung beschreibt, wie die Python-Skripte zur Bachelorarbeit ausgeführt werden können.

## Setup

### Voraussetzungen

Für die Ausführung wird Python benötigt. Die benötigten Pakete sind in der Datei `requirements.txt` aufgeführt.

### Ausführung

Im Projektordner `model/` nacheinander folgende Befehle ausführen:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/main.py