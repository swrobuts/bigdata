# BigData Lab - Docker Setup Guide

Complete Docker environments for four cutting-edge big data technologies. Each lab is independently containerized and optimized for student laptops.

**Table of Contents:**
- [Quick Start](#quick-start)
- [Lab Overview](#lab-overview)
- [Detailed Instructions](#detailed-instructions)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)

---

## Quick Start

### Prerequisites
- Docker Desktop (or Docker Engine) installed
- Docker Compose installed
- ~4GB free disk space
- 2+ CPU cores, 4GB+ RAM recommended

### Start All Labs
```bash
# Navigate to docker directory
cd docker/

# Start a specific lab
./start-lab.sh mongodb    # MongoDB + Mongo Express
./start-lab.sh duckdb     # DuckDB analytics engine
./start-lab.sh neo4j      # Neo4j graph database
./start-lab.sh spark      # PySpark distributed processing

# Stop all labs
./start-lab.sh stop

# Check status
./start-lab.sh status
```

### Manual Docker Commands
If you prefer not to use the start script:

```bash
# Start MongoDB lab
cd mongodb/
docker-compose up -d

# Start DuckDB lab
cd duckdb/
docker-compose up -d

# Start Neo4j lab
cd neo4j/
docker-compose up -d

# Start Spark lab
cd spark/
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

---

## Lab Overview

### 1. MongoDB Lab
**Type:** Document Database (NoSQL)
**Use Case:** Flexible data storage, product catalog, customer profiles

#### Access
- **Database:** `mongodb://localhost:27017`
- **Mongo Express UI:** http://localhost:8081
- **Credentials:** admin / pass

#### Quick Tasks
```bash
# Connect with mongosh
docker exec -it megastore-mongodb mongosh

# Query example
db.megastore.products.find().limit(5)
db.megastore.customers.countDocuments()
db.megastore.orders.aggregate([
  { $group: { _id: "$customer_id", total: { $sum: "$total_amount" } } }
])
```

#### What's Included
- MongoDB 7 Community Edition
- Mongo Express web UI for visual management
- Pre-loaded MegaStore data collections:
  - `products` - Product catalog
  - `customers` - Customer profiles
  - `orders` - Order history
  - `reviews` - Product reviews
  - `categories` - Product categories
  - `suppliers` - Supplier information

#### Resources
- 512MB memory limit
- Persistent volume storage
- Auto-indexes on key fields

---

### 2. DuckDB Lab
**Type:** In-Process OLAP Database
**Use Case:** Fast analytical queries, SQL analytics without server setup

#### Access
- **Jupyter Notebook:** http://localhost:8888
- **Look for token in logs:** `docker-compose logs duckdb`

#### Quick Tasks
```python
import duckdb

# Connect and query
con = duckdb.connect(':memory:')
result = con.execute("SELECT * FROM read_csv_auto('data/products.csv') LIMIT 5").fetchall()

# Read Parquet files (faster for analytics)
con.execute("SELECT COUNT(*) FROM read_parquet('data/orders.parquet')").show()

# Join multiple sources
con.execute("""
  SELECT
    DATE(o.order_date) as date,
    COUNT(*) as orders,
    SUM(o.total_amount) as revenue
  FROM read_parquet('data/orders.parquet') o
  GROUP BY DATE(o.order_date)
""").show()
```

#### What's Included
- Jupyter minimal notebook environment
- DuckDB 1.0 SQL analytics engine
- Data science stack: pandas, matplotlib, seaborn
- Pre-loaded MegaStore data:
  - CSV files: products, customers, orders, order_items, clickstream
  - Parquet files: orders, order_items, clickstream (faster)

#### Resources
- 1GB memory limit
- Interactive SQL queries
- Starter notebook: `megastore_duckdb_intro.py`

---

### 3. Neo4j Lab
**Type:** Graph Database
**Use Case:** Relationship analysis, recommendations, network analysis

#### Access
- **Neo4j Browser:** http://localhost:7474
- **Bolt Protocol:** `bolt://localhost:7687` (for apps)
- **Auth:** None (disabled for learning)

#### Quick Tasks
```cypher
// Browser queries - run in Neo4j Browser at localhost:7474

// Find all products
MATCH (p:Product) RETURN p LIMIT 10;

// Find products by category
MATCH (p:Product)-[:BELONGS_TO]->(c:Category)
WHERE c.name = "Electronics"
RETURN p.name, p.price;

// Find product relationships
MATCH (p1:Product)-[r:RELATED_TO]-(p2:Product)
RETURN p1.name, r.type, p2.name;

// Find customer network
MATCH (c1:Customer)-[r:CONNECTED_TO]-(c2:Customer)
RETURN c1.name, r.type, c2.name;

// Supply chain analysis
MATCH (p:Product)-[:SUPPLIED_BY]->(s:Supplier)
RETURN p.name, s.name, s.country;
```

#### What's Included
- Neo4j 5 Community Edition
- APOC library for advanced operations
- Data import scripts in Cypher format
- Node types: Product, Customer, Category, Supplier
- Relationships: BELONGS_TO, SUPPLIED_BY, RELATED_TO, CONNECTED_TO

#### Resources
- 512MB heap memory, 256MB page cache
- Browser UI with query editor
- Import scripts: `neo4j/import/import-megastore.cypher`

#### Data Import
To import data:
1. Open Neo4j Browser: http://localhost:7474
2. Copy commands from `neo4j/import/import-megastore.cypher`
3. Paste into query editor and execute (Ctrl+Enter)

---

### 4. Spark Lab
**Type:** Distributed Processing Engine
**Use Case:** Big data analytics, machine learning, distributed computing

#### Access
- **Jupyter Notebook:** http://localhost:8888
- **Spark UI:** http://localhost:4040
- **Look for token:** `docker-compose logs spark`

#### Quick Tasks
```python
# In Jupyter notebook
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("MegaStore").getOrCreate()

# Load data
orders = spark.read.parquet("data/orders.parquet")
products = spark.read.csv("data/products.csv", header=True)

# Explore
orders.show(5)
orders.describe('total_amount').show()

# Analytics
orders.groupBy("customer_id").agg(
    count("order_id").alias("order_count"),
    sum("total_amount").alias("total_spent")
).orderBy("total_spent").show()

# Join tables
orders.join(products, on="product_id").show()
```

#### What's Included
- PySpark (Python Spark API)
- Jupyter Lab environment
- ML libraries: scikit-learn
- Visualization: matplotlib, seaborn, plotly
- Pre-loaded MegaStore data (Parquet optimized)

#### Resources
- 1GB driver memory, 512MB executor memory
- Spark UI at localhost:4040 for job monitoring
- Starter notebook: `megastore_spark_intro.py`

---

## Detailed Instructions

### MongoDB Lab Setup

```bash
cd docker/mongodb/

# Start the lab
docker-compose up -d

# Wait for initialization (15-30 seconds)
docker-compose logs -f mongodb | grep -i "initialization complete"

# Access Mongo Express
# Browser: http://localhost:8081
# Username: admin
# Password: pass

# Connect with CLI
docker exec -it megastore-mongodb mongosh megastore

# Example queries
db.products.countDocuments()
db.orders.find({ "customer_id": "CUST001" })
db.orders.aggregate([
  { $group: { _id: "$customer_id", count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 10 }
])

# Stop the lab
docker-compose down
```

### DuckDB Lab Setup

```bash
cd docker/duckdb/

# Build and start
docker-compose up -d

# Wait for Jupyter to start (10-15 seconds)
docker-compose logs duckdb | grep -i "token="

# Copy the token URL and open in browser
# Format: http://localhost:8888/?token=abc123def456

# In Jupyter, create a new Python notebook and run:

import duckdb
con = duckdb.connect(':memory:')

# Query CSV
con.execute("SELECT * FROM read_csv('data/products.csv') LIMIT 5").show()

# Query Parquet (faster)
con.execute("SELECT COUNT(*) FROM read_parquet('data/orders.parquet')").show()

# Complex analysis
con.execute("""
  SELECT
    DATE(order_date) as date,
    COUNT(*) as orders,
    SUM(total_amount) as revenue
  FROM read_parquet('data/orders.parquet')
  GROUP BY DATE(order_date)
  ORDER BY date DESC
  LIMIT 10
""").df()  # Returns Pandas DataFrame

# Stop the lab
docker-compose down
```

### Neo4j Lab Setup

```bash
cd docker/neo4j/

# Start the lab
docker-compose up -d

# Wait for Neo4j to fully start (20-30 seconds)
docker-compose logs neo4j | grep -i "started"

# Open Neo4j Browser
# URL: http://localhost:7474
# Authentication: None (disabled)

# In the Browser query editor, run import scripts:
# Copy from: neo4j/import/import-megastore.cypher

# Example: Create products
LOAD CSV WITH HEADERS FROM 'file:///products.csv' AS row
CREATE (p:Product {
    product_id: row.product_id,
    name: row.product_name,
    price: toFloat(row.price)
});

# Query the graph
MATCH (p:Product) RETURN p LIMIT 5;

# Stop the lab
docker-compose down
```

### Spark Lab Setup

```bash
cd docker/spark/

# Build and start (first run takes 1-2 minutes)
docker-compose up -d

# Wait for Jupyter
docker-compose logs spark | grep -i "token="

# Open Jupyter
# Format: http://localhost:8888/?token=abc123def456

# In Jupyter, create Python notebook:

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("MegaStore").getOrCreate()

# Load data
orders = spark.read.parquet("data/orders.parquet")
customers = spark.read.csv("data/customers.csv", header=True, inferSchema=True)

# Show schema
orders.printSchema()

# Analyze
orders.groupBy("customer_id").agg(
    count("order_id").alias("orders"),
    sum("total_amount").alias("spent")
).show(10)

# Monitor in Spark UI: http://localhost:4040

# Stop the lab
docker-compose down
```

---

## Troubleshooting

### General Issues

**Port already in use**
```bash
# Find process using port (e.g., 8888)
lsof -i :8888

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml
# Change "8888:8888" to "8889:8888"
```

**Container won't start**
```bash
# Check logs for errors
docker-compose logs mongodb  # or duckdb, neo4j, spark

# Remove container and try again
docker-compose down -v  # -v removes volumes too
docker-compose up -d
```

**Out of memory**
```bash
# Check current usage
docker stats

# Stop other containers to free memory
docker-compose down

# Adjust memory limits in docker-compose.yml
# deploy.resources.limits.memory
```

### MongoDB Issues

**Data not loading**
```bash
# Check init script logs
docker-compose logs mongodb | grep -i "importing\|error"

# Re-import manually
docker exec megastore-mongodb mongoimport \
  --db megastore \
  --collection products \
  --file /data/megastore/products.json \
  --jsonArray
```

**Connection refused**
```bash
# Make sure MongoDB is fully initialized
docker-compose logs mongodb | grep "initialized"

# Wait another 10 seconds and retry
```

### Jupyter Labs Issues (DuckDB, Spark)

**Can't find data files**
```bash
# Check volume mounts
docker exec megastore-duckdb ls -la /home/jovyan/data/

# Verify relative paths from docker/ directory
ls -la data/megastore/
```

**Out of memory in Jupyter**
```bash
# Reduce data load or filter first
# Instead of: df = spark.read.parquet("data/orders.parquet")
# Use: df = spark.read.parquet("data/orders.parquet").limit(10000)
```

**Token not found in logs**
```bash
# Retrieve token manually
docker exec megastore-duckdb jupyter notebook list

# Or restart with explicit logging
docker-compose logs -f duckdb | grep -i "token"
```

### Neo4j Issues

**Can't access browser**
```bash
# Check if Neo4j is ready
docker-compose logs neo4j | grep -i "started\|ready"

# Wait 30 seconds after container starts
# Then try http://localhost:7474
```

**Import scripts not working**
```bash
# Verify data files are readable
docker exec megastore-neo4j ls -la /var/lib/neo4j/import/

# Check file permissions
docker exec megastore-neo4j ls -la /var/lib/neo4j/import/products.csv
```

### Spark UI Not Available

**Spark UI at localhost:4040 not loading**
```bash
# Spark UI only appears during job execution
# Run a query in Jupyter first, then access http://localhost:4040

# Or check logs
docker-compose logs spark | grep -i "listening"
```

---

## Architecture

### Data Flow
```
┌─────────────────────────────────────────────────────────┐
│          data/megastore/ (MegaStore Dataset)            │
│  CSV, JSON, Parquet files (readonly mount to all labs)  │
└────────────┬────────────┬────────────┬─────────────────┘
             │            │            │
    ┌────────▼────┐  ┌────▼─────┐  ┌─▼───────┐
    │  MongoDB    │  │ DuckDB   │  │ Neo4j   │
    │  Lab        │  │ Lab      │  │ Lab     │
    │             │  │          │  │         │
    │ :27017      │  │ :8888    │  │ :7474   │
    │ :8081 (UI)  │  │          │  │ :7687   │
    └─────────────┘  └──────────┘  └─────────┘

    ┌───────────────────────────┐
    │  Spark Lab                │
    │  :8888 (Jupyter)          │
    │  :4040 (Spark UI)         │
    └───────────────────────────┘
```

### Resource Usage (Approximate)

| Lab       | CPU  | Memory | Disk  | Status |
|-----------|------|--------|-------|--------|
| MongoDB   | 0.5  | 512MB  | 500MB | Startup: 30s |
| DuckDB    | 1.0  | 1GB    | 1GB   | Startup: 15s |
| Neo4j     | 0.5  | 768MB  | 1GB   | Startup: 30s |
| Spark     | 1.5  | 1.5GB  | 1.5GB | Startup: 60s |
| **Total** | 3.5  | 3.5GB  | 4GB   | All running |

### Data Volume Mounts

All labs mount data in read-only mode:
```
../data/megastore/ -> /data/megastore (MongoDB)
                   -> /home/jovyan/data (DuckDB)
                   -> /var/lib/neo4j/import (Neo4j)
                   -> /home/jovyan/data (Spark)
```

### Network Architecture

Each lab runs in its own Docker container with:
- Independent network (bridge mode)
- Isolated data storage
- Port mappings to localhost
- No inter-lab dependencies

---

## Advanced Usage

### Running Specific Containers

```bash
# Start only MongoDB
cd mongodb/
docker-compose up -d

# Start only DuckDB
cd duckdb/
docker-compose up -d
```

### Persisting Jupyter Notebooks

Notebooks are saved in `duckdb/notebooks/` and `spark/notebooks/` which are mounted in containers.

```bash
# Notebooks persist between restarts
docker-compose down
docker-compose up -d
# Your notebooks are still there!
```

### Custom Configuration

Edit docker-compose files to adjust:
- Memory limits: `deploy.resources.limits.memory`
- Ports: `ports: ["8889:8888"]` (map to different port)
- Data paths: `../data/megastore:/custom/path`

### Building Images Manually

```bash
# DuckDB
cd docker/duckdb/
docker build -t megastore-duckdb:latest .
docker run -p 8888:8888 -v ${PWD}/../data/megastore:/home/jovyan/data megastore-duckdb:latest

# Spark
cd docker/spark/
docker build -t megastore-spark:latest .
docker run -p 8888:8888 -p 4040:4040 -v ${PWD}/../data/megastore:/home/jovyan/data megastore-spark:latest
```

### Docker Debugging

```bash
# View all containers
docker ps -a

# View logs
docker-compose logs -f [service-name]

# Execute commands in container
docker exec -it megastore-mongodb mongosh

# Monitor resource usage
docker stats

# Clean up everything
docker-compose down -v  # removes containers, networks, volumes
```

---

## Support & Learning Resources

### MongoDB
- https://docs.mongodb.com/
- Mongo Express: Visual database manager included
- mongosh: Command-line tool for queries

### DuckDB
- https://duckdb.org/docs/
- SQLite-like but for analytics (OLAP)
- Excellent for CSV/Parquet processing

### Neo4j
- https://neo4j.com/docs/
- Graph database query language: Cypher
- APOC library: Advanced operations

### Apache Spark
- https://spark.apache.org/docs/latest/
- PySpark: Python API for Spark
- MLlib: Machine learning library

---

## Next Steps

1. **Explore each lab** with the starter notebooks/scripts
2. **Load your own data** by adding files to `data/megastore/`
3. **Connect labs** - export data from one, import to another
4. **Build analytics** - create dashboards and reports
5. **Scale up** - these configs scale to distributed clusters

---

*Created for BigData Lab - Sommersemester 2026*
*MegaStore Dataset*
