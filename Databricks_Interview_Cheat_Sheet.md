# Databricks Vibe Interview - Quick Reference Cheat Sheet

## 🎯 Remember: Think Out Loud at ALL Times!

---

## 📝 Opening Template (First 5 mins)

**Ask Clarifying Questions**:
- "What's the business objective we're solving for?"
- "What's the expected data volume? Thousands, millions, billions?"
- "Are there specific performance or latency requirements?"
- "What's the expected output format?"

**Restate the Problem**:
- "So we're building [X] that does [Y] to produce [Z], correct?"

---

## 💻 Quick Syntax Reference

### Data Generation (dbldatagen)
```python
import dbldatagen as dg
from pyspark.sql import functions as F

spec = (dg.DataGenerator(spark, rows=10000, partitions=4)
    .withColumn("id", "int", minValue=1, uniqueValues=10000)
    .withColumn("name", "string", template=r"\w \w")
    .withColumn("amount", "float", minValue=0, maxValue=1000,
                distribution="log-normal")
    .withColumn("category", "string",
                values=["A", "B", "C"], weights=[50, 30, 20])
    .withColumn("date", "date", begin="2024-01-01", end="2025-12-31"))

df = spec.build()
```

### Common Transformations
```python
# Filter & select
df.filter(F.col("amount") > 100).select("id", "name")

# Aggregation
df.groupBy("category").agg(
    F.sum("amount").alias("total"),
    F.avg("amount").alias("average"),
    F.count("*").alias("count")
)

# Window functions
from pyspark.sql.window import Window
w = Window.partitionBy("category").orderBy(F.desc("amount"))
df.withColumn("rank", F.rank().over(w))

# Joins
df1.join(F.broadcast(df2), "key", "inner")  # Broadcast small table
```

### Data Quality
```python
# Check for nulls
df.filter(F.col("column").isNull()).count()

# Remove duplicates
df.dropDuplicates(["key_column"])

# Handle nulls
df.fillna({"column": 0})
df.na.drop(subset=["critical_column"])
```

### Delta Operations
```python
# Write
df.write.format("delta").mode("overwrite").saveAsTable("table_name")

# MERGE (upsert)
from delta.tables import DeltaTable
delta_table = DeltaTable.forName(spark, "table_name")
(delta_table.alias("target")
 .merge(new_df.alias("source"), "target.id = source.id")
 .whenMatchedUpdateAll()
 .whenNotMatchedInsertAll()
 .execute())
```

---

## 🗣️ Think-Out-Loud Phrases

### When Generating Data
✅ "I'm using a log-normal distribution because real-world [X] follows that pattern"
✅ "Adding 5% null values to simulate data quality issues"
✅ "Using unique values to ensure no duplicate IDs"

### When Transforming
✅ "This filter is a narrow transformation—no shuffle required"
✅ "This groupBy will trigger a shuffle to co-locate records with the same key"
✅ "Using a broadcast join because this table is small (<10GB)"

### When Optimizing
✅ "I'll cache this DataFrame since we're using it multiple times"
✅ "Let me check the query plan with .explain() to see if there are redundant stages"
✅ "Filtering early to take advantage of predicate pushdown"

### When Debugging
✅ "Getting an error—let me read it carefully... [read error aloud]"
✅ "Let me check the schema... ah, column name mismatch"
✅ "This is taking longer than expected—let me add a .explain() to investigate"

### When Using AI
✅ "Let me use AI to scaffold this code... [review output] I notice it's using collect(), which could cause OOM—let me refactor"
✅ "The AI suggested X, but Y would be more efficient because [reason]"

---

## 🚨 Red Flags to Avoid

❌ **Silent coding** for >30 seconds → Always narrate!
❌ **Using .collect()** on large DataFrames → OOM risk!
❌ **Ignoring performance** → Mention shuffles, partitioning
❌ **Trusting AI blindly** → Always review and audit
❌ **Getting stuck >2 mins on syntax** → Ask for help or use "bail out"

---

## ✅ Validation Checklist (After Each Step)

```python
# Always validate your work!
df.printSchema()           # Check data types
df.show(5, truncate=False) # Visual inspection
df.count()                 # Row count sanity check
df.describe().show()       # Statistics (min, max, mean, stddev)

# Check for data quality
df.filter(F.col("col").isNull()).count()  # Null count
df.select("key").distinct().count()       # Uniqueness
```

---

## 📊 Performance Optimization Quick Wins

1. **Broadcast small tables** (<10GB)
   ```python
   large_df.join(F.broadcast(small_df), "key")
   ```

2. **Cache reused DataFrames**
   ```python
   df.cache()
   df.count()  # Trigger caching
   ```

3. **Partition appropriately**
   ```python
   df.repartition(20)  # Increase parallelism
   df.coalesce(5)      # Reduce files (no shuffle)
   ```

4. **Filter early** (predicate pushdown)
   ```python
   df.filter(...).select(...)  # Filter before select
   ```

5. **Use appropriate file formats**
   - Delta: ACID, time travel, updates
   - Parquet: Columnar, good compression
   - Avoid CSV for large data

---

## 🎓 Distributed Computing Talking Points

**Narrow Transformations** (no shuffle):
- `select`, `filter`, `withColumn`, `map`

**Wide Transformations** (shuffle required):
- `groupBy`, `join` (non-broadcast), `orderBy`, `distinct`

**When explaining scalability**:
- "For 10K rows, this works fine. At 100M rows, I'd partition by [date/key]"
- "This shuffle is necessary for the aggregation, but we could reduce it by pre-aggregating"
- "If the dimension table grows beyond 10GB, we'd switch from broadcast to sort-merge join"

---

## 🔧 Common Debugging Commands

```python
# Check execution plan
df.explain(mode="formatted")

# View physical plan stages
df.explain(mode="extended")

# Sample data
df.sample(0.1).show()  # 10% sample

# Check partitioning
df.rdd.getNumPartitions()

# Force computation (to see if it works)
df.count()
```

---

## 💬 Customer Translation Examples

**Technical**: "We're using a window function with lag to calculate period-over-period changes"
**Customer**: "This code compares each month's sales to the previous month to identify trends"

**Technical**: "Broadcasting the small dimension table to avoid a shuffle"
**Customer**: "By sending the small lookup table to all workers, we avoid expensive data movement"

**Technical**: "Implementing a medallion architecture: bronze → silver → gold"
**Customer**: "We have three layers: raw data, cleaned data, and business-ready aggregates"

---

## 🎯 Success Criteria Reminder

| What They Test | How to Show It |
|---------------|---------------|
| **Computational Thinking** | Break problem into steps, explain flow |
| **Code Stewardship** | Review AI output, identify issues |
| **Resilience** | Debug methodically, ask for help when stuck |
| **Distributed Reasoning** | Explain shuffles, partitioning, scalability |

---

## ⏰ Time Management (60 mins total)

- **Discovery** (5-10 min): Clarify, restate, ask questions
- **Data Gen** (10-15 min): Generate realistic data, validate
- **Solution** (25-35 min): Build, transform, think out loud
- **Validation** (10-15 min): Test, explain, discuss scalability

---

## 🆘 If You Get Stuck

1. **Read error message aloud** and reason through it
2. **Check documentation** (it's open book!)
3. **Ask for "bail out"** if stuck >2 mins on syntax
4. **Explain what you're trying** - interviewer may guide you

---

## 🎤 Opening Line (Use This!)

"Let me make sure I understand the requirements. We need to [restate problem]. Before I start, a few quick questions: [ask 2-3 clarifying questions]. Great! Here's my approach: [outline 3-5 steps]. I'll think out loud as I work through this."

---

## 🎬 Closing Line (Use This!)

"Let me validate the output... [run checks]. This solution works for our dataset. To discuss scalability: if we had 100x more data, I'd consider [partitioning strategy, optimization]. The code is now production-ready with [mention: Delta format, data quality checks, idempotency, etc.]. Happy to walk through any part in more detail!"

---

**Good luck! You've got this. Remember: THINK OUT LOUD! 🚀**
