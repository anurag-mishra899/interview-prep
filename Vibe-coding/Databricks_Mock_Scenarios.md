# Databricks Vibe Interview - Mock Scenario Prompts

Practice these scenarios in Databricks Free Edition. Treat each as a 60-minute exercise.

---

## 🏢 Business Analytics Scenarios

### Scenario 1: Customer Lifetime Value Analysis
**Prompt**: "A retail company wants to identify their highest-value customers. Generate synthetic customer transaction data spanning 2 years and calculate customer lifetime value (CLV). Identify the top 10% of customers and any trends in their behavior."

**What to demonstrate**:
- Multi-table data generation (customers, transactions, products)
- Realistic distributions (log-normal for prices, seasonal patterns)
- Join operations and aggregations
- Window functions for ranking
- Customer segmentation logic

**Expected deliverables**:
- Customer insights table with CLV, frequency, recency
- Top customer identification
- Behavioral patterns (avg order value, purchase frequency)

**Think-aloud points**:
- Why you chose certain distributions
- How joins will execute (broadcast vs shuffle)
- Business logic validation ("Does this CLV formula make sense?")

---

### Scenario 2: Sales Funnel Analysis
**Prompt**: "An e-commerce platform wants to analyze their sales funnel. Generate event data for user sessions showing: page views, add-to-cart, checkout initiation, and purchase completion. Calculate conversion rates at each stage and identify drop-off points."

**What to demonstrate**:
- Event sequence generation with timestamps
- Funnel logic (users progressing through stages)
- Conversion rate calculations
- Cohort analysis (by traffic source, date)

**Expected deliverables**:
- Funnel metrics table (stage, users, conversion rate)
- Drop-off analysis
- Time-to-conversion metrics

**Think-aloud points**:
- How to model event sequences realistically
- Why some users should drop off at each stage
- Window functions for sequential event analysis

---

### Scenario 3: Inventory Optimization
**Prompt**: "A warehouse needs to optimize inventory levels. Generate data for product stock levels, daily sales, and reorder events. Identify products at risk of stockout and those with excess inventory."

**What to demonstrate**:
- Time-series data generation
- Running totals (inventory = previous + reorders - sales)
- Alert logic (stock < threshold)
- Aggregation for inventory trends

**Expected deliverables**:
- Current inventory status by product
- Products requiring reorder
- Historical inventory trends

---

## 🔍 Data Engineering Scenarios

### Scenario 4: ETL Pipeline with Data Quality
**Prompt**: "Build a pipeline to ingest daily sales files. The data has quality issues: missing values, duplicates, invalid records (negative quantities, future dates). Clean the data, quarantine bad records, and write clean data to a Delta table using MERGE for idempotency."

**What to demonstrate**:
- Data quality validation framework
- Error handling and quarantine strategy
- Delta MERGE for upsert logic
- Idempotent pipeline design

**Expected deliverables**:
- Clean sales table (Delta format)
- Quarantine table with invalid records
- Data quality metrics (% valid, common errors)

**Think-aloud points**:
- Why MERGE makes pipeline idempotent
- Trade-offs: reject vs fix bad data
- How to handle schema evolution

---

### Scenario 5: Slowly Changing Dimension (SCD Type 2)
**Prompt**: "Implement a Type 2 SCD for customer dimension data. When a customer's address or status changes, keep historical records. Generate initial customer data and then simulate updates to show how your pipeline handles changes."

**What to demonstrate**:
- SCD Type 2 logic (effective dates, current flags)
- Delta MERGE with conditional logic
- Historical tracking

**Expected deliverables**:
- Customer dimension table with history
- Demonstration of update handling
- Query showing historical state at a point in time

---

### Scenario 6: Change Data Capture (CDC) Processing
**Prompt**: "Simulate CDC events from a source database (inserts, updates, deletes). Process these events to maintain a current-state table and an audit trail of all changes."

**What to demonstrate**:
- CDC event generation (operation type: I/U/D)
- Event sequence processing
- MERGE logic for different operation types
- Audit trail maintenance

**Expected deliverables**:
- Current-state table
- Audit log of all changes
- Validation that state is correct

---

## 📊 Analytics & Reporting Scenarios

### Scenario 7: Time-Series Anomaly Detection
**Prompt**: "Generate sensor data from IoT devices over 30 days. Include normal operational patterns and periodic anomalies (sensor failures, unusual readings). Identify anomalous periods using statistical methods."

**What to demonstrate**:
- Time-series data generation with patterns
- Rolling window calculations
- Statistical anomaly detection (z-score, IQR)
- Grouping by device for per-device baselines

**Expected deliverables**:
- Anomaly events table
- Per-device baseline metrics
- Visualization-ready aggregates

**Think-aloud points**:
- Why you chose specific anomaly detection method
- How window functions calculate rolling stats
- Handling different anomaly types (spike, drift, missing data)

---

### Scenario 8: Cohort Analysis
**Prompt**: "A SaaS platform wants to analyze user retention by signup cohort. Generate user signup and activity data. Calculate retention rates for each weekly cohort over their first 12 weeks."

**What to demonstrate**:
- Cohort definition (grouping by signup week)
- Retention logic (active in week N after signup)
- Pivot operations for retention matrix
- Visualization-ready output

**Expected deliverables**:
- Retention rate table (cohort x week)
- Cohort size and activity metrics
- Churn indicators

---

### Scenario 9: A/B Test Analysis
**Prompt**: "Analyze results of an A/B test on website UI. Generate user interaction data for control and treatment groups. Calculate statistical significance of conversion rate differences."

**What to demonstrate**:
- Experimental design data generation
- Group comparison metrics
- Statistical significance calculation
- Confidence intervals

**Expected deliverables**:
- Test metrics (conversion rate, avg value per control/treatment)
- Statistical significance results
- Recommendation (launch/iterate/abandon)

---

## 🔧 Data Quality & Operations Scenarios

### Scenario 10: Duplicate Detection & Deduplication
**Prompt**: "A CRM system has accumulated duplicate customer records over time. Generate customer data with duplicates (exact, fuzzy matches on name/email). Implement a deduplication strategy to identify and resolve duplicates."

**What to demonstrate**:
- Duplicate detection logic (exact and fuzzy)
- Grouping and merging strategies
- Master record selection (most recent, most complete)

**Expected deliverables**:
- Deduplicated customer table
- Duplicate groups for manual review
- Deduplication logic explanation

---

### Scenario 11: Schema Evolution Handling
**Prompt**: "Data schema changes over time (new columns added, types changed). Generate data representing multiple schema versions and build a pipeline that handles schema evolution gracefully."

**What to demonstrate**:
- Schema inference and validation
- Delta schema evolution features
- Backward compatibility handling

**Expected deliverables**:
- Unified table with all schema versions
- Demonstration of schema merge
- Null handling for new columns

---

### Scenario 12: Data Lineage & Audit Trail
**Prompt**: "Build a pipeline that tracks data lineage. Every transformation should be auditable: when it ran, what data it processed, what changes it made. Generate source data, apply transformations, and maintain full audit trail."

**What to demonstrate**:
- Metadata capture (run timestamp, record counts)
- Audit table design
- Idempotent processing with audit

**Expected deliverables**:
- Transformed data table
- Audit/lineage table
- Query showing full data lineage

---

## 🚀 Performance & Scale Scenarios

### Scenario 13: Handling Data Skew
**Prompt**: "You have transaction data where 80% of transactions belong to 5% of customers (heavy skew). Generate skewed data and demonstrate how you'd handle this for efficient aggregation."

**What to demonstrate**:
- Skew detection (partition size analysis)
- Salting technique for skewed keys
- Comparison of performance with/without salting

**Expected deliverables**:
- Aggregation results
- Explanation of skew mitigation
- Query plan showing improved parallelism

**Think-aloud points**:
- How to detect skew (partition sizes)
- Why skew causes performance issues
- Trade-offs of salting approach

---

### Scenario 14: Incremental Processing
**Prompt**: "Transform a batch processing job to incremental. Generate daily data files and process only new/changed data instead of full refreshes. Maintain watermarks to track processing state."

**What to demonstrate**:
- Watermark/checkpoint management
- Incremental data identification
- Delta table updates (MERGE)
- Recovery/replay handling

**Expected deliverables**:
- Incrementally updated target table
- Watermark tracking mechanism
- Demonstration of idempotency

---

### Scenario 15: Large-Scale Aggregation Optimization
**Prompt**: "Generate 10M+ rows of transaction data. Calculate complex aggregations (multiple dimensions, window functions). Optimize for performance using partitioning, caching, and query optimization techniques."

**What to demonstrate**:
- Large data generation (efficient methods)
- Query plan analysis (.explain())
- Optimization techniques applied
- Performance measurement

**Expected deliverables**:
- Aggregation results
- Before/after optimization metrics
- Explanation of improvements

---

## 🌐 Real-Time & Streaming Scenarios

### Scenario 16: Streaming Simulation
**Prompt**: "Simulate a real-time clickstream using batch data with timestamps. Process it incrementally using Structured Streaming concepts to calculate rolling metrics (sessions per hour, top pages)."

**What to demonstrate**:
- Micro-batch processing simulation
- Windowing operations (tumbling, sliding)
- Watermarking for late data
- Stateful aggregations

**Expected deliverables**:
- Real-time metrics table
- Handling of late/out-of-order events
- Checkpoint/recovery explanation

---

### Scenario 17: Event-Time Processing
**Prompt**: "Generate IoT sensor events where event timestamps differ from ingestion timestamps (late arrivals, out-of-order). Process using event time for accurate windowed aggregations."

**What to demonstrate**:
- Event-time vs processing-time understanding
- Watermark configuration
- Late data handling strategies

**Expected deliverables**:
- Time-windowed aggregations
- Late event statistics
- Explanation of watermarking

---

## 🤖 ML & Advanced Analytics Scenarios

### Scenario 18: Feature Engineering Pipeline
**Prompt**: "Prepare a dataset for a churn prediction model. Generate customer activity data and engineer features: recency, frequency, monetary value, engagement scores, rolling averages. Handle categorical encoding and feature scaling."

**What to demonstrate**:
- Feature extraction from raw events
- Categorical encoding (one-hot, label)
- Feature scaling/normalization
- Train/test split

**Expected deliverables**:
- Feature table ready for ML
- Feature distribution analysis
- Correlation analysis

---

### Scenario 19: Recommendation System Data Prep
**Prompt**: "Generate user-item interaction data (views, purchases, ratings). Create co-occurrence matrices and user/item similarity features for a collaborative filtering recommender."

**What to demonstrate**:
- User-item matrix creation
- Similarity calculations (cosine, Jaccard)
- Sparse matrix handling in Spark

**Expected deliverables**:
- User-item interaction matrix
- Item similarity scores
- Top-N similar items per item

---

### Scenario 20: Text Analytics Pipeline
**Prompt**: "Generate customer review data with text comments. Extract insights: sentiment trends, common keywords, topic clustering. Clean text, tokenize, and aggregate by product/time period."

**What to demonstrate**:
- Text preprocessing (lowercase, remove punctuation)
- Tokenization and stopword removal
- Aggregation of text features
- (Optional) Basic sentiment scoring

**Expected deliverables**:
- Cleaned review dataset
- Keyword frequency by product
- Review metrics aggregates

---

## 📋 Practice Framework

For each scenario, follow this structure:

### 1. Discovery (5-10 min)
- Read prompt
- Ask 3-5 clarifying questions
- Restate problem in your own words
- Outline approach (3-5 steps)

### 2. Data Generation (10-15 min)
- Generate realistic synthetic data
- Introduce appropriate complexity (nulls, skew, etc.)
- Validate data quality
- Show sample records

### 3. Implementation (25-35 min)
- Build solution step by step
- Think out loud continuously
- Validate intermediate results
- Handle errors gracefully

### 4. Validation & Scale Discussion (10-15 min)
- Test solution correctness
- Explain code to a "customer"
- Discuss scalability considerations
- Identify potential improvements

---

## 🎯 Success Metrics for Practice

After each mock scenario, evaluate yourself:

**Computational Thinking**: ⭐⭐⭐⭐⭐
- Did I break the problem into logical steps?
- Were my transformations efficient?

**Code Stewardship**: ⭐⭐⭐⭐⭐
- Did I review AI-generated code?
- Did I explain what code does under the hood?

**Resilience**: ⭐⭐⭐⭐⭐
- How did I handle errors/blockers?
- Did I use resources effectively?

**Distributed Reasoning**: ⭐⭐⭐⭐⭐
- Did I explain shuffles, partitioning?
- Did I discuss scalability?

**Think Out Loud**: ⭐⭐⭐⭐⭐
- Did I narrate continuously?
- Did I explain trade-offs?

**Communication**: ⭐⭐⭐⭐⭐
- Could a customer understand my explanation?
- Were my responses concise and clear?

---

## 💡 Pro Tips

1. **Time yourself**: Stick to 60-minute limit for realism
2. **Record yourself**: Review to catch silent coding periods
3. **Practice with a friend**: Have them play the interviewer
4. **Rotate scenarios**: Don't over-practice the same one
5. **Focus on weak areas**: If distributed reasoning is hard, practice more Scenario 13-15

---

**Start with easier scenarios (1-3) then progress to complex ones (16-20). Good luck! 🚀**
