# SLIDE 1: Titelblatt
**LB-Projekt M347: Dienst in Betrieb nehmen**
*Eine containerbasierte Multi-Service-Infrastruktur*

**Autoren:** Arnis Morina & Kilian Fluri
**Datum:** 2. Juni 2026
**Präsentationsdauer:** 10 Minuten
**Modul:** M347 - Dienst in Betrieb nehmen (Benedict Schule)

---

# SLIDE 2: Agenda
1. **Projekt-Übersicht & Zielsetzung**
   - Bereitstellung von Web-Applikationen mit Docker Compose.
2. **Eingesetzte Software-Komponenten**
   - WordPress, MediaWiki, Jira Software, Portainer.
3. **Infrastruktur & Netzwerk-Architektur**
   - Isolierung, Port-Mappings und persistente Volumes.
4. **Ablauf des Deployments**
   - Der "Hands-off" Installationsprozess.
5. **Ergebnisse & Fazit**
   - Erkenntnisse aus der Projektarbeit.

---

# SLIDE 3: Software-Komponenten
Die vier Kernkomponenten unseres Systems:
- **WordPress:** Führendes Content Management System (CMS) zur Veröffentlichung von Blog-Artikeln und Webseiten. Gekoppelt an MariaDB.
- **MediaWiki:** Das kollaborative Wissensmanagement-Tool (bekannt durch Wikipedia) zur Dokumentation. Gekoppelt an MariaDB.
- **Jira Software:** Professionelles Projektmanagement- und Bug-Tracking-Tool für agile Teams. Gekoppelt an PostgreSQL.
- **Portainer CE:** Intuitive, webbasierte Benutzeroberfläche zur Containerverwaltung und zum System-Monitoring.

---

# SLIDE 4: Infrastruktur-Architektur
- **Isolierte Brückennetzwerke (Bridge Networks):**
  - Jede Applikation läuft in einem separaten Docker-Netzwerk (z. B. `wordpress_network`), um Inter-Container-Angriffe zu verhindern.
- **Exponierte Ports am Host:**
  - WordPress: `8080` (HTTP)
  - MediaWiki: `8081` (HTTP)
  - Jira Software: `8082` (HTTP, intern 8080)
  - Portainer CE: `9000` (HTTP) / `9443` (HTTPS)
- **Persistenz (Named Volumes):**
  - Daten überleben Container-Löschungen (`docker compose down`). Datenbanken und Web-Inhalte werden in benannten Docker-Volumes auf dem Host dauerhaft gespeichert.

---

# SLIDE 5: Ablauf des Deployments
Wie die Lehrperson das System ohne Anpassungen in Betrieb nimmt:
1. **ZIP entpacken:** Archiv lokal auf dem Host extrahieren.
2. **In das Projektverzeichnis wechseln:** `cd Projekt`
3. **Services starten (jeweils mit docker compose):**
   - `cd wordpress && docker compose up -d && cd ..`
   - `cd mediawiki && docker compose up -d && cd ..`
   - `cd jira && docker compose up -d && cd ..`
   - `cd portainer && docker compose up -d && cd ..`
4. **Zugreifen & Einrichten:** Services über die zugewiesenen Ports im Webbrowser konfigurieren.

---

# SLIDE 6: Fazit & Fragen
- **Erreichung der Projektziele:**
  - Alle Services (WordPress, MediaWiki, Jira, Portainer) laufen stabil und isoliert.
  - Daten bleiben dank Docker Volumes über Container-Neustarts hinweg persistent.
  - Das Deployment erfolgt vollautomatisch ("Hands-off") über standardisierte Konfigurationsdateien.
- **Wichtigste Erkenntnisse:**
  - Richtige Konfiguration der Speicherlimits (speziell für Jira/Java Virtual Machine) ist essenziell für die Host-Stabilität.
  - Separate Netzwerke erhöhen die Sicherheit nachhaltig.

*Vielen Dank für Ihre Aufmerksamkeit. Haben Sie Fragen?*
