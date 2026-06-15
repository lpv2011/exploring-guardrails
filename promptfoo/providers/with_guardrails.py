import time
from dotenv import load_dotenv

from exploring_guardrails.guards import input_guard, multi_output_guard
from exploring_guardrails.openrouter_client import OpenRouterConfig, chat

load_dotenv()
config = OpenRouterConfig.from_env()

def call_api(prompt, options, context):
    start = time.perf_counter()

    try:
        input_guard().validate(prompt)

        output = chat(
            [
                {"role": "system", "content": "Return concise, safe marketing copy."},
                {"role": "user", "content": prompt},
            ],
            config=config,
        )

        multi_output_guard().validate(output)

        status = "allowed"

    except Exception as e:
        output = f"BLOCKED_BY_GUARDRAILS: {str(e)}"
        status = "blocked"

    end = time.perf_counter()

    return {
        "output": output,
        "metadata": {
            "latency_ms": round((end - start) * 1000, 2),
            "guardrails": True,
            "status": status,
        },
    }