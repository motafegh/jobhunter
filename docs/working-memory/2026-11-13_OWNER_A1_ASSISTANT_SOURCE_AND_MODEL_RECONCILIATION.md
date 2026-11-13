# Owner Audit A1 — assistant source-first completion and model reconciliation

**Recorded:** November 13, 2026
**Packet:** `JH-OWNER-A1-20261113`
**Status:** Four original-source cases assessed by assistant; existing owner responses on two cases preserved; saved model outputs compared; **NO semantic promotion or new human owner verdict**
**Repository:** documentation-only follow-up to accepted Stage A at main `3b13e7f0ba049d55b1eb43f1caaa1a4b2a0d42d8`
**Private originals:** ignored `data/local-acceptance/owner-audit-2026-11-13/`
**Sanitized machine-readable results:** `docs/working-memory/2026-11-13_owner_a1_assistant_review/SAFE_RECONCILIATION_METRICS.json`

## 1. Review authority and methodology

The owner initially submitted a source-only Pass A JSON covering `tNhZ` and `tMps`, leaving `tNDx` and `tMjm` blank. The owner then explicitly delegated completion of the reviews to the assistant and asked to be consulted **only** for matters the evidence could not resolve.

We preserved the exact **2977-byte original owner submission**, SHA-256 `55ae967a2d3015ac077822cb9667690b0178dc585ad5f502c58385f6aeb584c6`, without revising or retroactively extending it. The two missing owner verdicts are **not** attributed to the owner.

The assistant then examined the four frozen parsed original **Persian** employer descriptions in the isolated source database, independently of the active Pass B artifacts. The assistant annotated **59 evidence-anchored assertions**, including original Unicode offsets, source-version identity and SHA-256, with mandatory / preferred / duty / arrangement / unresolved categories and metadata separated. This source-review snapshot was frozen at SHA-256 `2d57a8a96483e7ef32307bddb4edd5ff9978d1da9a85aceb2dfb254ad7e58ccd` before the focused model-output comparison.

This **is not a blind independent assistant review**: earlier conversations included prior model failure findings, and the assistant had that contextual exposure. No new independent human evaluation of the assistant's 59 statements is asserted. The original owner's two answers remain genuine, separate and prior to this new reconciliation.

After the source-only freeze, the assistant inspected the retained, source-identity-verified English projections, original-language artifact, v31 experimental candidate, rejected candidate archive and failed run evidence. Prior Pass B input seal SHA-256: `112f7f10912a22560ef1073a13d0983d00d62bd7abc5db43f64fb8df26900c07`. Detailed comparisons remain in ignored `ASSISTANT_PASS_B_SOURCE_MODEL_RECONCILIATION.json`.

**Important limit:** Legacy English projection v2 is tied to the *whole source field*; manually comparing original/translated phrases does not upgrade it into a proven automated one-to-one item alignment. Every new source claim here is an **assistant evaluation**, not an accepted P1.6 artifact.

## 2. Source-only findings on the four original advertisements

### `tNhZ` — Python/backend trading-platform development

The advertisement's headline emphasizes AI/LLM, but the employer description explicitly seeks a **Python Backend Developer** for a financial-market analytical/backtesting product. Six specific duties appear under the explicit role-task prompt: developing the Python core; implementing market/trading logic; building data-processing and backtest functions; developing services and APIs; participating in AI/LLM features; testing and optimization.

The main explicit technical qualification is good Python/backend proficiency. The employer also emphasizes problem-solving, creativity, diligence, ownership and responsibility for output. The original explicitly says **financial-market, backtesting, technical-analysis OR LLM familiarity is an advantage, not a requirement**. Participation in developing an AI/LLM feature as assigned work does not establish prior LLM expertise as mandatory.

GitHub/portfolio is welcomed when available as **optional supporting application material**; it is not an alternative eligibility route. The employer prose permits part-time or full-time **by agreement**, remote work and negotiated compensation. The board's `full-time` category conflicts with the prose's stated flexibility. The board's `LLM` skill tag must not be treated as a mandatory qualification against the employer's explicit optional statement. The board's "less than three years" experience category is not an employer minimum.

Unknown: exact frameworks, infrastructure/database/cloud technologies, precise salary, and numerical employer seniority threshold.

### `tMps` — applied enterprise AI engineering with alternative tracks

Explicit duties include designing/developing/deploying practical enterprise AI solutions; LLM applications, prompt engineering and optimization, inference performance/cost, RAG/agents, enterprise system integrations and local-model serving/lifecycle work. Named frameworks in duty descriptions are not **individually** mandatory credentials just because they appear as examples of work.

The employer explicitly lists familiarity with **vector databases, vector search, reranking, agent architecture, and context management** under required skills. The separate advantages section covers on-premise/self-hosted AI, Dify/Hugging Face/OpenAI-compatible APIs, Kubernetes/Kafka/MLflow/observability, and the listed security/privacy concepts.

There are two **alternative** eligibility pathways: Middle (2–4 relevant years, practical experience in **one of** LLM/RAG/GenAI/ML/NLP, and at least one practical completed project) **OR** Senior (4–7 relevant years plus design and production deployment of at least one AI/ML/LLM system). Both are not cumulatively required. Full-time and hybrid are working arrangements, not qualifications. The board's 3–6 years tag does not accurately express those alternative employer paths, and its `skills` list includes section headings and non-skill page content (field contamination).

Unknown: minimum proficiency in each example tool, compensation, formal certification and degree authority beyond board metadata.

### `tNDx` — enterprise endpoint-detection-response technical support

Five explicit employer duties: deploy/configure/support Kaspersky EDR and other security brands; troubleshoot enterprise customers; perform onsite/remote/phone technical tasks under internal procedures; handle customer technical tickets; prepare technical documents and periodic reports.

Requirements clearly include **3 years continuous IT/network-security experience**, Network+/Security+ conceptual mastery with **certificate OR equivalent knowledge**, practical Windows Server/VMware/enterprise networking familiarity, and independent technical decisions.

**Corrected historical error:** The Persian source explicitly says teamwork/acceptance of management structure **is an advantage** (`مزیت محسوب می‌شود`), and the English rendering preserves it. Do not reintroduce the earlier mistaken "teamwork was required" or "English translation changed the requirement" interpretations.

Kaspersky-specialist certifications and government/large-enterprise customer experience are present after this item; their exact mandatory/preferred status is not independently explicit. Retain **unresolved obligation**, not automatic required/preferred. Final hiring depends on passing a technical entrance examination. The employer prose indicates approximately **80 million toman, negotiable and conditioned on the entrance result/experience**; the board advertises "from 45 million toman." These are conflicting source-labeled salary statements. Onsite/remote/telephone *customer support channels* do not prove employees may work from home.

Unknown: specific Kaspersky certificate obligation, employer remote-work arrangement, full entrance-test scope and committed salary.

### `tMjm` — penetration-testing skills and general employment conditions

The posting lists specialized requirements: information-security concepts; web/network penetration-testing methodologies; web-service vulnerabilities; OWASP methods; pentesting tools; the **ability** to find, document and propose remediation for vulnerabilities, and technical documentation. Behavioral/general conditions include working under pressure, teamwork and knowledge sharing, conscientiousness, compliance with stated organizational and legal values, and continuous learning.

**Do not fabricate an explicit day-to-day work statement.** The ad mostly describes applicant *capabilities*, despite its broad `شرح شغل و وظایف` introductory heading. The role and required skills strongly suggest penetration-testing work, but no distinct scope, target systems, engagement process or specific operational responsibilities are assigned in a separate duty list. `امکان دورکاری` means **remote work is possible**—a work arrangement, not a skill. The employer states a range of 30–50 million toman. Bachelor's degree and full-time appear in structured board metadata; neither should silently be claimed as a specific employer-description sentence.

Unknown: actual target assets, assessment scope, named mandatory tools beyond OWASP standards, cadence/reporting responsibilities and remote-work conditions.

## 3. Owner draft reconciliation (source only)

The owner's original two-case submission remains frozen. This is feedback on **source classifications**, not a retroactive human approval:

| Case | Supported in owner's draft | Material missing / incorrect |
| --- | --- | --- |
| `tNhZ` | Recognized Python/backend focus and the optional value of financial knowledge | Six explicit duties overlooked; AI/LLM prior proficiency classified mandatory despite optional source; GitHub/portfolio misread as alternate eligibility; part-/full-time remote arrangements omitted |
| `tMps` | Correct enterprise AI role summary, experience tiers and broad preferred tooling | Work technologies bundled into mandatory qualifications; Middle and Senior not marked alternative; one-of domain requirement not clearly preserved; hybrid/full-time included as qualifications; explicit required vector-search list omitted |

No owner answers or review verdicts existed for `tNDx` or `tMjm`; the assistant's review is not represented as having come from the owner. This may eliminate routine manual effort, but **does not generate independent human evidence** for a final semantic promotion gate.

## 4. Pass B — actual saved JobHunter model outputs versus source

| Case | Real saved product/exploratory output | What is supported | What fails or remains unknown |
| --- | --- | --- | --- |
| `tNhZ` | English v30 no candidate; English v31 experimental pending candidate | v31 extracted six actual duties and preferred experience | Structured Jobinja `LLM` tag generated a **required** LLM claim despite explicitly optional source. AI/API board tags were also automatically required; residual LLM item concept malformed. Not advice-ready |
| `tMps` | No stored valid English candidate under v30 or v31 trial | Source includes detailed AI engineering duties and clear Middle/Senior alternatives | Missing usable analysis/required work coverage, not absent employer facts. Cannot score nonexistent model claims |
| `tNDx` | English v30/v31 no valid artifact; original-language v9 mechanically `accepted` | Original v9 correctly marked teamwork preferred; preserved 3-year experience and certificate-or-equivalent Network+/Security+ concept | Only 4 of 5 original duties are under responsibilities; core EDR deployment/configuration duty was misfiled as **role purpose**. Report-writing duty swallowed the following requirements heading; Kaspersky certificate item not recorded; government-customer preference rationale rests on uncertain heading inference |
| `tMjm` | English v30 generated a candidate later **rejected and archived**; no v31 trial | Most explicit penetration-test abilities extracted as qualifications; no invented direct-duty list | **Remote-work possibility** incorrectly classified required. General conditions and board Bachelor's tag were conflated with technical requirements; translation distorted conscientiousness as "identification of duties" |

**Two crucial distinctions:**

1. An artifact stored with `semantic_review_status=accepted` on the historical original-language v9 route is not proof it passed independent source fidelity review. This remains an authority-state risk.
2. `tMps` has no persisted P1.6 candidate in these runs. A missing result cannot be scored as accurate, inaccurate, or proof that the advertisement lacks qualifications. It is a failure to produce usable intelligence.

### Translation fidelity issues independently observed

- `tNDx`: the English translation merges the **requirements heading** into the preceding report-writing duty. It also introduces an **"Advantages"** heading before Kaspersky certifications although no corresponding explicit heading appears at that location in the Persian source. This creates a false certainty about what follows. **Teamwork optionality itself was translated correctly.**
- `tMjm`: original `وظیفه شناس` (*conscientious*) becomes "identification of duties." The English text also leaves remote-work availability joined to a specialized-requirements sentence, which contributed to the model's later incorrect mandatory skill classification.
- `tNhZ`: optional familiarity and duties were conveyed reasonably; the translation leaves out a minor "by agreement" qualifier on part-/full-time.
- `tMps`: Middle/Senior paths, one-of domains and explicit advantages heading are preserved in the saved English text. Model coverage failure should not automatically be blamed on the translation.

There were **11 assistant-observed source/English comparison observations**, including six supported meaning-preserving comparisons and five translation/boundary risks or deviations. A manual phrase comparison does not constitute programmatically proven item alignment.

## 5. Root causes and prioritized engineering work

The four exposed cases provide **18 diagnostic flags**, not 18 independently adjudicated production defects or any population reliability estimate. Prioritize architecture rather than endless prompt-only tuning:

**P0 — stop invalid fact promotion**
1. Reconcile **board metadata versus employer prose** before materializing required skills or years. Do not let source skill tags override explicit optional conditions or append unrelated page text as skills. Preserve conflicting salary/working arrangement statements without choosing a winner.
2. Enforce **original-source section and item-strength ownership**, including original Persian headings, explicit optional/required modality and source-exact spans. A model or translator-added heading is not authoritative.
3. Separate **mechanical schema acceptance from reviewed semantic authority**. Do not allow original-language v9 auto-accepted artifacts to masquerade as independently source-reviewed claims.

**P1 — preserve usefulness and accurate output boundaries**
4. Retain work responsibilities separately from applicant capabilities, job purpose, generic employment context and application instructions. Specifically detect "remote work possible" as arrangement rather than mandatory qualification.
5. Preserve **OR alternatives** (Middle/Senior, certificate/equivalent knowledge, alternative domain experience), numerical years and preferences; explicitly record unresolved cases instead of invented obligations.
6. Build **source-bound bilingual item review and section alignment**, keeping each translation's original field/version, exact item, and semantic-review state. Detect mistranslated individual traits (e.g. conscientiousness) and accidental heading absorption.

**P2 — measured product behavior**
7. Provide graceful source-faithful, clearly marked partial job understanding when full P1.6 candidate generation fails or times out, without claiming absent requirements.
8. Re-run only a bounded new diagnostic set after fixing input truth; verify independently on a **fresh unseen cohort** before upgrading current P1.6. Report timeouts/validity/semantic usefulness separately.

## 6. Review delegation and unresolved matters

The owner has delegated routine source/model review to the assistant. We will not require full manual review packages for each source by default. Assistant findings stay **assistant-reviewed** and source-anchored, not independently human-certified. Ask the owner only where their judgment is actually needed; source ambiguities that only the **employer** can resolve should remain explicitly unresolved rather than asking the owner to guess.

No owner clarification is needed to finish this four-job exposed diagnostic review. The only materially unresolved items are employer-source questions such as Kaspersky certification strength, actual remote-work policy, and conflicting board-versus-employer salary/experience metadata. These cannot be decided reliably from the captured description.

No new model output was generated, no current English P1.6 artifact was accepted, and there was no production database write. This report is review/evaluation evidence; it is **not** a merge approval of source-lineage heuristics, a v31 rollout, or a replacement for fresh verification.

## 7. Evidence and reproduction

- Frozen owner submission: ignored `data/local-acceptance/owner-audit-2026-11-13/JH-OWNER-A1-20261113_ORIGINAL_OWNER_PASS_A.json`, SHA-256 `55ae967a2d3015ac077822cb9667690b0178dc585ad5f502c58385f6aeb584c6`.
- Frozen assistant source-only 59-claim review: ignored `ASSISTANT_PASS_A_SOURCE_REVIEW.json`, SHA-256 `2d57a8a96483e7ef32307bddb4edd5ff9978d1da9a85aceb2dfb254ad7e58ccd`; every source-span identity and UTF-8 offset was verified.
- Archived Pass B evidence seal: ignored `packet-b-sealed/MODEL_COMPARISON_SEAL.json`, SHA-256 `112f7f10912a22560ef1073a13d0983d00d62bd7abc5db43f64fb8df26900c07`.
- Detailed private four-case model reconciliation: ignored `ASSISTANT_PASS_B_SOURCE_MODEL_RECONCILIATION.json`; hash is recorded in sanitized report.
- Sanitized source-safe public counts, original identifiers, flags and hashes: `docs/working-memory/2026-11-13_owner_a1_assistant_review/SAFE_RECONCILIATION_METRICS.json`.
- Original employer snapshots, saved English projections and preserved model artifacts: isolated `data/local-acceptance/current-real-ads-2026-11-12/` and `data/local-acceptance/p16-source-fidelity-v31-2026-11-12/`.
- Historical EDR erratum: `evaluation/current-real-ads-2026-11-12` branch, `docs/working-memory/2026-11-13_EDR_TEAMWORK_SOURCE_INTERPRETATION_ERRATUM.md`.

**Next action:** start a separate source-fidelity Stage B design/implementation slice using this review's prioritized issues. Do **not** automatically promote or persist new employer facts until a fresh, independently checked verification gate demonstrates accuracy.
