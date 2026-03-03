# Feedback & Changelog: Big Data Labs – THWS BBA

**Review:** 2026-03-03 | Reviewer: Bot (systematische Code-Prüfung + didaktisches Review)

---

## ✅ Umgesetzte Fixes (dieser Commit)

### 🔴 Kritische Bugs – behoben

**1. MongoDB Lab – Exercise 5: Task/Code-Mismatch**
- **Problem:** Übungsaufgabe fragte nach `db.order_items.aggregate()`, aber das Beispiel zeigte `db.orders.aggregate()`. Einsteiger konnten die Aufgabe nicht lösen ohne $lookup aus Ex6.
- **Fix:** Task auf `orders`-Collection angepasst. Neue Aufgabe: Bestellungen pro Status zählen und Gesamtumsatz berechnen – konsistent mit Beispiel-Code.

**2. MongoDB Lab – RFM Pipeline: `$addFields`-Stage-Bug**
- **Problem:** `rfm_score` und `segment` wurden in derselben `$addFields`-Stage berechnet. MongoDB erlaubt keine Vorwärtsreferenz innerhalb einer Stage — `segment` konnte `rfm_score` nicht nutzen.
- **Fix:** Zweite `$addFields`-Stage in zwei separate Stages aufgeteilt: erst `rfm_score`, dann `segment`.

**3. Spark Lab – Exercise 6: `customers` Variable undefiniert**
- **Problem:** Ex6 referenziert `customers.join(orders, ...)` aber die Variable `customers` wurde nie definiert. Ex1 lädt die Datei als `df`. → `NameError` beim Ausführen.
- **Fix:** `customers = spark.read.csv(...)` explizit am Anfang von Ex6 definiert.

### 🟡 Didaktische Verbesserungen – umgesetzt

**4. Neo4j Lab – Exercise 6: Beschreibung vereinfacht**
- **Problem:** "Collaborative Filtering" und "Recommendation Engine" wirken einschüchternd für Einsteiger.
- **Fix:** Aufgabe umformuliert: "Finde alle Kunden, die dasselbe Produkt wie Alice gekauft haben." Hint erklärt das Graph-Muster Schritt für Schritt.

**5. Neo4j Lab – Prerequisites ergänzt**
- Lab-Abhängigkeit klargestellt: MongoDB Lab empfohlen als Einstieg.

**6. Spark Lab – Prerequisites ergänzt**
- Lab-Abhängigkeit klargestellt: DuckDB Lab empfohlen, Spark als fortgeschrittenstes Lab markiert.

---

## 🟢 Stärken des Projekts (bereits in sehr gutem Zustand)

- Durchgängige MegaStore-Fallstudie mit echten Business-Szenarien
- Progressive Schwierigkeit pro Lab (Beginner → Boss)
- SQL-Analogien für MongoDB und DuckDB – ideal für Studierende mit SQL-Vorwissen
- Alle Labs mit Zeitangaben, Troubleshooting und Self-Check
- 6-Sprachen-Support, Copy-Buttons, "Next Exercise"-Navigation

---

## 🔵 Offene Verbesserungsvorschläge (nächste Iteration)

1. **Glossar** – BSON, ObjectId, DAG, RDD, Cypher beim ersten Auftreten erklären
2. **Intermediate Badges** – Übungen 3-5 mit `INTERMEDIATE` statt nur `BEGINNER` markieren
3. **DuckDB Ex1** – `SELECT 42` als Einstieg ist sehr trivial; könnte ein echtes DuckDB-Feature (z.B. direkte CSV-Abfrage) zeigen
4. **MongoDB Fundamentals** – CRUD-Tabelle könnte interaktiv sein (jede Operation ausklappbar)
5. **Self-Check Back-Links** – Bei jeder Frage auf den relevanten Abschnitt verweisen

---

*Letzte Aktualisierung: 2026-03-03*
