from __future__ import annotations

import json

from dotenv import load_dotenv

from .guards import input_guard, json_cleanup_guard, multi_output_guard, structured_product_guard
from .openrouter_client import OpenRouterConfig, chat


def main() -> None:
    load_dotenv()
    config = OpenRouterConfig.from_env()

    user_prompt = "Summarize a fictional product named Acme Note in one sentence. Do not include emails or phone numbers."
    input_guard().validate(user_prompt)

    raw = chat([
        {"role": "system", "content": "Return concise, safe marketing copy."},
        {"role": "user", "content": user_prompt},
    ], config=config)
    multi_output_guard().validate(raw)
    print("Safe text output:\n", raw, "\n")

    json_prompt = (
        "Return ONLY JSON with keys product, summary, sentiment. "
        "Use product='Acme Note' and sentiment one of positive, neutral, negative."
    )
    raw_json = chat([
        {"role": "system", "content": "You output strict JSON only."},
        {"role": "user", "content": json_prompt},
    ], config=config)

    cleaned = json_cleanup_guard().validate(raw_json).validated_output
    parsed = structured_product_guard().parse(cleaned)
    print("Structured validated output:\n", json.dumps(parsed.validated_output, indent=2))


if __name__ == "__main__":
    main()
