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

CREATE TABLE pevnykod (
	cislo VARCHAR(5),
	znacka VARCHAR(1),
	rezerva VARCHAR(254)
);

CREATE TABLE dopravci (
	ICO VARCHAR(10) PRIMARY KEY,
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
	unk VARCHAR(5)
);

CREATE TABLE linky (
	cislo INT PRIMARY KEY,
	nazev VARCHAR(254),
	ICO VARCHAR(10),
	typ CHAR(1),
	rezerva VARCHAR(3),
	licence VARCHAR(48),
	licence_od VARCHAR(8),
	licence_do VARCHAR(8),
	unk3 VARCHAR(5),
	unk4 VARCHAR(5),
	unk5 VARCHAR(5),
	unk6 VARCHAR(5),
	jr_od VARCHAR(8),
	jr_do VARCHAR(8),
	unk1 VARCHAR(5),
	unk2 VARCHAR(5)
);

CREATE TABLE spoje (
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
	p_kod11 VARCHAR(5),
	unk VARCHAR(5)
);

CREATE TABLE zaslinky (
	linka INT,
	tarif_cis INT,
	rezerva VARCHAR(254),
	zastavka INT,
	p_kod1 VARCHAR(5),
	p_kod2 VARCHAR(5),
	p_kod3 VARCHAR(5),
	p_kod4 VARCHAR(5),
	unk VARCHAR(5)
);

CREATE TABLE zasspoje (
	linka INT,
	spoj INT,
	tarif_cis INT,
	zastavka INT,
	stanoviste VARCHAR(48),
	p_kod1 VARCHAR(5),
	p_kod2 VARCHAR(5),
	p_kod3 VARCHAR(5),
	km VARCHAR(6),
	prijezd VARCHAR(5),
	odjezd VARCHAR(5),
	unk VARCHAR(5)
);

CREATE TABLE udaje (
	linka INT,
	udaj INT,
	text VARCHAR(254),
	unk VARCHAR(5)
);

CREATE TABLE caskody (
	linka INT,
	spoj INT,
	cas_kod INT,
	cas_kod_ozn CHAR(2),
	cas_kod_typ CHAR(1),
	datum_od CHAR(8),
	datum_do CHAR(8),
	poznamka VARCHAR(254),
	unk VARCHAR(5)
);

CREATE TABLE altdop (
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
	unk1 VARCHAR(5),
	unk2 VARCHAR(5)
);

CREATE TABLE altlinky (
	linka INT,
	alt_linka VARCHAR(20),
	stat VARCHAR(3)
);

CREATE TABLE mistenky (
	linka INT,
	spoj INT,
	text VARCHAR(254),
	unk VARCHAR(5)
);
