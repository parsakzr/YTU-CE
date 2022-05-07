DROP TABLE IF EXISTS trip;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS driver;
DROP TABLE IF EXISTS station;
DROP TABLE IF EXISTS car;

CREATE TABLE car (
	license_plate VARCHAR(10) PRIMARY KEY,
	car_type VARCHAR(8),
    car_model VARCHAR(16),
	prod_year NUMERIC(4),
	engine_spec VARCHAR(10),
	car_loc VARCHAR(10),
	base_rate NUMERIC(5),
    is_available BOOLEAN DEFAULT TRUE
);

CREATE TABLE station (
	s_id VARCHAR(10) PRIMARY KEY,
	s_name VARCHAR(20) NOT NULL,
	s_addr VARCHAR(20),
	s_district VARCHAR(20),
	s_neighborhood VARCHAR(20),
	s_mgr_id VARCHAR(10), -- #TODO: implement + foreign key
	num_of_cars NUMERIC(3)
);

CREATE TABLE driver (
	d_id VARCHAR(10) PRIMARY KEY,
	d_name VARCHAR(12) NOT NULL,
	d_surname VARCHAR(18) NOT NULL,
	car_id VARCHAR(10),
	station_id VARCHAR(10),
	start_date DATE,
	earnings NUMERIC(5),
	avg_rating NUMERIC(3,1),
	d_addr VARCHAR(20),
	FOREIGN KEY (station_id) REFERENCES station (s_id) ON DELETE CASCADE,
	FOREIGN KEY (car_id) REFERENCES car (license_plate) ON DELETE CASCADE
);

CREATE TABLE trip (
	t_id VARCHAR(10) PRIMARY KEY,
	d_id VARCHAR(10),
	car_id VARCHAR(10),
	start_loc VARCHAR(20),
	end_loc VARCHAR(20),
	start_time TIME,
	end_time TIME,
	total_cost NUMERIC(5,2),
	rating NUMERIC(3,1),
	FOREIGN KEY (d_id) REFERENCES driver (d_id) ON DELETE CASCADE,
	FOREIGN KEY (car_id) REFERENCES car (license_plate) ON DELETE CASCADE
);

CREATE TABLE customer (
	c_id VARCHAR(10) PRIMARY KEY,
	c_name VARCHAR(20),
	c_surname VARCHAR(20),
	gender CHAR(1),
	c_addr VARCHAR(20),
	c_district VARCHAR(20),
	reg_date DATE
);

CREATE TABLE credentials (
    username VARCHAR (16) PRIMARY KEY,
    password VARCHAR (64), -- hashed password
    user_type VARCHAR (10), -- customer, manager
    user_id VARCHAR (10) -- d_id, c_id, m_id
);