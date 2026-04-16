# Spec-Driven Development: Implementation Guide

**Quick Start Guide for Engineering Teams**

---

## Overview

This guide provides a practical, step-by-step approach to implementing the 7-Dimensional Spec-Driven Development Framework in your organization.

---

## Phase 1: Setup (Week 1)

### Day 1: Prepare Your Environment

**1. Install Required Tools**
```bash
# Markdown editor with preview
brew install --cask visual-studio-code

# Mermaid CLI for diagrams
npm install -g @mermaid-js/mermaid-cli

# Git for version control
brew install git
```

**2. Configure VS Code Extensions**
```bash
code --install-extension yzhang.markdown-all-in-one
code --install-extension bierner.markdown-mermaid
code --install-extension davidanson.vscode-markdownlint
```

**3. Create Project Structure**
```bash
mkdir -p my-project/{specs,templates,docs}
cd my-project/specs
mkdir -p {intent,requirements,design,quality,constraints,evolution,validation}
```

### Day 2-3: Team Training

**Workshop 1: Framework Overview (2 hours)**
- Present the 7-dimensional framework
- Show examples from successful projects
- Discuss benefits and trade-offs

**Workshop 2: Hands-On Practice (3 hours)**
- Select a simple feature (e.g., "user login")
- Each team member writes a dimension
- Group review and feedback
- Iterate until comfortable

**Materials Needed:**
- Framework document
- Template files
- Example specifications
- AI coding assistant (Claude Code, Cursor, etc.)

### Day 4-5: Pilot Project Selection

**Criteria for Good Pilot:**
✅ Small scope (deliverable in 4-6 weeks)
✅ Clear business value
✅ Well-understood requirements
✅ Greenfield preferred (no legacy integration)
✅ Team willing to experiment

**Bad Pilot Choices:**
❌ Mission-critical production system
❌ Unclear requirements
❌ Heavy legacy integration
❌ Tight deadline (no room for learning)

---

## Phase 2: First Specification (Week 2)

### The "1-Hour Sprint" Method

**Objective:** Get to 80% completeness in 60 minutes

**Setup:**
- Timer visible to all participants
- Template file open
- Product owner + tech lead + 1-2 engineers
- AI assistant ready

**Minute-by-Minute Breakdown:**

**Minutes 0-10: Intent Layer**
```markdown
## Business Objective
[Product owner answers: What business problem? Why now?]

## User Persona
[Who is this for? What's their pain?]

## Success Metrics
[How do we measure success?]
```

**Minutes 10-30: Behavioral Layer**
```markdown
## Key Use Cases
UC-001: [Primary happy path]
UC-002: [Secondary flow]

## EARS Requirements
REQ-001: WHEN user clicks login THEN system SHALL validate credentials
REQ-002: IF validation fails THEN system SHALL show error message

## Edge Cases
- What if email not found?
- What if password wrong?
- What if account locked?
```

**Minutes 30-45: Structural Layer**
```markdown
## Architecture
[Quick C4 context diagram]

## Data Model
User { id, email, password_hash, status, created_at }

## API
POST /auth/login
  Request: { email, password }
  Response: { token, user }
```

**Minutes 45-55: Quality + Constraints**
```markdown
## Performance
- Login response: < 300ms
- Password hash: bcrypt cost 12

## Security
- Rate limit: 5 attempts per 15 minutes
- JWT expiry: 24 hours

## Constraints
- DO NOT store plaintext passwords
- DO NOT allow weak passwords
```

**Minutes 55-60: Validation**
```markdown
## Acceptance Test
Given user with email "test@example.com" and password "SecurePass123!"
When I POST to /auth/login with correct credentials
Then I receive a JWT token
And token is valid for 24 hours
```

**Output:** 80% complete specification ready for refinement

---

### Refinement (Next 2-3 Hours)

**Use AI to Identify Gaps:**
```
Prompt: "Review this specification for login functionality.
Identify unstated assumptions, missing edge cases, and security gaps."
```

**AI will likely surface:**
- Password reset flow not specified
- Email verification requirement unclear
- Token refresh strategy missing
- Concurrent login handling undefined
- Audit logging not mentioned

**Add these to specification**

**Run Completeness Checklist:**
```markdown
Intent Layer:
- [x] Business objective clear
- [x] User personas defined
- [x] Success metrics quantified
- [ ] Decision log started (add why JWT over sessions)

Behavioral Layer:
- [x] Main use cases defined
- [ ] Add password reset use case
- [ ] Add account lockout use case
- [x] Edge cases enumerated
```

**Result:** 95% complete, production-ready specification

---

## Phase 3: Implementation (Weeks 3-4)

### Spec-to-Code Workflow

**Step 1: Load Spec into AI Context**
```
AI Prompt: "I'm implementing a user authentication system.
I have a complete specification. I'll share it in sections.
Please confirm you understand each section before I proceed."
```

**Step 2: Incremental Generation**
```
Prompt: "Generate the User data model based on Dimension 3: Structural Layer.
Follow these constraints from Dimension 5:
- Use bcrypt for password hashing (cost 12)
- Validate email format
- Include created_at timestamp"
```

**Step 3: Validate Each Generation**
```bash
# Run acceptance tests
npm test -- auth.test.js

# Check against AI Code Review Checklist
- [ ] No hardcoded secrets
- [ ] Parameterized queries
- [ ] Error handling present
- [ ] Tests passing
```

**Step 4: Update Spec as You Learn**
```markdown
## Decision Log (Dimension 1)
| Decision | Rationale | Date |
|----------|-----------|------|
| Used Passport.js | Battle-tested, reduces custom code | 2026-04-16 |
```

**Step 5: Iterate Feature by Feature**
- ✅ Data model + validation
- ✅ Registration endpoint
- ✅ Login endpoint
- ✅ Password reset flow
- ✅ Rate limiting
- ✅ Audit logging

**Anti-Pattern to Avoid:**
❌ Generating entire codebase at once
✅ Generate one feature, validate, repeat

---

## Phase 4: Validation (Week 5)

### Specification Quality Review

**Run Automated Checks:**
```bash
# Check for TODO/TBD markers
grep -r "TODO\|TBD\|FIXME" specs/

# Validate Mermaid diagrams compile
mmdc -i specs/design/architecture.md -o /tmp/test.png

# Check requirements coverage
python scripts/trace_requirements.py
```

**Manual Review Checklist:**
- [ ] Every use case has acceptance test
- [ ] Every API endpoint has schema
- [ ] Every data field has validation
- [ ] Every security requirement addressed
- [ ] Every performance target quantified

### Code Quality Review

**Run Against AI Code Review Checklist:**

**Security:**
```bash
# Check for secrets
git secrets --scan

# Dependency vulnerabilities
npm audit

# SQL injection patterns
grep -r "execute.*\+\|query.*\+" src/
```

**Performance:**
```bash
# Run load tests (from Dimension 4 targets)
k6 run load-test.js

# Check for N+1 queries
npx clinic doctor -- node server.js
```

**Coverage:**
```bash
# Must meet target from Dimension 4
npm test -- --coverage
# Expect: >80% per specification
```

---

## Phase 5: Retrospective (Week 6)

### Measure Success

**Specification Quality Metrics:**
- Completeness Score: _____% (target: >90%)
- Assumption Gaps Found: _____ (target: <5)
- Spec Updates During Implementation: _____ (indicates quality)

**Development Efficiency:**
- First-Gen Success Rate: _____% (target: >80%)
- Spec-to-Code Time: _____ hours
- Rework Due to Spec Gaps: _____% (target: <20%)

**Business Impact:**
- Time to Market vs. Baseline: _____ days
- Production Defects: _____ (target: <5%)
- Developer Satisfaction: _____/10

### Lessons Learned

**What Worked Well:**
- [Example: "EARS notation made requirements unambiguous"]
- [Example: "AI Code Review Checklist caught 3 security issues"]

**What Needs Improvement:**
- [Example: "Need better templates for integration specs"]
- [Example: "Validation layer took too long to write"]

**Action Items:**
- [ ] Update templates based on learnings
- [ ] Add new examples to documentation
- [ ] Schedule framework training for next team
- [ ] Plan rollout to 2-3 additional projects

---

## Common Pitfalls & Solutions

### Pitfall 1: Specification Bloat
**Symptom:** Spec is 50+ pages, too large for AI context window

**Solution:**
- Split into bounded contexts
- Keep core spec < 5000 words
- Link to detailed appendices
- Focus on contracts, not implementation details

### Pitfall 2: Analysis Paralysis
**Symptom:** Team spends weeks on spec, never starts coding

**Solution:**
- Use 1-hour sprint method
- Set time limit: 8 hours max for first draft
- Ship with 80% completeness, refine during implementation
- Remember: specs are living documents

### Pitfall 3: Spec-Code Drift
**Symptom:** Code implements features not in spec, spec describes non-existent code

**Solution:**
- Enforce spec-first culture (code without spec is rejected in PR)
- Update spec before changing code
- Run traceability checks in CI/CD
- Weekly spec review meetings

### Pitfall 4: AI Hallucinations
**Symptom:** AI generates plausible-looking code that violates spec

**Solution:**
- Use AI Code Review Checklist religiously
- Run acceptance tests after every generation
- Validate against OpenAPI schemas
- Have human review all security-critical code

### Pitfall 5: Ignoring Constraints
**Symptom:** AI generates code that violates anti-patterns or constraints

**Solution:**
- Make constraints explicit and prominent
- Repeat constraints in prompts
- Use linting rules to enforce
- Add constraints to code review checklist

---

## Templates & Checklists

### Daily Standup Questions (Spec-Driven Version)

Instead of: "What did you work on?"
Ask: "Which spec dimension did you complete?"

Instead of: "What's blocking you?"
Ask: "Which spec assumption proved incorrect?"

### Code Review Template

```markdown
## Specification Compliance
- [ ] Feature matches spec requirements (cite: REQ-XXX)
- [ ] API follows defined contract (cite: design.md)
- [ ] Performance targets met (cite: quality.md)

## AI Code Review Checklist
- [ ] Security: No OWASP Top 10 violations
- [ ] Performance: No N+1 queries
- [ ] Error Handling: All failure modes addressed
- [ ] Tests: Coverage >80%, acceptance tests pass

## Spec Updates
- [ ] Decision log updated
- [ ] Technical debt logged (if applicable)
- [ ] Traceability matrix updated
```

### Sprint Planning Template

```markdown
## Sprint Goal
[Feature to deliver]

## Specification Status
- Intent: [Complete / In Progress / Not Started]
- Behavioral: [Complete / In Progress / Not Started]
- Structural: [Complete / In Progress / Not Started]
- Quality: [Complete / In Progress / Not Started]
- Constraints: [Complete / In Progress / Not Started]
- Evolution: [Complete / In Progress / Not Started]
- Validation: [Complete / In Progress / Not Started]

## Ready for Implementation
- [ ] Spec completeness >90%
- [ ] Acceptance tests written
- [ ] Technical risks identified

## Sprint Tasks
1. [Spec refinement: 4 hours]
2. [Implementation: 20 hours]
3. [Validation: 8 hours]
4. [Spec updates: 4 hours]
```

---

## Scaling Beyond the Pilot

### When to Scale (Checklist)

**Before expanding to more teams:**
- [ ] Pilot project completed successfully
- [ ] Metrics show >80% first-gen success rate
- [ ] Team satisfaction score >7/10
- [ ] Templates refined based on learnings
- [ ] At least 3 successful specifications created
- [ ] AI Code Review Checklist proven effective

### Rollout Strategy

**Month 1-2: Pilot (1 team)**
- Learn and iterate
- Build internal examples
- Refine templates

**Month 3-4: Early Adopters (2-3 teams)**
- Teams that are excited about AI
- Greenfield projects preferred
- Create more diverse examples

**Month 5-6: Broader Rollout (5-10 teams)**
- Include brownfield projects
- Mandate for new features
- Offer internal training

**Month 7-12: Organization-Wide**
- Integrate into SDLC
- Make templates mandatory
- Measure ROI at org level

### Governance Setup

**Specification Review Board:**
- Meets weekly
- Reviews high-risk specs before implementation
- Maintains template library
- Shares best practices

**Specification Champions:**
- One per team
- Trained on full framework
- First point of contact for questions
- Contributes to template improvements

**Specification Repository:**
- Central Git repo for all specs
- Standardized folder structure
- Automated linting in CI/CD
- Search/discovery for reuse

---

## Tool Recommendations

### Essential Tools (Free)

| Category | Tool | Purpose |
|----------|------|---------|
| Editor | VS Code + Markdown extensions | Spec authoring |
| Diagrams | Mermaid | Architecture diagrams |
| AI Assistant | Claude Code / Cursor | Code generation |
| Version Control | Git + GitHub | Spec versioning |
| Testing | Jest / Pytest | Acceptance tests |

### Advanced Tools (Paid)

| Category | Tool | Purpose | Cost |
|----------|------|---------|------|
| Specification Platform | GitHub Spec Kit | Full workflow | Free |
| API Design | Stoplight Studio | OpenAPI editing | $79/mo |
| Diagram Collaboration | Lucidchart | Team diagramming | $9/user/mo |
| Test Automation | Cypress / Playwright | E2E testing | Free |
| Contract Testing | Pact | API contracts | Free |

### AI Coding Assistants Comparison

| Platform | Best For | Spec Support | Cost |
|----------|----------|--------------|------|
| Claude Code | Complex reasoning, full context | Excellent | Usage-based |
| Cursor | Fast iteration, inline editing | Good | $20/mo |
| GitHub Copilot | Autocomplete, common patterns | Basic | $10/mo |
| Windsurf | Team collaboration | Good | $15/mo |

---

## Success Stories (Template)

**Company:** [Your Company]
**Team Size:** [X engineers]
**Project:** [Feature name]

**Before Spec-Driven Development:**
- Specification time: _____ hours
- Implementation time: _____ hours
- Defects found in QA: _____
- Time to production: _____ days

**After Spec-Driven Development:**
- Specification time: _____ hours
- Implementation time: _____ hours (via AI generation)
- Defects found in QA: _____
- Time to production: _____ days

**Key Wins:**
- [Example: "50% reduction in implementation time"]
- [Example: "Zero production defects in first month"]

**Lessons Learned:**
- [What worked]
- [What didn't]
- [What we'd do differently]

---

## Getting Help

### Internal Resources
- Framework Documentation: `Spec_Driven_Development_Framework.md`
- Templates: `templates/spec_template.md`
- Examples: `examples/` directory

### External Resources
- GitHub Spec Kit: https://github.com/liatrio-labs/spec-driven-workflow
- Thoughtworks on SDD: https://thoughtworks.medium.com/spec-driven-development-d85995a81387
- Addy Osmani's Guide: https://addyosmani.com/blog/good-spec/

### Community
- Join #spec-driven-dev Slack channel
- Weekly office hours: [Day/Time]
- Specification Champions: [List of names]

---

## Next Steps

### For Individual Contributors
1. ✅ Read framework document
2. ✅ Complete hands-on training
3. ✅ Write first spec using template
4. ✅ Generate code with AI assistant
5. ✅ Share learnings with team

### For Team Leads
1. ✅ Select pilot project
2. ✅ Allocate time for learning (1 week)
3. ✅ Set up toolchain
4. ✅ Run team training
5. ✅ Measure and report results

### For Engineering Managers
1. ✅ Approve pilot budget
2. ✅ Define success metrics
3. ✅ Set up governance model
4. ✅ Plan scaling strategy
5. ✅ Communicate wins to org

---

**Remember:** The goal is not perfect specifications on day one. The goal is to make specifications the living source of truth that enables AI to accelerate development while maintaining quality.

Start small. Iterate fast. Scale with confidence.

---

**Guide Version:** 1.0
**Last Updated:** April 16, 2026
**Feedback:** [Your contact info]