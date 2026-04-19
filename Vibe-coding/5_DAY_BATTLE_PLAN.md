# 5-Day Battle Plan: Databricks Vibe Coding Interview
**Interview Date: April 24th | Today: April 19th**

---

## 🎯 Reality Check: What This Interview ACTUALLY Tests

Based on real candidate feedback:
- **70% Spark Internals**: Shuffles, query plans, optimization, data skew
- **20% Structured Problem-Solving**: Spec creation, step-by-step execution, explaining decisions
- **10% Synthetic Data**: Just the vehicle for testing Spark knowledge

**Critical Insight**: You'll get **curveball scenarios** after the initial task:
- "Scale this from 10k to 100M records" → test optimization skills
- "Here's data skew" → test broadcast/salting/sort-merge knowledge
- "Extend this architecture" → test facts/dims design patterns

---

## 📅 Day-by-Day Breakdown (April 19-23)

### **DAY 1 (TODAY - April 19): Spark Internals Deep Dive**
**Goal**: Master the concepts they'll ask about when they throw curveballs

#### Morning (2-3 hours): Shuffles & Query Plans
- [ ] **Read**: `Databricks_Technical_Concepts.md` sections 2-3 (Transformations, Shuffles)
- [ ] **Hands-on Practice**:
  ```python
  # In Databricks, run these and EXPLAIN the query plans

  # 1. Identify shuffles
  df = spark.range(10000000).withColumn("key", (rand() * 1000).cast("int"))
  df.groupBy("key").count().explain("formatted")  # Spot the Exchange

  # 2. Before/After broadcast
  large = spark.range(10000000).withColumn("cat", (rand() * 10).cast("int"))
  small = spark.range(10).withColumnRenamed("id", "cat")

  # Without broadcast
  large.join(small, "cat").explain("formatted")

  # With broadcast
  from pyspark.sql.functions import broadcast
  large.join(broadcast(small), "cat").explain("formatted")
  ```

- [ ] **Memorize**: When shuffles happen (groupBy, join, distinct, orderBy, repartition)
- [ ] **Practice explaining**: "This triggers a shuffle because we need to co-locate all records with the same key"

#### Afternoon (2-3 hours): Data Skew Scenarios
- [ ] **Read**: `Databricks_Technical_Concepts.md` section 7 (Data Skew Handling)
- [ ] **Hands-on Practice**:
  ```python
  # Generate skewed data
  from pyspark.sql.functions import when, rand, col

  skewed = spark.range(1000000).withColumn(
      "key",
      when(rand() < 0.8, lit("hot_key"))  # 80% in one key
      .otherwise((rand() * 100).cast("int").cast("string"))
  )

  # BAD: Regular groupBy
  skewed.groupBy("key").count().explain("formatted")

  # GOOD: Salting
  salted = skewed.withColumn("salt", (rand() * 10).cast("int"))
  partial = salted.groupBy("key", "salt").count()
  final = partial.groupBy("key").sum("count")
  final.explain("formatted")
  ```

- [ ] **Drill**: Explain salting in 30 seconds or less
- [ ] **Drill**: When to use broadcast vs salting vs isolate hot keys

#### Evening (1 hour): UI & Environment Setup
- [ ] **Create Databricks Free Edition account** (if not done)
- [ ] **Practice workflow**:
  - Start cluster (note: takes 2-3 mins)
  - Create catalog/schema: `CREATE CATALOG interview_prep; USE CATALOG interview_prep;`
  - Create notebook
  - Install packages: `%pip install dbldatagen faker`
  - Test Databricks Assistant
- [ ] **Screen sharing test**: Share your screen and narrate while typing

---

### **DAY 2 (April 20): Scaling & Optimization Scenarios**
**Goal**: Handle the "scale from 10k to 100M" curveball

#### Morning (2-3 hours): Performance Optimization Drills
- [ ] **Scenario**: You built a query on 10k rows. Now scale to 100M.
  ```python
  # Small dataset (works fine)
  small_df = spark.range(10000).withColumn("category", (rand() * 10).cast("int"))
  result = small_df.groupBy("category").agg(
      avg("id"), count("*")
  ).orderBy("category")

  # Now scale it
  large_df = spark.range(100000000).withColumn("category", (rand() * 10).cast("int"))

  # BEFORE optimization
  result = large_df.groupBy("category").agg(
      avg("id"), count("*")
  ).orderBy("category")
  result.explain("formatted")  # Analyze the plan

  # AFTER optimization
  # 1. Check partition count
  print(f"Partitions: {large_df.rdd.getNumPartitions()}")

  # 2. Tune shuffle partitions
  spark.conf.set("spark.sql.shuffle.partitions", "200")

  # 3. Cache if reused
  large_df.cache().count()

  # 4. Re-run and compare
  result = large_df.groupBy("category").agg(
      avg("id"), count("*")
  ).orderBy("category")
  ```

- [ ] **Practice explaining**:
  - "The default 200 shuffle partitions is too many/few for this data size"
  - "I'm caching because this DataFrame is used multiple times"
  - "This groupBy requires a shuffle to co-locate data by key"

#### Afternoon (2-3 hours): Join Strategy Optimization
- [ ] **Drill**: Broadcast Hash Join vs Sort-Merge Join
  ```python
  # Scenario: Join a large fact table with dimension tables
  facts = spark.range(100000000).withColumn("prod_id", (rand() * 100).cast("int"))
  dim_small = spark.range(100).withColumnRenamed("id", "prod_id")
  dim_large = spark.range(10000000).withColumnRenamed("id", "cust_id")

  # GOOD: Broadcast small dim
  result1 = facts.join(broadcast(dim_small), "prod_id")
  result1.explain("formatted")  # Look for BroadcastHashJoin

  # GOOD: Pre-partition for large join
  facts_part = facts.repartition(200, "cust_id")
  dim_part = dim_large.repartition(200, "cust_id")
  result2 = facts_part.join(dim_part, "cust_id")
  result2.explain("formatted")  # Look for SortMergeJoin without Exchange
  ```

#### Evening (1 hour): Partitioning Best Practices
- [ ] **Read**: `Databricks_Technical_Concepts.md` section 5 (Partitioning)
- [ ] **Memorize**:
  - Ideal partition size: 100MB - 1GB
  - Formula: `partitions = data_size_GB / 0.5`
  - `repartition()` = full shuffle
  - `coalesce()` = reduce partitions without shuffle

---

### **DAY 3 (April 21): Synthetic Data + Structured Workflow**
**Goal**: Master the initial task execution with perfect structure

#### Morning (2 hours): Structured Prompt Engineering
- [ ] **Practice the workflow from real interview feedback**:

**Step 1: Clarify Requirements (5 mins)**
```
Template Questions:
1. "What industry are we modeling?" [e-commerce, healthcare, fintech]
2. "What's the data volume for each dataset?" [10k, 100k, 1M?]
3. "What's the grain?" [transaction-level, customer-level, daily aggregates?]
4. "What metrics are we calculating?" [revenue, retention, conversion?]
5. "Output format?" [Delta table, visualization, both?]
```

**Step 2: Create Structured Spec (5 mins)**
```
Use ChatGPT to create a spec like this:

"I need to generate synthetic e-commerce data for a Databricks demo. Here's the spec:

DATASET 1: Customers
- Volume: 10,000 records
- Grain: One row per customer
- Columns: customer_id (PK), name, email, signup_date, country
- Distribution: 40% USA, 20% UK, 15% Canada, 15% Germany, 10% France

DATASET 2: Transactions
- Volume: 100,000 records
- Grain: One row per transaction
- Columns: transaction_id (PK), customer_id (FK), product_id, amount, date
- Distribution: amount follows log-normal (mean=100, stddev=50)
- Relationships: customer_id references Customers.customer_id

METRICS TO CALCULATE:
1. Customer Lifetime Value (CLV) = sum(amount) per customer
2. Average Order Value (AOV) = avg(amount) per customer
3. Top 10% customers by revenue

OUTPUT: Delta table with customer_id, CLV, AOV, revenue_rank
"

Then use this spec with Databricks Assistant step-by-step.
```

#### Afternoon (3 hours): End-to-End Practice Run
- [ ] **Pick a scenario from `Databricks_Mock_Scenarios.md`** (e.g., Scenario 1)
- [ ] **Time yourself: 60 minutes total**
- [ ] **Follow the structure**:
  - 5 mins: Clarify + create spec
  - 10 mins: Generate datasets
  - 5 mins: Validate data (schema, counts, distributions)
  - 25 mins: Join + calculate metrics
  - 10 mins: Write to Delta + create simple viz
  - 5 mins: Explain what you built

- [ ] **Think out loud the entire time** (record yourself!)
- [ ] **Practice explaining**:
  - "I'm using log-normal distribution because..."
  - "This join will use broadcast because the dimension table is small..."
  - "I'm validating referential integrity before proceeding..."

#### Evening (1 hour): Review Recording
- [ ] Watch your practice run
- [ ] Note silent periods (red flag!)
- [ ] Count how many times you explained trade-offs
- [ ] Check: Did you validate intermediate results?

---

### **DAY 4 (April 22): Curveball Scenarios Drills**
**Goal**: Prepare for the extensions they'll throw at you

#### Morning (2 hours): "Scale This" Curveball
- [ ] **Practice scenario**:
  ```python
  # You just built this with 10k customers, 100k transactions
  clv = transactions.groupBy("customer_id").agg(
      sum("amount").alias("total_revenue")
  ).join(customers, "customer_id")

  # CURVEBALL: "What if we have 100M transactions instead?"

  # YOUR RESPONSE (think out loud):
  # "With 100M transactions, I need to consider:
  # 1. Partition count - default 200 may be too low
  # 2. Broadcast join still works for customers (10k << 10GB)
  # 3. The groupBy will trigger a shuffle - unavoidable
  # 4. I'd check partition sizes after groupBy
  # 5. Consider caching if we reuse the result
  # 6. For incremental processing, I'd use Delta MERGE instead of full refresh"

  # DEMONSTRATE:
  spark.conf.set("spark.sql.shuffle.partitions", "400")  # Increase

  large_txn = spark.range(100000000).withColumn(
      "customer_id", (rand() * 10000).cast("int")
  ).withColumn("amount", rand() * 1000)

  clv_large = large_txn.groupBy("customer_id").agg(
      sum("amount").alias("total_revenue")
  ).join(broadcast(customers), "customer_id")

  clv_large.explain("formatted")  # Walk through the plan
  ```

#### Afternoon (2 hours): "Handle This Skew" Curveball
- [ ] **Practice scenario**:
  ```python
  # CURVEBALL: "I'm introducing data skew - 80% of transactions
  #             are from the top 5 customers. How would you handle this?"

  # Generate skewed data
  skewed_txn = spark.range(100000).withColumn(
      "customer_id",
      when(rand() < 0.8, (rand() * 5).cast("int"))  # Hot keys
      .otherwise((rand() * 10000).cast("int"))
  ).withColumn("amount", rand() * 1000)

  # YOUR RESPONSE:
  # "I'd use salting to distribute the hot keys across multiple partitions.
  #  This adds a random salt to the skewed key, performs partial aggregations,
  #  then re-aggregates. Let me demonstrate..."

  # 1. Add salt
  salted = skewed_txn.withColumn("salt", (rand() * 10).cast("int"))

  # 2. Partial aggregation with salt
  partial = salted.groupBy("customer_id", "salt").agg(
      sum("amount").alias("partial_sum"),
      count("*").alias("partial_count")
  )

  # 3. Final aggregation
  final = partial.groupBy("customer_id").agg(
      sum("partial_sum").alias("total_revenue"),
      sum("partial_count").alias("transaction_count")
  )

  final.explain("formatted")  # Show improved parallelism
  ```

#### Evening (2 hours): "Extend the Architecture" Curveball
- [ ] **Practice scenario**:
  ```python
  # CURVEBALL: "Design this as a fact/dimension model that can
  #             accommodate new datasets in the future"

  # YOUR RESPONSE:
  # "I'd implement a medallion architecture with star schema:
  # Bronze (raw) → Silver (cleaned) → Gold (aggregated facts + dims)"

  # Demonstrate:

  # BRONZE: Raw ingestion
  bronze_txn.write.format("delta").mode("append").saveAsTable("bronze.transactions")

  # SILVER: Cleaned data with facts/dims separation
  # Fact table: Transactions (deduped, validated)
  fact_transactions = bronze_txn.dropDuplicates(["transaction_id"]) \
      .filter(col("amount") > 0) \
      .select("transaction_id", "customer_id", "product_id", "amount", "date")

  fact_transactions.write.format("delta") \
      .mode("overwrite") \
      .partitionBy("date") \
      .saveAsTable("silver.fact_transactions")

  # Dimension table: Customers (SCD Type 2 for history)
  dim_customers.write.format("delta") \
      .mode("overwrite") \
      .saveAsTable("silver.dim_customers")

  # GOLD: Aggregated metrics
  gold_clv = fact_transactions.join(
      dim_customers, "customer_id"
  ).groupBy("customer_id", "country").agg(
      sum("amount").alias("clv")
  )

  gold_clv.write.format("delta") \
      .mode("overwrite") \
      .saveAsTable("gold.customer_metrics")

  # EXPLAIN:
  # "This design allows us to:
  # 1. Add new fact tables (orders, returns) without changing existing ones
  # 2. Add new dimensions (products, stores) via star schema joins
  # 3. Maintain history with SCD Type 2
  # 4. Query optimized gold layer for dashboards"
  ```

---

### **DAY 5 (April 23): Mock Interview & Final Review**
**Goal**: Full simulation under time pressure

#### Morning (3 hours): Full Mock Interview
- [ ] **Set timer: 60 minutes**
- [ ] **Pick a NEW scenario** (one you haven't practiced)
- [ ] **Record yourself** (video + screen)
- [ ] **Simulate curveballs**:
  - After initial task: "Scale this to 500M records"
  - "I'm seeing slow performance on the join - optimize it"
  - "Add a streaming ingestion component for real-time updates"

**Mock Interview Structure**:
```
0-5 min:   Clarify requirements, create spec
5-15 min:  Generate synthetic data, validate
15-30 min: Join + calculate metrics
30-35 min: Write to Delta, simple viz
35-45 min: CURVEBALL 1 - Scaling
45-55 min: CURVEBALL 2 - Optimization/Architecture
55-60 min: Explain end-to-end solution
```

#### Afternoon (2 hours): Review & Gap Analysis
- [ ] Watch your mock interview recording
- [ ] **Checklist**:
  - [ ] Did I think out loud continuously?
  - [ ] Did I explain why, not just what?
  - [ ] Did I validate intermediate results?
  - [ ] Did I use `.explain()` to show query plans?
  - [ ] Did I handle curveballs confidently?
  - [ ] Did I structure my approach before coding?

- [ ] **Fix gaps**: If you struggled with any concept, re-read that section

#### Evening (1-2 hours): Cheat Sheet Creation
- [ ] **Create a one-page reference** (you can't use during interview, but helps memorization):

```markdown
# Quick Reference

## Shuffles trigger on:
- groupBy, join (non-broadcast), distinct, orderBy, repartition

## Join strategies:
- Small (<10GB) → Broadcast: `broadcast(df)`
- Large → Sort-Merge: pre-partition on join key
- Skew → Broadcast if possible, else salting

## Skew handling:
1. Broadcast (if small enough)
2. Salting (add random salt, partial agg, re-agg)
3. Isolate hot keys (process separately)

## Optimization checklist:
- [ ] Predicate pushdown (filter early)
- [ ] Column pruning (select only needed)
- [ ] Broadcast small tables
- [ ] Partition by query-filter columns
- [ ] Cache if reused multiple times
- [ ] Check partition count: data_GB / 0.5

## Common functions:
- `F.broadcast()`, `F.rand()`, `F.when()`, `F.coalesce()`
- `Window.partitionBy().orderBy()`, `F.lag()`, `F.ntile()`
- `DeltaTable.forPath().merge()`

## Think-out-loud phrases:
- "This triggers a shuffle because..."
- "I'm using broadcast here since the table is small..."
- "Let me validate this with .explain()..."
- "For 100M rows, I'd adjust partitions to..."
```

---

## 🎯 Interview Day Strategy (April 24)

### Pre-Interview (30 mins before)
- [ ] Start Databricks cluster (takes 2-3 mins)
- [ ] Create workspace: `CREATE CATALOG vibe_interview; USE CATALOG vibe_interview;`
- [ ] Install packages: `%pip install dbldatagen faker`
- [ ] Test Databricks Assistant with simple query
- [ ] Have documentation tabs ready (PySpark functions, Delta Lake)
- [ ] Close all other apps, notifications off

### During Interview - Opening (First 5 mins)
1. **Listen carefully** to the scenario
2. **Ask clarifying questions**:
   - "What industry are we modeling?"
   - "What's the expected data volume for each dataset?"
   - "What metrics are we calculating?"
   - "What's the output format?"
3. **Restate the problem**: "So we're building a pipeline that..."
4. **Outline your approach**: "Here's how I'll tackle this: Step 1..., Step 2..."

### During Interview - Execution (35-40 mins)
**CRITICAL**: Think out loud continuously
- "I'm using log-normal distribution because real-world spending..."
- "This join will broadcast the small table to avoid shuffle..."
- "Let me validate the data before proceeding..."
- "I'll use `.explain()` to check the query plan..."

**When using AI assistants**:
- "Let me draft a prompt for Databricks Assistant..."
- Read generated code out loud
- "I notice it's using X, but Y would be better because..."

**When errors occur**:
- "I'm seeing a [error type]. Let me check..."
- Read error message out loud
- "This is likely because... let me fix it..."

### During Interview - Curveballs (15-20 mins)
**Expected curveballs**:
1. "Scale this from 10k to 100M records"
   - Response: "I'd adjust shuffle partitions, ensure broadcast joins for small dims, check partition sizes..."

2. "Handle data skew on customer_id"
   - Response: "I'd use salting - add random salt, partial aggregate, then final aggregate..."

3. "Design this as extensible architecture"
   - Response: "I'd use medallion architecture with fact/dim tables..."

**For ANY curveball**:
1. Pause, think (15 seconds is OK!)
2. "Here's how I'd approach this..."
3. Explain before coding
4. Code while narrating

### Interview - Closing (Last 5 mins)
- Summarize what you built
- Explain end-to-end data flow
- Mention scalability considerations
- Ask if they want to see anything else

---

## 🚨 Red Flags to Avoid

❌ **Silent coding** for more than 30 seconds
✅ Narrate continuously

❌ **Blindly trusting AI output**
✅ "Let me review this... I notice X, I'd change it because..."

❌ **Not validating intermediate results**
✅ `df.show()`, `df.count()`, `df.printSchema()` frequently

❌ **Ignoring errors** or saying "weird, let me try something else"
✅ "This error says X, which means Y, so I'll fix it by Z"

❌ **Overcomplicating** the initial solution
✅ "The simplest approach is... if we needed to scale, then..."

---

## 📚 Must-Review Sections Before Interview

### Critical Reading (1-2 hours night before):
1. `Databricks_Technical_Concepts.md`:
   - Section 3: Shuffles
   - Section 4: Join Strategies
   - Section 5: Partitioning
   - Section 7: Data Skew
   - Section 10: Quick Decision Trees

2. `Databricks_Vibe_Interview_Prep_Guide.md`:
   - Phase 2: Data Generation
   - Phase 3: Building Solution
   - Communication Templates

---

## 🎓 Key Phrases to Memorize

**When explaining shuffles**:
"This groupBy triggers a shuffle because we need to co-locate all records with the same key across partitions"

**When using broadcast**:
"I'm using a broadcast join here because the dimension table is small - less than 10GB - so we can send it to all executors to avoid a shuffle"

**When handling skew**:
"I'll use salting: add a random salt to the skewed key, perform partial aggregations with the salt, then re-aggregate without the salt to get the final result"

**When scaling**:
"To scale from 10k to 100M records, I'd: 1) Increase shuffle partitions, 2) Ensure broadcast joins for small tables, 3) Check partition sizes are 100MB-1GB, 4) Consider caching if reused, 5) Use Delta MERGE for incremental processing"

**When showing query plan**:
"Let me check the query plan with `.explain()`... I see an Exchange here, which indicates a shuffle. This is expected for the groupBy operation"

---

## ✅ Final Checklist (Night Before)

- [ ] Databricks cluster starts successfully
- [ ] Can create catalog/schema
- [ ] Can install packages (`dbldatagen`, `faker`)
- [ ] Databricks Assistant works
- [ ] Screen sharing tested
- [ ] Know how to use `.explain("formatted")`
- [ ] Can generate simple synthetic data from memory
- [ ] Can explain a shuffle in 30 seconds
- [ ] Can explain salting in 30 seconds
- [ ] Can explain broadcast join in 30 seconds
- [ ] Reviewed common PySpark functions
- [ ] Practiced thinking out loud (recorded yourself)
- [ ] Good night's sleep planned (7-8 hours!)

---

## 🎯 Success Criteria

You'll know you're ready when:
1. You can explain **why** a shuffle happens, not just that it happens
2. You can **read a query plan** and identify optimization opportunities
3. You can **handle data skew** with salting (explain + code in 2 mins)
4. You can **scale a solution** from 10k to 100M records (explain what changes)
5. You can **think out loud** naturally without awkward silences
6. You can **structure your approach** before coding (spec-driven)

---

## 💪 You've Got This!

**Remember**:
- They want to see how you **think**, not perfect code
- **Explaining > Speed** - slow and narrated beats fast and silent
- **AI is your assistant**, you're the architect
- **Errors are normal** - your response to them matters
- **Ask questions** - it's collaborative, not adversarial

**Your mantra for April 24th**:
*"I am the architect. AI is my tool. I explain my reasoning. I validate my work. I scale with confidence."*

Good luck! 🚀
