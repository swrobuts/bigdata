"""
PySpark MegaStore Analytics Introduction
========================================

PySpark provides a Python API to Apache Spark, enabling distributed data processing
at scale. This notebook demonstrates key concepts with the MegaStore dataset.

To run in Jupyter:
1. Create a new Python notebook cell
2. Copy the code below into cells
3. Run each cell with Shift+Enter
"""

# ============================================================================
# 1. INITIALIZE SPARK
# ============================================================================
print("Initializing PySpark...")

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import pandas as pd

# Create Spark session
spark = SparkSession.builder \
    .appName("MegaStore Analytics") \
    .config("spark.sql.shuffle.partitions", "2") \
    .config("spark.default.parallelism", "2") \
    .getOrCreate()

# Set log level for cleaner output
spark.sparkContext.setLogLevel("WARN")

print(f"Spark Version: {spark.version}")
print(f"App Name: {spark.sparkContext.appName}")
print("Spark initialized successfully!")

# ============================================================================
# 2. LOAD DATA
# ============================================================================
print("\n" + "="*60)
print("LOADING MEGASTORE DATA")
print("="*60)

# Load orders from Parquet (columnar format, optimized for analytics)
print("\nLoading orders.parquet...")
orders_df = spark.read.parquet("data/orders.parquet")
print(f"Orders shape: {orders_df.count()} rows, {len(orders_df.columns)} columns")

# Load order items
print("Loading order_items.parquet...")
order_items_df = spark.read.parquet("data/order_items.parquet")
print(f"Order items shape: {order_items_df.count()} rows")

# Load clickstream data
print("Loading clickstream.parquet...")
clickstream_df = spark.read.parquet("data/clickstream.parquet")
print(f"Clickstream shape: {clickstream_df.count()} rows")

# Load CSV data
print("Loading products.csv...")
products_df = spark.read.csv("data/products.csv", header=True, inferSchema=True)
print(f"Products shape: {products_df.count()} rows")

print("Loading customers.csv...")
customers_df = spark.read.csv("data/customers.csv", header=True, inferSchema=True)
print(f"Customers shape: {customers_df.count()} rows")

# ============================================================================
# 3. EXPLORE DATA SCHEMAS
# ============================================================================
print("\n" + "="*60)
print("DATA SCHEMAS")
print("="*60)

print("\nOrders schema:")
orders_df.printSchema()

print("\nOrder items schema:")
order_items_df.printSchema()

print("\nProducts schema:")
products_df.printSchema()

# ============================================================================
# 4. BASIC DATA EXPLORATION
# ============================================================================
print("\n" + "="*60)
print("BASIC DATA EXPLORATION")
print("="*60)

print("\nSample orders (first 5 rows):")
orders_df.show(5)

print("\nSample products (first 3 rows):")
products_df.show(3)

# Summary statistics
print("\nOrder statistics:")
orders_df.describe('total_amount').show()

# ============================================================================
# 5. AGGREGATIONS
# ============================================================================
print("\n" + "="*60)
print("AGGREGATION QUERIES")
print("="*60)

# Total orders and revenue
summary = orders_df.agg(
    count("order_id").alias("total_orders"),
    sum("total_amount").alias("total_revenue"),
    avg("total_amount").alias("avg_order_value"),
    max("total_amount").alias("max_order_value"),
    min("total_amount").alias("min_order_value")
)
print("\nOrder Summary:")
summary.show()

# ============================================================================
# 6. GROUP BY ANALYSIS
# ============================================================================
print("\n" + "="*60)
print("GROUP BY ANALYSIS")
print("="*60)

# Orders per customer
print("\nTop 10 customers by number of orders:")
top_customers = orders_df.groupBy("customer_id") \
    .agg(
        count("order_id").alias("order_count"),
        sum("total_amount").alias("total_spent")
    ) \
    .orderBy(desc("total_spent")) \
    .limit(10)
top_customers.show()

# ============================================================================
# 7. JOINS
# ============================================================================
print("\n" + "="*60)
print("JOINS - COMBINING DATAFRAMES")
print("="*60)

# Join orders with order items
print("\nJoining orders with order items...")
orders_with_items = orders_df.join(
    order_items_df,
    on="order_id",
    how="left"
)

print("Sample joined data:")
orders_with_items.select("order_id", "quantity", "unit_price").show(5)

# ============================================================================
# 8. TIME-BASED ANALYSIS
# ============================================================================
print("\n" + "="*60)
print("TIME-BASED ANALYSIS")
print("="*60)

# Daily order count
print("\nDaily order counts:")
daily_orders = orders_df \
    .withColumn("order_date", to_date(col("order_date"))) \
    .groupBy("order_date") \
    .agg(
        count("order_id").alias("order_count"),
        sum("total_amount").alias("daily_revenue")
    ) \
    .orderBy(desc("order_date"))

daily_orders.show(10)

# ============================================================================
# 9. WINDOW FUNCTIONS (ADVANCED)
# ============================================================================
print("\n" + "="*60)
print("WINDOW FUNCTIONS - ADVANCED ANALYTICS")
print("="*60)

from pyspark.sql.window import Window

# Running total of orders per customer
print("\nRunning total per customer (first 10):")
window_spec = Window.partitionBy("customer_id").orderBy("order_date")

customer_running_total = orders_df \
    .withColumn(
        "running_total",
        sum("total_amount").over(window_spec)
    ) \
    .select("order_id", "customer_id", "order_date", "total_amount", "running_total") \
    .limit(10)

customer_running_total.show()

# ============================================================================
# 10. CONVERTING TO PANDAS FOR VISUALIZATION
# ============================================================================
print("\n" + "="*60)
print("CONVERTING TO PANDAS FOR VISUALIZATION")
print("="*60)

# Convert Spark DataFrame to Pandas (for small results)
print("\nConverting daily orders to Pandas DataFrame...")
daily_orders_pandas = daily_orders.toPandas()
print(f"Pandas shape: {daily_orders_pandas.shape}")
print(daily_orders_pandas.head())

# ============================================================================
# 11. CACHING AND PERFORMANCE
# ============================================================================
print("\n" + "="*60)
print("PERFORMANCE TIPS")
print("="*60)

print("""
1. CACHING:
   - Use df.cache() to cache frequently used DataFrames
   - Use df.unpersist() to remove from cache

2. PARTITIONING:
   - Repartition for parallel processing: df.repartition(4)
   - Write partitioned data for faster reads

3. FORMAT SELECTION:
   - Use Parquet for analytics (columnar, compressed)
   - Use CSV for interoperability

4. QUERY OPTIMIZATION:
   - Use predicates pushdown: filter data early
   - Use select() to choose only needed columns
   - Avoid shuffles when possible

5. SINGLE-NODE VS CLUSTER:
   - This setup runs on a single node (laptop)
   - Increase parallelism in cluster environments
   - Monitor resource usage at localhost:4040 (Spark UI)
""")

# ============================================================================
# 12. SPARK UI AND DEBUGGING
# ============================================================================
print("\n" + "="*60)
print("SPARK UI AND DEBUGGING")
print("="*60)

print("""
Access the Spark UI at: http://localhost:4040

The Spark UI shows:
- Stages: Processing stages of your job
- Tasks: Individual tasks across executors
- Storage: Cached DataFrames
- Executors: Node information and memory usage
- SQL: Detailed SQL query execution plans
""")

# ============================================================================
# 13. NEXT STEPS
# ============================================================================
print("\n" + "="*60)
print("LEARNING PATHS")
print("="*60)

print("""
BEGINNER:
1. Load different data formats (CSV, Parquet, JSON)
2. Practice basic SQL: SELECT, WHERE, GROUP BY
3. Create simple joins between tables

INTERMEDIATE:
1. Use window functions for ranking and trends
2. Create custom columns with transformations
3. Analyze patterns in the clickstream data
4. Perform product performance analysis

ADVANCED:
1. Machine learning: predict customer behavior
2. Graph analysis: product relationships
3. Streaming: real-time clickstream analysis
4. Delta Lake: ACID transactions on big data

Resources:
- PySpark Docs: https://spark.apache.org/docs/latest/api/python/
- MegaStore Dataset: Check data/
- Spark UI: http://localhost:4040
""")

# Stop Spark session when done (optional)
# spark.stop()
