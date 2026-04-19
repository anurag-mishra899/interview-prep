# Databricks Vibe Interview - Practice Scenarios
# Run these in Databricks Free Edition notebooks to prepare

"""
SETUP INSTRUCTIONS:
1. Create a Databricks Free Edition account
2. Start a cluster
3. Create a new Python notebook
4. Copy each scenario into separate cells
5. Practice thinking out loud while coding
"""

# ============================================================================
# SCENARIO 1: E-Commerce Customer Analytics
# ============================================================================

"""
PROMPT: Generate synthetic e-commerce data and identify high-value customers
GOAL: Practice multi-table generation, joins, and aggregations
"""

# Cell 1: Install dbldatagen (if not already available)
# %pip install dbldatagen

# Cell 2: Generate Customers Table
import dbldatagen as dg
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from datetime import datetime, timedelta

# THINK OUT LOUD:
# "I'm generating 10,000 customers with realistic email patterns.
#  Using unique values ensures no duplicate customer_ids."

customers_spec = (
    dg.DataGenerator(spark, name="customers", rows=10000, partitions=4)
    .withColumn("customer_id", "int", minValue=1, maxValue=10000, uniqueValues=10000)
    .withColumn("first_name", "string", template=r"\w")
    .withColumn("last_name", "string", template=r"\w")
    .withColumn("email", "string", template=r"\w.\w@\w.com")
    .withColumn("signup_date", "date", begin="2023-01-01", end="2025-12-31")
    .withColumn("country", "string", values=["USA", "UK", "Canada", "Germany", "France"],
                weights=[40, 20, 15, 15, 10])
)

customers_df = customers_spec.build()
display(customers_df)

# Cell 3: Generate Orders Table with Log-Normal Distribution
# THINK OUT LOUD:
# "Using log-normal distribution for order amounts because real spending
#  follows this pattern - most orders are small, with a long tail of large orders"

import numpy as np
from pyspark.sql.types import TimestampType

orders_spec = (
    dg.DataGenerator(spark, name="orders", rows=50000, partitions=4)
    .withColumn("order_id", "int", minValue=1, maxValue=50000, uniqueValues=50000)
    .withColumn("customer_id", "int", minValue=1, maxValue=10000)  # FK to customers
    .withColumn("order_date", "timestamp",
                begin="2024-01-01 00:00:00",
                end="2025-12-31 23:59:59")
    .withColumn("order_amount", "float", minValue=10.0, maxValue=1000.0,
                random=True, distribution="log-normal")
    .withColumn("status", "string",
                values=["completed", "pending", "cancelled", "refunded"],
                weights=[70, 15, 10, 5])
)

orders_df = orders_spec.build()

# Introduce some NULL values (5%) to simulate data quality issues
orders_df = orders_df.withColumn(
    "order_amount",
    F.when(F.rand() < 0.05, None).otherwise(F.col("order_amount"))
)

display(orders_df)

# Cell 4: Validation - Always Check Your Generated Data
# THINK OUT LOUD:
# "Let me validate the data before proceeding. Checking for referential integrity,
#  null counts, and distribution of values."

print("=== CUSTOMERS VALIDATION ===")
print(f"Total customers: {customers_df.count()}")
print(f"Distinct customer_ids: {customers_df.select('customer_id').distinct().count()}")

print("\n=== ORDERS VALIDATION ===")
print(f"Total orders: {orders_df.count()}")
print(f"Orders with null amounts: {orders_df.filter(F.col('order_amount').isNull()).count()}")
print(f"Date range: {orders_df.agg(F.min('order_date'), F.max('order_date')).collect()[0]}")

# Check referential integrity
orphaned_orders = orders_df.join(customers_df, "customer_id", "left_anti")
print(f"Orphaned orders (no matching customer): {orphaned_orders.count()}")

display(orders_df.describe("order_amount"))

# Cell 5: Analytics - Customer Lifetime Value (CLV)
# THINK OUT LOUD:
# "I'm calculating CLV by grouping orders by customer and summing amounts.
#  This requires a shuffle since we need to co-locate all orders per customer.
#  Filtering out cancelled/refunded orders to get accurate revenue."

clv_df = (
    orders_df
    .filter(F.col("status").isin(["completed", "pending"]))  # Only revenue-generating
    .filter(F.col("order_amount").isNotNull())  # Exclude nulls
    .groupBy("customer_id")
    .agg(
        F.sum("order_amount").alias("total_revenue"),
        F.count("order_id").alias("total_orders"),
        F.avg("order_amount").alias("avg_order_value"),
        F.min("order_date").alias("first_order_date"),
        F.max("order_date").alias("last_order_date")
    )
    .withColumn(
        "days_as_customer",
        F.datediff(F.col("last_order_date"), F.col("first_order_date"))
    )
)

display(clv_df.orderBy(F.desc("total_revenue")).limit(20))

# Cell 6: Enrichment - Join with Customer Demographics
# THINK OUT LOUD:
# "Using a broadcast join here since customers table is small (~10K rows).
#  This avoids a shuffle by sending the small table to all executors."

customer_insights = (
    clv_df
    .join(F.broadcast(customers_df), "customer_id", "inner")
    .select(
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "country",
        "signup_date",
        "total_revenue",
        "total_orders",
        "avg_order_value",
        "days_as_customer"
    )
)

display(customer_insights)

# Cell 7: Ranking - Identify Top 10% Customers
# THINK OUT LOUD:
# "Using ntile() window function to segment customers into deciles.
#  This is more efficient than calculating percentiles and filtering."

window_spec = Window.orderBy(F.desc("total_revenue"))

top_customers = (
    customer_insights
    .withColumn("revenue_rank", F.rank().over(window_spec))
    .withColumn("revenue_decile", F.ntile(10).over(window_spec))
    .filter(F.col("revenue_decile") == 1)  # Top 10%
)

display(top_customers)

# Cell 8: Write to Delta Table
# THINK OUT LOUD:
# "Writing to Delta format for ACID guarantees and time travel capability.
#  Using overwrite mode for this full refresh, but in production we'd use MERGE
#  for incremental updates."

customer_insights.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("customer_insights")

print("✅ Data successfully written to Delta table: customer_insights")


# ============================================================================
# SCENARIO 2: Log Processing & Anomaly Detection
# ============================================================================

"""
PROMPT: Generate server log data and identify anomalies
GOAL: Practice time-series data, window functions, statistical analysis
"""

# Cell 1: Generate Server Logs with Semi-Structured Data
import json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

# THINK OUT LOUD:
# "Generating logs with varying response times. Will introduce anomalies by
#  occasionally spiking the response time to simulate server issues."

logs_spec = (
    dg.DataGenerator(spark, name="server_logs", rows=100000, partitions=8)
    .withColumn("timestamp", "timestamp",
                begin="2025-04-01 00:00:00",
                end="2025-04-16 23:59:59")
    .withColumn("server_id", "string", values=[f"server_{i:03d}" for i in range(1, 21)])
    .withColumn("endpoint", "string",
                values=["/api/users", "/api/orders", "/api/products", "/api/analytics"],
                weights=[40, 30, 20, 10])
    .withColumn("response_time_ms", "int", minValue=50, maxValue=500,
                distribution="normal", mean=200, stddev=50)
    .withColumn("status_code", "int",
                values=[200, 201, 400, 404, 500, 503],
                weights=[80, 5, 5, 5, 3, 2])
)

logs_df = logs_spec.build()

# Introduce anomalies: 2% of logs have very high response times
logs_df = logs_df.withColumn(
    "response_time_ms",
    F.when(F.rand() < 0.02, F.lit(5000) + (F.rand() * 5000).cast("int"))
    .otherwise(F.col("response_time_ms"))
)

display(logs_df.orderBy("timestamp").limit(100))

# Cell 2: Time-Window Aggregations
# THINK OUT LOUD:
# "Using a 5-minute tumbling window to aggregate logs. This groups events
#  into non-overlapping time buckets for trend analysis."

from pyspark.sql.functions import window

windowed_metrics = (
    logs_df
    .groupBy(
        F.window("timestamp", "5 minutes"),
        "server_id"
    )
    .agg(
        F.count("*").alias("request_count"),
        F.avg("response_time_ms").alias("avg_response_time"),
        F.max("response_time_ms").alias("max_response_time"),
        F.sum(F.when(F.col("status_code") >= 500, 1).otherwise(0)).alias("error_count")
    )
    .select(
        F.col("window.start").alias("window_start"),
        F.col("window.end").alias("window_end"),
        "server_id",
        "request_count",
        "avg_response_time",
        "max_response_time",
        "error_count"
    )
)

display(windowed_metrics.orderBy("window_start", "server_id"))

# Cell 3: Anomaly Detection using Z-Score
# THINK OUT LOUD:
# "Calculating z-score to identify statistical outliers. Values >3 standard
#  deviations from mean are considered anomalies."

# Calculate global statistics
stats = logs_df.select(
    F.mean("response_time_ms").alias("mean_response"),
    F.stddev("response_time_ms").alias("stddev_response")
).collect()[0]

mean_val = stats["mean_response"]
stddev_val = stats["stddev_response"]

anomalies_df = (
    logs_df
    .withColumn("z_score", (F.col("response_time_ms") - mean_val) / stddev_val)
    .withColumn("is_anomaly", F.abs(F.col("z_score")) > 3)
    .filter(F.col("is_anomaly") == True)
)

print(f"Total anomalies detected: {anomalies_df.count()}")
display(anomalies_df.orderBy(F.desc("response_time_ms")))


# ============================================================================
# SCENARIO 3: Data Quality Pipeline
# ============================================================================

"""
PROMPT: Build a pipeline to validate and clean incoming data
GOAL: Practice error handling, data validation, Delta MERGE
"""

# Cell 1: Generate Raw Data with Quality Issues
# THINK OUT LOUD:
# "Intentionally introducing data quality issues: nulls, duplicates, invalid values,
#  to simulate real-world ingestion challenges."

raw_data_spec = (
    dg.DataGenerator(spark, name="raw_sales", rows=5000, partitions=4)
    .withColumn("transaction_id", "string", template=r"TXN\d\d\d\d\d")
    .withColumn("product_id", "int", minValue=1, maxValue=100)
    .withColumn("quantity", "int", minValue=-5, maxValue=50)  # Some negative!
    .withColumn("price", "float", minValue=-10.0, maxValue=1000.0)  # Some negative!
    .withColumn("transaction_date", "date", begin="2025-01-01", end="2025-12-31")
)

raw_df = raw_data_spec.build()

# Introduce nulls (10%)
raw_df = raw_df.withColumn(
    "product_id",
    F.when(F.rand() < 0.1, None).otherwise(F.col("product_id"))
)

# Introduce duplicates
duplicates = raw_df.limit(50)
raw_df = raw_df.union(duplicates)

print(f"Total raw records: {raw_df.count()}")
display(raw_df)

# Cell 2: Data Quality Checks
# THINK OUT LOUD:
# "Implementing a validation framework. Tagging bad records instead of dropping
#  them so we can review and potentially fix issues."

validated_df = (
    raw_df
    .withColumn("is_valid", F.lit(True))
    .withColumn("validation_errors", F.array())

    # Check for nulls
    .withColumn("is_valid",
        F.when(F.col("product_id").isNull(), False)
        .otherwise(F.col("is_valid")))
    .withColumn("validation_errors",
        F.when(F.col("product_id").isNull(),
               F.array_union(F.col("validation_errors"), F.array(F.lit("NULL_PRODUCT_ID"))))
        .otherwise(F.col("validation_errors")))

    # Check for negative values
    .withColumn("is_valid",
        F.when((F.col("quantity") < 0) | (F.col("price") < 0), False)
        .otherwise(F.col("is_valid")))
    .withColumn("validation_errors",
        F.when(F.col("quantity") < 0,
               F.array_union(F.col("validation_errors"), F.array(F.lit("NEGATIVE_QUANTITY"))))
        .when(F.col("price") < 0,
               F.array_union(F.col("validation_errors"), F.array(F.lit("NEGATIVE_PRICE"))))
        .otherwise(F.col("validation_errors")))
)

# Separate valid and invalid records
valid_records = validated_df.filter(F.col("is_valid") == True)
invalid_records = validated_df.filter(F.col("is_valid") == False)

print(f"Valid records: {valid_records.count()}")
print(f"Invalid records: {invalid_records.count()}")

display(invalid_records)

# Cell 3: Deduplication
# THINK OUT LOUD:
# "Using dropDuplicates() to remove duplicates based on transaction_id.
#  Keeping the first occurrence based on arbitrary ordering."

clean_df = (
    valid_records
    .dropDuplicates(["transaction_id"])
    .select("transaction_id", "product_id", "quantity", "price", "transaction_date")
    .withColumn("total_amount", F.col("quantity") * F.col("price"))
)

print(f"Clean records after deduplication: {clean_df.count()}")
display(clean_df)

# Cell 4: Write to Delta with MERGE (Idempotent Pipeline)
# THINK OUT LOUD:
# "Using Delta MERGE for upsert logic. This makes the pipeline idempotent -
#  we can rerun it without creating duplicates."

# Create target table if not exists
clean_df.limit(0).write.format("delta").mode("overwrite").saveAsTable("sales_clean")

# MERGE statement
from delta.tables import DeltaTable

delta_table = DeltaTable.forName(spark, "sales_clean")

(delta_table.alias("target")
 .merge(
     clean_df.alias("source"),
     "target.transaction_id = source.transaction_id"
 )
 .whenMatchedUpdateAll()
 .whenNotMatchedInsertAll()
 .execute())

print("✅ Data merged into sales_clean table")

# Quarantine invalid records
invalid_records.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("sales_quarantine")

print("✅ Invalid records written to sales_quarantine table")


# ============================================================================
# SCENARIO 4: Performance Optimization Exercise
# ============================================================================

"""
PROMPT: Optimize a slow query
GOAL: Practice reading query plans, identifying bottlenecks, applying optimizations
"""

# Cell 1: Create a Slow Query (Intentionally Inefficient)
# Generate two large datasets
large_df1_spec = dg.DataGenerator(spark, rows=1000000, partitions=10) \
    .withColumn("id", "int", minValue=1, maxValue=1000000, uniqueValues=1000000) \
    .withColumn("category", "string", values=[f"cat_{i}" for i in range(100)]) \
    .withColumn("value", "float", minValue=0, maxValue=1000)

large_df1 = large_df1_spec.build()

large_df2_spec = dg.DataGenerator(spark, rows=1000000, partitions=10) \
    .withColumn("id", "int", minValue=1, maxValue=1000000) \
    .withColumn("metric", "float", minValue=0, maxValue=100)

large_df2 = large_df2_spec.build()

# SLOW VERSION: Multiple operations without optimization
# THINK OUT LOUD:
# "This query has several issues: no caching of reused DataFrames,
#  unnecessary shuffles, and no broadcast hints for joins."

slow_result = (
    large_df1
    .groupBy("category")
    .agg(F.avg("value").alias("avg_value"))
    .join(
        large_df2.groupBy("id").agg(F.sum("metric").alias("total_metric")),
        large_df1.select("id").distinct()  # This is problematic!
    )
    .filter(F.col("avg_value") > 500)
)

# Show query plan
print("=== SLOW QUERY PLAN ===")
slow_result.explain(mode="formatted")

# Cell 2: Optimized Version
# THINK OUT LOUD:
# "Optimizations applied:
#  1. Cache large_df1 since it's used multiple times
#  2. Broadcast join for small aggregated results
#  3. Predicate pushdown by filtering early
#  4. Proper join condition"

large_df1.cache()
large_df1.count()  # Trigger caching

# Filter early (predicate pushdown)
filtered_df1 = large_df1.filter(F.col("value") > 500)

# Aggregate
agg_df1 = filtered_df1.groupBy("category").agg(F.avg("value").alias("avg_value"))

# If the aggregated result is small, broadcast it
optimized_result = (
    filtered_df1
    .join(F.broadcast(agg_df1), "category", "inner")
    .select("id", "category", "value", "avg_value")
)

print("=== OPTIMIZED QUERY PLAN ===")
optimized_result.explain(mode="formatted")

display(optimized_result.limit(100))


# ============================================================================
# PRACTICE EXERCISE: Think Out Loud Template
# ============================================================================

"""
Use this template when solving problems in the interview:

1. RESTATE THE PROBLEM
   "So we need to [summarize the ask]. The expected output is [describe output]."

2. ASK CLARIFYING QUESTIONS
   "Quick questions: What's the expected data volume? Any specific performance requirements?
    Are there data quality issues I should anticipate?"

3. OUTLINE YOUR APPROACH
   "Here's how I'll tackle this:
    Step 1: Generate synthetic data with [characteristics]
    Step 2: Clean/validate the data
    Step 3: Apply transformations [list key operations]
    Step 4: Aggregate/analyze
    Step 5: Write results to Delta"

4. THINK OUT LOUD WHILE CODING
   "I'm using a log-normal distribution here because..."
   "This will trigger a shuffle, but it's necessary for..."
   "Let me validate this intermediate result before proceeding..."
   "I notice the AI suggested X, but that won't scale because..."

5. EXPLAIN TRADE-OFFS
   "I could cache this DataFrame, but given the size, the overhead might not be worth it"
   "Option A is simpler but slower. Option B is more complex but scales better.
    I'll go with A for this dataset size."

6. VALIDATE AND TEST
   "Let me check: row count looks right, no nulls where unexpected,
    data types are correct, business logic validates"

7. DISCUSS SCALABILITY
   "This works for our current volume. If we scaled to billions of rows,
    I'd consider partitioning by date, using Z-order clustering,
    and implementing incremental processing"
"""


# ============================================================================
# COMMON ANTI-PATTERNS TO AVOID
# ============================================================================

# ❌ BAD: Using collect() on large DataFrames
def bad_pattern_1(df):
    rows = df.collect()  # OOM risk!
    for row in rows:
        print(row)

# ✅ GOOD: Use distributed operations
def good_pattern_1(df):
    df.show()  # Or write to storage
    # If you need to process: use map/foreach with distributed operations


# ❌ BAD: Row-by-row operations
def bad_pattern_2(df):
    result = []
    for row in df.collect():
        result.append(row.value * 2)
    return spark.createDataFrame(result)

# ✅ GOOD: Vectorized operations
def good_pattern_2(df):
    return df.withColumn("doubled", F.col("value") * 2)


# ❌ BAD: Ignoring data skew
def bad_pattern_3(df):
    # One key has 90% of data
    df.groupBy("skewed_key").agg(F.sum("value"))

# ✅ GOOD: Salt the key
def good_pattern_3(df):
    df_salted = df.withColumn("salt", (F.rand() * 10).cast("int"))
    intermediate = df_salted.groupBy("skewed_key", "salt").agg(F.sum("value").alias("partial_sum"))
    final = intermediate.groupBy("skewed_key").agg(F.sum("partial_sum").alias("total"))
    return final


# ❌ BAD: Multiple passes over data
def bad_pattern_4(df):
    count1 = df.filter(F.col("status") == "A").count()
    count2 = df.filter(F.col("status") == "B").count()
    return count1, count2

# ✅ GOOD: Single aggregation
def good_pattern_4(df):
    result = df.groupBy("status").count().collect()
    counts = {row.status: row.count for row in result}
    return counts.get("A", 0), counts.get("B", 0)


print("✅ All practice scenarios loaded!")
print("Copy these into Databricks notebooks and practice thinking out loud while executing.")
