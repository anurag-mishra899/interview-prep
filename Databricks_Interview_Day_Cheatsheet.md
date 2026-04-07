# Databricks SA Interview - Day-Of Cheatsheet
**Quick Reference Guide - Read This Morning of Interview**

---

## 🎯 Interview Structure (60 minutes)

1. **Discovery & Problem Framing** (10-15 min) - ASK QUESTIONS FIRST
2. **Core Architecture Design** (25-30 min) - THINK OUT LOUD, DRAW
3. **Technical Deep-Dive** (15-20 min) - FOCUS ON AI/ML SPIKE

---

## ❓ Essential Discovery Questions

**Business:**
- What's the primary business objective?
- Who are the end users and their expectations?
- What's the timeline (POC, MVP, production)?

**Data:**
- What are data sources and volume (GB/TB/PB per day)?
- Structured, semi-structured, or unstructured?
- Data freshness requirements (real-time, hourly, daily)?

**Non-Functional:**
- Latency SLA? (sub-second, seconds, minutes?)
- Throughput requirements? (QPS/TPS?)
- Budget constraints?
- Compliance (GDPR, HIPAA, SOC2)?
- Disaster recovery (RTO/RPO)?

---

## 🏗️ ML System Design Framework (30 seconds)

1. **Clarify** → Ask questions (5-7 min)
2. **Define** → Frame ML problem (3-5 min)
3. **Data** → Feature pipeline (5-7 min)
4. **Train** → Model architecture (7-10 min)
5. **Serve** → Inference system (7-10 min)
6. **Monitor** → Feedback loop (5-7 min)

---

## 🎨 Architecture Components Checklist

**Data Layer:**
- [ ] Bronze (raw) → Silver (cleaned) → Gold (aggregated)
- [ ] Delta Lake for storage (ACID, time travel)
- [ ] Unity Catalog for governance

**Feature Engineering:**
- [ ] Feature Store (online + offline)
- [ ] Batch features (daily) vs Real-time (streaming)
- [ ] Point-in-time correctness

**Model Training:**
- [ ] MLflow for experiment tracking
- [ ] Model Registry for versioning
- [ ] Distributed training (if needed)
- [ ] Hyperparameter tuning (Hyperopt)

**Model Serving:**
- [ ] Serverless vs Provisioned endpoints
- [ ] Feature retrieval (online store)
- [ ] Caching strategy
- [ ] A/B testing (10% new, 90% baseline)

**Monitoring:**
- [ ] Data drift (feature distributions)
- [ ] Model drift (prediction distributions)
- [ ] Performance (latency, throughput)
- [ ] Business metrics (CTR, revenue)

---

## 🔥 2026 Focus: GenAI is CRITICAL

**RAG Architecture (Know This Cold):**
```
Documents → Chunking → Embedding → Vector DB →
User Query → Embed → Retrieve Top-K → Augment Context →
LLM Generate → Evaluate (Faithfulness, Groundedness, Relevance)
```

**Key Components:**
- **Vector Search**: Databricks Vector Search (Delta Sync index)
- **Embeddings**: bge-large-en, e5-mistral (on Model Serving)
- **LLM**: DBRX, Llama 3, GPT-4 (via Foundation Model API)
- **Evaluation**: LLM-as-judge, faithfulness, groundedness, citation accuracy

**Agent Patterns:**
1. **Deterministic Chains**: Predictable tool calling (low latency, auditable)
2. **Agentic Systems**: LLM decides which tools (flexible, autonomous)
3. **Hybrid**: Combine both (best of both worlds)

---

## 💡 Key Talking Points (Memorize These)

### Why Databricks?
"Databricks provides a unified lakehouse where data and ML coexist, eliminating data silos. Unlike SageMaker where you copy data from S3 to training to serving, Databricks uses Delta Lake as a single source of truth. This reduces latency, ensures consistency, and accelerates time to market."

### Feature Store Value
"Feature Store solves three problems: (1) Training-serving consistency—same feature code for both, eliminating skew. (2) Feature reuse—data scientists discover and reuse features instead of reimplementing. (3) Governance—Unity Catalog tracks lineage and access control for features."

### MLflow Integration
"MLflow tracks all experiments—parameters, metrics, artifacts, code. Model Registry provides versioning and stage transitions (dev → staging → prod). Unity Catalog extends this with fine-grained access control and lineage across workspaces, critical for governance."

### GenAI Focus (2026)
"RAG combines the knowledge of LLMs with real-time retrieval from our data. Databricks makes this seamless: documents in Delta Lake, embeddings via Model Serving, Vector Search for retrieval, and Foundation Model API for generation. All with Unity Catalog governance."

---

## ⚖️ Common Trade-offs (Always Mention These)

### Latency vs Accuracy
- Simple models fast but less accurate
- Deep learning accurate but slow
- **Solution**: Two-stage (fast filter + precise ranking)

### Real-time vs Batch
- Real-time fresh but expensive
- Batch cheap but stale
- **Solution**: Hybrid (batch heavy features, stream critical signals)

### Cost vs Performance
- Serverless cheaper for variable load
- Provisioned better for steady high throughput
- **Solution**: Match to workload pattern

### Exploration vs Exploitation
- Pure exploitation misses new options
- Pure exploration ignores what works
- **Solution**: Multi-armed bandit (Thompson Sampling)

---

## 📊 Key Metrics (Quick Reference)

**Classification:**
- Imbalanced data → PR-AUC (not ROC-AUC)
- Balanced data → Accuracy, F1-score

**Ranking:**
- NDCG@K (rewards top positions)
- Precision@K, Recall@K
- MRR (mean reciprocal rank)

**GenAI/RAG:**
- Faithfulness (matches sources?)
- Groundedness (supported by context?)
- Relevance (answers question?)
- Hallucination rate
- Citation accuracy

**System:**
- Latency: p50, p95, p99
- Throughput: QPS/TPS
- Availability: Uptime %
- Cost: Cost per prediction

---

## 🚨 Common Pitfalls (AVOID THESE)

1. ❌ Jumping to solution without asking questions
2. ❌ Ignoring cost, security, disaster recovery
3. ❌ Not explaining trade-offs
4. ❌ Silent thinking (think out loud!)
5. ❌ Forgetting monitoring and feedback loops
6. ❌ Over-engineering or under-engineering
7. ❌ Not mentioning Unity Catalog (governance is critical)
8. ❌ Ignoring GenAI (it's 2026, LLMs are everywhere)

---

## 🎯 3 Scenario Templates

### Template 1: Personalization/Recommendation
**Pattern:**
- Two-stage (retrieval + ranking)
- Feature Store (user + item features)
- Real-time serving (low latency)
- A/B testing
- Cold start (bandit)

### Template 2: Fraud/Anomaly Detection
**Pattern:**
- Imbalanced data (SMOTE, class weights)
- Real-time inference (<100ms)
- Two-tier response (reject, review, challenge)
- Adversarial robustness
- Weekly retraining

### Template 3: GenAI/RAG
**Pattern:**
- Document → Chunk → Embed → Vector DB
- Retrieval → Augment → Generate
- LLM-as-judge evaluation
- Multi-turn conversation
- Guardrails (input, output, PII)

---

## 🗣️ Opening Lines (Use These)

**Start with discovery:**
"Great question. Before I dive into the architecture, let me clarify a few requirements to ensure I understand the problem correctly. First, what's the primary business objective here—are we optimizing for [X, Y, or Z]?"

**Transition to design:**
"Understood. So we're [restate requirements]. This sounds like a [classification/ranking/generation] problem. Let me frame the ML task and then walk through the architecture on the whiteboard."

**Explain trade-offs:**
"I'm choosing [X] over [Y] because [reason], but this trades off [downside]. If [condition changes], we could switch to [alternative approach]."

**Close the loop:**
"That's my high-level design covering [list components]. I'm happy to deep-dive into any area—feature engineering, model architecture, serving infrastructure, or monitoring. What would you like to explore further?"

---

## ⏰ Time Management

| Phase | Time | What to Cover |
|-------|------|---------------|
| **Discovery** | 10-15 min | Ask 10-15 clarifying questions |
| **Problem Definition** | 3-5 min | Frame ML task, metrics |
| **Architecture** | 25-30 min | Draw end-to-end system |
| **Deep-Dive** | 15-20 min | Answer follow-ups on AI/ML |
| **Wrap-up** | 5 min | Ask your questions |

**Pacing check at 30 min:** Should be done with discovery + architecture, starting deep-dive

---

## 🧠 Mental Models

### ML Lifecycle
```
Data → Features → Train → Evaluate →
Deploy → Monitor → Retrain (loop)
```

### Databricks Stack
```
Data: Delta Lake + Unity Catalog
Processing: Spark + Delta Live Tables
ML: MLflow + Feature Store + Model Serving
GenAI: Vector Search + Foundation Models
Governance: Unity Catalog (lineage, access)
```

### Production ML Challenges
```
Training-serving skew → Feature Store
Data drift → Monitoring + retraining
Cold start → Bandit + content features
Cost → Autoscaling + caching
Latency → Two-stage + caching
Bias → Fairness metrics + auditing
```

---

## 💪 Confidence Boosters

**You have:**
- 8+ years ML/DS experience
- Deep understanding of production ML
- Strong system design thinking
- Expertise in ML algorithms and evaluation

**They want to see:**
- How you think (not just what you know)
- How you ask questions (discovery)
- How you make trade-offs (engineering judgment)
- How you communicate (clarity, structure)

**Remember:**
- No perfect solution (acknowledge trade-offs)
- It's okay to say "I don't know, but here's how I'd find out"
- Interviewer is your partner (not adversary)
- You're advising a customer (consultative approach)

---

## 📝 Your Questions for Interviewer (Pick 2-3)

1. "What are the most common customer challenges you see with ML deployments on Databricks?"
2. "How is the team thinking about GenAI and LLMs in the roadmap?"
3. "What's the typical team structure for Solutions Architects? Do you work solo or in teams?"
4. "Can you share an example of a recent customer engagement that was particularly challenging?"
5. "What's the most exciting thing about Databricks' AI/ML platform right now?"

---

## ✅ Final Pre-Interview Checklist (30 min before)

- [ ] Read this cheatsheet (10 min)
- [ ] Test video/audio/whiteboard tool (5 min)
- [ ] Review 3 scenario templates (5 min)
- [ ] Practice opening lines out loud (3 min)
- [ ] Deep breathing exercise (2 min)
- [ ] Arrive to call 5 min early

---

## 🎯 Last Minute Reminders

1. **THINK OUT LOUD** - Narrate your thought process
2. **ASK QUESTIONS** - Discovery before design
3. **DRAW DIAGRAMS** - Visual communication
4. **EXPLAIN TRADE-OFFS** - Show engineering judgment
5. **MENTION DATABRICKS PLATFORM** - Unity Catalog, MLflow, Feature Store, Vector Search
6. **FOCUS ON GENAI** - RAG is critical in 2026
7. **BE CONFIDENT** - You have the experience, trust yourself

---

**You've got this! Go crush it! 🚀**

Remember: They're hiring you for how you think, not what you memorized. Be yourself, be curious, be consultative.
