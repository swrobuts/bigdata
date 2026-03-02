"""
DuckDB MegaStore Analytics Introduction
========================================

DuckDB is a lightweight, in-process SQL analytics database that's perfect for
data exploration and analysis. This notebook demonstrates common tasks.

To convert this to a Jupyter notebook, copy the code into notebook cells.
"""

import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize DuckDB connection (in-memory or to a file)
conn = duckdb.connect(':memory:')  # or ':memory:' for in-memory
print("DuckDB initialized successfully!")

# ============================================================================
# 1. LOADING DATA
# ============================================================================
print("\n" + "="*50)
print("1. LOADING DATA FROM CSV AND PARQUET")
print("="*50)

# Load orders data from Parquet (faster for analytics)
orders_df = conn.execute(
    "SELECT * FROM read_parquet('data/orders.parquet') LIMIT 5"
).fetchall()
print(f"\nLoaded {len(orders_df)} sample orders")

# Load order items from Parquet
order_items_df = conn.execute(
    "SELECT * FROM read_parquet('data/order_items.parquet') LIMIT 5"
).fetchall()
print(f"Loaded sample order items")

# Load clickstream from CSV
clickstream_sample = conn.execute(
    "SELECT * FROM read_csv_auto('data/clickstream.csv') LIMIT 5"
).fetchall()
print(f"Loaded clickstream sample")

# ============================================================================
# 2. BASIC SQL QUERIES
# ============================================================================
print("\n" + "="*50)
print("2. BASIC SQL QUERIES")
print("="*50)

# Count orders
count_result = conn.execute(
    "SELECT COUNT(*) as total_orders FROM read_parquet('data/orders.parquet')"
).fetchone()
print(f"\nTotal orders: {count_result[0]}")

# Aggregate order values
agg_result = conn.execute("""
    SELECT
        COUNT(*) as order_count,
        SUM(total_amount) as total_value,
        AVG(total_amount) as avg_order_value,
        MAX(total_amount) as max_order_value
    FROM read_parquet('data/orders.parquet')
""").fetchone()
print(f"\nOrder Statistics:")
print(f"  Total Orders: {agg_result[0]}")
print(f"  Total Value: ${agg_result[1]:.2f}")
print(f"  Average Order Value: ${agg_result[2]:.2f}")
print(f"  Max Order Value: ${agg_result[3]:.2f}")

# ============================================================================
# 3. JOINS AND RELATIONSHIPS
# ============================================================================
print("\n" + "="*50)
print("3. JOINS - COMBINING TABLES")
print("="*50)

# Join orders with order items
join_query = """
    SELECT
        o.order_id,
        o.order_date,
        COUNT(*) as items_in_order,
        SUM(oi.quantity) as total_quantity
    FROM read_parquet('data/orders.parquet') o
    LEFT JOIN read_parquet('data/order_items.parquet') oi
        ON o.order_id = oi.order_id
    GROUP BY o.order_id, o.order_date
    LIMIT 10
"""
join_result = conn.execute(join_query).fetchdf()
print("\nSample joined data (orders with item counts):")
print(join_result)

# ============================================================================
# 4. TIME-BASED ANALYSIS
# ============================================================================
print("\n" + "="*50)
print("4. TIME-BASED ANALYSIS")
print("="*50)

# Orders by date
time_query = """
    SELECT
        DATE(order_date) as order_date,
        COUNT(*) as orders,
        SUM(total_amount) as daily_total
    FROM read_parquet('data/orders.parquet')
    GROUP BY DATE(order_date)
    ORDER BY order_date DESC
    LIMIT 10
"""
time_result = conn.execute(time_query).fetchdf()
print("\nOrders by date (last 10 days):")
print(time_result)

# ============================================================================
# 5. WORKING WITH PARQUET VS CSV
# ============================================================================
print("\n" + "="*50)
print("5. PARQUET VS CSV COMPARISON")
print("="*50)

import time

# Compare reading times (this is just a demonstration)
print("\nDuckDB automatically optimizes for your data format:")
print("  - Parquet: Columnar, compressed, faster for analytics")
print("  - CSV: Text-based, universal, but slower to parse")

# ============================================================================
# 6. EXPORTING RESULTS
# ============================================================================
print("\n" + "="*50)
print("6. EXPORTING RESULTS")
print("="*50)

# Convert DuckDB result to Pandas DataFrame
result_df = conn.execute("""
    SELECT
        DATE(order_date) as date,
        COUNT(*) as orders
    FROM read_parquet('data/orders.parquet')
    GROUP BY DATE(order_date)
""").fetchdf()

print("\nResult as Pandas DataFrame:")
print(result_df.head())

# Save to CSV
# result_df.to_csv('output/daily_orders.csv', index=False)
# print("Saved to output/daily_orders.csv")

# ============================================================================
# 7. ADVANCED QUERIES - WINDOW FUNCTIONS
# ============================================================================
print("\n" + "="*50)
print("7. ADVANCED QUERIES - WINDOW FUNCTIONS")
print("="*50)

window_query = """
    SELECT
        order_id,
        total_amount,
        SUM(total_amount) OVER (ORDER BY order_id) as running_total,
        total_amount - LAG(total_amount, 1, 0) OVER (ORDER BY order_id) as diff_from_prev
    FROM read_parquet('data/orders.parquet')
    LIMIT 10
"""
window_result = conn.execute(window_query).fetchdf()
print("\nWindow functions (running totals):")
print(window_result)

# ============================================================================
# 8. DATA QUALITY CHECKS
# ============================================================================
print("\n" + "="*50)
print("8. DATA QUALITY CHECKS")
print("="*50)

quality_query = """
    SELECT
        COUNT(*) as total_rows,
        COUNT(DISTINCT order_id) as unique_orders,
        COUNT(*) FILTER (WHERE total_amount IS NULL) as null_amounts,
        COUNT(*) FILTER (WHERE total_amount < 0) as negative_amounts
    FROM read_parquet('data/orders.parquet')
"""
quality_result = conn.execute(quality_query).fetchone()
print(f"\nData Quality Metrics:")
print(f"  Total rows: {quality_result[0]}")
print(f"  Unique orders: {quality_result[1]}")
print(f"  Null amounts: {quality_result[2]}")
print(f"  Negative amounts: {quality_result[3]}")

# ============================================================================
# NEXT STEPS
# ============================================================================
print("\n" + "="*50)
print("NEXT STEPS")
print("="*50)
print("""
1. Explore the MegaStore data:
   - Load products.csv and analyze product categories
   - Join orders with products to understand buying patterns

2. Practice SQL:
   - Find top customers by purchase amount
   - Analyze product performance (sales, revenue)
   - Calculate customer lifetime value

3. Create visualizations:
   - Plot order trends over time
   - Analyze product category distribution

4. Export results:
   - Save analysis results to CSV
   - Create summary reports

DuckDB Documentation: https://duckdb.org/docs/
""")

# Close connection when done
conn.close()
