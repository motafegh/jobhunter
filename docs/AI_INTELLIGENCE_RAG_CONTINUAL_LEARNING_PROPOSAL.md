# JobHunter AI Intelligence, RAG, Agents, and Continual-Learning Proposal

**Status:** Proposed — discussion/design artifact only  
**Date:** 2026-08-02  
**Authority:** Non-controlling until explicitly approved and incorporated into the master implementation plan  
**Scope:** Future AI/inference, retrieval, agentic intelligence, evaluation, and continual-improvement capabilities for JobHunter

---

## 1. Purpose

JobHunter is growing from a bounded Jobinja acquisition/parser/translation application into a
long-lived personal career-intelligence system. As the corpus grows from tens to hundreds and
later thousands of job observations, the value of the system should come increasingly from what
it can **reliably learn from, retrieve from, compare across, and reason over that evidence**.

This proposal defines a possible next-generation AI architecture for JobHunter. It combines:

- local and remote inference providers;
- task-specific model routing and fallbacks;
- specialist AI agents/workers;
- a JobHunter-owned Retrieval-Augmented Generation (RAG) system;
- incremental indexing as the corpus grows;
- human-review and verifier loops;
- model/prompt/retrieval evaluation;
- an explicit continual-learning/data-flywheel system;
- AI Lab and benchmark infrastructure;
- privacy, cost, provenance, and safety controls;
- future personal capability, gap, learning, and career-decision intelligence.

The proposal is intentionally ambitious at the **capability level** while remaining conservative
at the **authority level**. More AI should not mean weaker evidence discipline or opaque
autonomy.

---

## 2. Relationship to the current product

The accepted JobHunter authority hierarchy remains:

```text
original employer/source evidence        authoritative
        ↓
deterministic parsing                     source-derived
        ↓
English projection                        derived convenience
        ↓
semantic analysis                         model-derived interpretation
        ↓
canonical market intelligence             reviewed/derived aggregation
        ↓
personal capability intelligence          evidence-backed personal layer
        ↓
career/action recommendations              explainable derived decisions
```

The proposed AI/RAG system must extend this hierarchy, not replace it.

A RAG answer, agent decision, verifier result, summary, recommendation, embedding, cluster,
or learned routing preference must never silently become more authoritative than the evidence
from which it was derived.

---

## 3. Core design position

The desired end state is not:

```text
JobHunter + one LLM
```

It is closer to:

```text
                         JobHunter
                            │
             authoritative evidence + state
                            │
             ┌──────────────┴──────────────┐
             │                             │
      deterministic systems          AI intelligence fabric
             │                             │
             │                  provider/model/task router
             │                             │
             │             ┌───────────────┼───────────────┐
             │             │               │               │
             │          local LLM        NVIDIA         OpenCode
             │             │               │               │
             │             └───────────────┼───────────────┘
             │                             │
             │                 specialist AI workers
             │                             │
             └─────────────── validation / provenance
                                           │
                                accepted derived artifacts
                                           │
                     ┌─────────────────────┴─────────────────────┐
                     │                                           │
               RAG / retrieval                           market + personal
               knowledge layer                             intelligence
                     │                                           │
                     └─────────────────────┬─────────────────────┘
                                           │
                                   explainable actions
```

The application should become increasingly intelligent without becoming increasingly opaque.

---

## 4. Permanent principles proposed for this capability family

1. **Evidence first.** Model output is never source truth.
2. **Provider independence.** No core intelligence capability should depend permanently on one
   vendor or one model family.
3. **Task-specific models.** Translation, extraction, verification, synthesis, retrieval, and
   planning may use different models.
4. **Local-first where practical.** Remote inference is optional and policy-controlled.
5. **Privacy-aware routing.** Public job text and personal evidence have different routing rules.
6. **Version everything important.** Provider, model, prompt, schema, embedding model, chunking
   strategy, retrieval strategy, reranker, and evaluator versions must be reproducible.
7. **Persist provenance.** Every accepted AI artifact must be traceable to its exact inputs and
   inference contract.
8. **Deterministic calculations stay deterministic.** Models interpret calculated facts; they do
   not become the source of counts, percentages, lifecycle state, or database identity.
9. **Retrieval before hallucination.** Answers about the corpus should retrieve supporting
   evidence instead of relying on generic model memory.
10. **Human review at authority transitions.** Search-catalog changes, canonical taxonomy changes,
    personal capability claims, and consequential recommendations require explicit review until
    evidence proves a safer automation level.
11. **Uncertainty is a first-class state.** Disagreement, insufficient evidence, and low retrieval
    confidence must be representable.
12. **Continual learning is initially data/evaluation learning, not self-training.** JobHunter must
    not train on its own unverified generations.
13. **Bound all expensive work.** Network, tokens, cost, concurrency, retries, corpus reprocessing,
    and agent loops need explicit ceilings.
14. **No autonomous application submission.** Intelligence may prepare and explain; it does not
    silently apply for jobs.
15. **Agents have narrow tools.** No semantic-analysis agent receives unrestricted shell,
    filesystem, browser, or arbitrary network access.

---

# Part I — Multi-provider inference fabric

## 5. Generic inference-provider architecture

JobHunter should evolve from an LM-Studio-specific inference composition into a provider registry
with reusable protocol adapters.

The preferred abstraction is:

```text
InferenceProvider
    │
    ├── OpenAICompatibleProvider
    │      ├── LM Studio
    │      ├── NVIDIA hosted NIM / Build API
    │      ├── OpenCode Zen compatible models
    │      ├── local self-hosted NIMs
    │      ├── OpenRouter or other compatible gateways later
    │      └── user-configured compatible endpoints
    │
    └── ProviderSpecificAdapter
           ├── Anthropic-style endpoint if needed
           ├── Google-style endpoint if needed
           └── future APIs whose semantics genuinely differ
```

Do not create a separate implementation merely because the provider has a different brand when
it exposes the same protocol semantics.

### Current external examples

As of 2026-08-02:

- NVIDIA documents `https://integrate.api.nvidia.com/v1/chat/completions` as an OpenAI-compatible
  hosted NIM inference endpoint.
- OpenCode Zen exposes several protocol families; many models use
  `https://opencode.ai/zen/v1/chat/completions` through an OpenAI-compatible interface, while
  other models may use Responses-, Anthropic-, or Google-style endpoints.
- OpenCode Zen currently lists multiple explicitly free model IDs as well as paid models. Model
  availability/pricing must therefore be discovered/configured rather than hard-coded as a
  permanent assumption.

Provider URLs and model catalogs are operational configuration, not durable product truth.

---

## 6. Provider registry

Each provider definition should eventually describe:

```text
provider_id
provider_type
base_url
credential reference
local / external
privacy classes allowed
health state
model discovery capability
structured-output support
tool-calling support
streaming support
rate-limit policy
cost policy
operator enabled/disabled
```

Credentials should be referenced through environment variables or a future safe secret store;
they should never be written into source evidence, model artifacts, operation logs, Git, or normal
SQLite analytical records.

Example conceptual configuration:

```toml
[inference.providers.local]
type = "openai-compatible"
base_url = "http://127.0.0.1:12345/v1"
privacy = "local"

[inference.providers.nvidia]
type = "openai-compatible"
base_url = "https://integrate.api.nvidia.com/v1"
api_key_env = "NVIDIA_API_KEY"
privacy = "external-public-data"

[inference.providers.opencode]
type = "openai-compatible"
base_url = "https://opencode.ai/zen/v1"
api_key_env = "OPENCODE_API_KEY"
privacy = "external-public-data"
```

This syntax is illustrative, not yet approved configuration schema.

---

## 7. Model capability registry

A model should not be treated as merely a string ID. JobHunter should be able to record/discover
capabilities relevant to tasks, for example:

```text
provider
model ID
local/remote
input modalities
multilingual capability
structured JSON/schema capability
tool calling
reasoning mode
context window if known
maximum output if known
embedding model vs generative model
reranker capability
free / paid / unknown cost class
observed JobHunter benchmark scores
operator notes
```

Capabilities obtained from provider metadata are operational hints, not permanent facts. Runtime
smoke tests and JobHunter-specific evaluations remain authoritative for whether a model is usable
for a particular task.

---

## 8. Task-specific routing

Different tasks should be independently configurable.

Potential task classes:

```text
translation
translation_verification
job_semantic_analysis
analysis_verification
relevance_triage
search_strategy
semantic_normalization
role_archetype_analysis
market_synthesis
trend_synthesis
job_comparison
RAG_answer_generation
RAG_query_planning
RAG_reranking
personal_capability_analysis
personal_gap_analysis
learning_planning
career_path_analysis
application_readiness
```

Conceptual configuration:

```toml
[inference.tasks.translation]
provider = "local"
model = "gemma-..."

[inference.tasks.job_semantic_analysis]
provider = "nvidia"
model = "..."

[inference.tasks.analysis_verification]
provider = "opencode"
model = "..."
```

Provider/model changes must create new derived-artifact identity where the task output is durable.

---

## 9. Fallback routing

Each task may define an ordered fallback policy:

```text
preferred model
    ↓ unavailable / retryable provider failure
fallback model 1
    ↓
fallback model 2
    ↓
explicit failure
```

Fallback must not hide provenance. The persisted artifact must contain the provider/model that
actually executed the task.

Examples of policy choices:

- translation may prefer local and optionally fall back to remote;
- public-job semantic analysis may use remote providers;
- future personal evidence may remain local-only by default;
- a 429 response may invoke provider cooldown rather than immediate repeated requests;
- challenge/auth/configuration failures are not ordinary fallbacks unless explicitly configured.

---

## 10. Privacy routing

Introduce data-sensitivity classes such as:

```text
public_source           public employer/job content
derived_public          translation/analysis of public job content
personal                private user capability/project/learning evidence
secret                  credentials or secret-bearing content
```

Example default provider policy:

```text
LM Studio/local     public_source, derived_public, personal
remote providers    public_source, derived_public
secrets             never sent to generative providers
```

The exact personal-data policy must be explicitly approved before Phase 3 remote inference.

---

## 11. Cost, quota, and usage ledger

Every inference attempt should eventually record operational telemetry where available:

```text
timestamp
task
provider
model
input artifact/reference
input tokens
output tokens
latency
retry count
outcome
provider request ID where safe/useful
reported or estimated monetary cost
rate-limit metadata if available
```

A UI could show:

```text
Today
Local LM Studio       83 calls      local
NVIDIA                17 calls      42k input / 8k output
OpenCode               5 calls      free/paid class as configured
```

Potential guardrails:

```text
remote_daily_request_limit
remote_daily_token_limit
remote_daily_cost_limit
per-task batch limit
provider cooldown after rate limiting
local concurrency
remote concurrency
```

No cost estimate should be presented as exact unless the provider supplies enough pricing/usage
information to make it exact.

---

# Part II — AI orchestration and specialist agents

## 12. Agent model

JobHunter should use **specialist bounded workers**, not an unrestricted autonomous agent swarm.

An agent is a versioned inference workflow with:

```text
agent type/version
allowed inputs
allowed retrieval/tools
provider/model route
prompt/schema contract
validation rules
budget
output artifact type
review requirements
```

Most agents should be stateless with respect to model memory. Durable knowledge belongs in
JobHunter records and RAG indexes, not hidden conversational state.

---

## 13. Job Intelligence Analyst

Evolution of P1.6.

Produces evidence-backed:

- role purpose;
- responsibilities;
- required qualifications;
- preferred qualifications;
- contextual/inferred concepts;
- technologies/tools;
- knowledge/practices/domains;
- seniority/experience signals;
- exact source evidence;
- confidence.

It does not decide personal fit.

---

## 14. Evidence Critic / Analysis Verifier

Independently checks an analyst artifact.

Possible verdicts per claim:

```text
supported
overstated
understated
evidence mismatch
classification questionable
unsupported
ambiguous
```

A stronger pipeline could be:

```text
analyst
   ↓
deterministic evidence validator
   ↓
independent verifier
   ↓
accepted / needs review / rejected
```

Different model families may be deliberately used for analyst and verifier to reduce correlated
failure modes.

Verification should be optional/bounded by quality mode rather than multiplying every model call
by default.

---

## 15. Translation Critic

Evaluates source-field/English-field pairs without replacing the source.

Potential labels:

```text
good
awkward_but_acceptable
meaning_changed
strength_changed
information_missing
information_invented
wrong_field_suspicion
needs_human_review
```

Use cases:

- golden-corpus evaluation;
- suspicious deterministic-integrity findings;
- testing a new translation provider/model;
- high-value jobs;
- sampling production translation quality.

---

## 16. Relevance Triage Agent

Provides a **derived relevance assessment**, separate from deterministic acquisition priority and
future personal fit.

Possible inputs before full detail fetch:

- title;
- company;
- search provenance;
- search-result snippet where available;
- selected market focus profile.

Output should be categorical/explainable, for example:

```text
likely_relevant
uncertain
likely_irrelevant
```

Do not create an unexplained percentage score.

---

## 17. Search Strategist

Analyzes actual acquisition evidence and proposes search-catalog improvements.

Inputs may include:

- search effectiveness;
- unique contributions;
- overlap;
- later triage outcomes;
- analyzed job concepts;
- emerging role titles;
- corpus gaps.

Outputs are proposals:

```text
add term
add bilingual variant
add/remove pack relation
demote noisy term
investigate missing role family
```

Catalog mutation remains human-approved.

---

## 18. Lifecycle Interpreter

Runs only when deterministic response/lifecycle classification is uncertain.

Potential tasks:

- distinguish valid job page from generic error page;
- interpret explicit expiry/closed language;
- detect authentication/challenge-like content when deterministic signals are inconclusive.

It must not override strong deterministic HTTP evidence silently.

---

## 19. Semantic Normalizer

Phase-2 worker that proposes canonical mappings such as:

```text
Postgres → PostgreSQL
K8s → Kubernetes
Large Language Models → LLM
```

Mappings are reviewable artifacts, not direct silent database rewrites.

---

## 20. Role Archetype Builder

Proposes role families from accepted semantic analysis, responsibilities, and requirements.

Potential outputs:

```text
AI Engineer
ML Engineer
LLM/Application Engineer
AI Security Engineer
Security Automation Engineer
Detection Engineer
MLOps/ML Platform Engineer
Platform/SRE-adjacent Engineer
```

Archetypes must be evidence-backed by the actual collected market, not generic occupational
knowledge alone.

---

## 21. Market Analyst

Receives deterministic aggregates and produces explanations.

Correct division of responsibility:

```text
SQL/Python calculation
    Python required in X/N jobs
    Docker preferred in Y/N jobs
    sample size N
        ↓
Market Analyst
    interpret concentration, combinations, and implications
```

The LLM does not invent or calculate the base statistics when deterministic calculation is
available.

---

## 22. Trend Analyst

Future temporal worker that interprets deterministic period-over-period changes:

```text
requirement prevalence
role-family volume
seniority mix
technology combinations
location/employment changes
search coverage changes
```

It should distinguish measured movement from speculative explanation.

---

## 23. Job Comparison Agent

Compares selected opportunities through accepted job analyses.

Before personal evidence exists:

- responsibilities;
- technical expectations;
- seniority;
- domains;
- learning exposure;
- role similarity/difference.

After Phase 3:

- demonstrated personal matches;
- critical gaps;
- evidence gaps;
- learning value;
- readiness considerations.

---

## 24. Personal Capability Analyst

Phase-3 agent only.

Operates on explicit personal evidence and can classify capability depth such as:

```text
introduced
practiced
working
independent
advanced
```

Final labels must be separately approved.

It must distinguish:

```text
no evidence
```

from:

```text
evidence of inability
```

and must never convert conversational memory or a single exposure into a durable proficiency
claim.

---

## 25. Gap Analyst

Compares reviewed market concepts against reviewed personal capability evidence.

Possible gap classes:

```text
no evidence
introduced but shallow
practical-depth gap
production-evidence gap
outdated evidence
adequate evidence
strong evidence
```

Every conclusion must trace to both market and personal evidence.

---

## 26. Learning Planner

Uses target role/archetype, market evidence, capability evidence, and gap structure to propose:

- next learning objective;
- reason for priority;
- minimum prerequisite theory;
- project/practice task;
- evidence to generate;
- completion/stop condition;
- what depth is intentionally deferred.

This should integrate naturally with the user's project-based learning model rather than becoming
a generic course recommender.

---

## 27. Career Path Simulator

Compares possible career trajectories using collected evidence.

Example output dimensions:

```text
market sample size
role availability
skill overlap
required depth
largest personal gaps
learning distance
transferability
uncertainty
```

Avoid pseudo-scientific precision where the evidence does not support it.

---

## 28. Application Readiness Agent

Phase-4 worker that may eventually prepare:

- requirement-by-requirement readiness analysis;
- evidence checklist;
- missing proof to build before applying;
- job-specific preparation topics;
- source-grounded resume-targeting suggestions.

It must not submit applications automatically.

---

## 29. Quality Auditor Agent

Cross-cutting worker that samples accepted derived artifacts and looks for systematic failures:

- translation drift;
- evidence overstatement;
- taxonomy inconsistency;
- stale analysis contracts;
- abnormal model-output distributions;
- suspicious retrieval answers;
- disagreement spikes after a model/provider change.

Its findings should create review tasks, not silently rewrite history.

---

# Part III — JobHunter-owned RAG system

## 30. Why RAG belongs in JobHunter

As the corpus grows, repeatedly inserting entire job descriptions/analyses into model context becomes
inefficient, expensive, and eventually impossible. More importantly, JobHunter needs to answer
questions across **many kinds of evidence**, not merely perform semantic extraction on one job.

Examples:

- "What responsibilities keep recurring in AI-security jobs?"
- "Show the strongest evidence that Linux is expected in these roles."
- "Which Tehran jobs mention Docker but not Kubernetes?"
- "What changed in security-automation expectations over the last three months?"
- "Which jobs most resemble this role and why?"
- "What evidence supports the claim that RAG experience is becoming more common?"
- later: "Which market requirements are not demonstrated by my current projects?"

A JobHunter RAG system should be designed for **citation-first career intelligence**, not generic
chat over documents.

---

## 31. RAG is not only a vector database

The proposed retrieval architecture is hybrid:

```text
User/agent question
        ↓
query classification / planning
        ↓
┌─────────────────────────────────────────────────────┐
│ structured SQL filters                             │
│ lexical/full-text retrieval                        │
│ vector semantic retrieval                          │
│ optional graph/entity retrieval later              │
│ temporal/version filters                           │
└─────────────────────────────────────────────────────┘
        ↓
merge + deduplicate
        ↓
rerank where useful
        ↓
evidence package with stable references
        ↓
answer/synthesis model
        ↓
citations + uncertainty + retrieval diagnostics
```

SQL remains the best retrieval mechanism for exact structured questions. Vector similarity should
not replace deterministic filtering.

---

## 32. RAG knowledge zones

Indexes should preserve authority classes rather than mixing everything into one anonymous vector
collection.

Potential zones:

### 32.1 Source evidence zone

- original employer title/company/location/etc.;
- original job descriptions;
- source skill tags;
- semantic source versions;
- lifecycle/source history.

**Authority:** highest.

### 32.2 English projection zone

- current validated English v2;
- field-level translation provenance.

**Authority:** derived comprehension layer.

### 32.3 Accepted semantic-analysis zone

- role purposes;
- responsibilities;
- requirements;
- evidence links;
- confidence/classification.

**Authority:** accepted model-derived interpretation.

### 32.4 Canonical market-intelligence zone

Future:

- concepts;
- aliases;
- responsibility families;
- role archetypes;
- aggregate facts.

### 32.5 Personal-evidence zone

Future private zone:

- projects;
- work evidence;
- learning/practice evidence;
- assessments;
- capability depth.

Remote retrieval/generation policy may differ from public-source zones.

### 32.6 Product knowledge zone

Potentially include selected JobHunter documentation/specifications for an in-app technical/admin
assistant. This must stay logically separate from career-market data.

---

## 33. Semantic chunking

Do not blindly chunk everything every N characters.

JobHunter already has meaningful semantic boundaries:

```text
job title
company
source field
job-description section
responsibility claim
requirement claim
company description
canonical concept
role archetype
personal evidence item
```

Chunks should preserve:

```text
chunk ID
source record/version ID
field/path
original text
English text if applicable
authority class
created/current timestamps
provider/model provenance where derived
```

Long source descriptions may use structure-aware subchunks while retaining parent provenance.

---

## 34. Embedding subsystem

Embeddings should be provider-independent and versioned.

Each embedded unit needs identity including:

```text
source/chunk identity
embedding provider
embedding model
embedding dimensions
embedding contract/version
created_at
```

Changing embedding models should not overwrite vectors silently. Re-embedding is a migration with
explicit progress/state.

The proposal should support both:

- local embedding models;
- optional remote embedding APIs where privacy policy permits.

Multilingual retrieval quality must be tested because authoritative evidence may remain Persian,
English, or mixed.

---

## 35. Initial retrieval engines

Implementation should stay proportional to corpus size.

A reasonable progression is:

```text
Stage 1
SQLite structured queries + SQLite FTS5 lexical search

Stage 2
add local vector index behind RetrievalStore abstraction

Stage 3
hybrid retrieval + reranking

Stage 4
optional graph/entity retrieval if real queries justify it
```

The proposal does **not** require adopting a standalone vector database immediately. Candidate
storage technologies should be evaluated when corpus size/query requirements make the choice
meaningful.

---

## 36. Hybrid retrieval

A single query may use several signals:

```text
exact source filters
BM25/full-text relevance
vector similarity
current/historical version constraints
role/category/location filters
confidence/review state
semantic concept identity
human triage state
```

A retrieval planner determines which retrieval methods are needed.

Examples:

```text
"jobs in Fars posted this month"
→ SQL first

"roles similar to AI security automation"
→ semantic/vector + taxonomy filters

"show exact evidence for Kubernetes requirements"
→ canonical concept + source evidence + lexical matching

"what changed since May?"
→ temporal SQL + accepted semantic aggregates + evidence retrieval
```

---

## 37. Reranking

Reranking may improve precision after broad retrieval.

Possible implementations:

- lexical/vector score fusion;
- dedicated local/remote reranker model;
- bounded LLM reranking for high-value queries;
- authority/recency/review-state priors.

Reranker model/version and candidate set should be logged for evaluation.

---

## 38. Citation contract

Every RAG answer about JobHunter evidence should expose stable support references.

Conceptually:

```text
Claim
"Python is explicitly required by these four analyzed roles."

Support
job A → original employer excerpt
job B → original employer excerpt
job C → original employer excerpt
job D → original employer excerpt
```

Derived claims must not cite another generated summary as though it were the employer source when
primary evidence is available.

The UI should allow drill-down from RAG answer → analysis claim → exact original evidence → raw
source snapshot.

---

## 39. Temporal RAG and time-travel queries

JobHunter preserves semantic versions and observations, so retrieval should eventually understand
time.

Potential questions:

- "What did this job require when we first saw it?"
- "Which requirements were added later?"
- "What was the market picture on 2026-07-01?"
- "Which roles disappeared or were reposted?"

Indexes therefore need current/historical scope rather than treating the latest document as the
only retrievable truth.

---

## 40. Retrieval freshness and incremental indexing

The index should update from durable record changes, not by periodically rebuilding everything.

Potential events:

```text
new source semantic version
new validated English v2 artifact
new accepted analysis artifact
new approved canonical mapping
new personal evidence
artifact superseded by newer contract
```

Each event creates/updates the relevant retrieval units.

Indexing must be:

- repeat-safe;
- resumable;
- version-aware;
- inspectable;
- able to identify stale/missing embeddings.

---

## 41. Ask JobHunter

A future first-class page could provide evidence-grounded conversational queries.

Examples:

```text
Ask JobHunter

"What skills are appearing across AI-security roles?"
"Show me five jobs that combine Python and network security."
"Why does JobHunter think Linux is important?"
"Compare RAG-engineer and MLOps roles in my corpus."
```

Each response should include:

- answer;
- evidence/citations;
- sample size/scope;
- filters/time window;
- model/provider used;
- confidence/limitations when material;
- option to inspect retrieved evidence.

This should be a retrieval-backed intelligence surface, not an unrestricted chatbot.

---

## 42. RAG for agents

Specialist agents should retrieve only the context needed for their tasks.

Examples:

```text
Search Strategist
→ search effectiveness + recent analyzed titles/concepts

Market Analyst
→ deterministic aggregates + supporting examples

Gap Analyst
→ canonical market requirements + reviewed personal capabilities

Learning Planner
→ selected gap + prerequisite graph + personal learning/project evidence
```

This reduces prompt size and keeps agent decisions grounded.

---

## 43. Optional knowledge graph / Graph-RAG layer

Do not start with a graph database solely because "Graph RAG" is fashionable.

However, JobHunter naturally develops relationships such as:

```text
job → role archetype
job → responsibility
job → requirement
requirement → canonical concept
concept → alias
concept → prerequisite concept
personal project → demonstrated capability
capability → market concept
role archetype → common concept
```

If real queries benefit from multi-hop reasoning, introduce a versioned evidence graph or graph
projection later. SQLite relations may remain sufficient initially.

---

# Part IV — Continual learning and the JobHunter data flywheel

## 44. Definition of continual learning for JobHunter

"Continual learning" should initially mean that JobHunter **systematically improves its data,
retrieval, routing, prompts, taxonomy, and decisions as reviewed evidence accumulates**.

It does **not** initially mean:

```text
model generates answer
→ system treats its own answer as training truth
→ model retrains itself
```

That loop compounds hallucinations and bias.

The safer progression is:

```text
new evidence
   ↓
derived model output
   ↓
deterministic checks / verifier / human review
   ↓
quality outcome + correction
   ↓
evaluation dataset grows
   ↓
models/prompts/retrieval/routing are benchmarked
   ↓
reviewed improvement proposal
   ↓
new version deployed in shadow/test mode
   ↓
accepted only if evidence shows improvement
```

---

## 45. Feedback event model

Capture feedback as durable events rather than editing generated artifacts invisibly.

Potential events:

```text
translation accepted
translation corrected
analysis claim accepted
analysis claim rejected
requirement classification corrected
canonical alias accepted/rejected
search suggestion accepted/rejected
RAG answer useful/not useful
retrieval result relevant/not relevant
personal capability correction
agent proposal accepted/rejected
```

Feedback should reference the exact artifact/provider/model/prompt/retrieval contract that produced
the result.

---

## 46. Golden evaluation corpora

Maintain small reviewed benchmark sets that grow deliberately.

Potential sets:

```text
translation-golden-v1
analysis-golden-v1
retrieval-golden-v1
lifecycle-golden-v1
normalization-golden-v1
role-archetype-golden-v1
RAG-answer-golden-v1
```

A golden case contains expected evidence or judgment, not merely a previous model's output.

---

## 47. Model evaluation harness

The AI Lab should be able to run candidate providers/models against golden sets and report
JobHunter-specific results.

Metrics depend on task.

### Translation

- field association integrity;
- semantic fidelity review score;
- omission/invention rate;
- terminology consistency;
- latency/cost.

### Semantic analysis

- evidence support precision;
- claim recall where gold exists;
- required/preferred classification accuracy;
- unsupported-claim rate;
- schema failure rate;
- verifier disagreement rate.

### Retrieval

Potential IR metrics:

```text
Recall@k
Precision@k
MRR
nDCG
```

plus citation/support correctness.

### RAG answers

- evidence coverage;
- citation correctness;
- unsupported-claim rate;
- answer usefulness review;
- latency/cost.

---

## 48. Champion/challenger model lifecycle

For important tasks:

```text
champion
current accepted provider/model/prompt/retrieval contract

challenger
candidate tested against the same benchmark
```

A challenger does not become current merely because it is newer or larger.

Promotion criteria may include:

- quality improvement;
- no unacceptable regression;
- acceptable cost/latency;
- stable structured output;
- privacy compatibility.

---

## 49. Shadow mode

Before replacing a production analytical route, a challenger may run in shadow mode on a bounded
sample.

```text
current model → user-visible accepted artifact
candidate model → hidden comparison artifact
```

The system compares outputs without affecting current intelligence until review/benchmarking
passes.

---

## 50. Active-learning queue

Prioritize human review where it yields the most learning value.

Candidates include:

- analyst/verifier disagreement;
- low-confidence claims;
- translation integrity warnings;
- novel concepts;
- uncertain normalization mappings;
- retrieval queries with poor evidence coverage;
- model disagreements;
- rare role archetypes;
- high-impact personal gap conclusions.

This is more efficient than reviewing random artifacts uniformly.

---

## 51. Search-learning loop

The search catalog can improve from evidence without autonomous mutation.

```text
search results
→ effectiveness metrics
→ later relevance/analysis outcomes
→ Search Strategist proposals
→ review
→ catalog version change
→ compare future coverage
```

This turns search vocabulary into a measured evolving acquisition policy.

---

## 52. Taxonomy-learning loop

```text
raw semantic concepts
→ frequency/co-occurrence
→ normalizer proposals
→ reviewed aliases/concepts
→ canonical registry version
→ re-aggregate market facts
```

Historical source/analysis artifacts remain unchanged; the canonical interpretation layer evolves.

---

## 53. Retrieval-learning loop

Track retrieval behavior:

```text
query
candidate retrieval sets
reranker result
citations used
user/agent feedback
answer quality
```

Use it to evaluate:

- lexical/vector weights;
- embedding models;
- chunking strategies;
- rerankers;
- top-k;
- query planner policies.

Retrieval policy changes should be benchmarked, not tuned from one anecdotal query.

---

## 54. Routing-learning loop

Over time JobHunter can recommend task routes based on observed evidence:

```text
quality
latency
cost
failure rate
structured-output reliability
privacy compatibility
```

Example proposal:

```text
For job_semantic_analysis:
Model B is 12% cheaper and has equal evidence precision on the current golden set.
Recommend challenger trial.
```

Automatic provider switching based solely on self-measured quality should not occur initially;
operator approval is safer.

---

## 55. Drift detection

Continual systems need to detect when assumptions stop holding.

Potential drift signals:

- new terminology/technology clusters;
- search terms losing unique contribution;
- changing role-title distributions;
- analysis output distribution shifts after a provider update;
- rising verifier disagreement;
- falling retrieval benchmark performance as corpus grows;
- embedding coverage gaps;
- stale personal evidence;
- market requirement prevalence shifts.

Drift should create diagnostics/review tasks before causing automatic large-scale reprocessing.

---

## 56. Optional fine-tuning / adapters — later only

Fine-tuning, LoRA, adapters, or custom classifiers may eventually be useful for:

- relevance triage;
- requirement classification;
- normalization;
- domain-specific extraction;
- reranking.

Prerequisites:

1. sufficiently large reviewed dataset;
2. clear baseline task and metric;
3. train/validation/test split;
4. provenance/consent appropriate for the data;
5. reproducible training configuration;
6. evidence that prompting/RAG/routing alone is insufficient;
7. rollback path.

Never train on unreviewed model output as ground truth.

---

# Part V — AI Lab and experimentation platform

## 57. AI Lab

Add a dedicated future UI section for controlled experiments that do not silently alter current
production artifacts.

Potential modes:

### Translation comparison

```text
same job/source fields
→ local model
→ NVIDIA model
→ OpenCode model
→ integrity checks
→ side-by-side comparison
```

### Analysis comparison

```text
same reviewed job
→ model A
→ model B
→ verifier
→ claim/evidence diff
```

### Retrieval comparison

```text
same question
→ lexical only
→ vector only
→ hybrid
→ hybrid + reranker
```

### RAG comparison

Compare answer claims, citations, latency, and cost.

---

## 58. Experiment registry

Each experiment should retain:

```text
experiment ID
purpose
corpus snapshot / case IDs
task
provider/model
prompt/schema
retrieval/chunking/embedding settings
metrics
human review
result
promotion decision
```

This prevents repeating the same model/provider experiments without remembering why a previous
choice was made.

---

## 59. Quality modes

Potential user-facing modes:

```text
Fast
single accepted model, deterministic validation

Verified
analyst + verifier

Research
multiple candidate models + verifier + comparison
```

Quality mode affects cost/latency explicitly and must remain bounded.

---

# Part VI — AI decisions, review, and explainability

## 60. AI Decisions inbox

Create a future review surface for consequential proposals and uncertain cases.

Potential cards:

```text
3 suspicious translations
5 analyst/verifier disagreements
12 proposed search terms
4 canonical alias proposals
2 lifecycle ambiguities
7 new concepts needing classification
3 model-routing recommendations
```

Actions:

```text
inspect evidence
accept
reject
edit/correct
defer
```

The goal is to concentrate human attention where it creates durable value.

---

## 61. Explainability requirements

Every durable AI conclusion should make it possible to inspect:

```text
what task ran
why it ran
input records
retrieved context
provider/model
prompt/schema version
raw/structured output where appropriate
validation/verifier result
final accepted artifact
human feedback/correction
```

Future recommendations additionally explain contradictory and missing evidence.

---

# Part VII — AI task queue and operations

## 62. Durable AI task queue

As AI work grows beyond a single browser operation, introduce a durable queue rather than spawning
unbounded agent work.

Potential states:

```text
pending
running
completed
failed
blocked_review
cancelled
```

Task types could include translation, analysis, verification, embedding, reranking benchmark,
normalization, and synthesis.

Controls:

```text
pause
resume
cancel pending
retry eligible failures
inspect result
```

---

## 63. Concurrency policy

Default conservative concurrency:

```text
local inference          1
remote inference         small configured number
source acquisition       existing bounded/sequential policy
```

Provider-specific rate limiting and JobHunter cost budgets override generic concurrency.

---

## 64. Scheduling

Only after the complete workflow and durable task queue are proven idempotent.

Potential scheduled cycle:

```text
market acquisition
→ source processing
→ bounded translation
→ bounded analysis
→ incremental RAG indexing
→ deterministic aggregates
→ drift/quality checks
→ optional agent proposals
→ review inbox
```

Do not let scheduled agents modify high-authority taxonomy/personal/career conclusions without the
appropriate approval policy.

---

# Part VIII — RAG/agent memory model

## 65. Separate retrieval memory from conversational memory

JobHunter should distinguish:

```text
session context
    transient interaction state

durable evidence
    authoritative or reviewed records

derived knowledge
    versioned model/taxonomy artifacts

retrieval index
    reproducible projection of durable records

agent run history
    operational/provenance state
```

An agent should not "remember" a fact merely because it appeared in an earlier chat. Durable facts
must exist as records with provenance.

---

## 66. Personal memory later

Future personal evidence may support useful durable memory, but only through reviewed records.

Examples:

- verified project capability;
- stated target role;
- reviewed learning progress;
- explicit constraint/preferences.

Personal memory must remain correctable, timestamped where useful, and distinct from market truth.

---

# Part IX — Security and safety boundaries

## 67. Prompt injection from job postings

Job postings and arbitrary acquired text are untrusted.

Agents must treat source text as data, not instructions.

Required controls:

- strong system/task separation;
- no agent shell/browser access for ordinary job analysis;
- no credentials included in prompts;
- structured schemas where appropriate;
- explicit retrieval source classes;
- tool allowlists;
- output validation;
- bounded loops.

---

## 68. Remote-provider disclosure

Before data is sent to a remote provider, JobHunter should know:

```text
task
provider
privacy class
estimated/request budget
```

The UI should make local versus external routes visible.

---

## 69. Secret management

Never persist API keys in:

- repository files committed to Git;
- raw inference request artifacts;
- operation summaries;
- RAG chunks;
- SQLite model outputs.

Use environment references initially; evaluate OS keyring/secret-store integration only if it
materially improves usability.

---

# Part X — Product surfaces

## 70. System → AI Providers

Potential panel:

```text
LM Studio
Connected
Local/private
Models: ...

NVIDIA
Connected
External
Credential configured: yes

OpenCode Zen
Connected
External
Credential configured: yes
```

Actions:

- health test;
- refresh models;
- inspect capabilities;
- configure task route;
- inspect usage/budget.

---

## 71. AI Routes

Show current task routing and fallback chains in human language.

```text
Translation
Local Gemma
fallback: disabled

Job analysis
NVIDIA model X
fallback: OpenCode model Y → local model Z

Verifier
OpenCode model Y
```

---

## 72. Ask JobHunter

RAG-backed market/career intelligence interface with citations and scope controls.

Filters may include:

- current vs historical;
- date range;
- role archetype;
- category/location;
- reviewed-only;
- source vs derived evidence;
- personal evidence on/off later.

---

## 73. AI Lab

Controlled model/retrieval experiments.

---

## 74. AI Decisions

Human review queue for uncertain/consequential AI proposals.

---

## 75. AI Operations

Durable task queue, failures, provider cooldown, budgets, usage, and recent model activity.

---

# Part XI — Additional future intelligence opportunities

## 76. Similar-job discovery

Use semantic retrieval + canonical analysis to find:

- near-identical roles;
- related role families;
- unusual combinations;
- repost/near-duplicate candidates.

Keep source deduplication separate from semantic similarity.

---

## 77. Requirement dependency graph

Over time infer/review prerequisite relationships among concepts for learning planning.

Example:

```text
networking fundamentals
    → network security concepts
    → detection/network telemetry
```

Relationships should be reviewed and may combine project knowledge with market evidence; they are
not employer facts.

---

## 78. Opportunity novelty detector

Highlight jobs that are materially different from the current corpus:

- new role titles;
- new technology clusters;
- unusual responsibility combinations;
- previously unseen domains.

This supports both market monitoring and active-learning review.

---

## 79. Market coverage auditor

Ask whether JobHunter's current search plan appears to miss portions of the market represented by
its own analyzed concepts and emerging role titles.

It may propose searches but cannot claim coverage of the entire employment market from Jobinja
alone.

---

## 80. Evidence density / confidence views

A concept or recommendation should expose how much evidence exists:

```text
jobs supporting claim
independent employers
recent vs old observations
explicit vs inferred claims
reviewed vs unreviewed
```

This is more useful than a single confidence percentage.

---

## 81. Contradiction finder

Agents/RAG can surface apparent contradictions:

- same technology marked required in one cluster but merely preferred in another;
- translation vs source strength mismatch;
- personal self-report vs project evidence;
- old capability evidence vs newer contrary evidence.

Contradictions become review opportunities rather than being silently averaged away.

---

## 82. What-if analysis

Later, use deterministic market/personal data plus an explanatory model to answer bounded questions:

```text
What gaps remain if I become working-level in Kubernetes?
Which role archetypes become more reachable if I strengthen networking?
What evidence would most improve application readiness for this cluster?
```

The system should identify assumptions used in the scenario.

---

## 83. Research notebook / intelligence briefs

Generate durable, source-backed briefs from selected corpus slices:

- monthly AI-security market brief;
- Python/security overlap brief;
- role-archetype comparison;
- learning-priority evidence packet.

Generated prose is derived; supporting facts/citations remain inspectable.

---

# Part XII — Proposed implementation progression

## 84. Increment AI-A — Provider-agnostic inference foundation

Build first:

- generic OpenAI-compatible provider;
- provider registry;
- model registry/capability representation;
- LM Studio migration to the common provider abstraction;
- NVIDIA hosted NIM provider configuration;
- OpenCode Zen compatible provider configuration;
- environment-secret references;
- provider health/model discovery;
- local/external privacy metadata;
- deterministic tests with mock transports.

**Do not yet switch production routes automatically.**

---

## 85. Increment AI-B — Task routing, fallback, and usage governance

- task route configuration;
- fallback chains;
- provider cooldown/rate-limit state;
- inference usage ledger;
- token/cost/latency tracking where available;
- request/token/cost budgets;
- System → AI Providers/Routes UI;
- explicit local-vs-remote visibility.

Acceptance requires exact persisted provider/model provenance after fallback.

---

## 86. Increment AI-C — AI Lab and evaluation foundation

- experiment registry;
- golden-set schema;
- provider/model comparison;
- translation benchmark runner;
- P1.6 analysis benchmark runner;
- champion/challenger concepts;
- shadow-mode artifacts;
- basic review UI.

This should precede broad autonomous provider/model changes.

---

## 87. Increment AI-D — Verification agents

- Translation Critic;
- Evidence Critic/Analysis Verifier;
- disagreement/review states;
- Fast / Verified / Research quality modes;
- active-learning queue from disagreements.

---

## 88. Increment RAG-A — Retrieval foundation

- retrieval-store abstraction;
- versioned semantic chunk model;
- source/authority metadata;
- SQLite FTS5 index;
- deterministic structured retrieval;
- incremental indexing ledger;
- current/historical scope;
- retrieval diagnostics/tests.

No vector database required yet.

---

## 89. Increment RAG-B — Semantic retrieval

- embedding-provider abstraction;
- local embedding model support;
- versioned vector identity;
- multilingual retrieval evaluation;
- vector store selected based on measured corpus needs;
- hybrid lexical/vector fusion;
- stale/missing embedding repair.

---

## 90. Increment RAG-C — Reranking and Ask JobHunter

- query classification/planning;
- hybrid retrieval;
- optional reranker;
- evidence package;
- citation-first answer generation;
- Ask JobHunter UI;
- answer/retrieval provenance;
- retrieval golden set and Recall@k/MRR/nDCG evaluation.

---

## 91. Increment CL-A — Feedback and continual-improvement ledger

- durable feedback events;
- artifact correction links;
- AI Decisions inbox;
- quality sampling;
- active-learning selection;
- drift signals;
- no automatic self-training.

---

## 92. Increment CL-B — Search/taxonomy/retrieval learning loops

- Search Strategist proposals;
- Semantic Normalizer proposals;
- retrieval-policy experiments;
- benchmark-backed routing recommendations;
- human approval of policy/taxonomy changes.

---

## 93. Increment AI-E — Market intelligence agents

After enough accepted analysis exists:

- Role Archetype Builder;
- Market Analyst;
- Trend Analyst;
- Market Coverage Auditor;
- novelty detector;
- job comparison.

---

## 94. Increment AI-F — Personal career intelligence

Only after Phase-3 personal evidence exists:

- Personal Capability Analyst;
- Gap Analyst;
- Career Path Simulator;
- Learning Planner;
- Application Readiness Agent;
- what-if analysis;
- personal/private RAG zone.

---

## 95. Increment CL-C — Optional training/fine-tuning research

Only if reviewed evidence demonstrates value:

- dataset export/versioning;
- baseline benchmark;
- local fine-tuning/LoRA experiment;
- validation against untouched test set;
- rollback;
- no production promotion without measured improvement.

---

# Part XIII — Acceptance framework

## 96. Provider acceptance

A provider is usable for a task only when:

- connectivity succeeds;
- credentials are not leaked;
- model identity is exact;
- required structured-output/tool capability is verified;
- timeout/retry/rate-limit behavior is bounded;
- deterministic mocks pass;
- at least one safe live smoke test passes;
- privacy classification permits the task.

---

## 97. Agent acceptance

An agent is accepted only when:

- its authority boundary is defined;
- tool access is minimal;
- prompt/schema are versioned;
- outputs have deterministic validation where possible;
- provenance is persisted;
- failure/review states are explicit;
- golden/live evaluation meets a stated threshold;
- reruns are reproducible or differences are explainable.

---

## 98. RAG acceptance

Before relying on RAG for career conclusions:

- indexing is complete/repeat-safe;
- current vs historical scope works;
- retrieved records retain source/version provenance;
- benchmark retrieval metrics are measured;
- citations resolve to real evidence;
- unsupported answer claims are detectable/reviewed;
- model changes cannot silently alter retrieval identity;
- personal/private zones respect provider routing policy.

---

## 99. Continual-learning acceptance

A learning loop is accepted only when:

- it consumes reviewed feedback/evidence;
- the baseline and proposed change are measurable;
- the proposal can be rejected/rolled back;
- history is retained;
- no unreviewed model output becomes training truth;
- changes to high-authority policy/taxonomy/personal evidence require appropriate approval.

---

# Part XIV — Explicit non-goals / anti-patterns

## 100. Do not build these merely because the proposal mentions AI

Avoid:

- a swarm of agents that mostly talk to each other;
- a vector database before retrieval requirements justify one;
- autonomous fine-tuning from raw model outputs;
- opaque "career fit 93%" scores;
- model-calculated statistics that SQL can compute exactly;
- silently changing search vocabulary;
- silently changing canonical taxonomy;
- sending private personal evidence to remote providers by default;
- storing API keys in SQLite/Git/logs;
- unrestricted shell/browser tools for job-analysis agents;
- replacing authoritative source text with embeddings/summaries;
- rebuilding every embedding on every run;
- RAG answers without citations;
- treating one provider's current free tier as permanent architecture;
- creating separate browser-only and CLI-only AI backends.

---

# Part XV — Proposed future product experience

## 101. Normal repeated-use workflow

Eventually:

```text
Open JobHunter
    ↓
Run full workflow
    ↓
source acquisition + parsing
    ↓
translation + semantic analysis
    ↓
incremental RAG indexing
    ↓
market aggregates
    ↓
quality/drift checks
    ↓
review inbox only when attention is useful
```

The operator should not need to manually manage every intermediate model command.

---

## 102. Research workflow

```text
Ask JobHunter
"What is changing in AI-security requirements?"
    ↓
retrieval planner
    ↓
structured + lexical + semantic evidence
    ↓
source-backed synthesis
    ↓
citations + sample scope
    ↓
open supporting jobs / claims
```

---

## 103. Improvement workflow

```text
AI Lab
    ↓
run challenger model/retrieval strategy
    ↓
compare golden-set metrics
    ↓
inspect differences
    ↓
approve/reject route change
```

---

## 104. Personal career workflow later

```text
market evidence
+
reviewed personal capability evidence
+
RAG retrieval
        ↓
Gap Analyst
        ↓
Learning Planner / Career Path Simulator
        ↓
explainable recommended actions
        ↓
user reviews evidence and chooses action
```

---

# Part XVI — Decisions to make before implementation

This proposal intentionally leaves several implementation choices open.

Before AI-A/RAG-A begins, decide:

1. Which external providers are approved initially: NVIDIA, OpenCode Zen, both, others?
2. Which tasks may use remote inference initially?
3. Whether task routing is configured only in TOML first or also editable in UI.
4. Initial remote request/token/cost ceilings.
5. Whether remote fallback from a local-first task is opt-in globally or per task.
6. Which embedding models are candidates for Persian/English/mixed retrieval.
7. Whether the first vector index remains in-process/local-file or uses a separate local service.
8. Which 10–30 reviewed cases seed the first translation/analysis/retrieval golden sets.
9. Which agent proposals require mandatory human approval.
10. Whether AI Lab experiments may create non-current shadow artifacts in the production SQLite DB
    or use a separate experiment database.

These should be decided from implementation simplicity, privacy, measured quality, and current
corpus needs—not from provider popularity.

---

# Part XVII — Recommended immediate interpretation

The strongest architectural sequence is:

```text
Finish current Phase-1 acceptance
        ↓
AI-A provider abstraction
        ↓
AI-B task routing + governance
        ↓
AI-C evaluation/AI Lab
        ↓
AI-D verifier/critic layer
        ↓
RAG-A structured + lexical retrieval
        ↓
RAG-B semantic/vector retrieval
        ↓
RAG-C Ask JobHunter + citation-first synthesis
        ↓
CL-A feedback/active-learning loop
        ↓
CL-B search/taxonomy/retrieval improvement
        ↓
market-specialist agents
        ↓
personal career agents after personal evidence exists
        ↓
optional fine-tuning research only if benchmarks justify it
```

This sequence deliberately builds **evaluation before autonomy**, **retrieval before broad
synthesis**, and **reviewed evidence before self-improvement**.

---

## 105. Proposal success condition

If this proposal is eventually accepted and implemented well, JobHunter should become a system that:

- continuously acquires and preserves changing market evidence;
- incrementally understands and indexes that evidence;
- can retrieve exact supporting information across the growing corpus;
- can use different models/providers for the tasks each performs best;
- verifies consequential model interpretations rather than blindly trusting them;
- learns from reviewed corrections and measured quality outcomes;
- detects drift and novel market signals;
- improves its search, taxonomy, retrieval, and model routing through evidence-backed proposals;
- later compares the market against explicit personal capability evidence;
- generates explainable learning/career actions;
- remains local-first, reproducible, bounded, and inspectable throughout that growth.

The long-term target is therefore not simply an LLM-powered job scraper. It is an
**evidence-centered, continually improving personal career-intelligence platform** in which AI is
powerful because it is grounded, measured, replaceable, and accountable.
