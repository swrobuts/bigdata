#!/bin/bash
# MongoDB initialization script for MegaStore data
# This script runs automatically when the MongoDB container starts

set -e

echo "Starting MegaStore MongoDB initialization..."

# Wait for MongoDB to be ready
until mongosh --eval "db.adminCommand('ping')" --quiet; do
  echo "Waiting for MongoDB to be ready..."
  sleep 2
done

echo "MongoDB is ready. Importing data..."

# Create megastore database and import collections
MONGO_CMD="mongosh --quiet megastore"

# Import products collection
if [ -f "/data/megastore/products.json" ]; then
  echo "Importing products..."
  mongoimport --db megastore --collection products --file /data/megastore/products.json --jsonArray
fi

# Import customers collection
if [ -f "/data/megastore/customers.json" ]; then
  echo "Importing customers..."
  mongoimport --db megastore --collection customers --file /data/megastore/customers.json --jsonArray
fi

# Import orders collection
if [ -f "/data/megastore/orders_sample.json" ]; then
  echo "Importing orders..."
  mongoimport --db megastore --collection orders --file /data/megastore/orders_sample.json --jsonArray
fi

# Import reviews collection
if [ -f "/data/megastore/reviews.json" ]; then
  echo "Importing reviews..."
  mongoimport --db megastore --collection reviews --file /data/megastore/reviews.json --jsonArray
fi

# Import categories collection
if [ -f "/data/megastore/categories.json" ]; then
  echo "Importing categories..."
  mongoimport --db megastore --collection categories --file /data/megastore/categories.json --jsonArray
fi

# Import suppliers collection
if [ -f "/data/megastore/suppliers.json" ]; then
  echo "Importing suppliers..."
  mongoimport --db megastore --collection suppliers --file /data/megastore/suppliers.json --jsonArray
fi

# Create indexes for better query performance
$MONGO_CMD << EOF
db.products.createIndex({ product_id: 1 });
db.products.createIndex({ category: 1 });
db.customers.createIndex({ customer_id: 1 });
db.customers.createIndex({ email: 1 });
db.orders.createIndex({ order_id: 1 });
db.orders.createIndex({ customer_id: 1 });
db.reviews.createIndex({ product_id: 1 });
db.reviews.createIndex({ customer_id: 1 });
EOF

echo "MongoDB initialization complete!"
echo "Collections created:"
echo "  - products"
echo "  - customers"
echo "  - orders"
echo "  - reviews"
echo "  - categories"
echo "  - suppliers"
