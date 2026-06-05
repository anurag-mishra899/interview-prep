# Enterprise Search Architecture: Technical Comparison
## Three Platform Paths for Deploying RAG-Enabled Enterprise Search & Retrieval

---

## Analysis Framework

### Evaluation Dimensions
1. **RAG Architecture & Vector Capabilities** - Embedding models, vector stores, hybrid search
2. **Permission & Security Model** - Multi-tenant isolation, RBAC, data segmentation
3. **Integration & Ecosystem** - Connector breadth, vendor lock-in, interoperability
4. **Migration Complexity** - Technical debt, change management, cutover risk
5. **Cost Structure** - CapEx vs. OpEx, licensing, infrastructure scaling
6. **Technology Maturity** - Production readiness, enterprise adoption, roadmap risk

---

## Option A: Extend Current Orchestration (watsonx Foundation)

### Architecture Overview
**Core Technology Stack:**
- **Orchestration Layer**: IBM watsonx (keyword search + layered RAG)
- **Vector Store**: AWS Bedrock or watsonx.data Milvus
- **Embedding Models**: IBM Granite-embedding-278m-multilingual or Bedrock Titan
- **Search Pattern**: Hybrid (keyword-first, vector-augmented)

### Technical Deep Dive

#### RAG & Vector Capabilities
**Strengths:**
- **OpenRAG Framework**: IBM's 2026 release provides agentic RAG with multi-step reasoning and dynamic retrieval strategy selection (keyword/vector/hybrid)
- **OpenSearch Integration**: Native support for OpenSearch on watsonx.data enables lexical precision + semantic understanding
- **Incremental Layering**: Vector embeddings can be added on top of existing keyword search without disrupting current workflows
- **Multi-step Reasoning**: Agentic approach uses tool calling to drive accurate, context-aware results beyond single-shot retrieval

**Limitations:**
- **Retrofit Architecture**: Layering RAG onto keyword-first system creates technical debt; not purpose-built for semantic search
- **Hybrid Search Limitations**: Keyword search as primary orchestrator means vector capabilities are secondary, not co-equal
- **Embedding Flexibility**: Limited to IBM Granite models or requires integration work for other embedding providers

#### Permission & Security Model
**Strengths:**
- **Existing Foundation**: Current watsonx permission model can be extended rather than rebuilt
- **Familiar Controls**: IT teams already understand the permission paradigm

**Limitations:**
- **Retrofit Complexity**: Permission model designed for keyword search must be extended for vector-based retrieval patterns
- **Segmentation Granularity**: Existing advisor/employee/FI segments may not provide fine-grained isolation needed for RAG across diverse data sources
- **Multi-Tenant Constraints**: Not natively designed for strict tenant isolation required in modern RAG architectures

#### Integration & Ecosystem
**Strengths:**
- **Backward Compatible**: Existing integrations (Inside, AdvisorCompass, FI Connect) continue working
- **AWS Coexistence**: watsonx can run as SaaS on AWS, enabling hybrid architecture
- **Managed Connectors**: IBM provides 90+ product integrations

**Limitations:**
- **Vendor Dependency**: Deep coupling to IBM watsonx roadmap and pricing trajectory
- **Single-Vendor Lock-in**: Limited ability to swap orchestration layer without major rearchitecture
- **Connector Rigidity**: IBM-managed connectors may lag behind emerging data sources (e.g., newer SaaS tools)

#### Migration & Change Management
**Strengths:**
- **Lowest Migration Risk**: Incremental enhancement rather than platform replacement
- **Operational Continuity**: No cutover window, no dual-platform period
- **Skill Preservation**: Existing team expertise remains valuable

**Limitations:**
- **Technical Debt Accumulation**: Layering RAG increases architectural complexity over time
- **Future Migration Burden**: Deeper investment in watsonx makes eventual migration more expensive
- **Innovation Constraints**: Incremental approach may delay access to cloud-native RAG patterns

#### Cost Structure
**Strengths:**
- **CapEx Minimization**: Reuses existing watsonx investment
- **Predictable OpEx**: Incremental costs (vector store, embeddings) added to known baseline
- **No Dual-System Period**: Avoids running two platforms during migration

**Limitations:**
- **IBM Pricing Trajectory**: Unclear long-term cost as IBM shifts to consumption-based AI pricing
- **Hidden Costs**: Integration work to layer vector capabilities onto keyword-first architecture
- **Optimization Limits**: Hybrid architecture harder to optimize than purpose-built cloud-native stack

---

## Option B: AWS MCP Orchestration (Cloud-Native, Advisor-First)

### Architecture Overview
**Core Technology Stack:**
- **Orchestration Options**: ServiceNow AI Search, Coveo, or AWS-native (Bedrock + OpenSearch)
- **Vector Store**: Amazon OpenSearch Service (managed cluster or serverless)
- **Embedding Models**: Amazon Bedrock (Titan Embed v2, Cohere) or custom models via SageMaker
- **Search Pattern**: Hybrid-first (vector + lexical co-equal from day one)

### Technical Deep Dive

#### RAG & Vector Capabilities
**Strengths:**
- **Native Hybrid Search**: OpenSearch provides lexical, vector, and hybrid retrieval as first-class citizens, not layered afterthoughts
- **Embedding Flexibility**: Bedrock supports Titan Embed v2 (flexible 256-1024 dimensions), Cohere (1024 dim), and custom models
- **Bedrock Knowledge Bases**: Fully managed RAG solution automates chunking, embedding generation, indexing, and retrieval
- **Multi-Step Retrieval**: Bedrock agents orchestrate complex workflows with tool calling and reasoning chains
- **Production Patterns**: Extensive AWS documentation on multi-tenant RAG with JWT + FGAC (fine-grained access control)

**Limitations:**
- **Self-Assembly Required**: Unlike watsonx Orchestrate, AWS requires composing multiple services (Lambda, Step Functions, Bedrock, OpenSearch)
- **Operational Overhead**: Managing OpenSearch clusters, embedding pipelines, and orchestration logic requires deep AWS expertise
- **Maturity Gap**: AWS RAG patterns less prescriptive than turnkey solutions like watsonx or Moveworks

#### Permission & Security Model
**Strengths:**
- **Purpose-Built Isolation**: Multi-tenant RAG architectures with JWT + FGAC provide strict tenant data isolation from day one
- **Fine-Grained Policies**: OpenSearch supports document-level, field-level, and tenant-level access controls
- **Native IAM Integration**: AWS IAM roles seamlessly control access across S3, Bedrock, OpenSearch, and Lambda
- **Compliance-Ready**: FIPS, HIPAA, SOC2 compliance built into AWS managed services

**Limitations:**
- **Configuration Complexity**: Fine-grained permission models require significant setup and ongoing maintenance
- **Testing Burden**: Multi-tenant permission policies must be rigorously tested to prevent cross-tenant leakage

#### Integration & Ecosystem
**Strengths:**
- **Vendor Agnostic**: Choice of orchestration layer (ServiceNow AI Search, Coveo, AWS-native) avoids single-vendor lock-in
- **Broad Connector Ecosystem**: Coveo offers 55+ source connectors; ServiceNow integrates with 500+ enterprise systems
- **Cloud-Native Interoperability**: API-first design enables swapping components (e.g., switch from Cohere to Titan embeddings)
- **Future-Proofing**: Modular architecture allows adopting new models/services as they emerge

**Limitations:**
- **Integration Tax**: Connecting multiple best-of-breed services requires custom glue code and orchestration
- **Support Fragmentation**: Issues may span AWS, Coveo, and ServiceNow support boundaries
- **Version Management**: Keeping connectors, SDKs, and APIs in sync across vendors adds operational overhead

#### Migration & Change Management
**Strengths:**
- **Clean Slate Architecture**: Opportunity to design permission model, data flows, and retrieval patterns without legacy constraints
- **Cloud-Native Alignment**: Aligns with broader enterprise cloud strategy (presumably AWS-centric)
- **Scalability Foundation**: Cloud-native architecture designed for elastic scaling from day one

**Limitations:**
- **Highest Upfront Migration Cost**: Requires rebuilding orchestration layer, connectors, permission model, and user workflows
- **Extended Cutover Period**: Dual-platform operation (watsonx + new stack) during migration increases costs and complexity
- **Change Management Risk**: Users must adapt to new search interface, retrieval patterns, and potentially different result quality
- **Skill Gap**: Team must reskill on AWS Bedrock, OpenSearch, and chosen orchestration platform

#### Cost Structure
**Strengths:**
- **OpEx Transparency**: Consumption-based pricing for Bedrock (per 1K tokens), OpenSearch (per hour), and Lambda (per invocation)
- **Right-Sizing Flexibility**: Elastic scaling prevents over-provisioning; pay only for actual usage
- **Long-Term Optimization**: Cloud-native architecture enables continuous cost optimization (e.g., spot instances, reserved capacity)

**Limitations:**
- **High Initial CapEx**: Migration effort, proof-of-concept, re-integration work front-loads costs
- **Dual-Platform Period**: Running watsonx + AWS stack during migration doubles operational costs
- **Unpredictable OpEx**: Consumption-based pricing harder to forecast than fixed watsonx licensing
- **Hidden Costs**: Data egress fees, inter-service API calls, and CloudWatch logging add up at scale

---

## Option C: Moveworks EmployeeWorks + ServiceNow (Conversational AI, Employee-Wide)

### Architecture Overview
**Core Technology Stack:**
- **Orchestration Layer**: ServiceNow EmployeeWorks (Moveworks conversational AI + ServiceNow workflows)
- **Vector Store**: ServiceNow AI Search or integrated OpenSearch
- **Embedding Models**: ServiceNow-native or Moveworks-optimized models
- **Search Pattern**: Conversational-first (natural language queries → autonomous workflows)

### Technical Deep Dive

#### RAG & Vector Capabilities
**Strengths:**
- **Conversational Front Door**: Moveworks specializes in understanding employee intent and mapping to enterprise actions (not just returning search results)
- **Autonomous Workflows**: Goes beyond search—completes work (e.g., "submit my timesheet" → retrieves form, pre-fills data, submits)
- **Enterprise-Trained Models**: Moveworks models trained on 250+ enterprises, 5.5M users; understands business jargon, acronyms, org-specific language
- **Unified Search**: Single interface for ServiceNow knowledge base, connected SaaS tools, and enterprise repositories
- **Proven Deployment Scale**: 90% of Moveworks customers deploy to 100% of employees (broad adoption signal)

**Limitations:**
- **Black Box Models**: Moveworks embedding and ranking algorithms are proprietary; limited customization vs. Bedrock/OpenSearch
- **Conversational-First Bias**: Optimized for chat interactions; may not suit users who prefer traditional search interfaces
- **RAG Transparency**: Less visibility into retrieval strategies, chunking logic, and embedding choices compared to self-managed AWS stack

#### Permission & Security Model
**Strengths:**
- **Native Multi-Persona Support**: Purpose-built for all-employee deployment; inherently understands advisor, employee, FI, IT admin personas
- **ServiceNow RBAC Integration**: Leverages ServiceNow's mature role-based access control for content permissions
- **Cross-System Permissions**: Moveworks respects permissions in connected systems (e.g., won't surface Salesforce records user can't access)

**Limitations:**
- **Vendor Trust Requirement**: Moveworks AI must be granted broad access to enterprise systems to function (potential compliance concern)
- **Permission Model Opacity**: Less control over fine-grained permission logic compared to self-managed OpenSearch FGAC
- **Multi-Tenant Gaps**: Designed for single-enterprise deployment; may lack strict tenant isolation needed for financial services compliance

#### Integration & Ecosystem
**Strengths:**
- **Turnkey Integrations**: Moveworks offers 100+ pre-built connectors (Workday, Salesforce, SAP, Confluence, etc.)
- **ServiceNow Synergy**: Deep integration with ServiceNow ITSM, HRSD, and CSM workflows; no custom glue code required
- **Zero Connector Maintenance**: Moveworks manages connector updates, API changes, and schema migrations
- **Broad Deployment Proof**: 250 mutual ServiceNow + Moveworks customers validate enterprise-grade integration

**Limitations:**
- **ServiceNow-Centric**: Architecture assumes ServiceNow as central platform; less flexible if enterprise standardizes on other systems
- **Dual-Vendor Lock-in**: Tight coupling to both ServiceNow and Moveworks (now consolidated under ServiceNow post-acquisition)
- **Connector Black Box**: Pre-built connectors may not support custom schemas or niche enterprise systems

#### Migration & Change Management
**Strengths:**
- **Fastest Time-to-Value**: Turnkey deployment bypasses custom integration work; customers report production rollout in weeks, not months
- **High User Adoption**: Conversational interface lowers barrier to entry vs. traditional search portals; 90% full-employee deployment rate
- **Change Management Support**: Moveworks provides deployment playbooks, user training, and adoption analytics

**Limitations:**
- **Platform Lock-In Risk**: Migrating away from ServiceNow + Moveworks later would require rebuilding entire conversational AI layer
- **Highest Long-Term Migration Cost**: If Option C doesn't work, switching to Option A or B is more disruptive than switching between A and B
- **User Behavior Shift**: Training employees to use conversational AI vs. traditional search requires cultural change

#### Cost Structure
**Strengths:**
- **Predictable Per-User Pricing**: ServiceNow EmployeeWorks likely priced per employee, simplifying budgeting
- **No Infrastructure Overhead**: Fully managed SaaS eliminates OpenSearch cluster management, embedding pipeline ops, etc.
- **Included Connectors**: Pre-built integrations reduce custom development costs

**Limitations:**
- **Highest Per-User Cost**: Premium for conversational AI + ServiceNow platform likely exceeds DIY AWS or watsonx extension costs
- **Dual Licensing**: Requires both ServiceNow platform licenses and EmployeeWorks add-on; costs compound for large employee bases
- **Limited Cost Optimization**: SaaS pricing less flexible than consumption-based AWS; can't optimize via spot instances, reserved capacity, etc.
- **Usage-Based Upsells**: Potential for per-interaction or per-AI-call costs as usage scales

---

## Comparative Analysis Matrix

### RAG & Vector Capabilities
| Dimension | Option A (watsonx) | Option B (AWS MCP) | Option C (Moveworks/ServiceNow) |
|-----------|-------------------|-------------------|--------------------------------|
| **Hybrid Search Maturity** | Keyword-first + layered vector | Native hybrid (co-equal) | Conversational + semantic |
| **Embedding Flexibility** | Limited (Granite, Bedrock) | High (Titan, Cohere, custom) | Low (proprietary Moveworks) |
| **RAG Architecture** | Retrofit (OpenRAG 2026) | Purpose-built | Turnkey black box |
| **Multi-Step Reasoning** | Yes (agentic OpenRAG) | Yes (Bedrock agents) | Yes (Moveworks autonomous) |
| **Customization Depth** | Medium | High | Low |

### Permission & Security
| Dimension | Option A (watsonx) | Option B (AWS MCP) | Option C (Moveworks/ServiceNow) |
|-----------|-------------------|-------------------|--------------------------------|
| **Multi-Tenant Isolation** | Retrofit required | Native (JWT + FGAC) | Native (persona-based) |
| **Fine-Grained Control** | Limited | High (document/field-level) | Medium (ServiceNow RBAC) |
| **Compliance Posture** | Mature (IBM enterprise) | Mature (AWS FedRAMP, HIPAA) | Mature (ServiceNow + Moveworks) |
| **Permission Transparency** | Medium | High (self-managed) | Low (vendor-managed) |

### Integration & Ecosystem
| Dimension | Option A (watsonx) | Option B (AWS MCP) | Option C (Moveworks/ServiceNow) |
|-----------|-------------------|-------------------|--------------------------------|
| **Connector Breadth** | 90+ (IBM-managed) | 55+ (Coveo) + custom | 100+ (pre-built) |
| **Vendor Lock-In** | High (IBM-only) | Low (multi-vendor) | High (ServiceNow + Moveworks) |
| **Interoperability** | Medium | High (API-first) | Medium (ServiceNow-centric) |
| **Connector Maintenance** | IBM-managed | Self-managed | Moveworks-managed |

### Migration & Risk
| Dimension | Option A (watsonx) | Option B (AWS MCP) | Option C (Moveworks/ServiceNow) |
|-----------|-------------------|-------------------|--------------------------------|
| **Migration Complexity** | Lowest (incremental) | Highest (full replatform) | Medium (turnkey, but new UX) |
| **Change Management** | Minimal | Extensive | Medium (user behavior shift) |
| **Technical Debt** | Increases (layering) | Decreases (clean slate) | Low (managed service) |
| **Time to Production** | Fastest (weeks) | Slowest (6-12 months) | Fast (4-8 weeks) |

### Cost Structure
| Dimension | Option A (watsonx) | Option B (AWS MCP) | Option C (Moveworks/ServiceNow) |
|-----------|-------------------|-------------------|--------------------------------|
| **Upfront CapEx** | Lowest | Highest | Medium |
| **Ongoing OpEx** | Predictable | Variable (consumption) | High (per-user SaaS) |
| **Total Cost of Ownership (3yr)** | Medium | Low-Medium (after migration) | Highest |
| **Cost Optimization Potential** | Low | High | Low |

---

## Pros and Cons Summary

### Option A: Extend watsonx (Incremental Evolution)

#### ✅ Pros
1. **Lowest Risk Path**: No platform replacement, no cutover window, preserves existing investments
2. **Operational Continuity**: Teams continue using familiar tools; no retraining required
3. **Fast Time-to-Value**: Incremental RAG capabilities can be added in weeks
4. **Proven Compatibility**: Existing integrations (Inside, AdvisorCompass, FI Connect) remain stable
5. **OpenRAG Framework**: IBM's 2026 agentic RAG provides multi-step reasoning and adaptive retrieval
6. **Cost Predictability**: Incremental costs easier to forecast than full migration

#### ❌ Cons
1. **Technical Debt Accumulation**: Layering RAG onto keyword search creates long-term architectural complexity
2. **IBM Roadmap Dependency**: Deep coupling to IBM watsonx evolution and pricing changes
3. **Single-Vendor Lock-In**: Limited ability to pivot to alternative orchestration platforms
4. **Permission Model Retrofit**: Existing segmentation may not provide granularity needed for RAG use cases
5. **Innovation Lag**: Incremental approach delays access to cloud-native RAG design patterns
6. **Future Migration Burden**: Deeper investment makes eventual platform switch more expensive

### Option B: AWS MCP (Cloud-Native Replatform)

#### ✅ Pros
1. **Purpose-Built RAG Architecture**: Native hybrid search (vector + lexical co-equal) from day one
2. **Vendor Flexibility**: Multi-vendor ecosystem (ServiceNow AI Search, Coveo, AWS-native) avoids lock-in
3. **Embedding Choice**: Bedrock supports multiple models (Titan, Cohere) + custom via SageMaker
4. **Fine-Grained Permissions**: OpenSearch JWT + FGAC enables strict multi-tenant isolation
5. **Cloud-Native Alignment**: Fits enterprise AWS strategy; elastic scaling, consumption pricing
6. **Long-Term TCO**: After migration, optimized cloud-native stack likely costs less than watsonx or ServiceNow
7. **Extensibility**: API-first architecture enables custom workflows, models, and integrations

#### ❌ Cons
1. **Highest Migration Risk**: Full replatform requires rebuilding orchestration, connectors, permissions, UX
2. **Extended Cutover**: Dual-platform operation (watsonx + AWS) during migration doubles costs
3. **Skill Gap**: Team must learn Bedrock, OpenSearch, Lambda, Step Functions, chosen orchestrator
4. **Operational Overhead**: Self-managed stack requires expertise in cluster tuning, embedding pipelines, monitoring
5. **Time to Production**: 6-12 month migration timeline delays business value
6. **Integration Tax**: Connecting best-of-breed services requires custom glue code
7. **Support Fragmentation**: Issues may span AWS, Coveo, ServiceNow support boundaries

### Option C: Moveworks EmployeeWorks + ServiceNow (Conversational AI)

#### ✅ Pros
1. **Autonomous Workflows**: Goes beyond search—completes tasks (e.g., submit timesheet, approve request)
2. **Proven Enterprise Adoption**: 250 customers, 5.5M users, 90% full-employee deployment rate
3. **Zero Connector Maintenance**: Moveworks manages 100+ pre-built integrations and API updates
4. **Conversational UX**: Natural language interface lowers barrier to entry vs. traditional search
5. **Fast Time-to-Value**: Turnkey deployment enables production rollout in 4-8 weeks
6. **ServiceNow Synergy**: Deep ITSM/HRSD/CSM workflow integration with no custom code
7. **Enterprise-Trained Models**: Moveworks AI trained on 250+ orgs; understands business jargon

#### ❌ Cons
1. **Highest Per-User Cost**: Premium SaaS pricing (ServiceNow + EmployeeWorks) exceeds DIY options
2. **Dual-Vendor Lock-In**: Tight coupling to ServiceNow + Moveworks (consolidated post-acquisition)
3. **Black Box AI**: Limited visibility into embedding models, retrieval strategies, ranking algorithms
4. **Conversational-First Bias**: May not suit power users who prefer traditional search interfaces
5. **ServiceNow-Centric**: Architecture assumes ServiceNow as central platform; less flexible for non-ServiceNow enterprises
6. **Limited Customization**: Proprietary models and workflows harder to extend than self-managed AWS stack
7. **Future Migration Cost**: Switching away from ServiceNow + Moveworks requires rebuilding conversational AI layer

---

## Decision Criteria for Technical Leaders

### Choose Option A (watsonx) if:
- **Risk tolerance is low**: Cannot afford production disruption during migration
- **Timeline is compressed**: Need RAG capabilities in weeks, not months
- **Team bandwidth is limited**: No capacity for replatforming or learning new technologies
- **IBM roadmap confidence**: Believe watsonx will remain competitive and cost-effective
- **Incremental evolution preferred**: Want to defer big-bet architecture decision

### Choose Option B (AWS MCP) if:
- **Cloud-native strategy is priority**: Want to align search platform with AWS-centric infrastructure
- **Vendor lock-in is unacceptable**: Need flexibility to swap orchestration layers or embedding providers
- **Technical control is critical**: Require fine-grained customization of RAG pipeline, permissions, models
- **Long-term TCO optimization**: Willing to invest upfront for lower 3-5 year operational costs
- **Skill development is feasible**: Team can reskill on Bedrock, OpenSearch, and AWS orchestration

### Choose Option C (Moveworks + ServiceNow) if:
- **User experience is paramount**: Want conversational interface that completes tasks, not just returns links
- **ServiceNow is enterprise standard**: Already invested in ServiceNow ITSM/HRSD; want unified platform
- **Operational simplicity preferred**: Want fully managed SaaS with zero infrastructure overhead
- **Proven adoption is key**: Need platform with demonstrated 90% employee deployment rate
- **Fast time-to-value is critical**: Cannot wait 6-12 months for AWS migration; need production in 4-8 weeks

---

## Technical Recommendations

### For Financial Services Context:
1. **Compliance & Permissions**: Option B (AWS MCP) offers strongest fine-grained isolation (JWT + FGAC) for advisor/FI/employee segmentation
2. **Audit Trail**: Self-managed AWS stack provides deepest visibility into retrieval decisions for regulatory requirements
3. **Risk Management**: Option A (watsonx) minimizes migration risk but increases vendor dependency risk

### For Technical Maturity:
1. **DevOps Capability**: Option B requires advanced AWS expertise; Option A/C tolerate lower technical maturity
2. **Observability Needs**: If deep RAG pipeline instrumentation is critical, Option B provides most control
3. **Innovation Velocity**: Option B enables fastest adoption of new models/techniques; Option C depends on Moveworks roadmap

### For Cost Optimization:
1. **3-Year TCO**: Likely ranking = Option B < Option A < Option C (assuming successful AWS migration)
2. **Budget Flexibility**: Option B's consumption pricing better for variable workloads; Option A/C fixed costs suit stable demand
3. **Hidden Costs**: Factor in Option B's migration effort, Option A's technical debt, Option C's per-user premiums

---

## Sources

### IBM watsonx
- [Coming soon to watsonx.data: OpenRAG](https://www.ibm.com/new/announcements/coming-soon-to-watsonx-data-turn-unstructured-data-into-context-for-ai-with-openrag)
- [IBM announcements at Think 2026](https://www.ibm.com/new/announcements/ibm-announcements-at-think-2026)
- [OpenSearch on watsonx.data](https://www.ibm.com/new/announcements/opensearch-now-available-on-watsonx-data-for-enterprise-search-and-ai-retrieval)
- [AI Enterprise Search – Watsonx Data](https://www.ibm.com/products/watsonx-data/ai-enterprise-search)

### AWS Bedrock & OpenSearch
- [Building Intelligent Search with Amazon Bedrock and Amazon OpenSearch](https://aws.amazon.com/blogs/machine-learning/building-intelligent-search-with-amazon-bedrock-and-amazon-opensearch-for-hybrid-rag-solutions/)
- [How to Build a RAG Application with Amazon Bedrock and OpenSearch](https://oneuptime.com/blog/post/2026-02-12-build-a-rag-application-with-amazon-bedrock-and-opensearch/view)
- [Multi-tenant RAG with Amazon Bedrock and OpenSearch](https://aws.amazon.com/blogs/machine-learning/multi-tenant-rag-implementation-with-amazon-bedrock-and-amazon-opensearch-service-for-saas-using-jwt/)
- [Amazon Bedrock Knowledge Bases now supports OpenSearch](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-knowledge-bases-now-supports-amazon-opensearch-service-managed-cluster-as-vector-store/)

### Moveworks & ServiceNow
- [ServiceNow Adds Moveworks to the AI Platform](https://www.moveworks.com/us/en/company/news/press-releases/servicenow-adds-moveworks-to-the-servicenow-ai-platform)
- [ServiceNow launches Autonomous Workforce, adds Moveworks](https://newsroom.servicenow.com/press-releases/details/2026/ServiceNow-launches-Autonomous-Workforce-that-thinks-and-acts-adds-Moveworks-to-the-ServiceNow-AI-Platform/default.aspx)
- [Introducing ServiceNow EmployeeWorks](https://community.moveworks.com/product-updates/introducing-servicenow-employeeworks-3513)
- [EmployeeWorks: What Moveworks + ServiceNow Means](https://corexcorp.com/insights/the-employeeworks-advantage-what-moveworks-servicenow-signals-for-enterprise)

### Enterprise Search & Architecture
- [Best enterprise AI search platforms 2026](https://www.chapsvision.com/blog/enterprise-ai-search-compared/)
- [AI-Powered ServiceNow Search Engine | Coveo](https://www.coveo.com/en/integrations/servicenow-ai-search)
- [Best Enterprise Search Tools for 2026](https://onyx.app/insights/enterprise-search-tools-2026)
- [Multi-Tenant Architecture](https://clerk.com/blog/how-to-design-multitenant-saas-architecture)

---

**Document Version**: 1.0  
**Analysis Date**: June 5, 2026  
**Target Audience**: Technical stakeholders, Enterprise Architects, Engineering Leadership
