# Validierung von Metadaten pro Portal 

Wir können eine Portal URL (nur DKAN-Portale) übergeben und dann bekommen wir eine
JSON Datei mit der Validierung aller vorhandenen Datensätze


## Kommandos:

- `portal` für Portalvalidierung

## Parameter

- `url` der erste Parameter ist die URL des Portals oder einzelne Metadaten-URL
- `-p` Portal Typ: `ckan` oder `dkan`

# Aufruf


```bash
dcat_ap_de_validator portal https://opendata.heilbronn.de/ -p dkan
```
