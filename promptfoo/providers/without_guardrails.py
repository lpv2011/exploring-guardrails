import time
from dotenv import load_dotenv

from exploring_guardrails.openrouter_client import OpenRouterConfig, chat

load_dotenv()
config = OpenRouterConfig.from_env()

def call_api(prompt, options, context):
    start = time.perf_counter()

    output = chat(
        [
            {"role": "system", "content": "Return concise, safe marketing copy."},
            {"role": "user", "content": prompt},
        ],
        config=config,
    )

    end = time.perf_counter()

    return {
        "output": output,
        "metadata": {
            "latency_ms": round((end - start) * 1000, 2),
            "guardrails": False,
        },
    }