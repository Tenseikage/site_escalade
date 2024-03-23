--- Projet sql escalade--------
--- Supression des tables existantes
DROP TABLE IF EXISTS voie CASCADE;
DROP TABLE IF EXISTS sortie CASCADE;
DROP TABLE IF EXISTS cordee CASCADE;
DROP TABLE IF EXISTS adherent CASCADE;
DROP TABLE IF EXISTS site_escalade CASCADE;
DROP TABLE IF EXISTS voie_suivante CASCADE;
DROP TABLE IF EXISTS type_voie CASCADE;
DROP TABLE IF EXISTS niveau CASCADE;
DROP TABLE IF EXISTS  exerce CASCADE;
DROP TABLE IF EXISTS  inscrit CASCADE;
DROP TABLE IF EXISTS  appartient CASCADE;
DROP TABLE IF EXISTS  voies_grimpes CASCADE;

/*DROP VIEW sites_plus_grimpes;
DROP VIEW sorties_manquantes_guides;*/


--- Creation des tables avec la mise en place des contraintes de cle etrangères-------------------------------CREATE TABLE site_escalade (
  CREATE TABLE site_escalade (
    id_site SERIAL PRIMARY KEY,
    nom_site VARCHAR(50) UNIQUE NOT NULL,
    localite VARCHAR(50)
);

CREATE TABLE niveau (
    nivFR VARCHAR(2) PRIMARY KEY,
    nivUS VARCHAR(10),
    nivGB VARCHAR(10)
);

CREATE TABLE type_voie (
    code SERIAL PRIMARY KEY,
    nom_type VARCHAR(50)
);

CREATE TABLE adherent (
    id_adherent SERIAL PRIMARY KEY,
    email VARCHAR(70) NOT NULL,
    mdp VARCHAR(80) NOT NULL,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    niv_grimpeur VARCHAR(2),
    niv_guide VARCHAR(2),
    FOREIGN KEY (niv_grimpeur) REFERENCES niveau(nivFR) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (niv_guide) REFERENCES niveau(nivFR) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE voie (
    id_voie SERIAL PRIMARY KEY,
    id_site INT,
    code_voie INT,
    nivFR VARCHAR(2),
    nom_voie VARCHAR(50) UNIQUE,
    longueur_voie INT NOT NULL,
    FOREIGN KEY (nivFR) REFERENCES niveau(nivFR) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(code_voie)  REFERENCES type_voie(code) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(id_site) REFERENCES site_escalade(id_site) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE sortie (
    id_sortie SERIAL PRIMARY KEY,
    organisateur SERIAL REFERENCES adherent(id_adherent),
    site_souhaite VARCHAR(40),
    court_description TEXT,
    date_sortie DATE,
    nivFR VARCHAR(2),
    maniere VARCHAR(40),
    FOREIGN KEY (nivFR) REFERENCES niveau(nivFR) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE voie_suivante (
    id_voie INT,
    autre_id_voie INT,
    FOREIGN KEY (id_voie) REFERENCES voie(id_voie) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (autre_id_voie) REFERENCES voie(id_voie) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id_voie, autre_id_voie)
);

CREATE TABLE cordee (
    id_cordee SERIAL PRIMARY KEY,
    nom_cordee VARCHAR(50) NOT NULL,
    participants INT
);

CREATE TABLE exerce (
    id_adherent INT,
    id_site INT,
    liste_localites TEXT NOT NULL,
    FOREIGN KEY (id_adherent)  REFERENCES adherent(id_adherent) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_site)  REFERENCES site_escalade(id_site) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id_adherent, id_site)
);

CREATE TABLE inscrit (
    id_adherent INT,
    id_sortie INT,
    FOREIGN KEY(id_adherent) REFERENCES adherent(id_adherent) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_sortie) REFERENCES sortie(id_sortie) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id_adherent, id_sortie)
);

CREATE TABLE appartient (
    id_adherent INT,
    id_cordee INT,
    FOREIGN KEY (id_adherent)  REFERENCES adherent(id_adherent) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_cordee)  REFERENCES cordee(id_cordee) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id_adherent, id_cordee)
);

CREATE TABLE voies_grimpes (
    id_cordee INT,
    id_voie INT,
    maniere TEXT NOT NULL,
    date_escalade DATE NOT NULL,
    FOREIGN KEY (id_cordee) REFERENCES cordee(id_cordee) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_voie) REFERENCES voie(id_voie) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id_cordee, id_voie, date_escalade)
);



--- Test de l'insertion de valeurs dans les tables

--- table site_escalade (Sites d'escalade vrais et fictifs)

INSERT INTO site_escalade (id_site,nom_site, localite) VALUES (DEFAULT,'Ablon','Haute-Savoie');
INSERT INTO site_escalade (id_site,nom_site, localite) VALUES (DEFAULT,'Arsine','Haute-Alpes');
INSERT INTO site_escalade (id_site,nom_site, localite) VALUES (DEFAULT,'Super-2000','Haute-Alpes');
INSERT INTO site_escalade (id_site,nom_site, localite) VALUES (DEFAULT,'Vallee-Sacree','Massif-Central');
INSERT INTO site_escalade (id_site,nom_site, localite) VALUES (DEFAULT,'Mont-Dore','Massif-Central');
INSERT INTO site_escalade (id_site,nom_site, localite) VALUES (DEFAULT,'Vallee-Enneigee','Pyrenees');
INSERT INTO site_escalade (id_site,nom_site, localite) VALUES (DEFAULT,'Pic-du-Midi','Pyrenees');
INSERT INTO site_escalade (id_site,nom_site, localite) VALUES (DEFAULT,'Mont-Rocailleux','Pyrenees');


--- table niveau --------------(niveaux d'escalades)
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('1','5.1','Easy');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('2','5.3','M');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('3','5.4','D');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('4','5.5','HVD');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('5a','5.6','MS');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('5b','5.7','VS');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('5c','5.8','HVS');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('6a','5.9','E1');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('6b','5.10c','E2');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('6c', '5.11a','E3');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('7a','5.11d','E4');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('7b','5.12b','E5');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('7c','5.12d','E6');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('8a','5.13b','E7');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('8b','5.13d','E8');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('8c','5.14b','E9');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('9a','5.14d','E10');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('9b','5.15b','E11');
INSERT INTO niveau (nivFR,nivUS,nivGB) VALUES ('9c','5.15d','E12');

--- table type_voie --- (Types de voies)

INSERT INTO type_voie(code,nom_type) VALUES (DEFAULT,'Falaise');
INSERT INTO type_voie(code,nom_type) VALUES (DEFAULT,'Bloc');


--- table voie---(Voies fictives)

INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'Voie penteuse', 225,'1',1,3);
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'La celeste', 421,'2',2,4); 
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'Cobelstone', 112,'3',1,2);
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'Vie pleine', 365,'4',1,1);
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'Belle montee', 254,'5a',2,2);
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, ' Voie verte', 478,'6b',2,3);
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'Voie volcanique', 654,'2',1,3);
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'L escalatrice', 411,'1',1,1);
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'Voie dormante', 552,'9c',1,2);
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'Voie eveillee', 552,'3',2,8);
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'Pierres en folie', 220,'4',1,8);
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'Voie simple', 440,'1',2,7); 
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'Voie Noire', 552,'3',2,5);
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'Voie Blanche', 777,'9a',1,5);
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'Voie Grise', 365,'4',2,7);
INSERT INTO voie (id_voie, nom_voie, longueur_voie,nivFR,code_voie,id_site) VALUES (DEFAULT, 'Balade fraiche', 275,'3',2,1);



--- table adherent ---(liste fictive d'adherents)









-- table voies_suivantes---(Voies qui se suivent)

INSERT INTO voie_suivante (id_voie,autre_id_voie) VALUES (1,6);
INSERT INTO voie_suivante (id_voie,autre_id_voie) VALUES (5,9);
INSERT INTO voie_suivante (id_voie,autre_id_voie) VALUES (9,3);
INSERT INTO voie_suivante (id_voie,autre_id_voie) VALUES (7,6);
INSERT INTO voie_suivante (id_voie,autre_id_voie) VALUES (4,8);
INSERT INTO voie_suivante (id_voie,autre_id_voie) VALUES (10,11);
INSERT INTO voie_suivante (id_voie,autre_id_voie) VALUES (14,13);


--- table adherent ---(liste fictive d'adhérents)


INSERT INTO adherent (email, mdp, nom, prenom,niv_grimpeur,niv_guide ) VALUES ('john.doe@email.com', '$2b$12$cSko4Ahh0s5AsHVkhdz6A.QnV2VxQCk7prbizX1QSVi3MG.oZby16', 'Doe', 'John' ,'3','2');
INSERT INTO adherent (email, mdp, nom, prenom,niv_grimpeur ) VALUES ('alice.smith@email.com', '$2b$12$/f1RILFGSwyceem9WkBfIObTW85gL7ZgtaR4ueR33EHXswdkLrZwO', 'Smith', 'Alice','3');
INSERT INTO adherent (email, mdp, nom, prenom,niv_grimpeur ) VALUES ('bob.jones@email.com', '$2b$12$4QIoHLof2EQ8nPxdOVlMIuM/NV1Sg42kzecfUZTDOFqCgNnb43xNu', 'Jones', 'Bob','3');
INSERT INTO adherent (email, mdp, nom, prenom, niv_grimpeur,niv_guide) VALUES ('laura.miller@email.com', '$2b$12$OuJfpPNUDLDOKp04KKAEeeO.60Vm2H2UV4GO4Gb3X3t3g6viGq5b.', 'Miller', 'Laura','4','3');
INSERT INTO adherent (email, mdp, nom, prenom,niv_grimpeur) VALUES ('emma.white@email.com', '$2b$12$0xU7KcQEb9FzonStZzgBMO3LccGtib8pf2aQ.YBSFtWM3YS7Xb16u', 'White', 'Emma','5a');
INSERT INTO adherent (email, mdp, nom, prenom, niv_grimpeur) VALUES ('michael.brown@email.com', '$2b$12$scr.US18Mgz4zqESGxJIoeuC0Vr3X6SAnbiYJgqfP7bKghOgHUX8C', 'Brown', 'Michael','3');
INSERT INTO adherent (email, mdp, nom, prenom,niv_grimpeur ) VALUES ('sophie.wilson@email.com', '$2b$12$kHWz.GQ1fQAQofKsyI5vDuKMCjoaELpgi1LYOwzLHmR3A5euwnu6C', 'Wilson', 'Sophie','3');
INSERT INTO adherent (email, mdp, nom, prenom, niv_grimpeur) VALUES ('kevin.jenkins@email.com', '$2b$12$PQiUcOx52PTVIX19H.vcseKPFHAFnR2kOnSEl.EXmN05AXUwu1Jz2', 'Jenkins', 'Kevin','5b');
INSERT INTO adherent (email, mdp, nom, prenom, niv_grimpeur) VALUES ('natalie.hall@email.com', '$2b$12$J/8METj37s2XwImpSGjTo.BKQkR3tqLFML.1DghFNn5Xt6OgAl5nm', 'Hall', 'Natalie','3');
INSERT INTO adherent (email, mdp, nom, prenom,niv_grimpeur) VALUES ('alex.clark@email.com', '$2b$12$VP0hJWWxDz7n6SBCpfGEK..qz0TuC2uDZrFKynZlyTpwIVQM0Vih2', 'Clark', 'Alex','3');


--- table sortie----(Sorties crees par les adherents)

INSERT INTO sortie (organisateur ,site_souhaite,court_description, date_sortie,nivFR,maniere) VALUES (3, 'Ablon','Escalade a Ablon', '2023-12-01','3','Traditionnelle');
INSERT INTO sortie (organisateur ,site_souhaite,court_description, date_sortie,nivFR,maniere) VALUES (6, 'Arsine','Les grimpeurs de nouveau a Arsine', '2024-11-20','3','Solo Intégral');
INSERT INTO sortie (organisateur ,site_souhaite,court_description, date_sortie,nivFR,maniere) VALUES (4, 'Super 2000','En route pour Super 2000 !', '2022-11-16','2','Traditionnelle');








INSERT INTO cordee (id_cordee,nom_cordee,participants) VALUES (DEFAULT,'Les aguerris',4);
INSERT INTO cordee (id_cordee,nom_cordee,participants) VALUES (DEFAULT,'Grimpeurs de L extrême',1);
INSERT INTO cordee (id_cordee,nom_cordee,participants) VALUES (DEFAULT,'L amicale des grimpeurs',1);
INSERT INTO cordee (id_cordee,nom_cordee,participants) VALUES (DEFAULT,'Escalade en douce',1);
INSERT INTO cordee (id_cordee,nom_cordee,participants) VALUES (DEFAULT,'Super escaladeurs',1);









INSERT INTO exerce(id_adherent,id_site,liste_localites) VALUES (4,2,'Ablon, Arsine');
INSERT INTO exerce(id_adherent,id_site,liste_localites) VALUES (1,3,'Super 2000,Arsine');


---- table inscrit ---(adherents inscrits dans une cordee)
INSERT INTO inscrit (id_adherent,id_sortie) VALUES (3,1);
INSERT INTO inscrit (id_adherent,id_sortie) VALUES (2,2);
INSERT INTO inscrit (id_adherent,id_sortie) VALUES (6,3);
INSERT INTO inscrit (id_adherent,id_sortie) VALUES (6,);
INSERT INTO inscrit (id_adherent,id_sortie) VALUES (2,1);
INSERT INTO inscrit (id_adherent,id_sortie) VALUES (6,1);
INSERT INTO inscrit (id_adherent,id_sortie) VALUES (7,1);





--- table appartient --- (creation d'une cordee fictive)
INSERT INTO appartient(id_adherent,id_cordee) VALUES (3,1);
INSERT INTO appartient(id_adherent,id_cordee) VALUES (2,1);
INSERT INTO appartient(id_adherent,id_cordee) VALUES (6,1);
INSERT INTO appartient(id_adherent,id_cordee) VALUES (7,1);


--- table voies_escaladees --- (Certaines cordees n'ont qu'un adherent,c'est juste pour tester les insertions)

INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (2,3, 'Escalade traditionnelle', '2023-12-13');
INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (1,3 ,'Escalade artificielle', '2024-01-10');
INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (1,3 ,'Solo integral', '2024-02-11');
INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (1,4 ,'Solo integral', '2024-11-20');
INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (1,3 ,'Escalade artificielle', '2024-05-11');
INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (1,3 ,'Escalade artificielle', '2024-05-17');
INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (5,7 ,'Solo integral', '2024-02-11');
INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (1,8 ,'Solo integral', '2024-03-11');
INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (3,3 ,'Escalade traditionnelle', '2024-02-11');
INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (1,3 ,'Solo integral', '2024-04-23');
INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (5,8 ,'Solo integral', '2024-02-11');
INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (5,4 ,'Solo integral', '2024-02-11');
INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (1, 13,'Escalade Traditionnelle', '2024-12-21');
INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (5,11 ,'Escalade Traditionnelle', '2024-03-11');
INSERT INTO voies_grimpes(id_cordee,id_voie,maniere,date_escalade) VALUES (4,7 ,'Escalade artificielle', '2024-02-11');































