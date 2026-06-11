import os

import pytest

from guardrails_openrouter_basic.guards import (
    input_guard,
    json_cleanup_guard,
    multi_output_guard,
    output_guard,
    structured_product_guard,
)
from guardrails_openrouter_basic.openrouter_client import OpenRouterConfig, chat


def test_input_guard_passes_safe_prompt():
    result = input_guard().validate("Write a neutral product summary.")
    assert result.validation_passed is True


def test_input_guard_blocks_email():
    with pytest.raises(Exception):
        input_guard().validate("Use alice@example.com in the answer")


def test_output_guard_blocks_phone_number():
    with pytest.raises(Exception):
        output_guard().validate("Call me at 312-555-0199")


def test_multiple_validators_block_competitor():
    with pytest.raises(Exception):
        multi_output_guard().validate("Our product is better than Globex.")


def test_on_fail_fix_removes_markdown_json_fences():
    result = json_cleanup_guard().validate('```json\n{"ok": true}\n```')
    assert result.validated_output == '{"ok": true}'


def test_structured_pydantic_validation_passes():
    guard = structured_product_guard()
    result = guard.parse('{"product":"Acme Note","summary":"A tidy note app.","sentiment":"positive"}')
    assert result.validation_passed is True
    assert result.validated_output["sentiment"] == "positive"


def test_structured_pydantic_validation_rejects_bad_enum():
    guard = structured_product_guard()
    result = guard.parse('{"product":"Acme Note","summary":"A tidy note app.","sentiment":"ecstatic"}')
    assert result.validation_passed is False


@pytest.mark.live
def test_live_openrouter_free_model_smoke():
    if not os.getenv("OPENROUTER_API_KEY"):
        pytest.skip("OPENROUTER_API_KEY not set")
    content = chat(
        [{"role": "user", "content": "Reply with exactly: guardrails ok"}],
        OpenRouterConfig.from_env(),
    )
    assert "guardrails" in content.lower()
