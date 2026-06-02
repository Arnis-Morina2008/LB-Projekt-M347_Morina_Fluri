# Arbeitsjournal & Fazit: Kilian Fluri

## 1. Arbeitsjournal

| Datum | Zeit (Std) | Durchgeführte Arbeiten | Ergebnis / Erkenntnis |
| :--- | :--- | :--- | :--- |
| **26.05.2026** | 3.0 | Projektplanung, Erstellung des Testkonzepts für WordPress und MediaWiki. | Das Testkonzept definiert klare Erwartungen für Erreichbarkeit, Einrichtung und Persistenz der Dienste. |
| **28.05.2026** | 3.5 | Erstellung der Docker-Compose-Datei für Portainer. Testen der Socket-Weiterleitung. | Durch die Socket-Weiterleitung (`/var/run/docker.sock`) kann Portainer alle laufenden Container auf dem Host in Echtzeit erfassen und steuern. |
| **30.05.2026** | 4.5 | Ausarbeitung der Testpläne für Jira und Portainer. Durchführung der manuellen Funktionstests. | Die manuelle Testdurchführung half dabei, Konfigurationslücken (wie fehlende persistente Ordner) frühzeitig zu identifizieren und zu beheben. |
| **02.06.2026** | 3.5 | Verfassen der Installationsanleitung. Erstellung der PDF-Dokumente und Verpacken des Projekts. | Das System lässt sich nun ohne jegliche Vorkonfiguration deployen. Alle Dokumente liegen im geforderten PDF-Format vor. |

**Gesamtstunden:** 14.5 Stunden

---

## 2. Persönliches Fazit
Die Durchführung dieses Projekts hat mir die Relevanz einer sauberen und strukturierten Systemarchitektur verdeutlicht. Die Arbeit mit Docker und Docker Compose zeigt eindrücklich, wie einfach es ist, komplexe Services reproduzierbar bereitzustellen, sofern die Konfigurationsdaten (wie Volumes und Netzwerke) korrekt definiert sind.

Besonders lehrreich war für mich die Erstellung des Testkonzepts und die anschliessende Protokollierung der Testergebnisse. In containerisierten Umgebungen reicht es nicht aus, dass ein Dienst startet – man muss aktiv prüfen, ob Daten nach dem Löschen und erneuten Erstellen eines Containers wirklich persistent bleiben. Unser Testkonzept hat diese Verifikation lückenlos abgedeckt und die Funktionstüchtigkeit aller Microservices nachgewiesen.

Die Einbindung von Portainer als Monitoring-Werkzeug rundet das System ideal ab. Es erleichtert Administratoren die Überwachung ohne tiefe CLI-Kenntnisse. Die Zusammenarbeit mit Arnis verlief reibungslos, da wir uns inhaltlich perfekt ergänzt haben – er fokussierte sich primär auf die compose-bezogene Anwendungs-Stabilität, während mein Schwerpunkt auf Testkonzepten, Portainer-Monitoring und der finalen Dokumentenbereitstellung lag. Das Projekt war ein voller Erfolg.
