CREATE PROCEDURE p_clean_tables(IN schema_name VARCHAR(32))
BEGIN
    DECLARE t_name VARCHAR(200);
    DECLARE v_not_found BOOL DEFAULT FALSE;

    DECLARE table_cursor CURSOR FOR SELECT table_name FROM information_schema.tables
        WHERE table_schema = schema_name
        -- Tables only; create Views with CREATE OR REPLACE
        AND table_type = 'BASE TABLE'
        AND table_name <> 'plan_table';

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_not_found := TRUE;
    SET FOREIGN_KEY_CHECKS = 0;
    OPEN table_cursor;

    t_cursor_loop: LOOP
        FETCH table_cursor INTO t_name;
        IF v_not_found THEN
            LEAVE t_cursor_loop;
        END IF;

        SET @sql_text := CONCAT('DROP TABLE ', t_name, ';');
        PREPARE stmt FROM @sql_text;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END LOOP;

    CLOSE table_cursor;
    SET FOREIGN_KEY_CHECKS = 1;
END;
