# LB-Projekt M347: Dienst in Betrieb nehmen
**Modul:** M347 - Dienst in Betrieb nehmen
**Autoren:** Arnis Morina & Kilian Fluri
**Datum:** 2. Juni 2026
**Schule:** Benedict Schule
**Klasse:** 4. Semester (LB-Projekt)

---

## 1. Einleitung und Zielsetzung
Dieses Projekt dokumentiert die containerbasierte Bereitstellung einer integrierten IT-Infrastruktur für ein fiktives Unternehmen. Ziel ist es, die Web-Applikationen **WordPress**, **MediaWiki** und **Jira Software** automatisiert, persistent und isoliert mittels **Docker Compose** bereitzustellen. Zur Verwaltung und Überwachung der Container-Infrastruktur wird zusätzlich **Portainer** integriert.

Die Bereitstellung zeichnet sich durch folgende Qualitätsmerkmale aus:
- **Isolierung:** Jedes System läuft in seinem eigenen virtuellen Netzwerk, um unbefugten Zugriff zwischen Services zu verhindern.
- **Persistenz:** Sämtliche Daten (Datenbanken, Anwendungsdaten, Bilder und Konfigurationen) werden in benannten Docker-Volumes gesichert.
- **Hands-off-Installation:** Die Systeme lassen sich durch einfache, standardisierte Docker-Compose-Befehle ohne manuelle Vorarbeit starten.

---

## 2. Infrastruktur und Architektur
Das System besteht aus vier eigenständigen Applikations-Stapels (Stacks), die über das Docker-System auf dem Host-Betriebssystem verwaltet werden:

1. **WordPress Stack:**
   - Applikation: `wordpress:latest` (Port 8080)
   - Datenbank: `mariadb:10.11` (interner Port 3306)
   - Verbindung über das isolierte Netzwerk `wordpress_network`.

2. **MediaWiki Stack:**
   - Applikation: `mediawiki:1.41` (Port 8081)
   - Datenbank: `mariadb:10.11` (interner Port 3306)
   - Verbindung über das isolierte Netzwerk `mediawiki_network`.

3. **Jira Stack:**
   - Applikation: `atlassian/jira-software:9.12` (Port 8082)
   - Datenbank: `postgres:15-alpine` (interner Port 5432)
   - Verbindung über das isolierte Netzwerk `jira_network`.

4. **Portainer Stack:**
   - Applikation: `portainer/portainer-ce:latest` (Port 9000 HTTP, Port 9443 HTTPS)
   - Direkter Zugriff auf den Docker-Daemon des Hosts über die Socket-Weiterleitung `/var/run/docker.sock`.

*(Ein detailliertes Infrastrukturdiagramm befindet sich auf der folgenden Seite.)*

---

## 3. Konfiguration der Microservices

### 3.1 WordPress
- **Konfigurationsdatei:** `Projekt/wordpress/docker-compose.yml`
- **Exponierte Ports:** `8080` (HTTP)
- **Persistente Volumes:**
  - `wordpress_db_data` (Pfad im Container: `/var/lib/mysql`)
  - `wordpress_app_data` (Pfad im Container: `/var/www/html`)
- **Umgebungsvariablen (Auswahl):**
  - `WORDPRESS_DB_HOST`: `db:3306`
  - `WORDPRESS_DB_USER`: `wordpress`
  - `WORDPRESS_DB_PASSWORD`: `wordpress_db_secure_pass_2026`
  - `WORDPRESS_DB_NAME`: `wordpress`

### 3.2 MediaWiki
- **Konfigurationsdatei:** `Projekt/mediawiki/docker-compose.yml`
- **Exponierte Ports:** `8081` (HTTP)
- **Persistente Volumes:**
  - `mediawiki_db_data` (Pfad im Container: `/var/lib/mysql`)
  - `mediawiki_app_data` (Pfad im Container: `/var/www/html/images` - für hochgeladene Dateien)
- **Datenbank-Standardeinstellungen:**
  - Host: `db`
  - Datenbankname: `my_wiki`
  - Benutzer: `wikiuser`
  - Passwort: `wiki_db_secure_pass_2026`

### 3.3 Jira Software
- **Konfigurationsdatei:** `Projekt/jira/docker-compose.yml`
- **Exponierte Ports:** `8082` (HTTP, intern 8080)
- **Persistente Volumes:**
  - `jira_db_data` (Pfad im Container: `/var/lib/postgresql/data`)
  - `jira_app_data` (Pfad im Container: `/var/atlassian/application-data/jira`)
- **JVM-Speicherlimits:**
  - `JVM_MINIMUM_MEMORY=1024m` (Ermöglicht stabilen Start)
  - `JVM_MAXIMUM_MEMORY=2048m` (Verhindert Überlastung des Host-RAMs)
- **Datenbank-Einstellungen:**
  - Host: `db:5432`
  - Datenbankname: `jiradb`
  - Treiber: `org.postgresql.Driver`

### 3.4 Portainer (Monitoring & Management)
- **Konfigurationsdatei:** `Projekt/portainer/docker-compose.yml`
- **Exponierte Ports:** `9000` (HTTP Interface), `9443` (HTTPS Web-GUI)
- **Persistente Volumes:**
  - `portainer_app_data` (Pfad im Container: `/data`)
  - Socket: `/var/run/docker.sock` (Lese- und Schreibzugriff)

---

## 4. Testkonzept (Testpläne)
Die Überprüfung der Services erfolgt anhand strukturierter, manueller Testfälle.

### 4.1 WordPress Testkonzept
- **Ziel:** Verifikation der Webschnittstelle, der Datenbankkonnektivität und der Datenpersistenz.
- **Testfälle:**
  - **WP-01: Erreichbarkeit:** Öffnen von `http://localhost:8080` im Browser. Erwartetes Ergebnis: WordPress-Installationsseite erscheint.
  - **WP-02: Erstinstallation & Login:** Eingabe der Daten, Setup abschliessen und erfolgreiches Einloggen ins WordPress-Adminpanel (`http://localhost:8080/wp-admin`).
  - **WP-03: Datenpersistenz:** Erstellen eines Beitrags, anschliessend Stoppen/Löschen der Container (`docker compose down`) und erneutes Starten (`docker compose up -d`). Der Beitrag muss nach dem Neustart unverändert existieren.

### 4.2 MediaWiki Testkonzept
- **Ziel:** Verifikation des Initial-Setups, der Erstellung von Wiki-Seiten und der Medienpersistenz.
- **Testfälle:**
  - **MW-01: Erreichbarkeit:** Öffnen von `http://localhost:8081`. Erwartet: Wiki-Installations-Assistent wird angezeigt.
  - **MW-02: Wiki-Erstellung:** Ausführen des Web-Setups mit DB-Verbindung zu `db`, Generierung und Einpflegen der `LocalSettings.php`.
  - **MW-03: Artikelerstellung & Persistenz:** Erstellen einer Testseite mit Text. Container neu starten (`docker compose restart`). Die Seite muss vorhanden sein.

### 4.3 Jira Testkonzept
- **Ziel:** Überprüfung der ressourcenintensiven Java-Applikation und Verbindung zum PostgreSQL-Backend.
- **Testfälle:**
  - **JR-01: Startverhalten:** Starten der Container. Analyse der Log-Ausgaben (`docker compose logs -f`). Erwartet: Erfolgreicher Start innerhalb von 2 Minuten ohne Out-Of-Memory Error.
  - **JR-02: Erreichbarkeit:** Öffnen von `http://localhost:8082`. Erwartet: Jira Setup-Assistent.
  - **JR-03: Projekt-Erstellung:** Abschluss des Setups (Test-Lizenz) und Erstellung eines Kanban-Boards.

### 4.4 Portainer Testkonzept
- **Ziel:** Überwachung der Docker-Umgebung und Steuerung der Container.
- **Testfälle:**
  - **PT-01: Login-Setup:** Öffnen von `https://localhost:9443`. Erwartet: Aufforderung zur Erstellung des Admin-Kontos.
  - **PT-02: Docker-Integration:** Dashboard prüfen. Erwartet: Lokaler Docker-Socket wird erkannt, laufende Container, Netzwerke und Volumes werden korrekt aufgelistet.

---

## 5. Testprotokolle (Testergebnisse)

Die Tests wurden am 2. Juni 2026 durchgeführt.

| Test-ID | Testbeschreibung | Status | Bemerkung |
| :--- | :--- | :--- | :--- |
| **WP-01** | Öffnen von `http://localhost:8080` | **ERFOLGREICH** | Setup-Seite lädt sofort. |
| **WP-02** | Initial-Konfiguration & Login ins Dashboard | **ERFOLGREICH** | Dashboard lädt flüssig. MariaDB-Konnektivität fehlerfrei. |
| **WP-03** | Datenpersistenz nach Container-Recreation | **ERFOLGREICH** | Erstellter Blogbeitrag existiert weiterhin nach `down` und `up`. |
| **MW-01** | Öffnen von `http://localhost:8081` | **ERFOLGREICH** | MediaWiki-Installationsseite wird angezeigt. |
| **MW-02** | Verbindung zu MariaDB via Web-Assistent | **ERFOLGREICH** | Datenbank wird automatisch initialisiert. `LocalSettings.php` erfolgreich geladen. |
| **MW-03** | Erstellung einer Wiki-Seite und Persistenztest | **ERFOLGREICH** | Inhalt ist nach Container-Neustart vorhanden. |
| **JR-01** | Logs prüfen auf Startzeit und Speicherbedarf | **ERFOLGREICH** | Startet dank 2GB Limit zuverlässig in 85 Sekunden. |
| **JR-02** | Öffnen von `http://localhost:8082` | **ERFOLGREICH** | Einrichtungsassistent ist erreichbar. |
| **JR-03** | Datenbank-Setup & Kanban Board Erstellung | **ERFOLGREICH** | PostgreSQL wird erfolgreich angesprochen und Tabellen generiert. |
| **PT-01** | Initialer Zugriff auf `https://localhost:9443` | **ERFOLGREICH** | SSL-Zertifikatswarnung übersprungen, Admin-Passwort gesetzt. |
| **PT-02** | Visualisierung der laufenden Microservices | **ERFOLGREICH** | Alle 4 Compose-Stacks und Volumes werden in Portainer korrekt angezeigt. |

---

## 6. Installationsanleitung
Folgende Schritte müssen ausgeführt werden, um das gesamte System in Betrieb zu nehmen:

### Vorbedingungen
- Installiertes **Docker Desktop** (für Windows/macOS) oder **Docker Engine** mit **Docker Compose** (für Linux).
- Mindestens 6 GB freier Arbeitsspeicher (RAM) auf dem Host-System (aufgrund von Jira).

### Schritt 1: Entpacken des ZIP-Archivs
Entpacken Sie das übergebene ZIP-Archiv in ein beliebiges Verzeichnis:
```bash
unzip LB-Projekt-M347_Morina_Fluri.zip
cd Projekt
```

### Schritt 2: Starten der Microservices
Die Services können unabhängig voneinander gestartet werden. Führen Sie dazu im jeweiligen Verzeichnis den Befehl `docker compose up -d` aus:

1. **WordPress starten:**
   ```bash
   cd wordpress
   docker compose up -d
   cd ..
   ```
2. **MediaWiki starten:**
   ```bash
   cd mediawiki
   docker compose up -d
   cd ..
   ```
3. **Jira Software starten:**
   ```bash
   cd jira
   docker compose up -d
   cd ..
   ```
4. **Portainer starten:**
   ```bash
   cd portainer
   docker compose up -d
   cd ..
   ```

### Schritt 3: Erstkonfiguration im Webbrowser
- **WordPress:** Öffnen Sie `http://localhost:8080` und folgen Sie den Anweisungen zur Einrichtung der Webseite.
- **MediaWiki:** Öffnen Sie `http://localhost:8081`. Starten Sie die Konfiguration. Geben Sie als Datenbankserver `db` an, als DB-Name `my_wiki`, als DB-Benutzer `wikiuser` und als DB-Passwort `wiki_db_secure_pass_2026`. Nach Abschluss laden Sie die Datei `LocalSettings.php` herunter und verschieben Sie diese per Container-Kopie in den MediaWiki-Container:
  ```bash
  docker cp LocalSettings.php mediawiki_app:/var/www/html/LocalSettings.php
  ```
- **Jira:** Öffnen Sie `http://localhost:8082`. Wählen Sie "Set it up for me" oder "I'll set it up myself". Bei manueller Konfiguration wählen Sie "PostgreSQL" und geben Sie den Host `db`, Datenbank `jiradb`, Benutzer `jirauser` und Passwort `jira_db_secure_pass_2026` an.
- **Portainer:** Öffnen Sie `https://localhost:9443` (oder `http://localhost:9000`), legen Sie ein sicheres Admin-Passwort fest und wählen Sie "Get Started", um die lokale Docker-Umgebung zu verwalten.

---

## 7. Hilfestellungen und Quellenverzeichnis
- **Docker-Dokumentation:** Offizielle Guides für Docker Compose (https://docs.docker.com/compose/)
- **WordPress Docker Image:** Konfigurations-Parameter auf Docker Hub (https://hub.docker.com/_/wordpress)
- **MediaWiki Docker Image:** Installationsanleitungen für MediaWiki in Containern (https://hub.docker.com/_/mediawiki)
- **Atlassian Jira Software Docker:** Parameter für PostgreSQL-Datenbankanbindung (https://hub.docker.com/r/atlassian/jira-software)
- **Portainer Installation Guide:** Docker Compose Setup (https://docs.portainer.io/start/install-ce/docker/pdf)
