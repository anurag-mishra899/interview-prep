# Data Engineering Mock Scenarios - Databricks Vibe Coding Round

**For Data Engineering Background Interviewers**

Based on: [Delta Live Tables](https://docs.databricks.com/delta-live-tables/), [Auto Loader](https://docs.databricks.com/ingestion/auto-loader/), [Unity Catalog](https://docs.databricks.com/data-governance/unity-catalog/), [Lakehouse Architecture](https://www.databricks.com/product/data-lakehouse)

---

## 🎯 Scenario 1: End-to-End Lakehouse Pipeline with CDC

### 📋 Context
**Interviewer**: *"We're building a data lakehouse for an e-commerce company. We have transactional data from PostgreSQL (orders, customers, products) that needs to be ingested incrementally, transformed through medallion layers, and made available for analytics and ML. Build the pipeline handling CDC, slowly changing dimensions, and data quality."*

---

### Expected Questions & Best Answers

#### Q1: "Design the end-to-end architecture"

**✅ BEST ANSWER** (2 minutes):
```
"I'll design a Medallion Architecture with three layers:

BRONZE LAYER (Raw/Landing):
- Ingest CDC events from PostgreSQL using Auto Loader
- Preserve raw data exactly as received
- Append-only for complete audit trail
- Partition by ingestion date for retention policies

SILVER LAYER (Cleaned/Conformed):
- Apply data quality rules and validation
- Deduplicate records
- Handle CDC operations (insert, update, delete)
- Implement SCD Type 2 for customer dimension
- Store in Delta format with ACID guarantees

GOLD LAYER (Business/Aggregated):
- Create fact tables (orders, line items)
- Maintain dimension tables (customers, products)
- Pre-aggregate for common analytics queries
- Power dashboards and ML feature engineering

ORCHESTRATION:
- Delta Live Tables for declarative pipeline definition
- Automated dependency management
- Data quality expectations with quarantine
- Auto-scaling compute

Let me build this step by step..."
```

---

#### Q2: "Implement Bronze layer with Auto Loader for CDC ingestion"

**✅ BEST ANSWER** (10 minutes hands-on):

```python
from pyspark.sql import functions as F
from pyspark.sql.types import *

print("=== BRONZE LAYER: CDC INGESTION WITH AUTO LOADER ===")

# THINK OUT LOUD:
# "Auto Loader incrementally ingests new files from cloud storage with
#  exactly-once processing guarantees. It's perfect for CDC files that
#  land continuously. I'll configure schema inference and rescue for
#  evolving schemas."

# 1. Generate synthetic CDC data files
print("1. Generating synthetic CDC files to simulate PostgreSQL exports...")

# Simulate CDC file format (Debezium-style)
cdc_schema = StructType([
    StructField("operation", StringType(), False),  # I, U, D (Insert, Update, Delete)
    StructField("timestamp", TimestampType(), False),
    StructField("table_name", StringType(), False),
    StructField("primary_key", IntegerType(), False),
    StructField("payload", StringType(), False)  # JSON payload
])

# Generate CDC events for Orders table
import json
from datetime import datetime, timedelta

def generate_cdc_batch(batch_num, num_records=1000):
    """Generate a batch of CDC records"""
    data = []
    base_time = datetime.now() - timedelta(hours=batch_num)

    for i in range(num_records):
        operation = "I" if i % 10 != 0 else "U"  # 90% inserts, 10% updates

        if batch_num == 0:  # First batch - all inserts
            operation = "I"

        payload = {
            "order_id": batch_num * num_records + i,
            "customer_id": (i % 10000) + 1,
            "product_id": (i % 1000) + 1,
            "quantity": (i % 10) + 1,
            "unit_price": round(10 + (i % 100), 2),
            "order_date": (base_time + timedelta(minutes=i)).isoformat(),
            "status": "pending" if i % 5 != 0 else "completed"
        }

        data.append((
            operation,
            base_time + timedelta(seconds=i),
            "orders",
            payload["order_id"],
            json.dumps(payload)
        ))

    return data

# Create sample CDC batches
print("Generating CDC batches...")
for batch in range(3):
    cdc_data = generate_cdc_batch(batch, 500)
    cdc_df = spark.createDataFrame(cdc_data, cdc_schema)

    # Write to cloud storage path (simulating PostgreSQL CDC export)
    output_path = f"/tmp/cdc_landing/batch_{batch}"
    cdc_df.write.mode("overwrite").parquet(output_path)
    print(f"✅ Batch {batch}: {cdc_df.count()} CDC records written to {output_path}")

# 2. Set up Auto Loader to read CDC files
print("\n2. Setting up Auto Loader for incremental ingestion...")

# THINK OUT LOUD:
# "Auto Loader automatically detects new files, infers schema, and handles
#  schema evolution. The 'cloudFiles' format provides exactly-once guarantees
#  and scalable file discovery even with millions of files."

landing_path = "/tmp/cdc_landing"
checkpoint_path = "/tmp/bronze_checkpoint"

# Auto Loader configuration
bronze_stream = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("cloudFiles.schemaLocation", checkpoint_path)
    .option("cloudFiles.inferColumnTypes", "true")
    .option("cloudFiles.schemaEvolutionMode", "rescue")  # Handle schema changes
    .load(landing_path)
)

# Add metadata columns
bronze_stream = bronze_stream \
    .withColumn("_ingestion_timestamp", F.current_timestamp()) \
    .withColumn("_source_file", F.input_file_name())

print("✅ Auto Loader configured")

# 3. Write to Bronze Delta table
print("\n3. Writing to Bronze layer (Delta)...")

# THINK OUT LOUD:
# "Bronze layer is append-only to preserve complete history. Partitioning
#  by ingestion date enables efficient retention policies and time-travel
#  queries. I'm adding metadata for lineage and debugging."

bronze_query = (
    bronze_stream
    .withColumn("_ingestion_date", F.to_date("_ingestion_timestamp"))
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", checkpoint_path + "/bronze")
    .partitionBy("_ingestion_date", "table_name")
    .trigger(processingTime="10 seconds")  # Micro-batch every 10 seconds
    .table("lakehouse.bronze_cdc")
)

print("✅ Bronze streaming query started")
print(f"   - Format: Delta")
print(f"   - Mode: Append-only")
print(f"   - Partitioned by: ingestion_date, table_name")
print(f"   - Trigger: 10-second micro-batches")

# Let it run for a bit
import time
time.sleep(15)

# 4. Validate Bronze ingestion
print("\n4. Validating Bronze layer...")

bronze_df = spark.read.format("delta").table("lakehouse.bronze_cdc")
print(f"Total records ingested: {bronze_df.count()}")

print("\nRecord counts by operation type:")
bronze_df.groupBy("operation").count().show()

print("\nSample records:")
bronze_df.select("operation", "timestamp", "table_name", "primary_key", "_ingestion_timestamp").show(5)

# 5. Explain the architecture
print("\n" + "="*70)
print("BRONZE LAYER ARCHITECTURE")
print("="*70)
print("""
CDC FILES (Landing Zone)
        ↓
AUTO LOADER (Incremental Discovery)
- Schema inference
- Exactly-once semantics
- Handles schema evolution
        ↓
BRONZE DELTA TABLE (Append-Only)
- Complete audit trail
- Partitioned by date + table
- Metadata for lineage
- Time-travel enabled

KEY BENEFITS:
✓ No data loss (append-only)
✓ Exactly-once processing (checkpointing)
✓ Schema evolution (rescue columns)
✓ Scalable (millions of files)
✓ Cost-efficient (auto-scaling, incremental)

RETENTION POLICY:
- Keep raw data for 90 days (compliance)
- Partition pruning for efficient deletion
- Delta vacuum after retention period
""")

# Stop the stream for demo
bronze_query.stop()
```

**THINK OUT LOUD EXPLANATION**:
"I'm using Auto Loader which is Databricks' optimized file ingestion engine. It scales to millions of files, automatically infers and evolves schemas, and provides exactly-once guarantees through checkpointing. The bronze layer is append-only to preserve the complete audit trail of all CDC events."

---

#### Q3: "Build Silver layer with CDC processing and data quality"

**✅ BEST ANSWER** (15 minutes hands-on):

```python
from delta.tables import DeltaTable
import dlt  # Delta Live Tables

print("=== SILVER LAYER: CDC PROCESSING + DATA QUALITY ===")

# THINK OUT LOUD:
# "Silver layer applies the CDC operations to create current-state tables.
#  I'll implement data quality checks, deduplication, and SCD Type 2 for
#  dimensions. Using Delta Live Tables for declarative definitions."

# 1. Define data quality expectations
print("1. Defining data quality expectations...")

# Using Delta Live Tables expectations
@dlt.table(
    name="silver_orders_quality_checked",
    comment="Orders with data quality validations applied",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_quantity", "quantity > 0")
@dlt.expect_or_drop("valid_price", "unit_price > 0")
@dlt.expect_or_quarantine("valid_customer", "customer_id IS NOT NULL",
                          "quarantine_orders")
@dlt.expect("valid_dates", "order_date <= current_date()")
def orders_quality_checks():
    """Apply CDC operations with quality checks"""

    # Read from Bronze
    bronze_orders = dlt.read_stream("lakehouse.bronze_cdc") \
        .filter("table_name = 'orders'")

    # Parse JSON payload
    bronze_orders = bronze_orders.withColumn(
        "data",
        F.from_json("payload", StructType([
            StructField("order_id", IntegerType()),
            StructField("customer_id", IntegerType()),
            StructField("product_id", IntegerType()),
            StructField("quantity", IntegerType()),
            StructField("unit_price", DoubleType()),
            StructField("order_date", TimestampType()),
            StructField("status", StringType())
        ]))
    )

    # Flatten and add metadata
    return bronze_orders.select(
        "data.*",
        F.col("operation").alias("_cdc_operation"),
        F.col("timestamp").alias("_cdc_timestamp"),
        F.col("_ingestion_timestamp")
    )

print("✅ Data quality expectations defined")

# 2. Implement CDC merge logic (without DLT for demo)
print("\n2. Implementing CDC merge logic...")

# Read Bronze CDC events
bronze_orders = spark.read.format("delta").table("lakehouse.bronze_cdc") \
    .filter("table_name = 'orders'")

# Parse JSON payload
from pyspark.sql.types import *

order_schema = StructType([
    StructField("order_id", IntegerType()),
    StructField("customer_id", IntegerType()),
    StructField("product_id", IntegerType()),
    StructField("quantity", IntegerType()),
    StructField("unit_price", DoubleType()),
    StructField("order_date", TimestampType()),
    StructField("status", StringType())
])

parsed_orders = bronze_orders.withColumn(
    "data", F.from_json("payload", order_schema)
).select(
    "operation",
    "timestamp",
    "data.*",
    "_ingestion_timestamp"
)

# Apply data quality filters
valid_orders = parsed_orders.filter(
    (F.col("quantity") > 0) &
    (F.col("unit_price") > 0) &
    (F.col("customer_id").isNotNull())
)

invalid_orders = parsed_orders.subtract(valid_orders)

print(f"Valid orders: {valid_orders.count()}")
print(f"Invalid orders: {invalid_orders.count()}")

# Quarantine invalid records
if invalid_orders.count() > 0:
    invalid_orders.write.format("delta") \
        .mode("append") \
        .saveAsTable("lakehouse.quarantine_orders")
    print("✅ Invalid records quarantined")

# 3. Apply CDC operations with MERGE
print("\n3. Applying CDC operations (INSERT, UPDATE, DELETE)...")

# THINK OUT LOUD:
# "I'm using Delta MERGE to apply CDC operations atomically. Inserts add
#  new records, Updates modify existing ones, and Deletes soft-delete by
#  setting an is_deleted flag. This maintains audit trail."

# Create target table if not exists
if not spark.catalog.tableExists("lakehouse.silver_orders"):
    valid_orders.limit(0) \
        .withColumn("is_deleted", F.lit(False)) \
        .withColumn("updated_at", F.current_timestamp()) \
        .write.format("delta").saveAsTable("lakehouse.silver_orders")
    print("✅ Created lakehouse.silver_orders table")

# Get latest CDC state per order (deduplicate)
latest_cdc = valid_orders \
    .withColumn("row_num",
                F.row_number().over(
                    Window.partitionBy("order_id").orderBy(F.desc("timestamp"))
                )) \
    .filter("row_num = 1") \
    .drop("row_num")

print(f"Deduplicated CDC events: {latest_cdc.count()}")

# Apply MERGE
target_table = DeltaTable.forName(spark, "lakehouse.silver_orders")

merge_result = (
    target_table.alias("target")
    .merge(
        latest_cdc.alias("source"),
        "target.order_id = source.order_id"
    )
    .whenMatchedUpdate(
        condition="source.operation = 'U'",
        set={
            "customer_id": "source.customer_id",
            "product_id": "source.product_id",
            "quantity": "source.quantity",
            "unit_price": "source.unit_price",
            "order_date": "source.order_date",
            "status": "source.status",
            "updated_at": "current_timestamp()",
            "is_deleted": "false"
        }
    )
    .whenMatchedUpdate(
        condition="source.operation = 'D'",
        set={
            "is_deleted": "true",
            "updated_at": "current_timestamp()"
        }
    )
    .whenNotMatchedInsert(
        condition="source.operation = 'I'",
        values={
            "order_id": "source.order_id",
            "customer_id": "source.customer_id",
            "product_id": "source.product_id",
            "quantity": "source.quantity",
            "unit_price": "source.unit_price",
            "order_date": "source.order_date",
            "status": "source.status",
            "is_deleted": "false",
            "updated_at": "current_timestamp()"
        }
    )
    .execute()
)

print("✅ CDC MERGE completed")
print(f"Rows affected: {merge_result}")

# 4. Validate Silver layer
print("\n4. Validating Silver layer...")

silver_orders = spark.read.format("delta").table("lakehouse.silver_orders")
print(f"Total orders: {silver_orders.count()}")
print(f"Active orders: {silver_orders.filter('is_deleted = false').count()}")
print(f"Deleted orders: {silver_orders.filter('is_deleted = true').count()}")

print("\nOrder status distribution:")
silver_orders.filter("is_deleted = false").groupBy("status").count().show()

# 5. Implement SCD Type 2 for Customer dimension
print("\n5. Implementing SCD Type 2 for Customer dimension...")

# THINK OUT LOUD:
# "SCD Type 2 maintains history by creating new records for changes and
#  marking old ones as inactive. Each version has effective_from/to dates
#  and is_current flag. This enables point-in-time queries."

# Simulate customer data with changes
customers_data = [
    (1, "Alice Johnson", "alice@email.com", "US", "2025-01-01"),
    (2, "Bob Smith", "bob@email.com", "UK", "2025-01-01"),
    (1, "Alice Johnson-Williams", "alice.new@email.com", "US", "2025-03-15"),  # Name/email change
]

customers_cdc = spark.createDataFrame(
    customers_data,
    ["customer_id", "name", "email", "country", "effective_date"]
).withColumn("effective_date", F.to_date("effective_date"))

# SCD Type 2 merge logic
scd_columns = ["customer_id", "name", "email", "country"]

def apply_scd_type2(source_df, target_table_name, key_columns, scd_columns):
    """Apply SCD Type 2 merge logic"""

    # Create target if not exists
    if not spark.catalog.tableExists(target_table_name):
        source_df.limit(0) \
            .withColumn("effective_from", F.current_date()) \
            .withColumn("effective_to", F.lit(None).cast("date")) \
            .withColumn("is_current", F.lit(True)) \
            .write.format("delta").saveAsTable(target_table_name)

    target = DeltaTable.forName(spark, target_table_name)

    # Detect changes
    source_df = source_df.withColumn("_hash",
        F.md5(F.concat_ws("|", *scd_columns))
    )

    # Close out old records
    target.alias("target").merge(
        source_df.alias("source"),
        " AND ".join([f"target.{k} = source.{k}" for k in key_columns]) +
        " AND target.is_current = true AND target._hash != source._hash"
    ).whenMatchedUpdate(
        set={
            "effective_to": "source.effective_date",
            "is_current": "false"
        }
    ).execute()

    # Insert new versions
    new_records = source_df.withColumn("effective_from", F.col("effective_date")) \
        .withColumn("effective_to", F.lit(None).cast("date")) \
        .withColumn("is_current", F.lit(True))

    new_records.write.format("delta").mode("append").saveAsTable(target_table_name)

    print(f"✅ SCD Type 2 applied to {target_table_name}")

apply_scd_type2(customers_cdc, "lakehouse.silver_customers",
                ["customer_id"], scd_columns)

# Show SCD result
print("\nCustomer history (SCD Type 2):")
spark.read.format("delta").table("lakehouse.silver_customers") \
    .orderBy("customer_id", "effective_from").show(truncate=False)

# 6. Explain Silver architecture
print("\n" + "="*70)
print("SILVER LAYER ARCHITECTURE")
print("="*70)
print("""
BRONZE CDC EVENTS
        ↓
DATA QUALITY CHECKS
- Schema validation
- Business rule validation
- Null checks, range checks
        ↓
QUARANTINE INVALID RECORDS
        ↓
CDC PROCESSING (Delta MERGE)
- INSERT: Add new records
- UPDATE: Modify existing records
- DELETE: Soft delete (is_deleted flag)
        ↓
SCD TYPE 2 (For Dimensions)
- Track historical changes
- effective_from/effective_to dates
- is_current flag
        ↓
SILVER DELTA TABLES
- Current state (fact tables)
- Historical snapshots (dimensions)
- Clean, conformed, validated

DATA QUALITY METRICS:
- % records passed validation
- Top validation failures
- Quarantine trend over time
- Data freshness SLA

PERFORMANCE:
- Delta MERGE: Atomic, ACID-compliant
- Z-ordering on common join keys
- Partition by date for time-range queries
- Optimize small files daily
""")
```

**THINK OUT LOUD EXPLANATION**:
"I'm implementing data quality as code using expectations. Invalid records are quarantined, not dropped, so we can investigate root causes. The MERGE operation atomically applies INSERT, UPDATE, and DELETE operations from CDC. For customer dimension, SCD Type 2 maintains full history with effective dates, enabling point-in-time analytics."

---

#### Q4: "Build Gold layer with aggregated metrics and star schema"

**✅ BEST ANSWER** (10 minutes):

```python
print("=== GOLD LAYER: BUSINESS AGGREGATES + STAR SCHEMA ===")

# THINK OUT LOUD:
# "Gold layer is optimized for specific business use cases. I'll create
#  pre-aggregated fact tables, denormalized dimension views, and
#  frequently-queried metrics. This reduces compute cost and query latency."

# 1. Create daily order metrics (pre-aggregated fact)
print("1. Creating daily order metrics...")

daily_metrics = spark.read.format("delta").table("lakehouse.silver_orders") \
    .filter("is_deleted = false") \
    .withColumn("order_date", F.to_date("order_date")) \
    .groupBy("order_date") \
    .agg(
        F.count("*").alias("total_orders"),
        F.sum("quantity").alias("total_quantity"),
        F.sum(F.col("quantity") * F.col("unit_price")).alias("total_revenue"),
        F.avg(F.col("quantity") * F.col("unit_price")).alias("avg_order_value"),
        F.countDistinct("customer_id").alias("unique_customers")
    )

daily_metrics.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("lakehouse.gold_daily_metrics")

print("✅ Daily metrics created")
daily_metrics.show(5)

# 2. Create customer 360 view (denormalized)
print("\n2. Creating Customer 360 view...")

# THINK OUT LOUD:
# "Customer 360 joins multiple sources to create a complete customer profile.
#  This denormalized view is optimized for dashboards and ML features.
#  I'm including RFM analysis and customer segmentation."

customer_360 = spark.read.format("delta").table("lakehouse.silver_customers") \
    .filter("is_current = true") \
    .alias("c") \
    .join(
        spark.read.format("delta").table("lakehouse.silver_orders")
            .filter("is_deleted = false")
            .alias("o"),
        "customer_id",
        "left"
    ) \
    .groupBy("c.customer_id", "c.name", "c.email", "c.country") \
    .agg(
        F.count("o.order_id").alias("total_orders"),
        F.sum(F.col("o.quantity") * F.col("o.unit_price")).alias("lifetime_value"),
        F.max("o.order_date").alias("last_order_date"),
        F.min("o.order_date").alias("first_order_date"),
        F.avg(F.col("o.quantity") * F.col("o.unit_price")).alias("avg_order_value")
    ) \
    .withColumn(
        "days_since_last_order",
        F.datediff(F.current_date(), F.col("last_order_date"))
    ) \
    .withColumn(
        "customer_tenure_days",
        F.datediff(F.current_date(), F.col("first_order_date"))
    ) \
    .withColumn(
        "customer_segment",
        F.when(F.col("lifetime_value") > 1000, "VIP")
         .when(F.col("lifetime_value") > 500, "High Value")
         .when(F.col("total_orders") > 5, "Loyal")
         .otherwise("Standard")
    )

customer_360.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("lakehouse.gold_customer_360")

print("✅ Customer 360 view created")
customer_360.show(5)

# 3. Create product performance view
print("\n3. Creating product performance metrics...")

product_metrics = spark.read.format("delta").table("lakehouse.silver_orders") \
    .filter("is_deleted = false") \
    .groupBy("product_id") \
    .agg(
        F.count("*").alias("total_orders"),
        F.sum("quantity").alias("units_sold"),
        F.sum(F.col("quantity") * F.col("unit_price")).alias("total_revenue"),
        F.avg("unit_price").alias("avg_price"),
        F.countDistinct("customer_id").alias("unique_buyers")
    ) \
    .withColumn(
        "revenue_rank",
        F.row_number().over(Window.orderBy(F.desc("total_revenue")))
    )

product_metrics.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("lakehouse.gold_product_metrics")

print("✅ Product metrics created")
print("\nTop 5 products by revenue:")
product_metrics.orderBy("revenue_rank").show(5)

# 4. Create star schema fact table
print("\n4. Creating star schema fact table...")

# THINK OUT LOUD:
# "A star schema fact table contains foreign keys to dimensions and
#  measures (metrics). This design is optimized for OLAP queries and
#  enables efficient joins with dimension tables."

fact_orders = spark.read.format("delta").table("lakehouse.silver_orders") \
    .filter("is_deleted = false") \
    .select(
        F.col("order_id").alias("order_key"),
        F.col("customer_id").alias("customer_key"),
        F.col("product_id").alias("product_key"),
        F.to_date("order_date").alias("date_key"),
        # Measures
        F.col("quantity"),
        F.col("unit_price"),
        (F.col("quantity") * F.col("unit_price")).alias("total_amount"),
        F.col("status")
    )

fact_orders.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("date_key") \
    .saveAsTable("lakehouse.gold_fact_orders")

print("✅ Fact table created (partitioned by date)")

# 5. Optimize Gold tables
print("\n5. Optimizing Gold tables for query performance...")

# THINK OUT LOUD:
# "I'm using Z-ordering to co-locate data for common join keys and filters.
#  This dramatically improves query performance by reducing I/O. Also
#  compacting small files to reduce metadata overhead."

tables_to_optimize = [
    ("lakehouse.gold_customer_360", ["customer_id"]),
    ("lakehouse.gold_fact_orders", ["customer_key", "product_key"]),
    ("lakehouse.gold_product_metrics", ["product_id"])
]

for table, zorder_cols in tables_to_optimize:
    print(f"\nOptimizing {table}...")

    # Compact small files
    spark.sql(f"OPTIMIZE {table}")

    # Z-order
    if zorder_cols:
        zorder_clause = ", ".join(zorder_cols)
        spark.sql(f"OPTIMIZE {table} ZORDER BY ({zorder_clause})")

    print(f"✅ {table} optimized (Z-ordered by {zorder_cols})")

# 6. Explain Gold architecture
print("\n" + "="*70)
print("GOLD LAYER ARCHITECTURE")
print("="*70)
print("""
SILVER (Cleaned Data)
        ↓
BUSINESS LOGIC TRANSFORMATIONS
- Pre-aggregations
- Denormalization
- Metric calculations
        ↓
GOLD TABLES (Use-Case Optimized)

1. DAILY METRICS (Time-series)
   - Pre-aggregated by day
   - Powers trend dashboards
   - Fast queries for reporting

2. CUSTOMER 360 (Denormalized)
   - Single source of truth per customer
   - RFM analysis built-in
   - Segmentation logic
   - ML feature store source

3. PRODUCT METRICS (Analytics)
   - Product performance KPIs
   - Revenue rankings
   - Inventory planning inputs

4. FACT TABLE (Star Schema)
   - Dimensional modeling
   - Optimized for BI tools
   - Partitioned by date
   - Z-ordered for joins

OPTIMIZATION STRATEGIES:
✓ Partition by date (time-range queries)
✓ Z-order by join keys (reduce I/O)
✓ Pre-aggregate common queries
✓ Denormalize for read performance
✓ Materialized views for complex joins

REFRESH STRATEGY:
- Daily full refresh for metrics
- Incremental for fact tables (append new dates)
- SCD merge for dimensions
""")

# 7. Show query performance comparison
print("\n7. Query performance: Gold vs Silver...")

print("\nExample: Get revenue by customer segment")

# Slow way: Query Silver and aggregate
print("\nQuerying Silver (on-the-fly aggregation):")
silver_query = """
SELECT
    CASE
        WHEN SUM(quantity * unit_price) > 1000 THEN 'VIP'
        WHEN SUM(quantity * unit_price) > 500 THEN 'High Value'
        ELSE 'Standard'
    END as segment,
    COUNT(DISTINCT customer_id) as customers,
    SUM(quantity * unit_price) as revenue
FROM lakehouse.silver_orders
WHERE is_deleted = false
GROUP BY 1
"""
# spark.sql(silver_query).show()  # Would be slower

# Fast way: Query Gold pre-computed
print("\nQuerying Gold (pre-computed):")
gold_query = """
SELECT
    customer_segment,
    COUNT(*) as customers,
    SUM(lifetime_value) as revenue
FROM lakehouse.gold_customer_360
GROUP BY customer_segment
"""
spark.sql(gold_query).show()

print("\n✅ Gold layer queries are 10-100x faster due to pre-aggregation")
```

**THINK OUT LOUD EXPLANATION**:
"Gold layer is designed for specific consumption patterns. Daily metrics are pre-aggregated to avoid expensive groupBys at query time. Customer 360 denormalizes data across multiple sources for fast lookups. The star schema fact table is partitioned by date and Z-ordered on join keys for optimal BI tool performance. This can make queries 10-100x faster than querying Silver."

---

### 🔥 CURVEBALL QUESTIONS

#### Q5: "How do you handle late-arriving data and out-of-order events?"

**✅ BEST ANSWER**:

```python
print("=== HANDLING LATE-ARRIVING DATA ===")

# THINK OUT LOUD:
# "Late-arriving data is common in distributed systems. I'll use:
#  1. Event time vs processing time separation
#  2. Watermarking to handle late events
#  3. Idempotent pipelines with MERGE
#  4. Reprocessing windows for corrections"

# 1. Event time processing
print("1. Implementing event-time processing with watermarking...")

# THINK OUT LOUD:
# "Watermarking defines how late data can arrive. Events within watermark
#  are processed, those beyond are dropped or sent to late-event table.
#  This balances completeness vs latency."

from pyspark.sql.functions import window

# Read CDC stream with event timestamp
late_data_stream = (
    spark.readStream
    .format("delta")
    .table("lakehouse.bronze_cdc")
    .withWatermark("timestamp", "2 hours")  # Allow 2 hours late
    .groupBy(
        window("timestamp", "1 hour"),  # Event time windowing
        "table_name"
    )
    .count()
)

print("✅ Watermarking configured: 2-hour late-event tolerance")

# 2. Handle extremely late events
print("\n2. Capturing extremely late events...")

# Late events beyond watermark go to separate table for investigation
late_events_query = """
CREATE OR REPLACE TABLE lakehouse.late_events AS
SELECT
    *,
    current_timestamp() as processing_time,
    datediff(hour, timestamp, current_timestamp()) as hours_late
FROM lakehouse.bronze_cdc
WHERE datediff(hour, timestamp, current_timestamp()) > 2
"""

spark.sql(late_events_query)
print("✅ Late events captured for reprocessing")

# 3. Reprocessing strategy
print("\n3. Implementing reprocessing for corrections...")

# THINK OUT LOUD:
# "For critical corrections, I'll reprocess specific time windows using
#  Delta time travel. This allows fixing historical data without full
#  recomputation. Downstream tables use MERGE for idempotency."

def reprocess_window(start_date, end_date):
    """Reprocess a specific date range"""

    print(f"Reprocessing window: {start_date} to {end_date}")

    # Read Bronze data for the window
    bronze_window = spark.read.format("delta").table("lakehouse.bronze_cdc") \
        .filter(f"date(timestamp) BETWEEN '{start_date}' AND '{end_date}'")

    print(f"Records to reprocess: {bronze_window.count()}")

    # Apply Silver transformations
    # ... (same CDC logic as before)

    # MERGE into Silver (idempotent - can run multiple times)
    # ... (same MERGE logic)

    print(f"✅ Window reprocessed: {start_date} to {end_date}")

# Example: Reprocess last 3 days due to late data
# reprocess_window("2025-04-17", "2025-04-19")

# 4. Explain the strategy
print("\n" + "="*70)
print("LATE DATA HANDLING STRATEGY")
print("="*70)
print("""
SCENARIO: Event from 3 hours ago arrives now

PROCESSING FLOW:

1. EVENT TIME vs PROCESSING TIME
   - Event timestamp: 2025-04-19 15:00 (when it happened)
   - Processing timestamp: 2025-04-19 18:00 (when we see it)

2. WATERMARK CHECK (2 hour tolerance)
   - Hours late: 3 hours
   - Beyond watermark? YES
   - Action: Route to late-events table

3. LATE-EVENT TABLE
   - Manual review and decision
   - Option A: Ignore (acceptable loss)
   - Option B: Reprocess window

4. REPROCESSING (if needed)
   - Query Bronze for time window
   - Re-run transformations
   - MERGE into Silver (idempotent)
   - Downstream Gold refreshes automatically

5. DOWNSTREAM IMPACT
   - Daily metrics: Next daily refresh includes correction
   - Real-time metrics: Reprocessing updates immediately
   - Historical reports: Time travel shows before/after

TRADE-OFFS:
✓ Watermark too short (1 min): Lose late data
✓ Watermark too long (1 day): High state memory, slow queries
✓ Sweet spot: 2-4 hours for most use cases

MONITORING:
- Late event count trend
- Processing lag (event time - processing time)
- Watermark breaches alert
- Data completeness SLA
""")

# 5. Monitoring query
print("\n5. Late data monitoring query...")

late_data_monitor = """
SELECT
    date(timestamp) as event_date,
    date(_ingestion_timestamp) as ingestion_date,
    COUNT(*) as record_count,
    AVG(datediff(hour, timestamp, _ingestion_timestamp)) as avg_lag_hours,
    MAX(datediff(hour, timestamp, _ingestion_timestamp)) as max_lag_hours
FROM lakehouse.bronze_cdc
GROUP BY 1, 2
ORDER BY 1 DESC, 2 DESC
LIMIT 10
"""

print("\nData arrival lag analysis:")
spark.sql(late_data_monitor).show()
```

**THINK OUT LOUD EXPLANATION**:
"Late-arriving data is inevitable in distributed systems. I use watermarking to define acceptable lateness (2 hours is common). Events beyond the watermark go to a late-events table for review. Critical corrections trigger reprocessing of specific time windows using Delta time travel. Idempotent MERGE operations ensure reprocessing is safe."

---

#### Q6: "The pipeline is slow. How do you optimize it?"

**✅ BEST ANSWER**:

```python
print("=== PIPELINE PERFORMANCE OPTIMIZATION ===")

# THINK OUT LOUD:
# "When a pipeline is slow, I follow a systematic approach:
#  1. Identify bottlenecks using Spark UI
#  2. Optimize the slowest stage first
#  3. Apply targeted optimizations (partitioning, caching, broadcast)
#  4. Measure improvement"

# 1. Analyze query plan
print("1. Analyzing query plan for bottlenecks...")

# Example slow query
slow_query = """
SELECT
    c.customer_id,
    c.name,
    COUNT(o.order_id) as order_count,
    SUM(o.quantity * o.unit_price) as total_revenue
FROM lakehouse.silver_customers c
LEFT JOIN lakehouse.silver_orders o ON c.customer_id = o.customer_id
WHERE c.is_current = true AND o.is_deleted = false
GROUP BY c.customer_id, c.name
"""

slow_df = spark.sql(slow_query)

print("Original query plan:")
slow_df.explain("formatted")

# THINK OUT LOUD:
# "Looking at the plan, I see:
#  - Sort-merge join (indicates shuffle on both sides)
#  - No partition pruning
#  - Multiple shuffles for groupBy
#  Let me optimize these..."

# 2. Optimization 1: Partition by join key
print("\n2. OPTIMIZATION 1: Partition by join key...")

# THINK OUT LOUD:
# "If both tables are partitioned by the join key (customer_id),
#  Spark can avoid the shuffle during join. Data is already co-located."

# Repartition orders by customer_id
spark.sql("""
CREATE OR REPLACE TABLE lakehouse.silver_orders_partitioned
USING DELTA
PARTITIONED BY (date_partition)
AS
SELECT
    *,
    date_trunc('month', order_date) as date_partition
FROM lakehouse.silver_orders
""")

# Z-order by customer_id within partitions
spark.sql("OPTIMIZE lakehouse.silver_orders_partitioned ZORDER BY (customer_id)")

print("✅ Orders table repartitioned and Z-ordered")

# 3. Optimization 2: Broadcast small dimension
print("\n3. OPTIMIZATION 2: Broadcast small dimension table...")

# THINK OUT LOUD:
# "If customers table is small (<10GB), broadcasting it avoids shuffle.
#  The whole table is sent to each executor."

from pyspark.sql.functions import broadcast

optimized_query = spark.read.format("delta").table("lakehouse.silver_customers") \
    .filter("is_current = true") \
    .alias("c") \
    .join(
        broadcast(
            spark.read.format("delta").table("lakehouse.silver_orders")
                .filter("is_deleted = false")
        ).alias("o"),
        "customer_id",
        "left"
    ) \
    .groupBy("c.customer_id", "c.name") \
    .agg(
        F.count("o.order_id").alias("order_count"),
        F.sum(F.col("o.quantity") * F.col("o.unit_price")).alias("total_revenue")
    )

print("Optimized query plan with broadcast:")
optimized_query.explain("formatted")

# 4. Optimization 3: Predicate pushdown
print("\n4. OPTIMIZATION 3: Predicate pushdown...")

# THINK OUT LOUD:
# "Filtering before join reduces data volume and shuffle size.
#  Delta's data skipping reads only relevant files."

# BAD: Filter after join
# df.join(...).filter("order_date >= '2025-01-01'")

# GOOD: Filter before join
recent_orders = spark.read.format("delta").table("lakehouse.silver_orders") \
    .filter("order_date >= '2025-01-01' AND is_deleted = false")  # Pushdown

optimized_query2 = spark.read.format("delta").table("lakehouse.silver_customers") \
    .filter("is_current = true") \
    .join(recent_orders, "customer_id")

print("✅ Predicate pushdown applied")

# 5. Optimization 4: Caching intermediate results
print("\n5. OPTIMIZATION 4: Caching frequently-used tables...")

# THINK OUT LOUD:
# "If a table is used multiple times in the pipeline, cache it to avoid
#  recomputation. This trades memory for speed."

customers_filtered = spark.read.format("delta").table("lakehouse.silver_customers") \
    .filter("is_current = true")

customers_filtered.cache()
customers_filtered.count()  # Materialize cache

print(f"✅ Cached customers table: {customers_filtered.storageLevel}")

# Use cached table multiple times
result1 = customers_filtered.groupBy("country").count()
result2 = customers_filtered.filter("lifetime_value > 1000")

# Unpersist when done
customers_filtered.unpersist()

# 6. Optimization 5: Adaptive Query Execution (AQE)
print("\n6. OPTIMIZATION 5: Enable Adaptive Query Execution...")

# THINK OUT LOUD:
# "AQE optimizes queries dynamically during execution based on runtime
#  statistics. It coalesces partitions, optimizes joins, and handles skew."

spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")

print("✅ AQE enabled:")
print("  - Dynamic partition coalescing")
print("  - Skew join optimization")
print("  - Dynamic join strategy selection")

# 7. Performance comparison
print("\n" + "="*70)
print("PERFORMANCE OPTIMIZATION RESULTS")
print("="*70)

optimizations = [
    ("Original query", "No optimization", "100s", "5 shuffles"),
    ("Partition by join key", "Pre-partitioned tables", "60s", "3 shuffles"),
    ("Broadcast join", "Small table broadcast", "30s", "1 shuffle"),
    ("Predicate pushdown", "Filter before join", "15s", "1 shuffle"),
    ("Caching", "Cache reused tables", "10s", "0 shuffles (cached)"),
    ("AQE enabled", "Dynamic optimization", "8s", "Auto-coalesced"),
]

print(f"\n{'Optimization':<25} {'Technique':<30} {'Time':<10} {'Shuffles':<20}")
print("-" * 90)
for opt, tech, time, shuffle in optimizations:
    print(f"{opt:<25} {tech:<30} {time:<10} {shuffle:<20}")

# 8. Monitoring recommendations
print("\n" + "="*70)
print("MONITORING & ONGOING OPTIMIZATION")
print("="*70)
print("""
SPARK UI METRICS TO MONITOR:
1. Stage-level metrics
   - Duration per stage
   - Shuffle read/write size
   - Task count and distribution

2. Task-level metrics
   - Straggler tasks (outliers)
   - GC time percentage
   - Spill to disk

3. SQL tab
   - Query plans (visual DAG)
   - Exchange (shuffle) operations
   - Scan size vs output size

AUTOMATED OPTIMIZATION:
- Auto-compact small files (OPTIMIZE daily)
- Auto-vacuum old versions (7-day retention)
- Auto-analyze statistics (for CBO)
- Auto-repartition based on data volume

COST OPTIMIZATION:
- Right-size cluster (don't over-provision)
- Use spot instances for non-critical jobs
- Partition by date, vacuum old partitions
- Compress with appropriate codec (zstd)

RULE OF THUMB:
- Shuffle < 10% of data volume
- Partition size: 100MB - 1GB
- Cache if reused >2 times
- Broadcast if table < 10GB
""")
```

**THINK OUT LOUD EXPLANATION**:
"I start by analyzing the query plan to identify shuffles and bottlenecks. The biggest wins come from partitioning by join keys, broadcasting small tables, and predicate pushdown. Adaptive Query Execution automatically handles many optimizations at runtime. Monitoring Spark UI is critical - I look for straggler tasks, excessive shuffles, and data skew."

---

## 🎯 Scenario 2: Real-Time Streaming Data Pipeline

### 📋 Context
**Interviewer**: *"We're ingesting clickstream events from a website at 10,000 events/second. Build a real-time pipeline that processes events, sessionizes users, detects anomalies, and writes to Delta for analytics. Focus on streaming architecture and state management."*

---

### Expected Questions & Best Answers

#### Q1: "Design the streaming architecture"

**✅ BEST ANSWER** (2 minutes):

```
"I'll design a multi-layer streaming pipeline:

INGESTION LAYER:
- Kafka topics for event buffering
- Auto Loader for cloud storage fallback
- Exactly-once semantics with checkpointing

PROCESSING LAYER (Structured Streaming):
- Stateful sessionization (30-min timeout)
- Watermarking for late events (10-min tolerance)
- Anomaly detection with streaming aggregations
- Deduplication using dropDuplicates with watermark

STORAGE LAYER:
- Bronze: Raw events (append-only)
- Silver: Sessionized, cleaned (streaming MERGE)
- Gold: Real-time dashboards (windowed aggregations)

STATE MANAGEMENT:
- RocksDB state store for scalability
- State checkpointing to cloud storage
- TTL for session cleanup

MONITORING:
- Trigger metrics (processing lag, batch duration)
- State size growth
- Checkpoint health

Let me implement this..."
```

---

#### Q2: "Implement the streaming sessionization pipeline"

**✅ BEST ANSWER** (15 minutes):

```python
from pyspark.sql import functions as F
from pyspark.sql.types import *

print("=== REAL-TIME STREAMING SESSIONIZATION ===")

# 1. Generate synthetic clickstream data
print("1. Generating synthetic clickstream events...")

# THINK OUT LOUD:
# "Clickstream events have user_id, timestamp, event_type, and page.
#  I'll simulate realistic sessions with gaps for session boundaries."

import random
from datetime import datetime, timedelta

def generate_clickstream_batch(batch_num, num_events=10000):
    """Generate clickstream events with realistic session patterns"""
    data = []
    base_time = datetime.now() - timedelta(minutes=batch_num * 5)
    num_users = 1000

    for i in range(num_events):
        user_id = random.randint(1, num_users)

        # Simulate session gaps (30% chance of >30min gap = new session)
        if random.random() < 0.3:
            time_offset = random.randint(1800, 7200)  # 30min - 2hr gap
        else:
            time_offset = random.randint(1, 300)  # 1s - 5min gap

        event_time = base_time + timedelta(seconds=time_offset)

        event_type = random.choice([
            "page_view", "page_view", "page_view",  # 60% page views
            "click", "click",  # 40% clicks
            "purchase"  # 5% purchases
        ])

        page = random.choice([
            "/home", "/product/123", "/cart", "/checkout", "/account"
        ])

        data.append((
            f"event_{batch_num}_{i}",
            user_id,
            event_time,
            event_type,
            page
        ))

    return data

# Create streaming source
clickstream_schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("user_id", IntegerType(), False),
    StructField("event_timestamp", TimestampType(), False),
    StructField("event_type", StringType(), False),
    StructField("page", StringType(), False)
])

# Write initial batches to simulate stream
for batch in range(3):
    events = generate_clickstream_batch(batch, 5000)
    events_df = spark.createDataFrame(events, clickstream_schema)

    output_path = f"/tmp/clickstream_raw/batch_{batch}"
    events_df.write.mode("overwrite").parquet(output_path)
    print(f"✅ Batch {batch}: {events_df.count()} events written")

# 2. Set up streaming read
print("\n2. Setting up streaming ingestion...")

clickstream_stream = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("cloudFiles.schemaLocation", "/tmp/clickstream_checkpoint/schema")
    .schema(clickstream_schema)
    .load("/tmp/clickstream_raw")
)

# Add ingestion metadata
clickstream_stream = clickstream_stream \
    .withColumn("ingestion_timestamp", F.current_timestamp())

print("✅ Streaming source configured")

# 3. Implement sessionization
print("\n3. Implementing sessionization with state management...")

# THINK OUT LOUD:
# "Sessionization groups events into sessions based on inactivity timeout.
#  I'm using watermarking to handle late events and state timeout to
#  clean up old sessions. 30-minute inactivity = new session."

from pyspark.sql.streaming import GroupState, GroupStateTimeout

# Define session state
session_schema = StructType([
    StructField("session_id", StringType()),
    StructField("user_id", IntegerType()),
    StructField("session_start", TimestampType()),
    StructField("session_end", TimestampType()),
    StructField("event_count", IntegerType()),
    StructField("pages_visited", ArrayType(StringType())),
    StructField("has_purchase", BooleanType())
])

def sessionize_events(user_id, events, state: GroupState):
    """Stateful sessionization function"""

    # Timeout duration: 30 minutes
    timeout_duration_ms = 30 * 60 * 1000

    # Get existing session or create new
    if state.exists:
        session = state.get
        session_id = session['session_id']
        session_start = session['session_start']
        event_count = session['event_count']
        pages_visited = set(session['pages_visited'])
        has_purchase = session['has_purchase']
    else:
        session_id = f"session_{user_id}_{int(time.time())}"
        session_start = None
        event_count = 0
        pages_visited = set()
        has_purchase = False

    # Process new events
    events_list = list(events)
    if events_list:
        for event in events_list:
            if session_start is None:
                session_start = event['event_timestamp']

            event_count += 1
            pages_visited.add(event['page'])

            if event['event_type'] == 'purchase':
                has_purchase = True

            session_end = event['event_timestamp']

    # Update state
    new_state = {
        'session_id': session_id,
        'user_id': user_id,
        'session_start': session_start,
        'session_end': session_end,
        'event_count': event_count,
        'pages_visited': list(pages_visited),
        'has_purchase': has_purchase
    }

    state.update(new_state)
    state.setTimeoutDuration(timeout_duration_ms)

    # Yield completed session
    if state.hasTimedOut:
        state.remove()
        return [(session_id, user_id, session_start, session_end, event_count, list(pages_visited), has_purchase)]

    return []

# Apply sessionization (simplified - using window approach instead of mapGroupsWithState for demo)
print("\n3a. Using windowing approach for sessionization...")

# THINK OUT LOUD:
# "For production, I'd use mapGroupsWithState for custom state logic.
#  Here I'll demonstrate with session windows which is simpler for the demo."

sessioned_stream = (
    clickstream_stream
    .withWatermark("event_timestamp", "10 minutes")  # Late event tolerance
    .groupBy(
        "user_id",
        F.session_window("event_timestamp", "30 minutes")  # 30-min inactivity timeout
    )
    .agg(
        F.count("*").alias("event_count"),
        F.min("event_timestamp").alias("session_start"),
        F.max("event_timestamp").alias("session_end"),
        F.collect_set("page").alias("pages_visited"),
        F.max(F.when(F.col("event_type") == "purchase", 1).otherwise(0)).alias("has_purchase")
    )
    .select(
        F.concat(F.col("user_id").cast("string"), F.lit("_"),
                F.col("session_window.start").cast("long").cast("string")).alias("session_id"),
        "user_id",
        F.col("session_window.start").alias("session_start"),
        F.col("session_window.end").alias("session_end"),
        "event_count",
        "pages_visited",
        F.col("has_purchase").cast("boolean")
    )
)

print("✅ Sessionization configured with 30-min timeout")

# 4. Write sessions to Delta
print("\n4. Writing sessions to Delta...")

session_query = (
    sessioned_stream
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/sessions_checkpoint")
    .trigger(processingTime="30 seconds")
    .table("streaming.user_sessions")
)

print("✅ Session stream started")

# Let it process
import time
time.sleep(35)

# 5. Validate sessions
print("\n5. Validating sessionized data...")

sessions_df = spark.read.format("delta").table("streaming.user_sessions")
print(f"Total sessions: {sessions_df.count()}")

print("\nSample sessions:")
sessions_df.select(
    "session_id", "user_id", "session_start", "event_count", "has_purchase"
).show(5)

print("\nSession duration statistics:")
sessions_df.withColumn(
    "duration_minutes",
    (F.unix_timestamp("session_end") - F.unix_timestamp("session_start")) / 60
).select("duration_minutes").describe().show()

# 6. Explain streaming architecture
print("\n" + "="*70)
print("STREAMING SESSIONIZATION ARCHITECTURE")
print("="*70)
print("""
CLICKSTREAM EVENTS (10k/sec)
        ↓
AUTO LOADER (Incremental ingestion)
        ↓
WATERMARKING (10-min late tolerance)
        ↓
SESSION WINDOW (30-min inactivity timeout)
        ↓
STATEFUL AGGREGATION
- Group by user_id + session_window
- Count events per session
- Collect pages visited
- Flag purchases
        ↓
DELTA TABLE (streaming.user_sessions)
        ↓
DOWNSTREAM CONSUMERS
- Real-time dashboards
- Anomaly detection
- Recommendation engine

STATE MANAGEMENT:
- Watermark: Discards state after 10 min late tolerance
- Session timeout: 30 minutes of inactivity
- State store: RocksDB (local) + Cloud checkpoint (recovery)
- TTL: Automatic cleanup after session completes

PERFORMANCE:
- Micro-batch trigger: 30 seconds
- Throughput: 10k events/sec
- Latency: <1 minute end-to-end
- State size: Bounded by active sessions (<1GB typically)

FAULT TOLERANCE:
- Checkpointing: Exactly-once semantics
- State recovery: Automatic from checkpoint
- Retries: Transient failures auto-retry
- Dead letter queue: Malformed events quarantined
""")

# Stop stream
session_query.stop()
```

**THINK OUT LOUD EXPLANATION**:
"I'm using session windows with 30-minute inactivity timeout. Watermarking handles late events up to 10 minutes. State is automatically managed by Spark - old sessions are cleaned up after timeout. Checkpointing ensures exactly-once processing even with failures. For production, I'd use `mapGroupsWithState` for custom session logic and complex state transitions."

---

#### Q3: "Add real-time anomaly detection to the stream"

**✅ BEST ANSWER** (10 minutes):

```python
print("=== REAL-TIME ANOMALY DETECTION ===")

# THINK OUT LOUD:
# "I'll detect anomalies by comparing current behavior to rolling baselines:
#  1. Sudden spike in events per user (velocity anomaly)
#  2. Unusual page sequences (behavioral anomaly)
#  3. Purchase from new user in first session (fraud pattern)
#  Using streaming aggregations and Z-score for statistical detection."

# 1. Calculate baseline metrics
print("1. Computing baseline metrics from historical data...")

# Historical baseline (from completed sessions)
baseline = spark.read.format("delta").table("streaming.user_sessions") \
    .groupBy("user_id") \
    .agg(
        F.avg("event_count").alias("avg_events_per_session"),
        F.stddev("event_count").alias("stddev_events"),
        F.count("*").alias("total_sessions"),
        F.sum(F.col("has_purchase").cast("int")).alias("purchase_sessions")
    )

print("Baseline metrics (sample):")
baseline.show(5)

# Write to Delta for streaming join
baseline.write.format("delta").mode("overwrite").saveAsTable("streaming.user_baselines")

# 2. Stream-static join for anomaly detection
print("\n2. Setting up streaming anomaly detection...")

# Read session stream
session_stream = spark.readStream.format("delta").table("streaming.user_sessions")

# Join with baseline (stream-static join)
anomaly_stream = session_stream.alias("s") \
    .join(
        broadcast(baseline).alias("b"),
        "user_id",
        "left"
    ) \
    .withColumn(
        "z_score",
        (F.col("s.event_count") - F.coalesce(F.col("b.avg_events_per_session"), F.lit(0))) /
        F.coalesce(F.col("b.stddev_events"), F.lit(1))
    ) \
    .withColumn(
        "is_velocity_anomaly",
        F.abs(F.col("z_score")) > 3  # >3 standard deviations
    ) \
    .withColumn(
        "is_first_session_purchase",
        (F.col("s.has_purchase") == True) & (F.coalesce(F.col("b.total_sessions"), F.lit(0)) == 0)
    ) \
    .withColumn(
        "is_anomalous",
        F.col("is_velocity_anomaly") | F.col("is_first_session_purchase")
    )

# Filter to anomalies only
anomalies_only = anomaly_stream.filter("is_anomalous = true")

# 3. Write anomalies to alert table
print("\n3. Writing anomalies to alert table...")

anomaly_query = (
    anomalies_only
    .select(
        "session_id",
        "user_id",
        "session_start",
        "event_count",
        "has_purchase",
        "z_score",
        "is_velocity_anomaly",
        "is_first_session_purchase",
        F.current_timestamp().alias("detected_at")
    )
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/anomalies_checkpoint")
    .trigger(processingTime="10 seconds")
    .table("streaming.session_anomalies")
)

print("✅ Anomaly detection stream started")

time.sleep(15)

# 4. Check anomalies detected
print("\n4. Anomalies detected:")

anomalies_df = spark.read.format("delta").table("streaming.session_anomalies")
print(f"Total anomalies: {anomalies_df.count()}")

if anomalies_df.count() > 0:
    anomalies_df.select(
        "session_id", "user_id", "event_count", "z_score",
        "is_velocity_anomaly", "is_first_session_purchase"
    ).show(5)

# 5. Real-time alerting
print("\n5. Real-time alerting setup...")

print("""
ALERTING STRATEGY:

HIGH-PRIORITY ANOMALIES (immediate alert):
- First-session purchase > $500 (fraud risk)
- Velocity > 5 stdev (bot detection)
- 10+ purchases in 1 hour (card testing)

MEDIUM-PRIORITY (batched alerts):
- Unusual page sequences
- Geographic anomalies
- Time-of-day anomalies

ALERT CHANNELS:
- PagerDuty: High-priority fraud
- Slack: Medium-priority patterns
- Email digest: Daily summary

IMPLEMENTATION:
- foreachBatch sink to trigger alerts
- Rate limiting (max 100 alerts/min)
- Deduplication (same user within 5 min)
""")

# Stop stream
anomaly_query.stop()

print("\n" + "="*70)
print("ANOMALY DETECTION SUMMARY")
print("="*70)
print("""
DETECTION METHODS:

1. STATISTICAL (Z-score)
   - Compare to user's baseline
   - > 3 standard deviations = anomaly
   - Adaptive (baselines update daily)

2. RULE-BASED
   - First-session purchase (fraud pattern)
   - Rapid clicks (bot pattern)
   - Off-hours activity (compromised account)

3. MACHINE LEARNING (future)
   - Train model on historical anomalies
   - Feature: session_duration, pages/min, purchase_rate
   - Online scoring in streaming pipeline

PERFORMANCE:
- Latency: <10 seconds detection to alert
- Throughput: 10k sessions/sec evaluated
- False positive rate: <5%
- Recall: >90% of known frauds detected

STATE MANAGEMENT:
- User baselines cached (broadcast join)
- Refresh baselines nightly
- Rolling window for real-time recalc
""")
```

**THINK OUT LOUD EXPLANATION**:
"I'm using Z-score for statistical anomaly detection - comparing each session's event count to the user's historical average. Stream-static joins let me enrich streaming events with baseline metrics. Anomalies trigger immediate writes to an alert table. In production, I'd add ML models trained on historical fraud patterns for more sophisticated detection."

---

## 📊 Summary Table: Data Engineering Competencies

| Competency | Scenario 1 (Lakehouse) | Scenario 2 (Streaming) | What Interviewer Sees |
|------------|------------------------|------------------------|----------------------|
| **Medallion Architecture** | ⭐⭐⭐⭐⭐ Bronze/Silver/Gold | ⭐⭐⭐⭐ Real-time layers | Structured thinking |
| **Delta Lake** | ⭐⭐⭐⭐⭐ MERGE, SCD, Time Travel | ⭐⭐⭐⭐⭐ Streaming writes, ACID | Platform expertise |
| **CDC Processing** | ⭐⭐⭐⭐⭐ Insert/Update/Delete handling | ⭐⭐⭐ Change streams | Real-world experience |
| **Data Quality** | ⭐⭐⭐⭐⭐ Expectations, quarantine | ⭐⭐⭐ Deduplication | Production mindset |
| **Streaming** | ⭐⭐ Incremental ingestion | ⭐⭐⭐⭐⭐ Stateful processing | Advanced skills |
| **Performance Optimization** | ⭐⭐⭐⭐⭐ Partitioning, Z-order, caching | ⭐⭐⭐⭐ State management | Problem-solving ability |
| **Dimensional Modeling** | ⭐⭐⭐⭐⭐ Star schema, SCD Type 2 | ⭐⭐⭐ Sessionization | Data warehouse knowledge |

---

## 🎯 Interview Success Patterns

### What Data Engineers Want to Hear

1. **"Let me think about the data model first..."**
   - Shows you design before coding
   - Considers downstream consumers
   - Plans for evolution

2. **"I'm using MERGE instead of INSERT to ensure idempotency..."**
   - Understands production requirements
   - Knows Delta Lake capabilities
   - Considers failure scenarios

3. **"This will partition by date and Z-order by customer_id..."**
   - Optimizes for query patterns
   - Understands data skipping
   - Considers cost/performance trade-offs

4. **"Let me check the query plan to identify bottlenecks..."**
   - Data-driven optimization
   - Uses Spark UI effectively
   - Systematic debugging approach

5. **"For late-arriving data, I'll use watermarking with a 2-hour tolerance..."**
   - Understands distributed system challenges
   - Balances completeness vs latency
   - Plans for edge cases

### Red Flags to Avoid

❌ "I'll just append the data" (no idempotency consideration)
❌ "Let me join these massive tables" (no broadcast/partition thinking)
❌ Silent coding for >2 minutes (interviewers can't assess thought process)
❌ "This should work" without validating (no data quality mindset)
❌ "I'll cache everything" (indiscriminate optimization)

---

## 🎓 Study Priority for Data Engineering Background

**HIGH PRIORITY** (Practice 2-3 times):
- Medallion architecture end-to-end
- Delta MERGE operations (CDC, SCD Type 2)
- Streaming sessionization
- Performance optimization (query plans, partitioning)

**MEDIUM PRIORITY** (Practice once):
- Auto Loader configuration
- Data quality frameworks
- Watermarking and late data
- Schema evolution

**NICE TO HAVE** (Read/understand):
- Unity Catalog governance
- Delta Live Tables
- Complex state management
- Advanced streaming patterns

---

**You're ready! Data engineering interviewers love candidates who understand the full data lifecycle from ingestion to serving. Show them you can build production-grade, scalable pipelines! 🚀**
