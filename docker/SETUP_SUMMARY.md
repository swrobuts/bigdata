# Docker Labs Setup Summary

## Files Created

All files have been successfully created in:
`/sessions/determined-trusting-fermi/mnt/Sommersemester_2026/BBA/SP_BigData/bigdata-lab/docker/`

### Directory Structure
```
docker/
├── README.md                           # Main documentation
├── SETUP_SUMMARY.md                    # This file
├── start-lab.sh                        # Master startup script (executable)
│
├── mongodb/
│   ├── docker-compose.yml              # MongoDB + Mongo Express
│   └── init/
│       └── init-megastore.sh           # Auto-import script
│
├── duckdb/
│   ├── Dockerfile                      # Build image from Jupyter base
│   ├── docker-compose.yml              # DuckDB service
│   ├── .dockerignore                   # Exclude files from image
│   └── notebooks/
│       └── megastore_duckdb_intro.py   # Starter script
│
├── neo4j/
│   ├── docker-compose.yml              # Neo4j graph database
│   └── import/
│       └── import-megastore.cypher     # Cypher import scripts
│
└── spark/
    ├── Dockerfile                      # Build image from PySpark base
    ├── docker-compose.yml              # Spark service
    ├── .dockerignore                   # Exclude files from image
    └── notebooks/
        └── megastore_spark_intro.py    # Starter script
```

## Quick Start Commands

```bash
# Navigate to docker directory
cd docker/

# Start individual labs
./start-lab.sh mongodb      # MongoDB Lab
./start-lab.sh duckdb       # DuckDB Lab
./start-lab.sh neo4j        # Neo4j Lab
./start-lab.sh spark        # Spark Lab

# Management commands
./start-lab.sh status       # Show which labs are running
./start-lab.sh stop         # Stop all labs
./start-lab.sh restart-all  # Restart all labs
./start-lab.sh help         # Show help menu
```

## Lab Access Points

### MongoDB Lab
- **Data:** `mongodb://localhost:27017/megastore`
- **Web UI:** http://localhost:8081
- **CLI:** `docker exec -it megastore-mongodb mongosh`
- **Credentials:** admin / pass (Mongo Express UI only)

### DuckDB Lab
- **Jupyter:** http://localhost:8888
- **Token:** Check logs with `docker-compose logs duckdb | grep token`
- **Data location:** `/home/jovyan/data/`
- **Starter:** `/home/jovyan/notebooks/megastore_duckdb_intro.py`

### Neo4j Lab
- **Browser:** http://localhost:7474
- **Bolt:** `bolt://localhost:7687`
- **Auth:** None (disabled for learning)
- **Import scripts:** `neo4j/import/import-megastore.cypher`

### Spark Lab
- **Jupyter:** http://localhost:8888
- **Spark UI:** http://localhost:4040
- **Token:** Check logs with `docker-compose logs spark | grep token`
- **Data location:** `/home/jovyan/data/`
- **Starter:** `/home/jovyan/notebooks/megastore_spark_intro.py`

## Data Mounting

All labs mount read-only access to the MegaStore data:
- **Source:** `data/megastore/` (relative to docker/ directory)
- **Files included:**
  - CSV: products.csv, customers.csv, orders.csv, order_items.csv, clickstream.csv
  - JSON: products.json, customers.json, orders_sample.json, reviews.json, categories.json, suppliers.json
  - Parquet: orders.parquet, order_items.parquet, clickstream.parquet
  - Relationships: product_relationships.csv, customer_relationships.csv

## Resource Limits

| Lab       | Memory | Startup Time | Running Ports |
|-----------|--------|--------------|---------------|
| MongoDB   | 512MB  | 30s          | 27017, 8081   |
| DuckDB    | 1GB    | 15s          | 8888          |
| Neo4j     | 768MB  | 30s          | 7474, 7687    |
| Spark     | 1.5GB  | 60s          | 8888, 4040    |

## Key Features

✓ **Independent**: Each lab runs standalone (no dependencies)
✓ **Lightweight**: Optimized for student laptops
✓ **Persistent**: Data persists across restarts
✓ **Isolated**: Network isolation between labs
✓ **Auto-initialization**: Data loads automatically
✓ **Health checks**: Container readiness monitoring
✓ **Clear logging**: Helpful console output

## Important Notes

1. **Memory Management**: All labs run on single containers. Don't run all 4 simultaneously if your laptop has < 8GB RAM.

2. **First Run**: Initial builds (DuckDB, Spark) take 1-2 minutes. Subsequent runs are much faster.

3. **Data Import**:
   - MongoDB: Automatic via init script
   - DuckDB: Automatic (in-memory or file)
   - Neo4j: Manual (copy Cypher commands into browser)
   - Spark: Automatic (read-only mount)

4. **Relative Paths**: All data paths use relative paths from `docker/` directory:
   ```
   ../data/megastore/  → /sessions/.../bigdata-lab/data/megastore/
   ```

5. **Port Conflicts**: If ports are already in use, edit the docker-compose.yml files to change port mappings.

## Verification

To verify all files were created correctly:

```bash
# Check structure
ls -la docker/

# Verify each subdirectory
ls -la docker/mongodb/
ls -la docker/duckdb/
ls -la docker/neo4j/
ls -la docker/spark/

# Check startup script
file docker/start-lab.sh  # Should show "executable"

# List all Docker files
find docker/ -type f | sort
```

Expected output: 15 files total
- 1 README.md
- 1 SETUP_SUMMARY.md (this file)
- 1 start-lab.sh
- 4 docker-compose.yml files
- 2 Dockerfile files
- 4 .dockerignore files
- 2 starter Python scripts
- 1 init shell script
- 1 Cypher import script

## Troubleshooting

**Nothing starts:**
```bash
# Check Docker is running
docker ps

# Check docker-compose is installed
docker-compose version

# Check file permissions
ls -la docker/start-lab.sh
# Should show: -rwx------ or similar (executable)
```

**Ports already in use:**
```bash
# Find what's using the port
lsof -i :8888

# Kill the process or change port in docker-compose.yml
```

**Can't access data:**
```bash
# Verify data directory exists
ls -la data/megastore/

# Verify paths in docker-compose.yml use relative paths
# Should be: ../data/megastore
# Not: /full/path/to/data
```

## Next Steps

1. Read `README.md` for detailed documentation
2. Run `./start-lab.sh help` for command help
3. Start with `./start-lab.sh mongodb` to test setup
4. Follow lab-specific guides in README.md
5. Explore MegaStore data in each platform

## Support

- **Docker Docs:** https://docs.docker.com/
- **Docker Compose Docs:** https://docs.docker.com/compose/
- **Lab-specific docs:** See README.md

---

**Created:** March 2, 2026
**For:** BigData Lab - Sommersemester 2026
**Dataset:** MegaStore (sample e-commerce data)
