# MegaStore E-Commerce Dataset

## Overview
This dataset represents a fictional German e-commerce company called "MegaStore". It contains realistic e-commerce data including products, customers, orders, and interactions across multiple platforms.

**Total Records**: ~1 million transactions
**Time Period**: 2022-01-01 to 2025-12-31
**Geographic Focus**: Germany (with some Austrian and Swiss customers)

## Dataset Files

### 1. Products
- **files**: `products.csv`, `products.json`
- **records**: ~5,000 products
- **fields**: product_id, name, description, category, subcategory, brand, price, cost_price, weight_kg, rating_avg, rating_count, in_stock, stock_quantity, supplier_id, tags, created_at
- **categories**: Elektronik, Kleidung, Haushalt, Sport, Bücher, Spielzeug, Garten, Lebensmittel, Beauty, Auto

### 2. Customers
- **files**: `customers.csv`, `customers.json`
- **records**: ~50,000 customers
- **fields**: customer_id, first_name, last_name, email, age, gender, city, postal_code, country, registration_date, customer_segment, lifetime_value, total_orders, preferred_payment
- **segments**: Bronze, Silver, Gold, Platinum (lifetime value correlated with segment)
- **payment_methods**: Kreditkarte, PayPal, Überweisung, Klarna

### 3. Orders
- **files**: `orders.csv`, `orders.parquet`, `orders_sample.json`
- **records**: ~500,000 orders
- **fields**: order_id, customer_id, order_date, status, total_amount, discount_amount, shipping_cost, payment_method, shipping_city, delivery_days
- **statuses**: completed, shipped, cancelled, returned
- **temporal pattern**: Seasonal peaks in November-December (realistic holiday shopping)

### 4. Order Items
- **files**: `order_items.csv`, `order_items.parquet`
- **records**: ~1,200,000 items (average 2.4 items per order)
- **fields**: item_id, order_id, product_id, quantity, unit_price, total_price, discount_percent
- **note**: Links orders to products, enables detailed transaction analysis

### 5. Product Relationships (Neo4j)
- **file**: `product_relationships.csv`
- **records**: ~20,000 relationships
- **fields**: source_product_id, target_product_id, relationship_type
- **relationship_types**: BOUGHT_TOGETHER, SIMILAR_TO, ACCESSORY_OF, UPGRADE_OF
- **use_case**: Product recommendation systems, graph analytics

### 6. Customer Relationships (Neo4j)
- **file**: `customer_relationships.csv`
- **records**: ~30,000 relationships
- **fields**: source_customer_id, target_customer_id, relationship_type
- **relationship_types**: REFERRED_BY, SAME_HOUSEHOLD, SIMILAR_TASTE
- **use_case**: Customer network analysis, referral tracking

### 7. Categories
- **file**: `categories.json`
- **records**: ~30 categories + subcategories
- **structure**: Hierarchical (main category -> subcategories)
- **fields**: id, name, parent_id, level
- **use_case**: Neo4j category hierarchy, MongoDB document structure

### 8. Suppliers
- **files**: `suppliers.csv`, `suppliers.json`
- **records**: ~200 suppliers
- **fields**: supplier_id, company_name, contact_person, email, city, country, product_count, avg_delivery_days, rating
- **use_case**: Supply chain analysis, vendor management

### 9. Clickstream / Web Logs
- **files**: `clickstream.csv`, `clickstream.parquet`
- **records**: ~200,000 events
- **fields**: event_id, session_id, customer_id (nullable), timestamp, event_type, page_url, product_id (nullable), device_type, browser, referrer_source
- **event_types**: page_view, product_view, add_to_cart, checkout, purchase
- **funnel**: Realistic conversion funnel (many views → fewer carts → fewer purchases)
- **use_case**: Apache Spark analysis, user behavior analysis

### 10. Reviews
- **files**: `reviews.csv`, `reviews.json`
- **records**: ~100,000 reviews
- **fields**: review_id, product_id, customer_id, rating, title, text, helpful_votes, verified_purchase, review_date
- **rating_distribution**: Skewed towards positive (35% 5-star, 30% 4-star)
- **use_case**: Sentiment analysis, product quality assessment

## Data Characteristics

### Realistic Patterns
- **Seasonal Orders**: Peaks in November-December (holiday shopping)
- **Customer Segments**: Lifetime value correlated with order frequency
- **Price Distributions**: Category-specific price ranges with realistic variance
- **Conversion Funnel**: Realistic ratio of page views to purchases
- **Geographic**: Real German cities with postal code ranges

### Interconnections
- Products linked to suppliers and categories
- Orders linked to customers and products
- Reviews linked to customers and products
- Clickstream linked to products and customers
- All IDs consistent across datasets (enabling joins)

## Database Usage

### MongoDB (Document Store)
- Import `products.json`, `customers.json`, `orders_sample.json`, `reviews.json`, `categories.json`
- Document-oriented storage with flexible schema
- Use for product catalog, customer profiles, review collections

### Neo4j (Graph Database)
- Import `categories.json` as category hierarchy
- Import `product_relationships.csv` for product graphs
- Import `customer_relationships.csv` for customer networks
- Ideal for recommendation systems and network analysis

### DuckDB (Analytical SQL)
- Use `products.csv`, `customers.csv`, `orders.csv`, `order_items.csv`, `reviews.csv`
- Or use Parquet versions for better performance: `orders.parquet`, `order_items.parquet`
- Supports complex joins and analytical queries across dimensions

### Apache Spark (Batch Processing)
- Use `clickstream.parquet` for high-volume data processing
- Use `orders.parquet` for transaction analysis
- Use `order_items.parquet` for detailed item-level analytics
- Parquet format optimized for columnar processing

## Data Generation Details

- **Random Seed**: 42 (reproducible)
- **Generated**: 2026-03-02 11:37:21
- **Total Size**: ~500 MB across all formats
- **Format Support**: CSV, JSON, Parquet
- **Tools Used**: Python (pandas, numpy)

## Join Keys

```
products ← customers (via orders)
products.product_id ← order_items.product_id
orders.order_id ← order_items.order_id
orders.customer_id ← customers.customer_id
orders.product_id ← products.product_id (from order_items)
reviews.product_id ← products.product_id
reviews.customer_id ← customers.customer_id
clickstream.product_id ← products.product_id
clickstream.customer_id ← customers.customer_id
products.category ← categories.parent_id
```

## Statistics

| Dataset | Records | Size (CSV) | Size (Parquet) |
|---------|---------|-----------|---|
| Products | 5,000 | ~2 MB | ~0.5 MB |
| Customers | 50,000 | ~8 MB | ~2 MB |
| Orders | 500,000 | ~25 MB | ~5 MB |
| Order Items | 1,200,000 | ~40 MB | ~8 MB |
| Clickstream | 200,000 | ~20 MB | ~3 MB |
| Reviews | 100,000 | ~15 MB | ~2 MB |
| **Total** | **~2M** | **~120 MB** | **~25 MB** |

## Example Queries

### DuckDB: Top products by revenue
```sql
SELECT p.name, SUM(oi.total_price) as revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.name
ORDER BY revenue DESC
LIMIT 10;
```

### Neo4j: Product recommendations
```cypher
MATCH (p1:Product)<-[:REVIEWS]-(c:Customer)-[:REVIEWS]->(p2:Product)
WHERE p1.id = $product_id AND p1 <> p2
RETURN p2.name, COUNT(*) as common_reviewers
ORDER BY common_reviewers DESC
LIMIT 5;
```

### Spark: Customer lifetime value by segment
```python
orders_df.groupBy("customer_segment").agg(
    F.sum("total_amount").alias("total_revenue"),
    F.avg("total_amount").alias("avg_order_value"),
    F.count("order_id").alias("order_count")
).show()
```

## Limitations & Notes

- Customer IDs, product IDs, and order IDs are all sequential (not realistic UUIDs)
- Email addresses are generated and do not correspond to real people
- Company and product names are fictional
- Geographic data is accurate (real cities, postal codes) but customer names/profiles are synthetic
- Dates are realistic but randomly distributed (not following actual market patterns beyond seasonality)

## License
This dataset is provided for educational purposes in the Big Data university course.
