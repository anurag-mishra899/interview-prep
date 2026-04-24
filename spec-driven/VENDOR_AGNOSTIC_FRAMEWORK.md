# Spec-Driven Development: Universal Framework

**A Tool-Agnostic Guide for Enterprise Implementation**

---

## Executive Summary

This framework provides **vendor-neutral** guidance for implementing Spec-Driven Development across Greenfield, Brownfield, and Modern Legacy contexts. The principles and patterns described work with **any AI coding assistant** (GitHub Copilot, Claude Code, Cursor, Gemini, ChatGPT, or custom solutions) and **any tech stack**.

### Core Philosophy: Specifications as Executable Artifacts

**Traditional Development:**
```
Requirements → Design → Code → Tests → Documentation
                         ↑
                    (Truth lives here)
```

**Spec-Driven Development:**
```
Specifications ⇄ Code ⇄ Tests
      ↑
(Truth lives here)
```

The specification is the **source of truth**, not documentation that drifts from reality.

---

## Part 1: Universal Principles (Tool-Agnostic)

### 1.1 The Four Pillars of SDD

#### Pillar 1: Specifications Are Executable
**Not just documentation**—specifications directly generate or validate code.

**Traditional Spec (Non-Executable):**
```markdown
## User Authentication
The system should allow users to log in with email and password.
Sessions should expire after 30 minutes of inactivity.
```
👉 This is guidance, not truth. Code diverges over time.

**Executable Spec:**
```markdown
## User Authentication Specification

### Behavior Contract
GIVEN a user with valid credentials
WHEN they submit login form
THEN system creates session with 30-minute sliding expiration

### Acceptance Criteria (Testable)
1. Valid credentials → HTTP 200 + session cookie
2. Invalid credentials → HTTP 401 + error message
3. Session inactive >30 min → HTTP 401 on next request
4. Session active <30 min → expiration extends by 30 min

### Validation
- Tests MUST validate all criteria above
- Implementation MUST match this contract
- Any divergence MUST update this spec first
```
👉 This is a **contract**. Tests validate it. Code implements it.

#### Pillar 2: Natural Language > Formal Syntax
Unlike Model-Driven Development (UML, DSLs), SDD uses **human-readable specifications**.

**Why Natural Language?**
- Stakeholders can read and validate
- Domain experts can contribute
- AI models understand context and intent
- Lower barrier to entry than formal modeling

**Principle:** If a Product Manager can't understand your spec, it's over-specified.

#### Pillar 3: Specifications Evolve with Code
Specs are **versioned**, **reviewed**, and **maintained** like code.

**Git Workflow:**
```bash
# Traditional
git add src/auth.js tests/auth.test.js
git commit -m "Add authentication"

# Spec-Driven
git add specs/auth.md src/auth.js tests/auth.test.js
git commit -m "Add authentication per spec 001"
```

**Key Difference:** Spec changes are **first-class citizens** in version control.

#### Pillar 4: Progressive Formalization
Start loose (exploration), tighten over time (production).

```
Spec-First          →  Spec-Anchored      →  Spec-as-Source
(Prototype)            (Production)          (Strategic)
Informal specs         Formal contracts      Generative specs
Disposable             Maintained            Regenerative
```

### 1.2 Core Artifact Types (Universal)

All SDD implementations use these artifact types (names may vary):

| Artifact Type | Purpose | Lifecycle | Examples |
|--------------|---------|-----------|----------|
| **Constitution** | Immutable principles | Project lifetime | `PRINCIPLES.md`, `STANDARDS.md`, `GUARDRAILS.md` |
| **Memory Bank** | Persistent context | Long-lived | `ARCHITECTURE.md`, `TECH_STACK.md`, `GLOSSARY.md` |
| **Feature Spec** | Requirements (WHAT/WHY) | Feature lifetime | `AUTH_SPEC.md`, `PAYMENT_SPEC.md` |
| **Design Plan** | Implementation (HOW) | Feature lifetime | `AUTH_DESIGN.md`, `API_CONTRACTS.md` |
| **Task List** | Execution steps | Implementation only | `AUTH_TASKS.md`, `TODO.md` |
| **Contracts** | API/Data schemas | Feature lifetime | `openapi.yaml`, `schema.sql`, `events.json` |

**Tool-Agnostic:** Use whatever naming/format suits your team, but have all artifact types.

---

## Part 2: Universal Folder Structure

### 2.1 The Canonical Structure (Any Tool, Any Stack)

```
project-root/
│
├── specs/                              # Specification Workspace
│   ├── _meta/                          # Project-wide context
│   │   ├── CONSTITUTION.md             # Immutable principles
│   │   ├── ARCHITECTURE.md             # High-level design decisions
│   │   ├── TECH_STACK.md               # Technology choices & rationale
│   │   ├── GLOSSARY.md                 # Domain terminology
│   │   └── WORKFLOWS.md                # Team processes
│   │
│   ├── features/                       # Feature specifications
│   │   ├── 001-user-authentication/
│   │   │   ├── SPEC.md                 # Requirements (WHAT & WHY)
│   │   │   ├── DESIGN.md               # Implementation plan (HOW)
│   │   │   ├── TASKS.md                # Executable task list
│   │   │   ├── RESEARCH.md             # Technology research notes
│   │   │   ├── DATA_MODEL.md           # Database/entity design
│   │   │   ├── CONTRACTS/              # API/Event contracts
│   │   │   │   ├── api.yaml            # OpenAPI or GraphQL schema
│   │   │   │   ├── events.json         # Event definitions
│   │   │   │   └── data.sql            # Database schema
│   │   │   └── CHANGELOG.md            # Feature evolution history
│   │   │
│   │   ├── 002-payment-processing/
│   │   │   └── ... (same structure)
│   │   │
│   │   └── 003-notification-system/
│   │       └── ... (same structure)
│   │
│   ├── templates/                      # Spec templates
│   │   ├── FEATURE_SPEC_TEMPLATE.md
│   │   ├── DESIGN_TEMPLATE.md
│   │   └── TASKS_TEMPLATE.md
│   │
│   └── _archive/                       # Deprecated/superseded specs
│       └── 001-old-auth/               # Replaced by 001 v2
│
├── src/                                # Source code
│   ├── libs/                           # Modular libraries
│   │   ├── auth/                       # From feature 001
│   │   ├── payments/                   # From feature 002
│   │   └── notifications/              # From feature 003
│   │
│   └── apps/                           # Applications
│       ├── web/
│       ├── mobile/
│       └── admin/
│
├── tests/                              # Test suites
│   ├── specs/                          # Spec validation tests
│   │   ├── auth.spec.test.js           # Validates 001 contract
│   │   └── payments.spec.test.js       # Validates 002 contract
│   │
│   ├── unit/                           # Unit tests
│   ├── integration/                    # Integration tests
│   └── e2e/                            # End-to-end tests
│
├── docs/                               # Generated/human docs
│   ├── api/                            # API documentation (generated)
│   ├── architecture/                   # ADRs (Architecture Decision Records)
│   └── runbooks/                       # Operational guides
│
├── .ai/                                # AI assistant configuration
│   ├── prompts/                        # Custom prompts for your AI tool
│   │   ├── create-spec.md
│   │   ├── create-design.md
│   │   └── implement-feature.md
│   │
│   └── config.yaml                     # AI tool configuration
│
└── README.md                           # Project overview
```

**Key Design Decisions:**

1. **`specs/` is top-level** (same importance as `src/`)
2. **`_meta/` for cross-cutting concerns** (not buried in subdirectories)
3. **Numbered features** (`001-`, `002-`) for clear ordering and references
4. **Separate `SPEC.md` and `DESIGN.md`** (WHAT/WHY vs. HOW)
5. **`CONTRACTS/` for machine-readable schemas** (validated by tests)
6. **`.ai/` for tool-specific customizations** (gitignored if needed)

### 2.2 Adapting to Your Tool

**If using GitHub Copilot Workspace:**
```
+ .github/prompts/         # Custom prompts
```

**If using Cursor:**
```
+ .cursorrules             # Cursor-specific rules
+ .cursor/prompts/         # Cursor prompts
```

**If using Claude Code:**
```
+ .claude/commands/        # Slash commands
+ CLAUDE.md                # Claude project context
```

**If using ChatGPT/Custom:**
```
+ .ai/context/             # Context files for ChatGPT
+ .ai/system-prompts/      # System prompt templates
```

**Principle:** Keep tool-specific config in `.ai/` or vendor-specific directories. Keep specs in `specs/`.

---

## Part 3: Greenfield Implementation

### 3.1 Greenfield: Start with Specifications

**Context:** New project, blank canvas, no legacy constraints.

**Philosophy:** Establish constitutional foundation FIRST, then build everything from specs.

### 3.2 Greenfield Folder Structure

```
greenfield-project/
│
├── specs/
│   ├── _meta/
│   │   ├── CONSTITUTION.md ⭐          # START HERE
│   │   │   ## Architectural Principles
│   │   │   1. Library-First: All features as reusable libraries
│   │   │   2. Contract-First: APIs designed before implementation
│   │   │   3. Test-First: Tests written before code
│   │   │   4. Simplicity-First: Minimize dependencies
│   │   │   5. Security-First: Threat modeling mandatory
│   │   │
│   │   ├── ARCHITECTURE.md
│   │   │   ## High-Level Architecture
│   │   │   - Monorepo with modular libraries
│   │   │   - Event-driven communication between services
│   │   │   - API-first design (REST + GraphQL)
│   │   │   - Database-per-service pattern
│   │   │
│   │   ├── TECH_STACK.md
│   │   │   ## Core Technologies
│   │   │   - Backend: Node.js 20+ (TypeScript)
│   │   │   - Frontend: React 18+ (TypeScript)
│   │   │   - Database: PostgreSQL 15+
│   │   │   - Cache: Redis 7+
│   │   │   - Testing: Jest + Playwright
│   │   │
│   │   └── WORKFLOWS.md
│   │       ## Development Workflow
│   │       1. Write SPEC.md (what/why)
│   │       2. Peer review spec
│   │       3. Write DESIGN.md (how)
│   │       4. Architect review design
│   │       5. Generate TASKS.md
│   │       6. Implement with AI assistance
│   │       7. Validate against spec
│   │
│   ├── features/
│   │   └── 001-mvp-authentication/
│   │       ├── SPEC.md
│   │       ├── DESIGN.md
│   │       ├── TASKS.md
│   │       └── CONTRACTS/
│   │           └── auth-api.yaml
│   │
│   └── templates/
│       ├── FEATURE_SPEC_TEMPLATE.md
│       ├── DESIGN_TEMPLATE.md
│       └── TASKS_TEMPLATE.md
│
├── src/
│   ├── libs/                           # Principle 1: Library-First
│   │   └── auth/                       # Feature 001
│   │       ├── src/
│   │       │   ├── index.ts
│   │       │   ├── login.ts
│   │       │   └── session.ts
│   │       ├── tests/                  # Principle 3: Test-First
│   │       │   ├── login.test.ts
│   │       │   └── session.test.ts
│   │       └── package.json
│   │
│   └── apps/
│       └── web/
│           ├── src/
│           └── package.json
│
├── tests/
│   └── specs/
│       └── 001-auth-contract.test.ts   # Validates CONTRACTS/auth-api.yaml
│
└── package.json                        # Root monorepo config
```

### 3.3 Greenfield Workflow (Tool-Agnostic)

#### Phase 0: Constitutional Setup (One-Time)

**1. Create Constitution**
```markdown
# specs/_meta/CONSTITUTION.md

## Principles (Immutable)

### Principle 1: Library-First Architecture
Every feature MUST be implemented as a standalone library with:
- Clear public API
- Comprehensive tests
- Minimal dependencies
- Reusable across applications

### Principle 2: Contract-First Design
Every API MUST have a contract defined BEFORE implementation:
- OpenAPI 3.x for REST APIs
- GraphQL SDL for GraphQL APIs
- JSON Schema for events
- SQL DDL for databases

### Principle 3: Test-First Development
Every feature MUST have tests written BEFORE implementation:
1. Write acceptance tests based on SPEC.md
2. Validate tests FAIL (red phase)
3. Implement minimum code to pass (green phase)
4. Refactor for quality

### Principle 4: Simplicity-First
Every design MUST justify complexity:
- Start with <3 dependencies per library
- Document rationale for each new dependency
- Prefer standard library over external deps
- Complexity budget tracked in DESIGN.md

### Principle 5: Security-First
Every feature touching sensitive data MUST include:
- Threat model (STRIDE analysis)
- Security review checklist
- OWASP Top 10 mitigation
- Dependency vulnerability scanning

## Evolution
This constitution may be amended via:
1. Team consensus (>80% approval)
2. Documented rationale in ADR
3. Backwards compatibility assessment
```

**2. Document Architecture**
```markdown
# specs/_meta/ARCHITECTURE.md

## System Architecture

### Monorepo Structure
```
src/
├── libs/         # Shared libraries (Principle 1)
└── apps/         # Applications consuming libs
```

### Communication Patterns
- Synchronous: REST APIs (libs expose HTTP endpoints)
- Asynchronous: Event bus (Redis pub/sub)
- Data: Each library owns its data store

### Deployment Model
- Libraries: Published as npm packages
- Apps: Containerized (Docker) → Kubernetes
- Infrastructure: Terraform

## Architecture Decision Records
See docs/architecture/ for detailed ADRs
```

**3. Define Tech Stack**
```markdown
# specs/_meta/TECH_STACK.md

## Backend
- **Runtime:** Node.js 20 LTS (TypeScript 5.x)
- **Framework:** Express 4.x (minimal, well-known)
- **Database:** PostgreSQL 15+ (ACID compliance)
- **Cache:** Redis 7+ (session storage, pub/sub)
- **ORM:** Prisma 5.x (type-safe, migrations)

## Frontend
- **Framework:** React 18+ with TypeScript
- **Build Tool:** Vite 5.x
- **State Management:** Zustand (simple, minimal)
- **Styling:** Tailwind CSS 3.x

## Testing
- **Unit/Integration:** Jest 29.x
- **E2E:** Playwright 1.x
- **Contract:** Pact (consumer-driven contracts)

## Rationale
See ARCHITECTURE.md for decision rationale
```

#### Phase 1: Feature Development (Per Feature)

**Step 1: Write Specification (WHAT & WHY)**

Use your AI assistant (any tool):
```
Prompt:
"Using specs/templates/FEATURE_SPEC_TEMPLATE.md, create a specification for:
User authentication system supporting email/password login and OAuth2 providers.
Focus on WHAT users need and WHY, not implementation details.
Save to specs/features/001-authentication/SPEC.md"
```

**Generated SPEC.md:**
```markdown
# Feature 001: User Authentication

## Overview
Enable users to securely access the platform using email/password or OAuth2 providers.

## User Stories

### Story 1.1: Email/Password Registration
**As a** new user
**I want to** register with email and password
**So that** I can access the platform

**Acceptance Criteria:**
1. Email must be unique and validated
2. Password must meet strength requirements (min 12 chars, mixed case, numbers, symbols)
3. Email verification sent before account activation
4. User receives confirmation after successful registration

### Story 1.2: Email/Password Login
**As a** registered user
**I want to** log in with my credentials
**So that** I can access my account

**Acceptance Criteria:**
1. Valid credentials → session created (30-min sliding expiration)
2. Invalid credentials → clear error message (no email/password distinction for security)
3. Locked after 5 failed attempts (15-min cooldown)
4. Remember me option → 30-day session

### Story 1.3: OAuth2 Login (Google, GitHub)
**As a** user
**I want to** log in with Google or GitHub
**So that** I don't need to remember another password

**Acceptance Criteria:**
1. Redirect to OAuth provider
2. On success, create/update user profile
3. Link to existing account if email matches
4. Same session behavior as email/password login

## Non-Functional Requirements

### Security
- Passwords hashed with bcrypt (cost factor 12)
- Sessions stored in Redis (encrypted)
- HTTPS only (no cookies over HTTP)
- CSRF protection on all state-changing operations
- Rate limiting on login endpoint (10 req/min per IP)

### Performance
- Login response time <200ms (p95)
- OAuth redirect <500ms (p95)
- Support 100 concurrent logins

### Compliance
- GDPR: User data deletion on request
- Password reset link expires after 1 hour
- Audit log for all authentication events

## Out of Scope (Future)
- Multi-factor authentication (MFA)
- Biometric authentication
- Single sign-on (SSO) for enterprise

## Success Metrics
- 95% of users complete registration in <2 minutes
- <1% login failure rate (excluding wrong credentials)
- Zero security incidents in first 6 months
```

**Step 2: Clarify Ambiguities**

Review spec and mark unclear areas:
```markdown
## Questions for Clarification
1. [NEEDS CLARIFICATION] Should OAuth users set a password for fallback?
2. [NEEDS CLARIFICATION] Email verification required before OAuth login?
3. [NEEDS CLARIFICATION] Link multiple OAuth providers to one account?

## Answers (From Product Team)
1. No, OAuth-only users don't need password (can add later)
2. No, OAuth email is pre-verified by provider
3. Yes, allow linking multiple providers
```

**Step 3: Create Design Plan (HOW)**

```
Prompt:
"Using specs/_meta/TECH_STACK.md and specs/_meta/ARCHITECTURE.md,
create DESIGN.md for feature 001.
Include: component architecture, API contracts, data models, dependencies."
```

**Generated DESIGN.md:**
```markdown
# Feature 001: Authentication - Design

## Component Architecture

### Library: `@myapp/auth`
```
auth/
├── src/
│   ├── providers/
│   │   ├── email-password.ts    # Email/password strategy
│   │   ├── oauth-google.ts      # Google OAuth strategy
│   │   └── oauth-github.ts      # GitHub OAuth strategy
│   ├── session.ts               # Session management
│   ├── validation.ts            # Input validation
│   └── index.ts                 # Public API
├── tests/
└── package.json
```

## Data Model

### Database Schema (PostgreSQL)
```sql
-- users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),          -- NULL for OAuth-only users
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- oauth_accounts table
CREATE TABLE oauth_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,       -- 'google' | 'github'
    provider_user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(provider, provider_user_id)
);

-- sessions table (Redis, shown here for documentation)
Key: session:{sessionId}
Value: {
    userId: UUID,
    expiresAt: timestamp,
    rememberMe: boolean
}
TTL: 30 minutes (sliding) or 30 days (remember me)
```

## API Contracts

### REST API (OpenAPI)
```yaml
# CONTRACTS/auth-api.yaml
openapi: 3.0.0
info:
  title: Authentication API
  version: 1.0.0

paths:
  /auth/register:
    post:
      summary: Register new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 12
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                type: object
                properties:
                  userId:
                    type: string
                    format: uuid
                  message:
                    type: string
        '400':
          description: Validation error
        '409':
          description: Email already exists

  /auth/login:
    post:
      summary: Login with credentials
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                password:
                  type: string
                rememberMe:
                  type: boolean
                  default: false
      responses:
        '200':
          description: Login successful
          headers:
            Set-Cookie:
              schema:
                type: string
          content:
            application/json:
              schema:
                type: object
                properties:
                  userId:
                    type: string
                    format: uuid
        '401':
          description: Invalid credentials
        '429':
          description: Rate limit exceeded

  /auth/oauth/{provider}:
    get:
      summary: Initiate OAuth flow
      parameters:
        - name: provider
          in: path
          required: true
          schema:
            type: string
            enum: [google, github]
      responses:
        '302':
          description: Redirect to OAuth provider

  /auth/oauth/{provider}/callback:
    get:
      summary: OAuth callback
      # ... similar structure
```

## Dependencies

### New Dependencies (Justification Required per Principle 4)
1. **bcrypt** (v5.x) - Industry-standard password hashing
   - Rationale: Secure password storage is non-negotiable
   - Complexity: Low (single purpose library)

2. **passport** (v0.7.x) - Authentication middleware
   - Rationale: OAuth integration requires provider-specific logic
   - Complexity: Medium (well-documented, widely used)

3. **joi** (v17.x) - Input validation
   - Rationale: Type-safe validation of user inputs
   - Complexity: Low (declarative schema validation)

**Total Dependency Count:** 3 (within Principle 4 budget of <3)

## Security Analysis (Principle 5)

### Threat Model (STRIDE)
- **Spoofing:** Mitigated by bcrypt + rate limiting
- **Tampering:** Mitigated by HTTPS + CSRF tokens
- **Repudiation:** Mitigated by audit logging
- **Information Disclosure:** Mitigated by error message sanitization
- **Denial of Service:** Mitigated by rate limiting
- **Elevation of Privilege:** Mitigated by session isolation

### OWASP Top 10 Mitigation
1. **A01: Broken Access Control** → Session-based auth, expiration
2. **A02: Cryptographic Failures** → bcrypt, HTTPS, Redis encryption
3. **A03: Injection** → Parameterized queries (Prisma ORM)
4. **A07: Authentication Failures** → Rate limiting, account lockout
...

## Constitutional Compliance

✅ **Principle 1 (Library-First):** Implemented as `@myapp/auth` library
✅ **Principle 2 (Contract-First):** OpenAPI spec in CONTRACTS/auth-api.yaml
✅ **Principle 3 (Test-First):** Tests defined in TASKS.md before implementation
✅ **Principle 4 (Simplicity):** 3 dependencies, all justified
✅ **Principle 5 (Security):** Threat model + OWASP mitigation documented
```

**Step 4: Generate Task List**

```
Prompt:
"From DESIGN.md, create TASKS.md with executable steps.
Order tasks by dependencies. Mark test-writing tasks BEFORE implementation tasks."
```

**Generated TASKS.md:**
```markdown
# Feature 001: Authentication - Tasks

## Phase 0: Setup
- [ ] Task 0.1: Create library structure `src/libs/auth/`
- [ ] Task 0.2: Install dependencies (bcrypt, passport, joi)
- [ ] Task 0.3: Create Prisma schema for users, oauth_accounts tables
- [ ] Task 0.4: Run migrations

## Phase 1: Test-First (Principle 3)
- [ ] Task 1.1: Write acceptance tests for Story 1.1 (registration)
- [ ] Task 1.2: Write acceptance tests for Story 1.2 (login)
- [ ] Task 1.3: Write acceptance tests for Story 1.3 (OAuth)
- [ ] Task 1.4: Write unit tests for validation logic
- [ ] Task 1.5: Write unit tests for session management
- [ ] Task 1.6: Validate all tests FAIL (red phase)

## Phase 2: Implementation
- [ ] Task 2.1: Implement email validation (src/validation.ts)
- [ ] Task 2.2: Implement password hashing (src/providers/email-password.ts)
- [ ] Task 2.3: Implement registration endpoint
- [ ] Task 2.4: Implement login endpoint
- [ ] Task 2.5: Implement session management (src/session.ts)
- [ ] Task 2.6: Implement OAuth providers (src/providers/oauth-*.ts)
- [ ] Task 2.7: Implement rate limiting middleware

## Phase 3: Validation
- [ ] Task 3.1: Validate all tests PASS (green phase)
- [ ] Task 3.2: Contract testing (validate against CONTRACTS/auth-api.yaml)
- [ ] Task 3.3: Security scan (npm audit, OWASP ZAP)
- [ ] Task 3.4: Performance test (100 concurrent logins <200ms)

## Phase 4: Refactoring
- [ ] Task 4.1: Code review for simplicity
- [ ] Task 4.2: Refactor duplications
- [ ] Task 4.3: Update documentation

## Task Dependencies
- Phase 1 must complete BEFORE Phase 2 (Test-First)
- Phase 2 must complete BEFORE Phase 3 (Implementation before validation)
- Phase 3 must pass BEFORE Phase 4 (Refactor only after working)
```

**Step 5: Execute with AI Assistance**

```
Prompt to AI:
"Execute TASKS.md for feature 001 in order.
After each task, show me the result and wait for my approval before continuing.
Follow DESIGN.md exactly. Validate against SPEC.md acceptance criteria."
```

AI implements tasks sequentially:
1. Creates library structure
2. Writes tests (following Test-First principle)
3. Implements minimum code to pass tests
4. Refactors for quality

**Step 6: Validate Against Spec**

```bash
# Run contract tests
npm test -- tests/specs/001-auth-contract.test.ts

# Validate OpenAPI contract
npx @openapitools/openapi-generator-cli validate -i specs/features/001-authentication/CONTRACTS/auth-api.yaml

# Run all tests
npm test

# Security scan
npm audit
```

### 3.4 Greenfield Success Criteria

✅ **Constitutional Compliance:**
- All 5 principles documented and enforced
- Architecture defined BEFORE first feature
- Tech stack choices justified

✅ **Spec Coverage:**
- Every feature has SPEC.md + DESIGN.md
- Acceptance criteria are testable
- Contracts are machine-readable (OpenAPI, JSON Schema)

✅ **Test-First Adherence:**
- Tests written before implementation
- Contract tests validate specs
- 80%+ code coverage

✅ **Deliverable Quality:**
- Code matches design exactly
- No constitutional violations
- Security threats mitigated

---

## Part 4: Brownfield Implementation

### 4.1 Brownfield: Incremental Adoption

**Context:** Existing codebase, active development, can't stop to retrofit everything.

**Philosophy:** Add specs for NEW work, gradually document EXISTING work, avoid big-bang migration.

### 4.2 Brownfield Folder Structure

```
existing-monolith/                      # Your current codebase
│
├── src/                                # Existing code (UNCHANGED initially)
│   ├── controllers/
│   │   ├── UserController.js           # Existing auth logic
│   │   ├── OrderController.js          # Existing order logic
│   │   └── PaymentController.js        # Existing payment logic
│   ├── models/
│   ├── services/
│   └── utils/
│
├── tests/                              # Existing tests (keep running)
│   └── ...
│
├── specs/                              # NEW: Spec-Driven workspace
│   ├── _meta/
│   │   ├── CONSTITUTION.md             # Forward-looking principles
│   │   ├── EXISTING_ARCH.md ⭐         # Document current architecture
│   │   ├── MIGRATION_STRATEGY.md ⭐    # How to transition
│   │   ├── TECH_DEBT.md ⭐             # Known issues & constraints
│   │   └── GLOSSARY.md
│   │
│   ├── features/                       # NEW features only (initially)
│   │   ├── 001-realtime-notifications/
│   │   │   ├── SPEC.md
│   │   │   ├── DESIGN.md
│   │   │   ├── TASKS.md
│   │   │   └── INTEGRATION_POINTS.md ⭐  # How this integrates with existing code
│   │   │
│   │   └── 002-advanced-search/
│   │       └── ...
│   │
│   ├── existing/                       # OPTIONAL: Specs for existing features
│   │   ├── auth-system/                # Reverse-engineered from src/controllers/UserController.js
│   │   │   ├── SPEC.md                 # Documents what the code currently does
│   │   │   └── REFACTOR_PLAN.md        # How to improve it
│   │   │
│   │   └── order-system/
│   │       └── ...
│   │
│   └── templates/
│       ├── FEATURE_SPEC_TEMPLATE.md
│       ├── INTEGRATION_TEMPLATE.md ⭐  # Template for brownfield integration
│       └── REVERSE_ENGINEER_TEMPLATE.md ⭐
│
├── .ai/
│   └── prompts/
│       ├── reverse-engineer.md ⭐      # Prompt for documenting existing code
│       └── integrate-new-feature.md ⭐
│
└── docs/
    └── SDD_ADOPTION_LOG.md ⭐           # Track adoption progress
```

**Key Brownfield Artifacts:**

1. **`EXISTING_ARCH.md`** - Documents current architecture (warts and all)
2. **`MIGRATION_STRATEGY.md`** - Phased approach to SDD adoption
3. **`TECH_DEBT.md`** - Known issues that constrain new work
4. **`INTEGRATION_POINTS.md`** - How new specs integrate with old code
5. **`SDD_ADOPTION_LOG.md`** - Track what's been converted

### 4.3 Brownfield Workflow

#### Phase 0: Document Existing State

**1. Understand Current Architecture**

```
Prompt to AI:
"Analyze the following codebase structure and create EXISTING_ARCH.md:
- src/controllers/ (MVC pattern, Express routes)
- src/models/ (Mongoose ODM, MongoDB)
- src/services/ (Business logic layer)

Document:
- Architectural patterns in use
- Data flow (request → response)
- Database schema
- External dependencies
- Known pain points"
```

**Generated EXISTING_ARCH.md:**
```markdown
# Existing Architecture (As-Is)

## High-Level Pattern
**MVC (Model-View-Controller)** with service layer

```
Request → Router → Controller → Service → Model → MongoDB
                                    ↓
                                 Response
```

## Technology Stack
- **Backend:** Node.js 16, Express 4.x
- **Database:** MongoDB 5.x (Mongoose ODM)
- **Auth:** Passport.js (local strategy only)
- **Session:** express-session + MongoDB store

## Current Structure
```
src/
├── controllers/        # HTTP request handlers
├── models/            # Mongoose schemas
├── services/          # Business logic
├── middleware/        # Auth, validation, error handling
├── routes/            # Express route definitions
└── utils/             # Helpers
```

## Pain Points
1. **Monolithic:** All features in one codebase (hard to scale)
2. **No API Contracts:** Routes defined in code, no OpenAPI spec
3. **Inconsistent Error Handling:** Each controller handles errors differently
4. **Tight Coupling:** Controllers directly import models
5. **No Type Safety:** Plain JavaScript (no TypeScript)
6. **Test Coverage:** ~40% (low)

## Constraints for New Work
- Must maintain MongoDB (can't migrate to PostgreSQL)
- Can't break existing API endpoints (backwards compatibility)
- Existing auth system must continue working
- Deployment pipeline assumes monolith (can't split yet)
```

**2. Create Migration Strategy**

```markdown
# specs/_meta/MIGRATION_STRATEGY.md

## Phased Approach to SDD Adoption

### Phase 1 (Months 1-3): New Features Only
**Goal:** Prove SDD value without disrupting existing code

**Approach:**
- NEW features use SDD (specs → design → implementation)
- EXISTING features remain unchanged
- Spec integration points with existing code

**Example:** Feature 001 (realtime notifications)
- New service in src/services/notifications.js
- Integrates with existing UserController
- Spec documents integration contract

### Phase 2 (Months 4-6): Selective Reverse Engineering
**Goal:** Document critical paths

**Approach:**
- Create specs for most-changed existing features
- Prioritize: auth, payments, core business logic
- Use specs to guide refactoring

**Example:** Reverse engineer src/controllers/UserController.js
- Document current behavior in specs/existing/auth-system/SPEC.md
- Create REFACTOR_PLAN.md to improve incrementally

### Phase 3 (Months 7-12): Hybrid Maintenance
**Goal:** All changes start with specs

**Approach:**
- Bug fixes: Update spec FIRST, then fix code
- Enhancements: Standard SDD workflow
- Refactoring: Guided by specs

### Phase 4 (Year 2+): Architectural Evolution
**Goal:** Migrate toward target architecture

**Approach:**
- Extract libraries from monolith (guided by specs)
- Migrate critical services to TypeScript
- Introduce API contracts (OpenAPI)

## Success Metrics
- **Phase 1:** 100% of new features have specs
- **Phase 2:** Top 5 critical paths documented
- **Phase 3:** 80% of changes start with spec updates
- **Phase 4:** 50% of codebase extracted to libraries
```

**3. Track Technical Debt**

```markdown
# specs/_meta/TECH_DEBT.md

## Known Issues & Constraints

### Architectural Debt
1. **Monolithic Structure**
   - Impact: Hard to scale individual features
   - Constraint: Can't split until deployment pipeline supports multiple services
   - Migration Path: Phase 4 (extract to libraries)

2. **No API Contracts**
   - Impact: Frontend-backend coupling, no versioning
   - Constraint: Can't break existing clients
   - Migration Path: Phase 2 (introduce OpenAPI specs, versioned endpoints)

### Code Debt
3. **Inconsistent Error Handling**
   - Impact: Debugging difficulty, poor UX
   - Constraint: Changing existing endpoints may break clients
   - Migration Path: Phase 3 (standardize via middleware, new endpoints only)

4. **Low Test Coverage (40%)**
   - Impact: Risky refactoring
   - Constraint: Adding tests may reveal bugs
   - Migration Path: Phase 2 (spec-driven testing for critical paths)

### Data Debt
5. **MongoDB Schema Inconsistencies**
   - Impact: Data integrity issues
   - Constraint: Can't migrate existing data easily
   - Migration Path: Phase 3 (enforce schema via Mongoose strict mode)

## Impact on New Work
- New features MUST work with MongoDB (can't use PostgreSQL yet)
- New endpoints MUST follow `/api/v2/` convention (v1 is legacy)
- New code SHOULD use TypeScript (gradual migration)
- Integration MUST not break existing tests
```

#### Phase 1: First New Feature (SDD)

**Step 1: Write Spec with Integration Points**

```markdown
# specs/features/001-realtime-notifications/SPEC.md

## Overview
Real-time notifications for order status changes (new, processing, shipped, delivered).

## User Stories
[... standard spec content ...]

## Integration with Existing System ⭐

### Integration Point 1: Order Status Changes
**Existing Code:** `src/controllers/OrderController.js`
```javascript
// Current implementation (line 45)
exports.updateOrderStatus = async (req, res) => {
  const order = await Order.findByIdAndUpdate(req.params.id, { status: req.body.status });
  // ⭐ NEW: Trigger notification here
  res.json(order);
};
```

**Integration Contract:**
- WHEN: Order status changes
- WHERE: `OrderController.updateOrderStatus` (after DB update)
- HOW: Call `NotificationService.notifyOrderUpdate(orderId, newStatus)`

### Integration Point 2: User Subscription Management
**Existing Code:** `src/models/User.js`
```javascript
// Current schema (line 12)
const UserSchema = new mongoose.Schema({
  email: String,
  password: String,
  // ⭐ NEW: Add notification preferences
  notificationPreferences: {
    email: { type: Boolean, default: true },
    push: { type: Boolean, default: false },
    sms: { type: Boolean, default: false }
  }
});
```

**Integration Contract:**
- WHAT: Add new field to existing User model
- MIGRATION: Provide default values for existing users
- BACKWARDS COMPAT: Field is optional (defaults to email-only)

## Constraints from Existing System
1. Must use MongoDB (existing Order and User models)
2. Must integrate with express-session (existing auth)
3. Cannot modify existing API endpoints (only add new ones)
4. Must coexist with current OrderController
```

**Step 2: Design with Integration Plan**

```markdown
# specs/features/001-realtime-notifications/DESIGN.md

## Integration Architecture

### Approach: **Sidecar Pattern**
New NotificationService runs alongside existing code without modifying existing logic.

```
Existing OrderController         NEW NotificationService
        ↓                                  ↓
   Update Order ────────→ Event Emitter → Send Notification
        ↓                                  ↓
   Return Response                    WebSocket → Client
```

### Integration Steps
1. **Minimal Changes to Existing Code:**
   ```javascript
   // src/controllers/OrderController.js (line 47 - ADD ONLY)
   const NotificationService = require('../services/notifications');

   exports.updateOrderStatus = async (req, res) => {
     const order = await Order.findByIdAndUpdate(req.params.id, { status: req.body.status });
     NotificationService.notifyOrderUpdate(order._id, order.status); // ⭐ ADD THIS LINE
     res.json(order);
   };
   ```

2. **New Service (Fully Spec-Driven):**
   ```
   src/services/notifications.js      # New file (SDD)
   src/websocket/notificationServer.js # New file (SDD)
   ```

3. **Schema Extension:**
   ```javascript
   // src/models/User.js (line 18 - EXTEND SCHEMA)
   notificationPreferences: {
     email: { type: Boolean, default: true },
     push: { type: Boolean, default: false }
   }
   ```

### Backwards Compatibility
✅ Existing endpoints unchanged
✅ Existing tests continue to pass
✅ New functionality is additive only
✅ Can be feature-flagged for gradual rollout
```

**Step 3: Implement with Integration Tests**

```markdown
# specs/features/001-realtime-notifications/TASKS.md

## Phase 1: Tests (Spec-Driven)
- [ ] Task 1.1: Write integration test for OrderController + NotificationService
- [ ] Task 1.2: Write unit tests for NotificationService
- [ ] Task 1.3: Validate existing OrderController tests still pass

## Phase 2: Implementation
- [ ] Task 2.1: Create NotificationService
- [ ] Task 2.2: Add single line to OrderController (integration point)
- [ ] Task 2.3: Extend User schema
- [ ] Task 2.4: Create WebSocket server

## Phase 3: Validation
- [ ] Task 3.1: Run existing test suite (must pass 100%)
- [ ] Task 3.2: Run new integration tests
- [ ] Task 3.3: Manual testing in staging (feature flag ON)
```

#### Phase 2: Reverse Engineer Existing Feature (Optional)

**When to Reverse Engineer:**
- Feature changes frequently → needs spec for evolution
- Critical path → needs documentation
- Complex business logic → needs clarity
- Planning refactoring → spec guides improvement

**Example: Document Existing Auth System**

```
Prompt to AI:
"Analyze src/controllers/UserController.js and src/models/User.js.
Create a SPEC.md documenting CURRENT behavior (not ideal behavior).
Use specs/templates/REVERSE_ENGINEER_TEMPLATE.md"
```

**Generated specs/existing/auth-system/SPEC.md:**
```markdown
# Existing Auth System (As-Is Documentation)

## Current Behavior (Reverse-Engineered)

### Story 1: User Registration
**Current Implementation:** `UserController.register` (line 23)

**Observed Behavior:**
1. Accepts: email, password, name
2. Validation: Email regex, password min 6 chars (⚠️ weak)
3. Password storage: bcrypt with cost 10
4. Response: User object with password hash included (⚠️ security issue)

**Issues:**
- ❌ Password strength too weak (only 6 chars)
- ❌ Response leaks password hash
- ❌ No email verification
- ❌ No duplicate email check (throws MongoDB error)

### Story 2: User Login
**Current Implementation:** `UserController.login` (line 67)

**Observed Behavior:**
1. Accepts: email, password
2. Session: express-session with MongoDB store
3. Session duration: 24 hours (non-sliding)
4. Failed login: No rate limiting (⚠️ brute force risk)

**Issues:**
- ❌ No rate limiting
- ❌ Error message reveals if email exists ("Invalid password" vs "User not found")
- ❌ No account lockout mechanism

## Refactoring Opportunities
See REFACTOR_PLAN.md
```

**Create Refactoring Plan:**
```markdown
# specs/existing/auth-system/REFACTOR_PLAN.md

## Incremental Improvements

### Phase 1: Quick Wins (No Breaking Changes)
1. **Fix Response Leakage**
   - Change: Remove password hash from registration response
   - Risk: Low (clients shouldn't use it anyway)
   - Effort: 1 hour

2. **Add Rate Limiting**
   - Change: Add express-rate-limit middleware
   - Risk: Low (only affects attackers)
   - Effort: 2 hours

### Phase 2: Backwards-Compatible Enhancements
3. **Strengthen Password Requirements**
   - Change: Min 12 chars, require complexity
   - Migration: Existing users grandfathered (required on next password change)
   - Risk: Low
   - Effort: 3 hours

4. **Standardize Error Messages**
   - Change: Always return "Invalid credentials"
   - Risk: Medium (may break client error handling)
   - Effort: 2 hours

### Phase 3: Breaking Changes (Coordinate with Frontend)
5. **Add Email Verification**
   - Change: Require email verification before login
   - Migration: Existing users marked as "verified"
   - Risk: High (requires frontend changes)
   - Effort: 1 week

## Implementation via SDD
Each improvement will:
1. Start with spec update (document desired behavior)
2. Write tests (TDD)
3. Implement changes
4. Validate against spec
```

### 4.4 Brownfield Success Criteria

✅ **Incremental Adoption:**
- 100% of new features use SDD
- 0% disruption to existing features
- Existing tests continue to pass

✅ **Integration Quality:**
- Clear integration contracts documented
- Backwards compatibility validated
- Feature flags for gradual rollout

✅ **Knowledge Transfer:**
- Critical paths documented via reverse-engineered specs
- Refactoring guided by specs
- Technical debt tracked and prioritized

---

## Part 5: Modern Legacy (Technology Pivots)

### 5.1 Legacy Modernization: Parallel Systems

**Context:** Replacing legacy system with modern implementation while maintaining feature parity.

**Philosophy:** Specs as **migration contracts** ensuring behavioral equivalence.

### 5.2 Legacy Modernization Folder Structure

```
legacy-modernization/
│
├── legacy/                             # Original system (READ-ONLY)
│   ├── src/                            # Legacy codebase (frozen)
│   │   └── com/company/app/            # Java monolith
│   │       ├── UserModule.java
│   │       ├── OrderModule.java
│   │       └── ReportingModule.java
│   │
│   ├── docs/                           # Legacy documentation
│   └── tests/                          # Legacy tests (keep as regression suite)
│
├── specs/                              # Migration workspace
│   ├── _meta/
│   │   ├── CONSTITUTION.md             # Modern architectural principles
│   │   ├── LEGACY_CONTEXT.md ⭐        # Understanding legacy system
│   │   ├── PARITY_REQUIREMENTS.md ⭐   # Feature parity checklist
│   │   ├── MIGRATION_PHILOSOPHY.md ⭐  # Migration approach
│   │   └── MODERNARCH.md               # Target modern architecture
│   │
│   ├── features/                       # Feature parity specs
│   │   ├── 001-user-management/
│   │   │   ├── SPEC.md ⭐              # Behavior from legacy (AS-IS)
│   │   │   ├── LEGACY_ANALYSIS.md ⭐   # Analysis of Java implementation
│   │   │   ├── PARITY_CHECKLIST.md ⭐  # Feature-by-feature comparison
│   │   │   ├── DESIGN.md               # Modern Node.js design
│   │   │   ├── MIGRATION_STRATEGY.md ⭐ # Cutover plan
│   │   │   ├── CONTRACTS/
│   │   │   │   ├── legacy-api.yaml ⭐  # Document legacy API
│   │   │   │   └── modern-api.yaml ⭐  # Modern API (compatible)
│   │   │   └── DATA_MIGRATION.md ⭐    # Oracle → PostgreSQL migration
│   │   │
│   │   ├── 002-order-processing/
│   │   └── 003-reporting-engine/
│   │
│   ├── experiments/                    # What-if scenarios ⭐
│   │   ├── 901-graphql-api/            # What if we use GraphQL?
│   │   ├── 902-event-sourcing/         # What if we use event sourcing?
│   │   └── 903-serverless/             # What if we go serverless?
│   │
│   └── templates/
│       ├── PARITY_SPEC_TEMPLATE.md ⭐
│       ├── LEGACY_ANALYSIS_TEMPLATE.md ⭐
│       └── MIGRATION_STRATEGY_TEMPLATE.md ⭐
│
├── modern/                             # NEW: Modern implementation
│   ├── services/                       # Microservices (from specs)
│   │   ├── user-service/               # From spec 001
│   │   │   ├── src/
│   │   │   ├── tests/
│   │   │   │   ├── unit/
│   │   │   │   ├── integration/
│   │   │   │   └── parity/ ⭐          # Validate against legacy behavior
│   │   │   └── package.json
│   │   │
│   │   ├── order-service/              # From spec 002
│   │   └── reporting-service/          # From spec 003
│   │
│   └── frontend/                       # React app (from specs)
│
├── migration/                          # Migration tooling ⭐
│   ├── data/
│   │   ├── etl-scripts/                # Extract-Transform-Load
│   │   ├── validation/                 # Data integrity checks
│   │   └── rollback/                   # Contingency plans
│   │
│   ├── cutover/
│   │   ├── phase1-readonly.sh          # Legacy writes, modern reads
│   │   ├── phase2-dualwrite.sh         # Dual write for validation
│   │   ├── phase3-modern-primary.sh    # Modern writes, legacy deprecated
│   │   └── phase4-decommission.sh      # Turn off legacy
│   │
│   └── validation/
│       ├── parity-tests/               # Compare legacy vs modern output
│       └── load-tests/                 # Performance comparison
│
├── docs/
│   ├── migration-log.md ⭐             # Daily progress tracking
│   ├── decision-records/               # Migration ADRs
│   └── runbooks/
│       ├── emergency-rollback.md
│       └── dual-system-operations.md
│
└── .ai/
    └── prompts/
        ├── analyze-legacy-code.md ⭐
        ├── document-behavior.md ⭐
        └── generate-parity-tests.md ⭐
```

**Key Legacy Modernization Artifacts:**

1. **`LEGACY_CONTEXT.md`** - Deep understanding of legacy system
2. **`PARITY_REQUIREMENTS.md`** - Must-maintain behaviors
3. **`LEGACY_ANALYSIS.md`** - Per-feature analysis of legacy code
4. **`PARITY_CHECKLIST.md`** - Feature-by-feature validation
5. **`DATA_MIGRATION.md`** - Database migration strategy
6. **`experiments/`** - Technology pivot evaluations
7. **`migration/`** - Cutover automation and validation

### 5.3 Legacy Modernization Workflow

#### Phase 0: Legacy Analysis

**Step 1: Understand Legacy System**

```
Prompt to AI:
"Analyze legacy/src/com/company/app/UserModule.java
Document in specs/_meta/LEGACY_CONTEXT.md:
- Architecture patterns
- Technology stack
- Business rules embedded in code
- Data model
- Known issues
- Dependencies"
```

**Generated LEGACY_CONTEXT.md:**
```markdown
# Legacy System Context

## System Overview
**Type:** Monolithic Java EE application
**Era:** Built 2008-2015
**Scale:** ~500K LOC, ~2M users
**Status:** Stable but costly to maintain

## Technology Stack
- **Backend:** Java 8, Spring Framework 4.x, Hibernate ORM
- **Database:** Oracle 12c
- **Frontend:** JSP + jQuery
- **App Server:** WebLogic 12c
- **Build:** Maven 3.x
- **Deployment:** Manual WAR deployment

## Architectural Patterns
### Pattern 1: Layered Architecture
```
Presentation (JSP)
      ↓
Controllers (Spring MVC)
      ↓
Services (Business Logic)
      ↓
DAOs (Hibernate)
      ↓
Oracle Database
```

### Pattern 2: Anemic Domain Model
- Domain objects are POJOs with getters/setters
- All business logic in Service layer
- Heavy use of utility classes

## Business Rules (Embedded in Code)

### User Management Module
**Location:** `UserService.java` (lines 156-234)

**Rule 1: Password Complexity**
```java
// Hard-coded in code (no configuration)
if (password.length() < 6) throw new ValidationException();
if (!password.matches(".*[A-Z].*")) throw new ValidationException();
```
⚠️ **Migration Note:** These rules MUST be preserved (user expectation)

**Rule 2: User Roles**
```java
// Enum: ADMIN, USER, GUEST
// Permissions hard-coded in switch statements
switch (user.getRole()) {
    case ADMIN: return fullAccess();
    case USER: return limitedAccess();
    case GUEST: return readOnlyAccess();
}
```
⚠️ **Migration Note:** Role logic scattered across 15 files (refactor opportunity)

**Rule 3: Session Management**
```java
// Sessions never expire (!!!)
session.setAttribute("user", user);
// No expiration set
```
⚠️ **Migration Note:** Change this (security issue), but phase gradually

## Data Model (Oracle)

### Users Table
```sql
CREATE TABLE USERS (
    ID NUMBER(10) PRIMARY KEY,
    EMAIL VARCHAR2(255) UNIQUE NOT NULL,
    PASSWORD_HASH VARCHAR2(255),    -- MD5 (!!!) - security issue
    ROLE VARCHAR2(20),
    CREATED_DATE DATE,
    LAST_LOGIN_DATE DATE
);
```
⚠️ **Migration Issues:**
1. Primary keys are Oracle sequences (PostgreSQL uses different approach)
2. MD5 passwords (weak) → migrate to bcrypt
3. VARCHAR2 → VARCHAR in PostgreSQL

## Known Issues
1. **Security:** MD5 password hashing (deprecated since 2005)
2. **Performance:** N+1 query problem in reporting module
3. **Scalability:** Single database, no horizontal scaling
4. **Maintainability:** 15-year-old codebase, few original developers remain
5. **Tech Debt:** Java 8 EOL, Oracle licensing costs

## Dependencies & Integrations
- **Payment Gateway:** Legacy SOAP API (v1.0 - deprecated)
- **Email Service:** SMTP (internal mail server)
- **File Storage:** NFS mount (single point of failure)
- **Audit Logging:** Oracle DBMS_FGA (proprietary)

## Migration Drivers
1. **Cost:** Oracle + WebLogic licensing ($$$)
2. **Talent:** Hard to hire Java EE developers
3. **Agility:** Monthly release cycle (want weekly/daily)
4. **Cloud:** Can't easily deploy to cloud (requires WebLogic)
```

**Step 2: Define Parity Requirements**

```markdown
# specs/_meta/PARITY_REQUIREMENTS.md

## Feature Parity Checklist

### Critical (MUST Maintain Exact Behavior)
- [ ] User login with exact same credentials
- [ ] Password rules (min 6 chars, 1 uppercase) - EVEN THOUGH WEAK
- [ ] Role-based access control (ADMIN, USER, GUEST)
- [ ] Order status workflow (New → Processing → Shipped → Delivered)
- [ ] Report calculations (EXACT decimal precision)

### Important (Maintain Intent, May Improve)
- [ ] Session management (improve expiration, but don't break existing sessions during migration)
- [ ] Error messages (maintain meaning, may improve formatting)
- [ ] API response structure (maintain fields, may add new ones)

### Nice-to-Have (Can Change)
- [ ] UI layout (complete redesign allowed)
- [ ] Performance characteristics (can improve)
- [ ] Admin tools (can modernize)

### Intentional Changes (MUST Communicate)
- [ ] Password hashing: MD5 → bcrypt (requires one-time rehash on login)
- [ ] Sessions: Never expire → 30-day expiration (better security)
- [ ] API versioning: None → /api/v2/ (backwards compatible v1 during transition)

## Validation Strategy
Each feature MUST pass:
1. **Functional Parity Tests:** Same inputs → same outputs
2. **Data Parity Tests:** Migrated data produces same results
3. **Performance Parity Tests:** Modern system meets or exceeds legacy performance
4. **Security Parity Tests:** No degradation in security posture (improvements OK)
```

**Step 3: Create Migration Philosophy**

```markdown
# specs/_meta/MIGRATION_PHILOSOPHY.md

## Approach: Strangler Fig Pattern

**Metaphor:** Strangle the legacy monolith by gradually replacing it piece by piece.

```
Phase 1: Parallel Systems (Read-Only)
┌─────────────────┐          ┌──────────────────┐
│  Legacy System  │────────→ │  Modern System   │
│  (Writes)       │ Mirror   │  (Reads+Validate)│
└─────────────────┘          └──────────────────┘
         ↓                            ↓
    Oracle DB              Validate Against Legacy

Phase 2: Dual-Write
┌─────────────────┐          ┌──────────────────┐
│  Legacy System  │←────────→│  Modern System   │
│  (Writes)       │ Dual     │  (Writes)        │
└─────────────────┘ Write    └──────────────────┘
         ↓                            ↓
    Oracle DB                   PostgreSQL
         ↓                            ↓
    Compare Consistency

Phase 3: Modern Primary
┌─────────────────┐          ┌──────────────────┐
│  Legacy System  │◀─────────│  Modern System   │
│  (Deprecated)   │ Fallback │  (Primary)       │
└─────────────────┘          └──────────────────┘

Phase 4: Decommission
┌─────────────────┐
│  Modern System  │
│  (Only)         │
└─────────────────┘
```

## Principles

### Principle 1: Feature Parity First, Improvements Later
- Migrate behavior AS-IS in Phase 1-3
- Introduce improvements in Phase 4+ (after legacy is off)
- Rationale: Reduces risk, easier to validate

### Principle 2: Incremental Cutover
- Migrate one module at a time (User → Order → Reporting)
- Each module goes through 4 phases independently
- Rationale: Limit blast radius, enable rollback

### Principle 3: Validation-Driven Migration
- Every migrated feature has parity tests
- Compare legacy vs modern outputs on production traffic (shadowing)
- Block cutover until 99.9% parity achieved
- Rationale: Data-driven confidence

### Principle 4: Rollback-Ready
- Maintain rollback scripts for each phase
- Practice rollback procedures weekly
- Maximum rollback time: 15 minutes
- Rationale: Production safety

## Timeline
- **Month 1-2:** Specs + modern implementation (parallel development)
- **Month 3:** Phase 1 deployment (read-only validation)
- **Month 4:** Phase 2 deployment (dual-write)
- **Month 5:** Phase 3 deployment (modern primary)
- **Month 6:** Phase 4 deployment (decommission legacy)
- **Total:** 6 months per major module
```

#### Phase 1: Per-Feature Migration

**Step 1: Analyze Legacy Feature**

```
Prompt to AI:
"Analyze legacy/src/com/company/app/UserModule.java
Create specs/features/001-user-management/LEGACY_ANALYSIS.md
Document:
- All public methods (these are de-facto API contracts)
- Business rules embedded in code
- Data model (tables, relationships)
- Integration points with other modules
- Error handling behavior
- Edge cases and quirks"
```

**Generated LEGACY_ANALYSIS.md:**
```markdown
# Legacy User Module Analysis

## Public API (De-Facto Contract)

### Method 1: registerUser
**Signature:**
```java
public User registerUser(String email, String password, String name)
    throws ValidationException, DuplicateEmailException
```

**Behavior:**
1. Validates email format (regex: `^[A-Za-z0-9+_.-]+@(.+)$`)
2. Validates password (min 6 chars, ≥1 uppercase)
3. Checks email uniqueness (SELECT COUNT FROM USERS WHERE EMAIL = ?)
4. Hashes password with MD5 (⚠️)
5. Assigns role = 'USER' (hardcoded)
6. Inserts to database
7. Returns User object (includes password hash - ⚠️ security issue)

**Edge Cases:**
- Empty email → throws ValidationException("Email required")
- Null password → NullPointerException (⚠️ not handled)
- Duplicate email → DuplicateEmailException with email in message (⚠️ info leak)

**Quirks:**
- ⚠️ **User ID is Oracle sequence** (legacy.USERS_SEQ.NEXTVAL)
  - Migration: Must maintain ID continuity or update all foreign keys

### Method 2: loginUser
**Signature:**
```java
public Session loginUser(String email, String password)
    throws AuthenticationException
```

**Behavior:**
1. Lookup user by email (SELECT * FROM USERS WHERE EMAIL = ?)
2. If not found → throws AuthenticationException("User not found") ⚠️
3. Compare password: MD5(input) == stored hash
4. If mismatch → throws AuthenticationException("Invalid password") ⚠️
5. Create session (no expiration)
6. Update LAST_LOGIN_DATE
7. Returns Session object

**Edge Cases:**
- User exists but password wrong → different error than user not found ⚠️
  - Migration Note: MUST preserve this (even though bad practice) for parity
- Account locked (LOCKED = 1) → no special handling (can still login) ⚠️

**Quirks:**
- Error messages reveal if email exists (security issue)
- Sessions stored in-memory (lost on server restart)

## Data Model

### USERS Table (Oracle)
```sql
CREATE TABLE USERS (
    ID NUMBER(10) PRIMARY KEY,
    EMAIL VARCHAR2(255) UNIQUE,
    PASSWORD_HASH VARCHAR2(255),  -- MD5, 32 chars
    NAME VARCHAR2(100),
    ROLE VARCHAR2(20),            -- 'ADMIN', 'USER', 'GUEST'
    LOCKED NUMBER(1) DEFAULT 0,   -- Boolean via NUMBER
    CREATED_DATE DATE,
    LAST_LOGIN_DATE DATE
);

CREATE SEQUENCE USERS_SEQ START WITH 1;
```

**Migration to PostgreSQL:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,        -- Auto-increment (different from Oracle)
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),   -- Will be bcrypt (60 chars)
    name VARCHAR(100),
    role VARCHAR(20),
    locked BOOLEAN DEFAULT FALSE, -- Native boolean
    created_date TIMESTAMP DEFAULT NOW(),
    last_login_date TIMESTAMP
);

-- ⚠️ ISSUE: Oracle sequences start at 1, PostgreSQL SERIAL starts at next available
-- Must set nextval manually after data migration
```

## Business Rules

### Rule 1: Role Assignment
```java
// Line 78
user.setRole("USER");  // All new users are 'USER'
```
**Migration:** Preserve exact behavior (even though inflexible)

### Rule 2: Password Strength (Hard-Coded)
```java
// Line 45-47
if (password.length() < 6) throw new ValidationException("Password must be at least 6 characters");
if (!password.matches(".*[A-Z].*")) throw new ValidationException("Password must contain uppercase letter");
```
**Migration:** Preserve weak rules initially (improve in Phase 4)

### Rule 3: Email Uniqueness (Case-Sensitive)
```java
// Line 52
String sql = "SELECT COUNT(*) FROM USERS WHERE EMAIL = ?";  // Case-sensitive
```
**Migration:** Preserve case-sensitivity (even though users may expect case-insensitive)

## Integration Points

### Integration 1: Order Module
**Caller:** OrderService.createOrder(userId)
**Contract:** UserService validates userId exists
```java
// OrderService.java line 234
User user = userService.getUserById(userId);
if (user == null) throw new InvalidUserException();
```
**Migration Note:** Modern user-service must expose GET /users/:id endpoint

### Integration 2: Audit Logging
**Caller:** AuditService.logUserAction(userId, action)
**Contract:** Every login/logout triggers audit log
**Migration Note:** Must maintain audit log format for compliance

## Parity Checklist

- [ ] Registration: Same validation errors for same inputs
- [ ] Registration: User ID assignment (may differ, but must update FKs)
- [ ] Registration: Password hash (MD5 → bcrypt requires migration)
- [ ] Login: Same error messages (even "User not found" vs "Invalid password")
- [ ] Login: Session behavior (improve expiration, but don't break existing)
- [ ] Data: All user records migrated with ID preservation
- [ ] Integration: OrderService continues to work (no breaking changes)
```

**Step 2: Write Parity Spec**

```markdown
# specs/features/001-user-management/SPEC.md

## Overview
User management system with feature parity to legacy Java module.

## Parity Requirements ⭐

### MUST Maintain (Exact Behavior)
This spec documents CURRENT legacy behavior, not ideal behavior.
Improvements are deferred to Phase 4 (post-migration).

## User Stories (From Legacy)

### Story 1.1: User Registration (Parity)
**As a** new user
**I want to** register with email and password
**So that** I can access the platform

**Acceptance Criteria (Legacy Behavior):**
1. ✅ Email format validation: `^[A-Za-z0-9+_.-]+@(.+)$`
2. ✅ Password minimum 6 characters (⚠️ weak but required for parity)
3. ✅ Password requires ≥1 uppercase letter
4. ✅ Duplicate email → "Email already exists" error
5. ✅ Null password → NullPointerException (⚠️ bug but preserved for parity)
6. ✅ Role assigned as 'USER' (hardcoded)
7. ✅ Returns User object including password hash (⚠️ security issue but preserved)

**Parity Validation:**
```javascript
// Test legacy and modern with same inputs
const legacyResult = await legacyAPI.post('/user/register', { email: 'test@example.com', password: 'Pass123' });
const modernResult = await modernAPI.post('/api/v2/users', { email: 'test@example.com', password: 'Pass123' });

// MUST match
expect(modernResult.email).toBe(legacyResult.email);
expect(modernResult.role).toBe(legacyResult.role);
// Note: password_hash will differ (MD5 vs bcrypt) - handle in migration
```

### Story 1.2: User Login (Parity)
**Acceptance Criteria (Legacy Behavior):**
1. ✅ Valid credentials → session created (no expiration - ⚠️ but preserved)
2. ✅ Invalid password → "Invalid password" error
3. ✅ Unknown email → "User not found" error (⚠️ leaks info but preserved)
4. ✅ Updates LAST_LOGIN_DATE
5. ✅ No rate limiting (⚠️ security issue but preserved initially)

## Data Migration Plan

### Phase 1: Initial Data Migration
```sql
-- Oracle → PostgreSQL ETL
INSERT INTO users (id, email, password_hash, name, role, locked, created_date, last_login_date)
SELECT
    ID,
    EMAIL,
    PASSWORD_HASH,  -- MD5 initially (will rehash on first login)
    NAME,
    ROLE,
    CASE WHEN LOCKED = 1 THEN TRUE ELSE FALSE END,
    CREATED_DATE,
    LAST_LOGIN_DATE
FROM legacy.USERS;

-- Set sequence to max ID + 1
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
```

### Phase 2: Password Migration (Gradual)
```javascript
// On first successful login, rehash
if (user.password_hash.length === 32) {  // MD5 hash
    if (md5(password) === user.password_hash) {
        user.password_hash = await bcrypt.hash(password, 12);
        await user.save();
        // User now has bcrypt hash for future logins
    }
}
```

## Intentional Deviations (Documented)

### Deviation 1: Password Hashing (MD5 → bcrypt)
- **Reason:** Security requirement (MD5 is broken)
- **Impact:** Password hashes won't match byte-for-byte
- **Mitigation:** Gradual migration (rehash on first login)
- **Parity Test:** Functional parity (same password validates), not byte parity

### Deviation 2: Session Expiration (None → 30 days)
- **Reason:** Security improvement
- **Impact:** Users may be logged out after 30 days inactivity
- **Mitigation:** Phase in gradually (30 days → 7 days → 1 day over 3 months)
- **Parity Test:** Not tested (intentional deviation)

## Improvements Deferred to Phase 4
- Strengthen password requirements (12+ chars)
- Case-insensitive email matching
- Rate limiting on login
- Consistent error messages (don't reveal if email exists)
- Remove password hash from registration response
```

**Step 3: Implement Modern Service with Parity Tests**

```markdown
# specs/features/001-user-management/TASKS.md

## Phase 1: Parity Test Suite (BEFORE Implementation)

### Task 1.1: Legacy Behavior Capture
- [ ] Run legacy system with test inputs
- [ ] Capture all responses (success + error cases)
- [ ] Document quirks and edge cases
- [ ] Create golden master test dataset

### Task 1.2: Parity Test Framework
- [ ] Create `tests/parity/001-user-management.parity.test.js`
- [ ] Test: Registration with valid inputs
- [ ] Test: Registration with duplicate email
- [ ] Test: Registration with weak password
- [ ] Test: Registration with null password (expect NullPointerException)
- [ ] Test: Login with valid credentials
- [ ] Test: Login with wrong password (expect specific error message)
- [ ] Test: Login with unknown email (expect specific error message)

### Task 1.3: Data Migration Validation
- [ ] Migrate 100 test users from Oracle to PostgreSQL
- [ ] Validate all fields match (except password hash)
- [ ] Validate foreign key relationships preserved
- [ ] Validate sequence next value set correctly

## Phase 2: Modern Implementation

### Task 2.1: User Service (Matches Legacy Contract)
- [ ] Implement POST /api/v2/users (registration)
- [ ] Implement POST /api/v2/auth/login (login)
- [ ] Implement GET /api/v2/users/:id (for OrderService integration)
- [ ] Match exact validation rules (even weak ones)
- [ ] Match exact error messages

### Task 2.2: Password Migration Logic
- [ ] Implement MD5-to-bcrypt gradual migration
- [ ] Test with migrated user (MD5 hash)
- [ ] Test rehashing on first login
- [ ] Test subsequent logins use bcrypt

## Phase 3: Parity Validation

### Task 3.1: Functional Parity Tests
- [ ] Run parity test suite
- [ ] 100% of tests must pass
- [ ] Document any deviations (with justification)

### Task 3.2: Integration Parity Tests
- [ ] Test OrderService integration (modern user-service + legacy OrderService)
- [ ] Validate no breaking changes

### Task 3.3: Load Testing
- [ ] Compare performance: legacy vs modern
- [ ] Modern must meet or exceed legacy (100 req/s baseline)

## Phase 4: Deployment (Strangler Pattern)

### Task 4.1: Phase 1 - Read-Only Validation
- [ ] Deploy modern service (reads from PostgreSQL replica of Oracle)
- [ ] Shadow traffic: Send all requests to both systems
- [ ] Compare outputs (log discrepancies)
- [ ] Achieve 99.9% parity before proceeding

### Task 4.2: Phase 2 - Dual-Write
- [ ] Write to both Oracle (via legacy) and PostgreSQL (via modern)
- [ ] Compare data consistency daily
- [ ] Achieve 99.99% consistency before proceeding

### Task 4.3: Phase 3 - Modern Primary
- [ ] Route 1% of traffic to modern service
- [ ] Monitor errors, rollback if issues
- [ ] Gradually increase to 10%, 50%, 100%
- [ ] Legacy remains as fallback (degraded mode)

### Task 4.4: Phase 4 - Decommission
- [ ] Turn off legacy service
- [ ] Archive legacy database (read-only backup)
- [ ] Celebrate! 🎉
```

#### Phase 2: Experimental Specs (What-If Scenarios)

**Use Case:** Evaluate technology pivots BEFORE committing.

**Example: Should we use GraphQL instead of REST?**

```markdown
# specs/experiments/901-graphql-api/SPEC.md

## Experiment: GraphQL API for User Management

### Hypothesis
GraphQL will reduce API calls and improve frontend performance compared to REST.

### Implementation
Create parallel implementation of user-service using GraphQL schema.

### Schema
```graphql
type User {
  id: ID!
  email: String!
  name: String!
  role: Role!
  createdAt: DateTime!
}

enum Role {
  ADMIN
  USER
  GUEST
}

type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
}

type Mutation {
  registerUser(email: String!, password: String!, name: String!): User!
  loginUser(email: String!, password: String!): Session!
}
```

### Success Criteria
- [ ] 30% reduction in frontend API calls
- [ ] 20% improvement in page load time
- [ ] Developer satisfaction >8/10
- [ ] Learning curve <1 week

### Comparison
```javascript
// REST (multiple calls)
const user = await fetch('/api/v2/users/123');
const orders = await fetch('/api/v2/users/123/orders');
const preferences = await fetch('/api/v2/users/123/preferences');

// GraphQL (single call)
const data = await graphql.query(`{
  user(id: "123") {
    id name email
    orders { id status }
    preferences { notifications }
  }
}`);
```

### Decision Point
After 2-week POC:
- If success criteria met → Adopt GraphQL for all new services
- If not met → Stick with REST

### Implementation
See modern/experiments/user-service-graphql/
```

**Benefits of Experimental Specs:**
1. **De-risk technology decisions** - Try before committing
2. **Compare implementations** - Side-by-side code for evaluation
3. **Data-driven decisions** - Success criteria measured objectively
4. **Parallel development** - Experiment doesn't block main migration

### 5.4 Legacy Modernization Success Criteria

✅ **Feature Parity:**
- 99.9% functional parity validated by tests
- All legacy integrations continue working
- Data migrated with zero loss

✅ **Phased Cutover:**
- Each module goes through 4 phases independently
- Rollback plan tested and ready
- Maximum rollback time <15 minutes

✅ **Performance:**
- Modern system meets or exceeds legacy performance
- Scalability improvements validated under load

✅ **Knowledge Transfer:**
- Specs document all legacy behavior (tacit knowledge captured)
- New team can maintain modern system without legacy expertise

---

## Part 6: Universal Practices (All Contexts)

### 6.1 Specification Quality Checklist

**Use this checklist regardless of tool or context:**

#### Completeness
- [ ] **User stories** defined with actors, goals, benefits
- [ ] **Acceptance criteria** are testable (verifiable true/false)
- [ ] **Non-functional requirements** included (performance, security, compliance)
- [ ] **Out of scope** explicitly stated (prevents scope creep)
- [ ] **Success metrics** defined (how we measure success)

#### Clarity
- [ ] **No ambiguity** - Every requirement has one interpretation
- [ ] **Marked uncertainties** - Use `[NEEDS CLARIFICATION]` for unknowns
- [ ] **Domain terminology** defined in glossary
- [ ] **Examples provided** for complex behaviors
- [ ] **Diagrams included** for visual concepts (workflows, architecture)

#### Testability
- [ ] **Acceptance criteria → Tests** - Each criterion maps to automated test
- [ ] **Edge cases documented** - Boundary conditions, error cases, quirks
- [ ] **Contract defined** - API/data schemas in machine-readable format
- [ ] **Validation strategy** - How we verify implementation matches spec

#### Maintainability
- [ ] **Versioned** - Spec evolves with feature (CHANGELOG.md)
- [ ] **Traced** - Links to code, tests, docs
- [ ] **Reviewed** - Spec reviewed before implementation starts
- [ ] **Synchronized** - Spec updates when code changes

### 6.2 Constitutional Principles (Greenfield & Brownfield)

**Principles that work across all contexts:**

#### Principle 1: Specifications Are Contracts
- Specs define expected behavior
- Tests validate the contract
- Code implements the contract
- All three must stay synchronized

#### Principle 2: Test-First Development
- Tests written BEFORE implementation
- Tests validate specs (not just code)
- Contract tests verify API/data schemas
- Tests are spec enforcement mechanism

#### Principle 3: Progressive Formalization
- Start informal for exploration (Spec-First)
- Formalize for production (Spec-Anchored)
- Fully generative for strategic components (Spec-as-Source)
- Match formalization level to feature importance

#### Principle 4: Simplicity Over Complexity
- Justify every dependency
- Track complexity budget
- Prefer standard library over external dependencies
- Document rationale for complexity

#### Principle 5: Security and Compliance First
- Threat modeling for sensitive features
- Compliance requirements (GDPR, HIPAA, SOC2) documented in specs
- Security review before implementation
- Audit logging for accountability

### 6.3 Workflow Integration (Any AI Tool)

**Generic workflow that adapts to any AI assistant:**

#### Step 1: Context Loading
```
Load into AI conversation:
1. specs/_meta/CONSTITUTION.md
2. specs/_meta/ARCHITECTURE.md
3. specs/_meta/TECH_STACK.md
4. specs/templates/FEATURE_SPEC_TEMPLATE.md
```

#### Step 2: Specification Generation
```
Prompt:
"Using the FEATURE_SPEC_TEMPLATE, create a specification for:
[Feature description]

Focus on WHAT users need and WHY they need it.
Do NOT specify HOW to implement (no tech stack yet).
Mark ambiguities with [NEEDS CLARIFICATION].
Save to specs/features/[NNN]-[feature-name]/SPEC.md"
```

#### Step 3: Clarification Loop
```
Prompt:
"Review SPEC.md and identify all [NEEDS CLARIFICATION] markers.
For each marker, generate a clarifying question.
Once clarified, update SPEC.md to remove markers."
```

#### Step 4: Design Generation
```
Prompt:
"Using TECH_STACK.md and ARCHITECTURE.md, create DESIGN.md for this feature.

Include:
- Component architecture
- Data model (database schema)
- API contracts (OpenAPI/GraphQL schema)
- Dependencies (justify each per CONSTITUTION.md)
- Security analysis (threat model)
- Constitutional compliance checklist

Save to specs/features/[NNN]-[feature-name]/DESIGN.md"
```

#### Step 5: Task Generation
```
Prompt:
"From DESIGN.md, create TASKS.md with executable steps.

Requirements:
- Order tasks by dependencies
- Test-writing tasks BEFORE implementation tasks (Test-First principle)
- Mark parallel tasks with [P]
- Include validation tasks (contract tests, parity tests, security scans)

Save to specs/features/[NNN]-[feature-name]/TASKS.md"
```

#### Step 6: Implementation
```
Prompt:
"Execute TASKS.md in order.
After each task, show results and wait for approval.
Follow DESIGN.md exactly.
Validate against SPEC.md acceptance criteria."
```

**This workflow works with:**
- GitHub Copilot (via comments or Workspace)
- Claude Code (via conversation)
- Cursor (via Composer or Chat)
- ChatGPT (via multi-turn conversation)
- Custom AI tools (via API integration)

### 6.4 Measuring Success (Universal Metrics)

**Track these metrics regardless of tool:**

#### Leading Indicators (Process Quality)
| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Spec Clarity** | <5% clarification requests | Count `[NEEDS CLARIFICATION]` removals per spec |
| **Spec Review Time** | <30 min per spec | PR review duration for specs/ changes |
| **First-Pass Success** | >80% tasks complete without rework | Track task completion vs. revision count |
| **Constitutional Compliance** | 100% specs pass | Automated validation (scripts or manual checklist) |
| **Test Coverage** | >80% for spec-driven code | Code coverage tools (Jest, pytest, etc.) |

#### Lagging Indicators (Outcome Quality)
| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Time to Feature** | 30-50% reduction | Feature delivery time (spec creation → production) |
| **Defect Density** | <0.5 defects per KLOC | Post-release bug tracking |
| **Spec-Code Drift** | <10% of features | Manual review or automated drift detection |
| **Documentation Currency** | >90% specs up-to-date | Compare spec last-modified vs. code last-modified |
| **Developer Satisfaction** | >7/10 on SDD workflow | Quarterly surveys |

#### Adoption Metrics (Organizational Change)
| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Spec Coverage** | >60% of new features | Track features with specs vs. total features |
| **Team Adoption** | >70% developers participating | Count developers contributing to specs/ |
| **Brownfield Progress** | Incremental increase | Track reverse-engineered specs per month |
| **Legacy Migration** | Per module milestones | Track features migrated vs. total features |

---

## Part 7: Tool Selection Guide

### 7.1 Evaluation Criteria

**Choose tools based on your context and needs:**

| Criterion | Greenfield | Brownfield | Legacy | Weight |
|-----------|------------|------------|--------|--------|
| **Ease of Setup** | High | Medium | Low | 20% |
| **Template Customization** | High | High | Critical | 25% |
| **Integration with Existing Code** | Low | Critical | Critical | 30% |
| **AI Quality** | High | High | High | 15% |
| **Community/Support** | Medium | Medium | Medium | 10% |

### 7.2 Tool Landscape (Vendor-Agnostic)

#### Option 1: Custom Prompts + Any AI
**Best for:** Maximum flexibility, no tool lock-in

**Setup:**
1. Create folder structure manually (see Part 2)
2. Write custom prompts (in `.ai/prompts/`)
3. Use any AI assistant (ChatGPT, Claude, Gemini, etc.)
4. Manually manage workflow

**Pros:**
✅ No dependencies on specific tools
✅ Full control over process
✅ Works with any AI model

**Cons:**
❌ Manual workflow management
❌ No automation
❌ Requires discipline

**When to use:** Small teams, maximum flexibility, experimental adoption

---

#### Option 2: spec-kit (GitHub)
**Best for:** Structured workflow, multiple AI integrations

**Setup:**
```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify init my-project --ai copilot
```

**Pros:**
✅ 30+ AI agent integrations (Copilot, Claude, Cursor, etc.)
✅ Template-driven quality (constitutional enforcement)
✅ Extension ecosystem (275+ community extensions)
✅ Workflow automation (/speckit.specify → plan → implement)

**Cons:**
❌ Opinionated structure (may not fit all teams)
❌ Learning curve for extension system
❌ Tool-specific conventions

**When to use:** Greenfield projects, teams wanting structured approach, GitHub ecosystem

---

#### Option 3: Kiro (Martin Fowler Example)
**Best for:** Lightweight workflow, minimalist approach

**Pros:**
✅ Simple workflow (steering → feature → requirements → design → tasks)
✅ Less tooling overhead
✅ Familiar to agile teams

**Cons:**
❌ Less mature than spec-kit
❌ Fewer integrations
❌ Smaller community

**When to use:** Teams preferring simplicity over features

---

#### Option 4: Tessl (Spec-as-Source Focus)
**Best for:** True spec-as-source (generated code only)

**Setup:**
```bash
tessl document --code src/existing.js  # Reverse engineer
tessl implement --spec feature.spec.md  # Generate code
```

**Pros:**
✅ Only tool explicitly pursuing spec-as-source
✅ Reverse engineering support (brownfield)
✅ Clear "DO NOT EDIT" markers on generated code

**Cons:**
❌ High commitment (full spec-as-source or nothing)
❌ Less flexible for hybrid workflows
❌ Newer tool (less battle-tested)

**When to use:** Teams fully committed to spec-as-source, frequent tech pivots

---

#### Option 5: Hybrid Approach
**Best for:** Enterprise teams, gradual adoption

**Setup:**
- Use custom prompts for specs (tool-agnostic)
- Use spec-kit for automation (where beneficial)
- Use traditional development where SDD doesn't fit

**Pros:**
✅ Flexibility to mix approaches
✅ Gradual adoption path
✅ Use best tool for each context

**Cons:**
❌ More complex setup
❌ Requires clear conventions (when to use what)

**When to use:** Large enterprises, brownfield-heavy environments

---

### 7.3 Decision Matrix

```
┌─────────────────────────────────────────────────────────────┐
│ Choose Your Tool Based on Context                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  GREENFIELD + SMALL TEAM (3-5 devs)                         │
│    → Custom Prompts + Any AI                                │
│    → Rationale: Flexibility, no tool overhead               │
│                                                             │
│  GREENFIELD + STRUCTURED TEAM (6-15 devs)                   │
│    → spec-kit                                               │
│    → Rationale: Workflow automation, consistency            │
│                                                             │
│  BROWNFIELD + INCREMENTAL ADOPTION                          │
│    → Hybrid (Custom prompts + optional spec-kit)            │
│    → Rationale: Gradual adoption, no disruption             │
│                                                             │
│  LEGACY MODERNIZATION                                       │
│    → Tessl (reverse engineering) OR spec-kit (parity specs) │
│    → Rationale: Tooling for migration workflows             │
│                                                             │
│  ENTERPRISE + MULTI-TEAM                                    │
│    → Hybrid (Custom framework + standardized templates)     │
│    → Rationale: Flexibility with governance                 │
│                                                             │
│  EXPLORATION / PROTOTYPING                                  │
│    → Custom Prompts + ChatGPT/Claude                        │
│    → Rationale: Fastest to start, lowest commitment         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Part 8: Getting Started (Practical Steps)

### 8.1 Day 1: Initial Setup (2 hours)

**For Greenfield:**
```bash
# 1. Create folder structure
mkdir -p my-project/specs/{_meta,features,templates}
mkdir -p my-project/src/{libs,apps}
mkdir -p my-project/tests/{specs,unit,integration}

# 2. Create constitution
cat > my-project/specs/_meta/CONSTITUTION.md << EOF
# Project Constitution

## Principle 1: Specifications Are Contracts
Every feature MUST have a spec that defines expected behavior.

## Principle 2: Test-First Development
Tests MUST be written before implementation code.

## Principle 3: Simplicity First
Justify complexity. Start with <3 dependencies per feature.

## Principle 4: Security First
Sensitive features MUST include threat modeling.

## Principle 5: Progressive Formalization
Match spec formality to feature importance.
EOF

# 3. Create first spec template
cat > my-project/specs/templates/FEATURE_SPEC_TEMPLATE.md << EOF
# Feature NNN: [Feature Name]

## Overview
[Brief description]

## User Stories
### Story N.1: [Story Name]
**As a** [actor]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
1. [Testable criterion]
2. [Testable criterion]

## Non-Functional Requirements
- Performance: [metrics]
- Security: [requirements]
- Compliance: [standards]

## Out of Scope
- [Future work]

## Success Metrics
- [How we measure success]
EOF

# 4. Initialize version control
cd my-project
git init
git add specs/ src/ tests/
git commit -m "Initial SDD project structure"
```

**For Brownfield:**
```bash
# 1. Add specs workspace to existing project
cd existing-project
mkdir -p specs/{_meta,features,existing,templates}

# 2. Document existing architecture
# (Use AI to analyze your codebase)
cat > specs/_meta/EXISTING_ARCH.md << EOF
# Existing Architecture

## Technology Stack
- [Current technologies]

## Pain Points
- [Known issues]

## Constraints
- [What can't change]
EOF

# 3. Create migration strategy
cat > specs/_meta/MIGRATION_STRATEGY.md << EOF
# SDD Adoption Strategy

## Phase 1: New Features Only
- All new features use SDD
- Existing code unchanged

## Phase 2: Document Critical Paths
- Reverse engineer top 5 most-changed features

## Timeline
- Month 1-3: Phase 1
- Month 4-6: Phase 2
EOF

# 4. Commit specs workspace
git add specs/
git commit -m "Add SDD workspace for gradual adoption"
```

**For Legacy:**
```bash
# 1. Create migration workspace
mkdir -p legacy-modernization/{legacy,specs,modern,migration}

# 2. Archive legacy code (read-only)
cp -r /path/to/legacy/src legacy/src

# 3. Create parity requirements
cat > specs/_meta/PARITY_REQUIREMENTS.md << EOF
# Feature Parity Checklist

## Critical (MUST Maintain)
- [List must-maintain behaviors]

## Important (Maintain Intent)
- [List behaviors to preserve with improvements]

## Intentional Changes
- [List planned deviations with rationale]
EOF
```

### 8.2 Week 1: First Feature (8-16 hours)

**Step-by-Step:**

**Day 1-2: Write Specification**
1. Load constitution into AI context
2. Generate SPEC.md using template
3. Review for clarity and completeness
4. Mark `[NEEDS CLARIFICATION]` areas
5. Clarify with stakeholders
6. Peer review spec
7. Commit to version control

**Day 3: Design**
1. Load tech stack context into AI
2. Generate DESIGN.md with contracts
3. Review for constitutional compliance
4. Architect review
5. Commit design

**Day 4-5: Implement**
1. Generate TASKS.md
2. Write tests first (per Task 1.x)
3. Validate tests fail (red phase)
4. Implement minimum code (green phase)
5. Refactor for quality
6. Validate against spec

**Deliverables:**
- ✅ specs/features/001-[feature]/SPEC.md
- ✅ specs/features/001-[feature]/DESIGN.md
- ✅ specs/features/001-[feature]/TASKS.md
- ✅ specs/features/001-[feature]/CONTRACTS/*.yaml
- ✅ src/libs/[feature]/
- ✅ tests/specs/[feature].spec.test.js
- ✅ tests/unit/[feature]/*.test.js

### 8.3 Month 1: Team Onboarding

**Week 1:** Individual learning (each developer does first feature)
**Week 2:** Pair programming (experienced + new)
**Week 3:** Team retrospective (what's working, what's not)
**Week 4:** Process refinement (update templates, constitution)

**Onboarding Checklist:**
- [ ] Read CONSTITUTION.md
- [ ] Review example specs (001, 002, 003)
- [ ] Complete first feature (with mentor)
- [ ] Participate in spec review
- [ ] Provide feedback on templates

---

## Conclusion

This vendor-agnostic framework provides the foundation for Spec-Driven Development across **any context** (Greenfield, Brownfield, Legacy), using **any AI tool**, with **any tech stack**.

### Key Principles to Remember:

1. **Specifications Are Executable** - Not documentation, but contracts
2. **Natural Language > Formal Syntax** - Readable by humans and AI
3. **Progressive Formalization** - Match rigor to feature importance
4. **Context Matters** - Greenfield ≠ Brownfield ≠ Legacy
5. **Tool-Agnostic** - Principles over tools

### Next Steps:

1. **Evaluate Your Context:** Greenfield, Brownfield, or Legacy?
2. **Choose Maturity Level:** Spec-First, Spec-Anchored, or Spec-as-Source?
3. **Select Tools:** Custom prompts, spec-kit, Kiro, Tessl, or hybrid?
4. **Start Small:** One feature, one team, one month
5. **Measure & Iterate:** Track metrics, refine process

**Remember:** SDD is a paradigm shift, not a silver bullet. Start with principles, experiment with tools, and evolve your practice based on real-world results.

---

**Document Version:** 1.0
**Last Updated:** April 24, 2026
**Applies To:** Any AI tool, any tech stack, any team size
