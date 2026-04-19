# Interview Day Quick Reference - Keep This Open

**Interview Date: April 24th, 2026**

---

## 🚀 Pre-Interview Setup (Do This First!)

```python
# 1. Start cluster (takes 2-3 mins - do early!)

# 2. Create workspace
%sql
CREATE CATALOG IF NOT EXISTS vibe_interview;
USE CATALOG vibe_interview;
CREATE SCHEMA IF NOT EXISTS main;
USE SCHEMA main;

# 3. Install packages
%pip install dbldatagen faker

# 4. Import commonly used libraries
import dbldatagen as dg
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from delta.tables import DeltaTable
from pyspark.sql.functions import (
    col, lit, when, concat, rand, current_date, current_timestamp,
    sum as _sum, avg, count, max as _max, min as _min,
    broadcast, window, lag, lead, row_number, rank, dense_rank, ntile
)

print("✅ Environment ready!")
```

---

## 📊 Synthetic Data Generation Templates

### Template 1: Basic Table with dbldatagen
```python
spec = (
    dg.DataGenerator(spark, name="table_name", rows=10000, partitions=4)
    .withColumn("id", "int", minValue=1, maxValue=10000, uniqueValues=10000)
    .withColumn("name", "string", template=r"\w \w")  # Random words
    .withColumn("email", "string", template=r"\w.\ w@\w.com")
    .withColumn("amount", "float", minValue=10, maxValue=1000,
                distribution="log-normal")  # Realistic spending
    .withColumn("category", "string",
                values=["A", "B", "C"], weights=[50, 30, 20])
    .withColumn("date", "date", begin="2025-01-01", end="2025-12-31")
)
df = spec.build()
```

### Template 2: Introduce Data Quality Issues
```python
# Add nulls (5%)
df = df.withColumn("col_name",
    when(rand() < 0.05, None).otherwise(col("col_name")))

# Add duplicates
duplicates = df.limit(50)
df = df.union(duplicates)

# Add skew (80% in hot keys)
df = df.withColumn("key",
    when(rand() < 0.8, (rand() * 5).cast("int"))  # Hot keys: 0-4
    .otherwise((rand() * 10000).cast("int")))      # Normal keys
```

### Template 3: Quick Faker-based Generation
```python
from faker import Faker
fake = Faker()

# For small datasets or demos
data = [(i, fake.name(), fake.email(), fake.date_between(start_date='-1y'))
        for i in range(1000)]
df = spark.createDataFrame(data, ["id", "name", "email", "signup_date"])
```

---

## 🔍 Essential Validation Checks

```python
# ALWAYS validate your generated data!

# Schema check
df.printSchema()

# Row count & sample
print(f"Total rows: {df.count()}")
df.show(5, truncate=False)

# Distribution check
df.describe().show()

# Null check
df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns]).show()

# Distinct values
df.select("key_col").distinct().count()

# Referential integrity (for joins)
orphaned = df1.join(df2, "key", "left_anti")
print(f"Orphaned records: {orphaned.count()}")
```

---

## 🎯 Common PySpark Patterns

### Aggregations
```python
# Basic aggregation
df.groupBy("category").agg(
    _sum("amount").alias("total"),
    avg("amount").alias("average"),
    count("*").alias("count"),
    _max("date").alias("latest_date")
)

# Multiple aggregations
df.groupBy("category", "region").agg(
    _sum("revenue").alias("total_revenue"),
    count("transaction_id").alias("num_transactions"),
    F.approx_count_distinct("customer_id").alias("unique_customers")
)
```

### Window Functions
```python
# Define window
window_spec = Window.partitionBy("category").orderBy("date")

# Ranking
df.withColumn("row_num", row_number().over(window_spec))
df.withColumn("rank", rank().over(window_spec))
df.withColumn("quartile", ntile(4).over(window_spec))

# Lag/Lead
df.withColumn("prev_value", lag("amount", 1).over(window_spec))
df.withColumn("next_value", lead("amount", 1).over(window_spec))

# Running totals
df.withColumn("running_total", _sum("amount").over(window_spec))

# Moving average (last 3 rows)
window_3 = Window.partitionBy("category").orderBy("date").rowsBetween(-2, 0)
df.withColumn("ma_3", avg("amount").over(window_3))
```

### Joins
```python
# Broadcast join (small table)
large_df.join(broadcast(small_df), "key", "inner")

# Sort-merge join (both large, pre-partitioned)
df1_part = df1.repartition(100, "key")
df2_part = df2.repartition(100, "key")
df1_part.join(df2_part, "key", "inner")

# Join types
.join(other, "key", "inner")    # Only matches
.join(other, "key", "left")     # All from left
.join(other, "key", "outer")    # All from both
.join(other, "key", "left_anti") # Left without matches (orphan check)
```

---

## ⚡ Performance Optimization Quick Fixes

### Check Query Plan
```python
# Quick plan
df.explain("simple")

# Detailed plan
df.explain("formatted")

# Look for:
# - "Exchange" = shuffle (expensive!)
# - "BroadcastExchange" = broadcast join (good if small table)
# - "CartesianProduct" = cross join (usually bad!)
```

### Adjust Partitions
```python
# Too many small partitions after filter
df_filtered.coalesce(10)  # Reduce without shuffle

# Not enough partitions for large data
df.repartition(200)  # Full shuffle to increase

# Partition by column (for joins)
df.repartition(100, "customer_id")

# Set shuffle partition default
spark.conf.set("spark.sql.shuffle.partitions", "200")
```

### Caching
```python
# Cache if DataFrame used multiple times
df.cache()
df.count()  # Trigger caching
# ... use df multiple times ...
df.unpersist()  # Free memory when done

# Check what's cached
spark.catalog.listTables()
```

### Broadcast
```python
# Auto-broadcast threshold (default 10MB)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 10 * 1024 * 1024)

# Manual broadcast (for tables < 10GB)
large_df.join(broadcast(small_df), "key")
```

---

## 🔥 Data Skew - Copy-Paste Solutions

### Detect Skew
```python
# Check partition sizes
partition_sizes = df.rdd.mapPartitions(lambda it: [sum(1 for _ in it)]).collect()
print(f"Partition sizes: {partition_sizes}")
print(f"Skew ratio: {max(partition_sizes) / (min(partition_sizes) + 1)}")
# Ratio > 10 = significant skew

# Check key distribution
df.groupBy("key_col").count().orderBy(col("count").desc()).show(20)
# Top keys 10x+ more = skew
```

### Fix Skew: Salting (Aggregations)
```python
# 1. Add salt
NUM_SALTS = 10
salted = df.withColumn("salt", (rand() * NUM_SALTS).cast("int"))

# 2. Partial aggregation with salt
partial = salted.groupBy("skewed_key", "salt").agg(
    _sum("value").alias("partial_sum"),
    count("*").alias("partial_count")
)

# 3. Final aggregation without salt
final = partial.groupBy("skewed_key").agg(
    _sum("partial_sum").alias("total"),
    _sum("partial_count").alias("count")
)
```

### Fix Skew: Broadcast (Joins)
```python
# If skewed table can be broadcasted
large_skewed.join(broadcast(small_table), "key")
```

### Fix Skew: Isolate Hot Keys
```python
# Separate hot keys and process differently
hot_keys = [1, 2, 3]
hot_data = df.filter(col("key").isin(hot_keys))
normal_data = df.filter(~col("key").isin(hot_keys))

# Process separately
hot_result = hot_data.groupBy("key").agg(...)  # Single partition OK
normal_result = normal_data.groupBy("key").agg(...)  # Distributed

# Combine
result = hot_result.union(normal_result)
```

---

## 📦 Delta Lake Operations

### Write
```python
# Overwrite
df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("table_name")

# Append
df.write.format("delta") \
    .mode("append") \
    .saveAsTable("table_name")

# Partition by column
df.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("year", "month") \
    .saveAsTable("table_name")

# Allow schema changes
df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable("table_name")
```

### Read
```python
# Read latest
df = spark.read.format("delta").table("table_name")

# Time travel - by version
df = spark.read.format("delta") \
    .option("versionAsOf", 5) \
    .table("table_name")

# Time travel - by timestamp
df = spark.read.format("delta") \
    .option("timestampAsOf", "2025-01-01") \
    .table("table_name")
```

### MERGE (Upsert - CRITICAL for idempotency!)
```python
from delta.tables import DeltaTable

delta_table = DeltaTable.forName(spark, "target_table")

(delta_table.alias("target")
 .merge(
     source_df.alias("source"),
     "target.id = source.id"  # Match condition
 )
 .whenMatchedUpdate(set={  # If exists, update
     "value": "source.value",
     "updated_at": "current_timestamp()"
 })
 .whenNotMatchedInsert(values={  # If new, insert
     "id": "source.id",
     "value": "source.value",
     "created_at": "current_timestamp()"
 })
 .execute())

print("✅ MERGE complete - pipeline is idempotent!")
```

### Optimize & Vacuum
```python
# Compact small files
spark.sql("OPTIMIZE delta.`/path/to/table`")

# Z-order for better data skipping
spark.sql("OPTIMIZE delta.`/path/to/table` ZORDER BY (customer_id)")

# Remove old files (7 days retention)
spark.sql("VACUUM delta.`/path/to/table` RETAIN 168 HOURS")
```

---

## 💬 Think-Out-Loud Phrases (Use These!)

### When generating data:
- "I'm using log-normal distribution because real-world spending follows this pattern"
- "I'm introducing 5% nulls to simulate realistic data quality issues"
- "Let me validate the data before proceeding - checking schema, row count, and distributions"

### When joining:
- "I'm using broadcast join here because the dimension table is small - under 10GB"
- "This join will trigger a shuffle since both tables are large - I'll check the query plan"
- "Let me pre-partition both tables on the join key to avoid shuffle during the join"

### When aggregating:
- "This groupBy will trigger a shuffle to co-locate records with the same key"
- "I'm seeing data skew - 80% of data in a few keys - I'll apply salting"
- "Let me check partition sizes after the aggregation to ensure balanced distribution"

### When debugging:
- "I see an AnalysisException - let me read the error... it's a column name mismatch"
- "This is taking longer than expected - let me check the query plan with .explain()"
- "I'm seeing a shuffle here that I didn't expect - let me investigate why"

### When scaling:
- "For 100M records, I'd increase shuffle partitions from 200 to about 200-400"
- "I'd cache this DataFrame since we're using it multiple times - that's a 2x speedup"
- "For production, I'd switch to Delta MERGE for incremental processing instead of full refresh"

### When optimizing:
- "I see an opportunity for predicate pushdown - filtering before reading reduces I/O"
- "The default broadcast threshold is 10MB - I'll manually broadcast this 100MB table"
- "I'm partitioning the output by date so time-range queries only read relevant partitions"

---

## 🎯 Scenario Workflow Template

Use this structure for ANY scenario:

```python
# ============================================================
# PHASE 1: CLARIFY & SPEC (5 mins)
# ============================================================
"""
QUESTIONS TO ASK:
1. What industry are we modeling?
2. What's the expected data volume?
3. What's the grain of each dataset?
4. What metrics do we need to calculate?
5. What's the output format?

SPEC:
- Dataset 1: [name] with [N] rows, grain = [one row per X]
- Dataset 2: [name] with [N] rows, grain = [one row per Y]
- Metrics: [list 3-5 metrics]
- Output: Delta table + visualization
"""

# ============================================================
# PHASE 2: GENERATE DATA (10 mins)
# ============================================================
# Generate datasets (use templates above)
# VALIDATE: schema, counts, distributions, referential integrity

# ============================================================
# PHASE 3: TRANSFORM & AGGREGATE (25 mins)
# ============================================================
# Clean data
# Join datasets
# Calculate metrics
# THINK OUT LOUD the entire time!

# ============================================================
# PHASE 4: WRITE & VISUALIZE (10 mins)
# ============================================================
# Write to Delta
# Create simple visualization
# Explain what you built

# ============================================================
# PHASE 5: HANDLE CURVEBALLS (10 mins)
# ============================================================
# "Scale this to 100M records" → See CURVEBALL_DRILLS.md
# "Handle data skew" → See CURVEBALL_DRILLS.md
# "Extend architecture" → See CURVEBALL_DRILLS.md
```

---

## 🚨 Common Errors & Quick Fixes

### Error: Column not found
```python
# Check schema
df.printSchema()

# Check column names
df.columns

# Case sensitivity issue?
spark.conf.set("spark.sql.caseSensitive", "false")
```

### Error: AnalysisException (ambiguous column)
```python
# Use aliases
df1.alias("a").join(df2.alias("b"), "key").select("a.col", "b.col")
```

### Error: Out of Memory
```python
# Don't collect large DataFrames!
# df.collect()  # ❌ BAD

# Use distributed operations
df.write.parquet("output")  # ✅ GOOD

# Or show sample
df.show(100)
```

### Error: Slow query / Hanging
```python
# Check if broadcast is too large
spark.conf.get("spark.sql.autoBroadcastJoinThreshold")

# Check partition count
df.rdd.getNumPartitions()

# Kill and re-run with adjustments
spark.conf.set("spark.sql.shuffle.partitions", "400")
```

---

## ✅ Pre-Interview Final Checklist

- [ ] Cluster started and running
- [ ] Catalog/schema created
- [ ] Packages installed (dbldatagen, faker)
- [ ] Test query executed successfully
- [ ] Databricks Assistant tested
- [ ] Screen sharing working
- [ ] This cheat sheet open in browser
- [ ] CURVEBALL_DRILLS.md open in another tab
- [ ] Water bottle nearby
- [ ] Phone on silent
- [ ] Confident mindset! 💪

---

## 🎓 Remember

**What they care about**:
1. Can you think out loud?
2. Do you understand Spark internals (shuffles, joins, partitions)?
3. Can you handle curveballs (scaling, skew, architecture)?
4. Do you validate your work?
5. Can you explain trade-offs?

**What they DON'T care about**:
1. Perfect syntax
2. Memorizing every function
3. Never making mistakes
4. Fastest solution

**Your mantra**:
*"I am the architect. AI is my tool. I explain my reasoning. I validate my work. I scale with confidence."*

---

**Good luck! You've got this! 🚀**
