# Curveball Scenario Drills - Practice These Until Automatic

These are the "gotcha" scenarios that separate good from great candidates. Practice these until you can execute AND explain them in under 5 minutes each.

---

## 🎯 Curveball #1: "Scale This from 10k to 100M Records"

### Setup (What You Just Built)
```python
# You successfully created this with small data
customers = spark.range(10000).withColumn(
    "name", concat(lit("Customer_"), col("id").cast("string"))
)

transactions = spark.range(100000).withColumn(
    "customer_id", (rand() * 10000).cast("int")
).withColumn("amount", rand() * 1000)

clv = transactions.groupBy("customer_id").agg(
    sum("amount").alias("total_revenue"),
    count("*").alias("num_transactions")
).join(customers, "customer_id")

clv.write.format("delta").mode("overwrite").saveAsTable("customer_metrics")
```

### 🔴 CURVEBALL
**Interviewer**: *"Great! Now what if instead of 100k transactions, we have 100 million? Walk me through how you'd modify this."*

### ✅ PERFECT RESPONSE (Think Out Loud)

**Step 1: Pause and Analyze (15 seconds)**
"Let me think through the implications. With 100M transactions, we're looking at approximately 100M * 100 bytes = ~10GB of data, assuming simple schema. The key bottleneck will be the groupBy shuffle. Let me identify what needs to change."

**Step 2: Explain Your Strategy (30 seconds)**
```
"Here's my optimization approach:

1. PARTITIONS: Default 200 shuffle partitions may be too low for 10GB
   → I'll calculate: 10GB / 0.5GB = ~20 partitions minimum
   → I'll set to 100 for good parallelism

2. BROADCAST: Customer table is still 10k rows (~1MB)
   → Can still broadcast to avoid shuffle on join

3. CACHING: If we're doing multiple operations on the result,
   → Cache after the expensive groupBy

4. INCREMENTAL: For production, I'd switch to Delta MERGE
   → Process only new transactions vs full refresh

5. PARTITIONING: Partition output by time period for better queries
   → e.g., partition by year/month for time-range filters
"
```

**Step 3: Demonstrate the Changes (2 minutes)**
```python
# 1. Adjust shuffle partitions
spark.conf.set("spark.sql.shuffle.partitions", "100")
print(f"Set shuffle partitions to 100 (calculated from data size)")

# 2. Generate large dataset
print("Generating 100M transactions...")
large_transactions = spark.range(100000000).withColumn(
    "customer_id", (rand() * 10000).cast("int")
).withColumn(
    "amount", rand() * 1000
).withColumn(
    "transaction_date", date_add(current_date(), -(rand() * 365).cast("int"))
)

# 3. Explain the query plan BEFORE optimization
print("Let me show you the query plan first...")
test_query = large_transactions.groupBy("customer_id").agg(
    sum("amount").alias("total_revenue")
).join(customers, "customer_id")

test_query.explain("formatted")
print("Note the Exchange (shuffle) on the groupBy and the join strategy")

# 4. Apply optimizations
print("Now with optimizations...")
clv_large = (
    large_transactions
    .groupBy("customer_id")
    .agg(
        sum("amount").alias("total_revenue"),
        count("*").alias("num_transactions"),
        max("transaction_date").alias("last_transaction_date")
    )
)

# Cache if we'll reuse this result
clv_large.cache()
clv_large.count()  # Trigger caching
print(f"Cached groupBy result with {clv_large.rdd.getNumPartitions()} partitions")

# 5. Broadcast join the small customer table
final = clv_large.join(broadcast(customers), "customer_id")

# 6. Write with partitioning for query optimization
final.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("last_transaction_date")  # If you added date columns \
    .option("optimizeWrite", "true") \
    .saveAsTable("customer_metrics_large")

print("✅ Optimizations applied:")
print("  - Shuffle partitions: 100")
print("  - Broadcast join on customers table")
print("  - Cached intermediate aggregation")
print("  - Partitioned output by date for query optimization")
```

**Step 4: Explain Further Optimizations (30 seconds)**
"If we needed to scale even further to billions of records, I would:
1. Use **Adaptive Query Execution (AQE)** to auto-tune partitions
2. Implement **incremental processing** with Delta MERGE to avoid full scans
3. Consider **Z-ordering** on customer_id for better data skipping
4. Monitor partition skew and apply **salting** if needed"

---

## 🎯 Curveball #2: "I'm Adding Data Skew - Handle It"

### Setup
```python
# You built this
transactions = spark.range(1000000).withColumn(
    "customer_id", (rand() * 10000).cast("int")
).withColumn("amount", rand() * 1000)

clv = transactions.groupBy("customer_id").agg(sum("amount").alias("total_revenue"))
```

### 🔴 CURVEBALL
**Interviewer**: *"Let's make this realistic. 80% of transactions come from the top 5 customers - heavy skew. How do you handle this?"*

### ✅ PERFECT RESPONSE

**Step 1: Acknowledge and Detect (20 seconds)**
"Data skew is when some partitions have significantly more data than others. This causes stragglers - one task takes 10x longer while other executors sit idle. Let me first demonstrate how to detect it, then fix it."

**Step 2: Generate Skewed Data & Detect**
```python
# Generate heavily skewed data
skewed_txn = spark.range(1000000).withColumn(
    "customer_id",
    when(rand() < 0.8, (rand() * 5).cast("int"))  # 80% in 5 customers
    .otherwise((rand() * 10000).cast("int"))
).withColumn("amount", rand() * 1000)

# DETECTION: Check partition sizes after groupBy
skewed_grouped = skewed_txn.groupBy("customer_id").agg(sum("amount").alias("revenue"))

print("Checking partition sizes...")
partition_sizes = skewed_grouped.rdd.mapPartitions(
    lambda it: [sum(1 for _ in it)]
).collect()
print(f"Partition sizes: {partition_sizes}")
print(f"Max/Min ratio: {max(partition_sizes) / (min(partition_sizes) + 1)}")
# Ratio > 10 indicates significant skew
```

**Step 3: Explain Salting Strategy (30 seconds)**
"To handle skew, I'll use **salting**. The idea is:
1. Add a random 'salt' to the skewed key (e.g., customer_id → customer_id_0, customer_id_1, ...)
2. This distributes hot keys across multiple partitions
3. Do a partial aggregation with the salt
4. Then re-aggregate without the salt to get final results

This turns one slow task into N parallel tasks."

**Step 4: Implement Salting**
```python
from pyspark.sql.functions import rand, col, sum as _sum, count, lit

print("Applying salting technique...")

# 1. Add random salt (0-9)
NUM_SALTS = 10
salted = skewed_txn.withColumn(
    "salt", (rand() * NUM_SALTS).cast("int")
)

print(f"Added salt column with {NUM_SALTS} buckets")

# 2. Partial aggregation WITH salt
# This distributes each customer_id across 10 partitions
partial_agg = salted.groupBy("customer_id", "salt").agg(
    _sum("amount").alias("partial_revenue"),
    count("*").alias("partial_count")
)

print("Partial aggregation complete - hot keys now distributed")
partial_agg.show(20)

# 3. Final aggregation WITHOUT salt
# Combine the partial results
final_agg = partial_agg.groupBy("customer_id").agg(
    _sum("partial_revenue").alias("total_revenue"),
    _sum("partial_count").alias("total_transactions")
)

print("Final aggregation complete")

# 4. Verify improvement
print("\nChecking partition sizes after salting...")
final_partition_sizes = final_agg.rdd.mapPartitions(
    lambda it: [sum(1 for _ in it)]
).collect()
print(f"New partition sizes: {final_partition_sizes}")
print(f"New Max/Min ratio: {max(final_partition_sizes) / (min(final_partition_sizes) + 1)}")

# 5. Compare query plans
print("\n=== BEFORE SALTING ===")
skewed_txn.groupBy("customer_id").agg(_sum("amount")).explain("formatted")

print("\n=== AFTER SALTING ===")
final_agg.explain("formatted")
print("Note: More parallel tasks in the partial aggregation stage")
```

**Step 5: Alternative Solutions (30 seconds)**
"Salting is one approach. Depending on the scenario, I might also:

1. **Broadcast Join** (if joining skewed table with small table):
   - Hot keys don't matter since small table goes to all executors

2. **Isolate Hot Keys** (if only a few hot keys):
   ```python
   hot_keys = [0, 1, 2, 3, 4]
   hot_data = skewed_txn.filter(col("customer_id").isin(hot_keys))
   normal_data = skewed_txn.filter(~col("customer_id").isin(hot_keys))

   # Process separately with different strategies
   hot_result = hot_data.groupBy("customer_id").agg(...)  # Single partition OK
   normal_result = normal_data.groupBy("customer_id").agg(...)  # Distributed

   combined = hot_result.union(normal_result)
   ```

3. **Increase Partitions** (quick fix, not ideal):
   - More partitions = smaller max partition size
   - `spark.conf.set('spark.sql.shuffle.partitions', '400')`"

---

## 🎯 Curveball #3: "Design This as Extensible Architecture"

### 🔴 CURVEBALL
**Interviewer**: *"This works for now, but how would you design this to accommodate new datasets in the future? Think about a production data platform."*

### ✅ PERFECT RESPONSE

**Step 1: Explain Medallion Architecture (1 minute)**
"I'd implement a **Medallion Architecture** with a **Star Schema** design:

**Bronze Layer** (Raw):
- Land data as-is from sources
- Minimal transformation
- Append-only for audit trail

**Silver Layer** (Cleaned):
- Data quality checks applied
- Deduplicated
- Separated into Facts (events/transactions) and Dimensions (entities)
- Conformed data types and naming

**Gold Layer** (Business):
- Aggregated metrics
- Denormalized for query performance
- Optimized for specific use cases (dashboards, reports)

This design allows:
✅ New datasets integrate at Bronze without disrupting existing flows
✅ Facts and Dims can be joined in any combination
✅ Quality issues quarantined in Silver, don't pollute Gold
✅ Incremental processing via Delta MERGE"

**Step 2: Demonstrate the Design**
```python
from delta.tables import DeltaTable
from pyspark.sql.functions import current_timestamp, lit

# ============================================================
# BRONZE LAYER: Raw Ingestion
# ============================================================
print("=== BRONZE LAYER: Raw Data Landing ===")

# Simulate raw data landing
raw_customers = spark.range(10000).withColumn(
    "name", concat(lit("Customer_"), col("id").cast("string"))
).withColumn("_ingestion_timestamp", current_timestamp())

raw_transactions = spark.range(100000).withColumn(
    "customer_id", (rand() * 10000).cast("int")
).withColumn("amount", rand() * 1000) \
 .withColumn("transaction_date", current_date()) \
 .withColumn("_ingestion_timestamp", current_timestamp())

# Write to Bronze - append only, no transformations
raw_customers.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable("bronze.raw_customers")

raw_transactions.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable("bronze.raw_transactions")

print("✅ Raw data landed in Bronze")

# ============================================================
# SILVER LAYER: Cleaned Facts & Dimensions
# ============================================================
print("\n=== SILVER LAYER: Cleaned Facts & Dimensions ===")

# DIMENSION: Customers (SCD Type 2 for history tracking)
dim_customers = spark.read.format("delta").table("bronze.raw_customers") \
    .dropDuplicates(["id"]) \
    .select(
        col("id").alias("customer_id"),
        col("name"),
        col("_ingestion_timestamp").alias("effective_from"),
        lit(None).cast("timestamp").alias("effective_to"),
        lit(True).alias("is_current")
    )

# Write dimension with MERGE for SCD Type 2
dim_customers.write.format("delta") \
    .mode("overwrite") \
    .option("mergeSchema", "true") \
    .saveAsTable("silver.dim_customers")

print("✅ Dimension table created: dim_customers")

# FACT: Transactions (event grain)
fact_transactions = spark.read.format("delta").table("bronze.raw_transactions") \
    .filter(col("amount") > 0) \
    .dropDuplicates(["id"]) \
    .select(
        col("id").alias("transaction_id"),
        col("customer_id"),
        col("amount"),
        col("transaction_date"),
        col("_ingestion_timestamp")
    )

# Write fact table partitioned by date
fact_transactions.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("transaction_date") \
    .saveAsTable("silver.fact_transactions")

print("✅ Fact table created: fact_transactions (partitioned by date)")

# ============================================================
# GOLD LAYER: Business Metrics
# ============================================================
print("\n=== GOLD LAYER: Aggregated Business Metrics ===")

# Metric 1: Customer Lifetime Value (CLV)
gold_clv = spark.read.format("delta").table("silver.fact_transactions") \
    .join(
        spark.read.format("delta").table("silver.dim_customers"),
        "customer_id",
        "inner"
    ) \
    .groupBy("customer_id", "name") \
    .agg(
        _sum("amount").alias("total_revenue"),
        count("transaction_id").alias("transaction_count"),
        max("transaction_date").alias("last_purchase_date")
    ) \
    .withColumn("as_of_date", current_date())

gold_clv.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold.customer_lifetime_value")

print("✅ Gold metric created: customer_lifetime_value")

# Metric 2: Daily Revenue (Time-series for dashboards)
gold_daily_revenue = spark.read.format("delta").table("silver.fact_transactions") \
    .groupBy("transaction_date") \
    .agg(
        _sum("amount").alias("total_revenue"),
        count("transaction_id").alias("transaction_count")
    ) \
    .withColumn("as_of_date", current_date())

gold_daily_revenue.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold.daily_revenue")

print("✅ Gold metric created: daily_revenue")

print("\n" + "="*60)
print("ARCHITECTURE SUMMARY")
print("="*60)
print("Bronze: bronze.raw_customers, bronze.raw_transactions")
print("Silver: silver.dim_customers, silver.fact_transactions")
print("Gold:   gold.customer_lifetime_value, gold.daily_revenue")
```

**Step 3: Explain Extensibility (1 minute)**
"Now if we need to add new datasets:

**New Fact (e.g., Returns)**:
```python
# 1. Land in Bronze
bronze.raw_returns

# 2. Clean in Silver
silver.fact_returns  # Same pattern as fact_transactions

# 3. Join to existing dims in Gold
gold.return_metrics = fact_returns
    .join(dim_customers, 'customer_id')
    .join(dim_products, 'product_id')  # New dim!
```

**New Dimension (e.g., Products)**:
```python
# Add new dimension
silver.dim_products

# Extend existing facts with FK
ALTER TABLE silver.fact_transactions ADD COLUMN product_id INT

# Now Gold layer can slice by product
gold.product_revenue = fact_transactions
    .join(dim_products, 'product_id')
    .groupBy('product_id', 'product_name')
    .agg(sum('amount'))
```

**Benefits**:
✅ **Separation of Concerns**: Raw, Clean, Business logic isolated
✅ **Star Schema**: Easy to add dimensions without changing facts
✅ **Incremental**: Delta MERGE for idempotent updates
✅ **Auditable**: Bronze preserves raw data for compliance
✅ **Testable**: Can test Silver transformations independently"

---

## 🎯 Curveball #4: "Optimize This Slow Join"

### 🔴 CURVEBALL
**Interviewer**: *"The join is taking forever. Walk me through how you'd debug and optimize it."*

### ✅ PERFECT RESPONSE

**Step 1: Analyze the Query Plan (1 minute)**
```python
# Current slow query
result = large_df1.join(large_df2, "key_column")

print("Let me check the query plan to identify the bottleneck...")
result.explain("formatted")

print("\nLooking for:")
print("1. Exchange (shuffle) operations - these are expensive")
print("2. Join strategy - is it Sort-Merge or Broadcast?")
print("3. CartesianProduct - this would be a major problem")
print("4. Number of partitions involved")
```

**Step 2: Diagnose Common Issues**
```python
print("\n=== DIAGNOSTICS ===")

# Check 1: Table sizes
print(f"Table 1 size: {large_df1.count()} rows")
print(f"Table 2 size: {large_df2.count()} rows")

# Check 2: Join key cardinality
print(f"Distinct keys in table 1: {large_df1.select('key_column').distinct().count()}")
print(f"Distinct keys in table 2: {large_df2.select('key_column').distinct().count()}")

# Check 3: Data skew
print("\nChecking for skew in join key...")
skew_check = large_df1.groupBy("key_column").count() \
    .orderBy(col("count").desc()) \
    .limit(10)
skew_check.show()
print("If top keys have 10x+ more records, we have skew")

# Check 4: Partition count
print(f"\nTable 1 partitions: {large_df1.rdd.getNumPartitions()}")
print(f"Table 2 partitions: {large_df2.rdd.getNumPartitions()}")
```

**Step 3: Apply Optimizations Based on Diagnosis**
```python
print("\n=== OPTIMIZATION STRATEGY ===")

# SCENARIO 1: One table is small (<10GB)
if small_enough:
    print("✅ One table is small - using BROADCAST JOIN")
    optimized = large_df1.join(broadcast(small_df2), "key_column")

# SCENARIO 2: Both large, need sort-merge optimization
else:
    print("✅ Both tables large - optimizing SORT-MERGE JOIN")

    # A) Pre-partition both tables by join key
    print("Pre-partitioning by join key...")
    df1_partitioned = large_df1.repartition(200, "key_column")
    df2_partitioned = large_df2.repartition(200, "key_column")

    # B) Cache if tables reused
    df1_partitioned.cache().count()
    df2_partitioned.cache().count()

    # C) Now join
    optimized = df1_partitioned.join(df2_partitioned, "key_column")

    print("Partitioning ensures no shuffle during join")

# SCENARIO 3: Data skew detected
if skewed:
    print("✅ Data skew detected - using SALTED JOIN")

    # Salt the skewed table
    salted_df1 = large_df1.withColumn("salt", (rand() * 10).cast("int"))

    # Replicate the other table with all salt values
    salt_df = spark.range(10).withColumnRenamed("id", "salt")
    replicated_df2 = large_df2.crossJoin(salt_df)

    # Join with salt
    partial_join = salted_df1.join(
        replicated_df2,
        (salted_df1["key_column"] == replicated_df2["key_column"]) &
        (salted_df1["salt"] == replicated_df2["salt"])
    )

    # Remove salt
    optimized = partial_join.drop("salt")

print("\n=== VALIDATION ===")
print("Comparing query plans...")
print("\nBEFORE:")
result.explain("simple")
print("\nAFTER:")
optimized.explain("simple")

print("\nKey improvements:")
print("- Shuffle operations: reduced from X to Y")
print("- Join strategy: changed from Sort-Merge to Broadcast")
print("- Estimated speedup: [based on plan analysis]")
```

---

## 🎯 RAPID-FIRE DRILL: One-Minute Explanations

Practice explaining these in under 60 seconds each:

### Q1: "What causes a shuffle?"
**A**: "A shuffle happens when data needs to be redistributed across partitions. This occurs in wide transformations like groupBy, join (non-broadcast), distinct, orderBy, and repartition. During a shuffle, Spark writes intermediate data to disk, transfers it across the network, and deserializes it - making it expensive. Narrow transformations like filter and select don't shuffle because each partition is processed independently."

### Q2: "When would you use broadcast join vs sort-merge join?"
**A**: "Broadcast join when one table is small - under 10GB by default. The small table is sent to all executors, avoiding a shuffle. It's the fastest option. Sort-merge join when both tables are large - Spark sorts and partitions both tables by the join key, then merges matching keys. It requires a shuffle but scales to any size."

### Q3: "Explain salting for data skew"
**A**: "Salting distributes hot keys across multiple partitions by adding a random salt value. For example, customer_id=5 becomes customer_id=5_0, customer_id=5_1, etc. We do a partial aggregation with the salt, which spreads the work across partitions, then re-aggregate without the salt to get final results. This turns one slow task into N parallel tasks."

### Q4: "How do you choose partition count?"
**A**: "Aim for 100MB to 1GB per partition. Quick formula: data size in GB divided by 0.5. Also ensure 2-4 partitions per CPU core for good parallelism. Too few partitions means each is too large - memory pressure and stragglers. Too many means overhead from task scheduling. Use `spark.sql.shuffle.partitions` to adjust."

### Q5: "Delta Lake MERGE vs INSERT?"
**A**: "INSERT appends new rows - simple but creates duplicates if rerun. MERGE is an upsert - updates existing rows and inserts new ones based on a condition. It makes pipelines idempotent - safe to rerun without creating duplicates. Use MERGE for production pipelines where data might arrive late or need reprocessing."

---

## ✅ Practice Checklist

For each curveball, can you:
- [ ] Explain the strategy in 30 seconds
- [ ] Write the code in 2-3 minutes
- [ ] Explain why this approach works
- [ ] Identify when NOT to use this approach
- [ ] Show the difference in query plans

If yes to all → You're ready! 🚀
If no → Practice that scenario again
