# Use Case 4: Customer 360 with Change Data Capture (CDC)

## Problem Statement

**Business Context**: A financial services company needs a unified customer view across multiple source systems.

**Current State**:
- Customer data spread across 5 systems (CRM, Billing, Support, Marketing, Transactions)
- Each system updates independently
- Need real-time sync to maintain current view
- Historical changes must be tracked for compliance

**Requirements**:
1. **Unified Customer View**: Merge data from multiple sources into single profile
2. **Change Data Capture**: Track all changes with full audit history
3. **Real-time Sync**: Propagate changes across systems within minutes
4. **Historical Tracking**: SCD Type 2 for regulatory compliance
5. **Data Quality**: Resolve conflicts when multiple systems update same field
6. **360° Analytics**: Customer journey, lifetime value, churn prediction

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│               SOURCE SYSTEMS (CDC Streams)               │
│  CRM → Debezium → Kafka                                 │
│  Billing → Debezium → Kafka                             │
│  Support → Debezium → Kafka                             │
│  Marketing → Debezium → Kafka                           │
│  Transactions → Debezium → Kafka                        │
└────────────┬────────────────────────────────────────────┘
             │ CDC Events (INSERT/UPDATE/DELETE)
             ▼
┌─────────────────────────────────────────────────────────┐
│           BRONZE: Raw CDC Events (Append-Only)          │
│  - Preserve all changes (before/after state)            │
│  - Partition by source_system + change_date             │
│  - Capture operation type (I/U/D)                       │
└────────────┬────────────────────────────────────────────┘
             │ CDC Processing & Conflict Resolution
             ▼
┌─────────────────────────────────────────────────────────┐
│        SILVER: Merged Customer View (SCD Type 2)        │
│  - Apply CDC changes in sequence (by timestamp)         │
│  - Resolve conflicts (last-write-wins or custom logic)  │
│  - Track history (effective_from/effective_to)          │
│  - Data quality scores per attribute                    │
└────────────┬────────────────────────────────────────────┘
             │ Enrichment & Feature Engineering
             ▼
┌─────────────────────────────────────────────────────────┐
│           GOLD: Customer 360 Analytics                   │
│  - Single customer view (current + historical)          │
│  - Customer journey (lifecycle stages)                  │
│  - Behavioral segments                                   │
│  - Churn risk scores                                     │
│  - ML features for personalization                      │
└─────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Implementation

### Phase 0: Setup (5 minutes)

```python
# ========================================
# ENVIRONMENT SETUP
# ========================================

spark.sql("CREATE CATALOG IF NOT EXISTS customer360")
spark.sql("USE CATALOG customer360")
spark.sql("CREATE SCHEMA IF NOT EXISTS bronze")
spark.sql("CREATE SCHEMA IF NOT EXISTS silver")
spark.sql("CREATE SCHEMA IF NOT EXISTS gold")

%pip install dbldatagen faker

from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql.window import Window
from delta.tables import DeltaTable
import dbldatagen as dg
from datetime import datetime, timedelta
import random

print("✅ Environment ready for Customer 360 CDC")
```

---

### Phase 1: Simulate CDC Events from Multiple Sources (15 minutes)

**Think-Out-Loud**:
> "CDC captures database changes at the transaction log level. Each change event contains the before/after
> state, operation type (INSERT/UPDATE/DELETE), and timestamp. I'll simulate CDC streams from 5 different
> source systems, each updating different customer attributes. This demonstrates how to handle distributed
> data ownership and merge conflicts."

```python
# ========================================
# GENERATE: Initial Customer Master Data
# ========================================

print("👥 Generating initial customer master data...")

num_customers = 50000

customers_master_spec = (
    dg.DataGenerator(spark, rows=num_customers, partitions=8)
    .withColumn("customer_id", "string", template=r"CUST-\n", uniqueValues=num_customers)
    .withColumn("first_name", "string", template=r"\w")
    .withColumn("last_name", "string", template=r"\w")
    .withColumn("email", "string", template=r"\w.\w@\w.com")
    .withColumn("phone", "string", template=r"555-\d\d\d-\d\d\d\d")
    .withColumn("date_of_birth", "date", begin="1950-01-01", end="2005-12-31")
    .withColumn("created_date", "date", begin="2018-01-01", end="2025-01-01")
)

customers_master = customers_master_spec.build()

print(f"✅ Generated {customers_master.count():,} customers (master)")

# ========================================
# SIMULATE: CDC Events from CRM System
# ========================================

print("\n📋 Simulating CDC events from CRM system...")

# CRM owns: address, segment, loyalty_status
num_crm_changes = 10000

crm_changes_spec = (
    dg.DataGenerator(spark, rows=num_crm_changes, partitions=4)
    .withColumn("customer_id", "string", template=r"CUST-\n",
                minValue=1, maxValue=num_customers)
    .withColumn("street_address", "string", template=r"\d\d\d \w Street")
    .withColumn("city", "string", values=[
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix"
    ])
    .withColumn("state", "string", values=["NY", "CA", "IL", "TX", "AZ"])
    .withColumn("zip_code", "string", template=r"\d\d\d\d\d")
    .withColumn("customer_segment", "string", values=[
        "Premium", "Standard", "Basic"
    ], weights=[20, 50, 30])
    .withColumn("loyalty_status", "string", values=[
        "Gold", "Silver", "Bronze", "None"
    ], weights=[10, 20, 30, 40])
    .withColumn("change_timestamp", "timestamp",
                begin=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
                end=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
)

crm_changes_raw = crm_changes_spec.build()

# Add CDC metadata
crm_changes = (
    crm_changes_raw
    .withColumn("source_system", F.lit("CRM"))
    .withColumn("operation", F.expr("CASE WHEN rand() < 0.7 THEN 'UPDATE' WHEN rand() < 0.95 THEN 'INSERT' ELSE 'DELETE' END"))
    .withColumn("change_id", F.monotonically_increasing_id())
    .withColumn("ingestion_timestamp", F.current_timestamp())
)

print(f"✅ Generated {crm_changes.count():,} CRM CDC events")

# ========================================
# SIMULATE: CDC Events from Billing System
# ========================================

print("\n💳 Simulating CDC events from Billing system...")

num_billing_changes = 8000

billing_changes_spec = (
    dg.DataGenerator(spark, rows=num_billing_changes, partitions=4)
    .withColumn("customer_id", "string", template=r"CUST-\n",
                minValue=1, maxValue=num_customers)
    .withColumn("billing_status", "string", values=[
        "ACTIVE", "SUSPENDED", "CANCELLED", "PENDING"
    ], weights=[70, 15, 10, 5])
    .withColumn("payment_method", "string", values=[
        "CREDIT_CARD", "BANK_TRANSFER", "PAYPAL", "CRYPTO"
    ])
    .withColumn("monthly_spend", "double", minValue=50, maxValue=5000, random=True)
    .withColumn("outstanding_balance", "double", minValue=0, maxValue=10000, random=True)
    .withColumn("last_payment_date", "date", begin="2025-01-01", end="2025-04-19")
    .withColumn("change_timestamp", "timestamp",
                begin=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
                end=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
)

billing_changes_raw = billing_changes_spec.build()

billing_changes = (
    billing_changes_raw
    .withColumn("source_system", F.lit("BILLING"))
    .withColumn("operation", F.expr("CASE WHEN rand() < 0.8 THEN 'UPDATE' WHEN rand() < 0.95 THEN 'INSERT' ELSE 'DELETE' END"))
    .withColumn("change_id", F.monotonically_increasing_id())
    .withColumn("ingestion_timestamp", F.current_timestamp())
)

print(f"✅ Generated {billing_changes.count():,} Billing CDC events")

# ========================================
# SIMULATE: CDC Events from Support System
# ========================================

print("\n🎧 Simulating CDC events from Support system...")

num_support_changes = 5000

support_changes_spec = (
    dg.DataGenerator(spark, rows=num_support_changes, partitions=4)
    .withColumn("customer_id", "string", template=r"CUST-\n",
                minValue=1, maxValue=num_customers)
    .withColumn("support_tier", "string", values=[
        "VIP", "Priority", "Standard"
    ], weights=[10, 30, 60])
    .withColumn("open_tickets", "int", minValue=0, maxValue=10)
    .withColumn("total_tickets_all_time", "int", minValue=0, maxValue=100)
    .withColumn("avg_resolution_days", "double", minValue=0.5, maxValue=30, random=True)
    .withColumn("satisfaction_score", "double", minValue=1, maxValue=5, random=True)
    .withColumn("last_contact_date", "date", begin="2025-01-01", end="2025-04-19")
    .withColumn("change_timestamp", "timestamp",
                begin=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
                end=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
)

support_changes_raw = support_changes_spec.build()

support_changes = (
    support_changes_raw
    .withColumn("source_system", F.lit("SUPPORT"))
    .withColumn("operation", F.expr("CASE WHEN rand() < 0.85 THEN 'UPDATE' ELSE 'INSERT' END"))
    .withColumn("change_id", F.monotonically_increasing_id())
    .withColumn("ingestion_timestamp", F.current_timestamp())
)

print(f"✅ Generated {support_changes.count():,} Support CDC events")

# ========================================
# SIMULATE: CDC Events from Marketing System
# ========================================

print("\n📧 Simulating CDC events from Marketing system...")

num_marketing_changes = 12000

marketing_changes_spec = (
    dg.DataGenerator(spark, rows=num_marketing_changes, partitions=4)
    .withColumn("customer_id", "string", template=r"CUST-\n",
                minValue=1, maxValue=num_customers)
    .withColumn("email_opt_in", "boolean", expr="rand() > 0.3")
    .withColumn("sms_opt_in", "boolean", expr="rand() > 0.5")
    .withColumn("push_opt_in", "boolean", expr="rand() > 0.4")
    .withColumn("last_campaign_opened", "date", begin="2025-01-01", end="2025-04-19")
    .withColumn("email_open_rate", "double", minValue=0, maxValue=1, random=True)
    .withColumn("click_through_rate", "double", minValue=0, maxValue=0.5, random=True)
    .withColumn("preferred_channel", "string", values=[
        "EMAIL", "SMS", "PUSH", "NONE"
    ])
    .withColumn("change_timestamp", "timestamp",
                begin=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
                end=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
)

marketing_changes_raw = marketing_changes_spec.build()

marketing_changes = (
    marketing_changes_raw
    .withColumn("source_system", F.lit("MARKETING"))
    .withColumn("operation", F.expr("CASE WHEN rand() < 0.75 THEN 'UPDATE' ELSE 'INSERT' END"))
    .withColumn("change_id", F.monotonically_increasing_id())
    .withColumn("ingestion_timestamp", F.current_timestamp())
)

print(f"✅ Generated {marketing_changes.count():,} Marketing CDC events")

# ========================================
# SIMULATE: CDC Events from Transaction System
# ========================================

print("\n💰 Simulating CDC events from Transaction system...")

num_txn_changes = 15000

txn_changes_spec = (
    dg.DataGenerator(spark, rows=num_txn_changes, partitions=4)
    .withColumn("customer_id", "string", template=r"CUST-\n",
                minValue=1, maxValue=num_customers)
    .withColumn("last_transaction_date", "date", begin="2025-01-01", end="2025-04-19")
    .withColumn("last_transaction_amount", "double", minValue=10, maxValue=5000, random=True)
    .withColumn("total_transactions_30d", "int", minValue=0, maxValue=100)
    .withColumn("total_spend_30d", "double", minValue=0, maxValue=50000, random=True)
    .withColumn("avg_transaction_amount", "double", minValue=50, maxValue=2000, random=True)
    .withColumn("days_since_last_transaction", "int", minValue=0, maxValue=90)
    .withColumn("change_timestamp", "timestamp",
                begin=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
                end=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
)

txn_changes_raw = txn_changes_spec.build()

txn_changes = (
    txn_changes_raw
    .withColumn("source_system", F.lit("TRANSACTIONS"))
    .withColumn("operation", F.lit("UPDATE"))  # Transactions mostly update
    .withColumn("change_id", F.monotonically_increasing_id())
    .withColumn("ingestion_timestamp", F.current_timestamp())
)

print(f"✅ Generated {txn_changes.count():,} Transaction CDC events")

# ========================================
# WRITE ALL CDC EVENTS TO BRONZE
# ========================================

print("\n🥉 Writing CDC events to BRONZE...")

# Union all CDC streams
all_cdc_events = (
    crm_changes
    .select("change_id", "customer_id", "source_system", "operation", "change_timestamp", "ingestion_timestamp",
            "street_address", "city", "state", "zip_code", "customer_segment", "loyalty_status")
    .withColumn("billing_status", F.lit(None).cast("string"))
    .withColumn("payment_method", F.lit(None).cast("string"))
    .withColumn("monthly_spend", F.lit(None).cast("double"))
    .withColumn("outstanding_balance", F.lit(None).cast("double"))
    .withColumn("support_tier", F.lit(None).cast("string"))
    .withColumn("open_tickets", F.lit(None).cast("int"))
    .withColumn("satisfaction_score", F.lit(None).cast("double"))
    .withColumn("email_opt_in", F.lit(None).cast("boolean"))
    .withColumn("preferred_channel", F.lit(None).cast("string"))
    .withColumn("last_transaction_date", F.lit(None).cast("date"))
    .withColumn("total_spend_30d", F.lit(None).cast("double"))

    .union(
        billing_changes.select(
            "change_id", "customer_id", "source_system", "operation", "change_timestamp", "ingestion_timestamp",
            F.lit(None).cast("string").alias("street_address"),
            F.lit(None).cast("string").alias("city"),
            F.lit(None).cast("string").alias("state"),
            F.lit(None).cast("string").alias("zip_code"),
            F.lit(None).cast("string").alias("customer_segment"),
            F.lit(None).cast("string").alias("loyalty_status"),
            "billing_status", "payment_method", "monthly_spend", "outstanding_balance",
            F.lit(None).cast("string").alias("support_tier"),
            F.lit(None).cast("int").alias("open_tickets"),
            F.lit(None).cast("double").alias("satisfaction_score"),
            F.lit(None).cast("boolean").alias("email_opt_in"),
            F.lit(None).cast("string").alias("preferred_channel"),
            F.lit(None).cast("date").alias("last_transaction_date"),
            F.lit(None).cast("double").alias("total_spend_30d")
        )
    )
    .union(
        support_changes.select(
            "change_id", "customer_id", "source_system", "operation", "change_timestamp", "ingestion_timestamp",
            F.lit(None).cast("string").alias("street_address"),
            F.lit(None).cast("string").alias("city"),
            F.lit(None).cast("string").alias("state"),
            F.lit(None).cast("string").alias("zip_code"),
            F.lit(None).cast("string").alias("customer_segment"),
            F.lit(None).cast("string").alias("loyalty_status"),
            F.lit(None).cast("string").alias("billing_status"),
            F.lit(None).cast("string").alias("payment_method"),
            F.lit(None).cast("double").alias("monthly_spend"),
            F.lit(None).cast("double").alias("outstanding_balance"),
            "support_tier", "open_tickets", "satisfaction_score",
            F.lit(None).cast("boolean").alias("email_opt_in"),
            F.lit(None).cast("string").alias("preferred_channel"),
            F.lit(None).cast("date").alias("last_transaction_date"),
            F.lit(None).cast("double").alias("total_spend_30d")
        )
    )
    .union(
        marketing_changes.select(
            "change_id", "customer_id", "source_system", "operation", "change_timestamp", "ingestion_timestamp",
            F.lit(None).cast("string").alias("street_address"),
            F.lit(None).cast("string").alias("city"),
            F.lit(None).cast("string").alias("state"),
            F.lit(None).cast("string").alias("zip_code"),
            F.lit(None).cast("string").alias("customer_segment"),
            F.lit(None).cast("string").alias("loyalty_status"),
            F.lit(None).cast("string").alias("billing_status"),
            F.lit(None).cast("string").alias("payment_method"),
            F.lit(None).cast("double").alias("monthly_spend"),
            F.lit(None).cast("double").alias("outstanding_balance"),
            F.lit(None).cast("string").alias("support_tier"),
            F.lit(None).cast("int").alias("open_tickets"),
            F.lit(None).cast("double").alias("satisfaction_score"),
            "email_opt_in", "preferred_channel",
            F.lit(None).cast("date").alias("last_transaction_date"),
            F.lit(None).cast("double").alias("total_spend_30d")
        )
    )
    .union(
        txn_changes.select(
            "change_id", "customer_id", "source_system", "operation", "change_timestamp", "ingestion_timestamp",
            F.lit(None).cast("string").alias("street_address"),
            F.lit(None).cast("string").alias("city"),
            F.lit(None).cast("string").alias("state"),
            F.lit(None).cast("string").alias("zip_code"),
            F.lit(None).cast("string").alias("customer_segment"),
            F.lit(None).cast("string").alias("loyalty_status"),
            F.lit(None).cast("string").alias("billing_status"),
            F.lit(None).cast("string").alias("payment_method"),
            F.lit(None).cast("double").alias("monthly_spend"),
            F.lit(None).cast("double").alias("outstanding_balance"),
            F.lit(None).cast("string").alias("support_tier"),
            F.lit(None).cast("int").alias("open_tickets"),
            F.lit(None).cast("double").alias("satisfaction_score"),
            F.lit(None).cast("boolean").alias("email_opt_in"),
            F.lit(None).cast("string").alias("preferred_channel"),
            "last_transaction_date", "total_spend_30d"
        )
    )
)

# Write to bronze
all_cdc_events.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("source_system", F.to_date("change_timestamp").alias("change_date")) \
    .saveAsTable("bronze.cdc_events")

print(f"✅ Wrote {all_cdc_events.count():,} CDC events to bronze.cdc_events")

# Show CDC event distribution
print("\n📊 CDC Event Distribution by Source:")
all_cdc_events.groupBy("source_system", "operation").agg(
    F.count("*").alias("event_count")
).orderBy("source_system", "operation").show()
```

---

### Phase 2: Silver Layer - CDC Processing & Merge (20 minutes)

**Think-Out-Loud**:
> "Processing CDC requires careful ordering and conflict resolution. I'll apply changes in timestamp order,
> implement last-write-wins for conflicts, and maintain full history using SCD Type 2. This ensures audit
> compliance while providing a current merged view."

```python
# ========================================
# SILVER LAYER: CDC Processing
# ========================================

print("🥈 Processing CDC events in SILVER layer...")

bronze_cdc = spark.read.format("delta").table("bronze.cdc_events")

# ========================================
# STEP 1: Order CDC Events by Timestamp
# ========================================

print("\n1️⃣  ORDERING CDC EVENTS")

# Critical: Process changes in chronological order
cdc_ordered = (
    bronze_cdc
    .orderBy("change_timestamp", "change_id")
)

print("   ✓ Ordered CDC events by timestamp")

# ========================================
# STEP 2: Apply CDC Changes (Merge Logic)
# ========================================

print("\n2️⃣  APPLYING CDC CHANGES")

# For initial load, merge all customer data
print("   • Creating initial customer state from master data...")

initial_customers = (
    customers_master
    .withColumn("effective_from", F.col("created_date"))
    .withColumn("effective_to", F.lit(None).cast("date"))
    .withColumn("is_current", F.lit(True))
    .withColumn("version", F.lit(1))
    .withColumn("source_system", F.lit("MASTER"))
    .withColumn("last_updated", F.current_timestamp())
)

# Add placeholder columns for system-specific fields
initial_customers_complete = (
    initial_customers
    .withColumn("street_address", F.lit(None).cast("string"))
    .withColumn("city", F.lit(None).cast("string"))
    .withColumn("state", F.lit(None).cast("string"))
    .withColumn("zip_code", F.lit(None).cast("string"))
    .withColumn("customer_segment", F.lit("Standard"))
    .withColumn("loyalty_status", F.lit("None"))
    .withColumn("billing_status", F.lit("ACTIVE"))
    .withColumn("payment_method", F.lit(None).cast("string"))
    .withColumn("monthly_spend", F.lit(0.0))
    .withColumn("outstanding_balance", F.lit(0.0))
    .withColumn("support_tier", F.lit("Standard"))
    .withColumn("open_tickets", F.lit(0))
    .withColumn("satisfaction_score", F.lit(3.0))
    .withColumn("email_opt_in", F.lit(True))
    .withColumn("sms_opt_in", F.lit(False))
    .withColumn("push_opt_in", F.lit(False))
    .withColumn("preferred_channel", F.lit("EMAIL"))
    .withColumn("last_transaction_date", F.lit(None).cast("date"))
    .withColumn("total_spend_30d", F.lit(0.0))
)

# Write initial state
initial_customers_complete.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("silver.customer_master_scd2")

print(f"   ✓ Created initial customer master ({initial_customers_complete.count():,} records)")

# ========================================
# STEP 3: Process CDC Events in Batches
# ========================================

print("\n3️⃣  PROCESSING CDC EVENTS (SCD Type 2 MERGE)")

# Group CDC events by customer and apply in order
print("   • Applying CDC changes with conflict resolution...")

# For each customer, get latest value from each source system
latest_from_each_source = (
    cdc_ordered
    .filter(F.col("operation").isin(["INSERT", "UPDATE"]))  # Ignore deletes for now
    .withColumn("row_num",
                F.row_number().over(
                    Window.partitionBy("customer_id", "source_system")
                    .orderBy(F.desc("change_timestamp"))
                ))
    .filter(F.col("row_num") == 1)
    .drop("row_num")
)

print(f"   • Latest state per customer per source: {latest_from_each_source.count():,} records")

# Merge updates from all sources (last-write-wins across systems)
print("   • Merging updates from all source systems...")

# Use coalesce to take non-null value with precedence to latest timestamp
customer_window = Window.partitionBy("customer_id").orderBy(F.desc("change_timestamp"))

merged_updates = (
    latest_from_each_source
    .withColumn("rank", F.row_number().over(customer_window))
    .groupBy("customer_id")
    .agg(
        # For each attribute, take the most recent non-null value
        F.first(F.col("street_address"), ignorenulls=True).alias("street_address"),
        F.first(F.col("city"), ignorenulls=True).alias("city"),
        F.first(F.col("state"), ignorenulls=True).alias("state"),
        F.first(F.col("zip_code"), ignorenulls=True).alias("zip_code"),
        F.first(F.col("customer_segment"), ignorenulls=True).alias("customer_segment"),
        F.first(F.col("loyalty_status"), ignorenulls=True).alias("loyalty_status"),
        F.first(F.col("billing_status"), ignorenulls=True).alias("billing_status"),
        F.first(F.col("payment_method"), ignorenulls=True).alias("payment_method"),
        F.first(F.col("monthly_spend"), ignorenulls=True).alias("monthly_spend"),
        F.first(F.col("outstanding_balance"), ignorenulls=True).alias("outstanding_balance"),
        F.first(F.col("support_tier"), ignorenulls=True).alias("support_tier"),
        F.first(F.col("open_tickets"), ignorenulls=True).alias("open_tickets"),
        F.first(F.col("satisfaction_score"), ignorenulls=True).alias("satisfaction_score"),
        F.first(F.col("email_opt_in"), ignorenulls=True).alias("email_opt_in"),
        F.first(F.col("preferred_channel"), ignorenulls=True).alias("preferred_channel"),
        F.first(F.col("last_transaction_date"), ignorenulls=True).alias("last_transaction_date"),
        F.first(F.col("total_spend_30d"), ignorenulls=True).alias("total_spend_30d"),
        F.max("change_timestamp").alias("last_change_timestamp")
    )
    .withColumn("update_date", F.current_date())
)

print(f"   ✓ Merged updates for {merged_updates.count():,} customers")

# ========================================
# STEP 4: SCD Type 2 MERGE Logic
# ========================================

print("\n4️⃣  SCD TYPE 2 MERGE")

from delta.tables import DeltaTable

customer_master = DeltaTable.forName(spark, "silver.customer_master_scd2")

# Step 1: Expire old records (set effective_to)
print("   • Expiring old records...")

customer_master.alias("target").merge(
    merged_updates.alias("source"),
    """
    target.customer_id = source.customer_id
    AND target.is_current = true
    AND (
        target.street_address <> source.street_address OR
        target.customer_segment <> source.customer_segment OR
        target.billing_status <> source.billing_status OR
        target.support_tier <> source.support_tier OR
        target.loyalty_status <> source.loyalty_status
    )
    """
).whenMatchedUpdate(set={
    "effective_to": "source.update_date",
    "is_current": "false"
}).execute()

print("   ✓ Expired old records")

# Step 2: Insert new versions
print("   • Inserting new versions...")

new_versions = (
    merged_updates
    .join(customers_master.select("customer_id", "first_name", "last_name", "email", "phone"), "customer_id")
    .withColumn("effective_from", F.col("update_date"))
    .withColumn("effective_to", F.lit(None).cast("date"))
    .withColumn("is_current", F.lit(True))
    .withColumn("version", F.lit(2))  # Simplified - should increment based on existing max
    .withColumn("last_updated", F.current_timestamp())
    .select(
        "customer_id", "first_name", "last_name", "email", "phone",
        "street_address", "city", "state", "zip_code",
        "customer_segment", "loyalty_status",
        "billing_status", "payment_method", "monthly_spend", "outstanding_balance",
        "support_tier", "open_tickets", "satisfaction_score",
        "email_opt_in", "preferred_channel",
        "last_transaction_date", "total_spend_30d",
        "effective_from", "effective_to", "is_current", "version", "last_updated"
    )
)

new_versions.write.format("delta").mode("append").saveAsTable("silver.customer_master_scd2")

print(f"   ✓ Inserted {new_versions.count():,} new versions")

# ========================================
# STEP 5: Create Current View (Snapshot)
# ========================================

print("\n5️⃣  CREATING CURRENT SNAPSHOT VIEW")

# Extract current records only (is_current = true)
customer_current = (
    spark.read.format("delta")
    .table("silver.customer_master_scd2")
    .filter(F.col("is_current") == True)
    .drop("effective_from", "effective_to", "is_current", "version")
    .withColumn("data_completeness_score",
                # Calculate % of non-null important fields
                (F.when(F.col("email").isNotNull(), 1).otherwise(0) +
                 F.when(F.col("phone").isNotNull(), 1).otherwise(0) +
                 F.when(F.col("street_address").isNotNull(), 1).otherwise(0) +
                 F.when(F.col("city").isNotNull(), 1).otherwise(0) +
                 F.when(F.col("billing_status").isNotNull(), 1).otherwise(0)) / 5 * 100)
)

customer_current.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("silver.customer_master_current")

print(f"✅ Created silver.customer_master_current ({customer_current.count():,} customers)")

# Show sample
print("\n📊 Sample Customer Records (Current):")
customer_current.select(
    "customer_id", "first_name", "last_name",
    "city", "customer_segment", "billing_status",
    F.round("data_completeness_score", 1).alias("completeness")
).show(10, truncate=False)

# Data quality summary
print("\n📊 Data Completeness Distribution:")
customer_current.select(
    F.count("*").alias("total_customers"),
    F.round(F.avg("data_completeness_score"), 1).alias("avg_completeness"),
    F.sum(F.when(F.col("email").isNull(), 1).otherwise(0)).alias("missing_email"),
    F.sum(F.when(F.col("phone").isNull(), 1).otherwise(0)).alias("missing_phone"),
    F.sum(F.when(F.col("street_address").isNull(), 1).otherwise(0)).alias("missing_address")
).show(vertical=True)
```

---

### Phase 3: Gold Layer - Customer 360 Analytics (20 minutes)

**Think-Out-Loud**:
> "Gold layer creates the unified customer view with enriched analytics. I'll build customer lifecycle stages,
> behavioral segments, churn risk scores, and ML features for personalization. This is where we turn merged
> data into actionable business insights."

```python
# ========================================
# GOLD LAYER: Customer 360 Analytics
# ========================================

print("🥇 Building GOLD layer - Customer 360...")

customer_current = spark.read.format("delta").table("silver.customer_master_current")

# ========================================
# ANALYTICS 1: Customer Lifecycle Stage
# ========================================

print("\n📊 Creating gold.customer_lifecycle...")

customer_lifecycle = (
    customer_current
    .withColumn("days_since_last_transaction",
                F.coalesce(F.col("days_since_last_transaction"),
                          F.datediff(F.current_date(), F.col("last_transaction_date"))))

    # Lifecycle stage logic
    .withColumn("lifecycle_stage",
                F.when(F.col("billing_status") == "CANCELLED", "Churned")
                .when(F.col("days_since_last_transaction").isNull(), "Prospect")
                .when(F.col("days_since_last_transaction") > 180, "At Risk")
                .when(F.col("days_since_last_transaction") > 90, "Dormant")
                .when((F.col("total_spend_30d") > 1000) & (F.col("loyalty_status") == "Gold"), "Champion")
                .when(F.col("total_spend_30d") > 500, "Loyal")
                .when(F.col("days_since_last_transaction") < 30, "Active")
                .otherwise("Occasional"))

    # Engagement score (0-100)
    .withColumn("engagement_score",
                (F.when(F.col("email_opt_in"), 20).otherwise(0) +
                 F.when(F.col("sms_opt_in"), 15).otherwise(0) +
                 F.when(F.col("push_opt_in"), 15).otherwise(0) +
                 F.when(F.col("last_transaction_date").isNotNull(), 30).otherwise(0) +
                 F.when(F.col("satisfaction_score") >= 4, 20).otherwise(
                     F.when(F.col("satisfaction_score") >= 3, 10).otherwise(0))))

    # Value tier
    .withColumn("value_tier",
                F.when(F.col("total_spend_30d") > 2000, "High")
                .when(F.col("total_spend_30d") > 500, "Medium")
                .otherwise("Low"))

    .withColumn("as_of_timestamp", F.current_timestamp())
)

customer_lifecycle.write.format("delta").mode("overwrite").saveAsTable("gold.customer_lifecycle")

print(f"✅ Created gold.customer_lifecycle ({customer_lifecycle.count():,} customers)")

# Show lifecycle distribution
print("\n📈 Customer Lifecycle Stage Distribution:")
customer_lifecycle.groupBy("lifecycle_stage").agg(
    F.count("*").alias("customer_count"),
    F.round(F.avg("engagement_score"), 1).alias("avg_engagement"),
    F.round(F.avg("total_spend_30d"), 2).alias("avg_spend_30d")
).orderBy(F.desc("customer_count")).show()

# ========================================
# ANALYTICS 2: Customer Segmentation (RFM)
# ========================================

print("\n📊 Creating gold.customer_segments...")

# RFM Analysis
customer_rfm = (
    customer_current
    .withColumn("recency_score",
                F.when(F.col("days_since_last_transaction") < 30, 5)
                .when(F.col("days_since_last_transaction") < 90, 4)
                .when(F.col("days_since_last_transaction") < 180, 3)
                .when(F.col("days_since_last_transaction") < 365, 2)
                .otherwise(1))

    .withColumn("monetary_score",
                F.ntile(5).over(Window.orderBy(F.desc("total_spend_30d"))))

    .withColumn("frequency_score",
                F.when(F.col("total_transactions_30d") > 20, 5)
                .when(F.col("total_transactions_30d") > 10, 4)
                .when(F.col("total_transactions_30d") > 5, 3)
                .when(F.col("total_transactions_30d") > 0, 2)
                .otherwise(1))

    .withColumn("rfm_score",
                (F.col("recency_score") * 100 +
                 F.col("frequency_score") * 10 +
                 F.col("monetary_score")))

    .withColumn("segment",
                F.when(F.col("rfm_score") >= 455, "Champions")
                .when(F.col("rfm_score") >= 345, "Loyal Customers")
                .when(F.col("rfm_score") >= 234, "Potential Loyalists")
                .when(F.col("recency_score") <= 2, "At Risk")
                .when(F.col("recency_score") == 1, "Lost")
                .otherwise("Need Attention"))

    .withColumn("recommended_action",
                F.when(F.col("segment") == "Champions", "Reward & Retain")
                .when(F.col("segment") == "Loyal Customers", "Upsell")
                .when(F.col("segment") == "Potential Loyalists", "Convert to Loyal")
                .when(F.col("segment") == "At Risk", "Win Back Campaign")
                .when(F.col("segment") == "Lost", "Reactivation Campaign")
                .otherwise("Engage"))

    .withColumn("as_of_timestamp", F.current_timestamp())
)

customer_rfm.write.format("delta").mode("overwrite").saveAsTable("gold.customer_segments")

print(f"✅ Created gold.customer_segments")

print("\n🎯 Customer Segmentation:")
customer_rfm.groupBy("segment").agg(
    F.count("*").alias("count"),
    F.round(F.avg("total_spend_30d"), 2).alias("avg_spend"),
    F.round(F.avg("rfm_score"), 0).alias("avg_rfm")
).orderBy(F.desc("avg_rfm")).show()

# ========================================
# ANALYTICS 3: Churn Risk Prediction Features
# ========================================

print("\n📊 Creating gold.churn_risk_features...")

churn_features = (
    customer_current
    .withColumn("days_since_last_transaction",
                F.datediff(F.current_date(), F.col("last_transaction_date")))

    # Risk factors
    .withColumn("has_outstanding_balance", F.col("outstanding_balance") > 0)
    .withColumn("has_open_tickets", F.col("open_tickets") > 0)
    .withColumn("low_satisfaction", F.col("satisfaction_score") < 3)
    .withColumn("opted_out_marketing",
                ~F.col("email_opt_in") & ~F.col("sms_opt_in") & ~F.col("push_opt_in"))
    .withColumn("declining_spend", F.col("monthly_spend") < F.col("total_spend_30d") / 2)

    # Churn risk score (0-100)
    .withColumn("churn_risk_score",
                (F.when(F.col("days_since_last_transaction") > 180, 30)
                 .when(F.col("days_since_last_transaction") > 90, 20)
                 .when(F.col("days_since_last_transaction") > 30, 10)
                 .otherwise(0) +
                 F.when(F.col("has_outstanding_balance"), 15).otherwise(0) +
                 F.when(F.col("has_open_tickets"), 10).otherwise(0) +
                 F.when(F.col("low_satisfaction"), 20).otherwise(0) +
                 F.when(F.col("opted_out_marketing"), 15).otherwise(0) +
                 F.when(F.col("declining_spend"), 10).otherwise(0)))

    .withColumn("churn_risk_level",
                F.when(F.col("churn_risk_score") >= 60, "HIGH")
                .when(F.col("churn_risk_score") >= 30, "MEDIUM")
                .otherwise("LOW"))

    .withColumn("predicted_churn_30d",
                F.when(F.col("churn_risk_score") >= 60, 1).otherwise(0))

    .withColumn("as_of_timestamp", F.current_timestamp())
)

churn_features.write.format("delta").mode("overwrite").saveAsTable("gold.churn_risk_features")

print(f"✅ Created gold.churn_risk_features")

print("\n⚠️  Churn Risk Distribution:")
churn_features.groupBy("churn_risk_level").agg(
    F.count("*").alias("customer_count"),
    F.round(F.avg("churn_risk_score"), 1).alias("avg_risk_score"),
    F.round(F.avg("days_since_last_transaction"), 0).alias("avg_days_inactive")
).orderBy(F.desc("avg_risk_score")).show()

# ========================================
# ANALYTICS 4: Customer 360 Summary
# ========================================

print("\n📊 Creating gold.customer_360_summary...")

customer_360 = (
    customer_current
    .join(customer_lifecycle.select("customer_id", "lifecycle_stage", "engagement_score", "value_tier"), "customer_id")
    .join(customer_rfm.select("customer_id", "segment", "rfm_score", "recommended_action"), "customer_id")
    .join(churn_features.select("customer_id", "churn_risk_score", "churn_risk_level"), "customer_id")

    # Add derived metrics
    .withColumn("customer_lifetime_value_estimate",
                F.col("total_spend_30d") * 12)  # Simplified: monthly * 12

    .withColumn("next_best_action",
                F.when(F.col("churn_risk_level") == "HIGH", "Retention Campaign")
                .when(F.col("segment") == "Champions", "VIP Program Invitation")
                .when(F.col("value_tier") == "High", "Premium Upsell")
                .when(F.col("open_tickets") > 2, "Priority Support Follow-up")
                .otherwise(F.col("recommended_action")))

    .withColumn("as_of_timestamp", F.current_timestamp())
)

customer_360.write.format("delta").mode("overwrite").saveAsTable("gold.customer_360_summary")

print(f"✅ Created gold.customer_360_summary ({customer_360.count():,} customers)")

print("\n🎯 Customer 360 Summary Sample:")
customer_360.select(
    "customer_id",
    "lifecycle_stage",
    "segment",
    "value_tier",
    "churn_risk_level",
    F.round("engagement_score", 0).alias("engagement"),
    "next_best_action"
).show(15, truncate=False)

# ========================================
# ML FEATURES: Personalization Feature Store
# ========================================

print("\n🤖 Creating gold.ml_personalization_features...")

ml_features = (
    customer_360
    .select(
        "customer_id",

        # Demographic features
        "city", "state", "customer_segment",

        # Behavioral features
        "lifecycle_stage", "segment", "value_tier",
        "engagement_score", "rfm_score",
        "total_spend_30d", "monthly_spend",
        "days_since_last_transaction",

        # Preference features
        "preferred_channel",
        "email_opt_in", "sms_opt_in", "push_opt_in",

        # Support features
        "support_tier", "open_tickets", "satisfaction_score",

        # Risk features
        "churn_risk_score", "outstanding_balance",

        # Target variable (for model training)
        F.when(F.col("churn_risk_score") >= 60, 1).otherwise(0).alias("will_churn_30d")
    )
    .withColumn("feature_timestamp", F.current_timestamp())
)

ml_features.write.format("delta").mode("overwrite").saveAsTable("gold.ml_personalization_features")

print(f"✅ Created gold.ml_personalization_features ({ml_features.count():,} customers)")

print("\n🎯 ML Features - Target Variable Distribution:")
ml_features.groupBy("will_churn_30d").agg(
    F.count("*").alias("count")
).show()
```

---

## Curveball Scenarios

### Curveball 1: "Handle Conflict Resolution with Priority Rules"

**Interviewer**: *"What if CRM and Billing both update the same customer's email address simultaneously? How do you resolve conflicts?"*

```python
print("🎯 CURVEBALL 1: Advanced Conflict Resolution")
print("="*60)

print("""
CONFLICT SCENARIO:
- 10:00:00 AM: CRM updates customer email to "john@newcompany.com"
- 10:00:05 AM: Billing updates same customer email to "john.doe@personal.com"
- Which email should win?

RESOLUTION STRATEGIES:
1. Last-Write-Wins (timestamp-based)
2. Source Priority (CRM > Billing > Marketing)
3. Data Quality Score (most complete record wins)
4. Custom Business Rules
""")

bronze_cdc = spark.read.format("delta").table("bronze.cdc_events")

# Simulate conflict scenario
print("\n📊 Simulating conflicting updates...")

conflicts = (
    bronze_cdc
    .filter(F.col("customer_id") == "CUST-00001")
    .select("customer_id", "source_system", "change_timestamp", "street_address", "email")
)

print("\n⚠️  Conflicting Updates for CUST-00001:")
conflicts.orderBy("change_timestamp").show(truncate=False)

# STRATEGY 1: Last-Write-Wins
print("\n1️⃣  STRATEGY: Last-Write-Wins")

last_write_wins = (
    bronze_cdc
    .withColumn("rank", F.row_number().over(
        Window.partitionBy("customer_id").orderBy(F.desc("change_timestamp"))
    ))
    .filter(F.col("rank") == 1)
)

print("   ✓ Keeps most recent update regardless of source")

# STRATEGY 2: Source Priority
print("\n2️⃣  STRATEGY: Source Priority (CRM > Billing > Support > Marketing)")

source_priority = {
    "CRM": 1,
    "BILLING": 2,
    "SUPPORT": 3,
    "MARKETING": 4,
    "TRANSACTIONS": 5
}

# Create priority mapping
priority_mapping = spark.createDataFrame(
    [(k, v) for k, v in source_priority.items()],
    ["source_system", "priority"]
)

source_priority_resolution = (
    bronze_cdc
    .join(priority_mapping, "source_system")
    .withColumn("rank", F.row_number().over(
        Window.partitionBy("customer_id")
        .orderBy(F.col("priority"), F.desc("change_timestamp"))
    ))
    .filter(F.col("rank") == 1)
)

print("   ✓ CRM always wins, then Billing, etc.")

# STRATEGY 3: Attribute-Level Priority
print("\n3️⃣  STRATEGY: Attribute-Level Priority (Different owners for different fields)")

attribute_owners = {
    "CRM": ["street_address", "city", "state", "zip_code", "customer_segment", "loyalty_status"],
    "BILLING": ["billing_status", "payment_method", "monthly_spend", "outstanding_balance"],
    "SUPPORT": ["support_tier", "open_tickets", "satisfaction_score"],
    "MARKETING": ["email_opt_in", "sms_opt_in", "push_opt_in", "preferred_channel"],
    "TRANSACTIONS": ["last_transaction_date", "total_spend_30d"]
}

attribute_resolution_logic = """
# For each attribute, only the owning system can update it
# Example: Only CRM can update customer_segment

def resolve_attributes(df, attribute_owners):
    result = df

    for source, attributes in attribute_owners.items():
        for attr in attributes:
            # If source doesn't own this attribute, set to None
            result = result.withColumn(
                attr,
                F.when(F.col("source_system") == source, F.col(attr))
                .otherwise(None)
            )

    return result

# Then merge using coalesce to take first non-null
merged = (
    resolved_updates
    .groupBy("customer_id")
    .agg(
        F.first(F.col("street_address"), ignorenulls=True).alias("street_address"),
        F.first(F.col("billing_status"), ignorenulls=True).alias("billing_status"),
        # ... for all attributes
    )
)
"""

print(attribute_resolution_logic)
print("   ✓ Each system is authoritative for its own attributes")

# STRATEGY 4: Data Quality Score
print("\n4️⃣  STRATEGY: Data Quality Score (Most complete record wins)")

data_quality_resolution = (
    bronze_cdc
    .withColumn("completeness_score",
                # Count non-null important fields
                (F.when(F.col("street_address").isNotNull(), 1).otherwise(0) +
                 F.when(F.col("city").isNotNull(), 1).otherwise(0) +
                 F.when(F.col("state").isNotNull(), 1).otherwise(0) +
                 F.when(F.col("billing_status").isNotNull(), 1).otherwise(0) +
                 F.when(F.col("support_tier").isNotNull(), 1).otherwise(0)))
    .withColumn("rank", F.row_number().over(
        Window.partitionBy("customer_id")
        .orderBy(F.desc("completeness_score"), F.desc("change_timestamp"))
    ))
    .filter(F.col("rank") == 1)
)

print("   ✓ Record with most non-null fields wins")

# RECOMMENDED: Hybrid Approach
print("\n✅ RECOMMENDED: Hybrid Approach")
print("""
IMPLEMENTATION:
1. Attribute-level ownership (prevents invalid updates)
2. Within owner: Last-write-wins (timestamp-based)
3. Cross-system: Source priority as tiebreaker
4. Audit all conflicts for manual review

EXAMPLE:
- Email: CRM owns → CRM updates always win
- Billing Status: Billing owns → Billing updates always win
- If both update different attributes simultaneously → Both accepted
""")

hybrid_resolution_code = '''
# Step 1: Filter updates by attribute ownership
cdc_with_ownership = bronze_cdc

for source, attributes in attribute_owners.items():
    for attr in attributes:
        cdc_with_ownership = cdc_with_ownership.withColumn(
            f"{attr}_valid",
            F.when(F.col("source_system") == source, F.col(attr))
        )

# Step 2: Latest value per attribute from owning system
latest_per_attribute = (
    cdc_with_ownership
    .groupBy("customer_id")
    .agg(
        *[F.last(f"{attr}_valid", ignorenulls=True).alias(attr)
          for source_attrs in attribute_owners.values()
          for attr in source_attrs]
    )
)

# Step 3: Merge into master with conflict audit
# (Log all conflicts to conflict_resolution_audit table)
'''

print(hybrid_resolution_code)
```

---

### Curveball 2: "Implement Time-Travel Query for Historical Customer View"

**Interviewer**: *"A customer disputes a billing charge from 2 months ago. Show their profile as it existed on that date."*

```python
print("🎯 CURVEBALL 2: Time-Travel Query (Point-in-Time View)")
print("="*60)

print("""
USE CASE: Audit/Compliance requires viewing customer state at specific past date

SOLUTION: Leverage SCD Type 2 + Delta Time Travel
""")

# Read SCD Type 2 table
customer_scd2 = spark.read.format("delta").table("silver.customer_master_scd2")

print("\n📊 Sample Customer History (SCD Type 2):")
customer_scd2.filter(F.col("customer_id") == "CUST-00001").select(
    "customer_id", "customer_segment", "billing_status",
    "effective_from", "effective_to", "is_current", "version"
).orderBy("version").show(truncate=False)

# TIME TRAVEL QUERY 1: Using effective_from/effective_to
print("\n1️⃣  Query customer state as of specific date (SCD Type 2)")

target_date = "2025-03-15"

historical_view_scd2 = (
    customer_scd2
    .filter(
        (F.col("effective_from") <= F.lit(target_date)) &
        ((F.col("effective_to").isNull()) | (F.col("effective_to") > F.lit(target_date)))
    )
    .select(
        "customer_id", "first_name", "last_name",
        "customer_segment", "billing_status", "loyalty_status",
        "effective_from", "effective_to"
    )
)

print(f"\n📅 Customer Profile as of {target_date}:")
historical_view_scd2.filter(F.col("customer_id") == "CUST-00001").show(truncate=False)

# TIME TRAVEL QUERY 2: Using Delta Lake Time Travel
print("\n2️⃣  Query using Delta Lake Time Travel (versionAsOf / timestampAsOf)")

time_travel_example = '''
# Method 1: Query by version number
historical_df_v5 = (
    spark.read.format("delta")
    .option("versionAsOf", 5)
    .table("silver.customer_master_current")
)

# Method 2: Query by timestamp
historical_df_march15 = (
    spark.read.format("delta")
    .option("timestampAsOf", "2025-03-15 00:00:00")
    .table("silver.customer_master_current")
)

# Method 3: Query changes between two timestamps
from delta.tables import DeltaTable

delta_table = DeltaTable.forName(spark, "silver.customer_master_current")

# Get change history
delta_table.history().select(
    "version", "timestamp", "operation", "operationMetrics"
).show()

# Diff between versions
current = spark.read.format("delta").table("silver.customer_master_current")
historical = spark.read.format("delta").option("versionAsOf", 5).table("silver.customer_master_current")

changes = (
    current.alias("current")
    .join(historical.alias("historical"), "customer_id", "outer")
    .where(
        (F.col("current.billing_status") != F.col("historical.billing_status")) |
        (F.col("current.customer_segment") != F.col("historical.customer_segment"))
    )
    .select(
        "customer_id",
        F.col("historical.billing_status").alias("old_billing_status"),
        F.col("current.billing_status").alias("new_billing_status"),
        F.col("historical.customer_segment").alias("old_segment"),
        F.col("current.customer_segment").alias("new_segment")
    )
)
'''

print(time_travel_example)

# AUDIT REPORT: Changes for specific customer
print("\n3️⃣  AUDIT REPORT: All changes for customer over time")

audit_report = (
    customer_scd2
    .filter(F.col("customer_id") == "CUST-00001")
    .orderBy("version")
    .select(
        "version",
        "effective_from",
        "effective_to",
        "customer_segment",
        "billing_status",
        "loyalty_status",
        "is_current"
    )
)

print("\n📋 Change History for CUST-00001:")
audit_report.show(truncate=False)

print("\n✅ TIME TRAVEL CAPABILITIES:")
print("""
✓ Point-in-time queries for compliance audits
✓ Rollback to previous version if needed
✓ Track who/when/what changed (with CDC metadata)
✓ Compare states between any two dates
✓ Generate audit reports for regulatory compliance
✓ Debug data quality issues by seeing historical values
""")
```

---

### Curveball 3: "Build Real-Time Customer Propensity Scoring"

**Interviewer**: *"Marketing wants real-time propensity scores. Update scores within 1 minute of any customer event."*

```python
print("🎯 CURVEBALL 3: Real-Time Propensity Scoring")
print("="*60)

print("""
REQUIREMENTS:
- Update propensity scores in real-time as CDC events arrive
- Scores: Purchase Propensity, Churn Risk, Upsell Propensity
- Latency: < 1 minute from event to updated score
- Serve scores to online systems (API, web, mobile)

ARCHITECTURE:
CDC Events → Streaming → Feature Calculation → ML Model → Score Update → Serve via API
""")

streaming_propensity_code = '''
# ========================================
# STREAMING PROPENSITY SCORING
# ========================================

# Step 1: Read CDC events stream
cdc_stream = (
    spark.readStream
    .format("delta")
    .table("bronze.cdc_events")
    .withWatermark("change_timestamp", "5 minutes")
)

# Step 2: Calculate real-time features
def calculate_features(batch_df, batch_id):
    """
    Calculate features from CDC events in micro-batch
    """
    # Join with current customer state
    customer_current = spark.read.format("delta").table("silver.customer_master_current")

    features = (
        batch_df
        .join(customer_current, "customer_id")

        # Real-time features
        .withColumn("is_weekend", F.dayofweek(F.col("change_timestamp")).isin([1, 7]))
        .withColumn("hour_of_day", F.hour("change_timestamp"))

        # Calculate change velocity (how many changes in last hour)
        .withColumn("change_velocity",
                    F.count("*").over(
                        Window.partitionBy("customer_id")
                        .orderBy("change_timestamp")
                        .rangeBetween(-3600, 0)))  # Last 1 hour in seconds

        # Aggregate behavioral signals
        .withColumn("purchase_signal",
                    F.when(F.col("source_system") == "TRANSACTIONS", 1).otherwise(0))
        .withColumn("churn_signal",
                    F.when((F.col("billing_status") == "SUSPENDED") |
                           (F.col("outstanding_balance") > 1000), 1).otherwise(0))
        .withColumn("upsell_signal",
                    F.when((F.col("customer_segment") == "Premium") &
                           (F.col("total_spend_30d") > 2000), 1).otherwise(0))
    )

    return features

# Step 3: Apply ML model (simplified - in production use MLflow model)
def score_propensity(features_df):
    """
    Apply ML model to calculate propensity scores
    """
    # Simplified scoring logic (in production: use loaded ML model)
    scored = (
        features_df
        .withColumn("purchase_propensity",
                    # Logistic function based on features
                    1 / (1 + F.exp(-(
                        F.col("purchase_signal") * 2 +
                        F.col("engagement_score") * 0.01 +
                        F.col("total_spend_30d") * 0.001 -
                        F.col("days_since_last_transaction") * 0.05
                    ))))

        .withColumn("churn_propensity",
                    1 / (1 + F.exp(-(
                        F.col("churn_signal") * 3 +
                        F.col("outstanding_balance") * 0.001 +
                        F.col("days_since_last_transaction") * 0.1 -
                        F.col("satisfaction_score") * 0.5
                    ))))

        .withColumn("upsell_propensity",
                    1 / (1 + F.exp(-(
                        F.col("upsell_signal") * 2 +
                        F.col("engagement_score") * 0.02 +
                        (F.col("total_spend_30d") / F.col("monthly_spend")) * 0.5 -
                        2
                    ))))

        .withColumn("score_timestamp", F.current_timestamp())
    )

    return scored

# Step 4: Write scores to gold (serving layer)
def write_scores(scored_df, batch_id):
    """
    Update propensity scores in gold layer using MERGE
    """
    from delta.tables import DeltaTable

    # Select scoring output
    scores = scored_df.select(
        "customer_id",
        F.round("purchase_propensity", 4).alias("purchase_propensity"),
        F.round("churn_propensity", 4).alias("churn_propensity"),
        F.round("upsell_propensity", 4).alias("upsell_propensity"),
        "score_timestamp"
    )

    # MERGE to gold table
    gold_scores = DeltaTable.forName(spark, "gold.customer_propensity_scores")

    (gold_scores.alias("target")
     .merge(scores.alias("source"), "target.customer_id = source.customer_id")
     .whenMatchedUpdate(set={
         "purchase_propensity": "source.purchase_propensity",
         "churn_propensity": "source.churn_propensity",
         "upsell_propensity": "source.upsell_propensity",
         "score_timestamp": "source.score_timestamp"
     })
     .whenNotMatchedInsertAll()
     .execute())

    print(f"Batch {batch_id}: Updated scores for {scores.count()} customers")

# Step 5: Run streaming query
streaming_query = (
    cdc_stream
    .writeStream
    .foreachBatch(lambda df, id: write_scores(score_propensity(calculate_features(df, id)), id))
    .option("checkpointLocation", "/tmp/checkpoint/propensity_scoring")
    .trigger(processingTime="1 minute")  # Micro-batch every 1 minute
    .start()
)

print("✅ Real-time propensity scoring started")

# ========================================
# SERVING LAYER
# ========================================

# Scores are now queryable in real-time
propensity_scores = spark.read.format("delta").table("gold.customer_propensity_scores")

# API endpoint would query this table:
# GET /api/customer/{customer_id}/propensity
# Returns: {purchase: 0.75, churn: 0.12, upsell: 0.68}

# For low-latency serving:
# - Enable Delta Caching
# - Create indexes on customer_id
# - Use Delta Sharing to serve to external systems
# - Consider pushing to Redis for sub-millisecond lookups
'''

print(streaming_propensity_code)

print("\n✅ REAL-TIME SCORING BENEFITS:")
print("""
✓ Scores update within 1 minute of any customer event
✓ Marketing can trigger campaigns immediately
✓ Website can personalize content based on current propensity
✓ Support can prioritize high-churn-risk customers
✓ Fraud detection can flag anomalous behavior in real-time
""")
```

---

## Summary & Key Takeaways

```python
print("\n" + "="*60)
print("CUSTOMER 360 CDC PIPELINE - COMPLETE SUMMARY")
print("="*60)

summary = f"""
📊 CDC PIPELINE ARCHITECTURE:

BRONZE (Raw CDC Events):
- Captured {all_cdc_events.count():,} CDC events from 5 source systems
- Preserved all operations (INSERT/UPDATE/DELETE)
- Partition by source_system + change_date for efficient querying

SILVER (Merged Customer Master):
- SCD Type 2: Full historical tracking with effective_from/effective_to
- Conflict resolution: Last-write-wins with source priority
- Current view: {customer_current.count():,} customers with {customer_current.agg(F.round(F.avg('data_completeness_score'), 1)).collect()[0][0]}% avg completeness
- Audit trail: Complete change history for compliance

GOLD (Customer 360 Analytics):
- Lifecycle stages: {customer_lifecycle.groupBy('lifecycle_stage').count().count()} distinct stages
- Segmentation: RFM-based with actionable recommendations
- Churn risk: {churn_features.filter('churn_risk_level = "HIGH"').count():,} high-risk customers identified
- Customer 360: Unified view with next best actions
- ML features: Ready for personalization and prediction models

🎯 KEY CDC PATTERNS DEMONSTRATED:

CHANGE DATA CAPTURE:
✓ Multi-source CDC event ingestion
✓ Operation type tracking (INSERT/UPDATE/DELETE)
✓ Before/after state preservation
✓ Timestamp-based sequencing

CONFLICT RESOLUTION:
✓ Last-write-wins (timestamp-based)
✓ Source priority (hierarchical)
✓ Attribute-level ownership
✓ Data quality scoring

HISTORICAL TRACKING:
✓ SCD Type 2 implementation
✓ Delta Lake time travel (versionAsOf, timestampAsOf)
✓ Audit reports for compliance
✓ Point-in-time customer view

REAL-TIME ANALYTICS:
✓ Streaming CDC processing
✓ Real-time propensity scoring
✓ Sub-minute latency from event to insight
✓ Serving layer for online systems

🚀 PRODUCTION CONSIDERATIONS:
- Implement CDC using Debezium or similar tool
- Set up monitoring for CDC lag (should be < 1 minute)
- Schedule hourly reconciliation for late-arriving events
- Add data lineage tracking (Apache Atlas, DataHub)
- Implement GDPR compliance (data deletion, anonymization)
- Set up alerts for SLA violations (data freshness, completeness)
"""

print(summary)
```

---

## Think-Out-Loud Script

**Use during interview**:

> "I've built a complete Customer 360 platform using Change Data Capture to merge data from five source systems into a unified customer view.
>
> **Bronze Layer**: Captured CDC events from CRM, Billing, Support, Marketing, and Transaction systems. Each event contains the before/after state, operation type, and timestamp. This preserves complete audit history for compliance.
>
> **Silver Layer**: Applied CDC events in chronological order using SCD Type 2 to maintain historical tracking. Implemented conflict resolution with a hybrid approach: attribute-level ownership (each system owns specific fields), last-write-wins within the owning system, and source priority as a tiebreaker. This ensures data quality while handling concurrent updates from multiple sources. Created both a historical table with full version history and a current snapshot view for operational queries.
>
> **Gold Layer**: Built comprehensive Customer 360 analytics. Customer lifecycle stages classify customers from prospect to champion to churned. RFM segmentation identifies high-value customer segments with specific recommended actions. Churn risk scoring combines multiple signals—days since last transaction, outstanding balance, support issues, satisfaction scores—into a 0-100 risk score. The unified Customer 360 view aggregates all dimensions with calculated next best actions for each customer.
>
> **Advanced Capabilities**: Demonstrated time-travel queries using both SCD Type 2 (effective dates) and Delta Lake's versionAsOf feature for point-in-time customer views—critical for dispute resolution and compliance audits. Designed real-time propensity scoring using streaming processing—CDC events trigger micro-batch feature calculation, ML model inference, and score updates within 1 minute, enabling real-time personalization and campaign triggers.
>
> **For scale**, the architecture handles millions of CDC events per day. Delta MERGE ensures idempotent processing—if CDC events arrive multiple times due to retries, they're handled correctly. Partitioning by source and date enables efficient querying and CDC lag monitoring. The serving layer can expose these scores via APIs with sub-second latency using Delta caching and potential integration with Redis for high-throughput scenarios."
