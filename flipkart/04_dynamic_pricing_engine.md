# Use Case 2: Dynamic Pricing Engine

## Problem Statement
Design an ML-driven system that updates the prices of **millions of SKUs every hour** based on competitor pricing, supply/demand, and historical conversion rates.

---

## Step 1: Clarifying Questions (Ask These!)

### Scale & Volume
- **Q**: How many SKUs do we need to price?
  - *Typical answer*: 10 million SKUs across categories
- **Q**: What's the update frequency? (Hourly mentioned, but confirm)
  - *Answer*: Every hour for most products, every 15 min for high-velocity items
- **Q**: How many competitors do we track?
  - *Answer*: Top 5-10 competitors per category
- **Q**: Traffic volume? How many price lookups per second?
  - *Answer*: 100K-500K price reads/sec during peak

### Business Logic
- **Q**: Are there pricing constraints? (Min margin, max discount, regulatory?)
  - *Critical*: Cannot sell below cost, max discount 40%, MRP compliance (India)
- **Q**: Different pricing strategies by category?
  - *Answer*: Electronics (price-sensitive), Fashion (brand-driven), Grocery (local competition)
- **Q**: Do we consider inventory levels in pricing?
  - *Answer*: Yes - clearance pricing for old inventory
- **Q**: What about vendor contracts? (MAP - Minimum Advertised Price)
  - *Answer*: Yes, some vendors have pricing agreements

### Data Sources
- **Q**: How do we get competitor pricing?
  - *Answer*: Web scraping, APIs, third-party data providers
- **Q**: Real-time inventory data available?
  - *Answer*: Yes, updated every 5 minutes
- **Q**: Historical sales data granularity?
  - *Answer*: Transaction-level data, last 2 years

### Latency & Consistency
- **Q**: Is eventual consistency acceptable for price updates?
  - *Answer*: Yes, 5-10 min delay is fine
- **Q**: Do all systems need to show the same price simultaneously?
  - *Answer*: No, cache TTL is acceptable
- **Q**: What happens during price update? Show old or new price?
  - *Answer*: Show old price to in-flight carts, new price to new sessions

---

## Step 2: Requirements

### Functional Requirements
1. **Price computation**: Calculate optimal price for each SKU hourly
2. **Multi-factor optimization**:
   - Competitor pricing
   - Supply/demand (inventory, velocity)
   - Historical conversion rates
   - Seasonality
3. **Constraints enforcement**: Min margin, max discount, MAP agreements
4. **A/B testing**: Test pricing strategies on subsets
5. **Price update propagation**: Push to all systems (web, app, cache)
6. **Price history**: Audit trail of all changes
7. **Manual override**: Allow pricing team to set prices

### Non-Functional Requirements
1. **Scale**: 10M SKU updates per hour = ~2,800 SKU/sec
2. **Data freshness**: Competitor data <1 hour old, inventory <5 min
3. **Computation time**: Full pricing cycle completes in <30 min (to allow buffer)
4. **Read latency**: Price lookup <10ms (for product pages)
5. **Availability**: 99.9% (3 nines) - can tolerate brief outages
6. **Consistency**: Eventual consistency (5-10 min propagation acceptable)
7. **Cost**: Optimize for cloud compute (batch vs real-time tradeoff)

---

## Step 3: High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    DATA INGESTION LAYER                          │
└──────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌──────────────────┐  ┌────────────────┐
│  Competitor     │  │   Inventory      │  │  Transaction   │
│  Price Scraper  │  │   Service        │  │  Events        │
│  (Scrapy/       │  │   (Real-time)    │  │  (Kafka)       │
│   Selenium)     │  │                  │  │                │
└────────┬────────┘  └────────┬─────────┘  └────────┬───────┘
         │                    │                      │
         ▼                    ▼                      ▼
┌──────────────────────────────────────────────────────────────────┐
│                   DATA LAKE / STORAGE LAYER                      │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │ Competitor   │  │  Inventory   │  │  Historical Sales   │   │
│  │ Prices (S3)  │  │  (Redis)     │  │  (S3/Parquet)       │   │
│  └──────────────┘  └──────────────┘  └─────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┴─────────────────────┐
         ▼                                          ▼
┌────────────────────────────────┐    ┌──────────────────────────┐
│   FEATURE ENGINEERING          │    │   PRICING ML MODELS      │
│   (Apache Spark)               │    │   (Airflow + MLflow)     │
│                                │    │                          │
│ - Price elasticity             │    │ - Demand forecasting     │
│ - Competitor position          │    │ - Price optimization     │
│ - Seasonality features         │    │ - Churn prediction       │
│ - Category trends              │    │                          │
└───────────┬────────────────────┘    └────────┬─────────────────┘
            │                                  │
            └───────────┬──────────────────────┘
                        ▼
┌──────────────────────────────────────────────────────────────────┐
│              PRICING ENGINE (Batch Processing)                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Scheduler: Apache Airflow (Hourly DAG)                │     │
│  │  1. Fetch latest data (competitor, inventory, sales)   │     │
│  │  2. Run ML models (predict demand, elasticity)         │     │
│  │  3. Optimize prices (multi-objective optimization)     │     │
│  │  4. Apply business rules & constraints                 │     │
│  │  5. Generate price updates (10M SKUs)                  │     │
│  │  6. Publish to Kafka                                   │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Compute: Spark on Kubernetes (auto-scaling)                    │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
                   ┌───────────────┐
                   │  Kafka Topic  │
                   │ price_updates │
                   └───────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌──────────────┐  ┌─────────────────┐  ┌────────────────┐
│  Price DB    │  │  Search Index   │  │  CDN Cache     │
│  (Cassandra) │  │  (Elasticsearch)│  │  Invalidation  │
└──────────────┘  └─────────────────┘  └────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│                      SERVING LAYER                               │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Price Service (Go / Java)                             │     │
│  │  - Read from Cassandra (primary)                       │     │
│  │  - L1 Cache: Application (Caffeine)                    │     │
│  │  - L2 Cache: Redis (distributed)                       │     │
│  │  - SLA: <10ms P99                                      │     │
│  └────────────────────────────────────────────────────────┘     │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  API Gateway    │
                  │  (Rate Limiting)│
                  └────────┬────────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
      ┌──────────┐  ┌──────────┐  ┌──────────┐
      │   Web    │  │   App    │  │  Seller  │
      │          │  │          │  │  Portal  │
      └──────────┘  └──────────┘  └──────────┘
```

---

## Step 4: Deep Dive - Critical Components

### 4.1 Competitor Price Scraping

**Challenge**: Collect 10M competitor prices daily from multiple websites

**Architecture:**
```
┌─────────────────────────────────────────────────┐
│  Scraping Cluster (Kubernetes)                  │
│  ┌───────────────────────────────────────┐     │
│  │  Scrapy Spiders (Python)              │     │
│  │  - Distributed crawling               │     │
│  │  - Respect robots.txt                 │     │
│  │  - Rate limiting per domain           │     │
│  │  - Proxy rotation (anti-ban)          │     │
│  └───────────────────────────────────────┘     │
│  ┌───────────────────────────────────────┐     │
│  │  Selenium Grid (for JS-heavy sites)   │     │
│  │  - Headless Chrome                    │     │
│  │  - Screenshot for visual diff         │     │
│  └───────────────────────────────────────┘     │
└─────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────┐
│  Data Quality & Matching                        │
│  - Product matching (SKU → competitor product)  │
│  - Outlier detection (price too high/low)       │
│  - Confidence score                             │
└─────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────┐
│  Storage: S3 + DynamoDB                         │
│  - Raw HTML: S3 (for debugging)                 │
│  - Parsed prices: DynamoDB (quick lookup)       │
│  - Time-series: TimescaleDB                     │
└─────────────────────────────────────────────────┘
```

**Key Considerations:**
- **Product matching**: Use ML to match Flipkart SKU → competitor product
- **Data quality**: Filter outliers, require 2+ sources for confirmation
- **Freshness**: Different refresh rates (hourly for electronics, daily for books)
- **Legal**: Respect robots.txt, terms of service, rate limits

### 4.2 Pricing ML Models

**Model 1: Demand Forecasting**
- **Goal**: Predict demand at different price points
- **Input features**:
  - Historical sales at various prices
  - Seasonality (day of week, month, holidays)
  - Inventory levels
  - Competitor prices
  - Product attributes (brand, rating, reviews)
- **Model**: Time-series (Prophet, LSTM) or Gradient Boosting
- **Output**: Demand curve (expected units sold vs price)

**Model 2: Price Elasticity**
- **Goal**: Understand how price changes affect demand
- **Formula**: Elasticity = (% change in quantity) / (% change in price)
- **Segmentation**: Different elasticity for different categories
  - Electronics: High elasticity (price-sensitive)
  - Fashion: Medium elasticity (brand matters)
  - Grocery: Low elasticity (convenience)
- **Model**: Regression (Linear, Ridge) or Causal inference

**Model 3: Price Optimization**
- **Goal**: Maximize profit = (Price - Cost) × Demand
- **Objective function**: 
  ```
  maximize: Σ (price - cost) × demand(price)
  subject to:
    - price >= cost × (1 + min_margin)
    - price <= MRP
    - price <= competitor_price × (1 + max_premium)
  ```
- **Solver**: Mixed Integer Programming (PuLP, OR-Tools) or Bayesian Optimization

**Training Pipeline:**
```
Airflow DAG (Weekly):
1. Extract sales data (last 90 days)
2. Feature engineering (Spark)
3. Train demand forecasting models (per category)
4. Train elasticity models
5. Validate on holdout set
6. If performance > baseline:
   - Deploy to staging
   - A/B test (1% traffic)
   - Gradual rollout
```

### 4.3 Pricing Engine (Batch Processing)

**Hourly Workflow (Airflow DAG):**

```python
# Pseudo-code
@dag(schedule_interval="@hourly")
def pricing_pipeline():
    
    # Task 1: Data ingestion (parallel)
    competitor_prices = fetch_competitor_prices()  # S3
    inventory = fetch_inventory_snapshot()  # Redis
    sales = fetch_sales_last_24h()  # Kafka → S3
    
    # Task 2: Feature engineering (Spark)
    features = build_features(
        competitor_prices, 
        inventory, 
        sales,
        historical_conversions
    )
    
    # Task 3: ML inference (parallel by category)
    demand_forecast = predict_demand(features)  # 10M predictions, ~5 min
    elasticity = predict_elasticity(features)
    
    # Task 4: Price optimization (parallel by category)
    # Divide 10M SKUs into 100 partitions, process in parallel
    optimized_prices = []
    for partition in range(100):
        skus = get_skus_partition(partition)  # 100K SKUs
        prices = optimize_prices(
            skus=skus,
            demand=demand_forecast,
            elasticity=elasticity,
            constraints=business_rules
        )
        optimized_prices.append(prices)
    
    # Task 5: Apply business rules
    final_prices = apply_constraints(optimized_prices)
    
    # Task 6: Diff computation (only changed prices)
    price_changes = compute_diff(current_prices, final_prices)
    
    # Task 7: Publish to Kafka
    publish_price_updates(price_changes)  # ~500K changes per hour
    
    # Task 8: Monitor & alert
    validate_price_changes(price_changes)
```

**Compute Resources:**
- Spark cluster: 50-100 workers (auto-scaling)
- Job completion: <30 minutes (to allow buffer within 1 hour)
- Cost optimization: Use spot instances for batch jobs

### 4.4 Price Update Propagation

**Challenge**: Update 500K prices across multiple systems in near real-time

**Architecture:**
```
Kafka Topic: price_updates
Partitions: 64 (for parallelism)
Message format:
{
  "sku_id": "ELEC123",
  "old_price": 9999,
  "new_price": 8999,
  "effective_at": "2026-06-04T10:00:00Z",
  "reason": "competitor_match"
}
```

**Consumers:**

**1. Price Database (Cassandra) - Source of Truth**
```python
# Consumer group: price-db-writer
# Throughput: 10K writes/sec
def consume_price_update(message):
    cassandra.execute("""
        UPDATE prices
        SET current_price = ?, updated_at = ?
        WHERE sku_id = ?
    """, [message.new_price, now(), message.sku_id])
    
    # Also write to price history table
    cassandra.execute("""
        INSERT INTO price_history (sku_id, price, changed_at, reason)
        VALUES (?, ?, ?, ?)
    """, [message.sku_id, message.new_price, now(), message.reason])
```

**2. Search Index (Elasticsearch) - For filtering/sorting**
```python
# Consumer group: search-indexer
# Throughput: 5K updates/sec
def consume_price_update(message):
    es.update(
        index="products",
        id=message.sku_id,
        body={"doc": {"price": message.new_price}}
    )
```

**3. Cache Invalidation (Redis)**
```python
# Consumer group: cache-invalidator
# Throughput: 20K invalidations/sec
def consume_price_update(message):
    redis.delete(f"price:{message.sku_id}")
    # Also invalidate category caches
    redis.delete(f"category:{message.category_id}:prices")
```

**4. CDN Cache Invalidation**
```python
# Consumer group: cdn-invalidator
# Batch invalidations (every 5 min, max 3000 URLs)
def consume_price_update(message):
    cdn.invalidate(f"/product/{message.sku_id}")
```

**5. Analytics & Monitoring**
```python
# Consumer group: price-analytics
def consume_price_update(message):
    # Track price change magnitude
    change_pct = (message.new_price - message.old_price) / message.old_price
    
    if abs(change_pct) > 0.2:  # >20% change
        alert_pricing_team(message)
    
    # Log to analytics
    write_to_data_warehouse(message)
```

### 4.5 Price Serving (Read Path)

**Goal**: Serve price lookups in <10ms P99

**Architecture:**
```
Request: GET /api/price?sku_id=ELEC123

1. L1 Cache: Application (Caffeine, in-memory)
   - Hit ratio: 60-70%
   - Latency: <1ms
   - TTL: 5 minutes

2. L2 Cache: Redis (distributed)
   - Hit ratio: 95% (combined with L1)
   - Latency: 2-3ms
   - TTL: 10 minutes

3. Database: Cassandra (if cache miss)
   - Latency: 5-8ms
   - Partition key: sku_id
   - Read consistency: ONE (fast, eventual)

Total P99 latency: <10ms
```

**Price Service Implementation (Go):**
```go
func GetPrice(skuID string) (Price, error) {
    // L1: Application cache
    if price, found := appCache.Get(skuID); found {
        metrics.CacheHit("L1")
        return price, nil
    }
    
    // L2: Redis
    price, err := redis.Get(ctx, "price:" + skuID).Result()
    if err == nil {
        metrics.CacheHit("L2")
        appCache.Set(skuID, price, 5*time.Minute)
        return price, nil
    }
    
    // L3: Cassandra
    metrics.CacheMiss()
    price, err := cassandra.Query(
        "SELECT current_price FROM prices WHERE sku_id = ?",
        skuID,
    ).Scan(&price)
    
    if err != nil {
        // Fallback: Return last known price from stale cache
        return getStalePrice(skuID), nil
    }
    
    // Warm caches
    redis.Set(ctx, "price:" + skuID, price, 10*time.Minute)
    appCache.Set(skuID, price, 5*time.Minute)
    
    return price, nil
}
```

**Optimization:**
- **Pre-warming**: Populate caches for popular SKUs before they expire
- **Batch API**: `GET /api/prices?sku_ids=A,B,C` (mget from Redis)
- **GraphQL**: Client requests only needed fields

---

## Step 5: Scaling Strategy

### Handling 10M SKUs

**Batch Processing:**
- **Partition by category**: Electronics, Fashion, Grocery (parallel processing)
- **Spark parallelism**: 100 executors, each processing 100K SKUs
- **Incremental updates**: Only recompute prices for SKUs with changed inputs

**Data Sharding:**
```
Cassandra:
- Partition key: sku_id (hash-based)
- Replication factor: 3
- Nodes: 20 (500K SKUs per node)

Redis:
- Cluster mode: 16 shards
- Each shard: 625K SKUs
- Eviction policy: LRU (keep hot data)
```

### Handling Read Traffic (500K req/sec)

**Horizontal scaling:**
- Price Service: 100 instances (5K req/sec each)
- Load balancer: HAProxy / AWS ALB
- Auto-scaling: CPU >70% → add instances

**Cache strategy:**
- 95% cache hit ratio
- Only 5% hits database (25K req/sec)
- Cassandra can handle 50K reads/sec (headroom)

---

## Step 6: Failure Handling & Resiliency

### Failure Modes:

**1. Pricing DAG Fails Mid-Execution**
- Rollback: Keep old prices (safe default)
- Alerting: Page on-call engineer
- Retry: Airflow retries with exponential backoff
- Fallback: Skip optimization, use rule-based pricing

**2. Kafka Lag (Price updates delayed)**
- Monitor: Consumer lag >10 minutes → alert
- Scale: Add more consumer instances
- Impact: Some users see stale prices (acceptable)

**3. Cassandra Node Down**
- Replication: Read from replica nodes (RF=3)
- Consistency: Use ONE (eventual consistency OK)
- Repair: Cassandra auto-repairs

**4. Competitor Scraping Blocked**
- Retry: Rotate proxies, user agents
- Fallback: Use stale competitor data (1-2 days old)
- Alternative: Third-party data providers

**5. Price Change Too Large (Bug Detection)**
```python
def validate_price_change(old_price, new_price):
    change_pct = abs(new_price - old_price) / old_price
    
    if change_pct > 0.5:  # 50% change
        # Block update, alert team
        raise PriceAnomalyException("Price change too large")
    
    if new_price < cost * 1.05:  # Below min margin
        # Override with min price
        new_price = cost * 1.05
    
    return new_price
```

---

## Step 7: A/B Testing for Pricing

**Goal**: Test new pricing strategies without risking revenue

**Setup:**
```
Experiment: "Higher margin for premium brands"
- Control: 90% of users, current algorithm
- Variant: 10% of users, new algorithm
- Metric: Revenue per user, conversion rate
- Duration: 2 weeks
```

**Implementation:**
```python
def get_price_for_user(sku_id, user_id):
    # Hash user_id to assign to experiment group
    group = hash(user_id) % 100
    
    if group < 10:  # 10% in variant
        price = get_price_from_db(sku_id, version="v2")
        log_experiment_exposure(user_id, sku_id, "variant")
    else:  # 90% in control
        price = get_price_from_db(sku_id, version="v1")
        log_experiment_exposure(user_id, sku_id, "control")
    
    return price
```

**Analysis:**
- Track: Revenue, units sold, conversion rate, margin
- Statistical significance: t-test, confidence intervals
- Decision: Rollout if variant shows +2% revenue with p<0.05

---

## Step 8: Monitoring & Observability

### Metrics to Track

**Business Metrics:**
- Revenue impact (before/after pricing updates)
- Gross margin %
- Conversion rate (by category, price bucket)
- Competitor price gap (Flipkart vs competition)
- Inventory turnover rate

**System Metrics:**
- Pricing DAG execution time (should be <30 min)
- Price update lag (time from compute to live)
- Price Service latency (P50, P95, P99)
- Cache hit ratio (L1, L2)
- Kafka consumer lag

**ML Metrics:**
- Demand forecast accuracy (MAPE, RMSE)
- Price optimization convergence time
- Model drift (feature distributions)

### Alerts
```
Critical:
- Pricing DAG failed
- Price Service P99 > 50ms
- Cache hit ratio < 80%
- >1000 SKUs with price = 0 (bug)

Warning:
- Competitor data >2 hours old
- Pricing DAG took >40 min
- Kafka lag > 10 min
```

### Dashboards
- **Real-time**: Grafana (price changes/min, cache hit rate)
- **Business**: Tableau (revenue impact, margin trends)
- **ML**: MLflow (model performance over time)

---

## Step 9: Expected Interview Questions

### Architecture Questions
1. **Q**: Why batch processing (hourly) instead of real-time pricing?
   - **A**: (1) Cost - real-time ML inference for 10M SKUs is expensive, (2) Stability - hourly updates prevent price whiplash (bad UX), (3) Computational complexity - optimization takes 20-30 min, (4) Business preference - prices should be stable within a session.

2. **Q**: How do you ensure all users see the same price at the same time?
   - **A**: We don't enforce strong consistency (too expensive). Instead: (1) Cache TTL ensures prices converge within 10 min, (2) Prices are versioned by timestamp, (3) In-flight carts honor the price at cart-add time, (4) Price updates are atomic per SKU.

3. **Q**: What if your pricing model suggests a price below cost?
   - **A**: (1) Constraint enforcement in optimization (price >= cost × 1.05), (2) Post-processing validation layer, (3) Alert pricing team for manual review, (4) Fallback to cost-plus pricing for that SKU.

### Scaling Questions
4. **Q**: How would you reduce the pricing cycle from 1 hour to 15 minutes?
   - **A**: (1) Incremental updates - only recompute SKUs with changed inputs (inventory, competitor prices), (2) Approximate optimization - warm start from previous solution, (3) More Spark workers (cost tradeoff), (4) Pre-computed demand models, (5) Simpler models for non-critical categories.

5. **Q**: Competitor scraping is slow and unreliable. How to handle this?
   - **A**: (1) Use third-party data providers (Priceonomics, Apify), (2) Crowd-source from users (price match claims), (3) Cache stale data (1-2 day old competitor prices still useful), (4) Fallback to demand-based pricing if no competitor data.

### ML-Specific Questions
6. **Q**: How do you handle seasonal products (e.g., winter jackets)?
   - **A**: (1) Seasonality features in demand forecasting (month, week of year), (2) Separate models for seasonal vs evergreen products, (3) Use historical data from previous seasons, (4) Cold start: Look at similar products.

7. **Q**: Your demand forecast is wrong. How do you detect and fix it?
   - **A**: (1) Monitor forecast vs actual sales daily, (2) Compute MAPE (Mean Absolute Percentage Error), (3) If MAPE > 20% for a category → trigger retraining, (4) Ensemble models to reduce variance, (5) Online learning to adapt quickly.

8. **Q**: How do you prevent price wars with competitors?
   - **A**: (1) Don't always match lowest price - optimize profit, not market share, (2) Set minimum margins (never sell below cost + X%), (3) Differentiate on value (bundling, faster delivery), (4) Strategic categories: match on electronics, premium on fashion.

### Trade-offs Questions
9. **Q**: Eventual consistency means some users see different prices. Is that acceptable?
   - **A**: Yes, because: (1) Price delta is small (typically <5%), (2) Users in carts see consistent price (locked at cart-add), (3) Cache TTL is short (10 min), (4) Alternative is strong consistency (expensive, slow).

10. **Q**: How do you balance revenue maximization vs customer trust?
    - **A**: (1) Price stability - avoid frequent drastic changes, (2) Transparency - show "price dropped" badges, (3) A/B test pricing strategies to measure long-term impact on retention, (4) Price match guarantees for loyalty, (5) Dynamic discounts, not dynamic base prices (perceived fairness).

### Data Questions
11. **Q**: How do you match Flipkart SKUs to competitor products?
    - **A**: (1) Exact match: UPC/EAN barcodes, (2) Fuzzy match: Product title + brand + specs (ML text similarity), (3) Image matching: Visual similarity for fashion, (4) Manual curation for top 10K SKUs, (5) Confidence scores - only use high confidence matches (>0.8).

12. **Q**: How do you store 2 years of price history for 10M SKUs?
    - **A**: (1) Time-series DB (TimescaleDB, InfluxDB), (2) Compression (Parquet format in S3), (3) Aggregations - daily avg instead of hourly for old data, (4) Partitioning by date, (5) Cold storage for >1 year old data (Glacier).

---

## Step 10: Edge Cases to Discuss

1. **Flash sale**: Temporary price drop, then revert
   - Solution: Manual override + scheduled revert

2. **Competitor out of stock**: Shows low price but can't fulfill
   - Solution: Weight competitor prices by availability

3. **Currency fluctuation**: Import costs change
   - Solution: Daily cost update from procurement system

4. **Vendor MAP violation**: Flipkart prices below minimum advertised price
   - Solution: Hard constraint in optimization + alerts

5. **Cart price vs checkout price**: User added item 2 hours ago, price changed
   - Solution: Honor cart price for 24 hours (better UX)

6. **Regional pricing**: Different prices for different cities
   - Solution: Add region to partition key, separate price per (SKU, region)

---

## Summary: Key Talking Points

✅ **Emphasize system design over ML:**
- "Batch processing is more cost-effective than real-time for 10M SKUs"
- "Multi-level caching ensures <10ms read latency"
- "Kafka decouples pricing engine from serving systems"

✅ **Show production thinking:**
- "Constraint enforcement prevents selling below cost"
- "A/B testing before rolling out new pricing strategies"
- "Graceful degradation when competitor data is stale"

✅ **Discuss trade-offs:**
- "Hourly updates balance cost and freshness"
- "Eventual consistency for scalability"
- "Approximate optimization for speed"

✅ **Demonstrate depth:**
- Deep dive into batch processing (Spark, Airflow)
- Discuss ML models (demand forecasting, elasticity)
- Explain cache propagation strategy
