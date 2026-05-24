# Bachelorarbeit Einlagenmodellierung

## Ziel

Analyse von Bankeinlagen in Abhängigkeit von makroökonomischen Faktoren. Diese Anleitung beschreibt, wie die Python-Skripte zur Bachelorarbeit ausgeführt werden können.

## Setup

### Voraussetzungen

Für die Ausführung werden Python und pip benötigt.

Verwendet wurde:

```bash
Python 3.14.3
```

### Ausführung unter Windows

Im Projektordner `model/` nacheinander folgende Befehle ausführen:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

Falls der Befehle "python" nicht erkannt wird, kann alternativ "py" verwender werden:

```bash
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py src/main.py
```