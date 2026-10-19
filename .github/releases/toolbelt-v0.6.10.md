**export HTML’s** veröffentlicht die vorhandenen Animate-Dateien eines MDA-Projekts in einem Durchlauf.

- Arbeitet pro Format alle Sprachen ab und speichert unter `_export/Format/Sprache/Projektname_Format_Sprache.html`. Dazu kommt ein gleichnamiges JPEG-Fallback.
- Nutzt standardmässig den Frame bei 5 Sekunden. Der Zeitpunkt lässt sich im Animate-KeyTween-Panel projektweit ändern.
- Verwendet PNG-/JPEG-Spritesheets und das Clicktag-Template aus `_links`. Fehlt es, erstellt Toolbelt es mit dem Link aus dem MDA Creator.
- Schliesst die zugehörigen offenen FLAs vor dem Export mit Animates Speichern-Rückfrage. Die ursprünglichen FLAs werden beim Veröffentlichen nicht verändert.
- Zeigt Fortschritt im pulsierenden Button und erlaubt den Abbruch. Fertige Exporte bleiben erhalten.

**Installation:** DMG herunterladen und Grafik Toolbelt nach Programme kopieren. Beide Adobe-Programme schliessen und KeyTween auf dev.44 aktualisieren. Danach Animate öffnen, im Panel **Connect KeyTween** klicken und im MDA Creator das vorhandene Projekt mit erstellten FLAs auswählen.

Enthält KeyTween dev.44. ZIP-Erstellung bleibt für einen späteren Schritt vorgesehen. Dev-Build für Intel und Apple Silicon; weiterhin ohne Developer-ID-Signierung/Notarisierung. Automatisierte macOS-Tests bestanden; der tatsächliche Animate-Publisher muss auf deinem Mac geprüft werden.

<!-- toolbelt-release app-build=22 plugin-version=0.1.0-dev.44 -->
<!-- toolbelt-source revision=301732de73be02e01864594d588655a87e9a48f0 -->
