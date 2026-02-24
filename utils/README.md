# dbutils.sh
This script can reset a local database. Never do this in production.

## Setup


Your need to set this. The first variables are what you want to set for the db you want to interact with. And the second part are variables for connection to postgres
```bash
export VAT_POSTGRES_DB=vat
export VAT_POSTGRES_USER=naoth
export VAT_POSTGRES_PASS=<password>
export VAT_POSTGRES_HOST=localhost
export VAT_POSTGRES_PORT=4000

export PGHOST="127.0.0.1"
export PGPORT="4000"
export PGUSER="naoth"
export PGPASSWORD=<password>
```

Run postgres instance locally with docker.
```bash
docker run --name local-postgres17 \
-e POSTGRES_PASSWORD=$VAT_POSTGRES_PASS \
-e POSTGRES_USER=$VAT_POSTGRES_USER \
-e POSTGRES_DB=$VAT_POSTGRES_DB \
-e POSTGRES_HOST_AUTH_METHOD=trust \
-p 4000:5432 \
-v pgdata:/var/lib/postgresql/data \
-d postgres:17
```
```


```bash
./db_reset.sh
```
