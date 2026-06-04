# Use Case 3: Real-Time Recommendation Feed

## Problem Statement
Design a personalized, infinitely scrolling video feed (like YouTube Shorts/Instagram Reels) that adapts to a user's interactions (likes, watch time) **in real-time**.

---

## Step 1: Clarifying Questions (Ask These!)

### Scale & Volume
- **Q**: How many daily active users (DAU)?
  - *Typical answer*: 50M DAU in India
- **Q**: Average session duration? Videos watched per session?
  - *Answer*: 20 min session, 40-60 videos (30 sec avg watch time)
- **Q**: How many videos in the catalog?
  - *Answer*: 100M videos (user-generated + brand content)
- **Q**: Video upload rate?
  - *Answer*: 1M new videos per day

### Latency & Real-Time Requirements
- **Q**: What does "real-time adaptation" mean? How fast should likes affect recommendations?
  - *Critical*: Within same session (next 5-10 videos should reflect preference)
- **Q**: Acceptable latency for loading next video?
  - *Answer*: <200ms to fetch next batch of 10 videos
- **Q**: Cold start: What to show new users with no history?
  - *Answer*: Trending videos + collaborative filtering from similar users

### Personalization Depth
- **Q**: What signals do we use? (Likes, watch time, shares, comments, skip?)
  - *Answer*: All of the above, plus implicit signals (pause, rewatch)
- **Q**: Diversity vs relevance tradeoff?
  - *Answer*: Need diversity to explore user interests, but not too random
- **Q**: Do we avoid showing the same video twice in a session?
  - *Answer*: Ideally yes, but can repeat after 24 hours

### Business Goals
- **Q**: Optimize for engagement (watch time) or monetization (ads)?
  - *Answer*: Primarily watch time, but also ad revenue
- **Q**: Content moderation? Filter NSFW, harmful content?
  - *Answer*: Yes, safety filters are critical
- **Q**: Regional/language preferences?
  - *Answer*: Yes, India has 10+ major languages

---

## Step 2: Requirements

### Functional Requirements
1. **Infinite scroll**: Always have next video ready (pre-fetch)
2. **Personalization**: Recommendations based on user history
3. **Real-time adaptation**: Likes/skips affect next 5-10 videos
4. **Cold start**: Good recommendations for new users
5. **Diversity**: Mix of relevant + exploratory content
6. **Content filtering**: Age-appropriate, safe, regional
7. **Ranking**: Order videos by predicted engagement
8. **Deduplication**: Don't show same video twice in 24h
9. **Trending**: Surface viral content quickly

### Non-Functional Requirements
1. **Latency**: 
   - P99 < 200ms for fetching next batch
   - Real-time signal processing < 100ms
2. **Throughput**: 50M DAU × 50 videos/day = 2.5B video serves/day = ~30K req/sec
3. **Availability**: 99.95% (video feed is core product)
4. **Freshness**: New videos appear in feed within 5 minutes of upload
5. **Personalization quality**: 
   - Average watch time: >30 sec per video
   - Click-through rate: >60%
6. **Scalability**: Handle traffic spikes (3x during evenings)
7. **Consistency**: Eventual consistency for user profile

---

## Step 3: High-Level Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                       CLIENT (Mobile App)                     │
│  - Infinite scroll UI                                         │
│  - Pre-fetch next 10 videos                                   │
│  - Send engagement events (like, skip, watch time)            │
└────────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
┌───────────────────────────────────────────────────────────────┐
│                      API GATEWAY / CDN                        │
│  - Rate limiting, auth                                        │
│  - CDN for video content                                      │
└────────────────────────────┬──────────────────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
┌──────────────────────┐          ┌─────────────────────────┐
│  Recommendation      │          │   Engagement Event      │
│  Service             │          │   Ingestion             │
│  (Fetch next videos) │          │   (Likes, views, etc)   │
└──────┬───────────────┘          └───────────┬─────────────┘
       │                                      │
       │                                      ▼
       │                          ┌────────────────────────┐
       │                          │  Kafka (Event Stream)  │
       │                          │  - User actions        │
       │                          │  - Video interactions  │
       │                          └───────┬────────────────┘
       │                                  │
       │                  ┌───────────────┴──────────────┐
       │                  ▼                              ▼
       │        ┌──────────────────┐        ┌──────────────────┐
       │        │  Real-time       │        │  Batch Analytics │
       │        │  Aggregator      │        │  (Spark)         │
       │        │  (Flink/Kafka    │        │  - Train models  │
       │        │   Streams)       │        │  - Update        │
       │        └────────┬─────────┘        │    embeddings    │
       │                 │                  └──────────────────┘
       │                 ▼
       │        ┌──────────────────┐
       │        │  User Profile    │
       │        │  Service         │
       │        │  (Real-time      │
       │        │   interests)     │
       │        └────────┬─────────┘
       │                 │
       ▼                 ▼
┌──────────────────────────────────────────────────────────────┐
│           RECOMMENDATION PIPELINE (3-stage)                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Stage 1: CANDIDATE GENERATION (Fast retrieval)        │ │
│  │  - Collaborative filtering (ALS, Matrix Factorization) │ │
│  │  - Content-based (video embeddings)                    │ │
│  │  - Trending/Popular                                    │ │
│  │  Output: 1000 candidate videos                         │ │
│  └────────────────────────────────────────────────────────┘ │
│                         ↓                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Stage 2: RANKING (ML-based scoring)                   │ │
│  │  - Deep learning model (TensorFlow)                    │ │
│  │  - Features: user profile, video metadata, context    │ │
│  │  - Predict: watch time, like probability              │ │
│  │  Output: Top 100 videos ranked by score               │ │
│  └────────────────────────────────────────────────────────┘ │
│                         ↓                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Stage 3: RE-RANKING (Business logic)                  │ │
│  │  - Diversity: Mix categories, creators                 │ │
│  │  - Freshness: Boost new videos                         │ │
│  │  - Safety: Filter NSFW, age-inappropriate              │ │
│  │  - Deduplication: Remove already seen                  │ │
│  │  Output: Final 20 videos                               │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────┐
│                  DATA STORES                                │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ User Profile │  │ Video Index  │  │ Embeddings      │  │
│  │ (Redis +     │  │ (Elastic-    │  │ (Vector DB:     │  │
│  │  Cassandra)  │  │  search)     │  │  Milvus/Pinecone│  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Interaction  │  │ Trending     │  │ Graph DB        │  │
│  │ History      │  │ Videos       │  │ (Neo4j)         │  │
│  │ (HBase)      │  │ (Redis)      │  │ - Social graph  │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

---

## Step 4: Deep Dive - Critical Components

### 4.1 Real-Time Event Ingestion

**User Actions to Capture:**
```json
{
  "event_type": "video_interaction",
  "user_id": "u123",
  "video_id": "v456",
  "session_id": "s789",
  "timestamp": "2026-06-04T10:30:45Z",
  "action": "like",  // or "skip", "watch", "share", "comment"
  "watch_time_sec": 28,
  "video_duration_sec": 30,
  "device": "mobile_android",
  "location": "bangalore"
}
```

**Architecture:**
```
Mobile App → API Gateway → Kafka
  ↓
Kafka Topic: user_interactions
- Partitions: 256 (for parallelism)
- Retention: 7 days (for replay)
- Throughput: 100K events/sec
  ↓
Kafka Streams / Flink (Real-time aggregation)
  ↓
User Profile Service (Update in-memory interests)
```

**Real-Time Aggregation (Flink):**
```java
// Pseudo-code
DataStream<Event> events = kafka.readFrom("user_interactions");

// Aggregate last 10 interactions per user (sliding window)
events
  .keyBy(event -> event.userId)
  .window(SlidingEventTimeWindows.of(Time.minutes(30), Time.minutes(5)))
  .aggregate(new InterestAggregator())
  .addSink(redis);  // Update user interests

// Output:
{
  "user_id": "u123",
  "recent_interests": ["tech", "comedy", "sports"],
  "liked_creators": ["c1", "c5"],
  "avg_watch_time": 32,
  "updated_at": "2026-06-04T10:31:00Z"
}
```

### 4.2 User Profile Service

**Data Structure:**
```
User Profile (in Redis + Cassandra):

Short-term (Redis, TTL 24h):
- recent_interactions: [v1, v2, v3, ...]  (last 50 videos)
- session_interests: ["tech", "comedy"]
- current_session_id: s789
- videos_seen_today: Set(v1, v2, v3, ...)

Long-term (Cassandra):
- user_id: u123
- embedding: [0.1, -0.3, 0.5, ...]  (128-dim vector)
- top_interests: {"tech": 0.8, "comedy": 0.6, ...}
- favorite_creators: [c1, c2, c3]
- language_preference: ["hindi", "english"]
- watch_history: (last 1000 videos, in HBase)
```

**Update Strategy:**
- **Real-time**: Update Redis on every interaction (within 100ms)
- **Batch**: Recompute user embeddings daily (Spark job)
- **Hybrid**: Combine long-term interests + recent session behavior

### 4.3 Candidate Generation (Stage 1)

**Goal**: Quickly retrieve ~1000 candidate videos (from 100M total)

**Method 1: Collaborative Filtering**
- **Approach**: "Users like you also watched..."
- **Model**: Matrix Factorization (ALS), Graph Neural Networks
- **Precomputation**: User embeddings + Video embeddings
- **Query**: Find videos with embedding similar to user embedding
  ```
  user_embedding = [0.1, -0.3, 0.5, ...]
  similar_videos = vector_db.query(user_embedding, top_k=500)
  ```
- **Storage**: Vector database (Milvus, Pinecone, FAISS)
- **Latency**: 20-50ms for 500 nearest neighbors

**Method 2: Content-Based Filtering**
- **Approach**: "More videos like what you watched"
- **Features**: Video tags, category, creator, audio, visual features
- **Query**: Find videos similar to recently liked videos
  ```
  recent_liked_videos = [v1, v2, v3]
  avg_embedding = mean(embeddings(recent_liked_videos))
  similar_videos = vector_db.query(avg_embedding, top_k=300)
  ```

**Method 3: Trending / Popular**
- **Approach**: "What's hot right now"
- **Computation**: 
  ```
  trending_score = (likes + shares * 2 + comments * 3) / (time_since_upload + 2)^1.5
  ```
- **Storage**: Redis sorted set (ZRANGE by score)
- **Query**: 
  ```
  redis.ZREVRANGE("trending:tech", 0, 100)  // Top 100 trending tech videos
  ```
- **Refresh**: Every 5 minutes (background job)
- **Personalization**: Filter trending by user's language + location

**Method 4: Social Graph (Follows)**
- **Approach**: "Videos from creators you follow"
- **Query**: 
  ```
  followed_creators = graph_db.get_follows(user_id)
  recent_videos = get_recent_videos(followed_creators, limit=100)
  ```

**Combining Sources:**
```python
def get_candidates(user_id):
    # Parallel fetch (fan-out)
    collaborative = get_collaborative_candidates(user_id, limit=500)
    content_based = get_content_based_candidates(user_id, limit=300)
    trending = get_trending_candidates(user_id, limit=100)
    social = get_social_candidates(user_id, limit=100)
    
    # Merge and deduplicate
    candidates = merge_unique([collaborative, content_based, trending, social])
    
    return candidates[:1000]  # Top 1000
```

**Latency Budget: 50ms total**

### 4.4 Ranking Model (Stage 2)

**Goal**: Rank 1000 candidates by predicted engagement

**Model Architecture: Two-Tower Neural Network**

```
User Tower:
  User features → Embedding layer → Dense layers → User vector (128-dim)

Video Tower:
  Video features → Embedding layer → Dense layers → Video vector (128-dim)

Interaction:
  dot_product(user_vector, video_vector) + bias → Sigmoid → Predicted engagement
```

**Features:**

**User features:**
- User ID (embedding)
- Recent interests (multi-hot encoding)
- Watch history stats (avg watch time, like rate)
- Demographics (age, gender, location)
- Device type
- Time of day / day of week
- Session duration so far

**Video features:**
- Video ID (embedding)
- Category, tags (multi-hot)
- Creator ID (embedding)
- Video duration
- Upload timestamp (freshness)
- Aggregate stats (total views, likes, watch time)
- Video quality score (resolution, production value)

**Context features:**
- Position in feed (earlier = higher CTR)
- Time since last interaction
- Diversity from previous videos

**Training Data:**
```
Positive: (user, video, watch_time > 20 sec OR liked)
Negative: (user, video, skipped OR watch_time < 5 sec)

Labels:
- Binary: engaged (1) vs not engaged (0)
- Regression: watch_time_normalized (0-1 scale)
```

**Training Pipeline:**
```
Daily Airflow DAG:
1. Extract interactions from last 7 days (Spark)
2. Feature engineering (user stats, video stats)
3. Train model (TensorFlow on GPU cluster)
4. Validate on holdout set (last day)
5. Export to TensorFlow Serving
6. A/B test (shadow mode for 24h)
7. Gradual rollout (10% → 50% → 100%)
```

**Model Serving:**
```
TensorFlow Serving cluster:
- 50 instances (GPU or CPU depending on model size)
- gRPC protocol
- Batch inference: batch size 100, max wait 10ms
- Latency: 50-100ms for ranking 1000 videos
```

**Optimization:**
- **Quantization**: INT8 instead of FP32 (4x faster)
- **Model distillation**: Teacher-student (smaller model, similar accuracy)
- **Caching**: Cache predictions for popular videos

### 4.5 Re-Ranking (Stage 3)

**Goal**: Apply business rules to final 100 videos

**Diversity Filter:**
```python
def ensure_diversity(videos, user_recent_categories):
    # Don't show >3 videos from same category consecutively
    result = []
    category_count = defaultdict(int)
    
    for video in videos:
        if category_count[video.category] < 3:
            result.append(video)
            category_count[video.category] += 1
        
        # Reset counter every 5 videos
        if len(result) % 5 == 0:
            category_count.clear()
    
    return result
```

**Freshness Boost:**
```python
def apply_freshness_boost(score, upload_time):
    hours_since_upload = (now - upload_time).hours
    
    if hours_since_upload < 1:
        boost = 1.5  # 50% boost for videos <1h old
    elif hours_since_upload < 24:
        boost = 1.2  # 20% boost for videos <24h old
    else:
        boost = 1.0
    
    return score * boost
```

**Safety Filtering:**
```python
def filter_unsafe_content(videos, user_age):
    safe_videos = []
    
    for video in videos:
        # Age-appropriate check
        if user_age < 18 and video.age_rating > 13:
            continue
        
        # Content moderation score (from ML model)
        if video.safety_score < 0.8:
            continue
        
        safe_videos.append(video)
    
    return safe_videos
```

**Deduplication:**
```python
def deduplicate(videos, user_id):
    # Check Redis set: videos seen in last 24h
    seen_videos = redis.smembers(f"seen:{user_id}")
    
    unseen = [v for v in videos if v.id not in seen_videos]
    
    # Add new videos to seen set
    for v in unseen[:20]:
        redis.sadd(f"seen:{user_id}", v.id)
        redis.expire(f"seen:{user_id}", 86400)  # 24h TTL
    
    return unseen
```

### 4.6 Video Embeddings

**Goal**: Represent videos as dense vectors for similarity search

**Approach 1: Content-Based Embeddings**
```
Video → Feature Extraction → Embedding

Visual features:
- Keyframes (sample 10 frames) → ResNet → 512-dim vector

Audio features:
- Audio spectrogram → VGGish → 128-dim vector

Text features:
- Title + Description + Tags → BERT → 768-dim vector

Combine:
  concat([visual, audio, text]) → Dense layer → 128-dim final embedding
```

**Approach 2: Collaborative Embeddings**
```
Learn embeddings from user interactions:
- Matrix Factorization (ALS)
- Graph Neural Networks (GNN)
  - Nodes: Users + Videos
  - Edges: User watched video (weighted by watch time)
  - GNN learns node embeddings
```

**Storage:**
```
Vector Database (Milvus):
- 100M video embeddings (128-dim each)
- Index: HNSW (Hierarchical Navigable Small World)
- Query latency: 20-50ms for top 500 neighbors
- Update: Add new video embeddings every hour
```

---

## Step 5: Real-Time Adaptation

**Challenge**: User likes a video → next 5-10 videos should reflect this

**Approach 1: Session-Based Context**
```python
# Maintain session state (in-memory)
session_state = {
  "user_id": "u123",
  "session_id": "s789",
  "recent_interactions": [
    {"video_id": "v1", "action": "like", "category": "tech"},
    {"video_id": "v2", "action": "watch", "watch_time": 28}
  ],
  "current_interests": ["tech", "comedy"],
  "last_updated": "2026-06-04T10:31:00Z"
}

# User likes a video
def handle_like(user_id, video_id):
    # Update session state
    session_state["recent_interactions"].append({
        "video_id": video_id,
        "action": "like"
    })
    
    # Boost related categories
    video_category = get_video_category(video_id)
    session_state["current_interests"].append(video_category)
    
    # Invalidate cached recommendations
    redis.delete(f"recs:{user_id}:{session_id}")
```

**Approach 2: Re-score Candidates in Real-Time**
```python
def get_next_batch(user_id, session_id):
    # Check cache first
    cached = redis.get(f"recs:{user_id}:{session_id}")
    if cached:
        return cached
    
    # Get candidates
    candidates = get_candidates(user_id)  # 1000 videos
    
    # Apply session-based boosting
    session_interests = get_session_interests(session_id)
    for video in candidates:
        if video.category in session_interests:
            video.score *= 1.3  # 30% boost
    
    # Re-sort by adjusted score
    candidates.sort(key=lambda v: v.score, reverse=True)
    
    # Cache for next request
    redis.setex(f"recs:{user_id}:{session_id}", 60, candidates[:20])
    
    return candidates[:20]
```

**Approach 3: Online Learning (Advanced)**
- Update user embedding in real-time (incremental update)
- Use online learning algorithms (contextual bandits)
- Trade-off: Complexity vs responsiveness

**Latency for real-time update**: <100ms
- Kafka event → Flink aggregation → Redis update: ~50ms
- Next request uses updated profile: immediate

---

## Step 6: Cold Start Problem

**New User (No History):**

**Strategy:**
1. **Onboarding quiz**: "Pick 5 interests" (tech, sports, comedy, ...)
2. **Popular videos**: Show trending in selected categories
3. **Collaborative filtering**: Find similar users (demographics, location)
4. **Fast learning**: After 5-10 interactions, personalize aggressively

**New Video (No Interactions):**

**Strategy:**
1. **Content-based**: Use video metadata, embeddings
2. **Creator-based**: Show to followers of creator
3. **Exploration**: Inject into 10% of feeds (random users)
4. **Multi-armed bandit**: Balance exploration vs exploitation

---

## Step 7: Scaling Strategy

### Handling 50M DAU

**Read Path (Recommendations):**
- Requests: 30K req/sec (peak)
- Recommendation Service: 200 instances (150 req/sec each)
- Cache: Redis cluster (16 shards), 95% hit ratio
- Database reads: 5% of 30K = 1,500 req/sec (Cassandra handles this easily)

**Write Path (Events):**
- Events: 100K events/sec
- Kafka: 256 partitions, 3 replicas
- Flink: 100 task managers (1K events/sec each)
- Redis writes: 10K updates/sec (user profiles)

**Batch Processing:**
- Daily model retraining: Spark cluster (500 workers)
- Embedding computation: GPU cluster (10 nodes)
- Time: 4-6 hours for 100M videos

### Database Sharding

**User Profiles (Cassandra):**
```
Partition key: user_id (hash-based)
Replication factor: 3
Nodes: 50 (1M users per node)
```

**Watch History (HBase):**
```
Rowkey: user_id + timestamp (reverse order)
Regions: 100
Each region: 500K users
```

**Video Metadata (Elasticsearch):**
```
Shards: 20
Replicas: 2
Documents: 100M videos
```

---

## Step 8: Failure Handling & Resiliency

### Failure Modes:

**1. Ranking Model Service Down**
- Fallback: Use trending + collaborative filtering only (skip ML ranking)
- Impact: Slightly worse personalization, but feed still works
- Recovery: Auto-restart, health checks

**2. Vector Database Slow/Down**
- Fallback: Use trending videos + social graph
- Cache: Keep popular embeddings in Redis
- Circuit breaker: Skip embedding search if latency >100ms

**3. Kafka Lag (Events delayed)**
- Monitor: Alert if lag >1 minute
- Impact: Real-time adaptation delayed, but not broken
- Mitigation: Scale Flink consumers

**4. Redis Cache Eviction**
- Impact: More database reads (slower, but functional)
- Mitigation: Increase Redis memory, tune eviction policy (LRU)

**5. Recommendation Service Overload**
- Auto-scaling: Add instances
- Short-term: Rate limiting, degrade to simpler algorithm
- Load shedding: Serve cached recommendations

---

## Step 9: Monitoring & Observability

### Metrics to Track

**Business Metrics:**
- Average watch time per video
- Session duration
- Daily active users (DAU)
- Videos watched per session
- Like rate, share rate
- User retention (day 1, day 7, day 30)

**System Metrics:**
- Recommendation latency (P50, P95, P99)
- Kafka event throughput
- Flink processing lag
- Cache hit ratio
- Model inference time
- Database query latency

**ML Metrics:**
- Click-through rate (CTR)
- Video completion rate
- Model prediction accuracy (offline)
- Diversity score (categories per session)
- Freshness score (new videos shown)

### Alerts
```
Critical:
- Recommendation Service P99 > 500ms
- Kafka lag > 5 minutes
- Model serving down
- Cache hit ratio < 70%

Warning:
- CTR drop >10%
- Average watch time drop >15%
- New video coverage <20% (not showing enough fresh content)
```

---

## Step 10: Expected Interview Questions

### Architecture Questions

1. **Q**: Why a 3-stage funnel (candidate generation → ranking → re-ranking)?
   - **A**: (1) Scalability - can't run expensive ML model on all 100M videos, (2) Latency - fast retrieval narrows to 1000, then slow ranking on fewer items, (3) Separation of concerns - retrieval for recall, ranking for precision, re-ranking for business rules.

2. **Q**: How do you ensure recommendations are diverse, not just an echo chamber?
   - **A**: (1) Diversity filter in re-ranking (max 3 videos/category consecutively), (2) Exploration: inject 10-20% random/trending videos, (3) Multi-objective optimization (relevance + diversity), (4) Penalize categories user has seen a lot recently.

3. **Q**: Real-time adaptation: How fast do likes affect the next video?
   - **A**: (1) Event ingestion to Kafka: <10ms, (2) Flink aggregation → Redis: ~50ms, (3) Next recommendation request uses updated profile: immediate. Total: Within same session, next batch reflects the like.

### Scaling Questions

4. **Q**: How would you handle 10x traffic (500M DAU)?
   - **A**: (1) Horizontal scaling: 2000 recommendation service instances, (2) More Kafka partitions (2560), more Flink workers, (3) Database sharding: 500 Cassandra nodes, (4) Regional deployments (geo-distributed), (5) Caching: Increase Redis cluster size, (6) Simplify models for scale (smaller embeddings, faster inference).

5. **Q**: Your vector database is slow. How to speed up similarity search?
   - **A**: (1) Better index: HNSW, IVF (Inverted File Index), (2) Reduce embedding dimensions (128 → 64), (3) Approximate search (trade accuracy for speed), (4) Pre-compute top candidates for popular user segments, (5) Cache frequent queries.

### ML-Specific Questions

6. **Q**: How do you handle the cold start problem for new users?
   - **A**: (1) Onboarding: ask for interests, (2) Demographic similarity: find users with similar age/location, (3) Trending: show popular videos, (4) Fast learning: after 5-10 interactions, switch to personalized, (5) Contextual bandits: balance exploration vs exploitation.

7. **Q**: Your recommendation model is biased toward popular videos. How to fix?
   - **A**: (1) Sample training data: stratified sampling (mix popular + long-tail), (2) Loss function: weight rare videos higher, (3) Diversity in retrieval: include content-based (not just collaborative), (4) Freshness boost: favor new videos, (5) Debias metrics: optimize for long-tail coverage.

8. **Q**: How do you evaluate recommendation quality offline (before deploying)?
   - **A**: (1) Holdout set: use last day's interactions, (2) Metrics: AUC, NDCG (Normalized Discounted Cumulative Gain), Precision@K, Recall@K, (3) Replay: simulate user sessions with historical data, (4) A/B test: small % of users, measure watch time, CTR, retention.

### Trade-offs Questions

9. **Q**: Personalization vs Privacy. How do you balance?
   - **A**: (1) Anonymization: aggregate at cohort level, (2) On-device ML: compute embeddings on phone, (3) Differential privacy: add noise to user data, (4) User control: let users delete history, opt-out of personalization, (5) Transparency: show why a video was recommended.

10. **Q**: Real-time vs Batch. Why not make everything real-time?
    - **A**: (1) Cost: real-time ML inference for 50M users is expensive, (2) Stability: batch models are more stable (less noise), (3) Hybrid: real-time for session context, batch for long-term interests, (4) Latency: batch pre-computation allows complex models.

### Data Questions

11. **Q**: How do you store 100M video embeddings for fast retrieval?
    - **A**: (1) Vector database: Milvus, Pinecone (optimized for similarity search), (2) Index: HNSW (sub-linear search), (3) Sharding: partition by category, (4) Compression: Product Quantization (reduce memory), (5) Tiering: hot embeddings in memory, cold in SSD.

12. **Q**: User watch history: 50M users × 1000 videos each. How to store?
    - **A**: (1) HBase: column-family DB, good for sparse data, (2) Rowkey: user_id + timestamp (reversed for recent-first), (3) Compression: Snappy, (4) TTL: Delete history >1 year old, (5) Aggregation: Store summary stats (avg watch time, top categories) separately in Cassandra.

---

## Step 11: Edge Cases to Discuss

1. **Filter bubble**: User only sees one type of content
   - Solution: Forced diversity, exploration, trending injection

2. **Viral video surge**: 1 video gets 10M views in 1 hour
   - Solution: Trending algorithm catches it, caching for popular videos

3. **Bot attacks**: Fake likes to game recommendations
   - Solution: Anomaly detection, rate limiting, user reputation score

4. **NSFW content slips through**: Safety filter fails
   - Solution: Multi-layer moderation (ML + human review), user reporting

5. **User in a new location/language**: Traveling, language change
   - Solution: Detect location change, ask for language preference, show local trending

6. **Session handoff**: User switches from phone to tablet mid-session
   - Solution: Sync session state via user_id, continue from last video

---

## Summary: Key Talking Points

✅ **Emphasize engineering over ML:**
- "3-stage funnel balances latency and accuracy"
- "Real-time event processing with Kafka + Flink"
- "Multi-level caching for sub-200ms latency"

✅ **Show production thinking:**
- "Fallback mechanisms when ML model fails"
- "A/B testing before full rollout"
- "Diversity filters to prevent echo chambers"

✅ **Discuss trade-offs:**
- "Batch for complex models, real-time for session context"
- "Collaborative filtering for personalization, content-based for cold start"
- "Eventual consistency for scalability"

✅ **Demonstrate depth:**
- Deep dive into vector databases for embeddings
- Explain two-tower neural network architecture
- Discuss real-time aggregation with Flink
