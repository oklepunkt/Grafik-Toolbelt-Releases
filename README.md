<p align="center"><img src="docs/app-icon.png" width="112" alt="Grafik-Toolbelt-Icon"></p>
<h1 align="center">Grafik Toolbelt</h1>
<p align="center">Deine kreativen Apps und Adobe-Plugins an einem Ort.</p>
<p align="center"><a href="https://github.com/oklepunkt/Grafik-Toolbelt-Releases/releases/latest"><strong>Neueste Version für macOS herunterladen</strong></a></p>

![Grafik Toolbelt](docs/toolbelt.png)

Grafik Toolbelt installiert und aktualisiert unsere eigenen kreativen Tools. Plugins verwaltest du im kompakten Hauptfenster. Eigenständige Apps wie **MDA Creator** öffnen sich in einem eigenen Fenster.

| Tool | Funktion | Status |
| --- | --- | --- |
| **KeyTween** | Überträgt unterstützte Animationen und Grafiken aus After Effects in bearbeitbare Adobe-Animate-Inhalte. | Dev-Build für After Effects und Animate |
| **MDA Creator** | Arbeitsbereich für Mobile-Display-Ads-Projekte. | Oberfläche als Vorschau; Projektfunktionen in Entwicklung |
| **MasterClip** | Geplante Tools für InDesign und Illustrator. | In Entwicklung |

### Installation

Lade die DMG herunter, öffne sie und ziehe Grafik Toolbelt in den Ordner Programme (Applications). Falls macOS den Preview-Build beim ersten Start blockiert, wähle unter Systemeinstellungen → Datenschutz und Sicherheit «Dennoch öffnen» («Open Anyway») und bestätige mit «Öffnen».

**Voraussetzungen:** macOS 13 oder neuer, Apple Silicon oder Intel. KeyTween benötigt aktuell After Effects 26.x und Animate 24.x mit CEP 12. Die AE-Composition muss für den Transfer auf 30 fps eingestellt sein. Schliesse beide Adobe-Apps vor der Plugin-Installation.

Statische PSD-Compositions werden als einzelnes sRGB-PNG übertragen. Intern animierte Compositions bleiben Symbole. Layer ohne Keyframes verwenden normale gehaltene Frames über ihre gesamte Dauer.

### Updates

Toolbelt prüft GitHub beim Start und alle 30 Minuten auf Updates. Eine manuelle Prüfung findest du unter **Grafik Toolbelt → Check for Updates**. Dev-Builds sind standardmässig enthalten.

Ab Toolbelt **0.6** werden neue KeyTween-Versionen direkt aus GitHub installiert. Dafür muss die Toolbelt-App nicht jedes Mal neu installiert werden. Ältere Toolbelt-Versionen benötigen einmalig das Update auf 0.6.

Der gemeinsame Update-Button neben **KeyTween** aktualisiert alle installierten Panels. Eine laufende Installation kannst du abbrechen; die vorherige Installation wird wiederhergestellt. Sicherungskopien bleiben im gewählten Arbeitsordner. Für Toolbelt-Updates öffnest du die heruntergeladene DMG, beendest die App und ersetzt sie im Ordner Programme.

Die Oberfläche startet mit 120 % Grösse. Über das View-Menü kannst du sie anpassen; deine Auswahl wird gespeichert.

### Preview-Status

Die aktuelle Version ist ein **Preview-Build ohne Apple-Notarisierung**. MDA Creator und MasterClip enthalten Funktionen in Entwicklung. Die neuesten Änderungen benötigen weiterhin Tests in der nativen App und den Adobe-Programmen.

Dieses öffentliche Repository enthält Downloads, Release Notes und Dokumentation. Für den Download ist kein GitHub-Konto nötig. Die Entwicklung liegt in einem separaten privaten Repository. Toolbelt-Releases enthalten die DMG, separate Plugin-Releases das Plugin-ZIP. GitHub ergänzt Quellcodearchive dieses Dokumentations-Repositorys.

— Cedric Okle · Emmi Grafik
