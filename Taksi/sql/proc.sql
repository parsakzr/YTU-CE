--Function 1, 2 (With Update)
CREATE FUNCTION set_car_status_false(lic_plt VARCHAR(10))
    RETURNS VOID AS $$ 
        BEGIN 
            UPDATE car
            SET is_available = FALSE
            WHERE license_plate = lic_plt;
        END;
    $$ LANGUAGE plpgsql;


CREATE FUNCTION set_car_status_true(lic_plt VARCHAR(10))
    RETURNS VOID AS $$ 
        BEGIN 
            UPDATE car
            SET is_available = TRUE
            WHERE license_plate = lic_plt;
        END;
    $$ LANGUAGE plpgsql;


--Function 3 (With Delete)
	CREATE FUNCTION delete_old_cars(lic_plt VARCHAR(10))
		RETURNS VOID AS $$ 
			BEGIN 
				DELETE FROM car
				WHERE prod_year < 2015;
			END;
		$$ LANGUAGE plpgsql;
		
		
--Trigger
	CREATE TRIGGER call_taxi
		AFTER INSERT
		ON trip
		FOR EACH ROW
			EXECUTE FUNCTION update_car_status(NEW.license_plate);
		
--Cursor
	CREATE OR REPLACE FUNCTION display_drivers(st_id VARCHAR(10))
		RETURNS void AS $$
			DECLARE
				drivers CURSOR FOR SELECT d_name, d_surname FROM driver WHERE st_id = station_id;
			BEGIN
				FOR I IN drivers LOOP
					RAISE INFO 'Sürücü: % %', I.d_name, I.d_surname;
				END LOOP;
			END;
		$$ LANGUAGE plpgsql;
	
--View
	CREATE VIEW kadikoy_taxi AS 
		SELECT s_name, car_model
		FROM car, station
		WHERE car_loc = 'Kadıköy' AND s_district = 'Kadıköy';
		

	
--Aggregate
	SELECT COUNT(car_model), car_loc, car_model, car_type, is_available
	FROM car
	GROUP BY car_loc, car_model, car_type, is_available;


	SELECT COUNT(d_name), d_name, d_surname, d_addr
	FROM driver
	GROUP BY d_name, d_surname, d_addr
	HAVING COUNT(d_addr) > 2;


    -- SELECT AVG(rating) 
    -- FROM driver, trip
    -- WHERE driver.d_id = trip.d_id
    -- WHERE rating IS NOT NULL;
	
--Intersect
	SELECT car_model, car_type, car_loc
	FROM car
	WHERE is_available = True
	INTERSECT
	SELECT car_model, car_type, car_loc
	FROM car 
	WHERE car_loc = 'Kadıköy' AND car_model = 'Egea';
	
--Type & Record
	CREATE TYPE trip_info AS (startloc VARCHAR(20), endloc VARCHAR(20), car_model VARCHAR(16), starttime TIME, endtime TIME, totalcost NUMERIC(5,2), rating NUMERIC(3,1));
	
	CREATE OR REPLACE FUNCTION display_trips(loc trip.start_loc%TYPE)
		RETURNS trip_info AS $$ 
			DECLARE
				ret_value trip_info;
			BEGIN 
				SELECT tr.start_loc, tr.end_loc, car.car_model, tr.start_time, tr.end_time, tr.total_cost, tr.rating INTO trip_info
				FROM trip tr, car
				WHERE tr.car_id = car.license_plate;
				RETURN trip_info;
			END;
		$$ LANGUAGE plpgsql;
		
	SELECT display_trips('Beşiktaş');
	
