// Neo4j MegaStore Graph Import Script
// This script creates nodes and relationships from the MegaStore data
//
// INSTRUCTIONS:
// 1. Start Neo4j: docker-compose up -d
// 2. Open Neo4j Browser: http://localhost:7474
// 3. Copy and paste each section into the query editor and run (Ctrl+Enter)
// 4. Or run from command line: cypher-shell < import-megastore.cypher

// ============================================================================
// PART 1: CREATE CONSTRAINTS AND INDEXES
// ============================================================================
// These improve query performance significantly

CREATE CONSTRAINT product_id_constraint IF NOT EXISTS FOR (p:Product) REQUIRE p.product_id IS UNIQUE;
CREATE CONSTRAINT customer_id_constraint IF NOT EXISTS FOR (c:Customer) REQUIRE c.customer_id IS UNIQUE;
CREATE CONSTRAINT category_id_constraint IF NOT EXISTS FOR (cat:Category) REQUIRE cat.category_id IS UNIQUE;
CREATE CONSTRAINT supplier_id_constraint IF NOT EXISTS FOR (s:Supplier) REQUIRE s.supplier_id IS UNIQUE;
CREATE CONSTRAINT order_id_constraint IF NOT EXISTS FOR (o:Order) REQUIRE o.order_id IS UNIQUE;

CREATE INDEX product_name_idx IF NOT EXISTS FOR (p:Product) ON (p.name);
CREATE INDEX customer_email_idx IF NOT EXISTS FOR (c:Customer) ON (c.email);
CREATE INDEX category_name_idx IF NOT EXISTS FOR (cat:Category) ON (cat.name);
CREATE INDEX order_status_idx IF NOT EXISTS FOR (o:Order) ON (o.status);

// ============================================================================
// PART 2: IMPORT PRODUCTS
// ============================================================================
// Load products from CSV
LOAD CSV WITH HEADERS FROM 'file:///products.csv' AS row
CREATE (p:Product {
    product_id: row.product_id,
    name: row.product_name,
    description: row.description,
    price: toFloat(row.price),
    rating: toFloat(row.average_rating),
    reviews_count: toInteger(row.review_count)
});

// ============================================================================
// PART 3: IMPORT CATEGORIES
// ============================================================================
// Load categories from CSV
LOAD CSV WITH HEADERS FROM 'file:///categories.csv' AS row
CREATE (c:Category {
    category_id: row.category_id,
    name: row.category_name,
    description: row.description
});

// ============================================================================
// PART 4: IMPORT SUPPLIERS
// ============================================================================
// Load suppliers from CSV
LOAD CSV WITH HEADERS FROM 'file:///suppliers.csv' AS row
CREATE (s:Supplier {
    supplier_id: row.supplier_id,
    name: row.supplier_name,
    email: row.email,
    country: row.country
});

// ============================================================================
// PART 5: IMPORT CUSTOMERS
// ============================================================================
// Load customers from CSV
LOAD CSV WITH HEADERS FROM 'file:///customers.csv' AS row
CREATE (c:Customer {
    customer_id: row.customer_id,
    name: row.customer_name,
    email: row.email,
    country: row.country,
    registration_date: row.registration_date
});

// ============================================================================
// PART 6: IMPORT ORDERS
// ============================================================================
// Load orders from CSV
LOAD CSV WITH HEADERS FROM 'file:///orders.csv' AS row
CREATE (o:Order {
    order_id: row.order_id,
    order_date: row.order_date,
    status: row.status,
    total_amount: toFloat(row.total_amount),
    discount_amount: toFloat(row.discount_amount),
    shipping_cost: toFloat(row.shipping_cost),
    payment_method: row.payment_method
});

// ============================================================================
// PART 7: IMPORT ORDER ITEMS
// ============================================================================
// Load order items from CSV
LOAD CSV WITH HEADERS FROM 'file:///order_items.csv' AS row
CREATE (oi:OrderItem {
    item_id: row.item_id,
    quantity: toInteger(row.quantity),
    unit_price: toFloat(row.unit_price),
    total_price: toFloat(row.total_price)
});

// ============================================================================
// PART 8: CREATE RELATIONSHIPS - CUSTOMERS PLACED ORDERS
// ============================================================================
// Link customers to their orders
LOAD CSV WITH HEADERS FROM 'file:///orders.csv' AS row
MATCH (c:Customer {customer_id: row.customer_id})
MATCH (o:Order {order_id: row.order_id})
CREATE (c)-[:PLACED]->(o);

// ============================================================================
// PART 9: CREATE RELATIONSHIPS - ORDERS CONTAIN ITEMS
// ============================================================================
// Link orders to their items
LOAD CSV WITH HEADERS FROM 'file:///order_items.csv' AS row
MATCH (o:Order {order_id: row.order_id})
MATCH (oi:OrderItem {item_id: row.item_id})
CREATE (o)-[:CONTAINS]->(oi);

// ============================================================================
// PART 10: CREATE RELATIONSHIPS - ORDER ITEMS REFERENCE PRODUCTS
// ============================================================================
// Link order items to products
LOAD CSV WITH HEADERS FROM 'file:///order_items.csv' AS row
MATCH (oi:OrderItem {item_id: row.item_id})
MATCH (p:Product {product_id: row.product_id})
CREATE (oi)-[:IS_PRODUCT]->(p);

// ============================================================================
// PART 11: CREATE RELATIONSHIPS - PRODUCTS TO CATEGORIES
// ============================================================================
// Link products to their categories
LOAD CSV WITH HEADERS FROM 'file:///products.csv' AS row
MATCH (p:Product {product_id: row.product_id})
MATCH (c:Category {category_id: row.category_id})
CREATE (p)-[:BELONGS_TO]->(c);

// ============================================================================
// PART 12: CREATE RELATIONSHIPS - PRODUCTS TO SUPPLIERS
// ============================================================================
// Link products to their suppliers
LOAD CSV WITH HEADERS FROM 'file:///products.csv' AS row
MATCH (p:Product {product_id: row.product_id})
MATCH (s:Supplier {supplier_id: row.supplier_id})
CREATE (p)-[:SUPPLIED_BY]->(s);

// ============================================================================
// PART 13: CREATE PRODUCT RELATIONSHIPS (from product_relationships.csv)
// ============================================================================
// Link related products (complementary items, alternatives, etc.)
LOAD CSV WITH HEADERS FROM 'file:///product_relationships.csv' AS row
MATCH (p1:Product {product_id: row.product_id_1})
MATCH (p2:Product {product_id: row.product_id_2})
CREATE (p1)-[:RELATED_TO {type: row.relationship_type}]->(p2);

// ============================================================================
// PART 14: CREATE CUSTOMER RELATIONSHIPS (from customer_relationships.csv)
// ============================================================================
// Link customers who know each other or have similar interests
LOAD CSV WITH HEADERS FROM 'file:///customer_relationships.csv' AS row
MATCH (c1:Customer {customer_id: row.customer_id_1})
MATCH (c2:Customer {customer_id: row.customer_id_2})
CREATE (c1)-[:CONNECTED_TO {type: row.relationship_type}]->(c2);

// ============================================================================
// VERIFICATION QUERIES
// ============================================================================
// Run these to verify the import was successful

// Count imported nodes
MATCH (n:Product) RETURN "Products: " + count(n) as count;
MATCH (n:Customer) RETURN "Customers: " + count(n) as count;
MATCH (n:Category) RETURN "Categories: " + count(n) as count;
MATCH (n:Supplier) RETURN "Suppliers: " + count(n) as count;
MATCH (n:Order) RETURN "Orders: " + count(n) as count;
MATCH (n:OrderItem) RETURN "OrderItems: " + count(n) as count;

// Count relationships
MATCH ()-[r:PLACED]->() RETURN "PLACED: " + count(r) as count;
MATCH ()-[r:CONTAINS]->() RETURN "CONTAINS: " + count(r) as count;
MATCH ()-[r:IS_PRODUCT]->() RETURN "IS_PRODUCT: " + count(r) as count;
MATCH ()-[r:BELONGS_TO]->() RETURN "BELONGS_TO: " + count(r) as count;
MATCH ()-[r:SUPPLIED_BY]->() RETURN "SUPPLIED_BY: " + count(r) as count;
MATCH ()-[r:RELATED_TO]->() RETURN "RELATED_TO: " + count(r) as count;
MATCH ()-[r:CONNECTED_TO]->() RETURN "CONNECTED_TO: " + count(r) as count;

// ============================================================================
// EXAMPLE QUERIES FOR EXPLORATION
// ============================================================================

// Find top-rated products
MATCH (p:Product)
RETURN p.name, p.price, p.rating
ORDER BY p.rating DESC
LIMIT 10;

// Find products by category
MATCH (p:Product)-[:BELONGS_TO]->(c:Category)
WHERE c.name = "Electronics"
RETURN p.name, p.price
LIMIT 20;

// Find related products
MATCH (p1:Product {name: "Laptop"})-[:RELATED_TO]-(p2:Product)
RETURN p2.name, p2.price;

// Find product supply chain
MATCH (p:Product)-[:SUPPLIED_BY]->(s:Supplier)
RETURN p.name, s.name, s.country;

// Find customer network
MATCH (c1:Customer {customer_id: "CUST001"})-[r:CONNECTED_TO]-(c2:Customer)
RETURN c2.name, r.type;

// Find customer orders with totals
MATCH (c:Customer)-[:PLACED]->(o:Order)
RETURN c.name, o.total_amount, o.status
ORDER BY o.total_amount DESC
LIMIT 10;

// Find top customers by revenue
MATCH (c:Customer)-[:PLACED]->(o:Order)
RETURN c.name, count(o) AS order_count, sum(o.total_amount) AS total_revenue
ORDER BY total_revenue DESC
LIMIT 10;
