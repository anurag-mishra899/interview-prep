# Enterprise Search Architecture: Technical Comparison Matrix
## RAG-Enabled Search Platform Options for Technical Decision-Makers

---

## Executive Summary Table

| **Evaluation Criteria** | **Option A: watsonx Extension** | **Option B: AWS MCP Cloud-Native** | **Option C: Moveworks EmployeeWorks** |
|------------------------|--------------------------------|-----------------------------------|-------------------------------------|
| **Core Approach** | Incremental Evolution | Full Replatform | Turnkey Conversational AI |
| **Primary Technology** | IBM watsonx + Layered RAG | AWS Bedrock + OpenSearch | ServiceNow + Moveworks |
| **Implementation Time** | 🟢 2-4 weeks | 🔴 6-12 months | 🟢 4-8 weeks |
| **Migration Risk** | 🟢 Lowest | 🔴 Highest | 🟡 Medium |
| **Total Cost (3yr)** | 🟡 Medium | 🟢 Low-Medium | 🔴 Highest |

---

## Detailed Technical Comparison

### 🔍 RAG & Search Architecture

| **Dimension** | **Option A: watsonx** | **Option B: AWS MCP** | **Option C: Moveworks** |
|--------------|----------------------|----------------------|------------------------|
| **Vector Search Maturity** | 🟡 Keyword-first + layered vector<br>OpenRAG framework (2026) | 🟢 Native hybrid search<br>Vector + lexical co-equal | 🟢 Conversational-first<br>Autonomous workflows |
| **Embedding Models** | 🟡 Limited flexibility<br>IBM Granite, AWS Bedrock | 🟢 High flexibility<br>Titan v2, Cohere, custom SageMaker | 🔴 Proprietary<br>Moveworks black box |
| **Hybrid Search** | 🟡 Retrofit architecture<br>Vector secondary to keyword | 🟢 Purpose-built<br>OpenSearch native hybrid | 🟢 Unified conversational<br>Natural language queries |
| **Multi-Step Reasoning** | 🟢 Yes (OpenRAG agentic) | 🟢 Yes (Bedrock agents) | 🟢 Yes (Moveworks autonomous) |
| **Customization Depth** | 🟡 Medium<br>IBM-managed pipelines | 🟢 High<br>Full pipeline control | 🔴 Low<br>Pre-built workflows only |
| **Retrieval Transparency** | 🟡 Medium<br>Some IBM abstraction | 🟢 High<br>Self-managed visibility | 🔴 Low<br>Vendor-managed black box |

### 🔐 Permission & Security

| **Dimension** | **Option A: watsonx** | **Option B: AWS MCP** | **Option C: Moveworks** |
|--------------|----------------------|----------------------|------------------------|
| **Multi-Tenant Isolation** | 🔴 Retrofit required<br>Not natively designed | 🟢 Native support<br>JWT + FGAC from day one | 🟢 Native personas<br>Advisor/employee/FI segments |
| **Fine-Grained Control** | 🔴 Limited<br>Legacy permission model | 🟢 High<br>Document/field/tenant-level | 🟡 Medium<br>ServiceNow RBAC |
| **Permission Transparency** | 🟡 Medium<br>IBM-managed policies | 🟢 High<br>Self-defined IAM + FGAC | 🔴 Low<br>Vendor-managed |
| **Compliance Posture** | 🟢 Mature<br>IBM enterprise heritage | 🟢 Mature<br>AWS FedRAMP, HIPAA, SOC2 | 🟢 Mature<br>ServiceNow + Moveworks certified |
| **Audit Trail** | 🟡 Standard<br>IBM logging | 🟢 Granular<br>CloudWatch, CloudTrail | 🟡 Standard<br>ServiceNow analytics |
| **Data Isolation** | 🔴 Weak<br>Shared keyword index | 🟢 Strong<br>Tenant-level vector stores | 🟡 Medium<br>Cross-system permissions |

### 🔌 Integration & Ecosystem

| **Dimension** | **Option A: watsonx** | **Option B: AWS MCP** | **Option C: Moveworks** |
|--------------|----------------------|----------------------|------------------------|
| **Pre-Built Connectors** | 🟢 90+ IBM-managed | 🟡 55+ (Coveo) + custom | 🟢 100+ Moveworks pre-built |
| **Connector Maintenance** | 🟢 IBM handles updates | 🔴 Self-managed<br>API version tracking | 🟢 Moveworks handles updates |
| **Vendor Lock-In** | 🔴 High<br>IBM-only orchestration | 🟢 Low<br>Multi-vendor, API-first | 🔴 High<br>ServiceNow + Moveworks |
| **Interoperability** | 🟡 Medium<br>IBM ecosystem focus | 🟢 High<br>Cloud-native APIs | 🟡 Medium<br>ServiceNow-centric |
| **Custom Integration Ease** | 🔴 Difficult<br>IBM SDK required | 🟢 Easy<br>REST APIs, Lambda glue | 🔴 Difficult<br>Vendor-dependent |
| **Future-Proofing** | 🔴 IBM roadmap risk | 🟢 Modular architecture<br>Swap components | 🔴 Dual-vendor dependency |

### 🚀 Migration & Implementation

| **Dimension** | **Option A: watsonx** | **Option B: AWS MCP** | **Option C: Moveworks** |
|--------------|----------------------|----------------------|------------------------|
| **Migration Complexity** | 🟢 Lowest<br>Incremental layering | 🔴 Highest<br>Full replatform | 🟡 Medium<br>New UX, turnkey backend |
| **Cutover Window** | 🟢 None<br>Gradual rollout | 🔴 Extended<br>Dual-platform period | 🟡 Short<br>4-8 week implementation |
| **Technical Debt** | 🔴 Increases<br>Layered architecture | 🟢 Decreases<br>Clean slate design | 🟢 Low<br>Managed SaaS |
| **Skill Requirements** | 🟢 Low<br>Existing team expertise | 🔴 High<br>Reskill on Bedrock, OpenSearch | 🟡 Medium<br>ServiceNow + Moveworks admin |
| **Change Management** | 🟢 Minimal<br>Familiar interface | 🔴 Extensive<br>New UX, workflows, training | 🟡 Medium<br>Conversational behavior shift |
| **Rollback Feasibility** | 🟢 Easy<br>Can disable vector layer | 🔴 Difficult<br>Cannot revert to watsonx | 🟡 Medium<br>Revert to ServiceNow native |
| **Time to Production** | 🟢 2-4 weeks | 🔴 6-12 months | 🟢 4-8 weeks |

### 💰 Cost Structure

| **Dimension** | **Option A: watsonx** | **Option B: AWS MCP** | **Option C: Moveworks** |
|--------------|----------------------|----------------------|------------------------|
| **Upfront CapEx** | 🟢 Lowest<br>Reuse existing investment | 🔴 Highest<br>$500K-$2M migration | 🟡 Medium<br>Implementation fees |
| **Annual OpEx (Steady)** | 🟡 $300K-$600K<br>IBM licensing + vector | 🟢 $200K-$400K<br>Consumption-based | 🔴 $500K-$1M+<br>Per-user SaaS |
| **Cost Predictability** | 🟢 High<br>Fixed IBM licensing | 🔴 Low<br>Variable consumption | 🟢 High<br>Per-user pricing |
| **Optimization Potential** | 🔴 Low<br>Fixed IBM pricing | 🟢 High<br>Elastic scaling, reserved capacity | 🔴 Low<br>Fixed per-user tiers |
| **Hidden Costs** | 🔴 High<br>Integration tax, tech debt | 🔴 High<br>Data egress, API calls, ops | 🟡 Medium<br>ServiceNow platform fees |
| **3-Year TCO** | 🟡 $1.5M-$2.5M | 🟢 $1.2M-$2M (after migration) | 🔴 $2M-$3.5M |

### ⚙️ Operational Considerations

| **Dimension** | **Option A: watsonx** | **Option B: AWS MCP** | **Option C: Moveworks** |
|--------------|----------------------|----------------------|------------------------|
| **Infrastructure Management** | 🟡 Medium<br>IBM-managed + vector layer | 🔴 High<br>Self-managed clusters, pipelines | 🟢 Low<br>Fully managed SaaS |
| **Monitoring & Debugging** | 🟡 Standard<br>IBM dashboards | 🟢 Deep<br>CloudWatch, X-Ray, custom | 🔴 Limited<br>Vendor-provided analytics |
| **Model Update Control** | 🔴 IBM-driven<br>Limited version control | 🟢 Self-managed<br>Pin model versions | 🔴 Vendor-driven<br>Automatic updates |
| **Incident Response** | 🟡 Medium<br>IBM support dependency | 🟢 High<br>Full stack visibility | 🔴 Low<br>Vendor black box |
| **Performance Tuning** | 🔴 Limited<br>IBM-managed indexing | 🟢 High<br>Custom sharding, caching | 🔴 Limited<br>Vendor-optimized |
| **Disaster Recovery** | 🟢 IBM-managed<br>Enterprise SLA | 🟡 Self-managed<br>AWS backup tools | 🟢 Vendor-managed<br>ServiceNow SLA |

---

## Summary: Strengths & Weaknesses

### Option A: watsonx Extension (Incremental Evolution)

| **Strengths 🟢** | **Weaknesses 🔴** |
|-----------------|-------------------|
| ✅ Lowest migration risk & fastest implementation (2-4 weeks) | ❌ Technical debt increases with layered architecture |
| ✅ Operational continuity; no team retraining required | ❌ Single-vendor lock-in to IBM roadmap & pricing |
| ✅ OpenRAG framework provides agentic multi-step reasoning | ❌ Retrofit permission model lacks fine-grained isolation |
| ✅ Predictable costs; reuses existing watsonx investment | ❌ Limited embedding model flexibility (Granite-centric) |
| ✅ Familiar tools & workflows for users | ❌ Future migration becomes more expensive over time |
| ✅ IBM-managed connectors (90+) | ❌ Innovation lag behind cloud-native architectures |

### Option B: AWS MCP Cloud-Native (Full Replatform)

| **Strengths 🟢** | **Weaknesses 🔴** |
|-----------------|-------------------|
| ✅ Purpose-built hybrid search (vector + lexical co-equal) | ❌ Highest migration risk & longest timeline (6-12 months) |
| ✅ Vendor flexibility; avoid single-vendor lock-in | ❌ Extended dual-platform period doubles costs |
| ✅ Fine-grained multi-tenant isolation (JWT + FGAC) | ❌ High operational overhead; self-managed infrastructure |
| ✅ High embedding model choice (Titan, Cohere, custom) | ❌ Significant skill gap; team reskilling required |
| ✅ Lowest long-term TCO after migration ($1.2M-$2M/3yr) | ❌ Integration tax; custom glue code for connectors |
| ✅ Deep observability & performance tuning control | ❌ Support fragmentation across AWS, Coveo, ServiceNow |
| ✅ Aligns with cloud-native enterprise strategy | ❌ Upfront CapEx $500K-$2M |

### Option C: Moveworks EmployeeWorks (Conversational AI)

| **Strengths 🟢** | **Weaknesses 🔴** |
|-----------------|-------------------|
| ✅ Autonomous workflows; completes tasks, not just search | ❌ Highest per-user cost ($500K-$1M+ OpEx) |
| ✅ Proven adoption: 90% deploy to 100% of employees | ❌ Dual-vendor lock-in (ServiceNow + Moveworks) |
| ✅ Fast time-to-value (4-8 weeks to production) | ❌ Black box AI; limited visibility into models/ranking |
| ✅ Zero connector maintenance (100+ pre-built) | ❌ Conversational-first bias; may not suit power users |
| ✅ Enterprise-trained models understand business jargon | ❌ ServiceNow-centric; less flexible for non-SN orgs |
| ✅ Natural language interface lowers user barrier | ❌ Limited customization of workflows & permissions |
| ✅ Fully managed SaaS; minimal ops overhead | ❌ Vendor-controlled model updates & feature roadmap |

---

## Decision Framework

### 🎯 Choose Option A (watsonx Extension) if:
- ✅ **Risk tolerance is LOW**: Cannot afford production disruption
- ✅ **Timeline is COMPRESSED**: Need RAG in weeks, not months
- ✅ **Team bandwidth is LIMITED**: No capacity for replatforming
- ✅ **IBM confidence is HIGH**: Trust watsonx roadmap & pricing
- ✅ **Incremental approach preferred**: Want to defer big-bet decision

**Best Fit**: Risk-averse organizations with tight timelines and existing watsonx investment

---

### 🎯 Choose Option B (AWS MCP Cloud-Native) if:
- ✅ **Cloud-native strategy is PRIORITY**: Align with AWS-centric infrastructure
- ✅ **Vendor lock-in is UNACCEPTABLE**: Need multi-vendor flexibility
- ✅ **Technical control is CRITICAL**: Require fine-grained RAG customization
- ✅ **Long-term TCO optimization**: Willing to invest upfront for lower 3-5yr costs
- ✅ **Team can reskill**: DevOps maturity to manage Bedrock/OpenSearch

**Best Fit**: Technically sophisticated orgs with AWS expertise and long-term optimization focus

---

### 🎯 Choose Option C (Moveworks + ServiceNow) if:
- ✅ **User experience is PARAMOUNT**: Want autonomous task completion, not just search
- ✅ **ServiceNow is STANDARD**: Already invested in ServiceNow ITSM/HRSD
- ✅ **Operational simplicity PREFERRED**: Want fully managed SaaS
- ✅ **Proven adoption is KEY**: Need platform with 90% deployment track record
- ✅ **Fast time-to-value CRITICAL**: Cannot wait 6-12 months

**Best Fit**: ServiceNow-centric orgs prioritizing UX and rapid deployment over cost optimization

---

## Technical Recommendations by Context

### For Financial Services (Advisor/FI/Employee Segmentation):
| Requirement | Recommendation |
|------------|---------------|
| **Compliance & Permissions** | 🥇 **Option B** (JWT + FGAC strongest)<br>🥈 Option C (persona-native)<br>🥉 Option A (retrofit) |
| **Audit Trail** | 🥇 **Option B** (self-managed visibility)<br>🥈 Option A (IBM logging)<br>🥉 Option C (vendor black box) |
| **Data Isolation** | 🥇 **Option B** (tenant-level vector stores)<br>🥈 Option C (cross-system permissions)<br>🥉 Option A (shared index) |

### For DevOps Maturity:
| Capability Level | Recommendation |
|-----------------|---------------|
| **High (Advanced AWS)** | 🥇 **Option B** - Maximize control & optimization |
| **Medium (Standard IT)** | 🥇 **Option C** - Managed SaaS simplicity<br>🥈 Option A - Incremental watsonx |
| **Low (Limited Ops)** | 🥇 **Option C** - Zero infrastructure burden<br>🥈 Option A - Familiar IBM tools |

### For Budget Scenarios:
| Budget Constraint | Recommendation |
|------------------|---------------|
| **Minimal Upfront CapEx** | 🥇 **Option A** ($50K-$100K)<br>🥈 Option C ($200K-$400K)<br>🥉 Option B ($500K-$2M) |
| **Lowest 3-Year TCO** | 🥇 **Option B** ($1.2M-$2M)<br>🥈 Option A ($1.5M-$2.5M)<br>🥉 Option C ($2M-$3.5M) |
| **Cost Predictability** | 🥇 **Option C** (per-user SaaS)<br>🥈 Option A (fixed IBM)<br>🥉 Option B (variable consumption) |

---

## Color Legend
- 🟢 **Green**: Strong capability / Low risk / Best-in-class
- 🟡 **Yellow**: Medium capability / Moderate risk / Acceptable
- 🔴 **Red**: Weak capability / High risk / Significant limitation

---

## Sources

**IBM watsonx:**
- [OpenRAG on watsonx.data](https://www.ibm.com/new/announcements/coming-soon-to-watsonx-data-turn-unstructured-data-into-context-for-ai-with-openrag) | [Think 2026 Announcements](https://www.ibm.com/new/announcements/ibm-announcements-at-think-2026) | [OpenSearch Integration](https://www.ibm.com/new/announcements/opensearch-now-available-on-watsonx-data-for-enterprise-search-and-ai-retrieval)

**AWS Bedrock & OpenSearch:**
- [Hybrid RAG Solutions](https://aws.amazon.com/blogs/machine-learning/building-intelligent-search-with-amazon-bedrock-and-amazon-opensearch-for-hybrid-rag-solutions/) | [Multi-Tenant RAG](https://aws.amazon.com/blogs/machine-learning/multi-tenant-rag-implementation-with-amazon-bedrock-and-amazon-opensearch-service-for-saas-using-jwt/) | [Knowledge Bases Guide](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-knowledge-bases-now-supports-amazon-opensearch-service-managed-cluster-as-vector-store/)

**Moveworks & ServiceNow:**
- [EmployeeWorks Launch](https://newsroom.servicenow.com/press-releases/details/2026/ServiceNow-launches-Autonomous-Workforce-that-thinks-and-acts-adds-Moveworks-to-the-ServiceNow-AI-Platform/default.aspx) | [Acquisition Details](https://www.moveworks.com/us/en/company/news/press-releases/servicenow-completes-acquisition-of-moveworks) | [Enterprise Impact](https://corexcorp.com/insights/the-employeeworks-advantage-what-moveworks-servicenow-signals-for-enterprise)

**Market Analysis:**
- [Enterprise AI Search 2026](https://www.chapsvision.com/blog/enterprise-ai-search-compared/) | [Coveo Integration](https://www.coveo.com/en/integrations/servicenow-ai-search) | [Multi-Tenant Architecture](https://clerk.com/blog/how-to-design-multitenant-saas-architecture)

---

**Document Version**: 1.1  
**Analysis Date**: June 5, 2026  
**Target Audience**: Technical Leadership, Enterprise Architects, Engineering Managers  
**Format**: Technical Comparison - Single Consolidated Table View
