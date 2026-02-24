#!/bin/bash

cd ../django
pushd .
cd /tmp

psql -d postgres -c "DROP DATABASE IF EXISTS $VAT_POSTGRES_DB";
psql -d postgres -c "CREATE DATABASE $VAT_POSTGRES_DB;"

psql -d postgres -c "DROP OWNED BY $VAT_POSTGRES_USER;"
psql -d postgres -c "DROP USER IF EXISTS $VAT_POSTGRES_USER"
psql -d postgres -c "CREATE USER $VAT_POSTGRES_USER WITH PASSWORD '${VAT_POSTGRES_PASS}'"

# set permissions
psql -d postgres -c  "GRANT ALL ON DATABASE $VAT_POSTGRES_DB TO $VAT_POSTGRES_USER;"
psql -d postgres -c  "GRANT ALL PRIVILEGES ON DATABASE $VAT_POSTGRES_DB TO $VAT_POSTGRES_USER;"
psql -d postgres -c  "ALTER DATABASE $VAT_POSTGRES_DB OWNER TO $VAT_POSTGRES_USER;"
psql -d postgres -c  "GRANT ALL ON SCHEMA PUBLIC TO $VAT_POSTGRES_USER;"
psql -d postgres -c  "GRANT SET ON PARAMETER session_replication_role TO $VAT_POSTGRES_USER;"
# needed for creating test databases
psql -d postgres -c  "ALTER USER $VAT_POSTGRES_USER CREATEDB;"

popd
source ../.venv/bin/activate
python manage.py migrate

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo "Database renewed successfully."
else
    echo "Failed to renew database."
fi
