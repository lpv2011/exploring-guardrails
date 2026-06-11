from __future__ import annotations

import re
from typing import Dict, Iterable, Optional

from guardrails.validators import FailResult, PassResult, ValidationResult, Validator, register_validator


@register_validator(name="no-secret-or-pii", data_type="string")
class NoSecretOrPII(Validator):
    """Reject common secrets and PII-like patterns."""

    PATTERNS = {
        "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
        "phone": re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
        "api_key": re.compile(r"\b(?:sk|pk|api|key)[-_]?[A-Za-z0-9]{12,}\b", re.I),
    }

    def __init__(self, on_fail: Optional[object] = None):
        super().__init__(on_fail=on_fail)

    def _validate(self, value: str, metadata: Dict) -> ValidationResult:
        hits = [name for name, pattern in self.PATTERNS.items() if pattern.search(value or "")]
        if hits:
            return FailResult(error_message=f"Detected prohibited content: {', '.join(hits)}")
        return PassResult()


@register_validator(name="no-competitors", data_type="string")
class NoCompetitors(Validator):
    """Reject explicit competitor mentions."""

    def __init__(self, competitors: Iterable[str], on_fail: Optional[object] = None):
        super().__init__(on_fail=on_fail, competitors=list(competitors))
        self.competitors = [c.lower() for c in competitors]

    def _validate(self, value: str, metadata: Dict) -> ValidationResult:
        lowered = (value or "").lower()
        found = [c for c in self.competitors if c in lowered]
        if found:
            return FailResult(error_message=f"Competitor mentions are not allowed: {', '.join(found)}")
        return PassResult()


@register_validator(name="ensure-json-only", data_type="string")
class EnsureJsonOnly(Validator):
    """Programmatically fixes fenced JSON output into bare JSON text."""

    def __init__(self, on_fail: Optional[object] = "fix"):
        super().__init__(on_fail=on_fail)

    def _validate(self, value: str, metadata: Dict) -> ValidationResult:
        text = (value or "").strip()
        if text.startswith("```"):
            fixed = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.I | re.S).strip()
            return FailResult(error_message="Output should not be wrapped in markdown fences", fix_value=fixed)
        return PassResult()
