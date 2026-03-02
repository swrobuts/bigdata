# Big Data Lab – THWS

Companion-Website und Docker-Lab-Umgebungen für den Kurs **Schwerpunkt Big Data & Anwendungen** (BBA, THWS).

## 🌐 Website

Die Companion-Website ist unter GitHub Pages erreichbar und enthält:

- **Landing Page** mit Kursüberblick und MegaStore-Fallbeispiel
- **4 Lab-Dokumentationen** mit Schritt-für-Schritt-Anleitungen
- **6 Sprachen**: Deutsch, English, العربية, Українська, Español, Türkçe

## 🐳 Docker Labs

| Lab | Technologie | Kapitel | RAM |
|-----|------------|---------|-----|
| **MongoDB** | Document Store + Python | Kap. 5 | 512 MB |
| **DuckDB** | Analytical SQL + Jupyter | Kap. 6 | 1 GB |
| **Neo4j** | Graph DB + Cypher | Kap. 5 | 768 MB |
| **Spark** | PySpark + Jupyter | Kap. 7 | 1.5 GB |

### Schnellstart

```bash
# 1. Repository klonen
git clone https://github.com/DEIN-USERNAME/bigdata-lab.git
cd bigdata-lab

# 2. Daten generieren
pip install faker pandas pyarrow
python data/generate_megastore_data.py

# 3. Ein Lab starten (z.B. MongoDB)
cd docker
chmod +x start-lab.sh
./start-lab.sh mongodb
```

Jedes Lab läuft unabhängig – ideal für Laptops mit begrenztem RAM.

## 📁 Projektstruktur

```
bigdata-lab/
├── index.html                 # Landing Page
├── lab-mongodb.html           # MongoDB Lab-Dokumentation
├── lab-duckdb.html            # DuckDB Lab-Dokumentation
├── lab-neo4j.html             # Neo4j Lab-Dokumentation
├── lab-spark.html             # Spark Lab-Dokumentation
├── data/
│   ├── generate_megastore_data.py   # Datengenerator
│   └── megastore/                   # Generierte Daten (nicht in Git)
├── docker/
│   ├── mongodb/               # MongoDB Docker-Konfiguration
│   ├── duckdb/                # DuckDB + Jupyter Konfiguration
│   ├── neo4j/                 # Neo4j Docker-Konfiguration
│   ├── spark/                 # Spark + Jupyter Konfiguration
│   ├── start-lab.sh           # Lab-Startskript
│   └── README.md              # Docker-Dokumentation
└── .github/workflows/
    └── deploy.yml             # GitHub Pages Auto-Deployment
```

## 📊 MegaStore-Fallbeispiel

Durchgängiges E-Commerce-Szenario mit ~2 Mio. Datensätzen:

- 5.000 Produkte, 50.000 Kunden, 500.000 Bestellungen
- 1 Mio.+ Bestellpositionen, 200.000 Clickstream-Events
- Formate: CSV, JSON, Parquet

## 🚀 GitHub Pages Setup

1. Repository auf GitHub erstellen
2. Unter **Settings → Pages → Source** auf "GitHub Actions" stellen
3. Push auf `main` löst automatisches Deployment aus

## Lizenz

Erstellt für den Kurs Schwerpunkt Big Data & Anwendungen an der THWS.
Prof. Dr. Robert Butscher
