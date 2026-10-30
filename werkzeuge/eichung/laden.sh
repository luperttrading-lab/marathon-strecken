#!/bin/sh
# Lädt Pace Notes v3 (Andrew Kam, Figshare, CC BY 4.0, 1,57 GB) nach $1 (Standard /tmp/pacenotes), prüft die Prüfsumme und
# entpackt ohne features.parquet (Läufer über mehrere Rennen verknüpft, hier nicht gebraucht). Die Rohdaten enthalten Namen:
# nie ins Repo legen.
set -e
Z=${1:-/tmp/pacenotes}; mkdir -p "$Z"; cd "$Z"
curl -sL --retry 4 -o pace-notes-FULL.tar.gz https://ndownloader.figshare.com/files/70458243
echo "6df47d5538023003271a89c289332e964aa136e34b3770ecffd2e704cc8490e5  pace-notes-FULL.tar.gz" | sha256sum -c -
tar xzf pace-notes-FULL.tar.gz --exclude='*/features.parquet' && rm pace-notes-FULL.tar.gz
echo "Daten in $Z/private-export-20261021-1050"
