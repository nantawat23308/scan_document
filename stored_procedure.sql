CREATE PROCEDURE nantawats.insert_data_json(IN json_data JSON)
begin
	DECLARE i INT DEFAULT 0;
    DECLARE total INT;

    SET total = JSON_LENGTH(json_data);

    WHILE i < total DO
        INSERT INTO scan_dir (absolute_path, file_name, file_type, file_encode, file_size, modified_time, file_permission, DIRorREGFILE, owner_uid, owner_gid, name_owner, md5)
        VALUES (
            JSON_UNQUOTE(JSON_EXTRACT(json_data, CONCAT('$[', i, '].absolute_path'))),
            NULLIF(JSON_UNQUOTE(JSON_EXTRACT(json_data, CONCAT('$[', i, '].file_name'))), 'NULL'),
            NULLIF(JSON_UNQUOTE(JSON_EXTRACT(json_data, CONCAT('$[', i, '].file_type'))), 'NULL'),
            NULLIF(JSON_UNQUOTE(JSON_EXTRACT(json_data, CONCAT('$[', i, '].file_encode'))), 'NULL'),
            NULLIF(JSON_UNQUOTE(JSON_EXTRACT(json_data, CONCAT('$[', i, '].file_size'))), 'NULL'),
            NULLIF(JSON_UNQUOTE(JSON_EXTRACT(json_data, CONCAT('$[', i, '].modified_time'))), 'NULL'),
            NULLIF(JSON_UNQUOTE(JSON_EXTRACT(json_data, CONCAT('$[', i, '].file_permission'))), 'NULL'),
            NULLIF(JSON_UNQUOTE(JSON_EXTRACT(json_data, CONCAT('$[', i, '].DIRorREGFILE'))), 'NULL'),
            NULLIF(JSON_UNQUOTE(JSON_EXTRACT(json_data, CONCAT('$[', i, '].owner_uid'))), 'NULL'),
            NULLIF(JSON_UNQUOTE(JSON_EXTRACT(json_data, CONCAT('$[', i, '].owner_gid'))), 'NULL'),
            NULLIF(JSON_UNQUOTE(JSON_EXTRACT(json_data, CONCAT('$[', i, '].name_owner'))), 'NULL'),
            NULLIF(JSON_UNQUOTE(JSON_EXTRACT(json_data, CONCAT('$[', i, '].md5'))), 'NULL')
        );
        SET i = i + 1;
    END WHILE;
END
