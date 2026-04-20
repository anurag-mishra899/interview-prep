# Databricks Vibe Coding Interview - Complete Preparation Guide

**Interview Date**: April 24, 2025
**Role**: Sr. Solutions Architect at Databricks
**Format**: 60-minute Collaborative Pair Programming Session

---

## 🚀 Quick Start: Your Path to Success

### **Day 1-2 (Today - April 20-21)**

1. **[START HERE: Read the Vibe Philosophy](./VIBE_PAIR_PROGRAMMING_GUIDE.md)** ⭐⭐⭐
   - Understand this is collaborative, not adversarial
   - Learn how to think out loud continuously
   - Master AI tool usage (you pilot, AI assists)
   - Study real interview transcripts

2. **[Study Spark Fundamentals](./Databricks_Technical_Concepts.md)**
   - Focus on: Shuffles, Join strategies, Partitioning, Window functions
   - Understand when and why performance issues occur

3. **[Practice Curveball Drills](./CURVEBALL_DRILLS.md)**
   - Scaling scenarios (10K → 100M records)
   - Data skew handling (salting techniques)
   - Architecture extensions (medallion, CDC)

### **Day 3 (April 21)**

Practice **1 complete end-to-end use case**:
- [Use Case 1: Retail PoS](./USE_CASE_1_Retail_PoS_Pipeline.md) (Batch + Streaming)
- [Use Case 2: E-Commerce Analytics](./USE_CASE_2_Ecommerce_Analytics.md) (Data Quality)

**Focus**: Execute in 60 minutes while thinking out loud continuously.

### **Day 4 (April 22)**

Practice **advanced streaming use case**:
- [Use Case 3: IoT Sensor Streaming](./USE_CASE_3_IoT_Sensor_Streaming.md) (Time-series)

**Focus**: Watermarking, windowed aggregations, anomaly detection.

### **Day 5 (April 23)**

**Full Mock Interview** with most complex use case:
- [Use Case 4: Customer 360 CDC](./USE_CASE_4_Customer_360_CDC.md)

**Focus**: CDC processing, conflict resolution, SCD Type 2, time travel.

**Evening**: Review the **[5-Day Battle Plan](./5_DAY_BATTLE_PLAN.md)** checklist.

---

## 📚 Complete File Guide

### **🎯 Essential Reading (Must Read Before Interview)**

| File | Purpose | Time to Read |
|------|---------|--------------|
| **[VIBE_PAIR_PROGRAMMING_GUIDE.md](./VIBE_PAIR_PROGRAMMING_GUIDE.md)** | **Communication & AI tool usage** | 30 min |
| [Databricks_Vibe_Interview_Prep_Guide.md](./Databricks_Vibe_Interview_Prep_Guide.md) | Overall strategy & what to expect | 20 min |
| [CURVEBALL_DRILLS.md](./CURVEBALL_DRILLS.md) | Practice rapid-fire scenarios | 30 min |

### **📖 Technical Reference (Review as Needed)**

| File | Purpose | When to Use |
|------|---------|-------------|
| [Databricks_Technical_Concepts.md](./Databricks_Technical_Concepts.md) | Spark fundamentals deep dive | Days 1-2, reference |
| [5_DAY_BATTLE_PLAN.md](./5_DAY_BATTLE_PLAN.md) | Structured day-by-day schedule | Ongoing guide |
| [USE_CASE_INDEX.md](./USE_CASE_INDEX.md) | Navigation to all use cases | Quick reference |

### **💻 Hands-On Practice (Execute in Databricks)**

| Use Case | Data Pattern | Complexity | Time Required |
|----------|--------------|------------|---------------|
| [Use Case 1: Retail PoS](./USE_CASE_1_Retail_PoS_Pipeline.md) | Batch + Streaming | ⭐⭐⭐⭐ | 60-90 min |
| [Use Case 2: E-Commerce](./USE_CASE_2_Ecommerce_Analytics.md) | Data Quality | ⭐⭐⭐⭐⭐ | 75-90 min |
| [Use Case 3: IoT Sensors](./USE_CASE_3_IoT_Sensor_Streaming.md) | Time-Series Streaming | ⭐⭐⭐⭐⭐ | 75-90 min |
| [Use Case 4: Customer 360 CDC](./USE_CASE_4_Customer_360_CDC.md) | Change Data Capture | ⭐⭐⭐⭐⭐ | 90 min |

---

## 🎯 The "Vibe" Philosophy - What This Interview Really Tests

### **What They're Looking For** ✅

1. **Computational Thinking** (40% weight)
   - Can you break messy problems into logical steps?
   - Do you understand distributed data processing?
   - Can you reason about data flows and transformations?

2. **Code Stewardship** (40% weight)
   - Can you audit AI-generated code?
   - Do you understand code "under the hood"?
   - Can you explain technical choices to customers?

3. **Resilience** (20% weight)
   - How do you handle bugs and blockers?
   - Do you stay methodical under pressure?
   - Can you ask for help appropriately?

### **What They're NOT Testing** ❌

- ❌ Syntax memorization
- ❌ Speed of typing
- ❌ Perfect code on first try
- ❌ Encyclopedic API knowledge

**The golden rule**: **Think out loud continuously.** Silent coding = red flag.

---

## 🗣️ Communication Framework: DEWA

Use this structure to think out loud naturally:

- **D - Describe** what you're about to do
  - "I'm going to generate customer data using dbldatagen..."

- **E - Explain** why you're doing it this way
  - "I'm using log-normal distribution because real spending follows that pattern..."

- **W - Walk through** your code as you write/review it
  - "This join will be broadcast because the table is small..."

- **A - Assess** what you just did
  - "Let me validate... running count() shows 100K records as expected..."

**Practice this until it feels natural!**

---

## 🤖 AI Tool Usage Strategy

### **The Golden Rule**: You Pilot, AI Assists

**DO** ✅:
- Use AI to scaffold code and generate boilerplate
- Draft prompts in a scratchpad before pasting
- Review ALL AI output out loud before running
- Identify and correct AI hallucinations
- Explain why you're changing AI-generated code

**DON'T** ❌:
- Blindly copy-paste AI code without reading
- Let AI make architectural decisions
- Run code you don't understand
- Stay silent while AI generates code

### **Common AI Pitfalls to Catch**

1. **Using `collect()` on large DataFrames** → Use distributed operations
2. **Unnecessary shuffles** → Combine groupBys when possible
3. **Missing broadcast joins** → Broadcast small tables (<10GB)
4. **Uniform distributions** → Use realistic distributions (log-normal, etc.)

**When you catch these, narrate your fix!**

---

## 📊 Pre-Interview Checklist

### **Environment Setup** (Do 1 day before)

- [ ] Databricks Free Edition account created and working
- [ ] Can start a cluster (takes 2-3 minutes)
- [ ] Installed `dbldatagen` and `faker` packages
- [ ] Tested Databricks Assistant
- [ ] Practiced screen sharing

### **Technical Knowledge** (Can you do these?)

- [ ] Explain medallion architecture in 30 seconds
- [ ] Write a streaming query with watermark from memory
- [ ] Explain when shuffles occur (5 triggers)
- [ ] Code salting for data skew in 2 minutes
- [ ] Explain broadcast vs sort-merge join
- [ ] Write a Delta MERGE statement
- [ ] Explain SCD Type 2 logic
- [ ] Calculate optimal partition count (formula)
- [ ] Use `.explain()` to analyze query plans

### **Communication Skills** (Most Important!)

- [ ] Can think out loud for 60 minutes without awkward silences
- [ ] Can explain WHY (not just WHAT) for each decision
- [ ] Can audit AI code and identify issues
- [ ] Can read error messages and diagnose root causes
- [ ] Know when to use "Bail Out" (>2 min on syntax)
- [ ] Can explain code to a "customer" without jargon

### **Recorded Practice** (Highly Recommended)

- [ ] Recorded yourself completing 1 full use case
- [ ] Reviewed recording for silent periods (red flag!)
- [ ] Counted how many times you explained trade-offs
- [ ] Verified you validated intermediate results

---

## 🎬 Interview Day: Your Game Plan

### **30 Minutes Before**

1. Start your Databricks cluster (takes 2-3 minutes)
2. Create workspace catalog: `CREATE CATALOG vibe_interview`
3. Install packages: `%pip install dbldatagen faker`
4. Test Databricks Assistant with simple query
5. Have docs open in tabs (PySpark functions, Delta Lake)
6. Close all other apps, turn off notifications
7. Deep breath - you've got this!

### **Phase 1: Discovery (5-10 min)**

**Interviewer gives scenario**: "Analyze customer transaction patterns..."

**Your Actions**:
1. **Ask 5W1H questions**: What volume? What metrics? What output? What time range?
2. **Restate the problem**: "So we're building a pipeline that..."
3. **Create a spec** in a Markdown cell before coding
4. **Get alignment**: "Does this approach make sense?"

### **Phase 2: Building (30-40 min)**

**For each step**:
1. **Think** (explain WHAT and WHY)
2. **Code** (narrate as you write)
3. **Validate** (check your work: `.count()`, `.show()`, `.describe()`)

**When using AI**:
1. Draft prompt in scratchpad
2. Submit to AI
3. Review output OUT LOUD
4. Identify issues and fix them
5. Explain your changes

**When hitting errors**:
1. Read error message OUT LOUD
2. Hypothesize cause
3. Verify with `.printSchema()` or similar
4. Fix and explain what you learned

### **Phase 3: Curveballs (10-15 min)**

**Expected**: "Scale this to 100M records" / "Handle data skew" / "Add CDC"

**Your Response**:
1. Pause and analyze (15 seconds of silence is OK!)
2. "Here's how I'd approach this..."
3. Explain strategy before coding
4. Implement with narration
5. Show query plan with `.explain()`

### **Wrap-Up (Last 5 min)**

- Summarize what you built
- Explain end-to-end data flow
- Mention scalability considerations
- Ask if they want to see anything else

---

## 💡 Key Concepts Quick Reference

### **When Shuffles Occur**
- `groupBy()`, `agg()`, `reduceByKey()`
- `join()` (except broadcast)
- `distinct()`, `dropDuplicates()`
- `orderBy()`, `sortBy()`
- `repartition()` (but not `coalesce()`)

### **Join Strategy Decision Tree**
```
Is one table < 10GB?
  Yes → Broadcast Join
  No → Are both pre-partitioned by join key?
    Yes → Sort-Merge (no repartition)
    No → Repartition both + Sort-Merge
```

### **Partition Count Formula**
```
partitions = data_size_GB / 0.5
Ensure: 2-4 partitions per CPU core
```

### **Data Skew Solutions**
1. **Salting**: Add random salt, partial aggregate, re-aggregate
2. **Broadcast**: If skewed table has small join partner
3. **Isolate hot keys**: Process separately
4. **Increase partitions**: Quick fix (not ideal)

---

## 🎯 Success Criteria

**You're ready when you can**:

1. ✅ Complete any use case in 60 minutes with continuous narration
2. ✅ Explain architectural decisions (why medallion, why broadcast, etc.)
3. ✅ Audit AI code and catch common issues (collect, shuffles, broadcasts)
4. ✅ Read query plans and identify optimization opportunities
5. ✅ Handle errors methodically (read, diagnose, fix, explain)
6. ✅ Scale solutions (10K → 100M) with specific optimizations

**If you can do all of these, you're ready!**

---

## 📞 Need Help? Use "Bail Out"

**When stuck >2 minutes on**:
- Syntax or imports
- Environment issues
- Trivial errors blocking progress

**How to ask**:
> "I've been stuck on this syntax for a couple minutes. Can we 'bail out' and move forward? I want to focus on architecture rather than commas."

**Why this is GOOD**: Shows you prioritize problem-solving over perfection.

---

## 💪 Your Interview Day Mantra

> **"I am the architect. AI is my assistant. My interviewer is my teammate.**
> **I think out loud. I explain my reasoning. I validate my work.**
> **I stay calm when stuck. I ask for help when needed.**
> **I focus on architecture, not syntax."**

---

## 🎉 Final Words

**Remember**:
- This is a **conversation**, not an exam
- Your interviewer **wants you to succeed**
- They're evaluating **how you think**, not what you've memorized
- **Thinking out loud** is more important than perfect code
- **AI is your tool**, but you're the expert
- **Asking questions** shows engagement, not weakness

**You're prepared. You've practiced. You've got this.** 🚀

---

## 📚 Official Resources

**Databricks Documentation**:
- [PySpark SQL Functions](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html)
- [Delta Lake Guide](https://docs.databricks.com/delta/index.html)
- [Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [dbldatagen Library](https://github.com/databrickslabs/dbldatagen)

**Databricks Free Edition**:
- [Sign Up](https://www.databricks.com/try-databricks)
- [Documentation](https://docs.databricks.com/)

---

**Good luck on April 24th!** 🎯

Remember: They're evaluating **how you work with customers**, not just your coding skills. Show them you'd be a great teammate, and you'll do great.

---

**Last Updated**: April 20, 2025
**Created for**: Databricks Sr. Solutions Architect - Vibe Coding Interview
