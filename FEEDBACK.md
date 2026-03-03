# Feedback: Big Data & Anwendungen Lab – THWS BBA

**URL:** https://swrobuts.github.io/bigdata/  
**Datum:** 2026-03-03  
**Review-Typ:** Didaktik & Gestaltung für Einsteiger  
**Reviewer:** Bot (Mac-Bot, lokaler Assistent)

---

## 🟢 Stärken des Projekts

### Konzept & Didaktik
- ✅ **Durchgängige MegaStore-Fallstudie** – roter Faden durch alle 4 Labs mit echten Business-Problemen (Retouren 23%, Churn 40%, Umsatzeinbrüche). Das gibt abstrakten Technologien Kontext.
- ✅ **Progressive Schwierigkeit** (Beginner → Boss Challenge) – didaktisch sauber, klare Rampe.
- ✅ **Hypothesengetriebenes Lernen** – explizit als Prinzip formuliert ("Bevor du abfragst: Was vermutest du?"). Hochschuldidaktik auf gutem Niveau.
- ✅ **Echte Technologien** – MongoDB, DuckDB, Neo4j, Spark. Keine Simulationen.
- ✅ **Docker-Ansatz** – eliminiert "bei mir läuft's"-Probleme.
- ✅ **Self-Check-Fragen** – sinnvoll platziert, mit Erklärungen.
- ✅ **Real-World Use Cases mit Quellen** – Walmart, PayPal, Netflix, Uber. Das motiviert Studierende.

### Inhalt
- ✅ **Big Data Einführung** klar und zugänglich: 5V-Modell, Datenquellen (IoT, Social Media), KI-Verbindung.
- ✅ **Zeitangaben** bei allen Labs vorhanden (MongoDB 90-120min, DuckDB 90min, Neo4j 2-3h, Spark 3-4h).
- ✅ **Troubleshooting-Sektionen** – praktisch und hilfreich.
- ✅ **Quellenangaben** für Statistiken – vorbildlich.
- ✅ **6-Sprachen-Support** (DE, EN, AR, UK, ES, TR) – internationaler als die meisten Hochschulprojekte.

### Design & UX
- ✅ **Konsistentes Farbschema** (Marineblau + Orange) – professionell.
- ✅ **Saubere Navigation** – Sidebar mit allen Abschnitten, klare Struktur.
- ✅ **Code-Blöcke mit Copy-Button** – kleines Detail, große Wirkung.
- ✅ **Difficulty-Badges** (BEGINNER / BOSS) – auf Anhieb erkennbar.

---

## 🟡 Verbesserungsvorschläge (Mittlere Priorität)

### 1. Lab-Abhängigkeiten nicht klar kommuniziert
**Problem:** MongoDB und DuckDB sind "Anfänger", Neo4j "Mittelstufe", Spark "Fortgeschritten". Aber: Muss MongoDB vor Neo4j gemacht werden? Kann man DuckDB ohne MongoDB-Kenntnisse starten?

**Empfehlung:** Im Intro jedes Labs explizit schreiben:
- "Voraussetzung: Keine Vorkenntnisse aus anderen Labs erforderlich" ODER
- "Voraussetzung: MongoDB Lab abgeschlossen"

### 2. Kapitel-Referenzen ohne Buchverweis
**Wo:** Landing Page → Lab-Karten ("Kapitel 5: NoSQL Datenbanken", "Kapitel 6", etc.)

**Problem:** Welches Buch? Welche Vorlesung? Internationale Studierende oder Quereinsteiger wissen das nicht.

**Empfehlung:** Buchverweis ergänzen oder Labels anpassen zu "Thema 5: NoSQL" statt "Kapitel 5".

### 3. Glossar fehlt
**Problem:** Begriffe wie BSON, ObjectId, OLAP, RDD, DAG, Sharding, Cypher, Graph Traversal tauchen ohne Erklärung auf. Ein Lab-übergreifendes Glossar oder Hover-Tooltips würden Einsteigern helfen.

**Empfehlung:** Entweder eine Glossar-Seite oder inline-Erklärungen beim ersten Auftreten (z.B. "BSON (Binary JSON)").

### 4. Exercise-Schwierigkeitsgrade zu grob
**Wo:** MongoDB Lab – Übungen 1-7 alle "BEGINNER", Übung 8 direkt "BOSS"

**Problem:** Übung 7 (Data Modeling) ist nicht auf demselben Level wie Übung 1 (First Steps).

**Empfehlung:** Granularere Labels: BEGINNER (1-2), INTERMEDIATE (3-5), ADVANCED (6-7), BOSS (8).

### 5. Keine "Weiter"-Navigation am Ende jeder Übung
**Problem:** Am Ende jedes Abschnitts gibt es keinen "Weiter zu Übung 2"-Button. Studierende müssen zurück in die Sidebar.

**Empfehlung:** UX-Verbesserung: "Next Exercise"-Button am Ende jeder Übung.

### 6. Self-Check ohne Remediation-Links
**Problem:** Die Fragen klappen auf (accordion), aber es gibt keinen Hinweis: "Wenn du die Antwort nicht kennst, geh zurück zu Abschnitt X".

**Empfehlung:** Bei jeder Self-Check-Frage einen Rückverweis auf den relevanten Abschnitt.

---

## 🔵 Kleinere Verbesserungen

### 7. MongoDB Setup: URL zu Mongo Express fehlt im Lab
**Problem:** Das Setup zeigt, wie man MongoDB per CLI verbindet, aber die Übersicht verspricht "Mongo Express Web UI". Die URL (`http://localhost:8081`) ist nur im Docker Guide erwähnt, nicht im Lab selbst.

**Empfehlung:** URL im MongoDB Lab Setup-Abschnitt ergänzen.

### 8. Footer GitHub-Link könnte direkter sein
**Wo:** `https://github.com/swrobuts/bigdata` (korrekt)

**Anmerkung:** Link ist OK, könnte aber direkt auf das Repo verlinken (nicht nur Organisation). Aktuell funktioniert es.

---

## ✅ Bereits gelöste Probleme (waren in früherer Analyse)

Diese Punkte aus der Morgen-Analyse sind **bereits im aktuellen Stand behoben**:

1. ✅ MongoDB `findOne( name: ... )` ohne geschweifte Klammern – **behoben** (nicht mehr im Code)
2. ✅ MongoDB Exercise 8 RFM: `#` Kommentare – **nicht vorhanden** (Pipeline nutzt keine Inline-Kommentare mehr oder nutzt `//`)
3. ✅ Zeitangaben fehlten – **behoben** (alle Labs haben `estimatedTime`)
4. ✅ Repo-URL inkonsistent – **behoben** (durchgängig `swrobuts/bigdata`)

---

## 📊 Zusammenfassung

| Kategorie | Bewertung | Notizen |
|-----------|-----------|---------|
| **Didaktisches Konzept** | ⭐⭐⭐⭐⭐ | Durchdacht, progressiv, praxisnah |
| **Fachliche Korrektheit** | ⭐⭐⭐⭐⭐ | Code-Beispiele lauffähig, Technologien korrekt erklärt |
| **Einsteiger-Freundlichkeit** | ⭐⭐⭐⭐☆ | Sehr gut, aber Glossar würde noch helfen |
| **Design & UX** | ⭐⭐⭐⭐⭐ | Professionell, konsistent, gut navigierbar |
| **Vollständigkeit** | ⭐⭐⭐⭐☆ | Umfassend, könnte noch Lab-Abhängigkeiten klären |

**Gesamteindruck:** Professionell gestaltetes, didaktisch durchdachtes Lehrprojekt. Die Verbesserungsvorschläge sind alle "nice to have" – das Projekt ist bereits in sehr gutem Zustand für den Einsatz in der Lehre.

---

## 🎯 Empfohlene nächste Schritte (Priorität)

1. **Hoch:** Lab-Abhängigkeiten im Intro jedes Labs erwähnen
2. **Mittel:** Glossar-Seite oder Tooltips für Fachbegriffe
3. **Mittel:** Exercise-Schwierigkeitsgrade granularer gestalten
4. **Niedrig:** "Weiter"-Navigation am Ende jeder Übung
5. **Niedrig:** Self-Check mit Rückverweisen ausstatten

---

*Review abgeschlossen am 2026-03-03. Bei Fragen zur Umsetzung: siehe `/Users/robert/clawd/memory/bigdata-feedback.md` für die ausführliche Erstanalyse.*
