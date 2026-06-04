# Flipkart AI Engineer Interview Prep

**Interview Date**: Tomorrow
**Role**: AI Engineer - AI Transformation Team
**Focus**: AI System Design with strong emphasis on distributed systems

---

## 📚 Preparation Materials

### 1. [Flipkart AI Role Overview](./01_flipkart_ai_role_overview.md)
- Company context and AI transformation charter
- Tech stack and current AI initiatives
- Role responsibilities and expectations
- Salary insights
- **Read this first** to understand what Flipkart is looking for

### 2. [Interview Framework](./02_interview_framework.md)
- **DRIVER method** for structuring your answers
- Communication tips and time management
- Common pitfalls to avoid
- Back-of-envelope calculation templates
- **Reference this** during interview prep to practice your approach

### 3. Use Case Deep Dives

#### [Real-Time Fraud Detection Engine](./03_fraud_detection_system.md)
- **Challenge**: Evaluate transactions in <50ms
- **Key concepts**: Feature engineering, ML model serving, circuit breakers
- **Architecture**: Multi-level caching, parallel processing, graceful degradation
- **Expected questions**: 12 detailed Q&As with answers

#### [Dynamic Pricing Engine](./04_dynamic_pricing_engine.md)
- **Challenge**: Update millions of SKUs every hour
- **Key concepts**: Batch processing, price optimization, event-driven architecture
- **Architecture**: Spark pipelines, Kafka propagation, multi-level caching
- **Expected questions**: 12 detailed Q&As with answers

#### [Real-Time Recommendation Feed](./05_realtime_recommendation_feed.md)
- **Challenge**: Personalized infinite scroll adapting in real-time
- **Key concepts**: 3-stage funnel, vector databases, online learning
- **Architecture**: Candidate generation, ML ranking, real-time aggregation
- **Expected questions**: 12 detailed Q&As with answers

### 4. [Core Concepts Cheat Sheet](./06_core_concepts_cheatsheet.md)
- Quick reference for distributed systems concepts
- Concurrency, scaling, data stores, async processing
- Circuit breakers, caching, load balancing, rate limiting
- **Review the night before** for quick refreshers

---

## 🎯 Interview Strategy

### What They're Evaluating

✅ **Software Engineering First, AI Second**
- Strong distributed systems knowledge
- Production-ready system design
- Not just "stitch APIs together"

✅ **Core Competencies** (from HR guide):
- Concurrency & parallelism
- System decoupling
- Horizontal scaling
- Fan-out architectures
- Data store selection
- Async processing
- Circuit breakers & resiliency
- Feedback loops

✅ **Communication**:
- Think out loud
- Ask clarifying questions
- Discuss trade-offs
- Draw diagrams

---

## 📖 How to Use These Materials

### Tonight (Day Before Interview)

1. **Read**: [Role Overview](./01_flipkart_ai_role_overview.md) (15 min)
   - Understand Flipkart's AI transformation
   - Note the tech stack
   - Remember key initiatives

2. **Study**: [Interview Framework](./02_interview_framework.md) (30 min)
   - Memorize the DRIVER method
   - Practice back-of-envelope calculations
   - Review communication tips

3. **Deep Dive**: Pick 2 of 3 use cases (2-3 hours)
   - Fraud Detection (if asked about real-time systems)
   - Dynamic Pricing (if asked about batch processing / scale)
   - Recommendations (if asked about ML/personalization)
   - For each: Understand architecture, read expected questions

4. **Review**: [Cheat Sheet](./06_core_concepts_cheatsheet.md) (30 min)
   - Quick scan of all concepts
   - Focus on areas you're less familiar with

### Morning of Interview

1. **Quick Review** (30 min):
   - Skim the DRIVER method
   - Review one use case architecture diagram
   - Scan cheat sheet for confidence

2. **Mental Prep**:
   - Remember: Clarify before designing
   - Think: Engineering > ML
   - Approach: Trade-offs, not perfect solutions

---

## 🔑 Key Talking Points to Remember

### Show Engineering Depth
- "We need sub-50ms latency, so parallel processing is critical"
- "Horizontal scaling of stateless services"
- "Multi-level caching with 95%+ hit ratio"
- "Circuit breakers for graceful degradation"
- "Event-driven architecture with Kafka for decoupling"

### Show Production Thinking
- "4 nines availability because downtime = revenue loss"
- "A/B testing before full model rollout"
- "Monitoring with Prometheus, tracing with Jaeger"
- "Failure modes: What if the ML model goes down?"

### Show Trade-off Analysis
- "Batch vs real-time: batch is cheaper for 10M SKUs"
- "Eventual consistency for scalability vs strong consistency for correctness"
- "XGBoost vs neural network: latency vs accuracy"
- "False positives hurt UX, false negatives hurt revenue"

### Reference Flipkart Context
- "Similar to how Flipkart uses ML for Mira chatbot..."
- "This aligns with Flipkart's OneTech initiative..."
- "Given Flipkart's scale (50M users), we'd need..."

---

## ✅ Pre-Interview Checklist

**Day Before**:
- [ ] Read all 6 documents
- [ ] Practice drawing architecture diagrams
- [ ] Prepare 2-3 questions to ask interviewer
- [ ] Get good sleep (seriously!)

**Morning Of**:
- [ ] Quick framework review
- [ ] Have pen and paper ready for diagrams
- [ ] Join 5 min early
- [ ] Deep breath, you got this!

---

## 💡 Sample Questions to Ask Interviewer

**About the Role**:
- "What are the immediate priorities for the AI transformation team?"
- "What AI use cases are you tackling first?"
- "How do you balance quick wins vs long-term infrastructure?"

**About the Team**:
- "What's the team composition? (ML engineers, data scientists, infrastructure?)"
- "How do you handle model deployment and monitoring?"
- "What's the collaboration model with product teams?"

**About Technology**:
- "What's the current ML tech stack?"
- "Are you building in-house or using managed services?"
- "How do you handle A/B testing for ML models?"

---

## 🎓 Final Tips

1. **Clarify First**: Spend 3-5 min asking questions before designing
2. **Draw Diagrams**: Visual communication is powerful
3. **Start Simple**: Get the basics right, then optimize
4. **Show Depth**: Pick 2-3 components to deep dive
5. **Discuss Failures**: Every component can fail, how to handle?
6. **Use Numbers**: "I estimate 10K req/sec, so we need..."
7. **Be Honest**: If you don't know, say "Here's how I'd find out..."

---

## 📊 Resources Created

| File | Purpose | Time to Review |
|------|---------|----------------|
| `01_flipkart_ai_role_overview.md` | Company context, role details | 15 min |
| `02_interview_framework.md` | DRIVER method, communication tips | 30 min |
| `03_fraud_detection_system.md` | Real-time system design | 1 hour |
| `04_dynamic_pricing_engine.md` | Batch processing at scale | 1 hour |
| `05_realtime_recommendation_feed.md` | ML personalization system | 1 hour |
| `06_core_concepts_cheatsheet.md` | Quick reference | 30 min |

**Total prep time**: ~5 hours (recommend focusing on 2 use cases for depth)

---

## 🚀 You're Ready!

You've prepared thoroughly with:
- ✅ Understanding of Flipkart's AI transformation
- ✅ Structured interview framework (DRIVER)
- ✅ 3 detailed system design examples
- ✅ 36 expected interview questions with answers
- ✅ Core distributed systems concepts mastery

**Remember**: They're evaluating your **engineering thinking**, not just AI knowledge. Show that you can build **production-ready, scalable, resilient** systems.

**Good luck!** 🎉
