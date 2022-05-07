-- CARS
INSERT INTO car VALUES('34T1221', 'Sedan', 'Corolla', 2019, '1.6 Dizel', 'Maltepe', 7);
INSERT INTO car VALUES('34T5412', 'Sedan', 'Focus', 2015, '1.6 Dizel', 'Besiktas', 7);
INSERT INTO car VALUES('34T7845', 'Sedan', 'Passat', 2020, '2.0 Petrol', 'Kadikoy', 12);
INSERT INTO car VALUES('34BAT45', 'Coupe', 'Batmobil', 2021, '4.0 Petrol', 'Sariyer', 90);
INSERT INTO car VALUES('34TA329', 'Sedan', 'Egea', 2019, '1.6 Dizel', 'Besiktas', 5);
INSERT INTO car VALUES('34TE567', 'Sedan', 'E220d', 2017, '2.0 Dizel', 'Esenler', 15);
INSERT INTO car VALUES('34TE873', 'Sedan', 'Linea', 2012, '1.6 Dizel', 'Esenler', 5);
INSERT INTO car VALUES('34TR679', 'SUV', 'TOGG', 2023, 'Elektrikli', 'Uskudar', 12);
INSERT INTO car VALUES('34TS666', 'Coupe', 'Viper ACR', 2019, '8.3 Petrol', 'Sariyer', 50);
INSERT INTO car VALUES('34TT319', 'Ticari', 'Doblo', 2014, '1.6 Dizel', 'Bakirköy', 8);

-- STATIONS
INSERT INTO station VALUES ('S178713409', 'Beşiktaş', '', 'Beşiktaş', '', 'MGR1173298',  20);
INSERT INTO station VALUES ('S170409409', 'Akasya', '', 'Kadıköy', '', 'MGR1184298',  12);
INSERT INTO station VALUES ('S170437509', 'Çiçek', '', 'Kadıköy', '', 'MGR1171254',  14);
INSERT INTO station VALUES ('S179766429', 'Mevlana', '', 'Esenyurt', '', 'MGR119046',  18); 


-- DRIVER
INSERT INTO driver VALUES ('D164083894', 'Mahmut', 'Ünlü', '34T1221', 'S178713409',  '2021-09-09', 6950, 7.1, 'Şişli');
INSERT INTO driver VALUES ('D164358948', 'Murat', 'Karayel', '34T5412', 'S170409409',  '2021-06-12', 8200, 6.2, 'Kadıköy');
INSERT INTO driver VALUES ('D164746664', 'Ömer', 'Kökcür', '34TA329', 'S170437509',  '2021-03-09', 6500, 8.3, 'Üsküdar');
INSERT INTO driver VALUES ('D160943750', 'Erman', 'Yaşar', '34TE873', 'S179766429',  '2021-05-11', 7980, 8.1, 'Beylikdüzü');

-- CUSTOMERS
INSERT INTO customer VALUES ('C198929081', 'Mehmet', 'Kaya', 'M', '', 'Beşiktaş', '2021-01-03');
INSERT INTO customer VALUES ('C190389093', 'Tuğçe', 'Ünal', 'F', '', 'Kadıköy', '2021-04-18');
INSERT INTO customer VALUES ('C194832734', 'Kaan', 'Kural', 'M', '', 'Kadıköy', '2021-07-11');
INSERT INTO customer VALUES ('C193827420', 'Parsa', 'Kazerooni', 'M', '', 'Esenyurt', '2021-06-11');

-- TRIP
INSERT INTO trip VALUES ('T204083894', 'D164083894', '34T5412', 'Kadıköy', 'Ataşehir', '19:08',  '19:52', 37, 8.0);
INSERT INTO trip VALUES ('T204358948', 'D164358948', '34TA329', 'Üsküdar', 'Kadıköy', '17:43',  '18:16', 25, 8.3);
INSERT INTO trip VALUES ('T204746664', 'D164746664', '34TE873', 'Beylikdüzü', 'Bakırköy', '15:38',  '16:24', 62, 9.0);
INSERT INTO trip VALUES ('T200943750', 'D160943750', '34T1221', 'Beşiktaş', 'Beyoğlu', '02:24',  '02:37', 19, 8.5);