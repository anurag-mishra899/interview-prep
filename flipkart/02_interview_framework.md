# AI System Design Interview Framework

## Response Structure: The DRIVER Method

Use this framework to structure your answers systematically:

### D - Define & Clarify
**Time: 3-5 minutes**

Ask clarifying questions to understand:
- **Scale**: Users, requests/sec, data volume, geographic distribution
- **Latency requirements**: Real-time (<100ms), near real-time (<1s), batch
- **Accuracy vs Speed tradeoff**: Can we compromise accuracy for speed?
- **Consistency requirements**: Strong vs eventual consistency
- **Budget constraints**: Infrastructure costs, team size
- **Existing infrastructure**: Legacy systems to integrate with

**Example Questions:**
- "What's the expected traffic? Peak vs average?"
- "What's the acceptable latency for this operation?"
- "Do we need strong consistency or is eventual consistency acceptable?"
- "Are there any existing systems we need to integrate with?"
- "What's more critical: precision, recall, or latency?"

### R - Requirements (Functional & Non-Functional)

**Functional Requirements:**
- What the system MUST do
- Core features and capabilities
- Input/output specifications
- Business logic

**Non-Functional Requirements:**
- **Availability**: 99.9%, 99.99%, 99.999%?
- **Scalability**: Horizontal scaling strategy
- **Latency**: P50, P95, P99 targets
- **Throughput**: Requests/sec, transactions/sec
- **Data consistency**: CAP theorem tradeoffs
- **Security**: Authentication, authorization, encryption
- **Observability**: Logging, metrics, tracing

### I - Initial Design (High-Level Architecture)

**Start with:**
1. Draw major components (boxes)
2. Show data flow (arrows)
3. Identify key services
4. Mark synchronous vs asynchronous paths
5. Highlight AI/ML components

**Components to consider:**
- Load balancers
- API Gateway
- Application servers
- ML model serving layer
- Caching layer
- Message queues
- Data stores (SQL, NoSQL, cache, streaming)
- Background workers

### V - Validate & Deep Dive

**Pick 2-3 critical components and go deep:**

1. **ML Model Component:**
   - Online vs offline inference
   - Model serving (TensorFlow Serving, TorchServe, custom)
   - A/B testing and experimentation
   - Model versioning and rollback
   - Feature store integration

2. **Data Store Selection:**
   - SQL vs NoSQL vs Cache vs Time-series
   - Partitioning and sharding strategy
   - Replication strategy
   - Consistency model

3. **Scaling Strategy:**
   - Horizontal vs vertical scaling
   - Auto-scaling policies
   - Load balancing algorithms
   - Circuit breakers and rate limiting

### E - Edge Cases & Failure Modes

**Discuss:**
- What happens when ML model service is down?
- How to handle traffic spikes (10x, 100x)?
- Cold start problems
- Data quality issues
- Model drift and degradation
- Cascading failures

**Mitigation strategies:**
- Circuit breakers
- Bulkheads
- Retry with exponential backoff
- Fallback mechanisms
- Health checks
- Chaos engineering

### R - Refine & Optimize

**After initial design, discuss:**
- Performance optimizations
- Cost optimizations
- Monitoring and alerting
- A/B testing strategy
- Continuous training pipeline
- Feature engineering pipeline
- Deployment strategy (blue-green, canary)

---

## Key Principles to Emphasize

### 1. Software Engineering First, ML Second
- Don't jump to ML solutions immediately
- Consider non-ML baselines
- Think about the entire system, not just the model
- Production reliability > Model accuracy

### 2. Decoupling & Modularity
- Separate concerns (data ingestion, processing, serving)
- Use message queues for async processing
- Event-driven architecture
- Microservices where appropriate

### 3. Scalability Patterns
- **Stateless services**: Easy horizontal scaling
- **Database sharding**: Partition by user_id, region, etc.
- **Caching layers**: Redis for hot data
- **CDN**: For static content and edge computing
- **Fan-out pattern**: Parallel processing

### 4. Real-Time AI Challenges
- **Inference latency**: Model optimization, quantization
- **Feature computation**: Pre-compute vs real-time
- **Model serving**: Batch vs online, GPU vs CPU
- **Cold start**: Model warm-up strategies

### 5. Data Management
- **Hot path vs Cold path**: Real-time vs batch
- **Lambda architecture**: Speed layer + batch layer
- **Kappa architecture**: Streaming-first
- **Feature stores**: Feast, Tecton for feature reuse

### 6. Observability
- **Metrics**: Latency, throughput, error rates, model metrics
- **Logging**: Structured logging, log aggregation
- **Tracing**: Distributed tracing (Jaeger, Zipkin)
- **Alerting**: SLOs, error budgets

---

## Common Pitfalls to Avoid

❌ **Jumping to implementation details too quickly**
- First get alignment on requirements and architecture

❌ **Ignoring non-functional requirements**
- Don't forget about monitoring, security, disaster recovery

❌ **Over-engineering**
- Start simple, then optimize
- "What would you do with 1000 users? 1M users? 100M users?"

❌ **Treating ML as a black box**
- Discuss model training, versioning, monitoring
- Talk about feedback loops and continuous improvement

❌ **Ignoring failure modes**
- Every component can fail
- Discuss graceful degradation

❌ **Not considering cost**
- GPU inference is expensive
- Consider CPU-optimized models, batching, caching

---

## Communication Tips

### Do:
✅ **Think out loud** - Show your reasoning process
✅ **Ask questions** - Clarify ambiguity before diving in
✅ **Draw diagrams** - Visual communication is powerful
✅ **State assumptions** - Make implicit things explicit
✅ **Consider tradeoffs** - No perfect solution, discuss pros/cons
✅ **Use numbers** - "I estimate 1000 req/s, so..."
✅ **Reference experience** - "In my previous project, we used..."

### Don't:
❌ Stay silent while thinking
❌ Make assumptions without stating them
❌ Ignore interviewer hints
❌ Get defensive about feedback
❌ Give up when stuck - talk through options

---

## Time Management (45-60 min interview)

- **0-5 min**: Clarify requirements
- **5-15 min**: High-level design
- **15-35 min**: Deep dive into critical components
- **35-40 min**: Discuss edge cases and failure modes
- **40-45 min**: Optimization and trade-offs
- **45-50 min**: Questions for interviewer

---

## Technical Depth Areas

### Distributed Systems
- Consistency models (strong, eventual, causal)
- Consensus algorithms (Raft, Paxos)
- Distributed transactions
- Message queues (Kafka, RabbitMQ, SQS)
- Service mesh (Istio, Linkerd)

### Database Design
- Indexing strategies
- Normalization vs denormalization
- Replication (leader-follower, multi-leader, leaderless)
- Partitioning (hash-based, range-based, geographic)
- CAP theorem and tradeoffs

### Caching
- Cache invalidation strategies
- Cache-aside vs write-through vs write-behind
- Distributed caching
- Cache stampede problem

### Load Balancing
- Round-robin, least connections, consistent hashing
- Health checks
- Sticky sessions
- Global vs local load balancing

### Async Processing
- Task queues (Celery, RQ)
- Event-driven architecture
- Pub-sub patterns
- Dead letter queues

### ML System Design Specifics
- Online learning vs offline learning
- Feature engineering pipeline
- Model versioning and experiments tracking (MLflow)
- A/B testing infrastructure
- Model monitoring (drift detection, performance decay)
- Multi-armed bandit vs A/B testing

---

## Sample Back-of-Envelope Calculations

**Traffic estimation:**
```
Daily Active Users: 10M
Actions per user per day: 20
Total daily requests: 10M × 20 = 200M
Requests per second (avg): 200M / 86400 ≈ 2,300 req/s
Peak traffic (3x): ≈ 7,000 req/s
```

**Storage estimation:**
```
Each transaction: 1KB
Daily transactions: 200M
Daily storage: 200M × 1KB = 200GB
Yearly storage: 200GB × 365 ≈ 73TB
With replication (3x): ≈ 219TB
```

**Bandwidth estimation:**
```
Average request size: 1KB
Average response size: 10KB
Total per request: 11KB
Peak bandwidth: 7,000 req/s × 11KB ≈ 77 MB/s ≈ 616 Mbps
```

**Model inference cost:**
```
Model inference time: 10ms
Requests per second: 2,300
Concurrent requests: 2,300 × 0.01 = 23 concurrent
With 4x buffer: ~100 concurrent connections
GPU utilization: Model load to GPU, batch processing
```

---

## Key Vocabulary to Use

**Demonstrate technical depth with these terms:**

- **Horizontal scaling** vs vertical scaling
- **Eventual consistency** vs strong consistency
- **Idempotency** for retry safety
- **Circuit breaker** for fault isolation
- **Bulkhead pattern** for resource isolation
- **Fan-out/fan-in** for parallel processing
- **CQRS** (Command Query Responsibility Segregation)
- **Event sourcing** for audit trails
- **Blue-green deployment** and canary releases
- **Feature flags** for gradual rollout
- **Backpressure** handling in streaming
- **Rate limiting** and throttling
- **SLA/SLO/SLI** for reliability
- **Multi-tenancy** for isolation
- **Data partitioning** vs sharding
- **Cold start** optimization
- **Model quantization** for inference speed
- **Batch inference** vs online inference
- **Feature store** for ML feature management

---

## Red Flags to Avoid

🚩 "I would use a neural network" - without justification
🚩 "Just use AWS Lambda" - without understanding tradeoffs
🚩 "MongoDB is web scale" - cargo cult engineering
🚩 "We don't need caching" - ignoring performance
🚩 "The model will figure it out" - ignoring engineering
🚩 "Just use microservices" - without understanding when/why
🚩 "I'd use the latest LLM" - without cost/latency analysis

---

## Summary: Your Interview Approach

1. **Listen carefully** - Understand the problem before solving
2. **Ask questions** - Clarify ambiguity upfront
3. **Start simple** - Get the basics right first
4. **Think systematically** - Use the DRIVER framework
5. **Consider tradeoffs** - Every decision has pros/cons
6. **Show depth** - Go deep on 2-3 critical areas
7. **Handle gracefully** - Discuss failures and edge cases
8. **Communicate clearly** - Think out loud, draw diagrams
9. **Reference reality** - Use real numbers and experiences
10. **Stay humble** - It's okay to say "I don't know, but here's how I'd find out"
