CREATE OR REPLACE FUNCTION rpref(INT,INT) 
RETURNS VARCHAR(50) 
AS '
BEGIN
	RETURN CONCAT($1,''-'',$2);
END
' LANGUAGE 'plpgsql' IMMUTABLE;

CREATE OR REPLACE FUNCTION rpref(INT,INT,INT) 
RETURNS VARCHAR(50)
AS '
BEGIN
	RETURN CONCAT($1,''-'',$2,''-'',$3);
END
' LANGUAGE 'plpgsql' IMMUTABLE;

CREATE OR REPLACE FUNCTION rpref(INT,INT,INT,INT) 
RETURNS VARCHAR(50)
AS '
BEGIN
	RETURN CONCAT($1,''-'',$2,''-'',$3,''-'',$4);
END
' LANGUAGE 'plpgsql' IMMUTABLE;

CREATE INDEX ON pevnykod(route);
CREATE INDEX ON pevnykod(cislo);
CREATE OR REPLACE FUNCTION p_kod_znak(CHAR(5),INT)
RETURNS CHAR(1)
AS 'SELECT znacka FROM pevnykod WHERE route = $2 AND cislo = $1; '
LANGUAGE 'sql' IMMUTABLE;

CREATE INDEX ON dopravci(rpref(route,ICO::INT,rozl_dop::INT));

DROP VIEW IF EXISTS agency;
CREATE VIEW agency AS
SELECT rpref(route,ICO::INT,rozl_dop::INT) AS agency_id,
	jmeno AS agency_name,
	www AS agency_url,
	'Europe/Prague'::VARCHAR(30) AS agency_timezone,
	tel_info AS agency_phone
FROM dopravci;



DROP VIEW IF EXISTS stops;
CREATE VIEW stops AS
SELECT DISTINCT(rpref(route,cislo)) AS stop_id,
	CONCAT(obec,',',cast_o,',',misto) AS stop_name,
	stop_lat,
	stop_lon
FROM zastavky AS z 
LEFT OUTER JOIN zas_pozice AS zp ON zp.stop_name = CONCAT(obec,',',cast_o,',',misto);


CREATE INDEX ON linky(rpref(route,cislo,rozl_linky));
CREATE INDEX ON linky(rpref(route,ICO::INT,rozl_dop));
CREATE INDEX ON linky(cislo);

DROP VIEW IF EXISTS routes;
CREATE VIEW routes AS
SELECT rpref(route,cislo,rozl_linky) AS route_id,
	rpref(route,ICO::INT,rozl_dop::INT) AS agency_id,
	cislo AS route_short_name,
	nazev AS route_long_name,
	prostredek AS route_type
FROM linky;
--WHERE cislo::INT < 200000;

CREATE INDEX ON spoje(rpref(route,linka,rozl_linky));
CREATE INDEX ON spoje(rpref(route,linka,rozl_linky,spoj));

DROP VIEW IF EXISTS trips;
CREATE VIEW trips AS
SELECT rpref(s.route,s.linka,s.rozl_linky) AS route_id,
	rpref(s.route,s.linka,s.rozl_linky,s.spoj) AS service_id,
	rpref(s.route,s.linka,s.rozl_linky,s.spoj) AS trip_id
FROM spoje AS s;
--WHERE s.linka::INT < 200000; --INNER JOIN caskody AS c ON
--	rpref(s.route,s.linka,s.rozl_linky,s.spoj) = rpref(c.route,c.linka,c.rozl_linky,c.spoj);
		
CREATE INDEX ON zasspoje(rpref(route,linka,rozl_linky,spoj));
CREATE INDEX ON zasspoje(linka);

DROP VIEW IF EXISTS stop_times;
CREATE VIEW stop_times AS
SELECT rpref(route,linka,rozl_linky,spoj) AS trip_id,
	prijezd AS arrival_time,
	odjezd AS departure_time,
	rpref(route,zastavka) AS stop_id,
	tarif_cis AS stop_sequence,
	km AS shape_dist_traveled,
	p_kod1,
	p_kod2,
	p_kod3,
	spoj
FROM zasspoje
WHERE odjezd NOT IN ('<','|');
--AND linka::INT < 200000;

CREATE INDEX ON caskody(rpref(route,linka,rozl_linky));

DROP VIEW IF EXISTS calendar;
CREATE VIEW calendar AS
SELECT rpref(s.route,s.linka,s.rozl_linky,s.spoj) AS service_id,
	p_kod_znak(s.p_kod1,s.route) AS p_kod1, p_kod_znak(s.p_kod2,s.route) AS p_kod2, p_kod_znak(s.p_kod3,s.route) AS p_kod3,
	p_kod_znak(s.p_kod4,s.route) AS p_kod4, p_kod_znak(s.p_kod5,s.route) AS p_kod5, p_kod_znak(s.p_kod6,s.route) AS p_kod6,
	p_kod_znak(s.p_kod7,s.route) AS p_kod7, p_kod_znak(s.p_kod8,s.route) AS p_kod8, p_kod_znak(s.p_kod9,s.route) AS p_kod9,
	l.jr_od AS start_date,l.jr_do AS end_date
FROM spoje AS s INNER JOIN linky AS l ON rpref(s.route,s.linka,s.rozl_linky) = rpref(l.route,l.cislo,l.rozl_linky);
--WHERE s.linka::INT < 200000;

CREATE INDEX ON caskody(rpref(route,linka,rozl_linky,spoj));

DROP VIEW IF EXISTS calendar_dates;
CREATE VIEW calendar_dates AS
SELECT rpref(s.route,s.linka,s.rozl_linky,s.spoj) AS service_id,
	ck.datum_od,
	ck.datum_do,
	ck.cas_kod_typ AS exception_type
FROM spoje AS s INNER JOIN caskody AS ck ON rpref(s.route,s.linka,s.rozl_linky,s.spoj) = rpref(ck.route,ck.linka,ck.rozl_linky,ck.spoj);
--WHERE s.linka::INT < 200000;




