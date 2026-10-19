KeyTween dev.42 verwendet bereits vorbereitete PSD-PNGs erneut und übernimmt den Bildordner eines geöffneten MDA-Projekts.

- Unveränderte PSD-Ebenen und statische Photoshop-Precomps verwenden ihr geprüftes sRGB-PNG aus dem Links-Ordner. Der zweite Transfer benötigt dafür weder AE-Renderqueue noch erneute Farbkonvertierung.
- Quellinhalt, unterstützte Ebenen-/Stileinstellungen, Bildgrösse, Farbkonfiguration und PNG-Prüfsumme werden berücksichtigt. Geänderte, fehlende oder beschädigte Dateien werden neu vorbereitet. Bei nicht zuverlässig erfassbaren Effekten wird weiterhin frisch gerendert.
- Bei geöffnetem MDA Creator mit gewähltem Projekt und bestehender Ordnerstruktur zeigt Image Handling auf dessen `_links`-Ordner. Die eigene Ordnerwahl bleibt gespeichert und gilt wieder, wenn keine passende aktive MDA-Sitzung vorhanden ist.
- Identische vorbereitete Bildkopien erhalten einen gemeinsamen Dateipfad. Vorhandene benutzerbearbeitete Bilder werden nicht überschrieben.
- Alte PNGs ohne Cache-Nachweis benötigen einmal einen neuen Export. Neue Cache-Metadaten liegen im versteckten Unterordner `.keytween-cache`.

In Grafik Toolbelt das Dev-Update für KeyTween installieren und beide Adobe-Panels auf dev.42 aktualisieren. Toolbelt 0.6.7 und das bestehende Team-Passwort bleiben gültig.

Prüfung: 392 Tests auf macOS bestanden, einschliesslich ColorSync und Transfer-/Zugriffsschutz. Vier Tests mit ausschliesslich von Adobe installierten ICC-Fixtures sind auf dem Build-Rechner ausgenommen. Der reale PSD-Render und die Bedienung in Adobe benötigen weiterhin den Mac-Praxistest. Alle 60 Paketdateien stimmen mit dem macOS-CI-Artefakt überein.

<!-- keytween-source revision=7bce81ec5b4e4137327c16e3e5669e44fa6d2bd4 -->
