# Spec-Driven Development: Comprehensive Research Report

## Executive Summary

Spec-Driven Development (SDD) represents a fundamental paradigm shift in software development where **specifications become executable artifacts** that generate code, rather than merely guiding it. This research synthesizes findings from GitHub's spec-kit project, Martin Fowler's analysis, and enterprise adoption patterns.

---

## 1. Core Concepts

### 1.1 Definition and Principles

**Primary Definition:**
> "Spec-Driven Development inverts the power structure. Specifications don't serve code—code serves specifications. The Product Requirements Document (PRD) isn't a guide for implementation; it's the source that generates implementation."
> — GitHub spec-driven.md

**Key Characteristics:**
- **Specifications as executable artifacts**: Not documentation that gets outdated, but living source files
- **Intent-driven development**: Natural language specifications express the "what" and "why"
- **Lingua franca shift**: Development communication moves to higher abstraction (specs), code becomes "last-mile approach"
- **Continuous transformation**: Maintaining software means evolving specifications, not just modifying code

### 1.2 Three Implementation Levels

Martin Fowler's analysis identifies three distinct implementation levels:

#### **1. Spec-First**
- A well thought-out spec is written first
- Used in AI-assisted development workflow for the task at hand
- Spec may be discarded after feature completion
- **Lifecycle**: Creation only

#### **2. Spec-Anchored**
- Spec is kept after task completion
- Continues to be used for evolution and maintenance
- Spec and code both maintained by humans and AI
- **Lifecycle**: Creation + Evolution

#### **3. Spec-as-Source**
- Spec is the main source file over time
- Only spec is edited by humans; code is generated
- Code marked as `// GENERATED FROM SPEC - DO NOT EDIT`
- **Lifecycle**: Creation + Evolution (spec-only)

**Quote from Martin Fowler article:**
> "All SDD approaches and definitions I've found are spec-first, but not all strive to be spec-anchored or spec-as-source. And often it's left vague or totally open what the spec maintenance strategy over time is meant to be."

### 1.3 What is a Spec?

**Structured Definition:**
> "A spec is a structured, behavior-oriented artifact - or a set of related artifacts - written in natural language that expresses software functionality and serves as guidance to AI coding agents."
> — Martin Fowler article

**Key Distinctions:**

| Aspect | Specs | Memory Bank |
|--------|-------|-------------|
| **Purpose** | Define specific features/functionality | General project context |
| **Scope** | Task-specific, feature-specific | Project-wide, cross-cutting |
| **Examples** | Story-324.md, product-search.md | AGENTS.md, constitution.md, architecture.md |
| **Lifecycle** | Created/updated per feature | Long-lived, rarely changed |
| **Relevance** | Only for tasks affecting that feature | All AI coding sessions |

### 1.4 How SDD Differs from Traditional Methodologies

**vs. Traditional Development:**
- **Code was truth** → Specs are truth
- **Specs guide coding** → Specs generate coding
- **Gap between spec and implementation** → No gap, only transformation
- **Documentation falls behind** → Documentation is the source

**vs. TDD (Test-Driven Development):**
- TDD: Write tests → Write code → Refactor
- SDD: Write specs → Generate plan → Generate tasks → Generate code + tests
- Both emphasize "definition before implementation"
- SDD operates at higher abstraction (natural language vs. code)

**vs. BDD (Behavior-Driven Development):**
- BDD: Given-When-Then scenarios drive implementation
- SDD: Comprehensive PRD-style specs drive implementation
- BDD is more narrow (scenarios), SDD is broader (complete system definition)

**vs. Model-Driven Development (MDD):**
> "Ultimately, MDD never took off for business applications, it sits at an awkward abstraction level and just creates too much overhead and constraints. But LLMs take some of the overhead and constraints of MDD away... With LLMs, we are not constrained by a predefined and parseable spec language anymore, and we don't have to build elaborate code generators. The price for that is LLMs' non-determinism of course."
> — Martin Fowler article

---

## 2. Enterprise Adoption Patterns

### 2.1 Greenfield Projects: Starting from Scratch

**Workflow:**
```
Constitution → Specify → Plan → Tasks → Implement
```

**Recommended approach from spec-kit:**

1. **Establish Constitutional Foundation** (`/speckit.constitution`)
   - Define immutable project principles
   - Set architectural standards
   - Establish quality gates
   - Example: "All features MUST begin as standalone libraries"

2. **Create Feature Specification** (`/speckit.specify`)
   - Focus on WHAT users need and WHY
   - Avoid HOW to implement (no tech stack yet)
   - Use `[NEEDS CLARIFICATION]` markers for ambiguities
   - Generate user stories with acceptance criteria

3. **Clarify Underspecified Areas** (`/speckit.clarify`)
   - Structured questioning workflow
   - Coverage-based sequential clarification
   - Record answers in Clarifications section
   - Run BEFORE creating technical plan

4. **Generate Implementation Plan** (`/speckit.plan`)
   - NOW specify tech stack and architecture
   - Create data models, API contracts
   - Research technology choices with rationale
   - Validate against constitutional principles

5. **Create Task Breakdown** (`/speckit.tasks`)
   - Parse plan and design documents
   - Order tasks respecting dependencies
   - Mark parallel execution opportunities `[P]`
   - Map tasks to specific file paths

6. **Execute Implementation** (`/speckit.implement`)
   - Execute tasks in dependency order
   - Follow TDD as defined in task plan
   - Provide progress updates
   - Handle errors with context

**Time Comparison (from spec-driven.md):**

Traditional Approach:
- PRD (2-3 hours)
- Design docs (2-3 hours)
- Project structure (30 min)
- Technical specs (3-4 hours)
- Test plans (2 hours)
- **Total: ~12 hours**

SDD with Commands:
- `/speckit.specify` (5 min)
- `/speckit.plan` (5 min)
- `/speckit.tasks` (5 min)
- **Total: ~15 minutes** for complete specification artifacts

### 2.2 Brownfield Projects: Introducing SDD to Existing Codebases

**Challenges identified by Martin Fowler:**
> "For two of the three tools I tried it also seems to be even more work to introduce them into an existing codebase, therefore making it even harder to evaluate their usefulness for brownfield codebases."

**Recommended strategies:**

1. **Incremental Adoption**
   - Start with new features only
   - Don't retrofit existing code initially
   - Build spec coverage gradually

2. **Reverse Engineering Approach** (Tessl Framework)
   ```bash
   tessl document --code existing-file.js
   ```
   - Generates specs from existing code
   - Creates baseline for future maintenance
   - Enables spec-anchored workflow going forward

3. **Hybrid Workflow**
   - Maintain existing code as-is
   - New features use SDD
   - Refactorings can create specs retroactively

**Community Extensions for Brownfield:**
- **Brownfield Bootstrap** (`spec-kit-brownfield`)
  - Auto-discover architecture
  - Adopt SDD incrementally
  - Bootstrap existing codebases

### 2.3 Modern Legacy: Applying SDD to Legacy Modernization

**Use Cases:**

1. **Feature Parity Documentation**
   - Document existing system behavior as specs
   - Use specs to drive modernized implementation
   - Maintain behavioral equivalence

2. **Incremental Migration**
   - Spec-first for replacement components
   - Parallel implementation from same spec
   - Gradual cutover with spec as contract

3. **Technology Stack Pivots**
   > "SDD can support what-if/simulation experiments: 'If we need to re-implement or change the application to promote a business need to sell more T-shirts, how would we implement and experiment for that?'"
   > — spec-driven.md

**Key principle:**
> "When specifications drive implementation, pivots become systematic regenerations rather than manual rewrites. Change a core requirement in the PRD, and affected implementation plans update automatically."

---

## 3. Tool Ecosystem

### 3.1 spec-kit Core Capabilities

**Distribution:**
- CLI tool (`specify`)
- Creates workspace structures for 30+ AI coding agents
- Supports both slash commands and agent skills

**Core Commands:**

| Command | Purpose | Generates |
|---------|---------|-----------|
| `/speckit.constitution` | Project governing principles | `memory/constitution.md` |
| `/speckit.specify` | Feature requirements | `specs/NNN-name/spec.md` |
| `/speckit.clarify` | Structured clarification | Clarifications section |
| `/speckit.plan` | Technical implementation plan | `plan.md`, `data-model.md`, `contracts/` |
| `/speckit.tasks` | Executable task list | `tasks.md` |
| `/speckit.implement` | Execute all tasks | Source code, tests |

**Optional Quality Commands:**
- `/speckit.analyze`: Cross-artifact consistency analysis
- `/speckit.checklist`: Quality validation checklists

**Installation:**
```bash
# Persistent installation (recommended)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z

# Initialize project
specify init <PROJECT_NAME> --ai copilot
```

### 3.2 Integration with AI/LLM Tools

**Supported Agents (30+):**
- GitHub Copilot
- Claude Code
- Cursor
- Gemini CLI
- Codex CLI
- Qwen CLI
- And many more...

**Integration Patterns:**

1. **Slash Commands** (default)
   - Prompts in `.github/prompts/` or `.claude/commands/`
   - Natural language interface
   - Example: `/speckit.specify Build a chat feature...`

2. **Agent Skills Mode** (`--ai-skills`)
   - Native agent skill integration
   - Deeper integration with agent capabilities
   - Required for some agents (Codex CLI)

3. **Template-Based Customization**
   - Templates in `.specify/templates/`
   - Override via presets or extensions
   - Priority: Overrides → Presets → Extensions → Core

### 3.3 CI/CD Integration Patterns

**Community Extensions for CI/CD:**

1. **CI Guard** (`spec-kit-ci-guard`)
   - Verify specs exist before merge
   - Check for spec-code drift
   - Block merges on compliance gaps

2. **Plan Review Gate** (`spec-kit-plan-review-gate`)
   - Require spec.md and plan.md merged via PR
   - Before allowing task generation
   - Human review gate

3. **Ship Release Extension** (`spec-kit-ship`)
   - Pre-flight checks
   - Branch sync
   - Changelog generation
   - CI verification
   - Automated PR creation

**Integration Approach:**
```yaml
# Example GitHub Actions workflow
- name: Spec Kit Validation
  run: |
    specify check
    # Custom validation from extensions
```

### 3.4 IDE/Editor Support

**File Structure Created:**
```
.specify/
├── memory/
│   └── constitution.md
├── scripts/
│   ├── create-new-feature.sh
│   ├── setup-plan.sh
│   └── common.sh
├── specs/
│   └── 001-feature-name/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── data-model.md
│       └── contracts/
│           └── api-spec.json
└── templates/
    ├── spec-template.md
    ├── plan-template.md
    └── tasks-template.md
```

**Editor Integration:**
- Markdown-based (universal support)
- YAML for configuration
- Shell scripts for automation
- JSON for contracts/schemas

---

## 4. Transition Strategies

### 4.1 Spec-First Adoption

**When to Use:**
- Exploratory prototypes
- Spike solutions
- Time-boxed experiments
- Learning SDD workflow

**Process:**
1. Write comprehensive spec for task
2. Use AI to generate implementation
3. Validate and iterate
4. **Delete spec after completion** (not anchored)
5. Next task creates new spec

**Advantages:**
- Lowest commitment
- Easy to try
- No long-term maintenance

**Disadvantages:**
- Specs not reusable
- Knowledge loss after completion
- No living documentation

### 4.2 Spec-Anchored Migration

**When to Use:**
- Production features
- Long-term maintenance needed
- Team collaboration required
- Documentation compliance

**Process:**
1. Create spec for feature
2. Generate and implement
3. **Keep spec alongside code**
4. Update spec when feature evolves
5. Regenerate or manually update code
6. Maintain spec-code synchronization

**Tools for Spec-Anchored:**
- **Spec Sync** (`spec-kit-sync`): Detect and resolve drift
- **Reconcile Extension** (`spec-kit-reconcile`): Surgically update specs
- **Retrospective Extension** (`spec-kit-retrospective`): Post-implementation review

**Challenges:**
> "Reviewing markdown over reviewing code? As just mentioned... spec-kit created a LOT of markdown files for me to review. They were repetitive, both with each other, and with the code that already existed. Some contained code already. Overall they were just very verbose and tedious to review."
> — Martin Fowler article

### 4.3 Spec-as-Source Full Adoption

**When to Use:**
- High non-determinism tolerance
- Frequent technology pivots needed
- Multiple implementation targets
- Strong spec review culture

**Process:**
1. Create and maintain ONLY specs
2. Code is 100% generated
3. Never manually edit generated code
4. All changes through spec updates
5. Regenerate code on every change

**Example from Tessl Framework:**
```javascript
// GENERATED FROM SPEC - DO NOT EDIT
// Source: dynamic-data-renderer.spec.md
```

**Current Status:**
> "Tessl is the only one of these three tools that explicitly aspires to a spec-anchored approach, and is even exploring the spec-as-source level of SDD."
> — Martin Fowler article

**Parallel to MDD:**
> "I worked on a few projects at the beginning of my career that heavily used MDD... Ultimately, MDD never took off for business applications, it sits at an awkward abstraction level and just creates too much overhead and constraints. But LLMs take some of the overhead and constraints of MDD away... I wonder if spec-as-source, and even spec-anchoring, might end up with the downsides of both MDD and LLMs: Inflexibility AND non-determinism."
> — Martin Fowler article

---

## 5. Project Structure & Organization

### 5.1 Recommended Folder Hierarchies

**spec-kit Standard Structure:**
```
project-root/
├── .specify/
│   ├── memory/              # Memory Bank (context files)
│   │   ├── constitution.md  # Project principles
│   │   └── AGENTS.md        # Agent-specific guidance
│   ├── specs/               # Feature Specifications
│   │   ├── 001-feature-a/
│   │   │   ├── spec.md
│   │   │   ├── plan.md
│   │   │   ├── tasks.md
│   │   │   ├── research.md
│   │   │   ├── data-model.md
│   │   │   ├── quickstart.md
│   │   │   └── contracts/
│   │   │       ├── api-spec.json
│   │   │       └── events.md
│   │   └── 002-feature-b/
│   │       └── ...
│   ├── templates/           # Core templates
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   └── tasks-template.md
│   ├── templates/overrides/ # Project-local customizations
│   ├── presets/             # Installed presets
│   ├── extensions/          # Installed extensions
│   └── scripts/             # Automation scripts
│       ├── create-new-feature.sh
│       └── setup-plan.sh
├── .github/ or .claude/     # AI agent commands
│   ├── prompts/ or commands/
│   │   ├── speckit.constitution.md
│   │   ├── speckit.specify.md
│   │   ├── speckit.plan.md
│   │   ├── speckit.tasks.md
│   │   └── speckit.implement.md
└── src/                     # Source code
```

**Kiro Structure:**
```
steering/                    # Memory Bank equivalent
├── product.md
├── tech.md
└── structure.md
feature-name/               # Per-feature directory
├── requirements.md         # User stories with acceptance criteria
├── design.md              # Component architecture, data models
└── tasks.md               # Task list with UI elements
```

**Tessl Framework Structure:**
```
.tessl/
└── framework/
    ├── config files
    └── templates
specs/                      # One spec per code file
└── component-name.spec.md
KNOWLEDGE.md               # Project knowledge
AGENTS.md                  # Agent guidance
src/
└── component-name.js      # Generated from spec
```

### 5.2 Spec File Organization Patterns

**Template-Driven Quality (from spec-driven.md):**

Templates act as sophisticated prompts constraining LLM behavior:

1. **Preventing Premature Implementation**
   ```markdown
   - ✅ Focus on WHAT users need and WHY
   - ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
   ```

2. **Forcing Explicit Uncertainty**
   ```markdown
   When creating this spec:
   1. Mark all ambiguities: Use [NEEDS CLARIFICATION: specific question]
   2. Don't guess: If the prompt doesn't specify something, mark it
   ```

3. **Structured Self-Review**
   ```markdown
   ### Requirement Completeness
   - [ ] No [NEEDS CLARIFICATION] markers remain
   - [ ] Requirements are testable and unambiguous
   - [ ] Success criteria are measurable
   ```

4. **Constitutional Compliance Gates**
   ```markdown
   ### Phase -1: Pre-Implementation Gates

   #### Simplicity Gate (Article VII)
   - [ ] Using ≤3 projects?
   - [ ] No future-proofing?

   #### Anti-Abstraction Gate (Article VIII)
   - [ ] Using framework directly?
   - [ ] Single model representation?
   ```

### 5.3 Documentation Structure

**Hierarchy of Documentation:**

1. **Constitution** (`.specify/memory/constitution.md`)
   - Immutable principles
   - Architectural standards
   - Quality requirements
   - **Scope**: All features, all time

2. **Memory Bank** (`.specify/memory/`)
   - Product vision
   - Architecture patterns
   - Technology standards
   - **Scope**: All features, stable over time

3. **Feature Specs** (`.specify/specs/NNN-name/`)
   - Specific requirements
   - User stories
   - Acceptance criteria
   - **Scope**: Single feature

4. **Implementation Plans** (`plan.md`, `data-model.md`)
   - Technical decisions
   - Component design
   - Integration points
   - **Scope**: Single feature implementation

5. **Task Lists** (`tasks.md`)
   - Executable steps
   - Dependency ordering
   - File paths
   - **Scope**: Implementation execution

### 5.4 Version Control Practices

**Branch Strategy (spec-kit default):**

1. **Automatic Branch Creation**
   - `/speckit.specify` creates branch `NNN-feature-name`
   - Spec number auto-incremented (001, 002, 003...)
   - Semantic naming from feature description

2. **Branch Lifecycle**
   ```
   main
   └── 001-feature-name
       ├── spec.md created
       ├── plan.md added
       ├── tasks.md added
       ├── implementation commits
       └── merge to main
   ```

3. **Spec Lifecycle Debate**
   > "spec-kit creates a branch for every spec that gets created, which seems to indicate that they see a spec as a living artifact for the lifetime of a change request, not the lifetime of a feature."
   > — Martin Fowler article

**Pull Request Integration:**

- **PR Bridge Extension** (`spec-kit-pr-bridge-`)
  - Auto-generate PR descriptions from specs
  - Include checklists from acceptance criteria
  - Summarize changes from artifacts

- **Manual PR Creation** (spec-kit recommendation)
  ```bash
  gh pr create --title "Feature: X" --body "$(cat specs/001-x/spec.md)"
  ```

**Commit Practices:**

- **Checkpoint Extension** (`spec-kit-checkpoint`)
  - Commit during implementation phases
  - Avoid single massive commit at end
  - Incremental history

- **Recommended Commit Message**
  ```
  feat(001): Implement user authentication

  - Implements spec.md user stories 1.1, 1.2
  - Completes tasks.md items 1-5
  - Follows constitutional Article III (TDD)
  ```

---

## 6. Constitutional Foundation: The Nine Articles

### 6.1 Article I: Library-First Principle

**Text:**
> "Every feature in Specify MUST begin its existence as a standalone library. No feature shall be implemented directly within application code without first being abstracted into a reusable library component."
> — constitution.md (from spec-driven.md)

**Impact:**
- Forces modular design from day one
- Ensures reusability
- Clear boundaries and contracts
- Prevents monolithic coupling

### 6.2 Article II: CLI Interface Mandate

**Requirements:**
```markdown
All CLI interfaces MUST:
- Accept text as input (via stdin, arguments, or files)
- Produce text as output (via stdout)
- Support JSON format for structured data exchange
```

**Impact:**
- Enforces observability
- Enables automation and testing
- No hidden functionality
- Text-based verification

### 6.3 Article III: Test-First Imperative

**Critical Requirement:**
> "This is NON-NEGOTIABLE: All implementation MUST follow strict Test-Driven Development. No implementation code shall be written before:
> 1. Unit tests are written
> 2. Tests are validated and approved by the user
> 3. Tests are confirmed to FAIL (Red phase)"
> — constitution.md

**Workflow Impact:**
- Completely inverts traditional AI code generation
- Tests define behavior first
- Human approval before implementation
- Verified Red → Green → Refactor cycle

### 6.4 Articles VII & VIII: Simplicity and Anti-Abstraction

**Article VII - Simplicity:**
```markdown
Section 7.3: Minimal Project Structure
- Maximum 3 projects for initial implementation
- Additional projects require documented justification
```

**Article VIII - Anti-Abstraction:**
```markdown
Section 8.1: Framework Trust
- Use framework features directly rather than wrapping them
```

**Enforcement via Gates:**
```markdown
### Phase -1: Pre-Implementation Gates

#### Simplicity Gate (Article VII)
- [ ] Using ≤3 projects?
- [ ] No future-proofing?

#### Anti-Abstraction Gate (Article VIII)
- [ ] Using framework directly?
- [ ] Single model representation?
```

**Impact:**
- Prevents over-engineering
- Forces justification for complexity
- Complexity tracked explicitly
- Simplicity as default

### 6.5 Article IX: Integration-First Testing

**Requirements:**
```markdown
Tests MUST use realistic environments:
- Prefer real databases over mocks
- Use actual service instances over stubs
- Contract tests mandatory before implementation
```

**Impact:**
- Ensures code works in practice
- Not just theoretical correctness
- Real-world validation
- Contract-driven development

### 6.6 Constitutional Evolution

**Amendment Process:**
```markdown
Section 4.2: Amendment Process
Modifications to this constitution require:
- Explicit documentation of the rationale for change
- Review and approval by project maintainers
- Backwards compatibility assessment
```

**Key Principle:**
> "While principles are immutable, their application can evolve... The constitution shows its own evolution with dated amendments, demonstrating how principles can be refined based on real-world experience."
> — spec-driven.md

---

## 7. Extensions & Presets Ecosystem

### 7.1 Extension Categories

**By Category:**

| Category | Purpose | Effect | Examples |
|----------|---------|--------|----------|
| `docs` | Read, validate, generate spec artifacts | Read-only or Read+Write | Spec Reference Loader, Archive |
| `code` | Review, validate, modify source code | Read-only or Read+Write | Review, Verify, Security Review |
| `process` | Orchestrate workflow across phases | Read+Write | MAQA, Fleet, Conduct |
| `integration` | Sync with external platforms | Read+Write | Jira, Azure DevOps, GitHub Issues |
| `visibility` | Report on health or progress | Read-only | Status, Doctor, Diagram |

**Installation:**
```bash
# Search extensions
specify extension search

# Install extension
specify extension add spec-kit-jira

# List installed
specify extension list
```

### 7.2 Notable Extensions

**Workflow Extensions:**

1. **MAQA (Multi-Agent & Quality Assurance)**
   - Coordinator → Feature → QA agent workflow
   - Parallel worktree-based implementation
   - Language-agnostic
   - Optional CI gate

2. **Fleet Orchestrator**
   - Full feature lifecycle
   - Human-in-the-loop gates
   - Across all SpecKit phases

3. **Canon**
   - Baseline-driven workflows
   - Spec-first, code-first, spec-drift modes
   - Requires Canon Core preset

**Quality Extensions:**

1. **Verify Extension**
   - Post-implementation validation
   - Code against spec artifacts
   - Read-only quality gate

2. **Review Extension**
   - Comprehensive code review
   - Specialized agents for: quality, comments, tests, error handling, types, simplification

3. **Security Review**
   - AI-powered DevSecOps analysis
   - Comprehensive security audit

**Integration Extensions:**

1. **Jira Integration**
   - Create Epics, Stories, Issues from specs
   - Configurable hierarchy
   - Custom field support

2. **GitHub Issues Integration**
   - Generate specs from Issues
   - Bidirectional traceability
   - Sync updates

3. **Confluence Extension**
   - Create Confluence docs
   - Summarize specs and planning files

**Developer Experience:**

1. **Blueprint**
   - Review complete code blueprint
   - Before `/speckit.implement` runs
   - Stay code-literate in AI development

2. **TinySpec**
   - Lightweight single-file workflow
   - For small tasks
   - Skip heavy multi-step process

### 7.3 Preset System

**Purpose:**
> "Use presets when you want to change HOW Spec Kit works without adding new capabilities. Presets override the templates and commands that ship with the core AND with installed extensions."

**vs. Extensions:**

| Goal | Use |
|------|-----|
| Add brand-new command or workflow | Extension |
| Customize format of specs, plans, tasks | Preset |
| Integrate external tool/service | Extension |
| Enforce organizational/regulatory standards | Preset |
| Ship reusable domain templates | Either |

**Priority Resolution:**
```
Priority 1 (Highest): Project-Local Overrides (.specify/templates/overrides/)
Priority 2:            Presets (.specify/presets/templates/)
Priority 3:            Extensions (.specify/extensions/templates/)
Priority 4 (Lowest):   Spec Kit Core (.specify/templates/)
```

**Installation:**
```bash
# Search presets
specify preset search

# Install preset
specify preset add <preset-name>

# Multiple presets can be stacked
```

**Example Use Cases:**
- Localize workflow to different language
- Adapt to methodology (Agile, Kanban, Waterfall, DDD)
- Enforce compliance/regulatory requirements
- Add mandatory security review gates
- Customize terminology for domain

### 7.4 Creating Custom Extensions

**Extension Structure:**
```
my-extension/
├── extension.json       # Metadata
├── commands/           # New slash commands
├── templates/          # Template overrides
├── scripts/            # Automation scripts
└── README.md
```

**Publishing:**
1. Create extension following structure
2. Publish to GitHub
3. Submit to community catalog
4. Others can install via:
   ```bash
   specify extension add my-extension
   ```

---

## 8. Critical Observations & Open Questions

### 8.1 One Workflow to Fit All Sizes?

**Problem:**
> "Kiro and spec-kit provide one opinionated workflow each, but I'm quite sure that neither of them is suitable for the majority of real life coding problems. In particular, it's not quite clear to me how they would cater to enough different problem sizes to be generally applicable."
> — Martin Fowler

**Example - Small Bug:**
When fixing a small bug with Kiro, it generated:
- 4 "user stories"
- 16 acceptance criteria total
- Including gems like: "As a developer, I want the transformation function to handle edge cases gracefully..."

**Question for the Field:**
- What problem sizes is SDD optimized for?
- How to scale workflow complexity with problem size?
- Need for multiple workflow variants?

### 8.2 Reviewing Markdown Over Reviewing Code?

**Challenge:**
> "To be honest, I'd rather review code than all these markdown files. An effective SDD tool would have to provide a very good spec review experience."
> — Martin Fowler

**Issues Observed:**
- LOT of markdown files created
- Repetitive content (with each other and existing code)
- Some contained code snippets
- Very verbose and tedious to review

**Implication:**
The promise of "reviewing intent, not implementation" may not hold if spec review is equally or more burdensome than code review.

### 8.3 False Sense of Control?

**Observation:**
> "Even with all of these files and templates and prompts and workflows and checklists, I frequently saw the agent ultimately not follow all the instructions. Yes, the context windows are now larger... But just because the windows are larger, doesn't mean that AI will properly pick up on everything that's in there."
> — Martin Fowler

**Examples:**
- Research notes described existing classes
- Agent regenerated them as duplicates (ignored "existing")
- Agent went overboard on constitution articles
- Ignored some instructions, over-applied others

**Question:**
Are we creating **Verschlimmbesserung** ("making something worse in the attempt of making it better")?

### 8.4 Spec-Anchored: Learning from MDD?

**Historical Parallel:**
> "The models in MDD were basically the specs, albeit not in natural language, but expressed in e.g. custom UML or a textual DSL. We built custom code generators to turn those specs into code... Ultimately, MDD never took off for business applications."
> — Martin Fowler

**Trade-offs:**

| Aspect | MDD | SDD |
|--------|-----|-----|
| Spec Language | Parseable, constrained DSL | Natural language, flexible |
| Code Generator | Custom built, deterministic | LLM, non-deterministic |
| Tool Support | IDE support, validation | Limited tooling |
| Abstraction Level | Awkward (too low or too high) | Natural (human intent) |

**Risk:**
> "I wonder if spec-as-source, and even spec-anchoring, might end up with the downsides of both MDD and LLMs: Inflexibility AND non-determinism."

### 8.5 Who Is the Target User?

**Observed Confusion:**
- Demos include product goal definition
- Use terms like "user story"
- Incorporate requirements analysis
- Presented as developer workflow

**Questions:**
- Is SDD for developers doing more product work?
- Cross-skilling enabler via AI?
- Developer-product pairing workflow?
- What problem size requires product specialist?

**Matrix:**
```
         │ Small Problem │ Large Problem
─────────┼────────────────┼───────────────
Clear    │      ?         │      ?
Problem  │                │
─────────┼────────────────┼───────────────
Unclear  │      ?         │      ?
Problem  │                │
```
Where does SDD sit?

### 8.6 Real-World Evaluation Challenges

**Time Investment:**
> "It turns out to be quite time-consuming to evaluate SDD tools and approaches in a way that gets close to real usage. You would have to try them out with different sizes of problems, greenfield, brownfield, and really take the time to review and revise the intermediate artifacts with more than just a cursory glance."
> — Martin Fowler

**Needed for Proper Evaluation:**
1. Different problem sizes (small bug → full feature)
2. Different problem types (greenfield, brownfield, legacy)
3. Real code review time (not just cursory glance)
4. Long-term maintenance cycles (weeks/months)
5. Team collaboration dynamics
6. Production incident response

**Current State:**
Most evaluations are:
- Tutorial-based (greenfield, small apps)
- Short-term (single feature)
- Individual developer (not team)
- Happy path (no production chaos)

---

## 9. Recommendations for Adoption

### 9.1 Start Small: Spec-First Exploration

**Recommended First Steps:**

1. **Pick a Greenfield Spike**
   - New feature, exploratory
   - Low production risk
   - Time-boxed (1-2 days)

2. **Use Minimal Tooling**
   - Install spec-kit
   - Use core commands only (no extensions yet)
   - Follow basic workflow

3. **Measure and Compare**
   - Time to spec vs. traditional approach
   - Quality of generated code
   - Review burden (spec vs. code)
   - AI misinterpretations

4. **Learn the Patterns**
   - How to write good specs
   - When to clarify vs. over-specify
   - Constitutional principles that matter

### 9.2 Gradual Migration: Spec-Anchored for Critical Paths

**Once Comfortable:**

1. **Identify Candidates**
   - Features with frequent changes
   - Complex business logic
   - Multiple stakeholder alignment needed
   - Documentation compliance requirements

2. **Maintain Specs**
   - Keep specs updated alongside code
   - Review spec changes in PRs
   - Use drift detection tools

3. **Build Team Practices**
   - Spec review checklist
   - Shared constitutional principles
   - Clarification workflow standards

### 9.3 Selective Spec-as-Source: High-Value Components

**Advanced Adoption:**

1. **Choose Carefully**
   - Components with low creative variance
   - Well-understood patterns
   - Frequent technology pivots
   - High testing requirements

2. **Accept Non-Determinism**
   - Code may vary between generations
   - Specs must be precise
   - Test coverage essential
   - CI/CD validation critical

3. **Monitor Closely**
   - Spec review discipline
   - Generated code quality trends
   - Developer satisfaction
   - Time savings vs. overhead

### 9.4 Avoid Pitfalls

**Don't:**

1. **Over-specify** - Leave room for AI creativity within bounds
2. **Under-clarify** - Use `[NEEDS CLARIFICATION]` liberally
3. **Ignore Constitution** - Principles prevent common mistakes
4. **Skip Reviews** - Both spec AND generated code need review
5. **Retrofit Everything** - Start with new features, not existing code
6. **Assume Tool Maturity** - These are experimental, expect rough edges

**Do:**

1. **Iterate Specs** - Use clarification workflow
2. **Track Complexity** - Document justified complexity
3. **Measure Impact** - Time, quality, satisfaction metrics
4. **Share Learnings** - Team retrospectives on SDD experience
5. **Contribute Back** - Extensions, presets, community feedback

---

## 10. The Future of SDD

### 10.1 Enablers

**Three Trends Making SDD Possible:**

1. **AI Capability Threshold**
   > "AI capabilities have reached a threshold where natural language specifications can reliably generate working code."
   > — spec-driven.md

2. **Growing Software Complexity**
   > "Modern systems integrate dozens of services, frameworks, and dependencies. Keeping all these pieces aligned with original intent through manual processes becomes increasingly difficult."

3. **Accelerating Pace of Change**
   > "Requirements change far more rapidly today than ever before. Pivoting is no longer exceptional—it's expected."

### 10.2 Open Research Questions

From the analysis:

1. **Semantic Diffusion**
   > "The term 'spec-driven development' isn't very well defined yet, and it's already semantically diffused. I've even recently heard people use 'spec' basically as a synonym for 'detailed prompt'."
   > — Martin Fowler

2. **Workflow Optimization**
   - Right workflow for each problem size?
   - Balancing structure with flexibility?
   - Tool support for spec review?

3. **Team Dynamics**
   - Cross-functional collaboration models?
   - Spec authorship and ownership?
   - Review and approval workflows?

4. **Long-Term Viability**
   - Will specs stay synchronized?
   - Maintenance burden over time?
   - Evolution of tools and practices?

### 10.3 Where We're Headed (GitHub's Vision)

> "That's why we're rethinking specifications — not as static documents, but as living, executable artifacts that evolve with the project. Specs become the shared source of truth. When something doesn't make sense, you go back to the spec; when a project grows complex, you refine it; when tasks feel too large, you break them down."
> — GitHub blog (spec-driven.md)

**Key Aspirations:**

1. **Specifications as Primary Artifact**
   - Code is subordinate to specs
   - Specs drive all development
   - Intent captured in natural language

2. **Continuous Evolution**
   - Specs evolve with product
   - Code regenerated as needed
   - Tight feedback loops

3. **Technology Independence**
   - Same spec, multiple implementations
   - Easy technology stack pivots
   - Framework-agnostic specifications

4. **AI-Native Development**
   - Designed for AI from ground up
   - Not retrofitted to AI capabilities
   - Workflows optimized for LLM strengths

---

## 11. Key Takeaways

### For Individual Developers

1. **SDD is a paradigm shift**, not just a tool
2. **Start with spec-first** for exploration
3. **Templates are critical** - they constrain LLM behavior productively
4. **Constitutional principles** prevent common pitfalls
5. **Review burden shifts** from code to specs (may not be lighter)

### For Teams

1. **Shared constitutional principles** essential for consistency
2. **Spec review culture** as important as code review
3. **Clarification workflow** prevents over-specification
4. **Extension ecosystem** allows customization
5. **Brownfield adoption is harder** than greenfield

### For Organizations

1. **Experimental stage** - tools and practices still evolving
2. **Selective adoption** recommended (not all-in immediately)
3. **Measure impact** - time, quality, developer satisfaction
4. **Invest in training** - writing good specs is a skill
5. **Community-driven** - contribute learnings back

### Critical Success Factors

1. **Precision without over-specification** - art of good spec writing
2. **Constitutional discipline** - principles enforced consistently
3. **Tool support** - spec review, drift detection, validation
4. **Team alignment** - shared understanding of SDD goals
5. **Realistic expectations** - acknowledge limitations and trade-offs

---

## 12. Sources

### Primary Sources

1. **GitHub spec-kit Repository**
   - URL: https://github.com/github/spec-kit
   - Files: README.md, spec-driven.md
   - Focus: Core methodology, tool usage, constitutional foundation

2. **Martin Fowler Article**
   - Title: "Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl"
   - URL: https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
   - Focus: Critical analysis, tool comparison, open questions

3. **GitHub Blog Post**
   - Title: "Spec-driven development with AI: Get started with a new open source toolkit"
   - URL: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
   - Focus: Enterprise use cases, adoption patterns

### Community Resources

- spec-kit Community Extensions Catalog (275+ extensions)
- Community Presets for workflow customization
- Video walkthroughs and tutorials

---

## Appendix A: Quick Reference

### Essential Commands

```bash
# Installation
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z

# Project Setup
specify init <project> --ai copilot
cd <project>

# Core Workflow
/speckit.constitution  # Create project principles
/speckit.specify      # Define feature requirements
/speckit.clarify      # Clarify underspecified areas
/speckit.plan         # Create implementation plan
/speckit.tasks        # Generate task breakdown
/speckit.implement    # Execute implementation

# Extension Management
specify extension search
specify extension add <name>
specify extension list

# Preset Management
specify preset search
specify preset add <name>
```

### Constitutional Checklist

```markdown
- [ ] Article I: Feature begins as library
- [ ] Article II: CLI interface exposed
- [ ] Article III: Tests written first
- [ ] Article VII: ≤3 projects initially
- [ ] Article VIII: Using framework directly
- [ ] Article IX: Real integration tests
```

### Spec Quality Checklist

```markdown
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable
- [ ] Success criteria measurable
- [ ] Focuses on WHAT and WHY, not HOW
- [ ] User stories with acceptance criteria
- [ ] Non-functional requirements included
- [ ] Error handling scenarios defined
```

---

*This research report compiled from multiple authoritative sources on Spec-Driven Development as of April 2026. The field is rapidly evolving; consult primary sources for latest developments.*
