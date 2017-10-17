# A thing to scrape GitHub for cool package.json and requirements.txt projects

To run psql:
```
pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
```

To run the program:
```
source ./localenv/bin/activate
make run
```

Config File:

```
{
    "github_api": {
        "pass": "password",
        "user": "github username"
    },
    "db": {
        "host": "127.0.0.1",
        "name": "database name",
        "password": "password here",
        "port": 5432,
        "user": "username"
    }
}
```
