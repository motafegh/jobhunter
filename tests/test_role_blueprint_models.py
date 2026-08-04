import json

from jobhunter.role_blueprint_models import RoleCapabilityBlueprint


def _payload() -> dict:
    return {
        "role_read": (
            "This is primarily an applied AI automation and integration role rather than a "
            "model-training position."
        ),
        "likely_role_shape": "Applied AI Automation / Integration Engineer",
        "capability_areas": [
            {
                "name": "Python for AI and systems integration",
                "interpretation_strength": "highly_likely",
                "likely_depth": (
                    "Practical intermediate application engineering: independently integrate, "
                    "validate, debug and operate ordinary API/document workflows."
                ),
                "why_this_matters": (
                    "Python connects AI APIs, document processing, business rules and internal "
                    "systems in the described automation work."
                ),
                "likely_subskills": [
                    "HTTP/JSON request handling and authentication",
                    "structured data validation",
                    "file/document ingestion",
                    "logging and exception handling",
                ],
                "likely_tools_or_examples": [
                    {
                        "name": "httpx or requests",
                        "relationship": "likely_example",
                        "why_relevant": "Typical Python HTTP clients for AI/CRM/API integrations.",
                    },
                    {
                        "name": "Pydantic",
                        "relationship": "possible_example",
                        "why_relevant": "Useful for validating structured AI extraction results.",
                    },
                ],
                "likely_work_products": [
                    (
                        "A service or script that sends documents to an AI API and validates "
                        "the structured result"
                    ),
                    "Integration code that updates an internal system after business-rule checks",
                ],
                "likely_failure_modes_or_operational_concerns": [
                    "timeouts and rate limits",
                    "malformed or incomplete model output",
                    "duplicate updates when retries occur",
                ],
                "probably_not_required": [
                    "CPython internals",
                    "training deep neural networks from scratch",
                ],
            }
        ],
        "hidden_requirements": [
            {
                "title": "Human review boundaries",
                "explanation": (
                    "Shipping/business documents can contain consequential fields, so uncertain "
                    "AI extraction likely needs validation or human review before system updates."
                ),
                "interpretation_strength": "highly_likely",
            }
        ],
        "likely_end_to_end_scenarios": [
            {
                "name": "Shipping-document automation",
                "why_likely": "The posting combines document AI with internal-system integration.",
                "flow_steps": [
                    "Receive document or attachment",
                    "Extract structured fields with AI",
                    "Validate fields and business rules",
                    "Update CRM/internal system or route for human review",
                ],
                "engineering_concerns": ["auditability", "idempotency", "data validation"],
                "interpretation_strength": "highly_likely",
            }
        ],
        "what_probably_does_not_matter": [
            "Deep transformer training research unless another part of the role adds it"
        ],
        "important_unknowns": ["The employer does not identify its CRM or email platform."],
        "bottom_line": (
            "A strong candidate likely needs to turn messy business processes into reliable "
            "AI-assisted workflows, not merely know how to chat with an LLM."
        ),
    }


def test_blueprint_accepts_professional_inference_without_evidence_contract() -> None:
    result = RoleCapabilityBlueprint.model_validate(_payload())

    area = result.capability_areas[0]
    assert "Pydantic" in [tool.name for tool in area.likely_tools_or_examples]
    assert area.interpretation_strength == "highly_likely"
    assert result.hidden_requirements[0].title == "Human review boundaries"


def test_blueprint_provider_schema_stays_lightweight() -> None:
    schema = RoleCapabilityBlueprint.model_json_schema()
    serialized = json.dumps(schema, sort_keys=True)

    assert '"minLength"' not in serialized
    assert '"maxLength"' not in serialized
    assert "evidence" not in serialized
    assert "highly_likely" in serialized
    assert "possible_example" in serialized
