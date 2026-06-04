# Core Concepts Cheat Sheet

Quick reference for distributed systems and AI engineering concepts critical for your Flipkart interview.

---

## Concurrency & Parallelism

### Concurrency vs Parallelism
- **Concurrency**: Multiple tasks making progress (interleaved execution, single core)
- **Parallelism**: Multiple tasks executing simultaneously (multiple cores)
- **Example**: Fetching user profile + device features concurrently (parallel I/O operations)

### Patterns
```python
# Thread-based (I/O bound)
with ThreadPoolExecutor() as executor:
    future1 = executor.submit(fetch_user_data, user_id)
    future2 = executor.submit(fetch_device_data, device_id)
    user_data = future1.result()
    device_data = future2.result()

# Process-based (CPU bound)
with ProcessPoolExecutor() as executor:
    results = executor.map(process_batch, batches)

# Async/await (I/O bound, single thread)
async def fetch_all():
    user_task = asyncio.create_task(fetch_user())
    device_task = asyncio.create_task(fetch_device())
    return await asyncio.gather(user_task, device_task)
```

### Challenges
- **Race conditions**: Multiple threads accessing shared state
- **Deadlock**: Circular dependency on locks
- **Starvation**: Task never gets resources

### Solutions
- **Locks**: Mutex, Semaphore, ReadWriteLock
- **Lock-free**: Atomic operations (CAS - Compare-And-Swap)
- **Immutability**: Make data structures immutable
- **Message passing**: Avoid shared state (Actor model, Go channels)

---

## System Decoupling

### Why Decouple?
- Independent scaling
- Fault isolation
- Technology diversity
- Team autonomy

### Synchronous vs Asynchronous

**Synchronous (Request-Response):**
- REST API, gRPC
- Tight coupling
- Immediate response
- Back-pressure natural (caller blocks)

**Asynchronous (Message Queue):**
- Kafka, RabbitMQ, SQS
- Loose coupling
- Eventually consistent
- Buffer for traffic spikes

### When to Use Each?

| Scenario | Sync | Async |
|----------|------|-------|
| User-facing API (needs immediate response) | ✅ | ❌ |
| Background job (email sending) | ❌ | ✅ |
| Event notification (order placed) | ❌ | ✅ |
| Database read/write | ✅ | Depends |

### Patterns

**Service Mesh**: Istio, Linkerd
- Service discovery
- Load balancing
- Circuit breaking
- Observability

**API Gateway**: Kong, Apigee
- Rate limiting
- Authentication
- Request routing
- Protocol translation

**Event-Driven Architecture**:
- Pub-Sub (Kafka, SNS)
- Event sourcing
- CQRS (Command Query Responsibility Segregation)

---

## Horizontal Scaling

### Horizontal vs Vertical

| Aspect | Horizontal | Vertical |
|--------|-----------|----------|
| **Method** | Add more machines | Add more CPU/RAM |
| **Limit** | Nearly unlimited | Hardware limit |
| **Cost** | Linear (commodity hardware) | Exponential (high-end hardware) |
| **Downtime** | None (add without stopping) | Requires restart |
| **Complexity** | Higher (distributed systems) | Lower (single machine) |

### Stateless Services
**Key principle**: Any instance can handle any request

```
Load Balancer
  ├─ Instance 1 (stateless)
  ├─ Instance 2 (stateless)
  └─ Instance 3 (stateless)
     ↓
  Shared State (Redis, DB)
```

**Anti-pattern**: Storing session state in application memory
**Solution**: Store in Redis, use JWT tokens

### Stateful Services
**Challenge**: Requests for same entity must go to same instance

**Solutions**:
- **Sticky sessions**: Load balancer routes user to same instance (not ideal)
- **Consistent hashing**: Route based on hash(key) % num_servers
- **Sharding**: Partition data across instances

### Auto-Scaling Policies

**Metrics-based**:
```
If CPU > 70% for 5 min → add 2 instances
If CPU < 30% for 10 min → remove 1 instance
```

**Predictive**:
- Use historical patterns (traffic high at 8 PM)
- Pre-scale before spike

**Request-based**:
```
If requests/sec > 1000 → add instances
```

---

## Fan-Out Architecture

### Pattern
Single request → Multiple parallel operations → Aggregate results

```
       Request
         │
         ▼
    ┌────────┐
    │ Gateway│
    └────┬───┘
         │ (Fan-out)
    ┌────┼────┬────┐
    ▼    ▼    ▼    ▼
   S1   S2   S3   S4  (Parallel execution)
    │    │    │    │
    └────┼────┴────┘
         │ (Fan-in / Aggregate)
         ▼
      Response
```

### Use Cases
- **Fraud detection**: Fetch user + device + payment features in parallel
- **Search**: Query multiple shards in parallel, merge results
- **Recommendation**: Fetch from collaborative + content-based + trending in parallel

### Implementation

**Go (Goroutines)**:
```go
results := make(chan Result, 3)
go fetchUserFeatures(userId, results)
go fetchDeviceFeatures(deviceId, results)
go fetchPaymentFeatures(paymentId, results)

features := []Result{}
for i := 0; i < 3; i++ {
    features = append(features, <-results)
}
```

**Java (CompletableFuture)**:
```java
CompletableFuture<UserFeatures> user = CompletableFuture.supplyAsync(() -> fetchUser());
CompletableFuture<DeviceFeatures> device = CompletableFuture.supplyAsync(() -> fetchDevice());

CompletableFuture.allOf(user, device).join();
Features features = combine(user.get(), device.get());
```

### Challenges
- **Timeout**: One slow service blocks entire response
  - Solution: Set timeouts, use fallback values
- **Partial failure**: One service fails, others succeed
  - Solution: Degrade gracefully, return partial results

---

## Data Store Selection

### CAP Theorem
**You can have at most 2 of 3:**
- **Consistency**: All nodes see same data at same time
- **Availability**: Every request gets a response (success or failure)
- **Partition tolerance**: System continues despite network partition

**Real-world**:
- **CP**: Strong consistency, sacrifice availability (e.g., HBase, MongoDB)
- **AP**: High availability, eventual consistency (e.g., Cassandra, DynamoDB)
- **CA**: Not realistic (networks always partition)

### Database Types

| Type | Use Case | Examples | Pros | Cons |
|------|----------|----------|------|------|
| **SQL** | Structured data, ACID transactions | PostgreSQL, MySQL | ACID, joins, mature | Hard to scale horizontally |
| **NoSQL (Document)** | Semi-structured data | MongoDB, Couchbase | Flexible schema, easy scaling | No joins, eventual consistency |
| **NoSQL (Wide-column)** | Time-series, high write throughput | Cassandra, HBase | Massive scale, fast writes | No joins, eventual consistency |
| **Key-Value** | Caching, session store | Redis, DynamoDB | Extremely fast, simple | No complex queries |
| **Graph** | Relationships, social networks | Neo4j, Amazon Neptune | Relationship queries fast | Not general purpose |
| **Time-series** | Metrics, logs, events | InfluxDB, TimescaleDB | Optimized for time queries | Specialized use case |
| **Search** | Full-text search, filtering | Elasticsearch, Solr | Fast search, aggregations | Not source of truth |
| **Vector** | Embeddings, similarity search | Milvus, Pinecone, FAISS | Fast similarity search | Specialized use case |

### Design Patterns

**Sharding (Horizontal Partitioning)**:
```
Partition key: user_id
Shard 1: user_id hash % 4 == 0
Shard 2: user_id hash % 4 == 1
Shard 3: user_id hash % 4 == 2
Shard 4: user_id hash % 4 == 3
```

**Replication**:
- **Leader-Follower**: 1 write node, N read replicas
- **Multi-Leader**: Multiple write nodes (conflict resolution needed)
- **Leaderless**: All nodes accept writes (Cassandra, DynamoDB)

**Consistency Models**:
- **Strong**: Read sees latest write (expensive)
- **Eventual**: Reads may see stale data temporarily (scalable)
- **Causal**: Reads respect causality (middle ground)

**Indexing**:
- **B-Tree**: Good for range queries
- **Hash**: Good for exact match
- **LSM-Tree**: Good for write-heavy workloads (Cassandra, HBase)

---

## Async Processing

### Why Async?
- **Decouple**: Producer doesn't wait for consumer
- **Buffer**: Queue absorbs traffic spikes
- **Retry**: Failed tasks can be retried
- **Scaling**: Scale producers and consumers independently

### Message Queue Patterns

**Point-to-Point (Queue)**:
```
Producer → Queue → Consumer
```
- One message consumed by one consumer
- Use: Task distribution (job queue)

**Pub-Sub (Topic)**:
```
Publisher → Topic → Subscriber 1
                  → Subscriber 2
                  → Subscriber 3
```
- One message consumed by all subscribers
- Use: Event notification (order placed → email, SMS, analytics)

### Kafka Concepts

**Topic**: Category of messages (e.g., "user_events")
**Partition**: Topic split into partitions for parallelism
**Producer**: Sends messages to topic
**Consumer**: Reads messages from topic
**Consumer Group**: Multiple consumers share load (each partition consumed by one consumer in group)

```
Topic: user_events (4 partitions)

Consumer Group: analytics
  ├─ Consumer 1 → Partition 0, 1
  └─ Consumer 2 → Partition 2, 3

Consumer Group: email
  └─ Consumer 1 → Partition 0, 1, 2, 3
```

**Guarantees**:
- **At least once**: Message delivered 1+ times (may duplicate)
- **At most once**: Message delivered 0 or 1 times (may lose)
- **Exactly once**: Message delivered exactly once (expensive)

### Handling Failures

**Dead Letter Queue (DLQ)**:
```
Message → Process → Success
                 → Fail (retry 3x) → DLQ
```

**Idempotency**:
Ensure processing same message twice has no side effect
```python
def process_order(order_id):
    # Check if already processed
    if redis.exists(f"processed:{order_id}"):
        return  # Skip
    
    # Process order
    create_shipment(order_id)
    
    # Mark as processed
    redis.set(f"processed:{order_id}", 1, ex=86400)
```

**Backpressure**:
When consumer is slow, producer should slow down
- **Solution**: Monitor queue depth, alert, scale consumers

---

## Circuit Breakers

### Problem
Service A calls Service B → Service B is slow/down → Service A threads blocked → Service A cascades failure

### Circuit Breaker Pattern

**States**:
1. **CLOSED**: Normal operation, requests flow
2. **OPEN**: Too many failures, stop calling service, return error/fallback immediately
3. **HALF-OPEN**: After timeout, try one request, if success → CLOSED, if fail → OPEN

```
       Success rate > 50%
CLOSED ←──────────────────── HALF-OPEN
  │                              ↑
  │ Failure rate > 50%           │
  │                              │
  ▼                              │
 OPEN ──────────────────────────┘
       After timeout (30s)
```

### Implementation (Pseudo-code)
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=0.5, timeout=30):
        self.state = "CLOSED"
        self.failures = 0
        self.requests = 0
        self.last_failure_time = None
    
    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                return self.fallback()
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            return self.fallback()
    
    def on_success(self):
        self.requests += 1
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            self.failures = 0
            self.requests = 0
    
    def on_failure(self):
        self.failures += 1
        self.requests += 1
        self.last_failure_time = time.time()
        
        if self.failures / self.requests > self.failure_threshold:
            self.state = "OPEN"
    
    def fallback(self):
        # Return cached value, default, or error
        return None
```

### Libraries
- **Java**: Resilience4j, Hystrix (deprecated)
- **Python**: pybreaker
- **Go**: gobreaker

### Related Patterns

**Bulkhead**:
Isolate thread pools for different services
```
Thread pool for Service A: 10 threads
Thread pool for Service B: 10 threads
If Service B is slow, doesn't exhaust all threads
```

**Retry with Exponential Backoff**:
```python
def retry_with_backoff(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i == max_retries - 1:
                raise
            wait_time = 2 ** i  # 1s, 2s, 4s
            time.sleep(wait_time)
```

**Timeout**:
```python
import timeout_decorator

@timeout_decorator.timeout(5)  # 5 second timeout
def call_external_service():
    return requests.get(url)
```

---

## Resiliency

### Principles

**Design for Failure**:
- Assume everything can and will fail
- Graceful degradation
- Self-healing

**Redundancy**:
- Multiple instances
- Multiple data centers
- Multiple regions

**Isolation**:
- Failure in one component doesn't cascade
- Bulkheads, circuit breakers

### Availability Math

**Serial components**: Availability = A1 × A2 × A3
```
API Gateway (99.9%) → Service (99.9%) = 99.8%
```

**Parallel components**: Availability = 1 - (1 - A1) × (1 - A2)
```
Database (99.9%) with failover (99.9%)
= 1 - (1 - 0.999) × (1 - 0.999) = 99.9999%
```

**SLA Calculations**:
- **99.9% (3 nines)**: 43.8 min downtime/month
- **99.99% (4 nines)**: 4.38 min downtime/month
- **99.999% (5 nines)**: 26.3 sec downtime/month

### Chaos Engineering
**Practice**: Intentionally inject failures to test resilience

**Netflix Chaos Monkey**:
- Randomly kill instances
- Simulates AWS availability zone failure

**Experiments**:
- Kill random service instances
- Inject network latency
- Fill disk space
- Spike CPU usage

---

## Feedback Loops

### Monitoring Feedback Loop
```
1. Collect metrics (Prometheus)
2. Visualize (Grafana)
3. Alert (PagerDuty)
4. Investigate (logs, traces)
5. Fix (deploy patch)
6. Verify (monitor metrics)
```

### ML Feedback Loop
```
1. Model predicts (fraud score)
2. Collect outcome (was it actually fraud?)
3. Label data (fraud = True/False)
4. Retrain model (daily)
5. Deploy new model
6. A/B test (compare to baseline)
7. Rollout if better
```

**Cold Start → Warm Start → Continuous Learning**

### Observability (3 Pillars)

**1. Metrics** (What's happening?)
- Time-series data (CPU, latency, error rate)
- Aggregations (P50, P95, P99)
- Tools: Prometheus, Datadog, CloudWatch

**2. Logs** (What happened?)
- Structured logging (JSON)
- Centralized (ELK stack: Elasticsearch, Logstash, Kibana)
- Sampling (log 1% of requests)

**3. Traces** (Where's the bottleneck?)
- Distributed tracing (follow request across services)
- Tools: Jaeger, Zipkin, OpenTelemetry
- Shows latency breakdown per service

### Key Metrics

**System (RED)**:
- **Rate**: Requests per second
- **Errors**: Error rate (5xx)
- **Duration**: Latency (P50, P95, P99)

**Application (USE)**:
- **Utilization**: % of resource used (CPU, memory)
- **Saturation**: Queue depth, backlog
- **Errors**: Error rate

**Business**:
- Conversion rate
- Revenue
- User engagement

---

## Caching Strategies

### Cache Levels
```
L1: Application (in-memory, per instance)
  ↓ (miss)
L2: Distributed cache (Redis)
  ↓ (miss)
L3: Database
```

### Cache Patterns

**1. Cache-Aside (Lazy Loading)**:
```python
def get_user(user_id):
    # Try cache first
    user = cache.get(user_id)
    if user:
        return user
    
    # Cache miss, read from DB
    user = db.query(user_id)
    cache.set(user_id, user, ttl=3600)
    return user
```
- **Pros**: Only cache what's needed
- **Cons**: Cache miss penalty

**2. Write-Through**:
```python
def update_user(user):
    db.update(user)
    cache.set(user.id, user)  # Update cache immediately
```
- **Pros**: Cache always fresh
- **Cons**: Write latency (2 operations)

**3. Write-Behind (Write-Back)**:
```python
def update_user(user):
    cache.set(user.id, user)  # Update cache
    queue.enqueue(WriteToDbJob(user))  # Async DB write
```
- **Pros**: Fast writes
- **Cons**: Risk of data loss if cache fails

**4. Refresh-Ahead**:
```python
# Before TTL expires, refresh cache
if cache.ttl(key) < 60:  # Less than 1 min left
    async_refresh(key)
```

### Cache Invalidation

**Hardest problem in CS**: "There are only two hard things in Computer Science: cache invalidation and naming things."

**Strategies**:
- **TTL (Time to Live)**: Expire after X seconds
- **Event-based**: Invalidate on update (Pub-Sub)
- **Versioning**: Cache key includes version (e.g., "user:123:v2")

**Cache Stampede**:
Problem: Cache expires → 1000 requests hit DB simultaneously
```python
# Solution: Lock
def get_with_lock(key):
    value = cache.get(key)
    if value:
        return value
    
    # Try to acquire lock
    if cache.set_nx(f"lock:{key}", 1, ex=10):
        # This request rebuilds cache
        value = db.query(key)
        cache.set(key, value, ex=3600)
        cache.delete(f"lock:{key}")
    else:
        # Wait for other request to rebuild
        time.sleep(0.1)
        return get_with_lock(key)  # Retry
    
    return value
```

---

## Load Balancing

### Algorithms

**Round Robin**:
```
Request 1 → Server A
Request 2 → Server B
Request 3 → Server C
Request 4 → Server A (repeat)
```
- **Pros**: Simple, fair
- **Cons**: Doesn't consider server load

**Least Connections**:
Route to server with fewest active connections
- **Pros**: Better load distribution
- **Cons**: Requires tracking state

**Weighted Round Robin**:
```
Server A (weight 3) gets 3x traffic of Server B (weight 1)
```
- **Use**: Heterogeneous servers (different CPU/RAM)

**IP Hash (Consistent Hashing)**:
```
hash(client_ip) % num_servers → Server X
```
- **Pros**: Same client always goes to same server (sticky)
- **Cons**: Uneven distribution if clients skewed

**Least Response Time**:
Route to server with lowest latency
- **Pros**: Best user experience
- **Cons**: Complex, requires health checks

### Layer 4 vs Layer 7

**Layer 4 (Transport Layer)**:
- Routes based on IP + port
- Fast (no payload inspection)
- Protocol-agnostic
- Example: AWS NLB, HAProxy in TCP mode

**Layer 7 (Application Layer)**:
- Routes based on HTTP headers, URL path, cookies
- Slower (inspects payload)
- Protocol-specific (HTTP, gRPC)
- Example: AWS ALB, Nginx, Envoy

### Health Checks

**Active**:
Load balancer periodically pings server
```
Every 30 seconds: GET /health
If 3 consecutive failures → remove from pool
If healthy → add back to pool
```

**Passive**:
Monitor actual traffic
```
If error rate > 50% for 5 min → remove from pool
```

---

## Rate Limiting & Throttling

### Why?
- Protect against abuse (DDoS)
- Ensure fair usage (one user doesn't hog resources)
- Cost control (limit API calls)

### Algorithms

**1. Fixed Window**:
```
Allow 100 requests per minute
Window: 10:00:00 - 10:00:59
At 10:01:00, counter resets
```
- **Pros**: Simple
- **Cons**: Burst at window boundary (100 at 10:00:59, 100 at 10:01:00 = 200 in 1 sec)

**2. Sliding Window Log**:
```
Store timestamp of each request
On new request: count requests in last 60 seconds
If count < 100: allow
```
- **Pros**: Precise, no burst
- **Cons**: Memory intensive (store all timestamps)

**3. Sliding Window Counter**:
```
Weighted count from previous + current window
If 70 requests in 10:00-10:01, 30 requests in 10:01-10:02
At 10:01:30 (halfway through), effective count:
  70 * 0.5 + 30 = 65
```
- **Pros**: Memory efficient, smooth
- **Cons**: Approximate

**4. Token Bucket**:
```
Bucket starts with N tokens
Each request consumes 1 token
Tokens refill at rate R per second
If bucket empty, reject request
```
- **Pros**: Allows bursts (up to bucket size)
- **Cons**: Complex

**5. Leaky Bucket**:
```
Requests enter queue
Processed at fixed rate
If queue full, drop requests
```
- **Pros**: Smooth output rate
- **Cons**: No bursts

### Implementation (Redis)

```python
def is_allowed(user_id, limit=100, window=60):
    key = f"ratelimit:{user_id}"
    current = redis.incr(key)
    
    if current == 1:
        # First request in window, set TTL
        redis.expire(key, window)
    
    return current <= limit
```

---

## Quick Reference: When to Use What

### Data Stores
- **PostgreSQL**: Complex queries, ACID transactions, joins
- **Cassandra**: High write throughput, time-series, eventual consistency OK
- **Redis**: Caching, session store, rate limiting
- **Elasticsearch**: Full-text search, log analytics
- **Neo4j**: Relationships, graph queries (fraud rings, social network)
- **S3**: Object storage, data lake, backups

### Message Queues
- **Kafka**: High throughput, event streaming, multiple consumers
- **RabbitMQ**: Complex routing, priority queues, lower latency
- **SQS**: Simple, managed, AWS-native

### Compute
- **Kubernetes**: Container orchestration, auto-scaling
- **AWS Lambda**: Serverless, event-driven, unpredictable load
- **Spark**: Batch processing, ETL, large-scale ML training
- **Flink**: Stream processing, real-time analytics

### Monitoring
- **Prometheus + Grafana**: Metrics
- **ELK**: Logs
- **Jaeger**: Distributed tracing
- **Sentry**: Error tracking

---

## Interview Pro Tips

### Numbers to Remember
- **Latency**:
  - L1 cache: 0.5 ns
  - RAM: 100 ns
  - SSD: 150 μs
  - HDD: 10 ms
  - Network (same datacenter): 0.5 ms
  - Network (cross-continent): 150 ms

- **Throughput**:
  - Redis: 100K ops/sec (single instance)
  - Cassandra: 100K writes/sec (per node)
  - Kafka: 1M messages/sec (per broker)
  - PostgreSQL: 10K writes/sec (single instance)

- **Storage**:
  - 1M users × 1 KB/user = 1 GB
  - 1B events/day × 100 bytes/event = 100 GB/day
  - Video: 1 min 720p ≈ 50 MB

### Phrases to Use
- "Let me clarify the requirements first..."
- "Here's how I'd approach this problem..."
- "The trade-off here is X vs Y..."
- "For scale, we need to..."
- "In my previous project, I handled similar..."
- "That's a great question, let me think..."

### Red Flags to Avoid
- Jumping to solution without clarifying
- Ignoring failure modes
- Over-engineering (suggesting Kubernetes for 10 users)
- Under-engineering (suggesting single DB for 100M users)
- Not considering cost
- Forgetting monitoring/alerting
