JDF2GTFS
========

Convert JDF files to GTFS

## Instalace
 * naklonovat tento repozitář
 * nainstalovat PostgreSQL server a vytvořit databázi `jdf`, kterou vlastní uživatel spouštějící skripty
 * nainstalovat gcc, make, dos2unix, unzip, 
 * nainstalovat moduly pythonu3: zipfile, psycopg2, csv
 * připravit soubor se souřadnicemi zastávek:
   - pořadí sloupců: stop_id, stop_name, stop_desc, stop_lat, stop_lon, stop_url, location_type, parent_station
   - stop_lat a stop_lon s desetinnou tečkou
   - sloupce odděleny středníkem
   - kódováno v UTF-8
 * uložit soubor jako `data/bus_stops/bus_stops-utf.csv`
 * naklonovat do hlavního adresáře repozitář `gtfstools`:
   - `git clone https://github.com/xtompok/gtfstools`

## Použití
V ideálním případě zavoláme `make` a vše se provede automaticky a výstupní soubor typu GTFS je uložen do `output/gtfs-bus-out.zip`.

## Průběh připravy dat
Samotný `make` vykonává postupně tyto činnosti (definované v `Makefile`):
 * stažení a rozbalení JDF pomocí skriptu `download.sh`
 * převedení textových souborů do UTF-8 s unixovými konci řádků pomocí skriptu `to-utf.sh`
 * přípravu databáze
   - vytvoření tabulek (a případné smazání starých) podle `schema.sql`
   - import jízdních řádů pomocí skriptu `import-to-db`
   - import pozic autobusových zastávek pomocí skriptu import-stop-po
   - vytvoření pohledů reprezentujících jednotlivé soubory v GTFS podle `GTFS/views.sql`
 * vytvoření výstupního souboru GTFS
   - vytvoření adresáře `output`
   - export z databáze a úprava formátů pomocí skriptu `export.py`
   - pročištění nepoužívaných zastávek a dalších entit pomocí `postprocess.py`
   - zabalení výstupních souborů do souboru `gtfs-bus-out.zip` 


 

