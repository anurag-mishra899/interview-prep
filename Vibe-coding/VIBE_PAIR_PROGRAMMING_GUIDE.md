# Vibe Coding Interview: Pair Programming Companion Guide

## The "Vibe" Philosophy - What This Interview Really Is

**This is NOT**:
- ❌ A traditional whiteboard coding test
- ❌ A "gotcha" quiz on syntax or memorization
- ❌ A race to write perfect code quickly
- ❌ An adversarial interrogation

**This IS**:
- ✅ A **collaborative pair programming session** with your future peers
- ✅ A simulation of **real customer engagement work**
- ✅ An **open-book test** with access to all tools (docs, AI, Stack Overflow)
- ✅ A chance to demonstrate **how you think and communicate**
- ✅ A conversation about **trade-offs, architecture, and problem-solving**

---

## 🎯 The Three Core Signals They're Evaluating

### 1. **Computational Thinking** (How You Break Down Problems)
**What they want to see**:
- Can you decompose a messy, ambiguous problem into logical steps?
- Do you think in terms of data transformations and flows?
- Can you reason about how code executes in a distributed environment?

**How to demonstrate**:
```
Good: "I'll break this into 4 steps: First, ingest raw data to Bronze.
       Second, validate and cleanse in Silver. Third, aggregate metrics
       in Gold. Finally, serve via APIs."

Bad: "I'll just start coding and see what happens."
```

---

### 2. **Code Stewardship** (You're the AI Pilot, Not Passenger)
**What they want to see**:
- Can you **audit** AI-generated code for correctness?
- Do you understand what the code does **under the hood**?
- Can you identify inefficiencies, anti-patterns, or hallucinations?
- Can you explain the code to a customer or stakeholder?

**How to demonstrate**:
```
Good: "Let me review this AI-generated code... I see it's using collect()
       which would pull all data to the driver. That's a problem for
       100M records. I'll refactor to use distributed operations instead."

Bad: *Copies AI code blindly without reading it*
```

---

### 3. **Resilience** (How You Navigate Obstacles)
**What they want to see**:
- How do you handle bugs, errors, or blockers?
- Do you stay calm and methodical, or panic?
- Can you ask for help appropriately (use "Bail Out")?
- Do you learn from mistakes and adapt?

**How to demonstrate**:
```
Good: "I'm getting an AnalysisException. Let me read the error...
       It says 'column not found'. Looking at the schema... ah, I see
       the issue. The column is 'customer_id' not 'customerId'.
       Let me fix that."

Bad: "This is weird, I don't know why it's not working."
     *Tries random things without reading the error*
```

---

## 🗣️ The Art of Thinking Out Loud

### Why This Is The MOST Important Skill

**Your interviewer cannot read your mind.** Silent coding looks like:
- You're stuck and don't know what to do
- You're copying code you don't understand
- You're not confident in your approach

**Continuous narration shows**:
- Your problem-solving process
- Your understanding of distributed systems
- Your ability to communicate with customers/stakeholders
- Your confidence and expertise

---

### The Narration Framework: DEWA

Use this structure to think out loud naturally:

#### **D - Describe** what you're about to do
```
"I'm going to generate synthetic customer data with 100K records.
 I'll use dbldatagen because it's optimized for Spark and can handle
 large-scale generation efficiently."
```

#### **E - Explain** why you're doing it this way
```
"I'm choosing log-normal distribution for transaction amounts because
 real-world spending follows that pattern - most transactions are small,
 with a long tail of high-value purchases."
```

#### **W - Walk through** your code as you write/review it
```
"This join will be a broadcast join because the customer table is small -
 only 10K rows, well under the 10GB threshold. This avoids a shuffle."
```

#### **A - Assess** what you just did
```
"Let me validate this... running df.count() shows 100K records as expected.
 The schema looks correct. Let me check the distribution with describe()..."
```

---

### Example Narration Scripts

#### **Scenario 1: Generating Data**

**❌ Silent Approach** (Bad):
```
*Types code silently for 2 minutes*
*Runs cell*
"Okay, done."
```

**✅ Narrated Approach** (Good):
```
"Let me start by generating customer data. I'll use dbldatagen for this.
 [Types import]

 I need three main attributes: customer_id, name, and email. For customer_id,
 I'll use a template pattern to ensure uniqueness.
 [Types .withColumn("customer_id"...)]

 For realistic names, I'll use the template function with word patterns.
 [Types .withColumn("name"...)]

 Let me specify 100,000 rows across 4 partitions. Why 4 partitions? Because
 my cluster has 4 cores, so this gives good parallelism without too much
 overhead.
 [Types rows=100000, partitions=4]

 Running this now... [Executes cell]

 Good, it generated in 2 seconds. Let me verify the data looks reasonable.
 [Runs df.show(5)]

 Perfect - the customer IDs are unique, names look varied. Ready to move on."
```

---

#### **Scenario 2: Reviewing AI-Generated Code**

**❌ Blind Trust** (Bad):
```
*Pastes AI code*
*Runs it*
"Okay, it worked."
```

**✅ Code Audit** (Good):
```
"I asked the AI to generate a groupBy aggregation. Let me review the code
 it produced before running it.
 [Reads code out loud]

 I see it's doing:
 df.groupBy('customer_id').agg(sum('amount'))

 That looks correct. The groupBy will trigger a shuffle, which is unavoidable
 for aggregation. The sum function is appropriate for calculating totals.

 However, I notice it's not caching the result. Since we use this DataFrame
 twice later, I should add .cache() before the first action.

 Let me add that... [Modifies code]

 Now running it... [Executes]

 Good. Let me check the query plan to confirm the shuffle happened as expected.
 [Runs .explain()]

 Yes, I see the Exchange (shuffle) operation here. This is correct."
```

---

#### **Scenario 3: Hitting an Error**

**❌ Panic Mode** (Bad):
```
*Error appears*
"Uh... this is weird. Let me try something else."
*Changes random things without reading error*
```

**✅ Methodical Debugging** (Good):
```
"Hmm, I got an error. Let me read it carefully...
 [Reads error message out loud]

 It says: 'AnalysisException: cannot resolve column customer_id'

 Okay, so Spark can't find the customer_id column. Let me check the schema.
 [Runs df.printSchema()]

 Ah, I see the issue. The actual column name is 'customerId' in camelCase,
 but I was referencing it as 'customer_id' with an underscore.

 This is a common issue when joining data from different sources with
 different naming conventions. Let me fix my reference.
 [Corrects code]

 Running again... [Executes]

 Perfect, that resolved it. The lesson here is to always check the schema
 before assuming column names, especially when merging from multiple sources."
```

---

## 🤖 Using AI Tools Effectively During the Interview

### The Golden Rule: **You Pilot, AI Assists**

**What the interviewer wants to see**:
- You use AI to **accelerate** (scaffold code, generate boilerplate)
- You **audit and correct** AI output
- You **understand** what the code does
- You **teach** the AI what you need (through prompts)

**What they DON'T want to see**:
- Blindly copying AI code without reading it
- Running code you don't understand
- Letting AI make architectural decisions for you

---

### The Prompt → Review → Refine Cycle

#### **Step 1: Draft Your Prompt (Before Pasting)**

Use a **scratchpad** (separate notepad, comments in cell) to iterate on your prompt:

```markdown
SCRATCHPAD (in a Markdown cell):
---
Prompt draft:
"Generate synthetic e-commerce transaction data with:
- 100K transactions
- Realistic distribution: 80% purchases, 15% returns, 5% refunds
- Customer IDs from 1-10000
- Transaction amounts: log-normal distribution, mean $100, stddev $50
- Date range: last 30 days
- Include: transaction_id, customer_id, product_id, amount, date, status"

Review: This is specific enough. Including the distribution details should
         prevent AI from using uniform random values.
---
```

**Then** paste this prompt into Databricks Assistant or ChatGPT.

---

#### **Step 2: Review AI Output OUT LOUD**

```
"Okay, the AI generated this code. Let me read through it...
 [Scrolls and reads key parts]

 I see it's using dbldatagen, which is correct. It's setting up the
 transaction_id with uniqueValues to ensure no duplicates - good.

 For the amount column, it's using... wait, it's using minValue/maxValue
 which gives uniform distribution. I specifically asked for log-normal.
 This is a hallucination. I need to fix this."
```

---

#### **Step 3: Refine and Explain Your Changes**

```
"I'm modifying the amount column to use an expression that creates
 log-normal distribution. The formula is:
 exp(normal(mean, stddev))

 In PySpark, that's:
 .withColumn('amount', exp(randn() * 50 + 100))

 This gives us the realistic spending pattern where most transactions
 are small, with a long tail of high-value purchases."
 [Makes change]

 Let me also verify the distribution after generation with describe().
 [Runs df.describe('amount').show()]

 Good, the mean is around $100 as expected, and we have that long tail."
```

---

### Common AI Pitfalls to Catch and Narrate

#### **Pitfall 1: Using `collect()` on Large DataFrames**

**AI might generate**:
```python
rows = df.collect()
for row in rows:
    process(row)
```

**Your narration**:
```
"I see the AI is using collect() to pull all data to the driver, then
 processing row-by-row. This won't scale - with 100M records, we'd run
 out of driver memory. I'll refactor to use distributed operations:

 df.withColumn('processed', process_udf(col('data')))

 This processes data in parallel across all executors."
```

---

#### **Pitfall 2: Unnecessary Shuffles**

**AI might generate**:
```python
df.groupBy('a').count().groupBy('b').count()
```

**Your narration**:
```
"This code has two groupBy operations in sequence, which means two shuffles.
 That's inefficient. If we can combine them:

 df.groupBy('a', 'b').count()

 Now it's a single shuffle. For 100M records, this could save minutes."
```

---

#### **Pitfall 3: Not Using Broadcast Joins**

**AI might generate**:
```python
large_df.join(small_df, 'key')
```

**Your narration**:
```
"The AI generated a regular join. Since the small_df is only 10K rows,
 I should broadcast it to avoid a shuffle:

 large_df.join(broadcast(small_df), 'key')

 This sends the small table to all executors once, rather than shuffling
 both tables. Much more efficient."
```

---

## 🎬 Interview Structure & Your Action Plan

### Phase 1: Discovery (5-10 minutes)

**Interviewer gives prompt**:
> "We have customer transaction data from multiple stores. Build a pipeline to analyze purchase patterns and identify high-value customers."

#### **Your Action: Ask Clarifying Questions**

Use the **5W1H Framework**:

**What**:
- "What's the expected data volume? Are we talking thousands, millions, or billions of transactions?"
- "What specific metrics define a 'high-value customer'? Total spend? Frequency? Recency?"
- "What's the output format? A dashboard, a scheduled report, or an API?"

**Where**:
- "Where is the source data? Is it coming from a database, files, or a stream?"
- "Where should the output be stored? Delta Lake, external database, or cloud storage?"

**When**:
- "What's the time range? Historical analysis or real-time monitoring?"
- "How frequently should this update? Daily batch, hourly, or real-time?"

**Who**:
- "Who's the audience? Business stakeholders, data scientists, or operational teams?"

**Why**:
- "What's the business objective? Targeted marketing, churn prevention, or revenue optimization?"

**How**:
- "How should we handle data quality issues? Quarantine bad records or fail the pipeline?"

#### **Then Restate the Problem**:
```
"So to summarize: We're building a daily batch pipeline that ingests
 transaction data from cloud storage, processes approximately 1M
 transactions per day, identifies customers with >$5000 spend in the
 last 90 days, and outputs a ranked list to a Delta table for the
 marketing team's dashboard. Is that correct?"
```

**Why this matters**: Shows you understand requirements before coding, prevents building the wrong thing.

---

### Phase 2: Building (30-40 minutes)

#### **Step 2.1: Create a Spec (In Markdown Cell)**

```markdown
# SOLUTION SPEC

## Data Generation
- **Volume**: 100K transactions (representative sample)
- **Schema**:
  - transaction_id (string, unique)
  - customer_id (string, 1-10000)
  - amount (double, log-normal $100 ± $50)
  - date (timestamp, last 90 days)
  - store_id (string, 1-100)

## Pipeline Architecture
**Bronze**: Raw ingestion (append-only)
**Silver**: Validated transactions (deduped, enriched)
**Gold**: Customer metrics (aggregated)

## Transformations
1. Deduplicate on transaction_id
2. Join with customer dimension (broadcast)
3. Calculate 90-day spend per customer
4. Rank by spend (window function)
5. Filter top 10%

## Output
- Table: gold.high_value_customers
- Columns: customer_id, total_spend_90d, transaction_count, rank
- Partitioned by: date
```

**Narrate this**:
```
"Before coding, let me create a spec to align on the approach.
 I've documented the data generation parameters, the medallion
 architecture I'll use, and the key transformations. Does this
 align with what you're expecting?"
```

---

#### **Step 2.2: Generate Data with AI**

**Narrate your prompt creation**:
```
"I'll use Databricks Assistant to generate the synthetic data.
 Let me draft my prompt first...

 [Types in scratchpad cell]:
 'Generate synthetic transaction data using dbldatagen:
  - 100K transactions
  - customer_id: 1-10000
  - amount: log-normal distribution (mean=100, stddev=50)
  - date: uniformly distributed over last 90 days
  - Include validation: no null amounts, positive values only'

 I'm being specific about the distribution to avoid uniform random data.
 Submitting this to the AI now..."
```

**Review AI output**:
```
"Let me review what the AI generated...
 [Reads code sections]

 Good, it's using dbldatagen. The transaction_id has uniqueValues=100000,
 so no duplicates. The customer_id range is correct.

 However, I see it's using minValue/maxValue for amount, which is uniform.
 I need to change this to log-normal. Let me add an expression column..."
```

**Validate the data**:
```
"Running the generation... [Executes]

 Generated in 3 seconds. Let me validate:
 [Runs df.printSchema()]
 Schema looks correct.

 [Runs df.count()]
 Exactly 100K records as specified.

 [Runs df.describe('amount').show()]
 Mean is $98, close to target $100. Standard deviation is $51.
 This looks realistic.

 [Runs df.show(5)]
 Sample data looks good. Moving on to transformations."
```

---

#### **Step 2.3: Build Pipeline (Think → Code → Validate Loop)**

For each transformation:

**1. Think (Explain WHAT and WHY)**:
```
"Next, I need to deduplicate transactions. I'll use dropDuplicates()
 on transaction_id. This is important because source systems sometimes
 send duplicate records, and we don't want to double-count revenue."
```

**2. Code (Narrate as you write)**:
```
"I'm using dropDuplicates with the transaction_id column...
 [Types: transactions_deduped = transactions.dropDuplicates(['transaction_id'])]

 This is a wide transformation that requires a shuffle, but it's necessary
 to ensure data quality."
```

**3. Validate (Check your work)**:
```
"Let me verify duplicates were removed:
 [Runs: print(f'Before: {transactions.count()}, After: {transactions_deduped.count()}')]

 Removed 50 duplicates. That's 0.05%, which is realistic for a production
 system."
```

---

#### **Step 2.4: Handle the Inevitable Error**

**When you hit an error** (you will, it's normal):

**1. Read it carefully OUT LOUD**:
```
"I'm getting an error. Let me read it...
 [Reads error message]
 'AnalysisException: cannot resolve `customer_id` given input columns: [customerId, amount, date]'

 So Spark can't find 'customer_id' because the actual column is 'customerId'.
```

**2. Hypothesize the cause**:
```
"This happened because when I generated the customer dimension, I didn't
 standardize the naming convention. Let me check the schema...
 [Runs customers.printSchema()]

 Yes, it's camelCase 'customerId', but my transactions table uses snake_case
 'customer_id'. I have two options: rename one, or use column objects in the join.

 I'll rename the customers column to match, since that's just the dimension.
 [Types: customers = customers.withColumnRenamed('customerId', 'customer_id')]
```

**3. Verify the fix**:
```
"Rerunning the join... [Executes]

 Success. This is a good reminder to establish naming conventions early,
 especially when merging data from different sources."
```

---

### Phase 3: Performance Discussion (10-15 minutes)

**Interviewer**: *"How would this scale to 100 million transactions?"*

#### **Your Response Framework**:

**1. Acknowledge the scale**:
```
"100 million transactions is approximately 1000x larger. That changes
 several things about the architecture."
```

**2. Identify bottlenecks**:
```
"The key bottlenecks would be:
 1. The groupBy aggregation - this requires a shuffle
 2. The join with the customer dimension
 3. The deduplication operation

 Let me walk through optimizations for each..."
```

**3. Propose specific optimizations**:
```
"SHUFFLE PARTITIONS:
 Current default is 200 partitions. With 100M rows at ~500 bytes each,
 that's 50GB of data. I'd calculate:
 50GB / 0.5GB per partition = 100 partitions minimum
 I'd set to 200-400 for headroom:
 spark.conf.set('spark.sql.shuffle.partitions', '400')

 BROADCAST JOIN:
 The customer dimension is 10K rows, so ~1MB. Well under the 10GB broadcast
 threshold. I'd explicitly broadcast it:
 transactions.join(broadcast(customers), 'customer_id')

 PARTITIONING:
 I'd partition the output by date:
 .partitionBy('date').saveAsTable('gold.high_value_customers')
 This enables partition pruning for time-range queries.

 INCREMENTAL PROCESSING:
 Instead of processing all 100M daily, I'd use Delta MERGE:
 - Process only new transactions since last run
 - MERGE to update existing customer aggregates
 - This makes the pipeline idempotent and more efficient"
```

**4. Demonstrate with query plan**:
```
"Let me show this with explain()...
 [Runs: result.explain('formatted')]

 Here I can see the Exchange (shuffle) on line 5. With my optimizations,
 this shuffle would be distributed across 400 partitions instead of 200,
 reducing the per-task data from 250MB to 125MB."
```

---

## 🚫 The "Bail Out" Strategy

### When to Use It

**Use "Bail Out" when**:
- You've spent >2 minutes on syntax/imports/minor errors
- You're debugging environment issues (cluster, libraries)
- You're stuck on something trivial that's blocking progress

**How to ask**:
```
"I've been stuck on this import syntax for a couple minutes. Can we
 'bail out' and move forward? I want to focus on the architecture rather
 than this syntax detail."
```

**Why this is GOOD**:
- Shows you prioritize high-level problem solving over syntax
- Demonstrates awareness of time management
- Signals you know when to ask for help (critical in consulting!)

---

### When NOT to Use It

**Don't "Bail Out" on**:
- Conceptual problems (how to solve the business logic)
- Architectural decisions (which join strategy to use)
- Performance questions (how to optimize a shuffle)

These are what the interview is testing. Syntax is not.

---

## 📊 Real Interview Example: Full Transcript

### **Scenario**: Customer Lifetime Value Analysis

**[Discovery Phase]**

**Interviewer**: "We need to analyze customer lifetime value from transaction data."

**You**:
```
"Great, let me ask a few clarifying questions to make sure I understand:

1. Data volume: How many customers and transactions are we working with?
   Thousands, millions, or more?

2. Time horizon: Are we calculating lifetime value over all history,
   or a specific period like the last 12 months?

3. Definition: How do we define 'lifetime value'? Total spend, profit,
   or something more complex like predicted future value?

4. Segmentation: Do we need to break this down by any dimensions like
   product category, region, or customer segment?

5. Output: What's the deliverable? A table, a report, or real-time API?
"
```

**Interviewer**: "Good questions. Let's say 100K customers, 1M transactions over the past year. LTV is total spend. No segmentation needed for now. Output to a Delta table."

**You**:
```
"Perfect. So to summarize: I'll build a pipeline that:
1. Generates synthetic transaction data (1M transactions, 100K customers, last year)
2. Aggregates total spend per customer
3. Ranks customers by spend
4. Outputs to a Delta table

I'll use medallion architecture: Bronze for raw data, Silver for validated,
Gold for the aggregated LTV metric. Does that sound right?"
```

**Interviewer**: "Yes, let's do it."

---

**[Building Phase]**

**You**:
```
"Let me start by creating a spec in a Markdown cell so we're aligned...
[Creates spec as shown earlier]

Now I'll generate the synthetic data. I'll use Databricks Assistant for this.
Let me draft my prompt first...
[Types in scratchpad]

Prompt: 'Generate synthetic transaction data using dbldatagen:
- 1M transactions
- 100K unique customers (customer_id)
- Transaction amounts: log-normal distribution, mean $75, stddev $50
- Dates: uniformly distributed over last 365 days
- Columns: transaction_id, customer_id, amount, date'

I'm specifying log-normal because real-world transaction amounts follow
that distribution - most are small, with a long tail of high values.

Submitting to AI... [Pastes into Databricks Assistant]
"
```

**You** (reviewing AI output):
```
"Okay, the AI generated this. Let me review it...
[Reads code]

I see it's using dbldatagen correctly. The transaction_id has uniqueValues
set to 1M, so no duplicates. Good.

However, I notice the amount column is using minValue/maxValue, which gives
uniform distribution. I asked for log-normal. Let me fix that...

[Modifies code to use expression with exp and randn]

Running this now... [Executes]

Generated in 5 seconds. Let me validate:
[Runs df.show(5), df.count(), df.describe('amount')]

Count is exactly 1M. Amount distribution shows mean around $75, good.
Let me check for nulls...
[Runs df.filter(col('amount').isNull()).count()]

Zero nulls. Perfect. Moving to transformations."
```

**You** (building pipeline):
```
"First step is writing to Bronze. This is the raw data layer...
[Writes code]

transactions.write.format('delta').mode('overwrite').saveAsTable('bronze.transactions')

Bronze is append-only in production, but for this demo I'm using overwrite.

Next, Silver layer. I need to validate the data. Let me check for any
negative amounts or missing customer IDs...
[Writes validation code]

validated = transactions.filter(
    (col('amount') > 0) &
    (col('customer_id').isNotNull())
)

Running validation... [Executes]

[Checks counts]
All records passed validation. In production, I'd quarantine invalid
records rather than filtering them, so we don't lose data silently.

Writing to Silver...
validated.write.format('delta').mode('overwrite').saveAsTable('silver.transactions')
"
```

**You** (calculating LTV):
```
"Now for the Gold layer: customer lifetime value.

This is a groupBy aggregation on customer_id to sum amounts. This will
trigger a shuffle, which is unavoidable for aggregation, but I'll make
sure the partition count is appropriate.

[Writes code]

ltv = (
    spark.read.format('delta').table('silver.transactions')
    .groupBy('customer_id')
    .agg(
        sum('amount').alias('lifetime_value'),
        count('transaction_id').alias('transaction_count'),
        avg('amount').alias('avg_transaction_value')
    )
)

I'm also calculating transaction count and average value, which are useful
business metrics.

Let me add a rank to identify top customers...
[Adds window function]

from pyspark.sql.window import Window

ltv_ranked = (
    ltv
    .withColumn('rank',
                row_number().over(Window.orderBy(desc('lifetime_value'))))
)

Running this... [Executes]

Great. Let me look at the top 10 customers:
[Runs ltv_ranked.show(10)]

Perfect. Lifetime values range from $75K down to $50K for top 10.
This looks realistic.

Writing to Gold:
ltv_ranked.write.format('delta').mode('overwrite').saveAsTable('gold.customer_ltv')

Done. Let me verify the output table...
[Runs spark.read.table('gold.customer_ltv').count()]

100K customers as expected."
```

---

**[Performance Discussion]**

**Interviewer**: "What if we had 100 million transactions instead of 1 million?"

**You**:
```
"100 million transactions changes the game. That's 100x larger, so roughly
 100GB of data assuming 1KB per transaction.

The main bottleneck would be the groupBy aggregation. Let me walk through
optimizations:

PARTITION COUNT:
Default 200 shuffle partitions would mean 500MB per partition (100GB / 200).
That's at the upper limit of acceptable. I'd increase to 400 partitions:
spark.conf.set('spark.sql.shuffle.partitions', '400')

This gives 250MB per partition, which is more manageable.

INCREMENTAL PROCESSING:
Instead of processing all 100M transactions daily, I'd use Delta MERGE:
- Process only new transactions since the last run
- Use MERGE to update customer aggregates incrementally
- This makes the job idempotent and much faster

Here's how that would look:
[Writes MERGE example]

from delta.tables import DeltaTable

new_transactions = spark.read...filter(date > last_run_date)

new_ltv = new_transactions.groupBy('customer_id').agg(sum('amount'))

gold_table = DeltaTable.forName(spark, 'gold.customer_ltv')

(gold_table.alias('target')
 .merge(new_ltv.alias('source'), 'target.customer_id = source.customer_id')
 .whenMatchedUpdate(set={'lifetime_value': 'target.lifetime_value + source.amount'})
 .whenNotMatchedInsert(values={'customer_id': 'source.customer_id',
                                'lifetime_value': 'source.amount'})
 .execute())

PARTITIONING:
I'd partition the output by date or month:
.partitionBy('year', 'month')

This enables partition pruning for time-based queries.

CACHING:
If this LTV calculation is used downstream multiple times, I'd cache it:
ltv.cache().count()

But only if reused - caching unused data wastes memory.

Would you like me to demonstrate the query plan with explain()?
"
```

**Interviewer**: "Yes, let's see the plan."

**You**:
```
"Sure. Let me run explain on the aggregation query...
[Runs ltv_ranked.explain('formatted')]

Looking at the plan:
- Line 7: Exchange hashpartitioning (customer_id, 200)
  This is the shuffle for the groupBy. With my optimization, this would
  be 400 partitions instead of 200.

- The HashAggregate operations before and after the Exchange are the
  map-side and reduce-side aggregations. This is expected for groupBy.

- No broadcast joins here because we're not joining in this query.
  But if we joined with a customer dimension table, I'd use:
  .join(broadcast(customers), 'customer_id')

The plan looks efficient. The only expensive operation is the shuffle,
which is unavoidable for aggregation."
```

---

## ✅ Final Checklist: Are You Ready?

Practice these until they feel natural:

- [ ] **I can think out loud continuously** for 60 minutes without awkward silences
- [ ] **I can explain WHY** I'm making each decision (not just WHAT I'm doing)
- [ ] **I can audit AI-generated code** and identify at least 3 common issues (collect, shuffles, broadcasts)
- [ ] **I can read an error message** and diagnose the root cause in <1 minute
- [ ] **I can use "Bail Out" appropriately** when stuck on syntax
- [ ] **I can explain code to a "customer"** without technical jargon
- [ ] **I can propose performance optimizations** with specific numbers (partition counts, data sizes)
- [ ] **I can use `.explain()`** to read query plans and identify shuffles
- [ ] **I stay calm and methodical** when hitting bugs or errors
- [ ] **I ask clarifying questions** before starting to code

---

## 🎤 Your Interview Day Mantra

> **"I am the architect. AI is my assistant. My interviewer is my teammate. I think out loud. I explain my reasoning. I stay calm when stuck. I ask for help when needed. I focus on architecture, not syntax."**

---

## 🌟 Remember

**This is a conversation, not an exam.**

Your interviewer wants you to succeed. They're evaluating how you'd work with them on real customer engagements. Show them:
- You can break down complex problems
- You can use modern tools effectively
- You can communicate technical concepts clearly
- You can stay resilient under pressure
- You'd be a great teammate

**You've got this!** 🚀

---

**Last Updated**: April 2025
**For**: Databricks Sr. Solutions Architect - Vibe Coding Interview
