Mit **generate FLA’s** erstellt der MDA Creator die Animate-Dateien eines Projekts in einem Durchlauf.

- Überträgt die Format- und Sprachkompositionen aus dem gespeicherten AE-Projekt und speichert jede fertige FLA direkt im passenden Formatordner, z. B. `300x600/Projektname_300x600-DE.fla`.
- Fragt einmal vor dem Überschreiben vorhandener FLAs. Bestehende Dateien werden erst nach erfolgreichem Transfer und Speichern ersetzt.
- Zeigt den Fortschritt im pulsierenden Button, hält das MDA-Fenster im Vordergrund und erlaubt den Abbruch per Klick. Bereits fertige Dateien bleiben erhalten.
- Aktualisiert Icons und Button-Beschriftungen nach dem aktuellen Figma-Design.

**Installation:** DMG herunterladen und Grafik Toolbelt nach Programme kopieren. Beide Adobe-Programme schliessen und KeyTween in Toolbelt aktualisieren. Danach beide Panels öffnen und **Connect KeyTween** klicken. Projekt-AEP speichern, im MDA Creator den vorhandenen Projektordner auswählen und **generate FLA’s** starten.

Enthält KeyTween dev.43. HTML-Veröffentlichung und ZIP-Erstellung folgen später. Dev-Build für Intel und Apple Silicon, noch ohne Developer-ID-Signierung/Notarisierung. Falls macOS den Start blockiert: Systemeinstellungen → Datenschutz & Sicherheit → Dennoch öffnen. Der interaktive Adobe-Test erfolgt auf deinem Mac.

<!-- toolbelt-release app-build=20 plugin-version=0.1.0-dev.43 -->
<!-- toolbelt-source revision=d72a097562a95e57b340d55d8f290faa6f1d3701 -->
