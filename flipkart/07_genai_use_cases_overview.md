# GenAI Engineer - Expected Use Cases for Flipkart

**Role Context**: GenAI Engineer in AI Transformation Team
**Focus**: LLM applications, RAG systems, conversational AI, content generation
**Flipkart's GenAI Initiatives**: SLAP (Shop Like a Pro), Flippi, Multimodal Search, Mira

---

## 🎯 GenAI-Specific Use Cases (Priority Order)

Based on Flipkart's current GenAI initiatives and industry trends, here are the most likely system design questions you'll face:

### **HIGH PRIORITY** (Most Likely to be Asked)

#### 1. **Conversational Shopping Assistant (SLAP/Flippi-like)**
**Problem**: Design an LLM-powered conversational shopping assistant that helps users discover and purchase products through natural language dialogue.

**Key Challenges**:
- Intent detection and query reformulation
- Product retrieval at scale (100M SKUs)
- Personalized recommendations in conversation
- Multi-turn dialogue management
- Hallucination prevention
- Low latency (<2 sec response time)

**Why Important**: Flipkart is actively launching SLAP in 2026 as their next-gen conversational AI assistant.

**Core Concepts to Emphasize**:
- LLM orchestration (prompt engineering, chain-of-thought)
- RAG (Retrieval-Augmented Generation)
- Vector databases for product embeddings
- Conversation state management
- Safety guardrails and content moderation

---

#### 2. **RAG-Based Product Search & Discovery**
**Problem**: Design a RAG system that converts natural language queries into relevant product results, using both structured data (catalog) and unstructured data (reviews, descriptions).

**Key Challenges**:
- Semantic search over 100M products
- Hybrid search (keyword + vector)
- Query understanding (intent, entities, filters)
- Result ranking and diversity
- Real-time inventory filtering
- Multilingual support (10+ Indian languages)

**Why Important**: Core to both search and conversational AI experiences.

**Core Concepts to Emphasize**:
- Embedding models (BERT, Sentence Transformers)
- Vector databases (Milvus, Pinecone, FAISS)
- Hybrid retrieval (BM25 + dense retrieval)
- Re-ranking models
- Query expansion and reformulation

---

#### 3. **Automated Product Description & Content Generation**
**Problem**: Design a system that generates high-quality product descriptions, titles, and marketing copy for millions of products using GenAI.

**Key Challenges**:
- Generate SEO-optimized content
- Maintain brand voice consistency
- Handle multiple languages
- Fact verification (no hallucinations)
- Batch generation at scale (1M+ products/day)
- Human-in-the-loop review workflow

**Why Important**: Sellers upload products with poor descriptions; GenAI can improve quality at scale.

**Core Concepts to Emphasize**:
- LLM fine-tuning (domain-specific)
- Prompt templates and few-shot learning
- Batch inference optimization
- Content moderation pipeline
- A/B testing for conversions

---

### **MEDIUM PRIORITY** (Likely to be Asked)

#### 4. **Multi-Modal Product Search**
**Problem**: Design a system where users can search using a combination of text and images (e.g., "Show me dresses like this image but in blue").

**Key Challenges**:
- Multi-modal embeddings (CLIP, ImageBind)
- Text + image query fusion
- Visual similarity search at scale
- Attribute extraction from images
- Cross-modal retrieval

**Why Important**: Flipkart already has "Immerse" - multimodal search feature.

**Core Concepts to Emphasize**:
- Multi-modal transformers (CLIP)
- Cross-modal retrieval
- Feature fusion strategies
- Image preprocessing and indexing

---

#### 5. **Review Summarization & Sentiment Analysis**
**Problem**: Design a system that uses LLMs to summarize thousands of product reviews into actionable insights for buyers and sellers.

**Key Challenges**:
- Summarize 10K+ reviews per product
- Extract pros/cons and key themes
- Real-time updates as new reviews arrive
- Multi-language review processing
- Detect fake/spam reviews

**Why Important**: Improves purchase decisions and seller insights.

**Core Concepts to Emphasize**:
- Extractive vs abstractive summarization
- Aspect-based sentiment analysis
- LLM prompting strategies
- Incremental summarization (streaming)

---

#### 6. **AI-Powered Customer Support Automation**
**Problem**: Design a GenAI system that automates customer support tickets (order tracking, returns, complaints) with high accuracy.

**Key Challenges**:
- Intent classification (100+ support intents)
- Entity extraction (order ID, product, issue type)
- Integration with backend systems (order DB, inventory)
- Escalation to human agents
- Multi-turn conversations

**Why Important**: Reduces support costs, improves response time.

**Core Concepts to Emphasize**:
- RAG over support documentation
- Function calling / tool use
- Agent orchestration
- Conversation memory and context

---

### **LOWER PRIORITY** (Good to Prepare)

#### 7. **Seller/Vendor Chatbot for Catalog Management**
**Problem**: Design an LLM-powered assistant that helps sellers upload products, optimize listings, and manage inventory through natural language.

**Why Important**: Flipkart has 500K+ sellers; automation improves seller experience.

---

#### 8. **Voice Commerce Assistant**
**Problem**: Design a voice-based shopping system (speech-to-text → LLM → text-to-speech) for regional language users.

**Why Important**: Voice commerce is growing in Tier 2/3 cities.

---

#### 9. **Ad Copy Generation & Personalization**
**Problem**: Generate personalized ad copy for millions of products using LLMs.

**Why Important**: Sponsored listings are a revenue driver.

---

#### 10. **Supply Chain & Logistics Query Assistant**
**Problem**: Internal GenAI assistant for warehouse staff to query inventory, shipping status, etc.

**Why Important**: Internal tooling for operational efficiency.

---

## 🔑 Common Themes Across GenAI Use Cases

Regardless of which specific use case is asked, you'll need to address these common GenAI challenges:

### 1. **LLM Selection & Deployment**
- OpenAI GPT-4 vs Anthropic Claude vs open-source (Llama, Mistral)
- Cost optimization (smaller models for simpler tasks)
- On-prem vs cloud (data privacy, latency)
- Model serving (vLLM, TensorRT-LLM, Triton)

### 2. **RAG Architecture**
- Chunking strategies for documents
- Embedding model selection
- Vector database scaling
- Retrieval quality (precision vs recall)
- Context window management

### 3. **Prompt Engineering**
- System prompts and instructions
- Few-shot examples
- Chain-of-thought reasoning
- Output formatting (JSON mode)

### 4. **Safety & Guardrails**
- Content moderation (profanity, NSFW)
- Hallucination detection
- PII (Personal Identifiable Information) redaction
- Jailbreak prevention
- Rate limiting and abuse prevention

### 5. **Evaluation & Monitoring**
- Offline metrics (BLEU, ROUGE, BERTScore)
- Online metrics (user satisfaction, task completion)
- A/B testing LLM versions
- Drift detection (prompt performance over time)
- Cost monitoring (tokens/request)

### 6. **Latency Optimization**
- Streaming responses (token-by-token)
- Caching frequent queries
- Batch inference
- Model quantization (INT8, INT4)
- Speculative decoding

### 7. **Multi-Tenancy & Scale**
- Handle 50M users concurrently
- Isolate user conversations
- Horizontal scaling of LLM servers
- Load balancing across models

---

## 📊 Comparison: Traditional AI vs GenAI Use Cases

| Aspect | Traditional AI (Fraud, Pricing, Recs) | GenAI (Conversational, RAG, Content) |
|--------|--------------------------------------|-------------------------------------|
| **Model Type** | Gradient Boosting, Neural Nets | LLMs (GPT, Claude, Llama) |
| **Inference** | Milliseconds (1-50ms) | Seconds (1-5 sec) |
| **Scale Challenge** | High throughput (100K req/sec) | High latency (large models) |
| **Data** | Structured (features) | Unstructured (text, images) |
| **Evaluation** | Precision, recall, F1 | BLEU, human eval, task success |
| **Failure Mode** | Wrong prediction | Hallucination, toxic output |
| **Cost** | $0.001 per inference | $0.01-0.10 per call |
| **Key Challenge** | Feature engineering, scaling | Prompt engineering, safety |

---

## 🎯 Interview Strategy for GenAI Use Cases

### What Interviewers Look For

**GenAI-Specific**:
✅ LLM orchestration (not just API calls)
✅ RAG pipeline design
✅ Prompt engineering depth
✅ Handling hallucinations
✅ Safety and moderation
✅ Cost optimization

**Still Important** (From HR Guide):
✅ Distributed systems (serving LLMs at scale)
✅ Async processing (batch generation jobs)
✅ Caching (prompt responses)
✅ Monitoring (latency, cost, quality)

### Common Pitfalls to Avoid

❌ "Just call OpenAI API" - Too simplistic, no engineering depth
❌ Ignoring latency - LLMs are slow, need streaming, caching
❌ Ignoring cost - Token usage adds up quickly at scale
❌ No safety guardrails - Hallucinations, jailbreaks, PII leaks
❌ No evaluation strategy - How do you measure quality?
❌ Forgetting data privacy - User data sent to external LLM APIs?

---

## 📖 Recommended Approach for GenAI Interviews

### Use the **GenAI-DRIVER** Framework

**D - Define & Clarify**
- User scale, query volume
- Latency requirements (real-time vs batch)
- **LLM choice**: OpenAI vs open-source?
- **Data privacy**: Can we send user data externally?
- **Quality bar**: How accurate must responses be?
- **Language support**: English only or multilingual?

**R - Requirements**
- Functional: What must the LLM do?
- **GenAI-specific NFRs**:
  - Latency: P95 response time
  - Quality: Accuracy, relevance, coherence
  - Safety: No hallucinations, toxic content
  - Cost: $ per 1M tokens

**I - Initial Design**
- High-level architecture with GenAI components:
  - LLM serving layer
  - RAG pipeline (if applicable)
  - Vector database
  - Prompt orchestration
  - Safety filters

**V - Validate & Deep Dive**
Pick 2-3 components:
- RAG retrieval strategy
- LLM serving infrastructure
- Prompt design and optimization
- Safety and moderation pipeline

**E - Edge Cases**
- LLM hallucinations
- Slow response times
- API rate limits (OpenAI throttling)
- Toxic user inputs
- Multi-language edge cases

**R - Refine**
- Caching strategies
- Cost optimization
- A/B testing prompts
- Monitoring and alerting

---

## 🔬 Key Technologies to Mention

### LLM Frameworks & Tools
- **LangChain / LlamaIndex**: Orchestration frameworks
- **vLLM / TensorRT-LLM**: Fast inference serving
- **Ollama / LocalAI**: Local LLM deployment
- **Prompt flow / DSPy**: Prompt optimization

### Vector Databases
- **Milvus**: Open-source, scalable
- **Pinecone**: Managed, easy to use
- **Weaviate**: Hybrid search
- **FAISS**: In-memory, fast

### Embedding Models
- **OpenAI text-embedding-3-large**: High quality
- **Sentence Transformers**: Open-source
- **E5, BGE**: SOTA open-source
- **Cohere Embed**: Multilingual

### LLM Providers
- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude 3 (Opus, Sonnet, Haiku)
- **Open-source**: Llama 3, Mistral, Mixtral
- **Google**: Gemini, PaLM

### Safety & Moderation
- **OpenAI Moderation API**
- **Perspective API** (Google Jigsaw)
- **LLM Guard**: Open-source guardrails
- **NeMo Guardrails**: NVIDIA

### Evaluation
- **RAGAS**: RAG evaluation framework
- **TruLens**: LLM app evaluation
- **Langfuse**: LLM observability
- **PromptFoo**: Prompt testing

---

## 🎓 Interview Preparation Priority

### Tonight (GenAI Focus)
1. **Read**: [Conversational Shopping Assistant](./08_genai_conversational_assistant.md) - 1.5 hours
2. **Read**: [RAG-Based Product Search](./09_genai_rag_product_search.md) - 1.5 hours
3. **Skim**: This overview document - 30 min
4. **Review**: Core GenAI concepts (RAG, embeddings, prompting) - 30 min

### If Time Permits
- Read: Content Generation use case
- Practice: Drawing RAG architecture diagrams
- Review: LLM evaluation metrics

---

## 📚 Next Steps

I'm creating detailed deep-dives for the top 3 GenAI use cases:

1. **Conversational Shopping Assistant (SLAP)** - Most important
2. **RAG-Based Product Search & Discovery** - Foundation for many GenAI apps
3. **Automated Product Content Generation** - Practical e-commerce problem

Each will include:
- Complete architecture diagram
- Component deep-dives
- 12+ expected interview questions with answers
- Prompt engineering examples
- Safety and evaluation strategies

---

## Sources

- [Flipkart SLAP Launch (2026)](https://www.medianama.com/2026/01/223-flipkart-conversational-ai-commerce-slap/)
- [Flippi: GenAI Assistant Research](https://arxiv.org/html/2507.05788v2)
- [Flipkart Immerse: Multimodal Search](https://stories.flipkart.com/flipkart-immerse-multi-modal-search/)
- [GenAI in E-commerce - Mayur Datar (Chief Data Scientist)](https://stories.flipkart.com/gen-ai-indian-ecommerce-mayur-datar)
- [RAG in E-commerce Use Cases](https://www.tensorway.com/post/rag-ecommerce-innovation)
- [LLM Applications in E-commerce](https://www.netguru.com/blog/llm-use-cases-in-e-commerce)
