CREATE VIEW agency AS
SELECT ICO AS agency_id,
	jmeno AS agency_name,
	www AS agency_url,
	"Europe/Prague" AS agency_timezone,
	tel_info AS agnecy_phone
FROM JDF.dopravci;

CREATE VIEW stops AS
SELECT cislo AS stop_id,
	CONCAT_WS(',',obec,cast_o,misto) AS stop_name,
	49.0 AS stop_lat,
	15.0 AS stop_lon
FROM JDF.zastavky;

CREATE VIEW routes AS
SELECT cislo AS route_id,
	ICO AS agency_id,
	cislo AS route_short_name,
	nazev AS route_long_name,
	3 AS route_type
FROM linky;

CREATE VIEW trips AS
SELECT linka AS route_id,
	0 AS service_id,
	CONCAT_WS("_",linka,spoj) AS trip_id
FROM spoje;
	
CREATE VIEW stop_times AS
SELECT CONCAT_WS("_",linka,spoj) AS trip_id,
	prijezd AS arrival_time,
	odjezd AS departure_time,
	zastavka AS stop_id,
	tarif_cis AS stop_sequence,
	km AS shape_dist_traveled
FROM zasspoje;

CREATE TABLE calendar (
	service_id INT,
	monday INT,
	tuesday INT,
	wednesday INT,
	thursday INT,
	friday INT,
	saturday INT,
	sunday INT,
	start_date CHAR(8),
	end_date CHAR(8)
);

INSERT INTO calendar VALUES (0,1,1,1,1,1,1,1,20131213,20141213);

