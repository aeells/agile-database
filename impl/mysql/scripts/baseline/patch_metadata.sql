-- Copyright (c) 2011, Andrew Eells. All Rights Reserved.

CREATE TABLE patch_metadata (
    release_number          BIGINT        NOT NULL,
    patch_number            VARCHAR(255)  NOT NULL,
    script                  VARCHAR(255)  NOT NULL,
    patch_type              ENUM ('BASELINE', 'PATCH', 'ROLLBACK'),
    patch_timestamp         TIMESTAMP     NOT NULL,
    script_checksum         BIGINT        NOT NULL,
    PRIMARY KEY (patch_number, script, patch_type)
) ENGINE = InnoDB;

CREATE TABLE seq_patch_metadata (value INT NOT NULL) ENGINE = MYISAM;
INSERT INTO seq_patch_metadata values(1);
