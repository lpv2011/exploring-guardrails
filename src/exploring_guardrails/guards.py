from __future__ import annotations

from guardrails import Guard
from pydantic import BaseModel, Field

from .validators import EnsureJsonOnly, NoCompetitors, NoSecretOrPII


class ProductSummary(BaseModel):
    product: str = Field(description="Product name")
    summary: str = Field(description="One-sentence product summary")
    sentiment: str = Field(pattern="^(positive|neutral|negative)$")


def input_guard() -> Guard:
    return Guard().use(NoSecretOrPII(on_fail="exception"))


def output_guard() -> Guard:
    return Guard().use(NoSecretOrPII(on_fail="exception"))


def multi_output_guard() -> Guard:
    return Guard().use(
        NoSecretOrPII(on_fail="exception"),
        NoCompetitors(["Contoso", "Globex"], on_fail="exception"),
    )


def json_cleanup_guard() -> Guard:
    return Guard().use(EnsureJsonOnly(on_fail="fix"))


def structured_product_guard() -> Guard:
    return Guard.for_pydantic(ProductSummary)
