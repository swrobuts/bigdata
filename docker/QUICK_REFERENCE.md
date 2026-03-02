# Docker Labs - Quick Reference

## One-Liner Commands

```bash
# Start all labs
cd docker/ && ./start-lab.sh mongodb && sleep 30 && ./start-lab.sh duckdb && ./start-lab.sh neo4j && ./start-lab.sh spark

# Stop all
./start-lab.sh stop

# Check status
./start-lab.sh status
```

## Individual Lab Commands

### MongoDB
```bash
# Start
cd docker/mongodb && docker-compose up -d

# Access
mongosh mongodb://localhost:27017/megastore
# Or web: http://localhost:8081 (admin/pass)

# Stop
docker-compose down
```

### DuckDB
```bash
# Start
cd docker/duckdb && docker-compose up -d

# Get token
docker-compose logs duckdb | grep token

# Access
http://localhost:8888/?token=xxx

# Stop
docker-compose down
```

### Neo4j
```bash
# Start
cd docker/neo4j && docker-compose up -d

# Access
http://localhost:7474

# Stop
docker-compose down
```

### Spark
```bash
# Start
cd docker/spark && docker-compose up -d

# Get token
docker-compose logs spark | grep token

# Access
http://localhost:8888/?token=xxx
http://localhost:4040  # Spark UI (during execution)

# Stop
docker-compose down
```

## Common Tasks

### Check Container Status
```bash
# All Docker containers
docker ps

# Specific lab
cd docker/mongodb && docker-compose ps
```

### View Logs
```bash
# Real-time logs
docker-compose logs -f

# Last 50 lines
docker-compose logs --tail=50

# Just errors
docker-compose logs | grep error
```

### Execute Commands in Container
```bash
# MongoDB
docker exec -it megastore-mongodb mongosh

# DuckDB (Python REPL)
docker exec -it megastore-duckdb python3

# Neo4j (cypher-shell)
docker exec -it megastore-neo4j cypher-shell

# Spark (PySpark shell)
docker exec -it megastore-spark pyspark
```

### Free Up Resources
```bash
# Stop all containers
docker-compose down

# Remove all containers
docker system prune

# Remove all data volumes
docker volume prune

# Remove everything
docker system prune --volumes
```

## Database Queries

### MongoDB
```javascript
// In mongosh
use megastore
db.products.find().limit(5)
db.orders.countDocuments()
db.orders.aggregate([{ $group: { _id: "$customer_id", count: { $sum: 1 } } }])
```

### DuckDB (Python)
```python
import duckdb
con = duckdb.connect(':memory:')

con.execute("SELECT * FROM read_parquet('data/orders.parquet') LIMIT 5").show()
con.execute("SELECT COUNT(*) FROM read_csv_auto('data/products.csv')").show()

# Complex query
con.execute("""
    SELECT DATE(order_date), COUNT(*), SUM(total_amount)
    FROM read_parquet('data/orders.parquet')
    GROUP BY DATE(order_date)
""").df()
```

### Neo4j (Cypher)
```cypher
// In Browser at localhost:7474
MATCH (p:Product) RETURN p LIMIT 5;
MATCH (c:Category) RETURN count(c);
MATCH (p:Product)-[:BELONGS_TO]->(c:Category) RETURN p.name, c.name LIMIT 10;
```

### Spark (PySpark)
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("test").getOrCreate()

orders = spark.read.parquet("data/orders.parquet")
orders.show(5)
orders.groupBy("customer_id").count().show()

# Complex aggregation
orders.groupBy("customer_id").agg(
    count("order_id").alias("orders"),
    sum("total_amount").alias("total")
).show(10)
```

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose logs

# Check if port is in use
lsof -i :8888

# Start fresh
docker-compose down -v
docker-compose up -d
```

### Out of Memory
```bash
# Check usage
docker stats

# Stop other containers
docker-compose down

# Reduce memory in docker-compose.yml
# deploy.resources.limits.memory: 1G
```

### Connection Refused
```bash
# Verify container is running
docker ps | grep megastore-

# Wait for service to fully start
sleep 30

# Try again
mongosh localhost:27017
```

### Can't Find Data
```bash
# Verify data directory
ls -la data/megastore/

# Check mounts in container
docker exec megastore-mongodb ls -la /data/megastore/

# Verify relative paths in docker-compose.yml
grep "../data" mongodb/docker-compose.yml
```

## Port Reference

| Service | Port | URL |
|---------|------|-----|
| MongoDB | 27017 | mongodb://localhost:27017 |
| Mongo Express | 8081 | http://localhost:8081 |
| DuckDB Jupyter | 8888 | http://localhost:8888 |
| Neo4j Browser | 7474 | http://localhost:7474 |
| Neo4j Bolt | 7687 | bolt://localhost:7687 |
| Spark Jupyter | 8888 | http://localhost:8888 |
| Spark UI | 4040 | http://localhost:4040 |

**Note:** DuckDB and Spark both use port 8888 - run them separately!

## Environment Variables

### MongoDB
```bash
MONGO_INITDB_DATABASE=megastore
```

### DuckDB
```bash
JUPYTER_ENABLE_LAB=yes
```

### Neo4j
```bash
NEO4J_AUTH=none
NEO4J_server_memory_heap_initial__size=512m
NEO4J_server_memory_heap_max__size=512m
NEO4J_PLUGINS=["apoc"]
```

### Spark
```bash
SPARK_DRIVER_MEMORY=1g
SPARK_EXECUTOR_MEMORY=512m
SPARK_LOCAL_CORES=2
JUPYTER_ENABLE_LAB=yes
```

## File Locations in Containers

### MongoDB
- Data: `/data/db`
- Imports: `/data/megastore/`

### DuckDB
- Data: `/home/jovyan/data/`
- Notebooks: `/home/jovyan/notebooks/`

### Neo4j
- Data: `/var/lib/neo4j/data`
- Import: `/var/lib/neo4j/import/`

### Spark
- Data: `/home/jovyan/data/`
- Notebooks: `/home/jovyan/notebooks/`
- Output: `/home/jovyan/output/`

## Pro Tips

1. **Use Relative Paths:** Data mounting uses relative paths from `docker/` directory
2. **Check Health:** Use `docker-compose ps` to verify all services are healthy
3. **Stream Logs:** `docker-compose logs -f [service]` for real-time debugging
4. **Save Notebooks:** Jupyter notebooks persist in `duckdb/notebooks/` and `spark/notebooks/`
5. **Neo4j Import:** Copy commands from `neo4j/import/import-megastore.cypher` into browser
6. **Memory:** Watch `docker stats` if performance is slow
7. **Isolation:** Each lab is independent - modify configs without affecting others

## Useful Links

- Start Script Help: `./start-lab.sh help`
- Full Documentation: `README.md`
- Setup Summary: `SETUP_SUMMARY.md`
- MegaStore Data: `../data/megastore/`

---

*Last updated: March 2, 2026*
