#!/usr/bin/env python3
"""
MegaStore E-Commerce Dataset Generator
Generates realistic datasets for a fictional German e-commerce company.
Outputs multiple formats for use with MongoDB, Neo4j, DuckDB, and Apache Spark.
"""

import os
import json
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import warnings

warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
random.seed(42)
np.random.seed(42)

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "megastore")
os.makedirs(OUTPUT_DIR, exist_ok=True)
TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# German cities for realistic data
GERMAN_CITIES = [
    'München', 'Berlin', 'Hamburg', 'Frankfurt am Main', 'Köln',
    'Stuttgart', 'Düsseldorf', 'Würzburg', 'Schweinfurt', 'Nürnberg',
    'Hannover', 'Dresden', 'Leipzig', 'Dortmund', 'Essen',
    'Leverkusen', 'Mannheim', 'Augsburg', 'Bielefeld', 'Wuppertal',
    'Bonn', 'Münster', 'Gelsenkirchen', 'Aachen', 'Freiburg'
]

POSTAL_CODES = {
    'München': '80000-81999',
    'Berlin': '10000-14999',
    'Hamburg': '20000-21999',
    'Frankfurt am Main': '60000-60999',
    'Köln': '50000-51999',
    'Stuttgart': '70000-70999',
    'Düsseldorf': '40000-40999',
    'Würzburg': '97000-97999',
    'Schweinfurt': '97400-97499',
    'Nürnberg': '90000-90999',
}

CATEGORIES = {
    'Elektronik': ['Smartphones', 'Laptops', 'Tablets', 'Kopfhörer', 'Kameras', 'Gaming'],
    'Kleidung': ['Herren', 'Damen', 'Kinder', 'Schuhe', 'Accessoires'],
    'Haushalt': ['Küche', 'Schlafzimmer', 'Wohnzimmer', 'Bad', 'Dekoration'],
    'Sport': ['Fitness', 'Outdoor', 'Ballsportarten', 'Wintersport', 'Fahrräder'],
    'Bücher': ['Sachbücher', 'Romane', 'E-Books', 'Kinderbücher', 'Comics'],
    'Spielzeug': ['Puppen', 'Bauklötze', 'Videospiele', 'Action-Figuren', 'Puzzle'],
    'Garten': ['Werkzeuge', 'Pflanzen', 'Möbel', 'Dekoration', 'Beleuchtung'],
    'Lebensmittel': ['Bio-Produkte', 'Getränke', 'Süßwaren', 'Backzutaten', 'Gewürze'],
    'Beauty': ['Kosmetik', 'Hautpflege', 'Haarpflege', 'Parfüm', 'Wellness'],
    'Auto': ['Zubehör', 'Reifen', 'Öl & Flüssigkeiten', 'Ersatzteile', 'Reinigung']
}

BRANDS = {
    'Elektronik': ['Apple', 'Samsung', 'Sony', 'LG', 'Bosch', 'Siemens', 'Lenovo'],
    'Kleidung': ['H&M', 'Zara', 'Nike', 'Adidas', 'Tom Tailor', 'Esprit', 'S.Oliver'],
    'Haushalt': ['Ikea', 'Mömax', 'Poco', 'Baumarkt', 'WMF', 'Fissler', 'Wmf'],
    'Sport': ['Nike', 'Adidas', 'Puma', 'Decathlon', 'Scott', 'Trek', 'Shimano'],
    'Bücher': ['Penguin', 'Random House', 'dtv', 'Heyne', 'Bastei Lübbe'],
    'Spielzeug': ['Lego', 'Playmobil', 'Ravensburger', 'Mattel', 'Hasbro'],
    'Garten': ['Bosch', 'Stihl', 'Kärcher', 'Gardena', 'Husqvarna'],
    'Lebensmittel': ['Bio Company', 'Bertschi', 'Ritter Sport', 'Lindt', 'Gepa'],
    'Beauty': ['Nivea', 'Loreal', 'Dove', 'Eucerin', 'Estee Lauder'],
    'Auto': ['Bosch', 'Michelin', 'Castrol', 'Liqui Moly', 'Sparco']
}

PRICE_RANGES = {
    'Elektronik': (99, 1499),
    'Kleidung': (15, 150),
    'Haushalt': (20, 500),
    'Sport': (30, 800),
    'Bücher': (8, 50),
    'Spielzeug': (10, 200),
    'Garten': (25, 1000),
    'Lebensmittel': (3, 50),
    'Beauty': (5, 150),
    'Auto': (15, 500)
}

PRODUCT_NAMES = {
    'Elektronik': [
        'Smartphone Pro Max', 'Wireless Earbuds', 'Smart Watch', 'Tablet Ultra',
        '4K Action Camera', 'Portable Speaker', 'USB-C Hub', 'Phone Stand'
    ],
    'Kleidung': [
        'Premium T-Shirt', 'Slim Jeans', 'Athletic Hoodie', 'Casual Dress',
        'Running Shoes', 'Winter Jacket', 'Baseball Cap', 'Wool Sweater'
    ],
    'Haushalt': [
        'Espresso Machine', 'Mixer Blender', 'Coffee Maker', 'Vacuum Cleaner',
        'Iron Board', 'Knife Set', 'Bed Sheets', 'Curtain Rod'
    ],
    'Sport': [
        'Yoga Mat', 'Dumbbells Set', 'Running Watch', 'Bicycle Helmet',
        'Fitness Tracker', 'Swimming Goggles', 'Tennis Racket', 'Skateboard'
    ],
    'Bücher': [
        'Bestseller Novel', 'Self-Help Guide', 'Science Fiction Epic',
        'Biography Book', 'Cookbook', 'Children\'s Story', 'Comic Series'
    ],
    'Spielzeug': [
        'LEGO Builder Set', 'Action Figure Pack', 'Puzzle Game', 'Dolly Set',
        'Remote Control Car', 'Building Blocks', 'Board Game'
    ],
    'Garten': [
        'Hedge Trimmer', 'Garden Hose', 'Plant Pots', 'Outdoor Chair',
        'LED Light Strip', 'Garden Fork', 'Watering Can', 'Plant Stakes'
    ],
    'Lebensmittel': [
        'Organic Coffee Beans', 'Chocolate Bar', 'Pasta Pack', 'Olive Oil',
        'Cereal Box', 'Juice Bottle', 'Bread Mix', 'Spice Set'
    ],
    'Beauty': [
        'Face Cream', 'Shampoo Bottle', 'Lipstick', 'Face Mask',
        'Body Lotion', 'Perfume Spray', 'Sunscreen', 'Lip Balm'
    ],
    'Auto': [
        'Car Wax', 'Floor Mats', 'Phone Mount', 'Air Freshener',
        'Tire Shine', 'Windshield Cleaner', 'Seat Cover', 'Dashboard Cleaner'
    ]
}

PAYMENT_METHODS = ['Kreditkarte', 'PayPal', 'Überweisung', 'Klarna']
CUSTOMER_SEGMENTS = ['Bronze', 'Silver', 'Gold', 'Platinum']
EVENT_TYPES = ['page_view', 'product_view', 'add_to_cart', 'checkout', 'purchase']
DEVICES = ['mobile', 'desktop', 'tablet']
REFERRERS = ['google', 'direct', 'social', 'email', 'affiliate']

def log_progress(message):
    """Print progress message with timestamp"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

def generate_suppliers(count=200):
    """Generate supplier data"""
    log_progress(f"Generating {count} suppliers...")

    suppliers = []
    for i in range(1, count + 1):
        suppliers.append({
            'supplier_id': i,
            'company_name': f"Supplier-{i:04d} GmbH",
            'contact_person': f"Contact Person {i}",
            'email': f"supplier{i}@megastore-suppliers.de",
            'city': random.choice(GERMAN_CITIES),
            'country': 'DE',
            'product_count': np.random.randint(10, 500),
            'avg_delivery_days': np.random.randint(1, 14),
            'rating': round(random.uniform(3.5, 5.0), 2)
        })

    return suppliers

def generate_products(suppliers, count=5000):
    """Generate product data"""
    log_progress(f"Generating {count} products...")

    products = []
    product_id = 1

    for category, subcategories in CATEGORIES.items():
        category_count = count // len(CATEGORIES)

        for _ in range(category_count):
            subcategory = random.choice(subcategories)
            brand = random.choice(BRANDS[category])
            product_name = random.choice(PRODUCT_NAMES[category])

            min_price, max_price = PRICE_RANGES[category]
            price = round(random.gauss((min_price + max_price) / 2, (max_price - min_price) / 6), 2)
            price = max(min_price, min(max_price, price))

            cost_price = round(price * random.uniform(0.3, 0.6), 2)

            products.append({
                'product_id': product_id,
                'name': f"{product_name} {brand} v{random.randint(1, 5)}",
                'description': f"Premium {category} product in {subcategory} category",
                'category': category,
                'subcategory': subcategory,
                'brand': brand,
                'price': price,
                'cost_price': cost_price,
                'weight_kg': round(random.uniform(0.1, 10), 2),
                'rating_avg': round(random.uniform(2.5, 5.0), 2),
                'rating_count': np.random.randint(0, 1000),
                'in_stock': random.choice([True, True, True, False]),  # 75% in stock
                'stock_quantity': np.random.randint(0, 500),
                'supplier_id': random.randint(1, len(suppliers)),
                'tags': [subcategory, brand, category.lower()],
                'created_at': (datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1826))).isoformat()
            })
            product_id += 1

    return products

def generate_customers(count=50000):
    """Generate customer data"""
    log_progress(f"Generating {count} customers...")

    first_names = [
        'Hans', 'Marie', 'Klaus', 'Anna', 'Peter', 'Petra', 'Georg', 'Gabriele',
        'Frank', 'Franziska', 'Wolfgang', 'Waltraud', 'Jürgen', 'Jutta',
        'Dieter', 'Dagmar', 'Heinz', 'Heidi', 'Karl', 'Käthe'
    ]

    last_names = [
        'Mueller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Becker', 'Schulz',
        'Hoffmann', 'Schröter', 'Koch', 'Bauer', 'Klein', 'Wolf', 'Neumann',
        'Schwarz', 'Zimmermann', 'Krämer', 'Huber', 'Kaiser', 'Krause'
    ]

    customers = []
    for i in range(1, count + 1):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        city = random.choice(GERMAN_CITIES)

        # Get postal code range for city
        postal_range = POSTAL_CODES.get(city, '70000-79999')
        start, end = [int(x) for x in postal_range.split('-')]
        postal_code = str(random.randint(start, end))

        # Assign segment based on random distribution (skew towards Bronze)
        segment_rand = random.random()
        if segment_rand < 0.5:
            segment = 'Bronze'
        elif segment_rand < 0.8:
            segment = 'Silver'
        elif segment_rand < 0.95:
            segment = 'Gold'
        else:
            segment = 'Platinum'

        # Lifetime value correlated with segment
        segment_ltv = {
            'Bronze': (100, 1000),
            'Silver': (1000, 5000),
            'Gold': (5000, 20000),
            'Platinum': (20000, 100000)
        }
        ltv_min, ltv_max = segment_ltv[segment]
        lifetime_value = round(random.uniform(ltv_min, ltv_max), 2)

        # Orders correlated with segment
        segment_orders = {
            'Bronze': (1, 5),
            'Silver': (5, 15),
            'Gold': (15, 50),
            'Platinum': (50, 200)
        }
        orders_min, orders_max = segment_orders[segment]
        total_orders = np.random.randint(orders_min, orders_max)

        registration_date = (datetime(2018, 1, 1) + timedelta(days=random.randint(0, 2190))).date()

        customers.append({
            'customer_id': i,
            'first_name': first_name,
            'last_name': last_name,
            'email': f"{first_name.lower()}.{last_name.lower()}{i}@email.de",
            'age': np.random.randint(18, 85),
            'gender': random.choice(['M', 'F', 'O']),
            'city': city,
            'postal_code': postal_code,
            'country': random.choice(['DE', 'DE', 'DE', 'DE', 'AT', 'CH']),  # Mostly DE
            'registration_date': registration_date.isoformat(),
            'customer_segment': segment,
            'lifetime_value': lifetime_value,
            'total_orders': total_orders,
            'preferred_payment': random.choice(PAYMENT_METHODS)
        })

    return customers

def generate_orders(customers, count=500000):
    """Generate order data"""
    log_progress(f"Generating {count} orders...")

    orders = []
    order_id = 1
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2025, 12, 31)

    for _ in range(count):
        customer = random.choice(customers)
        customer_id = customer['customer_id']

        # Add seasonal pattern (more orders in Nov/Dec)
        probs = np.array([0.06, 0.06, 0.07, 0.07, 0.08, 0.08,
                          0.08, 0.08, 0.08, 0.09, 0.12, 0.12])
        probs = probs / probs.sum()  # Normalize to sum to 1.0
        month = np.random.choice(range(1, 13), p=probs)
        year = random.randint(2022, 2025)

        # Random day in month
        if month == 2:
            day = random.randint(1, 28)
        elif month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 31)

        order_date = datetime(year, month, day) + timedelta(hours=random.randint(0, 23))

        # Order status (mostly completed)
        status_rand = random.random()
        if status_rand < 0.75:
            status = 'completed'
        elif status_rand < 0.85:
            status = 'shipped'
        elif status_rand < 0.95:
            status = 'cancelled'
        else:
            status = 'returned'

        # Total amount based on customer segment
        segment_amounts = {
            'Bronze': (20, 300),
            'Silver': (50, 500),
            'Gold': (100, 1000),
            'Platinum': (200, 2000)
        }
        min_amt, max_amt = segment_amounts[customer['customer_segment']]
        total_amount = round(random.uniform(min_amt, max_amt), 2)

        discount_amount = round(total_amount * random.uniform(0, 0.2), 2)
        shipping_cost = round(random.uniform(0, 15), 2) if total_amount > 50 else round(random.uniform(3.99, 8.99), 2)

        delivery_days = np.random.randint(1, 10) if status in ['completed', 'returned'] else None

        orders.append({
            'order_id': order_id,
            'customer_id': customer_id,
            'order_date': order_date.isoformat(),
            'status': status,
            'total_amount': total_amount,
            'discount_amount': discount_amount,
            'shipping_cost': shipping_cost,
            'payment_method': customer['preferred_payment'],
            'shipping_city': customer['city'],
            'delivery_days': delivery_days
        })
        order_id += 1

    return orders

def generate_order_items(orders, products, count=1200000):
    """Generate order items data"""
    log_progress(f"Generating ~{count} order items...")

    order_items = []
    item_id = 1

    for order in orders:
        # Average 2.4 items per order
        num_items = np.random.choice([1, 2, 3, 4, 5], p=[0.3, 0.4, 0.2, 0.07, 0.03])

        for _ in range(num_items):
            product = random.choice(products)
            quantity = np.random.randint(1, 5)
            unit_price = product['price']
            total_price = round(unit_price * quantity, 2)
            discount_percent = round(random.uniform(0, 15), 2)

            order_items.append({
                'item_id': item_id,
                'order_id': order['order_id'],
                'product_id': product['product_id'],
                'quantity': quantity,
                'unit_price': unit_price,
                'total_price': total_price,
                'discount_percent': discount_percent
            })
            item_id += 1

    log_progress(f"Generated {len(order_items)} order items")
    return order_items

def generate_product_relationships(products, count=20000):
    """Generate product relationships for Neo4j"""
    log_progress(f"Generating {count} product relationships...")

    relationships = []
    relationship_types = ['BOUGHT_TOGETHER', 'SIMILAR_TO', 'ACCESSORY_OF', 'UPGRADE_OF']

    for _ in range(count):
        source = random.choice(products)
        target = random.choice(products)

        if source['product_id'] != target['product_id']:
            relationships.append({
                'source_product_id': source['product_id'],
                'target_product_id': target['product_id'],
                'relationship_type': random.choice(relationship_types)
            })

    # Remove duplicates
    relationships = list({(r['source_product_id'], r['target_product_id'], r['relationship_type']): r
                         for r in relationships}.values())

    return relationships

def generate_customer_relationships(customers, count=30000):
    """Generate customer relationships for Neo4j"""
    log_progress(f"Generating {count} customer relationships...")

    relationships = []
    relationship_types = ['REFERRED_BY', 'SAME_HOUSEHOLD', 'SIMILAR_TASTE']

    for _ in range(count):
        source = random.choice(customers)
        target = random.choice(customers)

        if source['customer_id'] != target['customer_id']:
            relationships.append({
                'source_customer_id': source['customer_id'],
                'target_customer_id': target['customer_id'],
                'relationship_type': random.choice(relationship_types)
            })

    # Remove duplicates
    relationships = list({(r['source_customer_id'], r['target_customer_id'], r['relationship_type']): r
                         for r in relationships}.values())

    return relationships

def generate_clickstream(customers, products, count=200000):
    """Generate clickstream/web logs for Spark"""
    log_progress(f"Generating {count} clickstream events...")

    clickstream = []
    event_id = 1
    session_counter = 0

    for _ in range(count):
        session_counter += 1
        session_id = f"session_{session_counter:08d}"

        # Create funnel: many views -> fewer carts -> fewer purchases
        event_type_rand = random.random()
        if event_type_rand < 0.5:
            event_type = 'page_view'
            customer_id = None if random.random() < 0.3 else random.choice(customers)['customer_id']
            product_id = None
        elif event_type_rand < 0.75:
            event_type = 'product_view'
            customer_id = random.choice(customers)['customer_id'] if random.random() < 0.7 else None
            product_id = random.choice(products)['product_id']
        elif event_type_rand < 0.9:
            event_type = 'add_to_cart'
            customer_id = random.choice(customers)['customer_id']
            product_id = random.choice(products)['product_id']
        elif event_type_rand < 0.95:
            event_type = 'checkout'
            customer_id = random.choice(customers)['customer_id']
            product_id = None
        else:
            event_type = 'purchase'
            customer_id = random.choice(customers)['customer_id']
            product_id = None

        timestamp = datetime(2022, 1, 1) + timedelta(
            days=random.randint(0, 1460),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        clickstream.append({
            'event_id': event_id,
            'session_id': session_id,
            'customer_id': customer_id,
            'timestamp': timestamp.isoformat(),
            'event_type': event_type,
            'page_url': f"/category/{random.choice(list(CATEGORIES.keys())).lower()}",
            'product_id': product_id,
            'device_type': random.choice(DEVICES),
            'browser': random.choice(['Chrome', 'Firefox', 'Safari', 'Edge']),
            'referrer_source': random.choice(REFERRERS)
        })
        event_id += 1

    return clickstream

def generate_reviews(customers, products, count=100000):
    """Generate product reviews"""
    log_progress(f"Generating {count} reviews...")

    reviews = []
    review_id = 1

    for _ in range(count):
        product = random.choice(products)
        customer = random.choice(customers)

        rating = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.1, 0.2, 0.3, 0.35])

        review_texts = {
            5: ['Excellent product!', 'Highly recommended!', 'Perfect quality!', 'Love it!', 'Great value!'],
            4: ['Very good product', 'Good quality', 'Satisfied with purchase', 'Nice item'],
            3: ['Average product', 'Okay for the price', 'Decent quality', 'Could be better'],
            2: ['Not as expected', 'Poor quality', 'Disappointed', 'Not worth the price'],
            1: ['Terrible product', 'Waste of money', 'Very disappointed', 'Do not recommend']
        }

        title = random.choice(review_texts[rating])

        reviews.append({
            'review_id': review_id,
            'product_id': product['product_id'],
            'customer_id': customer['customer_id'],
            'rating': rating,
            'title': title,
            'text': f"{title} - This {product['category'].lower()} product is {review_texts[rating][0].lower()}.",
            'helpful_votes': np.random.randint(0, 100),
            'verified_purchase': random.choice([True, True, True, False]),
            'review_date': (datetime(2022, 1, 1) + timedelta(days=random.randint(0, 1460))).isoformat()
        })
        review_id += 1

    return reviews

def generate_categories():
    """Generate hierarchical category structure"""
    log_progress("Generating category hierarchy...")

    categories = []
    for main_cat, subcats in CATEGORIES.items():
        categories.append({
            'id': main_cat.lower().replace(' ', '_'),
            'name': main_cat,
            'parent_id': None,
            'level': 0
        })

        for subcat in subcats:
            categories.append({
                'id': f"{main_cat.lower().replace(' ', '_')}_{subcat.lower().replace(' ', '_')}",
                'name': subcat,
                'parent_id': main_cat.lower().replace(' ', '_'),
                'level': 1
            })

    return categories

def save_as_csv(data, filename):
    """Save data as CSV"""
    if not data:
        return

    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(filepath, index=False)
    log_progress(f"Saved: {filename} ({len(df)} rows)")

def save_as_parquet(data, filename):
    """Save data as Parquet"""
    if not data:
        return

    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, filename)
    df.to_parquet(filepath, index=False)
    log_progress(f"Saved: {filename} ({len(df)} rows, Parquet format)")

def save_as_json(data, filename):
    """Save data as JSON"""
    if not data:
        return

    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    log_progress(f"Saved: {filename} ({len(data)} records)")

def generate_readme():
    """Generate README.md documentation"""
    readme_content = """# MegaStore E-Commerce Dataset

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
- **Generated**: """ + TIMESTAMP + """
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
"""

    filepath = os.path.join(OUTPUT_DIR, 'README.md')
    with open(filepath, 'w') as f:
        f.write(readme_content)
    log_progress("Saved: README.md")

def generate_mermaid_diagram():
    """Generate ER diagram in Mermaid format"""
    mermaid_content = """erDiagram
    CUSTOMERS ||--o{ ORDERS : places
    CUSTOMERS ||--o{ REVIEWS : writes
    PRODUCTS ||--o{ ORDER_ITEMS : "in orders"
    PRODUCTS ||--o{ REVIEWS : "reviewed in"
    PRODUCTS ||--o{ PRODUCT_RELATIONSHIPS : source
    PRODUCTS ||--o{ PRODUCT_RELATIONSHIPS : target
    PRODUCTS }o--|| SUPPLIERS : "supplied by"
    PRODUCTS }o--|| CATEGORIES : "belongs to"
    ORDERS ||--o{ ORDER_ITEMS : contains
    ORDERS ||--o{ CLICKSTREAM : "generated"
    CUSTOMERS ||--o{ CUSTOMER_RELATIONSHIPS : source
    CUSTOMERS ||--o{ CUSTOMER_RELATIONSHIPS : target
    CLICKSTREAM }o--|| PRODUCTS : "views"

    CUSTOMERS {
        int customer_id PK
        string first_name
        string last_name
        string email UK
        int age
        string gender
        string city
        string postal_code
        string country
        date registration_date
        string customer_segment
        decimal lifetime_value
        int total_orders
        string preferred_payment
    }

    PRODUCTS {
        int product_id PK
        string name
        string description
        string category
        string subcategory
        string brand
        decimal price
        decimal cost_price
        decimal weight_kg
        decimal rating_avg
        int rating_count
        boolean in_stock
        int stock_quantity
        int supplier_id FK
        array tags
        datetime created_at
    }

    SUPPLIERS {
        int supplier_id PK
        string company_name
        string contact_person
        string email
        string city
        string country
        int product_count
        int avg_delivery_days
        decimal rating
    }

    CATEGORIES {
        string id PK
        string name
        string parent_id FK
        int level
    }

    ORDERS {
        int order_id PK
        int customer_id FK
        datetime order_date
        string status
        decimal total_amount
        decimal discount_amount
        decimal shipping_cost
        string payment_method
        string shipping_city
        int delivery_days
    }

    ORDER_ITEMS {
        int item_id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
        decimal total_price
        decimal discount_percent
    }

    REVIEWS {
        int review_id PK
        int product_id FK
        int customer_id FK
        int rating
        string title
        string text
        int helpful_votes
        boolean verified_purchase
        datetime review_date
    }

    CLICKSTREAM {
        int event_id PK
        string session_id
        int customer_id FK "nullable"
        datetime timestamp
        string event_type
        string page_url
        int product_id FK "nullable"
        string device_type
        string browser
        string referrer_source
    }

    PRODUCT_RELATIONSHIPS {
        int source_product_id FK
        int target_product_id FK
        string relationship_type
    }

    CUSTOMER_RELATIONSHIPS {
        int source_customer_id FK
        int target_customer_id FK
        string relationship_type
    }
"""

    filepath = os.path.join(OUTPUT_DIR, 'data_model.mermaid')
    with open(filepath, 'w') as f:
        f.write(mermaid_content)
    log_progress("Saved: data_model.mermaid")

def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("MegaStore E-Commerce Dataset Generator")
    print("="*80 + "\n")

    log_progress(f"Output directory: {OUTPUT_DIR}")
    log_progress("Starting data generation...\n")

    # Generate all data
    suppliers = generate_suppliers(200)
    products = generate_products(suppliers, 5000)
    customers = generate_customers(50000)
    orders = generate_orders(customers, 500000)
    order_items = generate_order_items(orders, products)
    product_relationships = generate_product_relationships(products, 20000)
    customer_relationships = generate_customer_relationships(customers, 30000)
    clickstream = generate_clickstream(customers, products, 200000)
    reviews = generate_reviews(customers, products, 100000)
    categories = generate_categories()

    print("\n" + "-"*80)
    log_progress("Saving datasets...\n")
    print("-"*80 + "\n")

    # Save products
    save_as_csv(products, 'products.csv')
    save_as_json(products, 'products.json')

    # Save customers
    save_as_csv(customers, 'customers.csv')
    save_as_json(customers, 'customers.json')

    # Save orders
    save_as_csv(orders, 'orders.csv')
    save_as_parquet(orders, 'orders.parquet')
    save_as_json(orders[:1000], 'orders_sample.json')  # Sample for MongoDB

    # Save order items
    save_as_csv(order_items, 'order_items.csv')
    save_as_parquet(order_items, 'order_items.parquet')

    # Save relationships
    save_as_csv(product_relationships, 'product_relationships.csv')
    save_as_csv(customer_relationships, 'customer_relationships.csv')

    # Save clickstream
    save_as_csv(clickstream, 'clickstream.csv')
    save_as_parquet(clickstream, 'clickstream.parquet')

    # Save reviews
    save_as_csv(reviews, 'reviews.csv')
    save_as_json(reviews, 'reviews.json')

    # Save categories and suppliers
    save_as_json(categories, 'categories.json')
    save_as_csv(suppliers, 'suppliers.csv')
    save_as_json(suppliers, 'suppliers.json')

    # Generate documentation
    print("\n" + "-"*80)
    log_progress("Generating documentation...\n")
    print("-"*80 + "\n")

    generate_readme()
    generate_mermaid_diagram()

    print("\n" + "="*80)
    log_progress("DATA GENERATION COMPLETE!")
    print("="*80)

    print(f"\nDataset Summary:")
    print(f"  Products:              {len(products):>10,}")
    print(f"  Customers:             {len(customers):>10,}")
    print(f"  Orders:                {len(orders):>10,}")
    print(f"  Order Items:           {len(order_items):>10,}")
    print(f"  Clickstream Events:    {len(clickstream):>10,}")
    print(f"  Reviews:               {len(reviews):>10,}")
    print(f"  Product Relationships: {len(product_relationships):>10,}")
    print(f"  Customer Relationships:{len(customer_relationships):>10,}")
    print(f"  Suppliers:             {len(suppliers):>10,}")
    print(f"  Categories:            {len(categories):>10,}")
    print(f"\nTotal Records:         {len(products) + len(customers) + len(orders) + len(order_items) + len(clickstream) + len(reviews):>10,}")
    print(f"\nOutput Location: {OUTPUT_DIR}\n")

    # List all generated files
    print("Generated Files:")
    for filename in sorted(os.listdir(OUTPUT_DIR)):
        filepath = os.path.join(OUTPUT_DIR, filename)
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"  ✓ {filename:<40} ({size_mb:>6.2f} MB)")

    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    main()
