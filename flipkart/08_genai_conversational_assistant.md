# GenAI Use Case 1: Conversational Shopping Assistant (SLAP)

## Problem Statement
Design an **LLM-powered conversational shopping assistant** that helps users discover and purchase products through natural language dialogue. Users should be able to have multi-turn conversations, get personalized recommendations, and complete purchases - all within a chat interface.

**Real-world Context**: Flipkart is launching "SLAP" (Shop Like a Pro) in 2026 as their next-generation conversational AI assistant.

---

## Step 1: Clarifying Questions (Ask These!)

### Scale & Volume
- **Q**: How many daily active users (DAU) do we expect?
  - *Answer*: 10M DAU initially, scaling to 50M
- **Q**: Average conversation length? Messages per session?
  - *Answer*: 5-10 message exchanges per conversation
- **Q**: Query volume per second?
  - *Answer*: 50K conversations concurrently during peak

### Latency & User Experience
- **Q**: What's the acceptable response latency?
  - *Critical*: First token <1 sec, full response <3 sec (streaming)
- **Q**: Should responses stream (token-by-token) or send complete?
  - *Answer*: Stream for better perceived latency
- **Q**: Offline mode or always connected?
  - *Answer*: Requires internet connection

### LLM & Data
- **Q**: Can we use external LLM APIs (OpenAI, Anthropic) or must be self-hosted?
  - *Critical*: Privacy considerations, data residency (India)
  - *Answer*: Prefer self-hosted for data privacy, but consider hybrid
- **Q**: What data can the LLM access?
  - *Answer*: Product catalog, user profile, order history, reviews
- **Q**: Language support?
  - *Answer*: English + 5 major Indian languages (Hindi, Tamil, Telugu, etc.)

### Personalization & Context
- **Q**: How personalized should responses be?
  - *Answer*: Should use past orders, preferences, browsing history
- **Q**: Should it remember conversation across sessions?
  - *Answer*: Yes, maintain long-term memory per user
- **Q**: Integration with existing systems (cart, checkout)?
  - *Answer*: Yes, should add to cart, place orders

### Safety & Quality
- **Q**: How do we handle hallucinations (LLM making up products)?
  - *Critical*: Must only recommend real, in-stock products
- **Q**: Content moderation requirements?
  - *Answer*: No profanity, NSFW, no competitive product mentions
- **Q**: What if LLM doesn't know the answer?
  - *Answer*: Gracefully hand off to human support

---

## Step 2: Requirements

### Functional Requirements
1. **Natural language understanding**: Parse user intents (search, compare, recommend, order)
2. **Product search**: Retrieve relevant products from catalog (100M SKUs)
3. **Multi-turn dialogue**: Maintain conversation context across messages
4. **Personalization**: Use user profile, history for tailored responses
5. **Actions**: Add to cart, place order, track shipment
6. **Explanations**: Explain why products are recommended
7. **Comparisons**: Compare multiple products side-by-side
8. **Multilingual**: Support 5+ Indian languages

### Non-Functional Requirements
1. **Latency**:
   - First token (TTFT): <1 sec
   - Full response: <3 sec for 200 tokens
   - Streaming: 30-50 tokens/sec
2. **Throughput**: 50K concurrent conversations
3. **Availability**: 99.95% (conversational UI is core product)
4. **Quality**:
   - Task completion rate: >70%
   - User satisfaction (CSAT): >4.0/5.0
   - Hallucination rate: <1%
5. **Cost**: <$0.05 per conversation (token costs)
6. **Scalability**: Handle 10x traffic spikes
7. **Safety**: 99.5% of responses pass content moderation

---

## Step 3: High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENT (Mobile App / Web)                    │
│  - Chat UI with streaming responses                             │
│  - Quick action buttons (Add to cart, Buy now)                  │
│  - Image/voice input capabilities                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API GATEWAY / CDN                            │
│  - WebSocket for streaming                                      │
│  - Rate limiting per user                                       │
│  - Auth & session management                                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              CONVERSATIONAL AI ORCHESTRATOR                     │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  LangChain / LlamaIndex Agent                             │ │
│  │  - Intent classification                                  │ │
│  │  - Tool selection (search, cart, order)                   │ │
│  │  - Response generation orchestration                      │ │
│  └───────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┬───────────────┐
         ▼               ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│ INTENT       │ │  RETRIEVAL   │ │  ACTION     │ │  SAFETY      │
│ CLASSIFIER   │ │  (RAG)       │ │  EXECUTOR   │ │  FILTER      │
└──────────────┘ └──────────────┘ └─────────────┘ └──────────────┘
         │               │               │               │
         └───────────────┴───────────────┴───────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LLM SERVING LAYER                            │
│  ┌─────────────────────┐  ┌──────────────────────────────┐    │
│  │  LLM Router         │  │  Model Servers               │    │
│  │  - Route by task    │  │  ┌────────────────────────┐  │    │
│  │  - Load balance     │  │  │ Llama-3-70B (General)  │  │    │
│  │  - Cache responses  │  │  │ (vLLM, 20 GPU nodes)   │  │    │
│  │                     │  │  └────────────────────────┘  │    │
│  │                     │  │  ┌────────────────────────┐  │    │
│  │                     │  │  │ Mistral-7B (Fast)      │  │    │
│  │                     │  │  │ (TensorRT-LLM, 5 nodes)│  │    │
│  │                     │  │  └────────────────────────┘  │    │
│  └─────────────────────┘  └──────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┬────────────────┐
         ▼               ▼               ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌────────────┐ ┌──────────────┐
│  VECTOR DB   │ │  USER PROFILE│ │  PRODUCT   │ │  CONV STATE  │
│  (Milvus)    │ │  (Cassandra) │ │  CATALOG   │ │  (Redis)     │
│              │ │              │ │  (Elastic) │ │              │
│ - Product    │ │ - Prefs      │ │            │ │ - History    │
│   embeddings │ │ - History    │ │            │ │ - Context    │
└──────────────┘ └──────────────┘ └────────────┘ └──────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ACTION EXECUTION LAYER                         │
│  ┌────────────┐  ┌──────────────┐  ┌────────────────────┐     │
│  │  Cart API  │  │  Order API   │  │  Tracking API      │     │
│  └────────────┘  └──────────────┘  └────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│               MONITORING & ANALYTICS                            │
│  - Conversation quality metrics (task completion, CSAT)         │
│  - LLM performance (latency, token usage, cost)                 │
│  - Safety metrics (hallucinations, moderation flags)            │
│  - A/B testing framework                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 4: Deep Dive - Critical Components

### 4.1 Conversational AI Orchestrator (Agent)

**Responsibilities**:
- Parse user message → determine intent
- Decide which tools to call (search, cart, order)
- Orchestrate multi-step workflows
- Generate natural language responses

**Implementation** (LangChain Agent):

```python
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool

# Define tools
tools = [
    Tool(
        name="ProductSearch",
        func=product_search_tool,
        description="Search for products. Input: natural language query. Returns: list of relevant products."
    ),
    Tool(
        name="AddToCart",
        func=add_to_cart_tool,
        description="Add product to user's cart. Input: product_id. Returns: confirmation."
    ),
    Tool(
        name="GetUserProfile",
        func=get_user_profile_tool,
        description="Get user's past orders and preferences. Input: user_id. Returns: profile data."
    ),
    Tool(
        name="CompareProducts",
        func=compare_products_tool,
        description="Compare multiple products. Input: list of product_ids. Returns: comparison table."
    )
]

# System prompt
system_prompt = """You are Flipkart's shopping assistant. Help users find and buy products.

RULES:
1. Only recommend products that exist in the catalog (use ProductSearch tool)
2. Be concise - max 3 sentences per response
3. Always ask if user wants to add to cart after showing products
4. Use user's profile to personalize recommendations
5. If unsure, say "Let me check" and use appropriate tool

CONVERSATION CONTEXT:
{conversation_history}

USER PROFILE:
{user_profile}
"""

# Create agent
agent = create_openai_functions_agent(llm, tools, system_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Execute
def handle_message(user_message, user_id, conversation_id):
    # Get conversation context
    conversation_history = get_conversation_history(conversation_id)
    user_profile = get_user_profile(user_id)
    
    # Run agent
    response = agent_executor.invoke({
        "input": user_message,
        "conversation_history": conversation_history,
        "user_profile": user_profile
    })
    
    # Save to conversation history
    save_message(conversation_id, role="user", content=user_message)
    save_message(conversation_id, role="assistant", content=response["output"])
    
    return response["output"]
```

**Agent Patterns**:

**ReAct (Reasoning + Acting)**:
```
User: "I need running shoes under 3000 rupees"

LLM Reasoning:
Thought: User wants running shoes with a price filter
Action: ProductSearch
Action Input: "running shoes price < 3000"
Observation: [Found 50 products]

Thought: I should show top 3 most popular ones
Final Answer: "I found great running shoes under ₹3000! Here are top picks:
1. Nike Revolution (₹2,799) - Best seller
2. Adidas Tensor (₹2,499) - Great cushioning
3. Puma Pacer (₹1,999) - Budget-friendly

Would you like to see details or add any to cart?"
```

**Tool Selection**:
```python
def select_tools(user_intent):
    intent_to_tools = {
        "search": ["ProductSearch", "GetUserProfile"],
        "compare": ["ProductSearch", "CompareProducts"],
        "order": ["AddToCart", "PlaceOrder", "GetAddress"],
        "track": ["GetOrderStatus"],
        "recommend": ["ProductSearch", "GetUserProfile", "GetSimilarProducts"]
    }
    return intent_to_tools.get(user_intent, ["ProductSearch"])
```

### 4.2 Intent Classification

**Purpose**: Fast pre-classification to route to appropriate handlers

**Approach 1: Lightweight Model (Fast)**
```python
# Fine-tuned BERT for intent classification
# Latency: 20-50ms

intents = [
    "product_search",      # "I need a laptop"
    "product_compare",     # "Compare iPhone 15 vs Samsung S24"
    "add_to_cart",        # "Add this to cart"
    "place_order",        # "I want to buy this"
    "track_order",        # "Where is my order?"
    "product_qa",         # "Does this have warranty?"
    "recommend",          # "Suggest something for me"
    "chitchat",           # "How are you?"
    "complaint"           # "Product was damaged"
]

def classify_intent(message):
    embeddings = bert_model.encode(message)
    intent_logits = classifier(embeddings)
    top_intent = intents[intent_logits.argmax()]
    confidence = softmax(intent_logits).max()
    
    if confidence < 0.7:
        return "unclear", confidence
    return top_intent, confidence
```

**Approach 2: LLM-based (Accurate but slower)**
```python
# Use LLM with structured output (JSON mode)
# Latency: 200-500ms

system_prompt = """Classify user intent into one of:
- product_search
- add_to_cart
- track_order
- recommend

Return JSON: {"intent": "...", "entities": {...}}
"""

response = llm.generate(
    system=system_prompt,
    user_message=message,
    response_format="json"
)
```

**Hybrid Approach** (Best):
- Use lightweight classifier first
- If confidence < 0.7, escalate to LLM
- 90% of queries handled by fast classifier

### 4.3 Retrieval (RAG) Pipeline

**Challenge**: Retrieve relevant products from 100M SKU catalog based on natural language query

**Architecture**:
```
User Query: "Blue formal shirts under 2000"
     │
     ▼
┌─────────────────────────────────────┐
│  Query Preprocessing                │
│  - Intent: product_search           │
│  - Entities: color=blue,            │
│    category=shirt, price<2000       │
│  - Query expansion                  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Hybrid Retrieval                   │
│  ┌───────────────────────────────┐  │
│  │ Dense Retrieval (Vector DB)   │  │
│  │ - Encode query → embedding    │  │
│  │ - Find top 500 similar items  │  │
│  │ - Cosine similarity search    │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ Sparse Retrieval (BM25)       │  │
│  │ - Keyword matching            │  │
│  │ - Elasticsearch               │  │
│  │ - Top 500 results             │  │
│  └───────────────────────────────┘  │
│                │                     │
│                ▼                     │
│  ┌───────────────────────────────┐  │
│  │ Merge & Deduplicate           │  │
│  │ - Reciprocal Rank Fusion      │  │
│  │ - Output: 1000 candidates     │  │
│  └───────────────────────────────┘  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Filtering                          │
│  - Apply price filter (<2000)       │
│  - In-stock only                    │
│  - Region-specific (delivery)       │
│  - Output: 200 products             │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Re-ranking                         │
│  - Cross-encoder model              │
│  - User personalization boost       │
│  - Business rules (margins)         │
│  - Output: Top 20 products          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  LLM Response Generation            │
│  - Format as natural language       │
│  - Include product details          │
│  - Add call-to-action               │
└─────────────────────────────────────┘
```

**Implementation**:

```python
def product_search_rag(query, user_id):
    # 1. Query preprocessing
    parsed = parse_query(query)  # Extract filters, entities
    expanded_query = expand_query(query)  # Synonyms, related terms
    
    # 2. Hybrid retrieval
    query_embedding = embedding_model.encode(expanded_query)
    
    # Dense retrieval (vector DB)
    dense_results = vector_db.query(
        embedding=query_embedding,
        top_k=500,
        filters=parsed.filters  # Pre-filter by category, price range
    )
    
    # Sparse retrieval (Elasticsearch BM25)
    sparse_results = elasticsearch.search(
        query=parsed.keywords,
        filters=parsed.filters,
        size=500
    )
    
    # Merge using Reciprocal Rank Fusion (RRF)
    merged = reciprocal_rank_fusion(dense_results, sparse_results)
    
    # 3. Filtering
    filtered = [p for p in merged if p.in_stock and p.price < parsed.price_limit]
    
    # 4. Re-ranking with cross-encoder
    scores = reranker_model.predict([(query, p.title + p.description) for p in filtered])
    ranked = sorted(zip(filtered, scores), key=lambda x: x[1], reverse=True)
    
    # 5. Personalization boost
    user_profile = get_user_profile(user_id)
    for product, score in ranked:
        if product.brand in user_profile.favorite_brands:
            score *= 1.2  # Boost preferred brands
    
    top_products = [p for p, s in ranked[:20]]
    
    # 6. Generate LLM response
    prompt = f"""User asked: "{query}"
    
Here are relevant products:
{format_products(top_products)}

Generate a helpful response recommending top 3 products. Be conversational."""
    
    response = llm.generate(prompt, temperature=0.7)
    
    return {
        "text": response,
        "products": top_products[:3],
        "metadata": {
            "retrieved_count": len(merged),
            "filtered_count": len(filtered)
        }
    }
```

**Embedding Model**:
- **Choice**: Sentence-BERT (multilingual) or E5-large
- **Dimension**: 768 or 1024
- **Training**: Fine-tune on Flipkart product queries + click data

**Vector Database**:
- **Milvus** (open-source, self-hosted)
- **Configuration**:
  - Index: HNSW (fast approximate nearest neighbor)
  - Distance: Cosine similarity
  - Partitions by category (for faster search)

### 4.4 LLM Serving Layer

**Model Selection**:

| Model | Use Case | Latency | Cost | Quality |
|-------|----------|---------|------|---------|
| **Llama-3-70B** | General conversation, complex queries | 2-3 sec | High | Excellent |
| **Mistral-7B** | Simple queries, chitchat | 0.5-1 sec | Low | Good |
| **GPT-3.5-turbo** | Fallback (via API) | 1-2 sec | Medium | Very Good |

**Serving Stack**:
```
┌──────────────────────────────────────────────────┐
│  vLLM (GPU Serving)                              │
│  - Continuous batching                           │
│  - PagedAttention (efficient memory)             │
│  - Serve 20 concurrent requests per GPU          │
│  - A100 (40GB) × 20 nodes                        │
└──────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────┐
│  Load Balancer                                   │
│  - Round-robin across GPU nodes                  │
│  - Health checks (ping /health every 30s)        │
│  - Auto-retry on failure                         │
└──────────────────────────────────────────────────┘
```

**Optimization Techniques**:

**1. Streaming Responses**:
```python
def stream_llm_response(prompt):
    for token in llm.generate_stream(prompt):
        yield token
        # Send token to client via WebSocket
```

**2. Response Caching**:
```python
def get_llm_response(prompt, user_context):
    # Cache key: hash(prompt + context)
    cache_key = hash((prompt, user_context))
    
    cached = redis.get(f"llm_response:{cache_key}")
    if cached:
        return cached
    
    response = llm.generate(prompt, context=user_context)
    
    # Cache for 1 hour
    redis.setex(f"llm_response:{cache_key}", 3600, response)
    
    return response
```

**3. Speculative Decoding** (Advanced):
- Use small model to predict tokens
- Large model verifies in parallel
- 2-3x speedup

**4. Quantization**:
- INT8 quantization (AWQ, GPTQ)
- 2x faster inference, minimal quality loss

### 4.5 Conversation State Management

**Challenge**: Maintain multi-turn conversation context

**Short-term Memory** (Redis):
```python
# Store last 10 messages per conversation
conversation_key = f"conv:{conversation_id}"

redis.lpush(conversation_key, json.dumps({
    "role": "user",
    "content": message,
    "timestamp": now()
}))

redis.ltrim(conversation_key, 0, 19)  # Keep last 20 messages (10 turns)
redis.expire(conversation_key, 3600)  # 1 hour TTL
```

**Long-term Memory** (Cassandra):
```python
# Store summary of past conversations
CREATE TABLE conversation_summaries (
    user_id UUID,
    conversation_id UUID,
    summary TEXT,
    products_discussed LIST<TEXT>,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, conversation_id)
);

# Generate summary after conversation ends
def summarize_conversation(conversation_id):
    messages = get_all_messages(conversation_id)
    
    prompt = f"""Summarize this conversation in 2-3 sentences:
    
{messages}

Focus on: user's needs, products discussed, outcome."""
    
    summary = llm.generate(prompt, max_tokens=100)
    
    save_summary(conversation_id, summary)
```

**Context Window Management**:
```python
def build_prompt(user_message, conversation_history):
    # LLM has 4K token context limit
    # Reserve: System (500) + User (200) + Output (300) = 1000
    # Available for history: 3000 tokens
    
    system_prompt = get_system_prompt()  # 500 tokens
    
    # Truncate history to fit context
    truncated_history = []
    token_count = 0
    
    for msg in reversed(conversation_history):
        msg_tokens = count_tokens(msg)
        if token_count + msg_tokens > 3000:
            break
        truncated_history.insert(0, msg)
        token_count += msg_tokens
    
    full_prompt = f"""{system_prompt}

CONVERSATION HISTORY:
{format_messages(truncated_history)}

USER: {user_message}
ASSISTANT:"""
    
    return full_prompt
```

### 4.6 Safety & Moderation Pipeline

**Input Moderation** (User message):
```python
def moderate_input(user_message):
    # 1. Profanity filter
    if contains_profanity(user_message):
        return {
            "safe": False,
            "reason": "profanity",
            "response": "Please keep the conversation respectful."
        }
    
    # 2. PII detection (credit card, SSN)
    pii_detected = detect_pii(user_message)
    if pii_detected:
        user_message = redact_pii(user_message, pii_detected)
        # Warn user
    
    # 3. Jailbreak detection
    if is_jailbreak_attempt(user_message):
        return {
            "safe": False,
            "reason": "jailbreak",
            "response": "I can only help with shopping-related queries."
        }
    
    return {"safe": True, "message": user_message}
```

**Output Moderation** (LLM response):
```python
def moderate_output(llm_response, product_context):
    # 1. Hallucination check
    mentioned_products = extract_product_references(llm_response)
    for product_id in mentioned_products:
        if product_id not in product_context:
            # LLM hallucinated a product!
            return {
                "safe": False,
                "reason": "hallucination",
                "fallback": "Let me search for that product..."
            }
    
    # 2. Toxicity check (Perspective API)
    toxicity_score = perspective_api.analyze(llm_response)
    if toxicity_score > 0.7:
        return {
            "safe": False,
            "reason": "toxic",
            "fallback": fallback_response()
        }
    
    # 3. Competitor mention
    if mentions_competitor(llm_response):
        # Remove competitor name
        llm_response = remove_competitor_names(llm_response)
    
    return {"safe": True, "response": llm_response}
```

**Guardrails** (NeMo Guardrails):
```python
from nemoguardrails import RailsConfig, LLMRails

config = RailsConfig.from_path("config/")

rails = LLMRails(config)

# Define rails
rails.register_action(
    "check_product_exists",
    check_product_exists_action
)

rails.register_action(
    "block_competitor_mention",
    block_competitor_mention_action
)

# Use rails
response = rails.generate(user_message=message)
```

---

## Step 5: Prompt Engineering

### System Prompt Design

```python
SYSTEM_PROMPT = """You are Flipkart's AI shopping assistant. Your goal is to help users find and purchase products.

## CAPABILITIES
- Search 100M products across all categories
- Compare products side-by-side
- Personalize recommendations based on user history
- Add items to cart and help with checkout
- Track orders and handle returns

## RULES
1. ONLY recommend products from the ProductSearch tool - never make up products
2. Be concise - keep responses under 100 words
3. Always show product prices in INR (₹)
4. After showing products, ask if user wants to add to cart
5. If you don't know something, say "Let me check" and use tools
6. Never mention competitor websites (Amazon, Myntra, etc.)
7. If user asks about sensitive topics (politics, religion), politely redirect to shopping

## TONE
- Friendly and conversational
- Use simple language (avoid jargon)
- Use emojis sparingly (max 1 per message)

## PERSONALIZATION
You have access to user's:
- Past orders: {user_past_orders}
- Favorite brands: {user_favorite_brands}
- Price range: {user_avg_price_range}

Use this to personalize recommendations.

## CONVERSATION CONTEXT
{conversation_history}
"""
```

### Few-Shot Examples

```python
FEW_SHOT_EXAMPLES = """
## Example 1: Product Search
User: I need a laptop for coding
Assistant: Great! What's your budget? Also, do you prefer any specific brand (Dell, HP, Lenovo)?

User: Under 60000, no brand preference
Assistant: Perfect! Here are top picks for coding under ₹60K:

1. **Lenovo IdeaPad 3** (₹54,999)
   - Intel i5, 16GB RAM, 512GB SSD
   - Best seller in your range

2. **HP Pavilion 14** (₹58,999)
   - AMD Ryzen 5, 16GB RAM, 512GB SSD
   - Great for multitasking

3. **Dell Inspiron 15** (₹59,499)
   - Intel i5, 16GB RAM, 1TB SSD
   - Largest storage

Would you like to add any to cart or see more options?

## Example 2: Comparison
User: Compare iPhone 15 and Samsung S24
Assistant: Here's a quick comparison:

**iPhone 15** (₹79,900)
✅ Better camera, smoother iOS
❌ No expandable storage

**Samsung S24** (₹74,999)
✅ Larger screen, Android flexibility
❌ Camera slightly less impressive

Both are excellent! iPhone if you value camera & ecosystem, Samsung if you want more customization. Which matters more to you?

## Example 3: Handling Vague Query
User: I want something nice
Assistant: I'd love to help! Can you tell me:
- What category? (clothes, electronics, home, etc.)
- For yourself or a gift?
- Budget range?

This helps me find perfect matches!
"""
```

### Structured Output (JSON Mode)

```python
# For tool calling, use structured output
prompt = """Extract product filters from user query.

User: "Blue formal shirts under 2000"

Return JSON with:
{
  "category": "shirts",
  "attributes": {"color": "blue", "type": "formal"},
  "price_range": {"max": 2000},
  "sort_by": "popularity"
}
"""

response = llm.generate(
    prompt,
    response_format="json_object"  # OpenAI JSON mode
)

filters = json.loads(response)
```

---

## Step 6: Scaling Strategy

### Handling 50K Concurrent Conversations

**Horizontal Scaling**:
```
Conversational AI Service: 200 instances
  - Each handles 250 concurrent WebSocket connections
  - Stateless (conversation state in Redis)
  - Auto-scaling based on active connections

LLM Serving (vLLM): 20 GPU nodes (A100 40GB)
  - Each node: 20 concurrent requests
  - Total: 400 concurrent LLM inferences
  - Queue for burst traffic

Redis Cluster: 16 shards
  - Conversation state: 10M active conversations
  - TTL: 1 hour (expire inactive)

Vector DB (Milvus): 10 nodes
  - 100M product embeddings
  - Sharded by category
```

**Cost Optimization**:
- Use smaller model (Mistral-7B) for simple queries (70% of traffic)
- Cache frequent responses (popular queries)
- Batch inference where possible
- Spot instances for GPU nodes (50% cost saving)

---

## Step 7: Monitoring & Evaluation

### Metrics to Track

**Business Metrics**:
- Task completion rate (user bought something): Target >30%
- Conversation length (avg messages): Target 5-8
- Add-to-cart rate: Target >50%
- User satisfaction (CSAT): Target >4.0/5
- Repeat usage: Target >40% week-over-week

**LLM Performance**:
- Latency (P50, P95, P99): Target <3 sec P95
- First token time (TTFT): Target <1 sec
- Tokens per second: Target 40-50
- Token usage per conversation: Target <2000 (cost control)
- Cache hit rate: Target >60%

**Quality Metrics**:
- Hallucination rate: <1% (product mentions not in catalog)
- Safety violations: <0.5% (profanity, toxicity)
- Tool call accuracy: >95% (correct tool for intent)
- Retrieval relevance: >80% (products match query)

**Cost Metrics**:
- Cost per conversation: Target <$0.05
- GPU utilization: Target >70%
- Token efficiency: Optimize prompt tokens

### Evaluation Framework

**Offline Evaluation**:
```python
# Test dataset: 10K user queries with ground truth
test_set = load_test_set()

for example in test_set:
    # Run RAG pipeline
    response = conversational_assistant(example.query)
    
    # Evaluate retrieval
    retrieval_precision = calculate_precision(
        retrieved=response.products,
        relevant=example.relevant_products
    )
    
    # Evaluate LLM response
    bleu_score = calculate_bleu(response.text, example.expected_response)
    
    # Check hallucinations
    hallucinated = check_hallucinations(response.text, response.products)
    
    log_metrics({
        "retrieval_precision": retrieval_precision,
        "bleu_score": bleu_score,
        "hallucinated": hallucinated
    })
```

**Online Evaluation** (A/B Testing):
```python
# Experiment: New prompt vs old prompt
def get_llm_response(query, user_id):
    # Assign user to experiment group
    group = hash(user_id) % 100
    
    if group < 10:  # 10% new prompt
        response = llm.generate(query, prompt=NEW_PROMPT)
        log_experiment("new_prompt", user_id, query, response)
    else:  # 90% old prompt
        response = llm.generate(query, prompt=OLD_PROMPT)
        log_experiment("old_prompt", user_id, query, response)
    
    return response

# After 1 week, analyze:
# - Task completion rate (new vs old)
# - User satisfaction (new vs old)
# - Latency, cost
```

**Human Evaluation**:
```python
# Sample 100 random conversations per day
# Have human raters score on:
# 1. Relevance (1-5): Did response answer query?
# 2. Helpfulness (1-5): Was response useful?
# 3. Safety (binary): Any violations?
# 4. Hallucinations (binary): Any made-up products?

# Calculate inter-rater agreement (Kappa score)
# Use as ground truth for model improvements
```

---

## Step 8: Expected Interview Questions

### Architecture Questions

1. **Q**: Why use an agent architecture (LangChain) instead of a simple LLM call?
   - **A**: (1) Agents can use tools (search, cart, order APIs) to ground responses in real data, preventing hallucinations. (2) Multi-step reasoning (user asks for comparison → search products → compare → respond). (3) Stateful conversations (remember context across turns). (4) Retry and error handling. Simple LLM calls can't interact with external systems.

2. **Q**: How do you prevent the LLM from hallucinating products?
   - **A**: (1) **RAG architecture**: LLM only responds based on retrieved products from catalog, never generates product names. (2) **Output validation**: Parse LLM response, check that all mentioned product IDs exist in retrieved set. (3) **System prompt**: Explicit instruction "ONLY use products from ProductSearch tool". (4) **Guardrails**: NeMo Guardrails to block responses mentioning unknown products. (5) **Monitoring**: Track hallucination rate, retrain if high.

3. **Q**: How do you handle multi-turn conversations with context?
   - **A**: (1) **Short-term**: Redis stores last 10 turns (20 messages) with 1-hour TTL. (2) **Context building**: When user sends new message, fetch conversation history from Redis, append to prompt. (3) **Token limit management**: Truncate old messages if context exceeds LLM limit (4K tokens). (4) **Long-term memory**: After conversation ends, generate summary with LLM, store in Cassandra for future personalization. (5) **Entity tracking**: Extract entities (product IDs, preferences) across turns, maintain in session state.

### Scaling Questions

4. **Q**: How would you reduce LLM inference latency from 3 seconds to <1 second?
   - **A**: (1) **Smaller model**: Use Mistral-7B (0.5s) for simple queries, Llama-70B only for complex ones. (2) **Streaming**: Start sending tokens immediately (perceived latency <1s). (3) **Speculative decoding**: Use small model to predict, large model to verify (2-3x speedup). (4) **Quantization**: INT8 quantization (2x faster, minimal quality loss). (5) **Caching**: Cache responses for frequent queries (cache hit = 20ms). (6) **Batch inference**: Group multiple requests (higher throughput). (7) **GPU optimization**: Use vLLM with PagedAttention.

5. **Q**: LLM API costs are too high ($0.10 per conversation). How to reduce to $0.05?
   - **A**: (1) **Use open-source models**: Self-host Llama-3-70B (infra cost ~$0.02/call vs OpenAI $0.10). (2) **Smaller models**: 70% of queries are simple (chitchat, basic search), use Mistral-7B (10x cheaper). (3) **Prompt optimization**: Reduce prompt tokens (remove unnecessary examples, compress context). (4) **Caching**: 40% of queries are similar, cache responses (0 LLM cost). (5) **Batch retrieval**: Reduce RAG calls (1 retrieval per conversation, not per message). (6) **Reject off-topic**: Filter out non-shopping queries before LLM call.

### GenAI-Specific Questions

6. **Q**: How do you evaluate the quality of LLM responses in production?
   - **A**: **Offline**: (1) BLEU/ROUGE for fluency, (2) Retrieval metrics (precision, recall), (3) Hallucination detection (product mentions validation), (4) Human eval on sample (100/day). **Online**: (1) Task completion rate (user bought something), (2) CSAT survey (1-5 rating), (3) Implicit signals (user abandoned? clicked products?), (4) A/B tests (compare prompt versions). **Hybrid**: (1) LLM-as-judge (use GPT-4 to rate response quality), (2) Embed human feedback into retraining.

7. **Q**: Your RAG system retrieves irrelevant products 30% of the time. How to improve?
   - **A**: (1) **Better embeddings**: Fine-tune embedding model on Flipkart data (query → clicked products). (2) **Hybrid search**: Combine dense (vector) + sparse (BM25) retrieval using reciprocal rank fusion. (3) **Query expansion**: Add synonyms, related terms ("mobile" → "phone", "smartphone"). (4) **Re-ranking**: Use cross-encoder model to re-score candidates (query, product) → relevance score. (5) **Filtering**: Apply hard filters first (category, price, in-stock) before semantic search. (6) **User feedback**: Track which products user clicks, use as training signal. (7) **Evaluate pipeline**: Measure retrieval precision@10, recall@100 separately.

8. **Q**: How do you handle code-mixed queries (Hindi + English: "Blue wale shoes dikhao")?
   - **A**: (1) **Multilingual embeddings**: Use XLM-RoBERTa or Sentence-BERT (multilingual) for encoding. (2) **Language detection**: Detect languages in query (fastText), translate to English for retrieval. (3) **Code-mixed training**: Fine-tune embedding model on code-mixed queries from Flipkart logs. (4) **LLM prompt**: Instruct LLM to handle multiple languages, respond in user's language. (5) **Transliteration**: Convert Hindi in Devanagari script to Roman (if needed). (6) **Query rewriting**: LLM rewrites code-mixed query to English for better retrieval.

### Trade-offs Questions

9. **Q**: Should you self-host open-source LLMs or use OpenAI API?
   - **A**: **OpenAI API**: ✅ Faster to deploy, no infra management, better quality. ❌ Expensive ($0.10/call at scale), data leaves your control (privacy concern), vendor lock-in. **Self-hosted**: ✅ Cheaper at scale ($0.02/call with amortized GPU cost), data privacy (India data residency), customizable (fine-tuning). ❌ Upfront GPU investment ($100K+), need ML infra team, model quality slightly lower. **Decision**: Hybrid - use OpenAI for 10% complex queries (where quality matters), self-host Llama-3 for 90% simple queries. Start with OpenAI (MVP), migrate to self-hosted at scale.

10. **Q**: Streaming responses improve perceived latency but complicate error handling. Worth it?
    - **A**: **Yes, absolutely**. (1) **UX**: Users see instant response (first token <1s), much better than waiting 3s for full response. (2) **Error handling**: Stream tokens until error occurs, then send error message ("Sorry, something went wrong. Let me try again"). Don't show partial response if hallucination detected mid-stream. (3) **Implementation**: WebSocket for streaming, buffer last few tokens in case we need to retract. (4) **Cost**: Streaming has no extra cost, same token usage. (5) **Mobile**: Works well on mobile (progressive rendering). Only downside: Slightly more complex client code, but worth the UX improvement.

### Data & Privacy Questions

11. **Q**: User asks "What did I order last month?" Should LLM access full order history?
    - **A**: **Security considerations**: (1) **Authentication**: Verify user identity (JWT token, session). (2) **Authorization**: LLM can only access current user's data (not other users). (3) **Data minimization**: Don't send full order details to LLM, only summary (product names, dates). (4) **PII redaction**: Remove addresses, phone numbers before sending to LLM. (5) **Audit logging**: Log all LLM queries accessing PII for compliance. (6) **On-prem LLM**: If using external API (OpenAI), consider self-hosting for sensitive data. (7) **Differential privacy**: Add noise to aggregated stats if needed.

12. **Q**: How do you handle rate limiting and abuse (users spamming the chatbot)?
    - **A**: (1) **Per-user rate limit**: 20 messages per minute, 200 per hour (via Redis counter with TTL). (2) **Concurrent conversation limit**: Max 1 active conversation per user. (3) **Token budget**: Max 10K tokens per user per day (cost control). (4) **Abuse detection**: If user sends same message 10x, block for 1 hour. (5) **CAPTCHA**: If suspicious activity (VPN, scripted behavior), require CAPTCHA. (6) **Circuit breaker**: If LLM service is overloaded, temporarily reject new conversations (503 response). (7) **Priority queue**: Premium users get higher priority in LLM queue.

---

## Step 9: Edge Cases & Failure Handling

### Edge Cases

1. **User sends image instead of text**
   - **Solution**: Use multimodal LLM (GPT-4V, Gemini Vision) to understand image, convert to text query

2. **User asks off-topic question** ("Who won IPL 2026?")
   - **Solution**: Intent classifier detects "chitchat", politely redirect: "I can help you shop! Looking for anything specific?"

3. **Product goes out of stock mid-conversation**
   - **Solution**: Check inventory before responding, show "Out of stock" badge, suggest alternatives

4. **User speaks in pure Hindi** (Devanagari script)
   - **Solution**: Detect language, use multilingual LLM (or translate to English internally)

5. **LLM response is cut off** (hits max token limit)
   - **Solution**: Set max_tokens high enough (512), if cut off, append "... (click for more)"

6. **User says "Add to cart" but no product shown**
   - **Solution**: LLM asks "Which product would you like to add?", show recent products discussed

### Failure Modes

**1. LLM Service Down**
- **Fallback**: Show pre-defined quick actions ("Search Products", "Track Order", "Talk to Human")
- **Graceful**: "I'm having trouble right now. Try again in a moment or browse products manually."

**2. Vector DB Slow (>1 sec)**
- **Circuit breaker**: If 50% queries >1s, skip vector search, use only keyword search (Elasticsearch)
- **Fallback**: Show trending products

**3. Hallucination Detected Post-Generation**
- **Action**: Don't send to user, generate fallback: "Let me search for products matching your request."
- **Alert**: Log for retraining

**4. User Conversation Exceeds Context Window**
- **Action**: Summarize old messages with LLM, keep summary + recent 5 turns

**5. Toxic User Input**
- **Action**: Don't send to LLM, respond: "Please keep the conversation respectful."

---

## Step 10: Summary - Key Talking Points

### ✅ Show GenAI Expertise

**LLM Orchestration**:
- "Agent architecture with tool use for grounded responses"
- "ReAct pattern: reasoning → action → observation → final answer"
- "Function calling for cart, order, tracking APIs"

**RAG Pipeline**:
- "Hybrid retrieval: dense (vector) + sparse (BM25) for best recall"
- "Cross-encoder re-ranking for precision"
- "Embedding fine-tuning on Flipkart click data"

**Prompt Engineering**:
- "Structured system prompt with rules and few-shot examples"
- "JSON mode for structured outputs (filters, entities)"
- "Context window management with truncation strategy"

### ✅ Show Engineering Depth

**Scaling**:
- "vLLM with continuous batching for efficient GPU utilization"
- "Streaming responses via WebSocket for <1s perceived latency"
- "Multi-level caching (prompt responses, embeddings, products)"
- "Horizontal scaling: 200 service instances, 20 GPU nodes"

**Safety**:
- "Input/output moderation pipeline"
- "Hallucination detection: validate product mentions against retrieved set"
- "Guardrails with NeMo for jailbreak prevention"
- "PII redaction before LLM processing"

**Monitoring**:
- "Offline metrics: BLEU, hallucination rate, retrieval precision"
- "Online metrics: task completion, CSAT, conversation length"
- "A/B testing for prompt optimization"
- "Cost monitoring: token usage, GPU utilization"

### ✅ Reference Flipkart Context

- "Similar to Flipkart's SLAP assistant launching in 2026"
- "Aligns with Flipkart's GenAI initiatives mentioned by Mayur Datar"
- "Multimodal search like Flipkart Immerse"
- "At Flipkart's scale (50M users), we need..."

---

## Sources

- [Flipkart SLAP Conversational AI Launch (2026)](https://www.medianama.com/2026/01/223-flipkart-conversational-ai-commerce-slap/)
- [Flippi: GenAI E-commerce Assistant Research](https://arxiv.org/html/2507.05788v2)
- [Flipkart's GenAI Strategy - Mayur Datar Interview](https://stories.flipkart.com/gen-ai-indian-ecommerce-mayur-datar)
- [RAG for E-commerce Innovation](https://www.tensorway.com/post/rag-ecommerce-innovation)
- [LLM Use Cases in E-commerce](https://www.netguru.com/blog/llm-use-cases-in-e-commerce)
