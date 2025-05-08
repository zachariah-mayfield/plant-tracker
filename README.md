# plant-tracker
plant-tracker Application

# Run the Stack
### From the plant-tracker/ directory:
```bash
docker-compose up -d
```

### To rebuild after changes:
```bash
docker-compose up -d --build
```

### To view Logs
```bash
docker-compose logs -f
```

### To stop and remove containers:
```bash
docker-compose down
```

### run a backup from the host like this:
```bash
docker exec -t plant-tracker-db pg_dump -U postgres plantdb > ./pg_backups/plantdb_backup.sql
```

### To restore a backup:
```bash
cat ./pg_backups/plantdb_backup.sql | docker exec -i plant-tracker-db psql -U postgres -d plantdb
```

### Test DB connection:
### Open browser:
http://localhost:8000/db-check
