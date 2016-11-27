DROP TABLE IF EXISTS zastavky CASCADE;
CREATE TABLE zastavky (
	id SERIAL PRIMARY KEY,
	route INT,
	cislo INT,
	obec VARCHAR(48),
	cast_o VARCHAR(48),
	misto VARCHAR(48),
	blizko VARCHAR(3),
	stat VARCHAR(3),
	p_kod1 VARCHAR(5),
	p_kod2 VARCHAR(5),
	p_kod3 VARCHAR(5),
	p_kod4 VARCHAR(5),
	p_kod5 VARCHAR(5),
	p_kod6 VARCHAR(5)
);

DROP TABLE IF EXISTS pevnykod CASCADE;
CREATE TABLE pevnykod (
	route INT,
	cislo VARCHAR(5),
	znacka VARCHAR(1),
	rezerva VARCHAR(254)
);

DROP TABLE IF EXISTS dopravci CASCADE;
CREATE TABLE dopravci (
	id SERIAL PRIMARY KEY,
	route INT,
	ICO VARCHAR(10),
	DIC VARCHAR(14),
	jmeno VARCHAR(254),
	druh INT,
	jmeno_os VARCHAR(254),
	adresa VARCHAR(254),
	tel_sidlo VARCHAR(48),
	tel_disp VARCHAR(48),
	tel_info VARCHAR(48),
	fax VARCHAR(48),
	email VARCHAR(48),
	www VARCHAR(48),
	rozl_dop VARCHAR(5)
);

--DROP TABLE IF EXISTS linky CASCADE;
--CREATE TABLE linky (
--	cislo INT PRIMARY KEY,
--	nazev VARCHAR(254),
--	ICO VARCHAR(10),
--	typ CHAR(1),
--	rezerva VARCHAR(3),
--	licence VARCHAR(48),
--	licence_od VARCHAR(8),
--	licence_do VARCHAR(8),
--	unk3 VARCHAR(5),
--	unk4 VARCHAR(5),
--	unk5 VARCHAR(5),
--	unk6 VARCHAR(5),
--	jr_od VARCHAR(8),
--	jr_do VARCHAR(8),
--	unk1 VARCHAR(5),
--	unk2 VARCHAR(5)
--);
DROP TABLE IF EXISTS linky CASCADE;
CREATE TABLE linky (
	id SERIAL PRIMARY KEY,
	route INT,
	cislo INT,
	nazev VARCHAR(254),
	ICO VARCHAR(10),
	typ CHAR(1),
	prostredek VARCHAR(1),
	vyluka BOOLEAN,
	seskupeni BOOLEAN,
	oznacnik BOOLEAN,
	jednosmer BOOLEAN,
	rezerva VARCHAR(5),
	licence VARCHAR(48),
	licence_od VARCHAR(8),
	licence_do VARCHAR(8),
	jr_od VARCHAR(8),
	jr_do VARCHAR(8),
	rozl_dop INT,
	rozl_linky INT
);

DROP TABLE IF EXISTS spoje CASCADE;
CREATE TABLE spoje (
	id SERIAL PRIMARY KEY,
	route INT,
	linka INT,
	spoj INT,
	p_kod1 VARCHAR(5),
	p_kod2 VARCHAR(5),
	p_kod3 VARCHAR(5),
	p_kod4 VARCHAR(5),
	p_kod5 VARCHAR(5),
	p_kod6 VARCHAR(5),
	p_kod7 VARCHAR(5),
	p_kod8 VARCHAR(5),
	p_kod9 VARCHAR(5),
	p_kod10 VARCHAR(5),
	skupina INT,
	rozl_linky INT
);

DROP TABLE IF EXISTS zaslinky CASCADE;
CREATE TABLE zaslinky (
	id SERIAL PRIMARY KEY,
	route INT,
	linka INT,
	tarif_cis INT,
	tarif_pasmo VARCHAR(50),
	zastavka INT,
	avg_doba VARCHAR(5),
	p_kod1 VARCHAR(5),
	p_kod2 VARCHAR(5),
	p_kod3 VARCHAR(5),
	rozl_linky INT
);

DROP TABLE IF EXISTS zasspoje CASCADE;
CREATE TABLE zasspoje (
	id SERIAL PRIMARY KEY,
	route INT,
	linka INT,
	spoj INT,
	tarif_cis INT,
	zastavka INT,
	kod_oznacniku INT,
	stanoviste VARCHAR(48),
	p_kod1 VARCHAR(5),
	p_kod2 VARCHAR(5),
	p_kod3 VARCHAR(5),
	km INT,
	prijezd VARCHAR(5),
	odjezd VARCHAR(5),
	prij_min VARCHAR(5),
	odj_max VARCHAR(5),
	rozl_linky INT
);

DROP TABLE IF EXISTS udaje CASCADE;
CREATE TABLE udaje (
	id SERIAL PRIMARY KEY,
	route INT,
	linka INT,
	udaj INT,
	text VARCHAR(254),
	rozl_linky INT
);


DROP TABLE IF EXISTS caskody CASCADE;
CREATE TABLE caskody (
	id SERIAL PRIMARY KEY,
	route INT,
	linka INT,
	spoj INT,
	cas_kod INT,
	cas_kod_ozn CHAR(2),
	cas_kod_typ CHAR(1),
	datum_od CHAR(8),
	datum_do CHAR(8),
	poznamka VARCHAR(254),
	rozl_linky INT
);

DROP TABLE IF EXISTS altdop CASCADE;
CREATE TABLE altdop (
	id SERIAL PRIMARY KEY,
	route INT,
	linka INT,
	spoj INT,
	ICO VARCHAR(10),
	p_kod1 VARCHAR(5),
	p_kod2 VARCHAR(5),
	p_kod3 VARCHAR(5),
	p_kod4 VARCHAR(5),
	p_kod5 VARCHAR(5),
	p_kod6 VARCHAR(5),
	cas_kod_typ CHAR(1),
	rezerva VARCHAR(254),
	datum_od VARCHAR(8),
	datum_do VARCHAR(8),
	rozl_dop INT,
	rozl_linky INT
);

DROP TABLE IF EXISTS altlinky CASCADE;
CREATE TABLE altlinky (
	id SERIAL PRIMARY KEY,
	route INT,
	linka INT,
	alt_linka VARCHAR(20),
	stat VARCHAR(3),
	rozl_linky INT
);

DROP TABLE IF EXISTS mistenky CASCADE;
CREATE TABLE mistenky (
	id SERIAL PRIMARY KEY,
	route INT,
	linka INT,
	spoj INT,
	text VARCHAR(254),
	rozl_linky INT
);

DROP TABLE IF EXISTS zas_pozice CASCADE;
CREATE TABLE zas_pozice (
	stop_id INT,
	stop_name VARCHAR(100),
	stop_desc VARCHAR(100),
	stop_lat DOUBLE PRECISION,
	stop_lon DOUBLE PRECISION,
	stop_url VARCHAR(100),
	location_t VARCHAR(1),
	parent_sta VARCHAR(10)
);


