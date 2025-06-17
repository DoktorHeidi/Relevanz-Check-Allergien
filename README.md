# Relevanz-Check-Allergien
Analyse von **Krankenkassendaten nach Diagnoseschlüsseln mit Fokus auf Allergien**

Diese Analyse entstand im Rahmen der Abschlusspräsentation meiner Weiterbildung. **Idee, Recherche, Datenauswahl und Umsetzung** wurden vollständig von mir durchgeführt. Die gewonnenen Erkenntnisse können als **Grundlage für weitere Analysen** dienen, sind jedoch nicht als abschließend zu betrachten und könnten Fehler enthalten. Eine Gewähr für die Richtigkeit der Daten und der daraus gewonnenen Erkenntnisse kann nicht übernommen werden.

Da diese Analyse Teil einer gemeinsamen Präsentation mit meiner Mitstreiterin Linda war, habe ich eine **Einleitung zur Gesamt-Thematik** erstellt. Ihr Beitrag ist zumindest in der Sidebar integriert. Aus urheberrechtlichen Gründen sind jedoch keine weiteren Seiten von ihr enthalten.

Die Visualisierungen sind für die Ansicht auf einem **Computerbildschirm optimiert**.

**Anspruch dieser Analyse**
Die analysierten Daten waren in Form von **PDF-Dateien** auf der Homepage des Bundesgesundheitsministeriums verfügbar. Um sie zu verarbeiten, wurden sie von mir mittels Webscraping **automatisiert** heruntergeladen. Da die enthaltenen Tabellen uneinheitlich formatiert waren, musste eine geeignete Methode gefunden werden, um **nur relevante Teile** zu extrahieren. Als beste Lösung erwies sich die Nutzung von pdfplumber.

Nach Erstellung eines Dataframes erfolgte eine weitere **Umgestaltung und Erweiterung der Daten** durch übergeordnete ICD-Kategorien. 

Die **Analyse** wurde **in drei Schritten** durchgeführt: 
- Zunächst wurde eine **Übersicht** über die Daten erstellt.
- Anschließend erfolgte eine Analyse mit standardisierten Daten, um mittels **kMeans** Muster zu erkennen.
- In der dritten Analyse wurden gefilterte Daten verwendet, wobei in manchen Fällen eine Transponierung von Spalten notwendig war.
**Ziel** war es herauszufinden, ob die Anzahl der Fälle bestimmter Diagnose-Schlüssel mit **Assoziation zu Allergien** mit anderen, die **mit Herz-Kreislauf-, Rheuma- und Atemwegserkrankungen** in Verbindung stehen, korrelieren.
