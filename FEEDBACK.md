# Feedback: Big Data & Anwendungen Lab – THWS BBA
**URL:** https://swrobuts.github.io/bigdata/  
**Stand:** 2026-03-03  
**Reviewer:** Bot (didaktisch & gestalterisch)  
**Zielgruppe:** BBA-Studierende ab 4. Semester, Einsteiger ohne Big-Data-Vorkenntnisse

---

## ✅ Stärken – Was sehr gut ist

### Konzept & Didaktik
- **Durchgängige MegaStore-Fallstudie** – ein überzeugender roter Faden durch alle 4 Labs mit echten Geschäftsproblemen (Retouren, Churn, Umsatzschwankungen). Abstrakte Technologien bekommen sofort Kontext.
- **Progressive Schwierigkeit** – 4 Stufen pro Lab (geführt → eigenständig → Boss Challenge) sind konsequent umgesetzt und didaktisch erstklassig.
- **Hypothesengetriebenes Lernen** – explizit als Lernprinzip eingebettet. Das ist Hochschuldidaktik auf sehr hohem Niveau.
- **Echte Technologien statt Simulationen** – MongoDB, DuckDB, Neo4j, Spark. Kein Spielzeug, das echte Industrietools.
- **Geschätzte Zeitangaben** pro Lab vorhanden (z.B. "90–120 Minuten").
- **Voraussetzungen** klar kommuniziert ("Docker installiert und ein Terminal…").

### Inhalt
- **5V-Modell** klar und einsteigertauglich erklärt mit Alltagsbeispielen (Netflix, Twitter).
- **Real-World-Use-Cases mit Quellen** (Walmart, PayPal, Netflix, Uber) – schafft Motivation und Glaubwürdigkeit.
- **Quellenangaben** für alle Statistiken – wissenschaftliche Arbeitsweise wird vorgelebt.
- **Self-Check-Fragen** am Ende jedes Labs – sinnvoll und prägnant.
- **Troubleshooting-Sektionen** – spart Stunden in der Sprechstunde.
- **Reflexion & Anwendungen** am Abschluss – gut für Transfer-Lernen.
- **Code mit Copy-Button** – kleines Detail, große Wirkung.
- **6-Sprachen-Support** – Inklusivität für internationale Studierende.
- **Docker Guide** sehr gelungen: Analogien (Versandcontainer, Küche), plattformspezifische Tabellen, klare Schritt-für-Schritt-Führung.

### Design & UX
- Konsistentes Farbschema (Marineblau + Orange) – professionell.
- Seitliche Sidebar-Navigation pro Lab – man verliert sich nicht.
- Difficulty-Badges (BEGINNER / BOSS) auf Anhieb erkennbar.
- Code-Blöcke zweifarbig (Input/Output) – sehr lesbar.

---

## 🔴 Kritische Probleme

*Stand 2026-03-03: Die meisten ursprünglich identifizierten Syntaxfehler (MongoDB findOne ohne `{}`, `#`-Kommentare in MongoDB) wurden bereits in Commit `ceee08f` behoben. Die folgenden Issues beziehen sich auf den aktuellen Code-Stand.*

Keine kritischen Bugs im aktuellen Code gefunden. ✅

---

## 🟡 Mittlere Probleme

### 1. Kapitel-Referenzen ohne Buchverweis
**Wo:** Landing Page → Lab-Karten ("Kapitel 5: NoSQL Datenbanken", "Kapitel 6", "Kapitel 7")

Die Labs verweisen auf Kapitel ohne zu erklären, welches Buch oder Skript gemeint ist. Studierende, die nicht in der Lehrveranstaltung sind (oder Extern-Interessierte), stehen vor einem Fragezeichen.

**Empfehlung:** Entweder kurzen Hinweis ergänzen ("aus dem Kurs-Skript SP_BBA") oder die Labels generischer halten ("NoSQL Grundlagen" statt "Kapitel 5").

---

### 2. Architektur-Diagramm: Sequenzielle Sprache irreführend
**Wo:** Landing Page → "Wie alles zusammenhängt"

Das Diagramm zeigt: Datenerfassung → MongoDB → Neo4j → DuckDB → Spark – als wäre das eine Pipeline, bei der Daten von MongoDB zu Neo4j fließen. In Wirklichkeit arbeiten alle 4 Labs **parallel und unabhängig** auf demselben MegaStore-Datensatz.

**Empfehlung:** Textanpassung bei `ingestDesc` und `storeDesc`: betonen, dass jede Technologie denselben Datensatz aus einer anderen Perspektive beleuchtet – nicht als sequentielle Verarbeitungspipeline.

---

### 3. Keine "Weiter zur nächsten Übung"-Navigation
Am Ende jeder Übung muss der Studierende zurück zur Sidebar navigieren. Besonders für lineare Bearbeitung (Übung 1 → 2 → 3) fehlt ein "Weiter"-Button.

---

### 4. Self-Check ohne Remediations-Link
Die Self-Check-Fragen klappen auf, aber es gibt keinen Hinweis: "Wenn du's nicht weißt → lies nochmal Abschnitt X". Self-Check ohne Lernpfad-Rückkopplung ist nur halb fertig.

---

## 🔵 Kleine Verbesserungen

### 5. `bigdata/`-Unterordner: Veraltetes Nested-Repo
Im Projektverzeichnis liegt ein veralteter `bigdata/`-Unterordner mit eigenem `.git` (Stand: Commit `44b3ead`, deutlich älter als `ceee08f`). Dieser sollte in `.gitignore` aufgenommen oder gelöscht werden, um Verwirrung zu vermeiden.

### 6. Sprachkonsistenz der Lab-Überschriften
Die Lab-Dateien schalten korrekt zwischen 6 Sprachen um. Kleinigkeit: Im MongoDB Lab sind einige UI-Labels (`Welcome to MongoDB Lab`) bei schnellem Sprachwechsel kurzzeitig auf EN sichtbar – i18n-Ladelogik könnte das smoothen.

### 7. Fehlende Index-Erklärung in MongoDB
MongoDB-Performance-Thema (Indexes) wird im Troubleshooting kurz erwähnt (`Use explain()`), aber es gibt keine dedizierte Übung dazu. Für Einsteiger ist Index-Verständnis wertvoll.

### 8. DuckDB: Kein Parquet-Vergleich mit CSV-Performance
DuckDB's Killer-Feature ist die Performance auf Parquet-Dateien. Ein direkter Vorher-/Nachher-Vergleich (CSV vs. Parquet Abfragezeit) würde das "Aha-Erlebnis" stark verstärken.

### 9. Neo4j: Graph-Visualisierung nicht erwähnt
Neo4j Browser zeigt Graphen visuell. Das ist für Einsteiger das beeindruckendste Feature – es sollte explizit als Schritt in den Setup-Anweisungen erwähnt werden ("Hier siehst du deinen ersten Graphen!").

### 10. Spark: MapReduce-Konzept fehlt als Theorie
Das Spark Lab geht direkt in PySpark-Code ohne MapReduce als Konzept zu erklären. Für Einsteiger wäre eine kurze visuelle Erklärung (Map: Aufteilen → Reduce: Zusammenführen) ein hilfreicher mentaler Anker.

---

## 📊 Prioritätenliste

| Prio | Problem | Impact |
|------|---------|--------|
| 🟡 Mittel | Kapitel-Referenzen ohne Buchverweis | Orientierungslosigkeit |
| 🟡 Mittel | Architektur-Diagramm suggeriert Pipeline | Falsches mentales Modell |
| 🟡 Mittel | Keine "Weiter"-Navigation zwischen Übungen | UX-Friction |
| 🟡 Mittel | Self-Check ohne Remediation-Links | Lerneffekt reduziert |
| 🔵 Klein | `bigdata/`-Nested-Repo aufräumen | Repo-Hygiene |
| 🔵 Klein | MongoDB Index-Übung fehlt | Wissenslücke |
| 🔵 Klein | DuckDB Parquet-Performance-Demo | Motivationsfeature |
| 🔵 Klein | Neo4j Visualisierung explizit erwähnen | Wow-Faktor |
| 🔵 Klein | Spark MapReduce Konzept-Erklärung | Beginner-Verständnis |

---

## 💡 Empfehlungen für künftige Erweiterungen

1. **Lab 5 – Redis (Cache & Session Storage):** Die Kursunterlagen enthalten bereits Redis-Beispieldaten (`sample.redis`). Ein kompaktes Redis-Lab würde das Portfolio perfekt ergänzen (Caching, Session-Management, Leaderboards).

2. **Gemeinsames Abschlussprojekt:** Ein "MegaStore Dashboard" das alle 4 Technologien kombiniert und abschließend zeigt, wie sie in einem echten Data-Stack zusammenspielen.

3. **Lernpfad-Visualisierung:** Eine klickbare Roadmap auf der Landing Page ("Du bist hier: Lab 2 von 4") würde den Fortschritt sichtbar machen.

---

*Erstellt: 2026-03-03 | Nächstes Review: Nach Pilotdurchlauf mit Studierenden*
