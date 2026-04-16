# Databricks Technical Concepts - Study Guide for Sr. Solutions Architect

## 🎯 Core Concepts You Must Know

---

## 1️⃣ Apache Spark Fundamentals

### Architecture Components

**Driver**:
- Runs the main() function
- Creates SparkContext
- Converts user code to tasks
- Schedules tasks on executors
- Maintains metadata (DAG, catalog)

**Executors**:
- Run on worker nodes
- Execute tasks assigned by driver
- Store data in memory or disk (RDD cache)
- Report status back to driver

**Cluster Manager**:
- Allocates resources (YARN, Kubernetes, Databricks)
- Manages executor lifecycle

### Execution Model

**Lazy Evaluation**:
- Transformations are lazy (build DAG)
- Actions trigger execution
- Allows for optimization before execution

**DAG (Directed Acyclic Graph)**:
- Logical plan of transformations
- Optimized by Catalyst Optimizer
- Converted to physical plan

**Jobs, Stages, Tasks**:
```
Action → Job
Job = Multiple Stages (separated by shuffles)
Stage = Multiple Tasks (one per partition)
Task = Unit of work on single partition
```

### Example Execution Flow
```python
# Lazy transformations - no execution yet
df = spark.read.parquet("data")
filtered = df.filter("age > 25")
grouped = filtered.groupBy("city").count()

# Action triggers execution
grouped.show()  # Now Spark executes the entire DAG
```

---

## 2️⃣ Transformations: Narrow vs Wide

### Narrow Transformations
**No shuffle required** - each input partition contributes to at most one output partition

Examples:
- `filter()`, `select()`, `withColumn()`
- `map()`, `flatMap()`
- `union()` (same partitioning)

```python
# Narrow - processes each partition independently
df.filter(col("amount") > 100)
df.withColumn("tax", col("amount") * 0.1)
```

**Performance**: Fast, can be pipelined

### Wide Transformations
**Shuffle required** - input partitions contribute to multiple output partitions

Examples:
- `groupBy()`, `agg()`
- `join()` (non-broadcast)
- `distinct()`, `orderBy()`
- `repartition()`

```python
# Wide - requires shuffle to co-locate data
df.groupBy("customer_id").sum("amount")
df.orderBy("timestamp")
df.join(other_df, "key")  # Sort-merge join
```

**Performance**: Expensive (disk I/O, network transfer, serialization)

---

## 3️⃣ Shuffles: The Performance Killer

### What is a Shuffle?
Redistributing data across partitions. Data from multiple input partitions must be moved across the network.

### Why Are Shuffles Expensive?
1. **Disk I/O**: Write intermediate data to disk
2. **Network I/O**: Transfer data between executors
3. **Serialization**: Serialize/deserialize data
4. **Sorting**: Often involves sorting operations

### When Do Shuffles Occur?
- `groupBy()`, `reduceByKey()`, `aggregateByKey()`
- `join()` (except broadcast join)
- `distinct()`, `intersection()`
- `repartition()`, `coalesce(numPartitions)` when reducing partitions
- `orderBy()`, `sortBy()`

### How to Minimize Shuffles?
```python
# ❌ BAD: Multiple shuffles
df.groupBy("a").count().groupBy("b").count()

# ✅ GOOD: Single shuffle
df.groupBy("a", "b").count()

# ❌ BAD: Shuffle on large table
large_df.join(small_df, "key")

# ✅ GOOD: Broadcast small table
large_df.join(broadcast(small_df), "key")

# ❌ BAD: Shuffle then filter
df.join(other, "key").filter("country = 'USA'")

# ✅ GOOD: Filter then shuffle
df.filter("country = 'USA'").join(other, "key")
```

---

## 4️⃣ Join Strategies

### 1. Broadcast Hash Join
**When**: One table is small (<10GB, configurable)
**How**: Small table sent to all executors
**Shuffle**: NO shuffle required
**Performance**: Fastest

```python
from pyspark.sql.functions import broadcast
large_df.join(broadcast(small_df), "key", "inner")
```

**Use Case**: Dimension table lookups

### 2. Sort-Merge Join
**When**: Both tables are large
**How**: Both tables sorted and partitioned by join key
**Shuffle**: YES - both tables shuffled
**Performance**: Slower but scalable

```python
# Spark auto-selects if no broadcast hint
large_df1.join(large_df2, "key", "inner")
```

**Use Case**: Large fact table joins

### 3. Shuffle Hash Join
**When**: One table is smaller (but not small enough to broadcast)
**How**: Hash smaller table, shuffle both
**Shuffle**: YES
**Performance**: Medium

**Use Case**: Rare - Spark usually prefers sort-merge

### 4. Cartesian Join
**When**: No join condition (cross join)
**How**: Every row from left with every row from right
**Shuffle**: YES
**Performance**: VERY SLOW (O(n*m))

```python
# Produces n * m rows
df1.crossJoin(df2)
```

**Use Case**: Rarely needed - usually indicates a problem

---

## 5️⃣ Partitioning Strategies

### What is a Partition?
- Chunk of data stored on a single executor
- Unit of parallelism (one task per partition)
- Optimal: 2-4 partitions per CPU core

### Types of Partitioning

**Hash Partitioning** (default):
```python
df.repartition(10, "customer_id")
# Data with same customer_id goes to same partition
```

**Range Partitioning**:
```python
df.repartitionByRange(10, "date")
# Partitions contain ranges of date values
```

**Coalesce** (reduce partitions without shuffle):
```python
df.coalesce(5)  # Combines partitions, no shuffle
# Use after filtering to reduce small partitions
```

### Partition Size Guidelines
- **Too small**: Overhead from task scheduling
- **Too large**: Memory pressure, stragglers
- **Ideal**: 100MB - 1GB per partition
- **Formula**: `partitions = data_size_GB / 0.5GB`

### Example
```python
# Check current partitions
df.rdd.getNumPartitions()

# Too many small partitions after filter
filtered = df.filter("amount > 1000")  # 99% filtered out
filtered.coalesce(5)  # Reduce to 5 partitions

# Prepare for join - partition by join key
df1.repartition(20, "customer_id").join(
    df2.repartition(20, "customer_id"), "customer_id"
)
# Now both tables have same partitioning scheme
```

---

## 6️⃣ Caching & Persistence

### When to Cache?
- DataFrame used multiple times
- Expensive computation (complex joins, aggregations)
- Iterative algorithms (ML training)

### When NOT to Cache?
- DataFrame used only once
- Large DataFrame that doesn't fit in memory
- Simple read operations

### Storage Levels

```python
from pyspark import StorageLevel

# Memory only (fastest, but may evict)
df.cache()  # Same as MEMORY_AND_DISK
df.persist(StorageLevel.MEMORY_ONLY)

# Memory and disk (spills to disk if needed)
df.persist(StorageLevel.MEMORY_AND_DISK)

# Disk only (for very large DataFrames)
df.persist(StorageLevel.DISK_ONLY)

# Serialized (saves memory, slower access)
df.persist(StorageLevel.MEMORY_ONLY_SER)
```

### Best Practices
```python
# ✅ GOOD: Cache before multiple actions
df.cache()
df.count()  # Triggers caching
df.show()   # Uses cached data
df.write.parquet("output")  # Uses cached data

# Unpersist when done
df.unpersist()

# ❌ BAD: Cache but don't reuse
df.cache()
df.count()
# Never used again - wasted memory
```

---

## 7️⃣ Data Skew Handling

### What is Data Skew?
Uneven data distribution across partitions. One partition has 10x, 100x, or more data than others.

### How to Detect?
```python
# Check partition sizes
df.rdd.mapPartitions(lambda it: [sum(1 for _ in it)]).collect()

# Use Spark UI - look for long-running tasks
```

### Symptoms
- One task takes much longer than others
- Executor OOM errors
- Most executors idle while one is working

### Solutions

**1. Salting** (for aggregations):
```python
# Add random salt to skewed key
df_salted = df.withColumn("salt", (rand() * 10).cast("int"))

# Aggregate with salt
partial = df_salted.groupBy("skewed_key", "salt").agg(sum("value"))

# Re-aggregate without salt
final = partial.groupBy("skewed_key").agg(sum("value"))
```

**2. Broadcast Join** (if skewed table is small):
```python
# Instead of regular join
large_skewed.join(broadcast(small_df), "key")
```

**3. Isolated Skew Keys**:
```python
# Separate hot keys and process differently
hot_keys = ["key1", "key2"]
hot_data = df.filter(col("key").isin(hot_keys))
normal_data = df.filter(~col("key").isin(hot_keys))

# Process separately with different strategies
```

**4. Increase Partitions**:
```python
# More partitions = smaller partition size
df.repartition(200)  # Increase from default
```

---

## 8️⃣ Delta Lake Essentials

### What is Delta Lake?
- ACID transactions on data lakes
- Built on Parquet format
- Transaction log for metadata
- Time travel and versioning

### Key Features

**1. ACID Transactions**:
```python
# Multiple writers can write concurrently
df.write.format("delta").mode("append").save("/path")
```

**2. Schema Enforcement**:
```python
# Rejects writes with incompatible schema
df.write.format("delta").mode("append").save("/path")
# Throws error if schema doesn't match
```

**3. Schema Evolution**:
```python
# Allow schema changes
df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save("/path")
```

**4. Time Travel**:
```python
# Read old version
df = spark.read.format("delta") \
    .option("versionAsOf", 5) \
    .load("/path")

# Read as of timestamp
df = spark.read.format("delta") \
    .option("timestampAsOf", "2025-01-01") \
    .load("/path")
```

**5. MERGE (Upsert)**:
```python
from delta.tables import DeltaTable

delta_table = DeltaTable.forPath(spark, "/path")

(delta_table.alias("target")
 .merge(new_df.alias("source"), "target.id = source.id")
 .whenMatchedUpdate(set={"value": "source.value"})
 .whenNotMatchedInsert(values={"id": "source.id", "value": "source.value"})
 .execute())
```

**6. OPTIMIZE & VACUUM**:
```python
# Compact small files
spark.sql("OPTIMIZE delta.`/path`")

# Z-order by column for better data skipping
spark.sql("OPTIMIZE delta.`/path` ZORDER BY (customer_id)")

# Remove old files (7 days retention)
spark.sql("VACUUM delta.`/path` RETAIN 168 HOURS")
```

---

## 9️⃣ Window Functions

### What are Window Functions?
Perform calculations across rows related to current row, without collapsing rows like `groupBy()`.

### Window Specification
```python
from pyspark.sql.window import Window
from pyspark.sql import functions as F

# Define window
window = Window.partitionBy("category").orderBy("date")
```

### Common Window Functions

**1. Ranking**:
```python
# ROW_NUMBER - unique sequential number
df.withColumn("row_num", F.row_number().over(window))

# RANK - same rank for ties, gaps
df.withColumn("rank", F.rank().over(window))

# DENSE_RANK - same rank for ties, no gaps
df.withColumn("dense_rank", F.dense_rank().over(window))

# NTILE - divide into N buckets
df.withColumn("quartile", F.ntile(4).over(window))
```

**2. Offset Functions**:
```python
# LAG - previous row value
df.withColumn("prev_value", F.lag("value", 1).over(window))

# LEAD - next row value
df.withColumn("next_value", F.lead("value", 1).over(window))

# FIRST - first value in partition
df.withColumn("first_value", F.first("value").over(window))

# LAST - last value in partition
df.withColumn("last_value", F.last("value").over(window))
```

**3. Aggregations**:
```python
# Running total
df.withColumn("running_total", F.sum("value").over(window))

# Moving average
window_3_rows = Window.partitionBy("category") \
    .orderBy("date") \
    .rowsBetween(-2, 0)  # Current + 2 previous rows

df.withColumn("ma_3", F.avg("value").over(window_3_rows))
```

### Frame Specifications

**Rows-based**:
```python
# 2 rows before to 1 row after
Window.rowsBetween(-2, 1)

# All rows before current
Window.rowsBetween(Window.unboundedPreceding, 0)
```

**Range-based** (value-based):
```python
# All rows with value within 7 days
Window.rangeBetween(-7 * 86400, 0)  # Seconds
```

---

## 🔟 Performance Tuning Checklist

### 1. **Data Skipping**
```python
# Partition by date for time-range queries
df.write.partitionBy("year", "month").parquet("/path")

# Query only reads relevant partitions
spark.read.parquet("/path").filter("year = 2025 AND month = 4")
```

### 2. **Predicate Pushdown**
```python
# Filter pushed to data source (reads less data)
spark.read.parquet("/path").filter("country = 'USA'")

# vs.
df = spark.read.parquet("/path")  # Reads all data
df.filter("country = 'USA'")      # Filters after read
```

### 3. **Column Pruning**
```python
# ✅ GOOD: Select only needed columns
df.select("id", "name", "amount").write.parquet("/output")

# ❌ BAD: Select all columns
df.write.parquet("/output")
```

### 4. **Broadcast Joins**
```python
# Auto-broadcast threshold (default 10MB)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 10 * 1024 * 1024)

# Manual broadcast
df1.join(broadcast(df2), "key")
```

### 5. **Partition Tuning**
```python
# Tune partition count
spark.conf.set("spark.sql.shuffle.partitions", 200)  # Default

# Adaptive Query Execution (auto-tuning)
spark.conf.set("spark.sql.adaptive.enabled", "true")
```

### 6. **File Format**
- **Delta**: ACID, time travel, MERGE
- **Parquet**: Columnar, compression, schema evolution
- **Avoid CSV**: No schema, no compression, slow

---

## 📊 Monitoring & Debugging

### Spark UI
- **Jobs**: See job execution
- **Stages**: Identify shuffle stages
- **Tasks**: Find stragglers (slow tasks)
- **Storage**: Check cached data
- **SQL**: View query plans

### Query Plans
```python
# Logical plan
df.explain(mode="simple")

# Physical plan
df.explain(mode="extended")

# Formatted (readable)
df.explain(mode="formatted")

# Cost-based
df.explain(mode="cost")
```

### Common Issues to Spot

**1. Excessive Shuffles**:
```
Exchange hashpartitioning  <-- Shuffle!
```

**2. Large Broadcasts**:
```
BroadcastExchange (size > 10GB)  <-- Problem!
```

**3. Cartesian Products**:
```
CartesianProduct  <-- Usually unintentional!
```

**4. Missing Predicate Pushdown**:
```
Filter after Scan  <-- Should push to scan!
```

---

## 🎯 Quick Decision Tree

**Choosing Join Strategy**:
```
Is one table < 10GB?
  Yes → Broadcast Join
  No → Is data pre-partitioned by join key?
    Yes → Sort-Merge Join (no repartition)
    No → Repartition both + Sort-Merge Join
```

**Choosing Partition Count**:
```
Data size in GB / 0.5 = Rough partition count
Ensure 2-4 partitions per CPU core
```

**Should I cache?**:
```
Used multiple times?
  Yes → Is it expensive to compute?
    Yes → Cache
    No → Maybe cache if data size is small
  No → Don't cache
```

**Handling Skew**:
```
Detect skew (partition size variance > 10x)
  → Aggregation? Use salting
  → Join? Try broadcast if possible
  → Otherwise: Isolate hot keys or increase partitions
```

---

## 📚 Must-Know SQL Functions

```python
# String functions
F.concat("first_name", F.lit(" "), "last_name")
F.regexp_replace("email", "@.*", "")
F.substring("phone", 1, 3)
F.lower("name")

# Date functions
F.current_date()
F.date_add("date", 7)
F.datediff("end_date", "start_date")
F.date_format("timestamp", "yyyy-MM-dd")
F.year("date"), F.month("date"), F.dayofmonth("date")

# Null handling
F.coalesce("col1", "col2", F.lit(0))  # First non-null
F.isNull("col"), F.isNotNull("col")
df.fillna({"col": 0})

# Conditional
F.when(condition, value).otherwise(default)
F.expr("CASE WHEN x > 10 THEN 'high' ELSE 'low' END")

# Aggregations
F.sum("amount"), F.avg("amount"), F.count("*")
F.min("date"), F.max("date")
F.stddev("value"), F.variance("value")
F.approx_count_distinct("user_id")  # Faster than exact

# Array/Map functions
F.array("col1", "col2")
F.explode("array_col")  # One row per array element
F.array_contains("array_col", "value")
F.size("array_col")
```

---

## 🚀 Production Best Practices

1. **Idempotency**: Use Delta MERGE, not append
2. **Partitioning**: Partition by query-filter columns (date, region)
3. **Schema**: Enforce schema, version changes
4. **Monitoring**: Log row counts, execution time, data quality metrics
5. **Error Handling**: Quarantine bad records, don't fail pipeline
6. **Testing**: Validate on sample data before full run
7. **Documentation**: Comment complex logic, maintain lineage

---

## 🎓 Study Plan

### Day 1-2: Fundamentals
- Spark architecture (driver, executors, DAG)
- Narrow vs wide transformations
- Shuffle mechanics

### Day 3-4: Joins & Partitioning
- Join strategies (broadcast, sort-merge)
- Partitioning best practices
- Skew handling

### Day 5-6: Delta & Windows
- Delta Lake features (ACID, time travel, MERGE)
- Window functions (ranking, lag/lead, moving averages)

### Day 7: Performance & Practice
- Query plan reading
- Optimization techniques
- Mock scenarios

---

**Master these concepts and you'll be able to think out loud confidently! 🚀**
