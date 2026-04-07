# Databricks Sr. Solutions Architect - ML/DS Focus
## 6-Day Crash Course for ML/Data Science Professionals

**Your Background**: 8+ years ML/Data Science experience
**Interview Date**: In 6 days
**Technical Spike**: AI/ML (Generative AI, MLOps, Feature Engineering)
**Interview Duration**: 60 minutes

---

## 🎯 Key Intelligence from 2026 Interviews

**CRITICAL INSIGHT**: GenAI and system design are now weighted **more heavily** than classical ML and coding combined. LLMs, Generative AI, and AI Agents represent the single largest category in 2026 Databricks interviews.

### What's Changed in 2026
- **Primary Focus**: Production RAG architectures, Mosaic AI, Agent Framework, Model Serving
- **Expected Knowledge**: Concrete metrics (faithfulness, groundedness, relevance) + LLM-as-judge pipelines
- **Platform Integration**: Delta Lake + Unity Catalog + MLflow + Model Serving (not standalone ML)
- **Coding Difficulty**: LeetCode Medium/Hard level (but less weight than GenAI system design)

---

## 📅 6-Day Preparation Plan

### Day 1 (Today): Core Platform + MLOps Fundamentals
**Time**: 4-5 hours
- [ ] **Morning (2h)**: Study Databricks ML platform architecture
  - Read: [AI and Machine Learning on Databricks](https://docs.databricks.com/aws/en/machine-learning/)
  - Understand: How Databricks unifies data eng + ML (vs SageMaker/Vertex AI)
  - Key differentiator: Lakehouse = unified data layer for both data and ML
- [ ] **Afternoon (2h)**: MLflow end-to-end
  - Read: [MLflow on Databricks](https://docs.databricks.com/aws/en/mlflow/)
  - Hands-on: Set up MLflow experiment tracking (use Community Edition)
  - Practice: Log model, parameters, metrics, artifacts
- [ ] **Evening (1h)**: MLOps workflow overview
  - Read: [MLOps Workflows on Databricks](https://docs.databricks.com/aws/en/machine-learning/mlops/mlops-workflow)
  - Understand: Dev → Staging → Prod promotion with Model Registry

### Day 2: Feature Store + Model Serving
**Time**: 4-5 hours
- [ ] **Morning (2h)**: Feature Engineering on Databricks
  - Read: [Feature Store Complete Guide](https://www.databricks.com/blog/what-feature-store-complete-guide-ml-feature-engineering)
  - Understand: Training-serving skew, online-offline parity
  - Key pattern: Feature tables in Delta + automatic tracking with MLflow
- [ ] **Afternoon (2h)**: Model Serving Architecture
  - Read: [Model Serving Architectures on Databricks](https://medium.com/marvelous-mlops/model-serving-architectures-on-databricks-700be679eb5c)
  - Study: Serverless vs provisioned endpoints, auto-scaling, A/B testing
  - Practice: Design a real-time inference endpoint (on paper)
- [ ] **Evening (1h)**: Review Feature Store + Model Serving system design
  - Resource: [Feature Store & Model Serving System Design](https://system-design.space/en/chapter/feature-store-model-serving/)
  - Practice: Whiteboard end-to-end ML platform architecture

### Day 3: Generative AI & RAG (CRITICAL)
**Time**: 5-6 hours
- [ ] **Morning (2.5h)**: RAG Architecture on Databricks
  - Read: [RAG on Databricks](https://docs.databricks.com/aws/en/generative-ai/retrieval-augmented-generation)
  - Read: [What is RAG?](https://www.databricks.com/blog/what-is-retrieval-augmented-generation)
  - Understand: Vector Search + Embedding models + LLM integration
  - Key components: Document ingestion → Chunking → Embedding → Vector DB → Retrieval → LLM
- [ ] **Afternoon (2h)**: Agent System Design Patterns
  - Read: [Agent System Design Patterns](https://docs.databricks.com/aws/en/generative-ai/guide/agent-system-design-patterns)
  - Study 3 patterns: Deterministic chains, Agentic systems, Hybrid approaches
  - Understand: When to use each pattern (predictability vs autonomy)
- [ ] **Evening (1.5h)**: Generative AI Evaluation
  - Study: LLM-as-judge pipelines, faithfulness/groundedness/relevance metrics
  - Read: [Generative AI Concepts](https://docs.databricks.com/aws/en/generative-ai/guide/concepts/)
  - Practice: Design RAG evaluation framework

### Day 4: ML System Design Practice
**Time**: 5-6 hours
- [ ] **Morning (3h)**: Study ML System Design Framework
  - Read: [ML System Design Interview Guide](https://www.tryexponent.com/blog/machine-learning-system-design-interview-guide)
  - Framework: Problem definition → Metrics → Architecture → Training → Inference → Monitoring
  - Practice 3 scenarios (see below): Recommendation system, Fraud detection, Personalization
- [ ] **Afternoon (2h)**: Practice Databricks-specific scenarios
  - Scenario 1: Design customer churn prediction platform (30 min)
  - Scenario 2: Design real-time fraud detection system (30 min)
  - Scenario 3: Design LLM-powered chatbot with RAG (30 min)
  - Focus: Think out loud, draw architecture, justify trade-offs
- [ ] **Evening (1h)**: Review common failure modes
  - Training-serving skew, data drift, model staleness
  - Cold start problems, latency vs accuracy trade-offs
  - Cost optimization (inference costs can exceed training costs)

### Day 5: Mock Interview + Advanced Topics
**Time**: 4-5 hours
- [ ] **Morning (2h)**: Full 60-min mock interview
  - Find a colleague or use AI to simulate
  - Practice: Discovery (10 min) → Architecture (30 min) → Deep-dive (20 min)
  - Record yourself and review
- [ ] **Afternoon (2h)**: Advanced ML topics
  - Distributed training (Horovod, Ray on Databricks)
  - Model monitoring and drift detection
  - A/B testing frameworks
  - Multi-model serving (champion-challenger)
- [ ] **Evening (1h)**: Unity Catalog for ML governance
  - Read: [Unity Catalog Best Practices](https://docs.databricks.com/aws/en/data-governance/unity-catalog/best-practices)
  - Understand: Model lineage, feature lineage, access control for models

### Day 6 (Day Before Interview): Review & Polish
**Time**: 3-4 hours
- [ ] **Morning (2h)**: Review all scenarios and talking points
  - Skim this document end-to-end
  - Review your whiteboard diagrams
  - Practice explaining trade-offs verbally
- [ ] **Afternoon (1h)**: Prepare your questions for interviewer
  - About Databricks AI/ML roadmap
  - About customer challenges with GenAI
  - About team structure and collaboration
- [ ] **Evening**: Light review + rest
  - Review key metrics and evaluation frameworks
  - Early dinner, good sleep
  - Confidence mindset

---

## 🔥 Critical ML/AI Interview Scenarios

### Scenario 1: Production ML Platform for Personalization
**Business Context:**
> "We're a streaming service with 100M users. We need to build a real-time personalization platform that recommends content based on user behavior, viewing history, and contextual signals. The system should serve recommendations in <100ms and continuously learn from user interactions. Design the end-to-end ML platform on Databricks."

**Discovery Questions to Ask:**
- What's the traffic pattern? (Peak QPS for recommendations?)
- What's the acceptable latency? (100ms includes model inference + feature retrieval?)
- How fresh should recommendations be? (Real-time learning vs batch retraining?)
- What features are available? (User profile, session context, content metadata?)
- What's the cold start strategy? (New users, new content?)
- Compliance requirements? (GDPR, explainability?)

**Your Architecture Should Cover:**

```
Data Layer (Lakehouse):
├── Bronze: Raw events (views, clicks, ratings) via streaming
├── Silver: Cleaned, joined user-content interactions
└── Gold: Aggregated user profiles, content features

Feature Engineering:
├── Offline Features (Delta Tables):
│   ├── User features: watch_history_28d, genre_preferences, avg_watch_time
│   ├── Content features: popularity_score, category, release_date
│   └── Contextual: time_of_day, device_type, location
├── Online Features (Feature Store):
│   ├── Low-latency lookup via Feature Serving
│   ├── Point-in-time correctness for training
│   └── Automated feature refresh pipelines

Model Training:
├── Training Pipeline (Databricks Workflows):
│   ├── Feature extraction from Feature Store
│   ├── Distributed training with Spark ML or PyTorch on Ray
│   ├── Hyperparameter tuning with Hyperopt
│   └── Model versioning with MLflow
├── Model Evaluation:
│   ├── Offline metrics: NDCG@10, Precision@K, Recall@K
│   ├── Online metrics: CTR, watch time, engagement rate
│   └── A/B testing framework

Model Serving:
├── Real-time Inference:
│   ├── Serverless Model Serving endpoint (auto-scaling)
│   ├── Feature retrieval from Online Feature Store (<10ms)
│   ├── Model inference (<50ms with optimized models)
│   └── Response caching for popular requests
├── Deployment Strategy:
│   ├── Blue-green deployment for safety
│   ├── A/B testing (10% traffic to new model)
│   └── Automated rollback on metric degradation

Monitoring & Feedback Loop:
├── Model Monitoring:
│   ├── Input drift detection (feature distributions)
│   ├── Prediction drift (recommendation diversity)
│   ├── Performance metrics (latency, throughput)
│   └── Business metrics (CTR, engagement)
├── Feedback Loop:
│   ├── Log predictions + outcomes (clicks, watches)
│   ├── Streaming feature updates (real-time user state)
│   ├── Incremental learning (daily retraining on new data)
│   └── Close the loop: predictions → outcomes → features → retrain
```

**Key Trade-offs to Discuss:**
1. **Latency vs Accuracy**:
   - Simpler models (matrix factorization) faster but less accurate
   - Deep learning (two-tower, transformers) more accurate but slower
   - Solution: Two-stage ranking (fast retrieval + precise ranking)

2. **Real-time vs Batch**:
   - Real-time feature updates expensive (streaming infrastructure)
   - Batch updates (hourly/daily) cheaper but stale
   - Solution: Hybrid (batch for heavy features, streaming for critical signals)

3. **Cold Start**:
   - New users: Use popularity-based or demographic-based recommendations
   - New content: Leverage content features (genre, actors) + explore
   - Solution: Multi-armed bandit (Thompson Sampling) for exploration

4. **Cost Optimization**:
   - Model serving can cost more than training
   - Use caching, model distillation, quantization
   - Serverless endpoints scale to zero during low traffic

**Expected Deep-Dive Questions:**
- "How would you handle data drift in user preferences?"
- "Explain your A/B testing framework. How do you avoid Simpson's Paradox?"
- "How do you ensure point-in-time correctness for features?"
- "What if a model update causes CTR to drop 5%? Walk me through your rollback process."

---

### Scenario 2: Real-Time Fraud Detection with ML
**Business Context:**
> "We're a fintech company processing 50,000 transactions per second. We need to detect fraudulent transactions in real-time (<100ms decision) while minimizing false positives (which hurt customer experience). Design the ML-powered fraud detection system."

**Discovery Questions:**
- What's the fraud rate? (Imbalanced dataset challenge)
- What's the cost of false positives vs false negatives?
- What features are available at inference time?
- Can we afford post-processing (review queue)?
- Compliance requirements? (Explainability for rejected transactions?)

**Your Architecture:**

```
Real-Time Data Pipeline:
├── Ingestion: Kafka → Structured Streaming → Delta Lake
├── Feature Engineering (streaming):
│   ├── Transaction features: amount, merchant, location, time
│   ├── User features: avg_transaction_amount_7d, velocity_1h
│   ├── Network features: IP reputation, device fingerprint
│   └── Graph features: merchant-user network, fraud rings
├── Feature Store: Low-latency online features (<10ms lookup)

Model Architecture:
├── Two-Stage Approach:
│   ├── Stage 1: Fast rule-based filter (eliminates 95% safe transactions)
│   ├── Stage 2: ML model for borderline cases
│   └── Latency budget: 20ms rules + 50ms ML = 70ms total
├── Model Options:
│   ├── Gradient Boosting (XGBoost/LightGBM): Fast, accurate, interpretable
│   ├── Deep Learning (AutoEncoder): Anomaly detection for novel fraud
│   └── Ensemble: Combine both for best of both worlds

Training Pipeline:
├── Data: Heavily imbalanced (0.1% fraud rate)
├── Sampling Strategy:
│   ├── Undersample majority class (legitimate transactions)
│   ├── Oversample minority class (SMOTE, ADASYN)
│   ├── Class weights in loss function
│   └── Focal loss for hard examples
├── Features:
│   ├── Point-in-time correctness (no data leakage)
│   ├── Aggregations: 1h, 6h, 24h, 7d windows
│   └── Handle missing values (fraud often has missing data)
├── Evaluation:
│   ├── Precision-Recall curve (not ROC for imbalanced data)
│   ├── PR-AUC, F1-score at operating point
│   ├── Cost-sensitive evaluation (FP cost = $5, FN cost = $100)
│   └── Stratified CV by time (no future data in training)

Model Serving:
├── Real-time Endpoint:
│   ├── Provisioned throughput (50K TPS, can't cold start)
│   ├── Multi-model deployment (rule-based + ML)
│   ├── Feature caching (user profile features)
│   └── Request batching for efficiency
├── Decision Thresholds:
│   ├── High confidence fraud → Auto-reject
│   ├── Low confidence fraud → Manual review queue
│   ├── Medium confidence → Step-up authentication (SMS/2FA)
│   └── Dynamic thresholds by risk segment (high-value customers)

Monitoring & Adaptive Learning:
├── Model Monitoring:
│   ├── Prediction distribution (fraud rate should be stable)
│   ├── Feature drift (new fraud patterns emerge weekly)
│   ├── Performance decay (fraudsters adapt to model)
│   └── Latency spikes (degraded service)
├── Feedback Loop:
│   ├── Manual review outcomes → Ground truth labels
│   ├── Customer disputes → False positives
│   ├── Chargebacks → False negatives (missed fraud)
│   └── Weekly retraining with new fraud patterns
├── Adversarial Robustness:
│   ├── Fraudsters will test model boundaries
│   ├── Explainability can leak model logic → Use carefully
│   ├── Model diversity (ensemble) harder to game
│   └── Honeypot features to detect adversarial attacks
```

**Key Trade-offs:**
1. **False Positives vs False Negatives**:
   - FP: Legitimate customer blocked (bad UX, lost revenue)
   - FN: Fraud goes through (direct financial loss)
   - Solution: Multi-tier response (reject, review, challenge)

2. **Latency vs Accuracy**:
   - Complex models (deep learning) more accurate but slower
   - Simple models (logistic regression) fast but miss complex fraud
   - Solution: Two-stage (fast filter + selective deep learning)

3. **Real-time Retraining vs Scheduled**:
   - Real-time: Catch new fraud patterns immediately
   - Scheduled: More stable, cheaper
   - Solution: Incremental learning daily + ad-hoc for major fraud waves

4. **Explainability vs Performance**:
   - Regulations may require explaining rejections
   - Black-box models (deep learning) perform better
   - Solution: SHAP values post-hoc, or use interpretable models

**Expected Deep-Dive Questions:**
- "How do you handle class imbalance in fraud detection?"
- "Fraudsters adapt to your model. How do you detect and respond to adversarial attacks?"
- "Explain how you'd implement online learning to adapt to new fraud patterns."
- "Walk me through your feature engineering for a network-based fraud feature (e.g., fraud ring detection)."

---

### Scenario 3: LLM-Powered Customer Support with RAG
**Business Context:**
> "We're an enterprise SaaS company with 10,000 customers. We want to build an AI assistant that can answer customer questions by retrieving relevant information from our documentation (1M+ pages), support tickets, and product knowledge base. The assistant should provide accurate, contextual answers with source citations. Design this RAG system on Databricks."

**Discovery Questions:**
- What's the query volume? (QPS for support requests?)
- What's the acceptable latency? (Interactive chat vs async email?)
- What documents are in scope? (Public docs, internal wikis, tickets?)
- Do we need multi-turn conversations? (Stateful vs stateless?)
- Privacy/security requirements? (Customer data in prompts?)
- Evaluation criteria? (Accuracy, hallucination rate, customer satisfaction?)

**Your Architecture:**

```
Data Ingestion & Preparation:
├── Document Sources:
│   ├── Public docs (website, API docs, tutorials)
│   ├── Internal knowledge base (Confluence, Notion)
│   ├── Support tickets (historical Q&A pairs)
│   └── Product changelogs (new features, deprecations)
├── Ingestion Pipeline (Delta Live Tables):
│   ├── Extract: Web scraping, API connectors, database dumps
│   ├── Parse: HTML → Markdown, PDF → text
│   ├── Chunk: Split long documents (500-1000 tokens per chunk)
│   ├── Metadata: Source, timestamp, version, access_level
│   └── Store: Delta tables (bronze → silver → gold)

Embedding & Vector Search:
├── Embedding Model:
│   ├── Options: bge-large-en, e5-mistral, OpenAI text-embedding-3
│   ├── Host on Databricks Model Serving (or use Foundation Model API)
│   ├── Batch embed all documents (offline pipeline)
│   └── Real-time embed user queries (online)
├── Vector Search Index:
│   ├── Databricks Vector Search (managed service)
│   ├── Index type: Delta Sync (auto-updates on new docs)
│   ├── Similarity metric: Cosine similarity
│   ├── Index config: HNSW for speed, IVF for scale
│   └── Hybrid search: Vector + keyword (BM25) for best recall

RAG Pipeline:
├── Query Processing:
│   ├── Intent classification (question, troubleshooting, how-to)
│   ├── Query expansion (rephrase, add context)
│   ├── Filter by metadata (product version, customer tier)
│   └── Semantic search (retrieve top-k chunks, k=5-10)
├── Context Augmentation:
│   ├── Retrieved chunks → Ranked by relevance
│   ├── Re-ranking model (cross-encoder for better precision)
│   ├── Context window management (4K-8K tokens for LLM)
│   ├── Include source citations (doc ID, URL)
│   └── Add system prompt (tone, format, constraints)
├── LLM Generation:
│   ├── Model options:
│   │   ├── Databricks DBRX (fast, cost-effective)
│   │   ├── Llama 3 70B (open-source, customizable)
│   │   ├── GPT-4 (highest quality, via Azure OpenAI)
│   │   └── Fine-tuned model (domain-specific)
│   ├── Prompt engineering:
│   │   ├── System: "You are a helpful assistant. Only use provided context."
│   │   ├── Context: Retrieved chunks with sources
│   │   ├── User question
│   │   ├── Instructions: "Cite sources using [doc_id]"
│   │   └── Safety: "If unsure, say 'I don't know' instead of hallucinating"
│   ├── Generation parameters:
│   │   ├── Temperature: 0.0 (deterministic for factual Q&A)
│   │   ├── Max tokens: 500 (concise answers)
│   │   └── Top-p: 0.9 (nucleus sampling)
│   └── Post-processing:
│       ├── Extract citations
│       ├── Format as markdown
│       └── Add disclaimer if confidence is low

Multi-turn Conversation:
├── Session Management:
│   ├── Store conversation history (Redis/DynamoDB)
│   ├── Context window: Last 5 turns (avoid token overflow)
│   ├── Session timeout: 30 minutes
│   └── Privacy: Encrypt conversation history
├── Conversational Features:
│   ├── Follow-up questions (use previous context)
│   ├── Clarification (ask user for more details)
│   ├── Handoff to human (if AI can't answer)
│   └── Feedback loop (thumbs up/down on responses)

Evaluation & Monitoring:
├── Offline Evaluation (Pre-deployment):
│   ├── Test set: 1000 curated Q&A pairs
│   ├── Retrieval metrics:
│   │   ├── Recall@k: Are correct docs in top-k? (target: >90%)
│   │   ├── MRR (Mean Reciprocal Rank): Rank of first correct doc
│   │   └── NDCG@k: Ranked quality of retrieval
│   ├── Generation metrics:
│   │   ├── Faithfulness: Does answer match source docs? (LLM-as-judge)
│   │   ├── Groundedness: Is answer supported by context? (entailment model)
│   │   ├── Relevance: Does answer address the question? (LLM-as-judge)
│   │   ├── Hallucination rate: % of unsupported claims
│   │   └── Citation accuracy: Are sources correctly cited?
│   ├── Human evaluation:
│   │   ├── Correctness (1-5 scale)
│   │   ├── Completeness (1-5 scale)
│   │   └── Helpfulness (1-5 scale)
├── Online Monitoring (Production):
│   ├── Usage metrics: Queries/day, users, session length
│   ├── Performance: Latency (p50, p95, p99), error rate
│   ├── Quality: User feedback (thumbs up/down rate)
│   ├── Business impact: Ticket deflection rate, CSAT
│   └── Safety: Harmful content detection, PII leakage

Continuous Improvement:
├── Feedback Loop:
│   ├── Log all queries + retrieved docs + generated answers
│   ├── User feedback (thumbs up/down) → Ground truth labels
│   ├── Analyze failures (low thumbs up, unanswered questions)
│   └── MLflow tracking for all experiments
├── Improvement Strategies:
│   ├── Expand knowledge base (add missing docs)
│   ├── Improve chunking (better boundaries, overlap)
│   ├── Fine-tune embedding model (domain-specific)
│   ├── Fine-tune LLM (on company-specific Q&A)
│   ├── Prompt engineering (A/B test prompts)
│   └── Hybrid search tuning (balance vector + keyword)
```

**Key Trade-offs:**
1. **Chunk Size**:
   - Small chunks (256 tokens): More precise retrieval, but lose context
   - Large chunks (1024 tokens): More context, but noisier retrieval
   - Solution: Hierarchical retrieval (retrieve large, rank small)

2. **Retrieval Quality vs Latency**:
   - More retrieved docs (k=20) → Better recall, but slower LLM + higher cost
   - Fewer docs (k=3) → Faster, cheaper, but might miss relevant info
   - Solution: Two-stage (fast retrieval + re-ranking)

3. **LLM Choice**:
   - DBRX: Fast, cheap, good for simple queries
   - GPT-4: Best quality, but expensive and slower
   - Solution: Route by complexity (simple → DBRX, complex → GPT-4)

4. **Freshness vs Cost**:
   - Real-time embedding: Always up-to-date, but expensive
   - Batch embedding (hourly/daily): Cheaper, but stale
   - Solution: Incremental updates (embed only new/changed docs)

**Expected Deep-Dive Questions:**
- "How do you evaluate faithfulness and groundedness in RAG systems?"
- "Explain your strategy for handling multi-hop questions (requires combining info from multiple docs)."
- "How would you implement hybrid search (vector + keyword)? When is each better?"
- "Walk me through your prompt engineering process. How do you prevent hallucinations?"
- "How do you handle PII in customer queries when sending to external LLMs?"

---

## 🧠 ML System Design Framework (6 Steps)

Use this framework for ANY ML scenario in the interview:

### Step 1: Clarify Requirements (5-7 minutes)
**Ask about:**
- Business objective (revenue, cost reduction, UX improvement?)
- Success metrics (online vs offline)
- Constraints (latency, cost, scale)
- Data availability (what features exist, what labels, volume?)
- Existing systems (greenfield vs integration)

**Example questions:**
- "What's the acceptable latency for predictions?"
- "How many predictions per second do we need to serve?"
- "What's more important: precision or recall?"
- "Do we have labeled data? How much?"

### Step 2: Define ML Problem (3-5 minutes)
**Frame the problem:**
- Task type (classification, regression, ranking, generation, etc.)
- Input (what features are available?)
- Output (what are we predicting?)
- Evaluation metric (precision@k, NDCG, MSE, faithfulness, etc.)

**Example:**
- "This is a binary classification problem (fraud vs not fraud)"
- "Input: Transaction features (amount, merchant, user history)"
- "Output: Probability of fraud (0-1)"
- "Metric: PR-AUC (because class imbalance) + cost-weighted F1"

### Step 3: Data & Features (5-7 minutes)
**Design feature pipeline:**
- Data sources (where does data come from?)
- Feature engineering (what features to compute?)
- Feature storage (online vs offline)
- Feature freshness (real-time vs batch?)
- Data quality (validation, monitoring)

**Example features for recommendation:**
- User features: age, location, watch_history_7d, genre_preferences
- Item features: popularity, category, release_date
- Context features: time_of_day, device_type
- Interaction features: user-item affinity, collaborative filtering scores

### Step 4: Model Training (7-10 minutes)
**Training pipeline:**
- Model architecture (which algorithm? why?)
- Training data (how to sample? class imbalance?)
- Experimentation (how to track experiments?)
- Evaluation (offline metrics, validation strategy)
- Hyperparameter tuning (grid search, Bayesian optimization?)

**Key decisions:**
- Simple model (logistic regression, decision tree) vs complex (deep learning)
- Online learning (incremental) vs batch retraining
- Ensemble (multiple models) vs single model

### Step 5: Inference & Serving (7-10 minutes)
**Serving architecture:**
- Batch prediction vs real-time serving
- Latency budget (how fast must predictions be?)
- Throughput (QPS, concurrent requests?)
- Caching strategy (cache predictions? features?)
- A/B testing (how to deploy safely?)

**Example architectures:**
- Real-time: REST API → Feature retrieval → Model inference → Response
- Batch: Scheduled job → Score all users → Write to database
- Hybrid: Pre-compute some predictions, real-time for personalized

### Step 6: Monitoring & Iteration (5-7 minutes)
**Production monitoring:**
- Input monitoring (feature drift, data quality)
- Output monitoring (prediction distribution, anomalies)
- Performance monitoring (latency, throughput, errors)
- Business metrics (CTR, revenue, customer satisfaction)
- Feedback loop (retrain on new data, close the loop)

**Key questions:**
- How do you detect model decay?
- What triggers a retrain?
- How do you handle concept drift?
- What's your rollback strategy if a new model performs poorly?

---

## 💡 Key Talking Points for ML/DS Background

### Demonstrate ML Expertise

**Instead of**: "I'd train a model on the data."
**Say**: "Given the class imbalance (0.1% fraud rate), I'd use stratified sampling and cost-sensitive learning. For evaluation, I'd focus on PR-AUC rather than ROC-AUC since accuracy is misleading with imbalanced classes. I'd also implement a two-stage approach: a fast rule-based filter for obvious cases, then a gradient boosting model for borderline transactions to stay within the 100ms latency budget."

**Instead of**: "I'd use a neural network."
**Say**: "I'm considering a two-tower neural network for this recommendation task because it allows us to pre-compute item embeddings offline and only compute user embeddings at inference time, reducing latency from 200ms to 50ms. However, this sacrifices some cross-feature interactions compared to a full interaction model. Given the 100ms SLA and 10K QPS requirement, I think this trade-off is justified. We could also distill the full model into the two-tower architecture to get the best of both worlds."

### Show Production ML Thinking

**Training-Serving Skew:**
"A critical challenge is training-serving skew. In training, we compute features using perfect hindsight (e.g., user's 7-day watch history). At inference, we need to reconstruct the same features from the online feature store. I'd use Databricks Feature Store to ensure consistency: define features once, use them in both training and serving. I'd also implement point-in-time correctness to prevent data leakage."

**Model Monitoring:**
"For monitoring, I'd track both statistical drift and business metrics. Statistical drift: compare feature distributions (KL divergence, population stability index) between training and production data. Business metrics: monitor precision@k, CTR, revenue per user. I'd set up alerts when metrics degrade beyond thresholds, triggering a retrain. However, I wouldn't retrain on every drift signal—sometimes drift is real (e.g., seasonal changes) and the model should adapt, not revert."

**A/B Testing:**
"For A/B testing, I'd use a multi-armed bandit approach rather than fixed traffic splits. Start with 10% traffic to the new model, monitor metrics hourly, and use Thompson Sampling to gradually increase traffic if it's performing better. This minimizes risk while maximizing learning. I'd also implement guardrail metrics (e.g., latency, error rate) that trigger automatic rollback if violated, independent of business metrics which can be noisy short-term."

### Databricks-Specific Value Propositions

**Unified Data + ML:**
"The key advantage of Databricks is the unified lakehouse. In a traditional setup, we'd have data in a data warehouse (Snowflake), then copy to S3 for training (SageMaker), then copy features to Redis for serving. Each copy introduces latency, staleness, and consistency issues. With Databricks, data lives in Delta Lake, accessible for both SQL analytics and ML training, with features served directly from the lakehouse. This eliminates data silos and reduces TTM (time to market) for ML models."

**MLflow Integration:**
"I'd use MLflow to track all experiments: hyperparameters, metrics, model artifacts, code version. This is critical for reproducibility and model governance. When a model is promoted to production, MLflow Model Registry provides versioning, stage transitions (dev → staging → prod), and audit logs. Unity Catalog extends this with fine-grained access control and lineage tracking across workspaces."

**Feature Store Benefits:**
"Databricks Feature Store solves three problems: (1) Feature reuse—data scientists can discover and reuse features instead of re-implementing, (2) Consistency—same feature code for training and serving, eliminating training-serving skew, (3) Governance—Unity Catalog tracks feature lineage and access control. For example, if a 'user_avg_purchase_30d' feature is used by 5 models, changing it requires understanding downstream impact via lineage."

---

## 🎓 Advanced ML Topics (Be Ready to Deep-Dive)

### 1. Handling Data Drift & Concept Drift

**Data Drift**: Input distribution changes (e.g., new customer demographics)
**Concept Drift**: Input-output relationship changes (e.g., what constitutes fraud evolves)

**Detection:**
- Statistical tests: Kolmogorov-Smirnov test, Chi-squared test
- Distance metrics: KL divergence, Wasserstein distance, PSI (Population Stability Index)
- Monitor per-feature distributions over time

**Response:**
- **Retrain**: If drift is real and model performance degrades → retrain on recent data
- **Adapt**: Use online learning (incremental updates) for gradual drift
- **Segment**: If drift affects only a user segment → train segment-specific models
- **Ignore**: Sometimes drift is noise or seasonal → don't overreact

**Example:**
"In a fraud detection system, concept drift is common because fraudsters adapt to detection methods. I'd monitor prediction distributions—if the fraud rate predicted by the model suddenly drops (e.g., from 0.1% to 0.01%), it suggests fraudsters have found a way to evade detection. I'd set up weekly retraining on the most recent data (30-day window) and use active learning to prioritize manual review of cases the model is uncertain about, creating a feedback loop for continuous improvement."

### 2. Feature Engineering at Scale

**Challenges:**
- Computing features for millions of users in real-time
- Ensuring point-in-time correctness (no data leakage)
- Handling late-arriving data
- Managing feature versioning

**Patterns:**
- **Pre-compute batch features**: Nightly job computes expensive features (e.g., 30-day aggregates)
- **Real-time feature updates**: Streaming pipeline for critical features (e.g., last action timestamp)
- **Feature caching**: Cache user features in Redis/DynamoDB for low-latency lookup
- **Feature serving**: Databricks Online Tables or AWS SageMaker Feature Store

**Example:**
"For a recommendation system, I'd pre-compute user embedding features (matrix factorization, 100-dim) nightly using Spark. These are stored in Databricks Feature Store. At inference time, we look up the pre-computed embedding (<10ms) rather than recomputing (which would take 100ms+). For real-time signals like 'user clicked on item X 5 seconds ago,' I'd use a streaming pipeline (Structured Streaming) to update a recent_interactions table, also served via Feature Serving."

### 3. Model Explainability & Interpretability

**When it matters:**
- Regulatory requirements (finance, healthcare)
- Building trust with stakeholders
- Debugging model behavior
- Detecting bias

**Techniques:**
- **SHAP (SHapley Additive exPlanations)**: Model-agnostic, local and global explanations
- **LIME (Local Interpretable Model-agnostic Explanations)**: Local explanations via surrogate models
- **Feature importance**: From tree-based models (Gini importance)
- **Attention weights**: From transformer models
- **Counterfactual explanations**: "If feature X was Y, prediction would change to Z"

**Example:**
"For a loan approval model, we need to explain rejections to customers and auditors. I'd use SHAP values to identify top-3 contributing features for each prediction. For example: 'Loan denied because: (1) debt-to-income ratio too high (SHAP = -0.3), (2) short credit history (SHAP = -0.2), (3) recent missed payment (SHAP = -0.15).' I'd also monitor SHAP values in aggregate to detect bias—if 'gender' or 'race' (even if not directly used) has non-zero SHAP via proxy features, that indicates potential bias."

### 4. Multi-Armed Bandits for Exploration-Exploitation

**Problem**: How to balance exploring new options vs exploiting known-good options?

**Algorithms:**
- **Epsilon-greedy**: Explore random action with probability ε, exploit best action with 1-ε
- **Thompson Sampling**: Bayesian approach, sample from posterior distribution
- **UCB (Upper Confidence Bound)**: Optimistic approach, choose action with highest upper bound

**Example:**
"For content recommendation, we face the cold-start problem with new content. A pure exploitation strategy (always recommend popular content) means new content never gets exposure. I'd use Thompson Sampling: maintain a Beta distribution for each content's CTR, sample from each distribution, and recommend the content with the highest sampled value. This naturally balances exploration (uncertain content gets tried) and exploitation (proven content is favored). Over time, as we collect feedback, the posterior converges and exploration decreases."

### 5. Distributed Training

**When to use:**
- Data doesn't fit in memory (data parallelism)
- Model doesn't fit in GPU memory (model parallelism)
- Need to speed up training (reduce wall-clock time)

**Approaches:**
- **Data Parallelism**: Split data across GPUs, each GPU has full model
  - Synchronous: Wait for all GPUs (slower but deterministic)
  - Asynchronous: Don't wait (faster but can diverge)
- **Model Parallelism**: Split model across GPUs (for very large models)
- **Pipeline Parallelism**: Split model into stages, pipeline batches through stages

**Databricks Options:**
- **Horovod**: Data parallelism for TensorFlow/PyTorch (MPI-based, efficient)
- **Ray on Databricks**: Distributed training + hyperparameter tuning
- **Spark ML**: Distributed training for classical ML (tree-based models)

**Example:**
"For training a large transformer model (1B+ parameters), I'd use Horovod on Databricks with 8 A100 GPUs. I'd use mixed-precision training (FP16) to reduce memory and speed up training. For data loading, I'd use Delta Lake as the data source, leveraging partitioning to ensure each GPU reads different data. For gradient synchronization, I'd use Horovod's ring-allreduce algorithm, which is more efficient than parameter server for all-reduce operations. Expected speedup: 6-7x on 8 GPUs (not linear due to communication overhead)."

### 6. LLM Fine-Tuning vs Prompting vs RAG

**When to use each:**

| Approach | Use Case | Cost | Latency | Effort |
|----------|----------|------|---------|--------|
| **Prompting (Zero-shot/Few-shot)** | General tasks, no training data | Low (inference only) | Low | Low |
| **RAG** | Needs up-to-date info, large knowledge base | Medium (embedding + inference) | Medium | Medium |
| **Fine-tuning** | Domain-specific language, behavior, or format | High (training cost) | Low (inference) | High |

**Decision tree:**
1. Start with prompting (cheapest, fastest)
2. If accuracy insufficient → Add RAG (no training needed)
3. If RAG insufficient → Fine-tune (expensive but best performance)

**Example:**
"For a customer support chatbot, I'd start with RAG using a pre-trained LLM (DBRX or Llama 3). RAG provides up-to-date information from our knowledge base without retraining. However, if the LLM's tone or format doesn't match our brand (e.g., too formal, too verbose), I'd fine-tune on our historical support tickets to learn the style. Fine-tuning would use LoRA (Low-Rank Adaptation) to reduce training cost—instead of updating all 70B parameters, we train 1% of parameters (700M), achieving 90% of full fine-tuning quality at 10% of the cost."

### 7. Guardrails for LLM Applications

**Risks:**
- **Hallucinations**: LLM generates false information
- **Prompt injection**: User manipulates LLM to ignore instructions
- **PII leakage**: LLM exposes sensitive data from training or context
- **Harmful content**: LLM generates offensive/dangerous content
- **Jailbreaking**: User tricks LLM into bypassing safety filters

**Mitigations:**
- **Input validation**: Check for prompt injection patterns, PII in user input
- **Output validation**: Check for hallucinations (faithfulness to context), harmful content
- **LLM-as-judge**: Use another LLM to evaluate output quality/safety
- **Retrieval filters**: Only retrieve from approved documents
- **Cite sources**: Require LLM to cite sources, verify citations
- **Human-in-the-loop**: Route high-risk queries to human review
- **Rate limiting**: Prevent abuse

**Example:**
"For our RAG-based Q&A system, I'd implement multiple guardrails: (1) Input guardrail: Scan user query for PII (SSN, credit card) and redact before sending to LLM. (2) Retrieval guardrail: Only retrieve from approved documents (filter by metadata). (3) Generation guardrail: Use LLM-as-judge to score faithfulness—compare generated answer to retrieved context using an entailment model. If faithfulness < 0.7, flag for human review. (4) Output guardrail: Check for harmful content using a content moderation API. (5) Audit log: Log all queries + responses for compliance."

---

## 📊 Critical Metrics for ML Systems

### Model Performance Metrics

**Classification:**
- **Accuracy**: Overall correctness (use only if balanced classes)
- **Precision**: TP / (TP + FP) — How many predicted positives are correct?
- **Recall**: TP / (TP + FN) — How many actual positives did we catch?
- **F1-score**: Harmonic mean of precision and recall
- **PR-AUC**: Area under precision-recall curve (better for imbalanced data)
- **ROC-AUC**: Area under ROC curve (use for balanced classes)

**Ranking (Recommendations):**
- **Precision@K**: Of top-K recommendations, how many are relevant?
- **Recall@K**: Of all relevant items, how many are in top-K?
- **NDCG@K**: Normalized Discounted Cumulative Gain (rewards top positions)
- **MRR**: Mean Reciprocal Rank (average 1/rank of first relevant item)
- **Hit Rate@K**: Fraction of users with at least 1 relevant item in top-K

**Regression:**
- **MAE**: Mean Absolute Error (average absolute difference)
- **RMSE**: Root Mean Squared Error (penalizes large errors more)
- **MAPE**: Mean Absolute Percentage Error (relative error)
- **R²**: Coefficient of determination (variance explained)

**Generative AI (LLMs/RAG):**
- **Faithfulness**: Does output match source documents? (LLM-as-judge)
- **Groundedness**: Is output supported by context? (entailment check)
- **Relevance**: Does output address the question? (LLM-as-judge)
- **Hallucination rate**: % of unsupported claims
- **BLEU/ROUGE**: N-gram overlap with reference (less used for RAG)
- **BERTScore**: Semantic similarity using embeddings
- **Citation accuracy**: Are sources correctly cited?

### System Performance Metrics

**Latency:**
- **p50 (median)**: 50% of requests faster than this
- **p95**: 95% of requests faster (important for UX)
- **p99**: 99% of requests faster (catch tail latencies)

**Throughput:**
- **QPS (Queries Per Second)**: How many requests can system handle?
- **RPS (Requests Per Second)**: Same as QPS

**Availability:**
- **Uptime**: % of time system is available (99.9% = 43 min downtime/month)
- **Error rate**: % of requests that fail

**Cost:**
- **Cost per prediction**: Total cost / number of predictions
- **DBU consumption**: Databricks Units consumed
- **GPU utilization**: % of GPU time actively computing

---

## 🔍 Common Interview Questions (ML/DS Focus)

### Technical Deep-Dive Questions

1. **"Explain how you'd implement feature versioning in a production ML system."**
   - Answer: Use Feature Store with versioned feature tables, track feature lineage in Unity Catalog, implement semantic versioning (v1.0, v1.1, v2.0) for breaking changes, maintain backward compatibility, A/B test new features before global rollout.

2. **"How do you prevent data leakage in ML pipelines?"**
   - Answer: Point-in-time correctness (use only data available at prediction time), time-based train/test split (no future data in training), hold-out test set from different time period, check for label leakage (features derived from target), validate feature computation logic.

3. **"Describe your approach to model monitoring in production."**
   - Answer: Three layers: (1) Data monitoring (feature drift via PSI/KL divergence), (2) Model monitoring (prediction drift, confidence distributions), (3) Business monitoring (CTR, revenue, customer satisfaction). Alert on statistical significance (2+ sigma from baseline) + business impact (>5% metric drop).

4. **"How would you debug a model that performs well offline but poorly online?"**
   - Answer: Check for training-serving skew (features computed differently), data drift (production data differs from training), feedback loop (model predictions change user behavior), evaluation mismatch (offline metric doesn't match online business metric), population mismatch (training data not representative).

5. **"Explain the difference between model parallelism and data parallelism."**
   - Answer: Data parallelism splits data across workers (each has full model), model parallelism splits model across workers (each has part of model). Use data parallelism when model fits in memory, model parallelism when model is too large. Databricks supports both via Horovod (data) and Megatron (model).

6. **"How do you handle cold start in recommendation systems?"**
   - Answer: For new users: use demographic features, popular items, or ask for preferences. For new items: use content features, explore via multi-armed bandit. Hybrid approach: contextual bandit combines content features with exploration. Monitor cold-start performance separately from warm-start.

7. **"Describe your strategy for A/B testing ML models."**
   - Answer: Randomized controlled trial (50/50 split), monitor guardrail metrics (latency, error rate) + business metrics (CTR, revenue). Use sequential testing (check daily) with Bonferroni correction for multiple comparisons. Implement automatic rollback if guardrails violated. Run for 2+ weeks to account for novelty effects and weekly seasonality.

8. **"How do you ensure fairness in ML models?"**
   - Answer: (1) Audit training data for bias, (2) Use fairness metrics (demographic parity, equalized odds), (3) Remove or de-bias sensitive features, (4) Post-processing adjustments (threshold tuning per group), (5) Monitor disparate impact in production, (6) Human review for high-stakes decisions.

9. **"Explain how you'd implement online learning."**
   - Answer: Incremental updates (SGD on new data), warm-start (initialize with current model), short feedback loop (minutes to hours), monitor for catastrophic forgetting (old patterns degraded), periodic full retrain (weekly) to prevent drift, use weighted sampling (recent data weighted higher).

10. **"How do you evaluate RAG systems?"**
    - Answer: Retrieval metrics (Recall@k, MRR, NDCG), generation metrics (faithfulness, groundedness, relevance), end-to-end metrics (user feedback, task completion), human evaluation (correctness, completeness, helpfulness), adversarial testing (jailbreak attempts), latency/cost monitoring.

### Scenario-Based Questions

11. **"Design an ML system for fraud detection with <100ms latency."**
    - Use framework from Scenario 2 above

12. **"Design a recommendation system for 100M users."**
    - Use framework from Scenario 1 above

13. **"Design a RAG system for enterprise Q&A."**
    - Use framework from Scenario 3 above

14. **"How would you build a real-time model monitoring system?"**
    - Streaming pipeline (Structured Streaming) to log predictions + features, compute drift metrics in real-time (sliding windows), alert on thresholds, dashboard (Databricks SQL) for visualization, integrate with PagerDuty for critical alerts.

15. **"Design an ML platform for a company with 100+ data scientists."**
    - Shared Feature Store (centralized feature repository), MLflow for experiment tracking (shared experiments across teams), Model Registry (promote models from dev → staging → prod), Unity Catalog (governance, access control), Databricks Workflows (standardized training pipelines), shared cluster policies (cost control).

### Databricks-Specific Questions

16. **"Why use Databricks over SageMaker/Vertex AI?"**
    - Answer: Unified lakehouse (data + ML in one place, no data copying), open standards (Delta Lake, MLflow, Spark), superior Spark performance (Photon 2-3x faster), Unity Catalog (centralized governance), better cost (auto-scaling, spot instances), GenAI focus (Mosaic AI, Agent Framework, Vector Search built-in).

17. **"Explain how Unity Catalog helps with ML governance."**
    - Answer: Model lineage (track model → features → data), feature lineage (track feature → tables → sources), access control (who can use which models/features), versioning (track model versions), audit logs (who accessed what when), centralized catalog (share across workspaces).

18. **"How does Databricks Feature Store prevent training-serving skew?"**
    - Answer: Single source of truth (same feature code for training + serving), automatic point-in-time correctness (use only past data at prediction time), online serving (low-latency feature lookup), automatic logging (features tracked with model in MLflow).

19. **"Describe the Databricks MLOps workflow."**
    - Answer: (1) Dev: Experiment in notebook, track with MLflow. (2) Staging: Register model in Model Registry, promote to Staging stage, run validation tests. (3) Prod: Promote to Production stage, deploy to Model Serving endpoint, monitor performance. (4) CI/CD: Automate with Databricks Workflows + GitHub Actions.

20. **"How do you use Databricks for distributed hyperparameter tuning?"**
    - Answer: Hyperopt on Spark (parallelize trials across cluster), MLflow tracking (log all trials), SpotML (use spot instances for 70% cost savings), Trials.fmin (distributed optimization), automated cluster scaling (match cluster size to trial count).

---

## 🎤 Mock Interview Script (Practice This)

**Scenario**: "Design a real-time personalization system for a news app with 50M users."

**Your Response** (think out loud):

"Great question. Let me start by clarifying some requirements to make sure I understand the problem space correctly.

*[Discovery - 5 mins]*
First, regarding the business objective—are we optimizing for engagement (click-through rate), time spent on app, or user retention? I'm guessing engagement, but wanted to confirm.

Second, what's the expected QPS for personalization? With 50M users, I'm assuming peak traffic is maybe 10K-50K requests per second during morning commute hours?

Third, what's the acceptable latency? For news recommendations, I'd expect under 200ms end-to-end, but please correct me if I'm wrong.

Fourth, what features are available? Do we have user demographics, reading history, device information, location? And for articles, do we have content features like category, author, publish time, or just IDs?

Fifth, how fresh should recommendations be? Real-time (reflecting user's last action) or can we pre-compute recommendations hourly/daily?

*[Wait for interviewer responses]*

Okay, understood. So we're optimizing for CTR, expecting 20K QPS peak, 150ms latency budget, have user reading history for the last 90 days plus demographics, and need real-time personalization (can't pre-compute).

*[Problem Definition - 3 mins]*
This is a ranking problem—given a user and a set of candidate articles, rank them by predicted CTR. I'll frame this as a pointwise learning-to-rank problem initially, though we could also use pairwise or listwise approaches.

The ML task is: Given user features (age, location, read_history) and article features (category, recency, popularity), predict P(click | user, article).

Success metric offline: NDCG@10 (we care about ordering of top 10 articles). Online: CTR in production via A/B test.

*[Architecture - 15 mins]*
Let me walk through the architecture on the whiteboard.

*[Start drawing]*

Data Layer: We'll use Delta Lake in Databricks to store:
- Bronze: Raw events (article_views, clicks, user_sessions) via Structured Streaming from Kafka
- Silver: Cleaned, joined user-article interaction history
- Gold: Aggregated features (user_genre_affinity, article_trending_score)

Feature Engineering: I'll use Databricks Feature Store for consistency. Features split into:
- Batch features (computed daily): user_avg_ctr_30d, user_favorite_categories, article_viral_score
- Real-time features (streaming): user_last_read_category, time_since_last_visit
Both stored in Feature Store, with online serving enabled for low-latency lookup.

Model Training: Two-stage approach for efficiency:
- Stage 1 (Candidate Generation): Matrix factorization or two-tower neural network to retrieve top 100 articles from 10M total. This can be pre-computed and cached.
- Stage 2 (Ranking): Gradient boosting (XGBoost or LightGBM) to rank top 100 by predicted CTR using rich features.

Why two-stage? Can't score all 10M articles in 150ms (too slow). Retrieve 100 candidates in <20ms, then rank in <50ms, leaving budget for feature retrieval (40ms) and network (40ms).

Model Serving: Deploy via Databricks Model Serving:
- Serverless endpoint for auto-scaling (20K QPS peak, but only 1K QPS off-peak)
- Feature lookup from Feature Serving (online feature store)
- Response caching (cache top articles per user segment for 5 minutes to reduce load)
- A/B testing (route 10% to new model, 90% to baseline)

Monitoring: Three-layer approach:
- Data: Monitor feature drift (has user behavior changed?)
- Model: Monitor prediction distribution (is CTR predicted still 5%, or has it dropped to 2%?)
- Business: Monitor online CTR, time-spent, bounce rate

Feedback Loop: Log all impressions + clicks, join with features (point-in-time correct), retrain daily with last 30 days of data to adapt to trending topics.

*[Trade-offs - 5 mins]*
Key trade-offs I made:
1. Two-stage vs single-stage: Single-stage (rank all 10M) would be more accurate but too slow. Two-stage sacrifices some accuracy (candidate generation might miss relevant articles) for speed.
2. Real-time vs batch features: Computing all features in real-time (e.g., user_avg_ctr_30d) would be too slow. I batch-compute heavy aggregations and only update critical features in real-time.
3. Model complexity: Deep learning (transformer-based) would be most accurate but can't meet 150ms SLA. Gradient boosting is 10x faster and 90% as accurate—good trade-off.
4. Freshness: Daily retraining is a compromise. Hourly would be more responsive to breaking news, but 10x more expensive. Daily is sufficient for most news (not breaking news alerts).

*[Deep-Dive - 10 mins]*
*[Wait for interviewer to ask follow-up]*

Example deep-dive: "How do you handle the cold start problem for new articles?"

"Great question. New articles have no interaction history, so collaborative filtering fails. I'd use a content-based approach initially:
- Extract article features: category, entities (using NLP), topic embeddings (via sentence transformers)
- For each user, compute affinity to these content features based on their reading history
- Score new article by content similarity to user's preferences
- Use multi-armed bandit (Thompson Sampling) to balance exploitation (recommend to users likely to click) vs exploration (show to diverse users to gather data)
- After 1000 impressions, we have enough data to use the collaborative model

I'd also boost new articles artificially (e.g., multiply predicted CTR by 1.5) to ensure they get exposure. This 'freshness boost' decays over 24 hours."

*[Wrap-up]*
"That's my high-level design. I'm happy to deep-dive into any component—feature engineering, model architecture, serving infrastructure, or monitoring. What would you like to explore further?"

---

## ✅ Final Checklist (Day Before Interview)

### Technical Knowledge
- [ ] Can explain Databricks lakehouse architecture (unified data + ML)
- [ ] Understand MLflow (experiment tracking, model registry, model serving)
- [ ] Understand Feature Store (training-serving consistency, online/offline)
- [ ] Understand Unity Catalog (governance, lineage, access control)
- [ ] Know RAG architecture (retrieval, augmentation, generation)
- [ ] Know agent design patterns (deterministic, agentic, hybrid)
- [ ] Familiar with Delta Lake (ACID, time travel, optimization)

### ML System Design
- [ ] Practiced 6-step framework (requirements, problem, data, training, serving, monitoring)
- [ ] Can whiteboard end-to-end ML architecture in 30 minutes
- [ ] Can articulate trade-offs (latency vs accuracy, cost vs performance)
- [ ] Know evaluation metrics (PR-AUC, NDCG, faithfulness, groundedness)
- [ ] Can discuss production challenges (drift, skew, cold start, bias)

### Databricks Platform
- [ ] Know key differentiators vs SageMaker/Vertex AI
- [ ] Understand cost optimization (autoscaling, spot, serverless, Photon)
- [ ] Familiar with Databricks Workflows (orchestration, CI/CD)
- [ ] Know Model Serving options (serverless, provisioned, A/B testing)
- [ ] Understand Vector Search (for RAG)

### Communication
- [ ] Practice thinking out loud (narrate thought process)
- [ ] Start with discovery (don't jump to solutions)
- [ ] Draw diagrams while explaining (visual communication)
- [ ] Acknowledge limitations and trade-offs
- [ ] Ask clarifying questions throughout

### Logistics
- [ ] Test video/audio setup
- [ ] Have whiteboarding tool ready (Google Slides, Excalidraw, paper)
- [ ] Prepare 3-5 questions for interviewer
- [ ] Review job description (align examples to role)
- [ ] Get good sleep night before

---

## 📚 Essential Resources (Prioritized for 6 Days)

### Must-Read (Day 1-2)
1. [AI and Machine Learning on Databricks](https://docs.databricks.com/aws/en/machine-learning/) - Official overview
2. [MLflow on Databricks](https://docs.databricks.com/aws/en/mlflow/) - Experiment tracking + model registry
3. [Feature Store Complete Guide](https://www.databricks.com/blog/what-feature-store-complete-guide-ml-feature-engineering) - Core concept

### Must-Read (Day 3)
4. [RAG on Databricks](https://docs.databricks.com/aws/en/generative-ai/retrieval-augmented-generation) - CRITICAL for 2026
5. [Agent System Design Patterns](https://docs.databricks.com/aws/en/generative-ai/guide/agent-system-design-patterns) - GenAI focus
6. [What is RAG?](https://www.databricks.com/blog/what-is-retrieval-augmented-generation) - Concept overview

### Must-Read (Day 4)
7. [ML System Design Interview Guide](https://www.tryexponent.com/blog/machine-learning-system-design-interview-guide) - Framework
8. [Feature Store & Model Serving System Design](https://system-design.space/en/chapter/feature-store-model-serving/) - Architecture patterns
9. [Model Serving Architectures on Databricks](https://medium.com/marvelous-mlops/model-serving-architectures-on-databricks-700be679eb5c) - Real-world

### Recommended (Day 5-6)
10. [MLOps Workflows on Databricks](https://docs.databricks.com/aws/en/machine-learning/mlops/mlops-workflow) - Production ML
11. [Unity Catalog Best Practices](https://docs.databricks.com/aws/en/data-governance/unity-catalog/best-practices) - Governance
12. [Databricks ML Interview Questions](https://www.datainterview.com/blog/databricks-machine-learning-engineer-interview) - Practice

---

## 🎯 Success Criteria

You'll know you're ready when you can:

1. **Whiteboard a production ML system in 30 minutes** including:
   - Data pipeline (ingestion, storage, processing)
   - Feature engineering (offline + online)
   - Model training (architecture, evaluation, tuning)
   - Model serving (inference, caching, A/B testing)
   - Monitoring (drift, performance, business metrics)

2. **Explain 3 trade-offs for every decision**:
   - "I chose X over Y because Z, but the downside is A, which we mitigate via B"

3. **Answer "why Databricks" confidently**:
   - Unified lakehouse, open standards, GenAI focus, Unity Catalog governance

4. **Design a RAG system from scratch**:
   - Document ingestion → Embedding → Vector Search → Retrieval → LLM → Evaluation

5. **Discuss production ML challenges**:
   - Training-serving skew, data drift, cold start, model monitoring, cost optimization

---

## Good luck! Remember:
- **Think out loud** - They want to see your thought process
- **Ask questions** - Clarify requirements before designing
- **Draw diagrams** - Visual communication is powerful
- **Acknowledge trade-offs** - No perfect solution, show you understand constraints
- **Stay calm** - You have 8+ years of ML experience, you've got this!

**You're ready. Trust your expertise. Go crush it! 🚀**
