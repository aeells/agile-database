#!/bin/sh

DB_USER=$1
DB_PASS=$2
DB_HOST=$3
DB_DATABASE=$4

if [ $# -ne 4 ]
then
    echo "Usage: sh $0 <DB_USER> <DB_PASS> <DB_HOST> <DB_DATABASE>"
    exit 1
fi

MYSQL_CONNECT="/usr/local/mysql/bin/mysql -u${DB_USER} -p${DB_PASS} -h${DB_HOST} ${DB_DATABASE}"
SCRIPTS_DIR=`pwd`/infrastructure/src/main/resources/scripts

# updates sequence number even if no patches i.e. we don't care if not contiguous
${MYSQL_CONNECT} -e "UPDATE seq_patch_metadata SET value = value + 1"
RELEASE_NUMBER=`${MYSQL_CONNECT} --skip-column-names -e "SELECT value FROM seq_patch_metadata"`

for PATCH_NUMBER in `find infrastructure/src/main/resources/scripts/patches/**/install.txt | cut -f7 -d/ | sort -n`;
do
    for PATCH_SCRIPT in `tail infrastructure/src/main/resources/scripts/patches/${PATCH_NUMBER}/install.txt`;
    do
        # Check that rollback has not already been executed.
        ROLLBACK_APPLIED=`${MYSQL_CONNECT} -e "
            SELECT COUNT(*) FROM patch_metadata
                WHERE patch_number = '${PATCH_NUMBER}'
                AND script = '${PATCH_SCRIPT}'
                AND patch_type IN ('ROLLBACK');"`

        # Check that patch has not already been executed.
        PATCH_APPLIED=`${MYSQL_CONNECT} -e "
            SELECT COUNT(*) FROM patch_metadata
                WHERE patch_number = '${PATCH_NUMBER}'
                AND script = '${PATCH_SCRIPT}'
                AND patch_type IN ('PATCH', 'BASELINE');"`

        SCRIPT_CHECKSUM=`cksum ${SCRIPTS_DIR}/patches/${PATCH_NUMBER}/patch/${PATCH_SCRIPT} | awk '{print $1}'`

        if [ ${ROLLBACK_APPLIED//[^0-9]/} = "1" ];
        then
            echo "  * Applying patch ${PATCH_NUMBER} ${PATCH_SCRIPT}"

            EXECUTION_OUTPUT=`${MYSQL_CONNECT} < ${SCRIPTS_DIR}/patches/${PATCH_NUMBER}/patch/${PATCH_SCRIPT} 2>&1`;

            if [[ "$EXECUTION_OUTPUT" =~ 'ERROR' ]];
            then
                echo "Execution of patch script ${PATCH_SCRIPT} failed with error: ${EXECUTION_OUTPUT}";
            else
                ${MYSQL_CONNECT} -e "
                UPDATE patch_metadata SET release_number = $RELEASE_NUMBER, patch_type = 'PATCH', patch_timestamp = NOW(), script_checksum = $SCRIPT_CHECKSUM
                    WHERE patch_number = '${PATCH_NUMBER}'
                    AND script = '${PATCH_SCRIPT}';
                COMMIT;"
            fi

        elif [ ${PATCH_APPLIED//[^0-9]/} = "0" ];
        then
            echo "  * Applying patch ${PATCH_NUMBER} ${PATCH_SCRIPT}"

            EXECUTION_OUTPUT=`${MYSQL_CONNECT} < ${SCRIPTS_DIR}/patches/${PATCH_NUMBER}/patch/${PATCH_SCRIPT} 2>&1`;

            if [[ "$EXECUTION_OUTPUT" =~ 'ERROR' ]];
            then
                echo "Execution of patch script ${PATCH_SCRIPT} failed with error: ${EXECUTION_OUTPUT}"
            else
                ${MYSQL_CONNECT} -e "
                INSERT INTO patch_metadata (release_number, patch_number, script, patch_type, patch_timestamp, script_checksum)
                    VALUES($RELEASE_NUMBER, '${PATCH_NUMBER}', '${PATCH_SCRIPT}', 'PATCH', NOW(), $SCRIPT_CHECKSUM);
                COMMIT;"
            fi
        fi
    done
done
