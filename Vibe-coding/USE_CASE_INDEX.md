# Databricks Vibe Coding Interview - Use Case Index

## Overview

This collection contains **4 comprehensive end-to-end use cases** designed for Databricks interview preparation. Each use case demonstrates different data patterns, architectural approaches, and optimization techniques.

---

## 📚 Use Case Catalog

### **[Use Case 1: Retail PoS Data Platform](./USE_CASE_1_Retail_PoS_Pipeline.md)** 🏪
**Data Pattern**: Batch + Streaming (Hybrid)
**Complexity**: ⭐⭐⭐⭐
**Key Topics**: Near real-time ingestion, Medallion architecture, Streaming + Batch reconciliation

**What You'll Build**:
- Ingest sales data from 500 stores
- Bronze → Silver → Gold medallion architecture
- Streaming ingestion with watermarking
- Daily/hourly batch processing
- Real-time inventory tracking

**Curveballs Covered**:
✓ Scaling from 10K to 100M transactions
✓ Handling data skew with salting
✓ Real-time streaming with late data

**Best For**: Understanding streaming + batch hybrid architecture, production-scale optimization

---

### **[Use Case 2: E-Commerce Transaction Analytics](./USE_CASE_2_Ecommerce_Analytics.md)** 🛒
**Data Pattern**: Batch Processing with Data Quality
**Complexity**: ⭐⭐⭐⭐⭐
**Key Topics**: Data quality framework, Quarantine pattern, ML feature engineering, SCD Type 2

**What You'll Build**:
- Multi-source data ingestion (orders, customers, products, clickstream)
- Comprehensive data quality validation
- Quarantine invalid records (don't drop!)
- Cart abandonment analysis
- Anomaly detection (fraud/data issues)
- ML feature store for recommendations

**Curveballs Covered**:
✓ Implementing SCD Type 2 for dimensions
✓ Cart abandonment rate calculation
✓ Multi-method anomaly detection

**Best For**: Data quality best practices, complex business logic, ML feature engineering

---

### **[Use Case 3: IoT Sensor Data Processing](./USE_CASE_3_IoT_Sensor_Streaming.md)** 📡
**Data Pattern**: Time-Series Streaming
**Complexity**: ⭐⭐⭐⭐⭐
**Key Topics**: Structured Streaming, Watermarking, Window functions, Anomaly detection, Time-series

**What You'll Build**:
- Real-time sensor data ingestion (10K sensors, 3.6M events/hour)
- Streaming with watermarks (5-minute tolerance)
- Tumbling windows (1-min, 5-min aggregations)
- Moving averages and statistical anomaly detection
- Equipment health scoring
- Sensor outage sessionization

**Curveballs Covered**:
✓ Handling out-of-order/late-arriving events
✓ Composite health scoring system
✓ Outage detection with sessionization

**Best For**: Streaming mastery, time-series analysis, real-time alerting

---

### **[Use Case 4: Customer 360 with CDC](./USE_CASE_4_Customer_360_CDC.md)** 👥
**Data Pattern**: Change Data Capture (CDC)
**Complexity**: ⭐⭐⭐⭐⭐
**Key Topics**: CDC processing, Conflict resolution, SCD Type 2, Delta Lake MERGE, Time travel

**What You'll Build**:
- Merge data from 5 source systems (CRM, Billing, Support, Marketing, Transactions)
- Process CDC events (INSERT/UPDATE/DELETE)
- Conflict resolution strategies
- SCD Type 2 for historical tracking
- Customer lifecycle stages
- RFM segmentation
- Churn risk prediction
- Real-time propensity scoring

**Curveballs Covered**:
✓ Multi-strategy conflict resolution
✓ Time-travel queries for audits
✓ Real-time propensity scoring

**Best For**: CDC expertise, customer analytics, regulatory compliance, real-time ML scoring

---

## 🎯 How to Use This Guide

### **For Day-by-Day Prep (5-Day Battle Plan)**

Follow the **[5_DAY_BATTLE_PLAN.md](./5_DAY_BATTLE_PLAN.md)** schedule:

- **Days 1-2**: Study **[Databricks_Technical_Concepts.md](./Databricks_Technical_Concepts.md)** + **[CURVEBALL_DRILLS.md](./CURVEBALL_DRILLS.md)**
- **Day 3**: Practice **Use Case 1 or 2** (batch-heavy)
- **Day 4**: Practice **Use Case 3** (streaming-heavy) + curveball drills
- **Day 5**: Full mock interview with **Use Case 4** (most complex)

### **For Targeted Practice**

| **If You Want to Practice...** | **Use This Use Case** |
|--------------------------------|-----------------------|
| Streaming with watermarks | Use Case 1, 3 |
| Data quality & validation | Use Case 2 |
| Time-series analysis | Use Case 3 |
| CDC & SCD Type 2 | Use Case 4 |
| Performance optimization (salting, broadcast) | Use Case 1, 2 |
| ML feature engineering | Use Case 2, 4 |
| Window functions | Use Case 2, 3 |
| Delta MERGE operations | Use Case 1, 4 |

### **Interview Day Strategy**

1. **Pick the use case that matches the interviewer's scenario**
   - Retail/IoT → Use Case 1 or 3
   - E-commerce/Marketing → Use Case 2 or 4
   - Financial Services/CDC → Use Case 4

2. **Follow the structure**:
   - Phase 1: Generate data (10 mins)
   - Phase 2: Bronze ingestion (5 mins)
   - Phase 3: Silver transformation (15 mins)
   - Phase 4: Gold analytics (15 mins)
   - Curveballs: As they come (10-15 mins)

3. **Think out loud continuously** using provided scripts

---

## 📊 Complexity Matrix

| Use Case | Batch | Streaming | Data Quality | ML Features | CDC | Difficulty |
|----------|-------|-----------|--------------|-------------|-----|------------|
| **1. Retail PoS** | ✅ | ✅ | ⭐⭐ | ⭐⭐ | ❌ | Medium-High |
| **2. E-Commerce** | ✅ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | High |
| **3. IoT Sensors** | ✅ | ✅✅✅ | ⭐⭐⭐ | ⭐⭐ | ❌ | Very High |
| **4. Customer 360** | ✅ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ✅✅✅ | Very High |

**Legend**:
- ✅✅✅ = Primary focus
- ✅✅ = Secondary focus
- ✅ = Basic coverage
- ⭐ = Complexity level (1-5)

---

## 🎓 Key Concepts Coverage

### **Spark Fundamentals**
- ✅ Narrow vs Wide transformations (all use cases)
- ✅ Shuffle optimization (Use Case 1, 2)
- ✅ Join strategies (broadcast, sort-merge) (Use Case 1, 2, 3)
- ✅ Partitioning strategies (all use cases)
- ✅ Query plan analysis with `.explain()` (all curveballs)

### **Streaming**
- ✅ Structured Streaming basics (Use Case 1, 3)
- ✅ Watermarking for late data (Use Case 1, 3)
- ✅ Micro-batching (Use Case 1, 3, 4)
- ✅ foreachBatch for complex logic (Use Case 3, 4)
- ✅ Windowed aggregations (Use Case 1, 3)

### **Delta Lake**
- ✅ ACID transactions (all use cases)
- ✅ MERGE operations (Use Case 1, 4)
- ✅ Time travel (Use Case 4)
- ✅ OPTIMIZE & VACUUM (Use Case 1)
- ✅ Schema evolution (Use Case 1, 2)

### **Data Quality**
- ✅ Validation frameworks (Use Case 2)
- ✅ Quarantine patterns (Use Case 2)
- ✅ Data quality scoring (Use Case 2, 4)
- ✅ Conflict resolution (Use Case 4)

### **Advanced Patterns**
- ✅ Medallion architecture (all use cases)
- ✅ SCD Type 2 (Use Case 2, 4)
- ✅ Data skew handling (salting) (Use Case 1, 2)
- ✅ CDC processing (Use Case 4)
- ✅ Anomaly detection (Use Case 2, 3)
- ✅ Sessionization (Use Case 2, 3)

---

## 💡 Interview Tips by Use Case

### **Use Case 1: Retail PoS**
**When to Pick**: Interviewer mentions "real-time", "stores", "transactions", "inventory"

**Key Points to Emphasize**:
- "I'll implement medallion architecture with both streaming and batch paths"
- "For 100M transactions, I'd increase shuffle partitions to 400 and use broadcast joins for dimensions"
- "Streaming provides 2-3 minute latency; batch reconciles daily for correctness"

**Common Mistakes to Avoid**:
- ❌ Using collect() on large DataFrames
- ❌ Not explaining watermark strategy
- ❌ Forgetting to broadcast small dimensions

---

### **Use Case 2: E-Commerce**
**When to Pick**: Interviewer mentions "data quality", "customers", "orders", "analytics"

**Key Points to Emphasize**:
- "I'll implement a comprehensive data quality framework with quarantine"
- "SCD Type 2 tracks historical customer changes for compliance"
- "Cart abandonment uses session window analysis with 24-hour conversion window"

**Common Mistakes to Avoid**:
- ❌ Silently dropping bad data without quarantine
- ❌ Not explaining SCD Type 2 logic clearly
- ❌ Missing anomaly detection multi-method approach

---

### **Use Case 3: IoT Sensors**
**When to Pick**: Interviewer mentions "sensors", "time-series", "real-time monitoring", "anomalies"

**Key Points to Emphasize**:
- "Watermark set to 5 minutes balances latency vs completeness"
- "Moving averages with window functions smooth noise for anomaly detection"
- "Outage sessionization identifies gaps larger than threshold"

**Common Mistakes to Avoid**:
- ❌ Not handling late-arriving data properly
- ❌ Forgetting to explain tumbling vs sliding windows
- ❌ Not discussing batch reconciliation for late data

---

### **Use Case 4: Customer 360**
**When to Pick**: Interviewer mentions "CDC", "customer", "merge", "compliance", "audit"

**Key Points to Emphasize**:
- "CDC events processed in chronological order with conflict resolution"
- "SCD Type 2 maintains full audit trail with effective_from/effective_to"
- "Attribute-level ownership prevents invalid cross-system updates"
- "Delta time travel enables point-in-time queries for disputes"

**Common Mistakes to Avoid**:
- ❌ Not explaining conflict resolution strategy
- ❌ Implementing SCD Type 2 incorrectly (missing effective_to logic)
- ❌ Not discussing time-travel for audits

---

## 🚀 Pre-Interview Checklist

Before your interview, ensure you can:

- [ ] Explain medallion architecture in 30 seconds
- [ ] Write a simple streaming query with watermark from memory
- [ ] Explain when shuffles occur (groupBy, join, distinct, orderBy, repartition)
- [ ] Code salting for data skew in 2 minutes
- [ ] Explain broadcast vs sort-merge join in 30 seconds
- [ ] Write a Delta MERGE statement from memory
- [ ] Explain SCD Type 2 logic clearly
- [ ] Calculate optimal partition count (formula: data_size_GB / 0.5)
- [ ] Use `.explain()` to analyze query plans
- [ ] Think out loud naturally (practice recording yourself!)

---

## 📚 Quick Reference Links

### **Core Prep Materials**
- [Main Interview Guide](./Databricks_Vibe_Interview_Prep_Guide.md) - Overall strategy
- [Technical Concepts](./Databricks_Technical_Concepts.md) - Spark fundamentals
- [Curveball Drills](./CURVEBALL_DRILLS.md) - Practice rapid-fire scenarios
- [5-Day Battle Plan](./5_DAY_BATTLE_PLAN.md) - Structured study schedule

### **Official Databricks Docs** (Bookmark These!)
- [PySpark SQL Functions](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html)
- [Delta Lake Guide](https://docs.databricks.com/delta/index.html)
- [Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Databricks Data Generator (dbldatagen)](https://github.com/databrickslabs/dbldatagen)

---

## 🎯 Success Criteria

You're ready when you can:

1. **Complete any use case in 60 minutes** (including curveballs)
2. **Think out loud continuously** without awkward silences
3. **Explain your reasoning** ("This triggers a shuffle because...")
4. **Handle curveballs confidently** (scaling, skew, conflicts)
5. **Read query plans** using `.explain()` and identify optimizations
6. **Code common patterns from memory** (MERGE, SCD Type 2, windowing)

---

## 💪 Your Interview Day Mantra

> *"I am the architect. I explain my reasoning. I validate my work. I handle curveballs with confidence."*

**Remember**:
- ✅ Thinking out loud > Perfect syntax
- ✅ Explaining trade-offs > Fastest solution
- ✅ Validating results > Assuming correctness
- ✅ Asking questions > Making assumptions
- ✅ AI as assistant > AI doing all work

---

## 🎉 Final Note

These use cases are **comprehensive learning tools**, not scripts to memorize. The goal is to:
- Understand **patterns** (medallion, CDC, streaming)
- Build **intuition** (when to broadcast, when to salt, how to partition)
- Develop **communication** (thinking out loud, explaining decisions)

**You've got this!** 🚀

Good luck with your interview! Remember: they want to see **how you think**, not just what you code.

---

**Last Updated**: April 2025
**For**: Databricks Sr. Solutions Architect - Vibe Coding Interview
