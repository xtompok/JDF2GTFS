CREATE OR REPLACE FUNCTION rpref(INT,INT) 
RETURNS VARCHAR(50) 
AS '
BEGIN
	RETURN CONCAT($1,''-'',$2);
END
' LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION rpref(INT,INT,INT) 
RETURNS VARCHAR(50)
AS '
BEGIN
	RETURN CONCAT($1,''-'',$2,''-'',$3);
END
' LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION rpref(INT,INT,INT,INT) 
RETURNS VARCHAR(50)
AS '
BEGIN
	RETURN CONCAT($1,''-'',$2,''-'',$3,''-'',$4);
END
' LANGUAGE 'plpgsql';

DROP VIEW IF EXISTS agency;
CREATE VIEW agency AS
SELECT rpref(route,ICO::INT,rozl_dop::INT) AS agency_id,
	jmeno AS agency_name,
	www AS agency_url,
	'Europe/Prague'::VARCHAR(30) AS agency_timezone,
	tel_info AS agnecy_phone
FROM dopravci;

DROP VIEW IF EXISTS stops;
CREATE VIEW stops AS
SELECT rpref(route,cislo) AS stop_id,
	CONCAT(obec,',',cast_o,',',misto) AS stop_name,
	stop_lat,
	stop_lon
FROM zastavky AS z 
LEFT OUTER JOIN zas_pozice AS zp ON zp.stop_name = CONCAT(obec,',',cast_o,',',misto);


DROP VIEW IF EXISTS routes;
CREATE VIEW routes AS
SELECT rpref(route,cislo,rozl_linky) AS route_id,
	rpref(route,ICO::INT,rozl_dop::INT) AS agency_id,
	cislo AS route_short_name,
	nazev AS route_long_name,
	prostredek AS route_type
FROM linky;

DROP VIEW IF EXISTS trips;
CREATE VIEW trips AS
SELECT rpref(s.route,s.linka,s.rozl_linky) AS route_id,
	rpref(s.route,c.cas_kod) AS service_id,
	rpref(s.route,s.linka,s.rozl_linky,s.spoj) AS trip_id
FROM spoje AS s INNER JOIN caskody AS c ON
	rpref(s.route,s.linka,s.rozl_linky,s.spoj) = rpref(c.route,c.linka,c.rozl_linky,c.spoj);
		
DROP VIEW IF EXISTS stop_times;
CREATE VIEW stop_times AS
SELECT rpref(route,linka,rozl_linky,spoj) AS trip_id,
	prijezd AS arrival_time,
	odjezd AS departure_time,
	zastavka AS stop_id,
	tarif_cis AS stop_sequence,
	km AS shape_dist_traveled
FROM zasspoje;

DROP VIEW IF EXISTS calendar;
CREATE VIEW calendar AS
SELECT rpref(s.route,s.linka,s.rozl_linky,s.spoj) AS service_id,
	s.p_kod1,s.p_kod2,s.p_kod3,s.p_kod4,s.p_kod5,s.p_kod6,s.p_kod7,s.p_kod8,s.p_kod9,
	l.jr_od,l.jr_do
FROM spoje AS s INNER JOIN linky AS l ON rpref(s.route,s.linka,s.rozl_linky) = rpref(l.route,l.cislo,l.rozl_linky);

DROP VIEW IF EXISTS calendar_dates;
CREATE VIEW calendar_dates AS
SELECT rpref(s.route,s.linka,s.rozl_linky,s.spoj) AS service_id,
	ck.datum_od,
	ck.datum_do,
	ck.cas_kod_typ AS exception_type
FROM spoje AS s INNER JOIN caskody AS ck ON rpref(s.route,s.linka,s.rozl_linky,s.spoj) = rpref(ck.route,ck.linka,ck.rozl_linky,ck.spoj);




