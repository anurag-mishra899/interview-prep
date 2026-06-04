# Use Case 1: Real-Time Fraud Detection Engine

## Problem Statement
Design a system that evaluates e-commerce transactions in **under 50ms** to block fraudulent purchases.

---

## Step 1: Clarifying Questions (Ask These!)

### Scale & Volume
- **Q**: How many transactions per second do we need to handle?
  - *Typical answer*: Peak during sales: 100K-500K TPS
- **Q**: What's the fraud rate historically?
  - *Typical*: 0.1-1% of transactions are fraudulent
- **Q**: Geographic distribution of users?
  - *Answer*: Pan-India, need regional data centers

### Latency & Accuracy
- **Q**: What's the acceptable false positive rate?
  - *Critical*: Too many false positives = bad UX, lost sales
- **Q**: Is 50ms P95 or P99 latency?
  - *Clarify*: Tail latency matters for user experience
- **Q**: Can we do async post-transaction analysis?
  - *Answer*: Yes, for detailed fraud investigation

### Business Logic
- **Q**: What constitutes fraud? (Account takeover, payment fraud, return fraud, promo abuse?)
  - *Answer*: All of the above, but prioritize payment fraud
- **Q**: What action should we take? (Block, challenge, flag for review?)
  - *Answer*: High confidence → block, medium → challenge, low → allow + monitor
- **Q**: Do we have historical fraud data for training?
  - *Answer*: Yes, labeled dataset available

### Integration
- **Q**: What existing systems do we integrate with?
  - *Answer*: Payment gateway, user service, inventory, order management
- **Q**: Can we delay payment processing slightly for fraud check?
  - *Answer*: Yes, but total checkout time should stay under 2-3 seconds

---

## Step 2: Requirements

### Functional Requirements
1. **Real-time scoring**: Evaluate transaction risk in <50ms
2. **Multi-signal analysis**: User behavior, device, payment, order patterns
3. **Decision engine**: Block/challenge/allow based on risk score
4. **Rule engine**: Support both ML models and business rules
5. **Feedback loop**: Capture outcomes to retrain models
6. **Manual review queue**: For borderline cases
7. **Fraud dashboard**: For fraud analysts

### Non-Functional Requirements
1. **Latency**: P99 < 50ms for risk scoring
2. **Throughput**: 500K TPS during peak
3. **Availability**: 99.99% (4 nines) - fraud system downtime = revenue loss
4. **Accuracy**: 
   - Fraud detection rate (recall): >90%
   - False positive rate: <1%
5. **Scalability**: Horizontal scaling for traffic spikes
6. **Consistency**: Eventual consistency acceptable for fraud patterns
7. **Auditability**: All decisions logged for compliance

---

## Step 3: High-Level Architecture

```
┌─────────────┐
│   Client    │
│  (Checkout) │
└──────┬──────┘
       │ 1. Transaction Request
       ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway / LB                         │
│            (Rate Limiting, Auth, Routing)                    │
└─────────────────┬───────────────────────────────────────────┘
                  │
       ┌──────────┴──────────┐
       │                     │
       ▼                     ▼
┌─────────────┐      ┌──────────────┐
│  Payment    │      │    Fraud     │
│  Service    │◄────►│   Service    │ 2. Sync fraud check
└─────────────┘      └──────┬───────┘    (< 50ms)
                            │
        ┌───────────────────┼────────────────────┐
        │                   │                    │
        ▼                   ▼                    ▼
  ┌──────────┐      ┌──────────────┐     ┌─────────────┐
  │  Rules   │      │  ML Model    │     │  Feature    │
  │  Engine  │      │  Serving     │     │  Service    │
  │ (Redis)  │      │ (TF Serving) │     │  (Cache)    │
  └──────────┘      └──────────────┘     └──────┬──────┘
                                                 │
                    ┌────────────────────────────┘
                    │
         ┌──────────┴──────────┬──────────────┐
         ▼                     ▼              ▼
  ┌─────────────┐      ┌─────────────┐  ┌──────────┐
  │  User       │      │  Device     │  │ Payment  │
  │  Profile DB │      │  Fingerprint│  │ History  │
  │  (Cassandra)│      │  (Redis)    │  │ (HBase)  │
  └─────────────┘      └─────────────┘  └──────────┘

       │ 3. Async processing (post-transaction)
       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Message Queue (Kafka)                     │
└───────┬────────────────────────────────────────────┬────────┘
        │                                            │
        ▼                                            ▼
┌──────────────────┐                        ┌────────────────┐
│  Fraud Analytics │                        │  Model         │
│  (Batch Jobs)    │                        │  Retraining    │
│  - Pattern detect│                        │  Pipeline      │
│  - Graph analysis│                        │  (Airflow)     │
└──────────────────┘                        └────────────────┘
        │
        ▼
┌──────────────────┐
│  Feature Store   │
│  (Feast/Tecton)  │
└──────────────────┘
```

---

## Step 4: Deep Dive - Critical Components

### 4.1 Fraud Service (Core Engine)

**Responsibilities:**
- Orchestrate fraud detection pipeline
- Aggregate signals from multiple sources
- Return risk score + decision in <50ms

**Implementation:**
```python
# Pseudo-code
def evaluate_transaction(transaction):
    # Parallel feature fetching (fan-out)
    with ThreadPoolExecutor() as executor:
        user_features = executor.submit(get_user_features, transaction.user_id)
        device_features = executor.submit(get_device_features, transaction.device_id)
        payment_features = executor.submit(get_payment_features, transaction.payment_method)
        order_features = executor.submit(get_order_features, transaction)
    
    # Aggregate features
    features = combine_features(
        user_features.result(),
        device_features.result(),
        payment_features.result(),
        order_features.result()
    )
    
    # Apply rules first (fast path)
    rule_result = rules_engine.evaluate(features)
    if rule_result.is_definitive:
        return rule_result
    
    # ML model scoring
    risk_score = ml_model.predict(features)
    
    # Decision logic
    if risk_score > 0.9:
        return Decision(action="BLOCK", reason="High fraud risk")
    elif risk_score > 0.6:
        return Decision(action="CHALLENGE", reason="Medium risk - require 2FA")
    else:
        return Decision(action="ALLOW", reason="Low risk")
```

**Tech Stack:**
- Language: Go (for low latency) or Java with Spring Boot
- Concurrency: Goroutines / CompletableFuture
- Circuit breaker: Hystrix / Resilience4j
- Timeouts: 40ms for feature fetching, 10ms buffer

### 4.2 Feature Service

**Key Features to Compute:**

**User Features:**
- Account age
- Number of previous orders
- Average order value
- Return rate
- Failed payment attempts (last 24h)
- Login location history
- Velocity: orders in last 1h, 24h, 7d

**Device Features:**
- Device fingerprint (browser, OS, screen size, timezone)
- Is device previously seen for this user?
- Number of accounts from this device
- IP reputation score
- VPN/Proxy detection

**Payment Features:**
- Payment method (card/UPI/wallet/COD)
- Card BIN analysis
- Is payment method previously used?
- Failed transactions on this card
- Card issuer reputation

**Order Features:**
- Cart value
- Number of items
- Product category (electronics = higher risk)
- Shipping address != billing address
- Rush delivery
- Promo code usage

**Architecture:**
```
┌─────────────────────────────────────────┐
│         Feature Service (Go)            │
│  ┌─────────────────────────────────┐   │
│  │  Feature Cache (Redis)          │   │
│  │  - TTL: 5 minutes               │   │
│  │  - Pre-computed features        │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │  Real-time Computation          │   │
│  │  - Velocity features            │   │
│  │  - Aggregations                 │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Feature Store (Feast)                  │
│  - Online store: Redis                  │
│  - Offline store: S3/Parquet            │
└─────────────────────────────────────────┘
```

**Optimization:**
- **Pre-compute** static features (user history, device reputation)
- **Cache** hot features (80% of users are repeat customers)
- **Approximate** where possible (HyperLogLog for unique counts)
- **Timeout**: If a feature service is slow, use default/cached value

### 4.3 ML Model Serving

**Model Architecture:**
- **Type**: Gradient Boosted Trees (XGBoost/LightGBM) - fast inference
- **Why not deep learning?**: GBDT has better latency (1-5ms vs 10-50ms)
- **Ensemble**: Multiple models for different fraud types
  - Payment fraud model
  - Account takeover model
  - Promo abuse model

**Serving Infrastructure:**
```
┌───────────────────────────────────────────┐
│     Model Serving Cluster                 │
│  ┌─────────────┐  ┌─────────────┐        │
│  │  Model v1.2 │  │  Model v1.3 │        │
│  │  (90% traff)│  │  (10% traff)│        │ A/B testing
│  └─────────────┘  └─────────────┘        │
│                                           │
│  - Stateless servers (easy scaling)      │
│  - Load models into memory at startup    │
│  - gRPC for low latency                  │
└───────────────────────────────────────────┘
```

**Tech:**
- **Server**: TensorFlow Serving / TorchServe / Custom (ONNX Runtime)
- **Protocol**: gRPC (faster than REST)
- **Batching**: Micro-batching (batch size 32, max wait 5ms)
- **Hardware**: CPU-optimized (cost-effective for tree models)

**Model versioning:**
- Blue-green deployment
- Shadow mode for new models (run both, compare results)
- Rollback capability

### 4.4 Rules Engine

**Why rules + ML?**
- Rules are explainable (regulatory compliance)
- Rules catch known fraud patterns instantly
- Rules as circuit breaker if ML model fails

**Example Rules:**
```
Rule 1: If (order_value > 100,000 AND account_age < 7 days) → BLOCK
Rule 2: If (device_never_seen AND shipping_address_new) → CHALLENGE
Rule 3: If (failed_payments_last_24h > 3) → BLOCK
Rule 4: If (VPN_detected AND high_risk_product) → CHALLENGE
Rule 5: If (user_on_blacklist) → BLOCK
```

**Implementation:**
- **Storage**: Redis (in-memory, sub-ms access)
- **Format**: JSON rules with conditions and actions
- **Engine**: Drools / Custom rule evaluator
- **Updates**: Hot-reload rules without service restart

### 4.5 Data Stores

**Selection criteria:**

| Data Type | Store | Why |
|-----------|-------|-----|
| User profiles | Cassandra | High write throughput, eventual consistency OK |
| Device fingerprints | Redis | In-memory, fast lookups |
| Payment history | HBase | Time-series data, range scans |
| Fraud patterns | Neo4j (graph DB) | Detect fraud rings, connected accounts |
| Rules | Redis | Low latency, frequently updated |
| Transaction logs | Kafka → S3 | Audit trail, replay capability |
| Model features | Feast (Redis + S3) | Online + offline feature store |

**Sharding strategy:**
- Cassandra: Partition by user_id hash
- HBase: Rowkey = user_id + timestamp (reverse order for recent first)
- Redis: Cluster mode, hash slot distribution

---

## Step 5: Handling 50ms Latency Constraint

### Latency Budget Breakdown:
```
Total: 50ms P99

1. Network (API Gateway → Fraud Service): 5ms
2. Feature fetching (parallel):
   - User features: 10ms
   - Device features: 8ms
   - Payment features: 8ms
   - Order features: 5ms
   (Parallel execution: max 10ms)
3. Rules engine: 2ms
4. ML model inference: 5ms
5. Decision logic: 1ms
6. Network (Fraud Service → API Gateway): 5ms
7. Buffer for variance: 12ms

Total: ~40ms avg, 50ms P99
```

### Optimizations:

**1. Parallel Feature Fetching (Fan-out)**
```go
// Fetch features concurrently
ch := make(chan FeatureResult, 4)
go fetchUserFeatures(userId, ch)
go fetchDeviceFeatures(deviceId, ch)
go fetchPaymentFeatures(paymentId, ch)
go fetchOrderFeatures(order, ch)

// Collect with timeout
timeout := time.After(10 * time.Millisecond)
for i := 0; i < 4; i++ {
    select {
    case result := <-ch:
        features.Add(result)
    case <-timeout:
        // Use cached/default features
        features.AddDefault()
    }
}
```

**2. Multi-level Caching**
- L1: Application cache (in-memory map)
- L2: Redis (distributed cache)
- L3: Database

**3. Pre-computation**
- User velocity features updated every minute (background job)
- Device reputation scores pre-computed

**4. Approximation**
- Use HyperLogLog for unique counts (trade accuracy for speed)
- Bloom filters to check "user never seen this device"

**5. Circuit Breaker**
```
If feature_service.latency > 10ms for 50% of requests:
    - Open circuit
    - Return cached features
    - Alert on-call engineer
```

---

## Step 6: Scaling Strategy

### Horizontal Scaling

**Stateless services** (easy to scale):
- Fraud Service: Auto-scale based on CPU/requests
- Feature Service: Scale independently
- Model Serving: Add more replicas

**Stateful services**:
- Redis: Cluster mode, add more shards
- Cassandra: Add more nodes, rebalance
- Kafka: Add more partitions

### Load Balancing
- **Algorithm**: Consistent hashing for sticky sessions (cache locality)
- **Health checks**: Remove unhealthy instances
- **Auto-scaling**: Scale out at 70% CPU, scale in at 30%

### Database Scaling
```
Reads >>> Writes (fraud checks are 99% reads)

Strategy:
- Read replicas for Cassandra (5 read replicas per write node)
- Redis read replicas
- Cache hit ratio target: >95%
```

---

## Step 7: Failure Handling & Resiliency

### Failure Modes:

**1. ML Model Service Down**
- Fallback: Use rules engine only
- Increase rule sensitivity temporarily
- Alert team immediately

**2. Feature Service Timeout**
- Use cached features (even if stale)
- Use default features (account age = 0 means high risk)
- Degrade gracefully (fewer features = less accurate, but still functional)

**3. Database Outage**
- Cassandra node down: Read from replica
- Redis cluster down: Fail open (allow transaction, log for async review)
- Circuit breaker: Stop hitting failing service

**4. Traffic Spike (10x normal)**
- Auto-scaling kicks in (takes 2-3 min)
- Short-term: Rate limiting, shed non-critical traffic
- Kafka buffer absorbs spike for async processing

### Circuit Breaker Pattern
```python
class CircuitBreaker:
    states = ["CLOSED", "OPEN", "HALF_OPEN"]
    
    def call_service(self):
        if self.state == "OPEN":
            return self.fallback()
        
        try:
            result = self.service.call()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            if self.failure_rate > threshold:
                self.state = "OPEN"
            return self.fallback()
```

### Bulkhead Pattern
- Isolate thread pools for different services
- If device service is slow, doesn't block user service calls

---

## Step 8: Feedback Loop & Continuous Improvement

### Online Feedback (Real-time)
```
User completes purchase
    ↓
Transaction allowed by fraud system
    ↓
(24-48 hours later)
    ↓
User disputes charge OR
Payment confirmed
    ↓
Label: Fraud=True/False
    ↓
Kafka → Feature Store
```

### Offline Analysis (Batch)
```
Daily job:
1. Analyze fraud patterns
2. Detect new fraud rings (graph analysis)
3. Update risk scores
4. Retrain models

Weekly:
1. Evaluate model performance (precision, recall, F1)
2. A/B test new models
3. Update rules based on analyst feedback
```

### Model Retraining Pipeline
```
┌─────────────────────────────────────────────────┐
│  Airflow DAG (Daily)                            │
│  1. Extract labeled transactions (last 30 days) │
│  2. Feature engineering                         │
│  3. Train model (XGBoost)                       │
│  4. Evaluate on holdout set                     │
│  5. If performance > baseline:                  │
│     - Deploy to shadow mode (1 week)            │
│     - Compare shadow vs production              │
│     - Gradual rollout (10% → 50% → 100%)        │
└─────────────────────────────────────────────────┘
```

---

## Step 9: Monitoring & Observability

### Metrics to Track

**Business Metrics:**
- Fraud detection rate (% of actual fraud caught)
- False positive rate (% of good transactions blocked)
- Revenue saved (estimated fraud blocked)
- Revenue lost (false positives)

**System Metrics:**
- Latency: P50, P95, P99 (target: <50ms)
- Throughput: Requests per second
- Error rate: 5xx errors, timeouts
- Model inference time
- Feature fetching time (per service)
- Cache hit rate

**ML Metrics:**
- Model precision/recall/F1
- Prediction distribution (drift detection)
- Feature importance changes
- Model version performance

### Alerts
```
Critical:
- P99 latency > 50ms for 5 minutes
- Error rate > 1%
- ML model service down

Warning:
- False positive rate spike (>2%)
- Cache hit rate < 90%
- Fraud detection rate drop (model degradation)
```

### Dashboards
- Real-time: Grafana + Prometheus
- Logs: ELK stack (Elasticsearch, Logstash, Kibana)
- Tracing: Jaeger (distributed tracing to debug latency)

---

## Step 10: Expected Interview Questions

### Architecture Questions
1. **Q**: Why did you choose Cassandra over MongoDB for user profiles?
   - **A**: Cassandra offers better write throughput (fraud events are write-heavy), tunable consistency, and proven horizontal scalability. For fraud detection, we can tolerate eventual consistency.

2. **Q**: How do you ensure the system stays under 50ms even during traffic spikes?
   - **A**: (1) Parallel feature fetching reduces serial latency, (2) Multi-level caching ensures fast reads, (3) Circuit breakers prevent cascading failures, (4) Auto-scaling handles load, (5) Timeout on feature services with fallback to cached values.

3. **Q**: What happens if your ML model degrades in production?
   - **A**: (1) Monitor model metrics daily (precision/recall), (2) Shadow mode new models before full rollout, (3) Fallback to rules engine if model fails, (4) A/B testing to compare models, (5) Automated retraining pipeline.

### Scaling Questions
4. **Q**: How would you handle 10x traffic (5M TPS)?
   - **A**: (1) Horizontal scaling of stateless services, (2) Database sharding (more Cassandra nodes, Redis shards), (3) Read replicas, (4) CDN for static content, (5) Rate limiting per user, (6) Regional deployments (geo-distributed).

5. **Q**: Your Redis cache goes down. What happens?
   - **A**: (1) Circuit breaker detects failures, (2) Fallback to database reads (slower but functional), (3) Application cache (L1) still serves some requests, (4) Auto-failover to Redis replica, (5) Alert on-call engineer.

### ML-Specific Questions
6. **Q**: Why XGBoost over a deep neural network for fraud detection?
   - **A**: (1) Lower latency (1-5ms vs 10-50ms), (2) Better interpretability (important for regulatory), (3) Works well with tabular data, (4) Less training data needed, (5) CPU-optimized (cost-effective).

7. **Q**: How do you handle the class imbalance problem (fraud is only 1% of transactions)?
   - **A**: (1) SMOTE for oversampling minority class, (2) Class weights in model training, (3) Use precision-recall curve instead of accuracy, (4) Stratified sampling, (5) Anomaly detection approaches.

8. **Q**: How do you detect new fraud patterns not seen during training?
   - **A**: (1) Anomaly detection models alongside supervised models, (2) Graph analysis to detect fraud rings, (3) Rules for known attack vectors, (4) Manual fraud analyst review queue, (5) Continuous model retraining with new labels.

### Trade-offs Questions
9. **Q**: How do you balance false positives (bad UX) vs false negatives (fraud loss)?
   - **A**: (1) Define business metric: cost of fraud vs cost of lost sale, (2) Three-tier approach: block/challenge/allow, (3) Lower threshold for high-value transactions, (4) A/B test different thresholds, (5) Feedback from customer support.

10. **Q**: Your fraud detection system has 99.9% availability. Is that enough?
    - **A**: No. System downtime = revenue loss + fraud exposure. Target 99.99% (4 nines). Achieve via: (1) Multi-region deployment, (2) Database replication, (3) Circuit breakers, (4) Graceful degradation (fail open with logging), (5) On-call team.

### Data Questions
11. **Q**: How do you store and query 1TB of transaction logs per day?
    - **A**: (1) Kafka for real-time streaming, (2) S3 for long-term storage (Parquet format), (3) Athena/Presto for ad-hoc queries, (4) Time-based partitioning, (5) Compression (Snappy/Gzip), (6) Data retention policy (archive after 2 years).

12. **Q**: How do you handle GDPR/data privacy for fraud detection?
    - **A**: (1) Data anonymization for analytics, (2) Encryption at rest and in transit, (3) Right to be forgotten (delete user data), (4) Audit logs for all access, (5) Data minimization (only collect what's needed).

---

## Step 11: Edge Cases to Discuss

1. **Cold start**: New user, no history
   - Solution: Use device signals, payment method, order characteristics

2. **Feature drift**: User behavior changes over time
   - Solution: Time-decay weights, continuous retraining

3. **Coordinated attacks**: Fraud rings with multiple accounts
   - Solution: Graph database (Neo4j) to detect connected accounts

4. **Model poisoning**: Fraudsters game the system
   - Solution: Combine rules + ML, anomaly detection, manual review

5. **Flash sale traffic**: 100x normal traffic in 1 minute
   - Solution: Auto-scaling, rate limiting, queue requests

6. **Payment gateway timeout**: Takes >50ms to respond
   - Solution: Async fraud check, allow transaction with post-processing

---

## Summary: Key Talking Points

✅ **Emphasize engineering over ML:**
- "We need sub-50ms latency, so parallel processing and caching are critical"
- "Circuit breakers ensure we degrade gracefully"
- "Horizontal scaling for stateless services"

✅ **Show production thinking:**
- "We need 4 nines availability because downtime = fraud exposure"
- "A/B testing for model rollout"
- "Feedback loop for continuous improvement"

✅ **Discuss trade-offs:**
- "GBDT over neural networks for latency"
- "Eventual consistency for scalability"
- "False positives hurt UX, false negatives hurt revenue - need to balance"

✅ **Demonstrate depth:**
- Deep dive into 2-3 components (feature service, ML serving, data stores)
- Discuss actual latency budgets with numbers
- Talk about specific technologies (Cassandra, Redis, Kafka, XGBoost)
