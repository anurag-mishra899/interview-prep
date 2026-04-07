# Databricks Sr. Solutions Architect Interview Preparation Guide
**Interview Date**: TBD
**Candidate**: Anurag Mishra
**Position**: Sr. Solutions Architect @ Databricks
**Interview Type**: Design & Architecture Interview (60 minutes)

---

## Table of Contents
1. [Interview Overview](#interview-overview)
2. [Interview Structure & Evaluation Areas](#interview-structure--evaluation-areas)
3. [Core Concepts to Master](#core-concepts-to-master)
4. [Architecture Patterns & Best Practices](#architecture-patterns--best-practices)
5. [Technical Spike Areas](#technical-spike-areas)
6. [Common Interview Scenarios](#common-interview-scenarios)
7. [Preparation Strategy](#preparation-strategy)
8. [Practice Questions](#practice-questions)
9. [Key Talking Points](#key-talking-points)
10. [Resources](#resources)

---

## Interview Overview

### What to Expect
- **Duration**: 60 minutes
- **Format**: High-level business scenario requiring production-ready solution design
- **Interviewers**: 1-2 Solutions Architects/Delivery Solutions Architects acting as stakeholders
- **Approach**: Treat this as a real customer discovery session
- **Deliverable**: Whiteboard/diagram your architecture (Google Slides, paper, or digital tool)

### Evaluation Criteria
The interview assesses you across **three core areas**:

1. **Discovery & Problem Framing (20-25%)**
   - How you gather requirements
   - How you identify constraints and assumptions
   - Ability to ask clarifying questions
   - Understanding business objectives vs technical requirements

2. **Core Architecture Design (40-50%)**
   - End-to-end flow and data layers
   - Technology selection and justification
   - Scalability and resilience
   - Cost optimization

3. **Technical "Spike" Areas (25-35%)**
   - Deep-dive into 1-3 specialized domains
   - Choose from: **Data Engineering**, **Data Warehousing**, or **AI/ML**
   - Ensure recruiter knows your spike area in advance

---

## Interview Structure & Evaluation Areas

### Phase 1: Discovery & Problem Framing (10-15 mins)

**What They're Looking For:**
- Do you jump straight to solutions, or do you ask clarifying questions?
- Can you distinguish between must-haves and nice-to-haves?
- Do you understand the business context beyond just technical requirements?

**Key Questions to Ask:**

**Business Context:**
- What are the primary business objectives? (Cost reduction, revenue growth, compliance, customer experience?)
- Who are the end users? (Data analysts, data scientists, business executives, external customers?)
- What does success look like? What are the KPIs?
- What's the timeline for delivery? (POC, MVP, full production?)

**Data Characteristics:**
- What are the data sources? (Databases, APIs, files, streaming sources, SaaS applications?)
- What's the data volume? (GB/TB/PB per day?)
- What's the data velocity? (Real-time streaming, micro-batch, daily batch?)
- What's the data variety? (Structured, semi-structured, unstructured?)
- What's the data quality like? (Clean, needs validation, transformation required?)

**Non-Functional Requirements:**
- What are the SLAs? (Latency, availability, recovery time?)
- What's the budget constraint?
- Are there compliance/regulatory requirements? (GDPR, HIPAA, SOC2, data residency?)
- What's the expected user concurrency?
- What are the disaster recovery requirements? (RTO/RPO?)

**Existing Infrastructure:**
- What cloud platform(s)? (AWS, Azure, GCP, multi-cloud?)
- What existing tools/systems must we integrate with?
- What's the current data architecture? (Migration vs greenfield?)
- What are the security requirements? (Network isolation, encryption, access control?)

---

### Phase 2: Core Architecture Design (25-30 mins)

**What They're Looking For:**
- Can you design a production-ready, not just functional, architecture?
- Do you consider the full lifecycle: ingestion → processing → storage → serving → governance?
- Can you articulate trade-offs and justify your decisions?
- Do you think about operational aspects: monitoring, disaster recovery, cost?

**Design Checklist:**

#### 1. **Data Ingestion Layer**
- [ ] Batch vs Streaming vs Hybrid approach
- [ ] Source connectors (Kafka, Event Hubs, Delta Sharing, Partner Connect, JDBC, REST APIs)
- [ ] Auto Loader for incremental file ingestion
- [ ] Schema evolution and validation
- [ ] Error handling and dead letter queues

#### 2. **Data Storage & Lake Architecture**
- [ ] Delta Lake as the storage format
- [ ] Medallion Architecture (Bronze → Silver → Gold)
  - **Bronze**: Raw, immutable data as-is from source
  - **Silver**: Cleaned, validated, deduplicated, joined
  - **Gold**: Aggregated, business-ready, optimized for consumption
- [ ] Partitioning strategy (by date, region, category?)
- [ ] Data retention policies
- [ ] Storage optimization (Z-ordering, compaction, vacuum)

#### 3. **Data Processing & Transformation**
- [ ] Apache Spark for distributed processing
- [ ] Delta Live Tables (DLT) for declarative ETL pipelines
- [ ] Batch vs Streaming processing mode
- [ ] Job orchestration (Workflows, Databricks Jobs, external orchestrators)
- [ ] Incremental processing patterns
- [ ] Error handling and retry logic

#### 4. **Data Governance & Security**
- [ ] Unity Catalog for centralized governance
  - Metastore design (one per region recommended)
  - Catalog structure (domain-based: sales, marketing, finance)
  - Schema organization (bronze, silver, gold per catalog)
- [ ] Identity and Access Management
  - SCIM integration with IdP
  - Principle of least privilege
  - Group-based ownership for production catalogs
- [ ] Row-level and column-level security
- [ ] Data lineage and audit logging
- [ ] Data classification (PII, sensitive data)
- [ ] Encryption (at rest, in transit)

#### 5. **Serving Layer**
- [ ] Databricks SQL for analytics and BI
- [ ] SQL warehouses (Serverless vs Classic)
- [ ] Delta Sharing for secure data sharing
- [ ] REST APIs for applications
- [ ] ML model serving (Model Serving endpoints)
- [ ] Query optimization and caching

#### 6. **Analytics & AI/ML**
- [ ] BI integration (Power BI, Tableau, Looker)
- [ ] Feature stores for ML
- [ ] MLflow for experiment tracking and model registry
- [ ] Model training and deployment
- [ ] Online vs batch inference

#### 7. **Operational Excellence**
- [ ] Monitoring and alerting (Databricks monitoring, CloudWatch/Azure Monitor)
- [ ] Logging and debugging
- [ ] Cost optimization (autoscaling, spot instances, photon)
- [ ] Disaster recovery and backup
- [ ] Multi-region deployment strategy
- [ ] Performance tuning and optimization

---

### Phase 3: Technical Deep Dives (15-20 mins)

**Choose Your Spike Area** (confirm with recruiter beforehand):

#### Option 1: Data Engineering
**Deep-dive topics:**
- Change Data Capture (CDC) patterns
- Slowly Changing Dimensions (SCD Type 1, 2, 3)
- Event-time processing vs processing-time
- Exactly-once semantics with Delta Lake
- Handling late-arriving data
- Data quality frameworks (expectations, constraints)
- Optimizing shuffle operations
- Partition pruning and predicate pushdown
- Streaming aggregations and windowing
- Backfill strategies for historical data

#### Option 2: Data Warehousing
**Deep-dive topics:**
- Star schema vs snowflake schema design
- Dimensional modeling best practices
- Aggregate tables and materialized views
- Query optimization techniques
- Concurrent user management (warehouse sizing)
- Workload isolation and prioritization
- Cost optimization for analytics workloads
- BI tool integration patterns
- Slowly Changing Dimensions (SCD) implementation
- Incremental refresh strategies

#### Option 3: AI/ML
**Deep-dive topics:**
- Feature engineering pipelines
- Feature Store design and implementation
- Model training at scale (distributed training)
- Hyperparameter tuning strategies
- Model versioning and experiment tracking (MLflow)
- Model deployment patterns (batch, real-time, streaming)
- A/B testing for models
- Model monitoring and drift detection
- AutoML integration
- LLMs and Generative AI on Databricks
- Agent system design patterns

---

## Core Concepts to Master

### 1. Databricks Lakehouse Architecture

**Key Principles:**
- **Unified platform**: One architecture for data warehousing, data engineering, streaming, data science, and ML
- **Open format**: Built on Apache Spark, Delta Lake, MLflow (all open source)
- **ACID transactions**: Delta Lake provides ACID guarantees on data lakes
- **Schema enforcement and evolution**: Prevent bad data, evolve schemas safely
- **Time travel**: Query historical versions of data
- **Scalability**: Elastic compute, decouple storage and compute

**Lakehouse vs Data Warehouse vs Data Lake:**
| Feature | Data Warehouse | Data Lake | Lakehouse |
|---------|---------------|-----------|-----------|
| Data Format | Proprietary | Open (Parquet, ORC) | Open (Delta) |
| ACID Support | ✅ Yes | ❌ No | ✅ Yes |
| Schema | Enforced | Schema-on-read | Enforced + Evolution |
| ML Support | ❌ Limited | ✅ Yes | ✅ Yes |
| BI Performance | ✅ Fast | ❌ Slow | ✅ Fast |
| Cost | 💰💰💰 High | 💰 Low | 💰💰 Medium |

### 2. Medallion Architecture (Multi-Hop)

**Bronze Layer (Raw/Landing):**
- **Purpose**: Ingest data as-is from source systems
- **Characteristics**:
  - Immutable, append-only
  - Minimal transformation (just schema validation)
  - Preserves full fidelity and history
  - Can replay/reprocess from source
- **Format**: Delta tables with minimal schema
- **Use Cases**: Audit trail, reprocessing, debugging

**Silver Layer (Cleaned/Conformed):**
- **Purpose**: Cleaned, validated, deduplicated, joined data
- **Characteristics**:
  - Apply business rules and data quality checks
  - Standardize formats and naming conventions
  - Merge incremental updates (SCD Type 1/2)
  - Join related datasets
- **Format**: Delta tables with enforced schema
- **Use Cases**: Data science, feature engineering, downstream ETL

**Gold Layer (Curated/Business):**
- **Purpose**: Business-level aggregates and dimensional models
- **Characteristics**:
  - Optimized for query performance
  - Aggregated metrics and KPIs
  - Star/snowflake schemas for BI
  - Highly denormalized
- **Format**: Delta tables with Z-ordering
- **Use Cases**: BI dashboards, reporting, executive analytics

**Alternative: Hub-and-Spoke Pattern**
- **Data Hub**: Centralized shared assets (e.g., SAP data, reference data)
- **Data Domains**: Domain-specific processing (e.g., sales domain, marketing domain)
- **Benefits**: Clear ownership, decentralized governance, domain-driven design

### 3. Delta Lake Deep Dive

**Core Features:**
- **ACID Transactions**: Multi-statement transactions with serializable isolation
- **Time Travel**: `SELECT * FROM table VERSION AS OF 10` or `TIMESTAMP AS OF '2024-01-01'`
- **Schema Enforcement**: Reject writes that don't match table schema
- **Schema Evolution**: `mergeSchema` option to add new columns
- **Upserts/Deletes/Merges**: `MERGE INTO` for CDC patterns
- **Audit History**: Full transaction log via `DESCRIBE HISTORY`
- **Compaction**: Small file problem solved with `OPTIMIZE`
- **Z-Ordering**: Co-locate related data for faster queries
- **Vacuum**: Remove old files beyond retention threshold

**Performance Optimizations:**
```sql
-- Optimize small files
OPTIMIZE my_table;

-- Z-order for specific columns (multi-dimensional clustering)
OPTIMIZE my_table ZORDER BY (date, customer_id);

-- Clean up old files (default 7 days retention)
VACUUM my_table RETAIN 168 HOURS;

-- Enable auto-optimization
ALTER TABLE my_table SET TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

### 4. Unity Catalog Architecture

**Three-Level Namespace:**
```
metastore
  └── catalog (e.g., sales_prod, marketing_dev)
       └── schema (e.g., bronze, silver, gold)
            └── table/view/function/volume
```

**Best Practices:**
- **Metastore**: One per cloud region (not per team)
- **Catalog**: One per environment/domain (e.g., `sales_prod`, `marketing_dev`)
- **Schema**: Organize by medallion layer or logical grouping
- **Ownership**: Always assign to groups, not individual users

**Access Control:**
```sql
-- Grant access to entire catalog
GRANT USE CATALOG, USE SCHEMA, SELECT ON CATALOG sales_prod TO `analysts_group`;

-- Grant specific table access
GRANT SELECT ON TABLE sales_prod.gold.revenue_summary TO `executives_group`;

-- Row-level security
CREATE FUNCTION filter_region(region STRING)
  RETURN IF(IS_MEMBER('us_team'), region = 'US', true);

ALTER TABLE sales_prod.gold.revenue_summary
  SET ROW FILTER filter_region ON (region);

-- Column masking
CREATE FUNCTION mask_email(email STRING)
  RETURN CASE
    WHEN IS_MEMBER('admin') THEN email
    ELSE '***@***.com'
  END;

ALTER TABLE sales_prod.silver.customers
  SET COLUMN MASK mask_email ON (email);
```

### 5. Streaming vs Batch Processing

**When to Use Streaming:**
- Sub-second to minute-level latency requirements
- Real-time dashboards or operational decisions
- Event-driven architectures
- IoT, clickstream, sensor data
- Fraud detection, anomaly detection

**When to Use Batch:**
- Hourly, daily, weekly processing cadence
- Large historical data processing
- Cost-sensitive workloads (batch is cheaper)
- Complex transformations that don't need real-time

**Hybrid Approach (Lambda Architecture):**
- Batch layer for historical accuracy
- Speed layer for real-time approximations
- Merge results for complete view
- **Note**: Databricks Lakehouse simplifies this with unified batch/streaming

**Structured Streaming Triggers:**
```python
# Continuous (micro-batch) - default
df.writeStream.trigger(processingTime="10 seconds")

# Once (triggered batch)
df.writeStream.trigger(once=True)

# Available now (process all available data, then stop)
df.writeStream.trigger(availableNow=True)

# Continuous (low-latency, experimental)
df.writeStream.trigger(continuous="1 second")
```

### 6. Data Ingestion Patterns

**Auto Loader (Recommended for Files):**
```python
df = (spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", "/path/to/schema")
  .option("cloudFiles.inferColumnTypes", "true")
  .option("cloudFiles.schemaEvolutionMode", "rescue")
  .load("/mnt/raw-data/"))
```

**Benefits:**
- Automatic file discovery
- Scalable (handles millions of files)
- Schema inference and evolution
- Exactly-once processing
- Cost-effective (event-driven, not polling)

**Partner Connect:**
- Pre-built integrations with Fivetran, Airbyte, Stitch, Segment
- Simplified setup for common data sources

**Delta Sharing:**
- Open protocol for secure data sharing
- No data copying
- Real-time updates
- Fine-grained access control
- Cross-cloud, cross-platform

### 7. Common Design Patterns

#### Pattern 1: Change Data Capture (CDC)
```sql
MERGE INTO target_table t
USING source_updates s
ON t.id = s.id
WHEN MATCHED AND s.op = 'D' THEN DELETE
WHEN MATCHED AND s.op = 'U' THEN UPDATE SET *
WHEN NOT MATCHED AND s.op = 'I' THEN INSERT *
```

#### Pattern 2: Slowly Changing Dimension (SCD Type 2)
```sql
MERGE INTO dim_customer t
USING updates s
ON t.customer_id = s.customer_id AND t.is_current = true
WHEN MATCHED AND t.customer_name != s.customer_name THEN
  UPDATE SET is_current = false, end_date = current_date()
WHEN NOT MATCHED THEN
  INSERT (customer_id, customer_name, is_current, start_date, end_date)
  VALUES (s.customer_id, s.customer_name, true, current_date(), null)
```

#### Pattern 3: Incremental Aggregation
```python
# Read stream with watermarking
df = (spark.readStream
  .format("delta")
  .table("bronze.events")
  .withWatermark("event_time", "1 hour")
  .groupBy(
    window("event_time", "5 minutes"),
    "user_id"
  )
  .agg(count("*").alias("event_count")))

# Write to gold layer
(df.writeStream
  .format("delta")
  .outputMode("complete")  # or "append" for append-only aggregations
  .option("checkpointLocation", "/checkpoints/aggregation")
  .toTable("gold.user_activity"))
```

---

## Architecture Patterns & Best Practices

### 1. Multi-Region Deployment

**Scenario**: Global organization needs low-latency access and disaster recovery

**Design Considerations:**
- **Active-Active**: Both regions serve traffic, complex data synchronization
- **Active-Passive**: Primary region serves traffic, secondary for DR
- **Data Residency**: GDPR, data sovereignty requirements

**Architecture:**
```
Region 1 (Primary - US East)
├── Unity Catalog Metastore 1
├── Databricks Workspace 1
├── Delta Tables (S3 bucket 1)
└── SQL Warehouses

Region 2 (DR/Secondary - EU West)
├── Unity Catalog Metastore 2
├── Databricks Workspace 2
├── Delta Tables (S3 bucket 2)
└── SQL Warehouses

Data Sync:
- Delta Sharing for read-only replication
- Nightly batch replication for near-real-time
- Event-driven replication for critical tables
```

**RTO/RPO Targets:**
- **RPO (Recovery Point Objective)**: How much data can we lose? (e.g., 15 minutes, 1 hour)
- **RTO (Recovery Time Objective)**: How long to recover? (e.g., 4 hours, 24 hours)

**Cost vs Resilience Trade-offs:**
- Active-Active: Highest cost, lowest RTO/RPO
- Active-Passive with warm standby: Medium cost, medium RTO/RPO
- Active-Passive with cold standby: Lowest cost, highest RTO/RPO

### 2. Cost Optimization Strategies

**Compute Optimization:**
- **Autoscaling clusters**: Scale down during low usage
- **Spot instances**: Use for fault-tolerant workloads (75% cost savings)
- **Photon engine**: 2-3x faster queries, lower TCO
- **Serverless SQL**: Pay per query, no idle time
- **Job clusters**: Terminate after job completion
- **Pool-based clusters**: Reuse VMs for faster startup

**Storage Optimization:**
- **Lifecycle policies**: Move old data to cheaper tiers (S3 Glacier, Azure Archive)
- **Compaction**: Reduce small files with `OPTIMIZE`
- **Vacuum**: Clean up old versions beyond retention
- **Compression**: Use efficient codecs (Snappy, Zstd)
- **Partitioning**: Prune unnecessary data scans

**Query Optimization:**
- **Predicate pushdown**: Filter early in query plan
- **Z-ordering**: Co-locate related data
- **Caching**: Cache frequently accessed data
- **Result caching**: Reuse query results
- **Materialized views**: Pre-compute aggregations

### 3. Security Best Practices

**Network Security:**
- **VPC/VNet peering**: Private connectivity
- **Private Link**: Avoid public internet
- **IP Access Lists**: Whitelist allowed IPs
- **VPC endpoints**: Secure S3/ADLS access

**Authentication & Authorization:**
- **SSO with SAML/OIDC**: Corporate identity integration
- **SCIM provisioning**: Automated user/group sync
- **Service principals**: For applications/CI-CD
- **Personal access tokens**: Rotate regularly, short-lived

**Data Encryption:**
- **At rest**: Customer-managed keys (CMK) via AWS KMS, Azure Key Vault
- **In transit**: TLS 1.2+ for all connections
- **Column-level encryption**: For highly sensitive data

**Compliance:**
- **Audit logging**: Track all data access via Unity Catalog
- **Data classification**: Tag PII, PHI, financial data
- **Access reviews**: Periodic certification of permissions
- **Data lineage**: Understand data flow for compliance

### 4. Monitoring & Observability

**Key Metrics to Track:**

**Cluster Metrics:**
- CPU, memory, disk utilization
- Autoscaling events
- Job failures and retries
- Shuffle read/write volumes

**Query Metrics:**
- Query duration (p50, p95, p99)
- Query failures
- Data scanned per query
- Concurrency levels

**Data Metrics:**
- Table size growth
- Number of files per table
- Schema changes
- Data freshness (staleness)

**Cost Metrics:**
- DBU consumption by workspace/cluster/user
- Storage costs
- Data transfer costs

**Alerting Strategy:**
```
Critical Alerts (PagerDuty):
- Production job failures
- Data pipeline SLA breaches
- Security incidents

Warning Alerts (Slack/Email):
- Cluster autoscaling limits reached
- High query latency
- Cost anomalies

Informational (Dashboard):
- Daily DBU usage
- Data growth trends
- Query patterns
```

---

## Technical Spike Areas

### Data Engineering Spike

#### Key Concepts:

**1. Change Data Capture (CDC)**
- **Debezium pattern**: Capture database changes via transaction logs
- **Merge pattern**: Upsert changes into Delta tables
- **SCD handling**: Type 1 (overwrite), Type 2 (versioning), Type 3 (current + previous)

**Example Scenario:**
> "We need to replicate data from 50 Oracle databases to Databricks for analytics. Changes happen continuously throughout the day. How would you design this?"

**Your Answer Should Cover:**
- Use Debezium or Oracle GoldenGate to capture CDC
- Stream to Kafka or directly to Databricks via JDBC
- Bronze layer: Raw CDC events (insert, update, delete operations)
- Silver layer: Merge CDC events to maintain current state
- Gold layer: Aggregated business metrics
- Handle out-of-order events with event-time processing
- Implement idempotency for exactly-once semantics
- Monitor lag between source and destination

**2. Data Quality & Expectations**

**Delta Live Tables Expectations:**
```python
@dlt.table
@dlt.expect_or_drop("valid_email", "email IS NOT NULL AND email LIKE '%@%'")
@dlt.expect_or_fail("valid_amount", "amount > 0")
@dlt.expect("valid_country", "country IN ('US', 'UK', 'CA')")
def clean_customers():
  return spark.read.table("bronze.raw_customers")
```

**Great Expectations Integration:**
```python
from great_expectations.dataset import SparkDFDataset

ge_df = SparkDFDataset(df)
ge_df.expect_column_values_to_not_be_null("customer_id")
ge_df.expect_column_values_to_be_between("age", 0, 120)
results = ge_df.get_expectation_suite()
```

**3. Performance Tuning**

**Common Bottlenecks:**
- **Shuffle operations**: Wide transformations (groupBy, join)
- **Small files**: Too many small files slow down reads
- **Data skew**: Uneven partition sizes
- **Spill to disk**: Memory pressure

**Optimization Techniques:**
```python
# Partition pruning
df.filter(col("date") >= "2024-01-01")  # Prune old partitions

# Broadcast join for small tables
df1.join(broadcast(df2), "key")

# Repartition to reduce shuffle
df.repartition(200, "customer_id")

# Coalesce to reduce small files
df.coalesce(10)

# Adaptive Query Execution (AQE) - enabled by default
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

**4. Handling Late Data**

**Watermarking:**
```python
df = (spark.readStream
  .format("delta")
  .table("bronze.events")
  .withWatermark("event_time", "2 hours")  # Allow 2 hours late
  .groupBy(
    window("event_time", "10 minutes"),
    "user_id"
  )
  .agg(count("*")))
```

**Trade-off:** Longer watermark = more state, more memory, but handles late data better

---

### Data Warehousing Spike

#### Key Concepts:

**1. Dimensional Modeling**

**Star Schema:**
```
Fact Table: fact_sales
├── sales_id (PK)
├── date_key (FK)
├── product_key (FK)
├── customer_key (FK)
├── store_key (FK)
├── quantity
├── revenue
└── profit

Dimension Tables:
├── dim_date (date_key, date, month, quarter, year)
├── dim_product (product_key, product_name, category, brand)
├── dim_customer (customer_key, name, segment, region)
└── dim_store (store_key, store_name, city, state)
```

**Benefits:**
- Simple queries (few joins)
- Fast aggregations
- Easy to understand for business users

**Snowflake Schema:**
- Normalized dimensions (e.g., dim_product → dim_category → dim_brand)
- Saves storage, but slower queries due to more joins
- Use when storage is a concern

**2. Aggregate Tables & Materialized Views**

```sql
-- Pre-aggregate for common queries
CREATE TABLE gold.monthly_revenue_by_region AS
SELECT
  date_trunc('month', date) as month,
  region,
  SUM(revenue) as total_revenue,
  COUNT(DISTINCT customer_id) as unique_customers
FROM fact_sales s
JOIN dim_date d ON s.date_key = d.date_key
JOIN dim_customer c ON s.customer_key = c.customer_key
GROUP BY 1, 2;

-- Refresh periodically
REFRESH TABLE gold.monthly_revenue_by_region;
```

**3. SQL Warehouse Sizing**

**Example Scenario:**
> "We have 200 analysts running ad-hoc queries during business hours (9am-5pm) and 50 automated reports running overnight. How would you size the SQL warehouses?"

**Your Answer:**
- **Two separate warehouses**: Isolate interactive vs automated workloads
  - **Interactive warehouse**:
    - Size: Large or X-Large (for concurrency)
    - Autoscaling: Yes (scale up during peak hours)
    - Auto-stop: 10 minutes idle
    - Serverless: Consider for cost optimization
  - **Batch warehouse**:
    - Size: Medium (reports are typically sequential)
    - Autoscaling: No (predictable workload)
    - Scheduled: Start at 10pm, stop at 6am
- **Query prioritization**: Use tags and query history to identify expensive queries
- **Result caching**: Enable to reduce redundant computation
- **Cost monitoring**: Set budget alerts

**4. Incremental Refresh Strategies**

**Full Refresh:**
```sql
-- Simple but expensive for large tables
CREATE OR REPLACE TABLE gold.customer_summary AS
SELECT customer_id, SUM(revenue) as total_revenue
FROM fact_sales
GROUP BY customer_id;
```

**Incremental Refresh:**
```sql
-- Only process new/updated records
MERGE INTO gold.customer_summary t
USING (
  SELECT customer_id, SUM(revenue) as revenue_delta
  FROM fact_sales
  WHERE update_date >= current_date() - INTERVAL 1 DAY
  GROUP BY customer_id
) s
ON t.customer_id = s.customer_id
WHEN MATCHED THEN UPDATE SET total_revenue = t.total_revenue + s.revenue_delta
WHEN NOT MATCHED THEN INSERT (customer_id, total_revenue) VALUES (s.customer_id, s.revenue_delta);
```

---

### AI/ML Spike

#### Key Concepts:

**1. Feature Engineering & Feature Store**

**Why Feature Store?**
- **Consistency**: Same features for training and serving
- **Reusability**: Share features across teams
- **Versioning**: Track feature definitions over time
- **Lineage**: Understand feature dependencies
- **Point-in-time correctness**: Avoid data leakage

**Example:**
```python
from databricks.feature_engineering import FeatureEngineeringClient

fe = FeatureEngineeringClient()

# Create feature table
fe.create_table(
  name="ml.features.customer_features",
  primary_keys=["customer_id"],
  timestamp_keys=["timestamp"],
  schema=customer_features_df.schema,
  description="Customer behavior features"
)

# Write features
fe.write_table(
  name="ml.features.customer_features",
  df=customer_features_df,
  mode="merge"
)

# Training: automatically joins features
training_set = fe.create_training_set(
  df=labels_df,
  feature_lookups=[
    FeatureLookup(
      table_name="ml.features.customer_features",
      lookup_key="customer_id"
    )
  ],
  label="churn",
  exclude_columns=["customer_id"]
)

# Train model
X_train, y_train = training_set.load_df().toPandas()
model = xgboost.train(...)
```

**2. MLflow Experiment Tracking**

```python
import mlflow
import mlflow.sklearn

mlflow.set_experiment("/Users/anurag/churn-prediction")

with mlflow.start_run():
  # Log parameters
  mlflow.log_param("max_depth", 5)
  mlflow.log_param("learning_rate", 0.1)

  # Train model
  model = train_model(params)

  # Log metrics
  mlflow.log_metric("accuracy", 0.92)
  mlflow.log_metric("auc", 0.87)

  # Log model
  mlflow.sklearn.log_model(model, "model")

  # Log artifacts
  mlflow.log_artifact("feature_importance.png")
```

**3. Model Deployment Patterns**

**Batch Inference:**
```python
# Load model from registry
model = mlflow.pyfunc.load_model("models:/churn_model/Production")

# Score entire table
predictions = model.predict(spark.table("gold.customers"))

# Write predictions
predictions.write.mode("overwrite").saveAsTable("gold.churn_predictions")
```

**Real-time Inference (Model Serving):**
```python
# Deploy model to serverless endpoint
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

w.serving_endpoints.create(
  name="churn-prediction-endpoint",
  config={
    "served_models": [{
      "model_name": "churn_model",
      "model_version": "3",
      "workload_size": "Small",
      "scale_to_zero_enabled": True
    }]
  }
)

# Call endpoint via REST API
import requests

response = requests.post(
  url="https://<workspace>.databricks.com/serving-endpoints/churn-prediction-endpoint/invocations",
  headers={"Authorization": f"Bearer {token}"},
  json={"dataframe_records": [{"age": 35, "tenure": 24, ...}]}
)
```

**4. Distributed Training**

**Single Node (pandas/sklearn):**
```python
# Limited by single machine memory
df_pandas = spark.table("features").toPandas()
model = sklearn.ensemble.RandomForestClassifier()
model.fit(X_train, y_train)
```

**Distributed Training (Spark ML):**
```python
from pyspark.ml.classification import RandomForestClassifier

# Distributed across cluster
rf = RandomForestClassifier(numTrees=100, maxDepth=10)
model = rf.fit(training_df)  # Spark DataFrame
```

**Distributed Training (Horovod for Deep Learning):**
```python
import horovod.spark

# Distributed TensorFlow/PyTorch training
model = horovod.spark.run(train_fn, args=..., num_proc=4)
```

**5. Generative AI & LLMs on Databricks**

**Foundation Models API:**
```python
from databricks.ai import ChatCompletion

response = ChatCompletion.create(
  model="databricks-dbrx-instruct",
  messages=[{"role": "user", "content": "Summarize this customer review: ..."}]
)
```

**RAG (Retrieval Augmented Generation):**
```python
from databricks.vector_search import VectorSearchClient

# Create vector search index
vsc = VectorSearchClient()
index = vsc.create_delta_sync_index(
  endpoint_name="vector-search-endpoint",
  index_name="product_docs_index",
  source_table_name="gold.product_documentation",
  pipeline_type="TRIGGERED",
  primary_key="doc_id",
  embedding_source_column="text",
  embedding_model_endpoint="bge-large-en"
)

# Query similar documents
results = index.similarity_search(
  query_text="How do I return a product?",
  num_results=5
)

# Pass to LLM for answer generation
context = "\n".join([r["text"] for r in results])
answer = ChatCompletion.create(
  model="databricks-dbrx-instruct",
  messages=[{
    "role": "user",
    "content": f"Answer based on this context:\n{context}\n\nQuestion: How do I return a product?"
  }]
)
```

---

## Common Interview Scenarios

### Scenario 1: Global E-commerce Data Platform

**Business Context:**
> "We're a global e-commerce company with operations in 50 countries. We generate 5TB of data daily from web clickstreams, mobile apps, order transactions, inventory systems, and customer service interactions. We need a unified platform for analytics, personalization, and fraud detection. Design an end-to-end solution."

**Key Requirements to Clarify:**
- Latency requirements for fraud detection? (Real-time vs near-real-time)
- How many analysts/data scientists? (Sizing SQL warehouses)
- Compliance requirements? (GDPR, PCI-DSS)
- Multi-region deployment? (Data residency)
- Existing BI tools? (Tableau, Power BI integration)
- Budget constraints?

**Recommended Architecture:**

```
Data Sources:
├── Web/Mobile Clickstream → Kafka/Event Hubs
├── Order Transactions → CDC from PostgreSQL/MySQL
├── Inventory → Daily batch from SAP
└── Customer Service → Salesforce API

Ingestion:
├── Kafka → Structured Streaming → Bronze (raw events)
├── Debezium CDC → Bronze (transaction log)
├── Auto Loader → Bronze (SAP files)
└── Partner Connect → Bronze (Salesforce)

Medallion Architecture:
├── Bronze: Raw data, partitioned by date and source
├── Silver:
│   ├── Deduplicated clickstream events
│   ├── Merged transactions (CDC applied)
│   ├── Joined customer-order-product datasets
│   └── Data quality checks applied
└── Gold:
    ├── Customer 360 view (for personalization)
    ├── Product analytics (for inventory optimization)
    ├── Fraud indicators (for ML model)
    └── Revenue dashboards (for executives)

Governance:
├── Unity Catalog with catalogs per region (GDPR compliance)
├── Row-level security for data residency
├── Audit logging for compliance
└── Data classification for PII

Serving:
├── Databricks SQL for BI (Tableau integration)
├── Feature Store for ML features
├── Model Serving for fraud detection (real-time scoring)
└── Delta Sharing for partner data access

ML Use Cases:
├── Fraud detection (real-time inference)
├── Product recommendations (batch scoring)
├── Churn prediction (weekly batch)
└── Demand forecasting (daily batch)
```

**Trade-offs to Discuss:**
- **Streaming vs Batch**: Fraud detection needs streaming, but analytics can be batch (cost vs latency)
- **Multi-region**: Active-passive for DR, or active-active for local latency? (cost vs performance)
- **Serverless SQL**: Better cost for variable workload, but cold start latency
- **Photon**: 2x faster queries, worth the premium for large tables

---

### Scenario 2: IoT Data Pipeline for Manufacturing

**Business Context:**
> "We operate 200 factories worldwide, each with 1,000 IoT sensors sending data every second. We need to detect anomalies in real-time, predict equipment failures, and optimize production schedules. Design the data platform."

**Key Requirements to Clarify:**
- Data volume? (200 factories × 1,000 sensors × 1 msg/sec = 200K msgs/sec = 17B msgs/day)
- Anomaly detection SLA? (Sub-second? 1 minute?)
- Equipment failure prediction frequency? (Real-time? Hourly?)
- Historical data retention? (How far back for trend analysis?)
- Alert mechanism? (Email, SMS, PagerDuty?)

**Recommended Architecture:**

```
Ingestion:
├── IoT Devices → AWS IoT Core / Azure IoT Hub
├── IoT Hub → Kafka/Kinesis/Event Hubs
└── Structured Streaming → Delta Lake

Bronze Layer:
├── Raw sensor readings (timestamp, sensor_id, value, factory_id)
├── Partitioned by factory_id and date
└── Retention: 90 days (configurable)

Silver Layer:
├── Clean sensor data (remove outliers, fill missing values)
├── Aggregate to 1-minute windows (reduce data volume)
├── Join with sensor metadata (sensor type, location, normal range)
└── Feature engineering for ML (rolling averages, std dev, rate of change)

Gold Layer:
├── Anomaly flags (real-time alerting table)
├── Equipment health scores (0-100)
├── Production efficiency metrics (OEE - Overall Equipment Effectiveness)
└── Predictive maintenance schedule

Real-time Processing:
├── Streaming aggregations with 1-minute tumbling windows
├── Stateful processing for anomaly detection (comparing to historical baseline)
├── Watermarking for late-arriving data (allow 5 minutes late)
└── Write to gold layer + trigger alerts

ML Models:
├── Anomaly Detection: Isolation Forest (batch training daily, real-time scoring)
├── Predictive Maintenance: XGBoost (weekly training, hourly scoring)
└── Production Optimization: Deep Learning (monthly training, daily scoring)

Alerting:
├── Critical anomalies → PagerDuty (immediate)
├── Predicted failures → Email to maintenance team (daily digest)
└── Dashboards → Grafana / Databricks SQL (real-time)

Cost Optimization:
├── Use Photon for fast streaming queries
├── Autoscaling clusters for variable load
├── Tiered storage: Hot (last 7 days), Warm (8-90 days), Cold (>90 days archive)
└── Spot instances for batch ML training
```

**Trade-offs to Discuss:**
- **Stream processing latency vs cost**: Sub-second requires continuous streaming (expensive), 1-minute micro-batches cheaper
- **Anomaly detection accuracy vs false positives**: Aggressive thresholds catch more issues but flood alerts
- **Storage retention**: Longer retention = better ML models but higher storage cost
- **Real-time vs batch scoring**: Real-time for critical alerts, batch for less urgent predictions

---

### Scenario 3: Healthcare Data Lake (HIPAA Compliance)

**Business Context:**
> "We're a healthcare provider with 100 hospitals. We need to consolidate patient records, medical imaging, claims data, and clinical trial data for research and operational analytics. The platform must be HIPAA compliant."

**Key Requirements to Clarify:**
- Data sources? (EHR systems, PACS, claims processors, research databases)
- User types? (Clinicians, researchers, administrators, data scientists)
- De-identification requirements? (Full de-ID, limited dataset, or identified data with BAA?)
- Access patterns? (Query latency, concurrent users)
- Audit requirements? (Track every access to patient data)

**Recommended Architecture:**

```
Data Sources:
├── EHR (Epic, Cerner) → HL7 FHIR API
├── PACS (Medical Imaging) → DICOM files
├── Claims → Batch files from clearinghouse
└── Clinical Trials → Snowflake via Delta Sharing

Ingestion (PHI Protected):
├── VPC with Private Link (no public internet)
├── Encrypted in transit (TLS 1.2+)
├── Auto Loader with customer-managed keys (CMK)
└── Bronze: Raw data with full encryption

De-identification Pipeline (Silver):
├── Scrub PII using NLP (remove names, addresses, SSN)
├── Date shifting (maintain temporal relationships)
├── Generalize ZIP codes (3-digit instead of 5-digit)
├── Replace IDs with hashed pseudonyms
└── Store de-identified data in separate catalog

Access Control (Unity Catalog):
├── Catalog: healthcare_identified (BAA required, minimal access)
├── Catalog: healthcare_deidentified (broader research access)
├── Row-level security by hospital/department
├── Column masking for sensitive fields (SSN, MRN)
└── Audit all queries via system tables

Governance:
├── Data classification tags (PHI, De-identified, Public)
├── Automatic PII detection and tagging
├── Retention policies (7 years for medical records)
├── Right to be forgotten (patient data deletion on request)
└── Audit logs stored immutably for 7 years

Serving:
├── Databricks SQL for operational dashboards (ER wait times, bed utilization)
├── Feature Store for ML (readmission risk, sepsis prediction)
├── Export to Snowflake for legacy BI tools (via Delta Sharing)
└── API for real-time clinical decision support

ML Use Cases:
├── Readmission prediction (identify high-risk patients)
├── Sepsis early warning (real-time scoring on vitals)
├── Medical imaging (tumor detection using deep learning)
└── Drug interaction alerts (NLP on prescriptions)

Security Controls:
├── Encryption at rest with BYOK (customer-managed KMS keys)
├── Network isolation (VPC peering, no public endpoints)
├── SSO with MFA required
├── Service principals for applications (rotate keys quarterly)
├── DLP (Data Loss Prevention) scanning for accidental PHI exposure
└── Penetration testing quarterly
```

**Trade-offs to Discuss:**
- **Identified vs De-identified**: De-ID enables broader access for research, but limits clinical use
- **Performance vs Security**: Encryption overhead, but non-negotiable for HIPAA
- **Centralized vs Federated**: Centralized easier to govern, but federated respects hospital autonomy
- **Cloud vs On-prem**: Cloud more scalable, but some hospitals require on-prem for compliance

---

### Scenario 4: Financial Services Real-Time Risk Analytics

**Business Context:**
> "We're an investment bank with thousands of traders executing millions of trades daily across equities, fixed income, derivatives, and crypto. We need real-time risk calculations, regulatory reporting, and fraud detection."

**Key Requirements to Clarify:**
- Trade volume? (Peak TPS - transactions per second)
- Risk calculation latency? (Sub-second? 1 second?)
- Regulatory reporting? (MiFID II, Dodd-Frank, EMIR)
- Data retention? (Regulatory requirement: 7 years minimum)
- Market data sources? (Bloomberg, Reuters, internal pricing engines)

**Recommended Architecture:**

```
Data Sources:
├── Trading Systems → Kafka (trade events)
├── Market Data → WebSocket streams (quotes, prices)
├── Reference Data → Oracle DB (instruments, counterparties)
└── External Data → Bloomberg API (corporate actions, analytics)

Ingestion:
├── Kafka Connect → Structured Streaming → Bronze
├── CDC from Oracle → Bronze (reference data changes)
├── Batch files → Auto Loader → Bronze (end-of-day positions)
└── Real-time streams (100K msgs/sec peak)

Bronze Layer:
├── Raw trades (partitioned by trade_date, asset_class)
├── Raw market data (quotes, ticks)
├── Immutable for audit trail
└── Retention: Forever (regulatory requirement)

Silver Layer:
├── Enriched trades (join with reference data)
├── Calculated fields (P&L, position, exposure)
├── Normalized market data (bid, ask, mid price)
└── SCD Type 2 for instrument master (track changes)

Gold Layer:
├── Real-time risk metrics:
│   ├── VaR (Value at Risk) - 1min windows
│   ├── Greeks (Delta, Gamma, Vega) - real-time
│   ├── Counterparty exposure - 5min windows
│   └── Concentration risk - 15min windows
├── Regulatory reports:
│   ├── MiFID II transaction reporting (< T+1)
│   ├── EMIR trade repository (real-time)
│   └── Dodd-Frank swap reporting (real-time)
└── Fraud detection:
    ├── Insider trading patterns
    ├── Market manipulation signals
    └── Unauthorized trading alerts

Real-time Processing:
├── Stateful streaming (maintain positions, cumulative P&L)
├── Sliding windows for VaR calculation (rolling 250-day)
├── Complex event processing (detect patterns)
└── Sub-second latency with Photon + real-time mode

ML Models:
├── Fraud detection (Isolation Forest, Autoencoders)
├── Trade anomaly detection (compare to historical patterns)
├── Price prediction (LSTM for time series)
└── Market regime detection (clustering)

Compliance & Governance:
├── Immutable audit log (who accessed what, when)
├── Data lineage (track every calculation)
├── Four-eyes principle (approval workflows for schema changes)
├── Separation of duties (traders can't access risk calculations)
└── Encryption with HSM for keys (hardware security module)

Disaster Recovery:
├── Active-Active multi-region (RTO < 5 minutes, RPO < 1 minute)
├── Continuous replication via Delta Sharing
├── Automated failover with health checks
└── Quarterly DR drills
```

**Trade-offs to Discuss:**
- **Latency vs Cost**: Real-time requires expensive always-on clusters, batch is cheaper
- **Accuracy vs Speed**: Complex VaR models take longer, simple approximations faster
- **Centralized vs Distributed**: Centralized risk easier to manage, distributed for performance
- **Active-Active vs Active-Passive**: Active-Active higher cost but lower RTO

---

## Preparation Strategy

### Week 1-2: Foundational Knowledge
- [ ] **Read Databricks Documentation**
  - Lakehouse architecture fundamentals
  - Delta Lake documentation
  - Unity Catalog architecture
  - Structured Streaming guide
- [ ] **Hands-on Labs**
  - Set up free Databricks Community Edition
  - Implement Medallion architecture with sample dataset
  - Practice Delta Lake operations (merge, time travel, optimize)
  - Build a simple streaming pipeline
- [ ] **Watch Databricks YouTube Videos**
  - Data + AI Summit talks (architecture deep-dives)
  - Customer case studies
  - Product demos

### Week 3: Architecture Patterns
- [ ] **Study Reference Architectures**
  - Download Databricks reference architectures (PDFs)
  - Understand industry-specific patterns (retail, finance, healthcare)
  - Map patterns to common use cases
- [ ] **Practice Whiteboarding**
  - Draw architectures from memory
  - Practice explaining trade-offs verbally
  - Time yourself (30-minute design exercises)
- [ ] **Cost Optimization Research**
  - Understand DBU pricing model
  - Learn autoscaling strategies
  - Study Photon vs standard runtime trade-offs

### Week 4: Technical Spikes
- [ ] **Deep-dive Your Chosen Area**
  - **Data Engineering**: Practice CDC, DLT, streaming
  - **Data Warehousing**: Design star schemas, query optimization
  - **AI/ML**: Feature Store, MLflow, model deployment
- [ ] **Mock Scenarios**
  - Role-play with a colleague
  - Practice asking discovery questions
  - Get comfortable with ambiguity
- [ ] **Study Real Scenarios**
  - Read Databricks customer case studies
  - Identify patterns in architecture decisions
  - Note how they justified trade-offs

### Final Week: Interview Simulation
- [ ] **Full Mock Interviews**
  - 60-minute end-to-end scenarios
  - Record yourself and review
  - Get feedback on communication style
- [ ] **Review Common Pitfalls**
  - Jumping to solutions without discovery
  - Ignoring non-functional requirements (cost, security, DR)
  - Over-engineering or under-engineering
- [ ] **Prepare Questions for Interviewer**
  - About team structure
  - About typical customer challenges
  - About Databricks product roadmap

---

## Practice Questions

### Discovery Questions (Practice Asking These)

**Business Context:**
1. "What's the primary business problem we're solving?"
2. "Who are the end users and what are their expectations?"
3. "What does success look like? How will we measure it?"
4. "What's the timeline? POC, MVP, or production-ready?"
5. "Are there any existing solutions we're replacing?"

**Data Characteristics:**
6. "What are the data sources and formats?"
7. "What's the data volume today and expected growth?"
8. "Is the data structured, semi-structured, or unstructured?"
9. "What's the data freshness requirement?"
10. "Are there data quality issues we should be aware of?"

**Non-Functional Requirements:**
11. "What are the SLAs for availability and latency?"
12. "What's the budget constraint?"
13. "Are there compliance requirements (GDPR, HIPAA, SOC2)?"
14. "What are the disaster recovery expectations (RTO/RPO)?"
15. "How many concurrent users do we expect?"

### Architecture Design Questions (Practice Answering These)

1. **"Design a data platform for a global retail company with 500 stores."**
   - Focus on: Multi-region, real-time inventory, customer analytics, fraud detection

2. **"How would you migrate 100TB of data from an on-prem Hadoop cluster to Databricks?"**
   - Focus on: Phased migration, minimal downtime, data validation, cost optimization

3. **"Design a streaming pipeline to process 1 million events per second."**
   - Focus on: Autoscaling, backpressure handling, fault tolerance, cost

4. **"How would you implement GDPR right-to-be-forgotten in a data lake?"**
   - Focus on: Data deletion, lineage tracking, cascade deletes, audit trail

5. **"Design a multi-tenant analytics platform for a SaaS company."**
   - Focus on: Data isolation, cost attribution, performance isolation, governance

### Technical Deep-Dive Questions

**Data Engineering:**
6. **"Explain how you'd implement SCD Type 2 in Delta Lake."**
7. **"How do you handle exactly-once semantics in streaming?"**
8. **"What's your approach to handling data quality issues?"**
9. **"How would you optimize a slow-running Spark job?"**
10. **"Explain the difference between foreachBatch and continuous processing."**

**Data Warehousing:**
11. **"When would you use a star schema vs a snowflake schema?"**
12. **"How do you size a SQL warehouse for 100 concurrent users?"**
13. **"Explain your strategy for incremental refresh of aggregate tables."**
14. **"How would you optimize a query that scans 10TB of data?"**
15. **"What's your approach to managing slowly changing dimensions?"**

**AI/ML:**
16. **"Explain how Feature Store solves the training-serving skew problem."**
17. **"When would you use batch inference vs real-time model serving?"**
18. **"How do you detect model drift in production?"**
19. **"Explain distributed training with Horovod vs single-node training."**
20. **"How would you implement A/B testing for ML models?"**

### Trade-off Questions (Think Aloud)

21. **"Streaming vs Batch processing - when to choose which?"**
    - Cost, latency, complexity, use case requirements

22. **"Serverless SQL vs Classic SQL warehouses?"**
    - Variable vs predictable workload, cold start latency, cost model

23. **"Multi-region active-active vs active-passive?"**
    - Cost, complexity, RTO/RPO, data consistency

24. **"Normalized vs denormalized data models?"**
    - Query performance, storage, maintenance, use case

25. **"Customer-managed keys vs Databricks-managed encryption?"**
    - Security posture, operational overhead, compliance requirements

---

## Key Talking Points

### Demonstrating First Principles Thinking

**Instead of:** "I'd use Databricks for this."
**Say:** "Let me think about the requirements. We need ACID transactions, schema enforcement, and time travel for auditing. Delta Lake provides these capabilities, which is why Databricks is a good fit. Alternatives like raw Parquet wouldn't give us ACID guarantees, and a traditional data warehouse would be more expensive and less flexible for ML workloads."

**Instead of:** "I'd build a medallion architecture."
**Say:** "The data quality requirements suggest we need multiple processing layers. Bronze for raw data immutability, Silver for cleaning and joining, and Gold for business-ready aggregates. This separation allows us to reprocess data if business logic changes, and provides clear ownership boundaries."

### Showing Trade-off Awareness

**Acknowledge limitations:**
- "This design optimizes for X, but trades off Y. If Y becomes more important, we could instead..."
- "The main risk with this approach is Z. To mitigate that, we could..."
- "This will cost approximately $X/month for Y TB of data. If budget is constrained, we could reduce costs by..."

**Discuss alternatives:**
- "I considered approach A, but chose B because..."
- "Another option would be X, which has the benefit of Y but the downside of Z."
- "If the latency requirement was relaxed to 1 hour instead of 1 minute, we could simplify to..."

### Demonstrating Operational Thinking

**Don't just design, operationalize:**
- "For monitoring, I'd track X, Y, Z metrics and alert on..."
- "The failure mode here is A, so we'd need to implement B for recovery."
- "Disaster recovery would require C, with an RTO of D hours."
- "To manage costs, I'd implement autoscaling with these parameters..."
- "For security, we'd need row-level filters on the gold tables because..."

### Consultative Communication

**Clarify ambiguity:**
- "I want to make sure I understand correctly. Are you saying that...?"
- "Help me understand the priority here. Is it more important to optimize for cost or for latency?"
- "I'm making an assumption that X. Is that correct, or should I consider Y instead?"

**Guide the conversation:**
- "Before I dive into the technical details, let me sketch the high-level architecture."
- "I think we should discuss the governance model before finalizing the data model."
- "This is a critical decision point. Let's explore both options before choosing."

---

## Resources

### Official Databricks Documentation
- [Databricks Lakehouse Architecture](https://www.databricks.com/product/data-lakehouse)
- [Introduction to the Well-Architected Data Lakehouse](https://learn.microsoft.com/en-us/azure/databricks/lakehouse-architecture/)
- [Databricks Production Planning Guide](https://docs.databricks.com/aws/en/lakehouse-architecture/deployment-guide/)
- [Delta Lake Design Patterns](https://docs.databricks.com/aws/en/lakehouse-architecture/deployment-guide/delta-lake)
- [Unity Catalog Best Practices](https://docs.databricks.com/aws/en/data-governance/unity-catalog/best-practices)
- [Data Ingestion Reference Architecture](https://www.databricks.com/resources/architectures/data-ingestion-reference-architecture)
- [Structured Streaming Concepts](https://docs.databricks.com/aws/en/structured-streaming/concepts)

### Architecture & Best Practices
- [Architecture Best Practices - Microsoft Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-databricks)
- [Data Architecture Pattern to Maximize Lakehouse Value](https://www.databricks.com/blog/data-architecture-pattern-maximize-value-lakehouse.html)
- [Delta Lake: The Definitive Guide](https://delta.io/pdfs/dldg_databricks.pdf)
- [Medallion Architecture Explained](https://www.databricks.com/glossary/medallion-architecture)

### Interview Preparation Resources
- [Databricks Solutions Architect Interview Guide 2026 - Nora AI](https://interview.norahq.com/interview-guides/databricks-solutions-architect-interview-guide-2026)
- [Databricks Interview Preparation - Official](https://www.databricks.com/company/careers/interview-prep)
- [Databricks Solutions Architect Interview Questions - Glassdoor](https://www.glassdoor.com/Interview/Databricks-Solutions-Architect-Interview-Questions-EI_IE954734.0,10_KO11,30.htm)
- [Databricks Questions - Exponent](https://www.tryexponent.com/questions?company=databricks&role=solutions-architect)
- [Data Engineering System Design Cheatsheet](https://blog.surfalytics.com/p/ultimate-cheatsheet-for-data-engineering)

### Technical Deep-Dives
- [Batch vs Streaming Processing](https://docs.databricks.com/aws/en/data-engineering/batch-vs-streaming)
- [Real-time Mode in Structured Streaming](https://docs.databricks.com/aws/en/structured-streaming/real-time)
- [Unity Catalog Implementation Guide](https://medium.com/@kanerika/databricks-unity-catalog-implementation-a-complete-guide-to-secure-and-scalable-data-governance-79ad0cb57df1)
- [Financial Services Reference Architecture](https://www.databricks.com/resources/architectures/financial-services-investment-management-reference-architecture)

### Additional Reading
- [Inside Lakehouse and Delta Lake](https://www.databricks.com/blog/2020/09/10/diving-deep-into-the-inner-workings-of-the-lakehouse-and-delta-lake.html)
- [Building the Lakehouse - 11-Part Series](https://medium.com/@infinitylearnings1201/building-the-lakehouse-a-practical-11-part-series-for-data-engineers-architects-f2483abf42ba)
- [Modern Data Architectures: Medallion, Layered, and Lakehouse](https://medium.com/@moshahriari/modern-data-architectures-medallion-layered-and-lakehouse-bb07693b0253)

### Disaster Recovery & Multi-Region
- [Databricks Disaster Recovery](https://docs.databricks.com/aws/en/admin/disaster-recovery)
- [Multi-AZ and Multi-Region Architectures Guide 2026](https://open-exam-prep.com/exams/aws-solutions-architect/design-resilient-architectures/multi-az-multi-region)
- [AWS Disaster Recovery Scenarios](https://mihirpopat.medium.com/backup-and-disaster-recovery-scenarios-in-aws-devops-interview-guide-5f509863c809)

---

## Final Tips for Interview Day

### Before the Interview
1. **Review your spike area** (Data Engineering, Data Warehousing, or AI/ML)
2. **Have a whiteboarding tool ready** (Google Slides, paper, or online tool)
3. **Prepare 2-3 questions to ask the interviewer** about the role or team
4. **Review the job description** and align your examples to the requirements
5. **Get in the right mindset**: You're a trusted advisor, not just a technologist

### During the Interview
1. **Start with discovery** - Don't jump straight to solutions
2. **Think out loud** - Narrate your thought process
3. **Draw as you talk** - Visual diagrams help communicate architecture
4. **Ask clarifying questions** - Don't make assumptions without validating
5. **Acknowledge trade-offs** - No solution is perfect
6. **Show operational thinking** - Monitoring, cost, disaster recovery, security
7. **Be consultative** - Act like you're advising a real customer
8. **Manage your time** - Discovery (10-15m), Design (25-30m), Deep-dive (15-20m)

### Common Mistakes to Avoid
1. ❌ **Jumping to solutions without understanding the problem**
2. ❌ **Ignoring non-functional requirements (cost, security, DR)**
3. ❌ **Over-engineering for the sake of complexity**
4. ❌ **Rigid thinking - not considering alternatives**
5. ❌ **Forgetting about operations - only designing the "happy path"**
6. ❌ **Not asking questions - assuming you know everything**
7. ❌ **Talking only about tools - not explaining the "why"**
8. ❌ **Not demonstrating first principles thinking**

---

## Interview Day Checklist

### 1 Day Before
- [ ] Review this prep guide (skim key sections)
- [ ] Practice 1-2 whiteboarding exercises
- [ ] Prepare questions for the interviewer
- [ ] Test your internet connection and video setup
- [ ] Get a good night's sleep

### Morning of Interview
- [ ] Review medallion architecture pattern
- [ ] Review your technical spike area (Data Eng/DW/ML)
- [ ] Skim Databricks architecture best practices
- [ ] Do a 5-minute breathing/meditation exercise
- [ ] Arrive 10 minutes early to the call

### During Interview
- [ ] Start with discovery questions
- [ ] Draw architecture diagram as you explain
- [ ] Explain trade-offs for major decisions
- [ ] Deep-dive into your technical spike area when asked
- [ ] Ask clarifying questions throughout
- [ ] Leave 5 minutes for your questions

### After Interview
- [ ] Send thank-you email within 24 hours
- [ ] Note any questions you struggled with for future prep
- [ ] Reflect on what went well and areas to improve

---

**Good luck with your interview! Remember: They want to see how you think, not just what you know. Be curious, consultative, and confident.**
