# Arbeitsjournal & Fazit: Arnis Morina

## 1. Arbeitsjournal

| Datum | Zeit (Std) | Durchgeführte Arbeiten | Ergebnis / Erkenntnis |
| :--- | :--- | :--- | :--- |
| **26.05.2026** | 2.5 | Kickoff-Meeting, Besprechung der Anforderungen, Erstellung der Ordnerstruktur. | Die Projektstruktur steht. Wir haben uns entschieden, für jeden Service eine eigene Docker-Compose-Konfiguration zu schreiben. |
| **28.05.2026** | 3.5 | Erstellung der Docker-Compose-Dateien für WordPress und MediaWiki. Konfiguration der MariaDB-Datenbanken. | WordPress lief direkt. Bei MediaWiki stellten wir fest, dass nach dem Web-Setup die `LocalSettings.php` manuell in das Root-Verzeichnis des Containers kopiert werden muss, um Persistenz zu garantieren. |
| **30.05.2026** | 4.0 | Implementierung der Jira Software Compose-Konfiguration. Einbindung von PostgreSQL. | Jira startete anfangs extrem langsam und stürzte ab. Durch das Erhöhen der JVM-Speicherlimits in den Umgebungsvariablen (`JVM_MINIMUM_MEMORY=1024m` und `JVM_MAXIMUM_MEMORY=2048m`) konnten wir den Container stabilisieren. |
| **02.06.2026** | 3.0 | Integration des Portainer-Stack. Tests des Gesamtsystems. Schreiben des persönlichen Fazits. | Alle Stacks laufen stabil nebeneinander. Die Container und Volumes werden in Portainer korrekt visualisiert. |

**Gesamtstunden:** 13.0 Stunden

---

## 2. Persönliches Fazit
Dieses Modulprojekt bot mir eine hervorragende Gelegenheit, meine praktischen Kenntnisse im Bereich der Container-Infrastruktur zu vertiefen. Die Bereitstellung komplexer Web-Applikationen wie WordPress, MediaWiki und insbesondere Atlassian Jira Software über Docker Compose hat verdeutlicht, wie effizient und portabel moderne IT-Dienste orchestriert werden können.

Eine der grössten Herausforderungen war die Konfiguration von Jira. Jira basiert auf Java und benötigt erhebliche Systemressourcen. Ohne die explizite Zuweisung von JVM-Speicherlimits kam es wiederholt zu Speicherengpässen auf dem Host-System. Nachdem wir die Umgebungsvariablen für den Heap-Speicher angepasst hatten, lief Jira jedoch performant und zuverlässig mit dem PostgreSQL-Backend. 

Die Zusammenarbeit im Team mit Kilian war äusserst produktiv. Durch die klare Aufteilung der Aufgaben konnten wir das Projekt effizient und termingerecht abschliessen. Die Kombination aus isolierten Netzwerken und persistenten Volumes stellt eine solide Basis dar, die den Anforderungen der Praxis gerecht wird. Ich fühle mich nun gut vorbereitet für komplexere Deployments in Cloud-Umgebungen.
