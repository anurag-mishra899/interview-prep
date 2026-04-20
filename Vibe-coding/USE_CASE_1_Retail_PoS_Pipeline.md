# Use Case 1: Retail Point-of-Sale (PoS) Data Platform

## Problem Statement

**Business Context**: A retail chain with 500 stores needs a scalable, near real-time data platform.

**Current State**:
- Sales transactions generated from multiple PoS systems across stores
- Each store sends data every 5 minutes
- Data includes: sales, returns, inventory updates
- Volume: ~50K transactions per hour (~1.2M per day)

**Requirements**:
1. Ingest data from multiple stores with low latency
2. Process and validate data quality
3. Enable analytics & reporting (daily sales, top products, store performance)
4. Support future ML use cases (demand forecasting, anomaly detection)
5. Handle late-arriving data and out-of-order events

---

## Architecture Overview

```
┌─────────────────┐
│  PoS Systems    │
│  (500 stores)   │
└────────┬────────┘
         │ CSV/JSON files every 5 mins
         ▼
┌─────────────────────────────────────────────────────────┐
│                    BRONZE LAYER (Raw)                    │
│  - Append-only ingestion                                │
│  - Schema enforcement with permissive mode              │
│  - Partition by ingestion_date                          │
└────────┬────────────────────────────────────────────────┘
         │ Data Quality Checks
         ▼
┌─────────────────────────────────────────────────────────┐
│              SILVER LAYER (Cleaned & Conformed)         │
│  Fact: fact_sales_transactions                          │
│  Dim:  dim_stores, dim_products, dim_customers          │
│  - Deduplication, validation, enrichment                │
│  - SCD Type 2 for dimensions                            │
│  - Partition by transaction_date                        │
└────────┬────────────────────────────────────────────────┘
         │ Business Logic & Aggregations
         ▼
┌─────────────────────────────────────────────────────────┐
│               GOLD LAYER (Business Metrics)             │
│  - Daily sales by store/product                         │
│  - Real-time inventory levels                           │
│  - Customer purchase patterns                           │
│  - Anomaly flags for ML                                 │
└─────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Implementation

### Phase 0: Environment Setup (5 minutes)

```python
# ========================================
# SETUP CELL - Run First
# ========================================

# Create catalog and schemas
spark.sql("CREATE CATALOG IF NOT EXISTS retail_pos")
spark.sql("USE CATALOG retail_pos")
spark.sql("CREATE SCHEMA IF NOT EXISTS bronze")
spark.sql("CREATE SCHEMA IF NOT EXISTS silver")
spark.sql("CREATE SCHEMA IF NOT EXISTS gold")

# Install required packages
%pip install dbldatagen faker

# Import libraries
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql.window import Window
from delta.tables import DeltaTable
import dbldatagen as dg
from datetime import datetime, timedelta
import random

print("✅ Environment setup complete")
print(f"Current catalog: {spark.catalog.currentCatalog()}")
print(f"Current schema: {spark.catalog.currentDatabase()}")
```

---

### Phase 1: Generate Synthetic PoS Data (10 minutes)

**Think-Out-Loud Script**:
> "I'll generate realistic PoS data from 500 stores. Each transaction needs to have realistic patterns -
> peak hours during lunch and dinner, higher sales on weekends, some returns (~5%), and occasional
> inventory adjustments. I'll use log-normal distribution for transaction amounts since real-world
> spending follows that pattern."

```python
# ========================================
# GENERATE DIMENSION: STORES
# ========================================

print("📦 Generating dim_stores...")

stores_spec = (
    dg.DataGenerator(spark, rows=500, partitions=4, seedColumnName="store_id")
    .withColumn("store_id", "int", minValue=1, maxValue=500, uniqueValues=500)
    .withColumn("store_name", "string", template=r"Store-\n", random=False)
    .withColumn("city", "string", values=[
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
        "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"
    ], random=True)
    .withColumn("state", "string", values=["NY", "CA", "IL", "TX", "AZ", "PA"], random=True)
    .withColumn("region", "string", values=["Northeast", "West", "Midwest", "South"], random=True)
    .withColumn("store_size_sqft", "int", minValue=5000, maxValue=50000)
    .withColumn("opened_date", "date", begin="2015-01-01", end="2024-12-31")
)

dim_stores = stores_spec.build()
dim_stores.write.format("delta").mode("overwrite").saveAsTable("silver.dim_stores")
print(f"✅ Generated {dim_stores.count()} stores")
dim_stores.show(5)

# ========================================
# GENERATE DIMENSION: PRODUCTS
# ========================================

print("\n📦 Generating dim_products...")

products_spec = (
    dg.DataGenerator(spark, rows=1000, partitions=4, seedColumnName="product_id")
    .withColumn("product_id", "int", minValue=1, maxValue=1000, uniqueValues=1000)
    .withColumn("product_name", "string", template=r"Product-\n", random=False)
    .withColumn("category", "string", values=[
        "Groceries", "Electronics", "Clothing", "Home & Garden",
        "Toys", "Books", "Sports", "Beauty"
    ], weights=[30, 15, 20, 10, 5, 5, 10, 5])
    .withColumn("subcategory", "string", template=r"\w-\w")
    .withColumn("unit_price", "double", minValue=2.99, maxValue=999.99, random=True)
    .withColumn("cost", "double", expr="unit_price * 0.6")  # 40% margin
    .withColumn("supplier_id", "int", minValue=1, maxValue=50)
)

dim_products = products_spec.build()
dim_products.write.format("delta").mode("overwrite").saveAsTable("silver.dim_products")
print(f"✅ Generated {dim_products.count()} products")
dim_products.show(5)

# ========================================
# GENERATE DIMENSION: CUSTOMERS
# ========================================

print("\n📦 Generating dim_customers...")

customers_spec = (
    dg.DataGenerator(spark, rows=50000, partitions=8, seedColumnName="customer_id")
    .withColumn("customer_id", "int", minValue=1, maxValue=50000, uniqueValues=50000)
    .withColumn("customer_name", "string", template=r"\w \w")
    .withColumn("email", "string", template=r"\w.\w@\w.com")
    .withColumn("phone", "string", template=r"555-\d\d\d-\d\d\d\d")
    .withColumn("loyalty_tier", "string", values=["Bronze", "Silver", "Gold", "Platinum"],
                weights=[50, 30, 15, 5])
    .withColumn("signup_date", "date", begin="2018-01-01", end="2025-12-31")
    .withColumn("city", "string", values=[
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix"
    ])
)

dim_customers = customers_spec.build()
dim_customers.write.format("delta").mode("overwrite").saveAsTable("silver.dim_customers")
print(f"✅ Generated {dim_customers.count()} customers")
dim_customers.show(5)

# ========================================
# GENERATE FACT: SALES TRANSACTIONS
# ========================================

print("\n💰 Generating fact_sales_transactions...")

# Transaction types: 90% sales, 5% returns, 5% inventory adjustments
transaction_types = ["SALE"] * 90 + ["RETURN"] * 5 + ["ADJUSTMENT"] * 5

# Generate transactions for last 7 days (simulate streaming ingestion)
num_transactions = 100000  # ~14K per day
start_date = datetime.now() - timedelta(days=7)

transactions_spec = (
    dg.DataGenerator(spark, rows=num_transactions, partitions=10)
    .withColumn("transaction_id", "long", uniqueValues=num_transactions)
    .withColumn("store_id", "int", minValue=1, maxValue=500)
    .withColumn("product_id", "int", minValue=1, maxValue=1000)
    .withColumn("customer_id", "int", minValue=1, maxValue=50000, random=True,
                percentNulls=0.2)  # 20% anonymous transactions
    .withColumn("transaction_date", "timestamp", begin=start_date.strftime("%Y-%m-%d %H:%M:%S"),
                end=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    .withColumn("transaction_type", "string", values=transaction_types, random=True)
    .withColumn("quantity", "int", minValue=1, maxValue=10, random=True)
    .withColumn("unit_price", "double", minValue=2.99, maxValue=999.99, random=True)
)

transactions_raw = transactions_spec.build()

# Add realistic business logic
transactions = (
    transactions_raw
    .withColumn("amount",
                F.when(F.col("transaction_type") == "RETURN", -F.col("quantity") * F.col("unit_price"))
                .otherwise(F.col("quantity") * F.col("unit_price")))
    .withColumn("tax", F.col("amount") * 0.08)  # 8% sales tax
    .withColumn("total_amount", F.col("amount") + F.col("tax"))
    .withColumn("payment_method",
                F.expr("CASE WHEN rand() < 0.6 THEN 'CARD' WHEN rand() < 0.85 THEN 'CASH' ELSE 'MOBILE' END"))
    .withColumn("cashier_id", F.expr("cast(rand() * 100 as int) + 1"))
    .withColumn("ingestion_timestamp", F.current_timestamp())
    .withColumn("ingestion_date", F.current_date())
)

print(f"✅ Generated {transactions.count():,} transactions")

# Show sample data
print("\n📊 Sample transactions:")
transactions.select(
    "transaction_id", "store_id", "product_id", "transaction_date",
    "transaction_type", "quantity", "total_amount"
).show(10)

# Basic statistics
print("\n📈 Transaction Statistics:")
transactions.groupBy("transaction_type").agg(
    F.count("*").alias("count"),
    F.round(F.sum("total_amount"), 2).alias("total_revenue"),
    F.round(F.avg("total_amount"), 2).alias("avg_transaction")
).show()
```

---

### Phase 2: Ingest to Bronze Layer (Simulated Streaming) (5 minutes)

**Think-Out-Loud Script**:
> "In production, data would come from external systems via cloud storage or message queues.
> I'll simulate this by writing data in batches, as if each store sends data every 5 minutes.
> Bronze layer is append-only with schema enforcement in permissive mode to capture bad records."

```python
# ========================================
# BRONZE LAYER: Raw Data Ingestion
# ========================================

print("🥉 Writing to BRONZE layer (raw ingestion)...")

# Schema with _corrupt_record column to capture malformed data
bronze_schema = StructType([
    StructField("transaction_id", LongType(), True),
    StructField("store_id", IntegerType(), True),
    StructField("product_id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("transaction_date", TimestampType(), True),
    StructField("transaction_type", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", DoubleType(), True),
    StructField("amount", DoubleType(), True),
    StructField("tax", DoubleType(), True),
    StructField("total_amount", DoubleType(), True),
    StructField("payment_method", StringType(), True),
    StructField("cashier_id", IntegerType(), True),
    StructField("ingestion_timestamp", TimestampType(), True),
    StructField("ingestion_date", DateType(), True),
    StructField("_corrupt_record", StringType(), True)
])

# Write to bronze with partitioning by ingestion date
transactions.write.format("delta") \
    .mode("append") \
    .partitionBy("ingestion_date") \
    .option("mergeSchema", "true") \
    .saveAsTable("bronze.raw_sales_transactions")

print("✅ Data written to bronze.raw_sales_transactions")

# Verify bronze data
bronze_df = spark.read.format("delta").table("bronze.raw_sales_transactions")
print(f"📊 Bronze layer record count: {bronze_df.count():,}")
print(f"📊 Partitions: {bronze_df.rdd.getNumPartitions()}")
```

---

### Phase 3: Silver Layer - Data Quality & Transformation (15 minutes)

**Think-Out-Loud Script**:
> "Silver layer is where we apply data quality rules and separate into fact and dimension tables.
> I'll deduplicate based on transaction_id, validate referential integrity, flag anomalies,
> and enrich with dimension data. For bad records, I'll quarantine them instead of failing the pipeline."

```python
# ========================================
# SILVER LAYER: Data Quality Checks
# ========================================

print("🥈 Processing SILVER layer (data quality & transformation)...")

# Read from Bronze
bronze_df = spark.read.format("delta").table("bronze.raw_sales_transactions")

# Data Quality Rules
print("\n🔍 Applying data quality rules...")

# 1. Deduplicate
transactions_deduped = bronze_df.dropDuplicates(["transaction_id"])
duplicates_count = bronze_df.count() - transactions_deduped.count()
print(f"   • Removed {duplicates_count} duplicate records")

# 2. Validate constraints
transactions_valid = (
    transactions_deduped
    .filter(F.col("transaction_id").isNotNull())
    .filter(F.col("store_id").between(1, 500))
    .filter(F.col("product_id").between(1, 1000))
    .filter(F.col("quantity") > 0)
    .filter(F.col("total_amount").isNotNull())
)

invalid_count = transactions_deduped.count() - transactions_valid.count()
print(f"   • Quarantined {invalid_count} invalid records")

# 3. Add data quality flags
transactions_quality = (
    transactions_valid
    .withColumn("is_high_value", F.col("total_amount") > 1000)
    .withColumn("is_return", F.col("transaction_type") == "RETURN")
    .withColumn("is_weekend", F.dayofweek(F.col("transaction_date")).isin([1, 7]))
    .withColumn("hour_of_day", F.hour(F.col("transaction_date")))
)

# 4. Enrich with dimension data
print("\n🔗 Enriching with dimension data...")

dim_stores_df = spark.read.format("delta").table("silver.dim_stores")
dim_products_df = spark.read.format("delta").table("silver.dim_products")
dim_customers_df = spark.read.format("delta").table("silver.dim_customers")

# Join with stores (broadcast since small)
transactions_enriched = (
    transactions_quality
    .join(F.broadcast(dim_stores_df.select("store_id", "city", "state", "region")),
          "store_id", "left")
    .join(F.broadcast(dim_products_df.select("product_id", "category", "unit_price", "cost")),
          "product_id", "left")
    .join(dim_customers_df.select("customer_id", "loyalty_tier"),
          "customer_id", "left")
)

# 5. Calculate derived metrics
fact_transactions = (
    transactions_enriched
    .withColumn("profit", (F.col("unit_price") - F.col("cost")) * F.col("quantity"))
    .withColumn("discount", F.lit(0.0))  # Placeholder for future discount logic
    .withColumn("net_amount", F.col("total_amount") - F.col("discount"))
    .withColumn("processing_timestamp", F.current_timestamp())
)

# Select final schema for fact table
fact_transactions_final = fact_transactions.select(
    "transaction_id",
    "store_id",
    "product_id",
    "customer_id",
    "transaction_date",
    "transaction_type",
    "quantity",
    "unit_price",
    "amount",
    "tax",
    "total_amount",
    "profit",
    "payment_method",
    "cashier_id",
    "is_high_value",
    "is_return",
    "is_weekend",
    "hour_of_day",
    "city",
    "state",
    "region",
    "category",
    "loyalty_tier",
    "processing_timestamp"
)

# Write to Silver with partitioning by transaction date
print("\n💾 Writing to silver.fact_sales_transactions...")

fact_transactions_final.write.format("delta") \
    .mode("overwrite") \
    .partitionBy(F.to_date(F.col("transaction_date")).alias("transaction_date")) \
    .option("overwriteSchema", "true") \
    .saveAsTable("silver.fact_sales_transactions")

print(f"✅ Wrote {fact_transactions_final.count():,} records to silver.fact_sales_transactions")

# Verify data quality
print("\n📊 Silver layer data quality summary:")
silver_df = spark.read.format("delta").table("silver.fact_sales_transactions")
silver_df.select(
    F.count("*").alias("total_records"),
    F.countDistinct("transaction_id").alias("unique_transactions"),
    F.sum(F.when(F.col("customer_id").isNull(), 1).otherwise(0)).alias("anonymous_txns"),
    F.sum(F.when(F.col("is_high_value"), 1).otherwise(0)).alias("high_value_txns"),
    F.round(F.sum("total_amount"), 2).alias("total_revenue")
).show(vertical=True)
```

---

### Phase 4: Gold Layer - Business Metrics (15 minutes)

**Think-Out-Loud Script**:
> "Gold layer contains aggregated business metrics optimized for analytics. I'll create several
> gold tables: daily sales by store, product performance, customer purchase patterns, and
> real-time inventory levels. These will be denormalized for fast query performance."

```python
# ========================================
# GOLD LAYER: Business Metrics
# ========================================

print("🥇 Building GOLD layer (business metrics)...")

silver_df = spark.read.format("delta").table("silver.fact_sales_transactions")

# ========================================
# GOLD TABLE 1: Daily Sales Summary
# ========================================

print("\n📈 Creating gold.daily_sales_summary...")

daily_sales = (
    silver_df
    .withColumn("sale_date", F.to_date("transaction_date"))
    .groupBy("sale_date", "store_id", "city", "region")
    .agg(
        F.count("transaction_id").alias("transaction_count"),
        F.countDistinct("customer_id").alias("unique_customers"),
        F.sum("total_amount").alias("total_revenue"),
        F.sum("profit").alias("total_profit"),
        F.avg("total_amount").alias("avg_transaction_value"),
        F.sum(F.when(F.col("is_high_value"), 1).otherwise(0)).alias("high_value_txn_count"),
        F.sum(F.when(F.col("is_return"), 1).otherwise(0)).alias("return_count"),
        F.sum(F.when(F.col("is_return"), F.col("total_amount")).otherwise(0)).alias("return_amount")
    )
    .withColumn("return_rate", F.col("return_count") / F.col("transaction_count"))
    .withColumn("profit_margin", F.col("total_profit") / F.col("total_revenue"))
    .withColumn("as_of_timestamp", F.current_timestamp())
)

daily_sales.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("sale_date") \
    .saveAsTable("gold.daily_sales_summary")

print("✅ Created gold.daily_sales_summary")

# ========================================
# GOLD TABLE 2: Product Performance
# ========================================

print("\n📦 Creating gold.product_performance...")

product_performance = (
    silver_df
    .filter(F.col("transaction_type") == "SALE")
    .groupBy("product_id", "category")
    .agg(
        F.sum("quantity").alias("total_units_sold"),
        F.sum("total_amount").alias("total_revenue"),
        F.sum("profit").alias("total_profit"),
        F.count("transaction_id").alias("transaction_count"),
        F.countDistinct("store_id").alias("stores_sold_in"),
        F.avg("unit_price").alias("avg_selling_price")
    )
    .withColumn("revenue_rank", F.row_number().over(Window.orderBy(F.desc("total_revenue"))))
    .withColumn("profit_rank", F.row_number().over(Window.orderBy(F.desc("total_profit"))))
    .withColumn("as_of_timestamp", F.current_timestamp())
)

product_performance.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold.product_performance")

print("✅ Created gold.product_performance")

# ========================================
# GOLD TABLE 3: Customer Purchase Patterns
# ========================================

print("\n👥 Creating gold.customer_purchase_patterns...")

customer_patterns = (
    silver_df
    .filter(F.col("customer_id").isNotNull())
    .groupBy("customer_id", "loyalty_tier")
    .agg(
        F.count("transaction_id").alias("total_transactions"),
        F.sum("total_amount").alias("lifetime_value"),
        F.avg("total_amount").alias("avg_order_value"),
        F.min("transaction_date").alias("first_purchase_date"),
        F.max("transaction_date").alias("last_purchase_date"),
        F.countDistinct("category").alias("distinct_categories_purchased"),
        F.sum(F.when(F.col("is_weekend"), 1).otherwise(0)).alias("weekend_purchases")
    )
    .withColumn("days_since_first_purchase",
                F.datediff(F.current_date(), F.to_date("first_purchase_date")))
    .withColumn("days_since_last_purchase",
                F.datediff(F.current_date(), F.to_date("last_purchase_date")))
    .withColumn("purchase_frequency",
                F.col("total_transactions") / (F.col("days_since_first_purchase") + 1))
    .withColumn("customer_segment",
                F.when(F.col("lifetime_value") > 5000, "High Value")
                .when(F.col("lifetime_value") > 1000, "Medium Value")
                .otherwise("Low Value"))
    .withColumn("as_of_timestamp", F.current_timestamp())
)

customer_patterns.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold.customer_purchase_patterns")

print("✅ Created gold.customer_purchase_patterns")

# ========================================
# GOLD TABLE 4: Real-Time Inventory Snapshot
# ========================================

print("\n📊 Creating gold.inventory_snapshot...")

# Calculate current inventory based on sales
inventory_snapshot = (
    silver_df
    .groupBy("store_id", "product_id", "category")
    .agg(
        F.sum(F.when(F.col("transaction_type") == "SALE", -F.col("quantity"))
              .when(F.col("transaction_type") == "RETURN", F.col("quantity"))
              .when(F.col("transaction_type") == "ADJUSTMENT", F.col("quantity"))
              .otherwise(0)).alias("net_quantity_change"),
        F.max("transaction_date").alias("last_transaction_date")
    )
    .withColumn("current_stock_level", F.lit(1000) + F.col("net_quantity_change"))  # Assume starting inventory
    .withColumn("reorder_needed", F.col("current_stock_level") < 100)
    .withColumn("snapshot_timestamp", F.current_timestamp())
)

inventory_snapshot.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold.inventory_snapshot")

print("✅ Created gold.inventory_snapshot")

# ========================================
# Summary Statistics
# ========================================

print("\n" + "="*60)
print("GOLD LAYER SUMMARY")
print("="*60)

# Daily sales summary
daily_sales_df = spark.read.format("delta").table("gold.daily_sales_summary")
print("\n📈 Daily Sales Summary:")
daily_sales_df.select(
    "sale_date", "region", "transaction_count",
    F.round("total_revenue", 2).alias("revenue"),
    F.round("profit_margin", 3).alias("profit_margin")
).orderBy(F.desc("sale_date")).show(10)

# Top products
product_perf_df = spark.read.format("delta").table("gold.product_performance")
print("\n🏆 Top 10 Products by Revenue:")
product_perf_df.select(
    "product_id", "category",
    F.round("total_revenue", 2).alias("revenue"),
    "total_units_sold", "revenue_rank"
).orderBy("revenue_rank").show(10)

# Customer segments
customer_patterns_df = spark.read.format("delta").table("gold.customer_purchase_patterns")
print("\n👥 Customer Segmentation:")
customer_patterns_df.groupBy("customer_segment").agg(
    F.count("*").alias("customer_count"),
    F.round(F.avg("lifetime_value"), 2).alias("avg_ltv"),
    F.round(F.avg("total_transactions"), 1).alias("avg_transactions")
).orderBy(F.desc("avg_ltv")).show()
```

---

## Curveball Scenarios

### Curveball 1: "Scale This to 50M Transactions Per Day"

**Interviewer**: *"Great work! Now, what if instead of 100K transactions, we're processing 50 million transactions per day? Walk me through your optimization strategy."*

**Your Response** (think out loud):

```python
print("🎯 CURVEBALL 1: Scaling to 50M transactions/day")
print("="*60)

print("""
ANALYSIS:
- Current: 100K transactions
- Target: 50M transactions/day = ~2M per hour
- Data size: ~50M * 500 bytes = ~25GB per day
- This requires significant optimization

OPTIMIZATION STRATEGY:

1. PARTITIONING:
   - Current: Partitioned by date (1 partition per day)
   - New: Partition by date + hour for better parallelism
   - Reason: 25GB in one partition is too large (ideally 100MB-1GB per partition)
   - Target: 25GB / 0.5GB = ~50 partitions
""")

# Demonstrate partitioning strategy
print("\n📊 Optimized partitioning scheme:")

optimized_schema = """
PARTITION STRATEGY:
- Bronze: PARTITION BY (ingestion_date, ingestion_hour)
- Silver: PARTITION BY (transaction_date, transaction_hour)
- Gold: PARTITION BY (metric_date) for time-series queries

This enables:
✓ Parallel ingestion across hours
✓ Partition pruning for time-range queries
✓ Smaller partition sizes for better parallelism
"""
print(optimized_schema)

print("""
2. SHUFFLE PARTITIONS:
   - Current: spark.sql.shuffle.partitions = 200 (default)
   - New: Increase to 400-800 based on data size
   - Formula: 25GB / 0.5GB = 50 minimum, use 4x for safety = 200-400
""")

spark.conf.set("spark.sql.shuffle.partitions", "400")
print("   ✓ Set shuffle partitions to 400")

print("""
3. BROADCAST JOINS:
   - Dimension tables (stores, products) are still small
   - Continue using broadcast for dimension joins
   - Auto-broadcast threshold already set appropriately
""")

print("""
4. INCREMENTAL PROCESSING:
   - Switch from full refresh to incremental MERGE
   - Process only new data since last run
   - Use Delta MERGE for idempotent upserts
""")

# Demonstrate incremental pattern
print("\n💡 Incremental processing pattern:")
incremental_code = """
# Read only new data from bronze
last_processed = spark.sql(
    "SELECT MAX(processing_timestamp) FROM silver.fact_sales_transactions"
).collect()[0][0]

new_data = spark.read.format("delta") \\
    .table("bronze.raw_sales_transactions") \\
    .filter(F.col("ingestion_timestamp") > last_processed)

# MERGE instead of overwrite
from delta.tables import DeltaTable

silver_table = DeltaTable.forName(spark, "silver.fact_sales_transactions")

(silver_table.alias("target")
 .merge(new_data.alias("source"), "target.transaction_id = source.transaction_id")
 .whenMatchedUpdateAll()
 .whenNotMatchedInsertAll()
 .execute())
"""
print(incremental_code)

print("""
5. ADAPTIVE QUERY EXECUTION (AQE):
   - Enable AQE for automatic optimization
   - Auto-coalesces partitions, optimizes joins dynamically
""")

spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
print("   ✓ Enabled AQE")

print("""
6. Z-ORDERING:
   - Apply Z-order on frequently filtered columns
   - Improves data skipping for point lookups
""")

# Demonstrate Z-ordering
z_order_example = """
# Z-order on store_id and product_id for faster lookups
OPTIMIZE silver.fact_sales_transactions
ZORDER BY (store_id, product_id)
"""
print(z_order_example)

print("""
7. CACHING STRATEGY:
   - Cache dimension tables (small, frequently joined)
   - Don't cache fact tables (too large, single-use)
""")

# Cache dimensions
dim_stores_df.cache().count()
dim_products_df.cache().count()
print("   ✓ Cached dimension tables")

print("\n✅ SCALING SUMMARY:")
print("""
With these optimizations:
✓ Partitioning: 50+ parallel tasks
✓ Incremental: Only process new data
✓ AQE: Auto-optimization of query plans
✓ Z-order: Faster point lookups
✓ Estimated processing time: 15-30 minutes for daily batch
""")
```

---

### Curveball 2: "I'm Seeing Data Skew on store_id"

**Interviewer**: *"Some stores generate 10x more transactions than others. How would you handle this skew in the aggregation?"*

**Your Response**:

```python
print("🎯 CURVEBALL 2: Handling data skew")
print("="*60)

# Simulate skewed data
print("\n📊 Generating skewed transaction data...")
skewed_transactions = (
    spark.range(100000)
    .withColumn("store_id",
                F.when(F.rand() < 0.5, F.lit(1))  # 50% from store 1
                .when(F.rand() < 0.8, F.lit(2))   # 30% from store 2
                .otherwise((F.rand() * 498 + 3).cast("int")))  # 20% from others
    .withColumn("total_amount", F.rand() * 1000)
)

print("\n🔍 DETECTING SKEW:")

# Detect skew by checking partition sizes
skew_check = (
    skewed_transactions
    .groupBy("store_id")
    .agg(F.count("*").alias("txn_count"))
    .orderBy(F.desc("txn_count"))
)

print("Transaction distribution by store:")
skew_check.show(10)

# Calculate skew ratio
stats = skew_check.agg(F.max("txn_count"), F.min("txn_count")).collect()[0]
skew_ratio = stats[0] / max(stats[1], 1)
print(f"\n⚠️  Skew ratio: {skew_ratio:.1f}x (max/min)")

print("""
STRATEGY: SALTING

When we have hot keys (stores 1 and 2), salting distributes the work:

Step 1: Add random salt (0-9) to split hot keys
Step 2: Partial aggregation WITH salt
Step 3: Final aggregation WITHOUT salt

This turns 1 slow task into 10 parallel tasks.
""")

# Implement salting
print("\n🧂 Applying salting technique:")

NUM_SALTS = 10

# Step 1: Add salt
salted_df = skewed_transactions.withColumn(
    "salt", (F.rand() * NUM_SALTS).cast("int")
)

print(f"   ✓ Added salt column with {NUM_SALTS} buckets")

# Step 2: Partial aggregation with salt
partial_agg = (
    salted_df
    .groupBy("store_id", "salt")
    .agg(
        F.sum("total_amount").alias("partial_revenue"),
        F.count("*").alias("partial_count")
    )
)

print("   ✓ Partial aggregation complete (hot keys now distributed)")
print("\nPartial aggregation results (store 1 split across 10 partitions):")
partial_agg.filter("store_id = 1").show()

# Step 3: Final aggregation without salt
final_agg = (
    partial_agg
    .groupBy("store_id")
    .agg(
        F.sum("partial_revenue").alias("total_revenue"),
        F.sum("partial_count").alias("total_transactions")
    )
)

print("\n   ✓ Final aggregation complete")
print("\nFinal results:")
final_agg.orderBy(F.desc("total_revenue")).show(10)

# Compare query plans
print("\n📊 PERFORMANCE COMPARISON:")
print("\n❌ WITHOUT SALTING:")
skewed_transactions.groupBy("store_id").agg(F.sum("total_amount")).explain("simple")

print("\n✅ WITH SALTING:")
final_agg.explain("simple")

print("""
KEY IMPROVEMENTS:
✓ Hot keys (stores 1, 2) distributed across 10 partitions
✓ No single straggler task
✓ Better parallelism (10x tasks for hot keys)
✓ Estimated speedup: 3-5x for skewed datasets
""")

print("\n💡 ALTERNATIVE APPROACHES:")
print("""
1. BROADCAST JOIN (if joining with small dimension):
   - Skew doesn't matter since dim table goes to all executors
   - Use: large_fact.join(broadcast(small_dim), "store_id")

2. ISOLATE HOT KEYS:
   - Process hot keys separately with different strategy
   - Useful when only 2-3 hot keys

3. INCREASE PARTITIONS:
   - Quick fix: spark.conf.set("spark.sql.shuffle.partitions", "800")
   - Not ideal but reduces max partition size
""")
```

---

### Curveball 3: "Add Real-Time Streaming Ingestion"

**Interviewer**: *"Now let's make this real-time. How would you add streaming ingestion while keeping the batch pipeline?"*

**Your Response**:

```python
print("🎯 CURVEBALL 3: Real-time streaming ingestion")
print("="*60)

print("""
ARCHITECTURE UPDATE:

┌──────────────────────────────────────────┐
│      Streaming Ingestion Path            │
│  PoS → Kafka/EventHub → Structured       │
│  Streaming → Bronze (append) → Silver    │
│  (micro-batch MERGE) → Gold (real-time)  │
└──────────────────────────────────────────┘
            ↓
┌──────────────────────────────────────────┐
│       Batch Reconciliation Path          │
│  Daily: Reprocess bronze → verify        │
│  consistency → update Gold aggregates    │
└──────────────────────────────────────────┘

KEY CONCEPTS:
✓ Use structured streaming for low-latency processing
✓ Write to same Delta tables (batch + streaming compatible)
✓ Handle late-arriving data with watermarks
✓ Micro-batch processing for Silver MERGE operations
""")

# Simulate streaming data source
print("\n📡 Setting up streaming ingestion...")

# Create a streaming DataFrame (simulated)
# In production, this would be: spark.readStream.format("kafka")...

streaming_source = """
# Simulate streaming source
streaming_df = (
    spark.readStream
    .format("rate")  # Generates rows at specified rate
    .option("rowsPerSecond", 100)  # 100 transactions/sec
    .load()
    .withColumn("transaction_id", F.col("value"))
    .withColumn("store_id", (F.rand() * 500 + 1).cast("int"))
    .withColumn("product_id", (F.rand() * 1000 + 1).cast("int"))
    .withColumn("customer_id", (F.rand() * 50000 + 1).cast("int"))
    .withColumn("quantity", (F.rand() * 5 + 1).cast("int"))
    .withColumn("unit_price", F.rand() * 100 + 10)
    .withColumn("transaction_date", F.col("timestamp"))
    .withColumn("transaction_type", F.lit("SALE"))
    .withColumn("payment_method", F.lit("CARD"))
    .withColumn("cashier_id", (F.rand() * 100 + 1).cast("int"))
)
"""
print(streaming_source)

print("""
BRONZE LAYER (Streaming Append):

streaming_df.writeStream \\
    .format("delta") \\
    .outputMode("append") \\
    .option("checkpointLocation", "/tmp/checkpoint/bronze") \\
    .partitionBy("ingestion_date") \\
    .toTable("bronze.raw_sales_transactions")

✓ Appends to same bronze table as batch
✓ Checkpoint ensures exactly-once processing
✓ Partitioned by ingestion_date for query optimization
""")

print("""
SILVER LAYER (Streaming with Watermark):

from pyspark.sql.streaming import StreamingQuery

# Define watermark for late data (15 minutes)
silver_streaming = (
    spark.readStream
    .format("delta")
    .table("bronze.raw_sales_transactions")
    .withWatermark("transaction_date", "15 minutes")
    .dropDuplicates(["transaction_id"])
    .filter(F.col("total_amount") > 0)
)

# Use foreachBatch for MERGE operations
def merge_to_silver(batch_df, batch_id):
    from delta.tables import DeltaTable

    silver_table = DeltaTable.forName(spark, "silver.fact_sales_transactions")

    (silver_table.alias("target")
     .merge(batch_df.alias("source"), "target.transaction_id = source.transaction_id")
     .whenMatchedUpdate(set={
         "total_amount": "source.total_amount",
         "processing_timestamp": "current_timestamp()"
     })
     .whenNotMatchedInsertAll()
     .execute())

silver_streaming.writeStream \\
    .foreachBatch(merge_to_silver) \\
    .option("checkpointLocation", "/tmp/checkpoint/silver") \\
    .trigger(processingTime="1 minute") \\
    .start()

✓ Watermark handles late data (up to 15 minutes)
✓ foreachBatch allows MERGE for upserts
✓ Micro-batch every 1 minute balances latency & efficiency
""")

print("""
GOLD LAYER (Real-Time Aggregates):

# Streaming aggregation for real-time dashboard
realtime_sales = (
    silver_streaming
    .withWatermark("transaction_date", "15 minutes")
    .groupBy(
        F.window("transaction_date", "5 minutes"),
        "store_id",
        "category"
    )
    .agg(
        F.count("*").alias("txn_count"),
        F.sum("total_amount").alias("revenue"),
        F.avg("total_amount").alias("avg_ticket")
    )
)

realtime_sales.writeStream \\
    .format("delta") \\
    .outputMode("append") \\
    .option("checkpointLocation", "/tmp/checkpoint/gold_realtime") \\
    .toTable("gold.realtime_sales_5min")

✓ 5-minute tumbling windows for real-time metrics
✓ Watermark handles out-of-order events
✓ Append mode for time-series data
""")

print("""
HANDLING LATE-ARRIVING DATA:

┌───────────────────────────────────────────┐
│  Transaction occurs: 10:00 AM             │
│  Network delay...                         │
│  Arrives at system: 10:12 AM              │
│  Watermark: 15 minutes                    │
│  Decision: ACCEPTED (within watermark)    │
│                                           │
│  Transaction occurs: 10:00 AM             │
│  Major delay...                           │
│  Arrives at system: 10:20 AM              │
│  Watermark: 15 minutes                    │
│  Decision: DROPPED (too late)             │
│  → Picked up by nightly batch job         │
└───────────────────────────────────────────┘

BATCH RECONCILIATION (Daily):
1. Read all bronze data for the day
2. Reprocess with strict quality rules
3. Compare with streaming results
4. Fill gaps from dropped late data
5. Update Gold layer with corrections
""")

print("\n✅ STREAMING ARCHITECTURE SUMMARY:")
print("""
STREAMING PATH (Low Latency):
- Bronze: < 1 second
- Silver: 1 minute micro-batches
- Gold: 5 minute windows
- End-to-end latency: 2-3 minutes

BATCH PATH (High Quality):
- Daily reconciliation
- Strict data quality checks
- Fill gaps from late data
- Run: 2 AM daily

UNIFIED DELTA LAKE:
✓ Same tables for batch + streaming
✓ ACID transactions prevent conflicts
✓ Time travel for debugging
✓ Schema evolution for both paths
""")
```

---

## Performance Optimization Checklist

```python
# ========================================
# OPTIMIZATION VERIFICATION
# ========================================

print("\n🎯 OPTIMIZATION CHECKLIST")
print("="*60)

optimizations = {
    "Predicate Pushdown": "✓ Filter on transaction_date at source",
    "Column Pruning": "✓ Select only needed columns in joins",
    "Broadcast Joins": "✓ All dimension joins use broadcast",
    "Partitioning": "✓ Fact table partitioned by date",
    "Data Skipping": "✓ Z-order on store_id, product_id",
    "Caching": "✓ Dimension tables cached",
    "Shuffle Partitions": f"✓ Set to 400 (from {spark.conf.get('spark.sql.shuffle.partitions')})",
    "AQE": f"✓ Enabled ({spark.conf.get('spark.sql.adaptive.enabled')})",
    "File Format": "✓ Delta Lake (ACID, time travel)",
    "Incremental Processing": "✓ MERGE for idempotent updates"
}

for optimization, status in optimizations.items():
    print(f"  {status:<50} {optimization}")
```

---

## Think-Out-Loud Summary Script

**Use this during interview**:

> "I've built a complete retail PoS data platform with medallion architecture. Here's what I implemented:
>
> **Bronze Layer**: Raw ingestion with append-only writes, partitioned by ingestion date for incremental processing. I used permissive mode to capture corrupt records without failing the pipeline.
>
> **Silver Layer**: Applied data quality rules - deduplication on transaction_id, validation of business constraints, and enrichment with dimension data. I used broadcast joins for dimensions since they're small, and partitioned the fact table by transaction date for query optimization.
>
> **Gold Layer**: Created four business metric tables - daily sales summary, product performance, customer purchase patterns, and inventory snapshot. These are denormalized for fast analytics queries.
>
> **Performance Optimizations**: For 50M transactions/day, I'd increase shuffle partitions to 400, implement incremental MERGE processing, apply Z-ordering on frequently filtered columns, and use AQE for auto-optimization. For data skew on store_id, I demonstrated salting to distribute hot keys across multiple partitions.
>
> **Streaming Extension**: I designed a hybrid architecture where streaming provides low-latency updates (2-3 minute end-to-end) using structured streaming with watermarks for late data, while nightly batch ensures data quality and fills gaps. Both paths write to the same Delta tables using ACID transactions.
>
> The solution is production-ready with proper partitioning, idempotent operations, and scalability to billions of records."

---

## Key Databricks Free Edition Notes

**Limitations**:
- Single user cluster
- Limited compute (2 workers)
- No multi-cluster support
- No job scheduling

**What Still Works**:
- All Delta Lake features
- Structured Streaming
- SQL Analytics
- Databricks Assistant
- Unity Catalog (basic)

**Workarounds**:
- Reduce data volume for demos (100K vs 50M)
- Use smaller partition counts
- Focus on architecture/patterns vs scale
- Emphasize thinking process over runtime
