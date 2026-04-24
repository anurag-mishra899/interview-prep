# Spec-Driven Development: Quick Start Guide

**Decision Trees, Templates & Practical Checklists**

---

## 📋 Table of Contents

1. [Decision Tree: Which Approach?](#1-decision-tree-which-approach)
2. [Context-Specific Quick Starts](#2-context-specific-quick-starts)
3. [Universal Templates](#3-universal-templates)
4. [Checklists](#4-checklists)
5. [Common Pitfalls](#5-common-pitfalls)
6. [Success Patterns](#6-success-patterns)

---

## 1. Decision Tree: Which Approach?

### Start Here: What's Your Situation?

```
┌─────────────────────────────────────────────────────────────┐
│ START: What are you building?                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┴───────────────────┐
        │                                       │
    New Project?                        Existing Codebase?
        │                                       │
        ↓                                       ↓
  GREENFIELD ───→ Go to Section A      BROWNFIELD/LEGACY ───→ Continue
                                                │
                                                ↓
                                    Is it actively maintained?
                                                │
                        ┌───────────────────────┴────────────┐
                        │                                    │
                    YES: Active                          NO: Legacy
                        │                                    │
                        ↓                                    ↓
                    BROWNFIELD                           LEGACY
                  Go to Section B                    Go to Section C


┌─────────────────────────────────────────────────────────────┐
│ SECTION A: GREENFIELD DECISION TREE                         │
└─────────────────────────────────────────────────────────────┘

What's the project type?
│
├─ Prototype/POC → Use: Spec-First (Disposable)
│                  Time: 1-2 days
│                  Commit: Low
│                  Template: QUICK_SPEC_TEMPLATE
│
├─ Production App → Use: Spec-Anchored
│                   Time: 1-2 weeks for setup
│                   Commit: Medium
│                   Template: FULL_GREENFIELD_TEMPLATE
│
└─ Strategic Platform → Use: Spec-Anchored + Select Spec-as-Source
                        Time: 1 month for setup
                        Commit: High
                        Template: ENTERPRISE_GREENFIELD_TEMPLATE


┌─────────────────────────────────────────────────────────────┐
│ SECTION B: BROWNFIELD DECISION TREE                         │
└─────────────────────────────────────────────────────────────┘

How much can you change?
│
├─ New Features Only → Use: Parallel SDD + Traditional
│                       Time: 1 week setup
│                       Commit: Low
│                       Template: BROWNFIELD_ADDITIVE_TEMPLATE
│
├─ New + Refactor → Use: Hybrid SDD + Reverse Engineering
│                    Time: 2-4 weeks setup
│                    Commit: Medium
│                    Template: BROWNFIELD_HYBRID_TEMPLATE
│
└─ Full Modernization → Use: Legacy Migration Approach
                         Time: 1-3 months setup
                         Commit: High
                         Template: See Section C


┌─────────────────────────────────────────────────────────────┐
│ SECTION C: LEGACY DECISION TREE                             │
└─────────────────────────────────────────────────────────────┘

What's the migration goal?
│
├─ Feature Parity → Use: Parity Specs + Strangler Fig
│                    Time: 3-6 months per module
│                    Commit: High
│                    Template: LEGACY_PARITY_TEMPLATE
│
├─ Tech Stack Pivot → Use: Experimental Specs + Parallel Implementation
│                      Time: 2-4 months for POC
│                      Commit: Very High
│                      Template: LEGACY_PIVOT_TEMPLATE
│
└─ Incremental Modernization → Use: Selective Migration
                                Time: 6-12 months
                                Commit: High
                                Template: LEGACY_INCREMENTAL_TEMPLATE
```

---

## 2. Context-Specific Quick Starts

### 2.1 Greenfield Quick Start (30 Minutes)

**Use when:** Starting a new project from scratch

**Steps:**

```bash
# 1. Create structure (5 min)
mkdir -p my-project/specs/{_meta,features,templates}
mkdir -p my-project/src/{libs,apps}
mkdir -p my-project/tests

cd my-project

# 2. Copy constitution template (2 min)
curl -o specs/_meta/CONSTITUTION.md https://raw.githubusercontent.com/[YOUR_TEMPLATES]/CONSTITUTION.md

# OR create minimal version:
cat > specs/_meta/CONSTITUTION.md << 'EOF'
# Principles

1. **Spec-First:** Write specs before code
2. **Test-First:** Write tests before implementation
3. **Simplicity:** Justify complexity
4. **Security:** Threat model sensitive features
5. **Contracts:** Define APIs before implementation
EOF

# 3. Create first feature spec (10 min with AI)
# Prompt your AI: "Using this template, create spec for [feature]"

# 4. Implement (varies)
# Follow Test → Implement → Validate cycle

# 5. Commit everything (1 min)
git add specs/ src/ tests/
git commit -m "feat: Initial SDD setup + first feature"
```

**Total Time:** 30 min setup + feature implementation time

**Deliverable:** Working SDD project structure

---

### 2.2 Brownfield Quick Start (1 Hour)

**Use when:** Adding SDD to existing active codebase

**Steps:**

```bash
# 1. Add specs workspace (5 min)
cd existing-project
mkdir -p specs/{_meta,features,existing,templates}

# 2. Document existing state (15 min with AI)
# Prompt: "Analyze my codebase structure and create EXISTING_ARCH.md"

cat > specs/_meta/EXISTING_ARCH.md << 'EOF'
# Current Architecture

## Stack
- [Your current tech stack]

## Structure
- [Current folder structure]

## Pain Points
- [Known issues]

## Constraints
- [What can't change]
EOF

# 3. Create migration strategy (10 min)
cat > specs/_meta/MIGRATION_STRATEGY.md << 'EOF'
# SDD Adoption Plan

## Phase 1 (Month 1-3): New Features Only
- NEW work uses SDD
- EXISTING code unchanged

## Phase 2 (Month 4-6): Selective Reverse Engineering
- Document top 5 critical features
- Use specs to guide refactoring

## Success Criteria
- 100% new features have specs by Month 3
- Top 5 features documented by Month 6
EOF

# 4. First new feature with SDD (20 min + implementation)
mkdir specs/features/001-new-feature
# Create SPEC.md following template
# Document integration points with existing code

# 5. Commit specs workspace (5 min)
git add specs/
git commit -m "chore: Add SDD workspace for new features"
```

**Total Time:** 1 hour setup + feature implementation

**Key Difference from Greenfield:** Focus on integration points and backwards compatibility

---

### 2.3 Legacy Migration Quick Start (4 Hours)

**Use when:** Migrating from legacy system to modern stack

**Steps:**

```bash
# 1. Create migration workspace (10 min)
mkdir -p legacy-migration/{legacy,specs,modern,migration}
cd legacy-migration

# 2. Archive legacy (read-only) (5 min)
cp -r /path/to/legacy legacy/

# 3. Analyze legacy behavior (1 hour with AI)
# Prompt: "Analyze legacy system and document behavior"

cat > specs/_meta/LEGACY_CONTEXT.md << 'EOF'
# Legacy System Analysis

## Technology Stack
- [Legacy tech]

## Business Rules
- [Rules embedded in code]

## Data Model
- [Database schema]

## Integration Points
- [External dependencies]

## Known Issues
- [Problems to fix in migration]
EOF

# 4. Define parity requirements (30 min)
cat > specs/_meta/PARITY_REQUIREMENTS.md << 'EOF'
# Feature Parity Checklist

## MUST Maintain (Critical)
- [Exact behaviors to preserve]

## Should Maintain (Important)
- [Intent to preserve, can improve]

## Intentional Changes
- [What we're fixing]

## Validation Strategy
- Parity tests for each feature
EOF

# 5. First module migration spec (1 hour)
mkdir -p specs/features/001-user-module
# Create SPEC.md documenting legacy behavior
# Create PARITY_CHECKLIST.md
# Create DESIGN.md for modern implementation

# 6. Create migration scripts (30 min)
mkdir -p migration/{data,cutover,validation}

cat > migration/cutover/phase1-readonly.sh << 'EOF'
#!/bin/bash
# Phase 1: Legacy writes, modern reads (validation)
echo "Deploying modern service in read-only mode..."
EOF

# 7. Implement first module (varies by complexity)
mkdir modern/services/user-service
# Implement following modern DESIGN.md
# Create parity tests

# 8. Commit migration workspace (5 min)
git add .
git commit -m "chore: Initialize legacy migration workspace"
```

**Total Time:** 4 hours setup + module implementation (weeks)

**Key Outputs:**
- Legacy behavior documented
- Parity requirements defined
- First module spec created
- Migration automation scaffolded

---

## 3. Universal Templates

### 3.1 CONSTITUTION Template

```markdown
# [Project Name] Constitution

## Preamble
This document defines immutable principles guiding all development.

## Article I: Specification Primacy
**Principle:** Specifications are the source of truth.

**Requirements:**
- Every feature MUST have a specification
- Specs MUST be reviewed before implementation
- Code changes MUST update specs first

**Exceptions:** Hotfixes (document retroactively within 24 hours)

## Article II: Test-First Development
**Principle:** Tests validate specifications.

**Requirements:**
- Tests MUST be written before implementation code
- Tests MUST validate acceptance criteria from specs
- Test coverage MUST be ≥80% for spec-driven code

**Verification:** CI blocks merge if coverage <80%

## Article III: Contract-First Design
**Principle:** APIs and data models are defined before implementation.

**Requirements:**
- APIs MUST have OpenAPI/GraphQL schema
- Databases MUST have DDL schema in specs
- Events MUST have JSON Schema definitions

**Validation:** Contract tests run in CI

## Article IV: Simplicity First
**Principle:** Complexity must be justified.

**Requirements:**
- Start with ≤3 dependencies per feature
- Document rationale for each dependency in DESIGN.md
- Track complexity budget in DESIGN.md

**Escalation:** >5 dependencies requires architect approval

## Article V: Security First
**Principle:** Security is not optional.

**Requirements:**
- Features handling PII MUST include threat model
- Security review required before implementation
- OWASP Top 10 mitigation documented

**Enforcement:** Security checklist in DESIGN.md template

## Article VI: Progressive Formalization
**Principle:** Match spec formality to feature importance.

**Levels:**
- **Spec-First:** Prototypes (disposable specs)
- **Spec-Anchored:** Production (maintained specs)
- **Spec-as-Source:** Strategic (generative specs)

**Guidance:** See WORKFLOWS.md for level selection

## Amendment Process
This constitution may be amended by:
1. Team consensus (>80% approval)
2. Documented rationale (ADR)
3. Backwards compatibility assessment
4. Update version and date

---

**Version:** 1.0
**Adopted:** [Date]
**Last Amended:** [Date]
```

---

### 3.2 SPEC Template (Feature Specification)

```markdown
# Feature [NNN]: [Feature Name]

> **Status:** [Draft | Review | Approved | Implemented]
> **Owner:** [Team/Person]
> **Created:** [Date]
> **Last Updated:** [Date]

## Overview
[2-3 sentence description of what this feature does and why it matters]

## Context
[Background information, problem statement, or motivation]

## User Stories

### Story [N.1]: [Story Title]
**As a** [actor/role]
**I want to** [action/capability]
**So that** [benefit/value]

**Acceptance Criteria:**
1. [Testable criterion - Given/When/Then format preferred]
2. [Testable criterion]
3. [Testable criterion]

**Priority:** [Critical | High | Medium | Low]

### Story [N.2]: [Story Title]
[... repeat structure ...]

## Non-Functional Requirements

### Performance
- [Metric with target, e.g., "Response time <200ms at p95"]
- [Load capacity, e.g., "Support 1000 concurrent users"]

### Security
- [Security requirement, e.g., "All data encrypted at rest"]
- [Compliance requirement, e.g., "GDPR compliant data handling"]

### Scalability
- [Scaling requirement, e.g., "Horizontal scaling to 10 instances"]

### Availability
- [Uptime target, e.g., "99.9% uptime SLA"]

### Compliance
- [Regulatory requirement, e.g., "SOC2 Type II compliant"]

## Assumptions
- [Assumption that affects design or implementation]
- [External dependency assumption]

## Constraints
- [Technical constraint, e.g., "Must use existing auth system"]
- [Business constraint, e.g., "Launch by Q2 2026"]

## Dependencies
- [Dependency on other features/systems]
- [External service dependency]

## Out of Scope
- [Future work explicitly excluded from this spec]
- [Alternative approaches not pursued (with rationale)]

## Success Metrics
- [Quantifiable metric, e.g., "80% user adoption within 2 months"]
- [Business metric, e.g., "20% reduction in support tickets"]

## Questions & Clarifications
- [ ] [NEEDS CLARIFICATION: Specific question]
- [ ] [NEEDS CLARIFICATION: Specific question]

**Clarification Log:**
| Question | Answer | Date | Answered By |
|----------|--------|------|-------------|
| [Question] | [Answer] | [Date] | [Person] |

## References
- [Link to related specs]
- [Link to external documentation]
- [Link to design docs]

---

**Review Checklist:**
- [ ] All user stories have testable acceptance criteria
- [ ] Non-functional requirements specified
- [ ] No `[NEEDS CLARIFICATION]` markers remain
- [ ] Success metrics defined
- [ ] Out of scope explicitly stated
```

---

### 3.3 DESIGN Template (Implementation Plan)

```markdown
# Feature [NNN]: [Feature Name] - Design

> **Spec:** [Link to SPEC.md]
> **Status:** [Draft | Review | Approved]
> **Author:** [Name]
> **Date:** [Date]

## High-Level Design

### Architecture Diagram
```
[ASCII diagram or link to diagram]
```

### Component Overview
[Description of major components and their responsibilities]

## Component Architecture

### Component 1: [Name]
**Responsibility:** [What this component does]

**Location:** `src/libs/[component-name]/`

**Structure:**
```
[component-name]/
├── src/
│   ├── index.ts
│   ├── [module].ts
│   └── [module].ts
├── tests/
└── package.json
```

**Public API:**
```typescript
// Key functions/classes exposed
export function functionName(param: Type): ReturnType;
export class ClassName { ... }
```

### Component 2: [Name]
[... repeat structure ...]

## Data Model

### Database Schema
```sql
-- Table definitions
CREATE TABLE table_name (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    column1 TYPE CONSTRAINTS,
    column2 TYPE CONSTRAINTS,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_column ON table_name(column);

-- Foreign Keys
ALTER TABLE table_name
    ADD CONSTRAINT fk_name FOREIGN KEY (column) REFERENCES other_table(id);
```

### Entity Relationships
```
[Entity-Relationship diagram or description]
```

### Data Migration Plan
[If modifying existing schema, document migration approach]

## API Contracts

### REST API (OpenAPI)
**Location:** `CONTRACTS/api.yaml`

**Key Endpoints:**
- `POST /api/v1/[resource]` - [Description]
- `GET /api/v1/[resource]/:id` - [Description]
- `PUT /api/v1/[resource]/:id` - [Description]
- `DELETE /api/v1/[resource]/:id` - [Description]

[Link to full OpenAPI spec in CONTRACTS/]

### GraphQL Schema
[If using GraphQL, include schema here or link to CONTRACTS/schema.graphql]

### Events (Async Communication)
**Location:** `CONTRACTS/events.json`

```json
{
  "eventType": "entity.action.v1",
  "schema": {
    "type": "object",
    "properties": {
      "field": { "type": "string" }
    }
  }
}
```

## Dependencies

### New Dependencies
| Package | Version | Purpose | Justification | Complexity |
|---------|---------|---------|---------------|------------|
| [name] | [version] | [purpose] | [why needed] | [Low/Med/High] |

**Total Dependencies:** [count] (Budget: ≤3 per Article IV)

### Existing Dependencies
[Dependencies from existing project that will be used]

## Security Analysis

### Threat Model (STRIDE)
- **Spoofing:** [Threat + Mitigation]
- **Tampering:** [Threat + Mitigation]
- **Repudiation:** [Threat + Mitigation]
- **Information Disclosure:** [Threat + Mitigation]
- **Denial of Service:** [Threat + Mitigation]
- **Elevation of Privilege:** [Threat + Mitigation]

### OWASP Top 10 Mitigation
1. **Broken Access Control:** [How mitigated]
2. **Cryptographic Failures:** [How mitigated]
3. **Injection:** [How mitigated]
[... continue for all 10 ...]

### Security Checklist
- [ ] Input validation on all user inputs
- [ ] Output encoding to prevent XSS
- [ ] Parameterized queries to prevent SQL injection
- [ ] Authentication on protected endpoints
- [ ] Authorization checks before data access
- [ ] HTTPS only (no HTTP)
- [ ] Secrets in environment variables (not code)
- [ ] Rate limiting on public endpoints

## Performance Considerations

### Expected Load
- Requests per second: [estimate]
- Concurrent users: [estimate]
- Data volume: [estimate]

### Performance Targets
- Response time: [target at p50, p95, p99]
- Throughput: [requests/second]
- Resource usage: [CPU, memory limits]

### Optimization Strategies
- [Caching strategy]
- [Database query optimization]
- [Background job processing]

## Error Handling

### Error Scenarios
| Scenario | HTTP Status | Error Response | User Impact |
|----------|-------------|----------------|-------------|
| [Scenario] | [Status] | [Response format] | [What user sees] |

### Logging Strategy
- **Info:** [What to log at INFO level]
- **Warn:** [What to log at WARN level]
- **Error:** [What to log at ERROR level]

## Testing Strategy

### Unit Tests
- [What components need unit tests]
- Target coverage: ≥80%

### Integration Tests
- [What integration points to test]
- [External service mocking strategy]

### Contract Tests
- API contract validation (OpenAPI spec)
- Event schema validation (JSON Schema)

### End-to-End Tests
- [Critical user flows to test]

## Deployment Strategy

### Environments
- **Development:** [Configuration]
- **Staging:** [Configuration]
- **Production:** [Configuration]

### Feature Flags
- [Feature flag name]: [Purpose, rollout plan]

### Rollout Plan
1. [Phase 1: Canary to 1% of users]
2. [Phase 2: Gradual rollout to 10%, 50%, 100%]
3. [Phase 3: Full deployment]

### Rollback Plan
- [Conditions triggering rollback]
- [Rollback procedure]
- [Maximum rollback time: X minutes]

## Monitoring & Observability

### Metrics
- [Business metric to track]
- [Technical metric to track]

### Alerts
- [Alert condition + severity + escalation]

### Dashboards
- [Key metrics dashboard]

## Constitutional Compliance

### Article I: Specification Primacy ✅
- [How this design follows spec]

### Article II: Test-First Development ✅
- [Test strategy defined above]

### Article III: Contract-First Design ✅
- [Contracts defined in CONTRACTS/]

### Article IV: Simplicity First ✅
- Dependencies: [count] ≤ 3 ✅ | > 3 ❌ [justification]

### Article V: Security First ✅
- Threat model: [Status]
- Security checklist: [Status]

## Open Questions
- [ ] [Question requiring decision]
- [ ] [Question requiring decision]

## Alternatives Considered
### Alternative 1: [Approach Name]
**Pros:** [Benefits]
**Cons:** [Drawbacks]
**Decision:** ❌ Not chosen because [reason]

### Alternative 2: [Approach Name]
**Decision:** ✅ Chosen because [reason]

---

**Review Checklist:**
- [ ] All components defined
- [ ] Data model complete
- [ ] API contracts in CONTRACTS/
- [ ] Security analysis complete
- [ ] Dependencies justified
- [ ] Constitutional compliance verified
```

---

### 3.4 INTEGRATION_POINTS Template (Brownfield)

```markdown
# Feature [NNN]: Integration Points with Existing System

> **Spec:** [Link to SPEC.md]
> **Existing Code:** [Files/modules affected]

## Overview
This feature integrates with the existing codebase in [number] places.

## Integration Point 1: [Name]

### Existing Code
**File:** `src/[path]/[file].js`
**Line:** [Line number]

**Current Implementation:**
```javascript
// Existing code that will be modified
exports.functionName = async (req, res) => {
  // Current logic
  res.json(result);
};
```

### Required Changes
**Type:** [Minimal Change | Refactor | Extension]

**New Code:**
```javascript
// Modified code
const NewService = require('../services/new-feature');

exports.functionName = async (req, res) => {
  // Current logic (unchanged)

  // ⭐ NEW: Integration point
  await NewService.handleEvent(result);

  res.json(result);
};
```

### Integration Contract
**Input:** [What new feature receives from existing code]
**Output:** [What new feature returns]
**Error Handling:** [How errors are propagated]

### Backwards Compatibility
✅ Existing behavior unchanged
✅ New functionality is additive
✅ Can be feature-flagged
✅ Existing tests continue to pass

---

## Integration Point 2: [Name]
[... repeat structure ...]

---

## Testing Strategy

### Integration Tests
```javascript
// Test that new feature integrates correctly
describe('Integration: NewFeature + ExistingModule', () => {
  it('should trigger new feature when existing module updates', async () => {
    // Call existing endpoint
    const response = await request.post('/api/existing');

    // Verify existing behavior unchanged
    expect(response.status).toBe(200);

    // Verify new feature was triggered
    expect(NewService.handleEvent).toHaveBeenCalled();
  });
});
```

### Regression Tests
- [ ] All existing unit tests pass
- [ ] All existing integration tests pass
- [ ] No performance degradation

## Rollout Plan

### Phase 1: Feature Flag OFF
- Deploy new code
- Feature flag OFF (no new behavior)
- Validate existing functionality

### Phase 2: Internal Testing
- Feature flag ON for internal users only
- Validate integration works correctly

### Phase 3: Gradual Rollout
- 1% of users → 10% → 50% → 100%
- Monitor for issues at each stage

### Rollback
- Feature flag OFF immediately reverts to old behavior
- No code deployment needed for rollback

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk description] | [Low/Med/High] | [Low/Med/High] | [Mitigation strategy] |

---

**Review Checklist:**
- [ ] All integration points documented
- [ ] Backwards compatibility verified
- [ ] Integration tests defined
- [ ] Rollback plan clear
- [ ] Feature flag configured
```

---

## 4. Checklists

### 4.1 Spec Quality Checklist

Before merging a spec, verify:

**Completeness:**
- [ ] Overview explains what and why
- [ ] All user stories have actors, actions, benefits
- [ ] Acceptance criteria are testable (can write automated tests)
- [ ] Non-functional requirements specified (performance, security, etc.)
- [ ] Out of scope explicitly stated
- [ ] Success metrics defined (how we measure success)

**Clarity:**
- [ ] No ambiguous language ("should", "might", "probably")
- [ ] All `[NEEDS CLARIFICATION]` markers resolved
- [ ] Domain terms defined (or in GLOSSARY.md)
- [ ] Examples provided for complex behaviors
- [ ] Diagrams included where helpful

**Testability:**
- [ ] Each acceptance criterion maps to a test
- [ ] Edge cases documented
- [ ] Error scenarios defined
- [ ] Contract files created (OpenAPI, JSON Schema, SQL DDL)

**Maintainability:**
- [ ] Versioned (date, status)
- [ ] Owner assigned
- [ ] References to related specs/docs
- [ ] Review by at least one other person

### 4.2 Design Quality Checklist

Before implementing, verify design has:

**Architecture:**
- [ ] Component diagram (visual representation)
- [ ] Component responsibilities clear
- [ ] Integration points defined
- [ ] Data flow documented

**Contracts:**
- [ ] API contracts in machine-readable format (OpenAPI, GraphQL)
- [ ] Data model with DDL (SQL schema)
- [ ] Event schemas if async communication

**Security:**
- [ ] Threat model (STRIDE analysis)
- [ ] OWASP Top 10 mitigation
- [ ] Security checklist complete

**Dependencies:**
- [ ] All dependencies listed
- [ ] Each dependency justified
- [ ] Complexity within budget (≤3 unless justified)

**Constitutional Compliance:**
- [ ] All constitutional articles addressed
- [ ] Exceptions documented with rationale

### 4.3 Implementation Checklist

**Before Starting:**
- [ ] Spec reviewed and approved
- [ ] Design reviewed and approved
- [ ] Tasks generated and ordered
- [ ] Development environment ready

**During Implementation:**
- [ ] Follow Test-First (tests before code)
- [ ] Validate tests FAIL before implementing (red phase)
- [ ] Implement minimum code to pass (green phase)
- [ ] Refactor for quality (refactor phase)
- [ ] Commit frequently with clear messages

**Before PR:**
- [ ] All acceptance criteria tests pass
- [ ] Contract tests pass (API/data schemas validated)
- [ ] Code coverage ≥80%
- [ ] Security scan clean
- [ ] Performance meets targets
- [ ] Spec still accurate (update if implementation diverged)

**PR Review:**
- [ ] Code reviewed by at least one peer
- [ ] Spec reviewed if updated
- [ ] CI/CD checks pass
- [ ] Documentation updated

---

## 5. Common Pitfalls

### ❌ Pitfall 1: Over-Specifying Too Early

**Symptom:** Spec includes implementation details (tech stack, class names, algorithms)

**Problem:** Limits AI creativity, locks in decisions prematurely

**Solution:**
- In SPEC.md: Focus on WHAT and WHY only
- In DESIGN.md: Specify HOW (tech stack, architecture)
- Keep them separate

**Example (Wrong):**
```markdown
## User Registration
Users should register using a React form that calls a Node.js API
which stores data in PostgreSQL using Prisma ORM with bcrypt hashing.
```

**Example (Right):**
```markdown
# SPEC.md
## User Registration
Users should be able to create an account with email and password.

# DESIGN.md
## Technology
- Frontend: React
- Backend: Node.js
- Database: PostgreSQL
- ORM: Prisma
- Hashing: bcrypt
```

---

### ❌ Pitfall 2: Under-Clarifying

**Symptom:** Spec has vague acceptance criteria, AI makes wrong assumptions

**Problem:** Implementation doesn't match intent

**Solution:**
- Use `[NEEDS CLARIFICATION]` liberally
- Include examples for complex behaviors
- Define edge cases explicitly

**Example (Wrong):**
```markdown
Passwords should be secure.
```

**Example (Right):**
```markdown
## Password Requirements
- Minimum 12 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character (!@#$%^&*)
- Not in common password list (top 10,000)
- Different from last 3 passwords

[NEEDS CLARIFICATION: Should we enforce password expiration? If yes, how often?]
```

---

### ❌ Pitfall 3: Ignoring Constitutional Principles

**Symptom:** Features violate constitution, technical debt accumulates

**Problem:** Inconsistency across codebase, quality degradation

**Solution:**
- Review constitution before every feature
- Include constitutional compliance section in DESIGN.md
- Automated checks in CI/CD

**Example:**
```markdown
## Constitutional Compliance

❌ Article IV (Simplicity): Using 7 dependencies (budget is 3)
**Justification:** Complex payment processing requires specialized libraries
**Approval:** [Architect Name] approved on [Date]
**Trade-off:** Accept complexity for PCI-DSS compliance

✅ All other articles compliant
```

---

### ❌ Pitfall 4: Spec-Code Drift

**Symptom:** Spec says one thing, code does another

**Problem:** Specs become useless, trust in SDD erodes

**Solution:**
- Automated drift detection (compare API contracts to actual code)
- Require spec update in every PR that changes behavior
- Periodic spec review (monthly)

**Prevention:**
```bash
# CI/CD script
npm run test:contract  # Validates OpenAPI spec matches actual API
npm run test:parity    # Validates behavior matches spec acceptance criteria

# Fail PR if drift detected
```

---

### ❌ Pitfall 5: Retrofitting Entire Brownfield Codebase

**Symptom:** Team tries to create specs for all existing code at once

**Problem:** Overwhelming, low ROI, blocks new work

**Solution:**
- NEW features only (Phase 1)
- Reverse engineer only critical paths (Phase 2)
- Accept that some code won't have specs

**Rule:**
- If code changes frequently → spec it
- If code is stable → leave it

---

## 6. Success Patterns

### ✅ Pattern 1: Start Small, Prove Value

**Approach:**
1. One feature (greenfield spike)
2. Measure time saved vs. traditional
3. Assess quality improvement
4. Team retrospective
5. If positive → scale; if not → adjust

**Timeline:** 1-2 weeks

**Success Metric:** Team votes >7/10 on "would use again"

---

### ✅ Pattern 2: Spec Review Culture

**Approach:**
- Treat specs like code (peer review required)
- Use PR templates with spec checklist
- Review BEFORE implementation starts
- Dedicated "spec reviewer" role (rotates)

**Benefits:**
- Catches issues early (cheapest time to fix)
- Spreads knowledge across team
- Improves spec writing skills

---

### ✅ Pattern 3: Constitutional Discipline

**Approach:**
- Print constitution on wall (physical reminder)
- Include in onboarding for all new devs
- Monthly "constitutional review" (are we following it?)
- Amendment process for evolution

**Benefits:**
- Consistent quality across features
- Shared understanding of "how we work"
- Prevents slow quality degradation

---

### ✅ Pattern 4: Automated Validation

**Approach:**
```yaml
# CI/CD pipeline
steps:
  - name: Validate Spec Completeness
    run: |
      # Check no [NEEDS CLARIFICATION] markers
      if grep -r "NEEDS CLARIFICATION" specs/; then
        echo "Spec has unresolved clarifications"
        exit 1
      fi

  - name: Validate Contracts
    run: |
      # Validate OpenAPI spec
      npx @openapitools/openapi-generator-cli validate -i specs/features/*/CONTRACTS/*.yaml

  - name: Contract Tests
    run: |
      # Validate implementation matches contracts
      npm run test:contract

  - name: Parity Tests (for brownfield/legacy)
    run: |
      # Validate new implementation matches legacy behavior
      npm run test:parity
```

**Benefits:**
- Catches drift automatically
- Enforces spec quality
- Reduces manual review burden

---

### ✅ Pattern 5: Living Documentation

**Approach:**
- Specs double as user documentation
- Generate API docs from OpenAPI specs
- Link specs from code comments
- Specs in same repo as code (versioned together)

**Example:**
```javascript
/**
 * User registration endpoint
 *
 * @spec specs/features/001-auth/SPEC.md#story-11-user-registration
 * @contract specs/features/001-auth/CONTRACTS/auth-api.yaml#/paths/~1auth~1register
 */
app.post('/auth/register', registerHandler);
```

**Benefits:**
- Docs never out of date (because they're the source)
- Developers reference specs (not outdated wiki)
- Onboarding uses specs (understand features quickly)

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│ SDD IN 5 STEPS                                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 1. WRITE SPEC (What & Why)                                  │
│    → User stories, acceptance criteria, success metrics    │
│    → Review with stakeholders                               │
│                                                             │
│ 2. CLARIFY (Resolve Ambiguities)                            │
│    → Mark [NEEDS CLARIFICATION]                             │
│    → Get answers, update spec                               │
│                                                             │
│ 3. DESIGN (How)                                             │
│    → Component architecture, data model, API contracts      │
│    → Security analysis, dependency justification            │
│    → Review with architects                                 │
│                                                             │
│ 4. IMPLEMENT (Test-First)                                   │
│    → Write tests (from acceptance criteria)                 │
│    → Implement minimum code to pass                         │
│    → Refactor for quality                                   │
│                                                             │
│ 5. VALIDATE (Against Spec)                                  │
│    → All acceptance criteria pass                           │
│    → Contract tests pass                                    │
│    → Performance/security targets met                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ KEY PRINCIPLES                                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 1. Specs Are Contracts (not documentation)                  │
│ 2. Test-First (validate before implement)                   │
│ 3. Progressive Formalization (match rigor to importance)    │
│ 4. Simplicity First (justify complexity)                    │
│ 5. Context Matters (greenfield ≠ brownfield ≠ legacy)      │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ COMMON MISTAKES TO AVOID                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ❌ Over-specify (implementation details in SPEC.md)         │
│ ❌ Under-clarify (vague acceptance criteria)                │
│ ❌ Ignore constitution (inconsistent quality)               │
│ ❌ Spec-code drift (spec outdated vs. code)                 │
│ ❌ Retrofit everything (overwhelm in brownfield)            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Next Steps

**Choose Your Path:**

1. **Greenfield Project?**
   - Copy CONSTITUTION template
   - Copy SPEC template
   - Copy DESIGN template
   - Start first feature (Section 2.1)

2. **Brownfield Project?**
   - Copy EXISTING_ARCH template
   - Copy MIGRATION_STRATEGY template
   - Copy INTEGRATION_POINTS template
   - Start first new feature (Section 2.2)

3. **Legacy Migration?**
   - Copy LEGACY_CONTEXT template
   - Copy PARITY_REQUIREMENTS template
   - Copy MIGRATION_STRATEGY template
   - Start first module analysis (Section 2.3)

**Resources:**
- Full Framework: `VENDOR_AGNOSTIC_FRAMEWORK.md`
- Enterprise Guide: `ENTERPRISE_ADOPTION_GUIDE.md`
- Folder Reference: `FOLDER_HIERARCHY_REFERENCE.md`

**Support:**
- Internal: [Your team's Slack/Discord]
- Community: [SDD community forums]

---

**Document Version:** 1.0
**Last Updated:** April 24, 2026
**Quick Start for:** Any team, any context, any tool
