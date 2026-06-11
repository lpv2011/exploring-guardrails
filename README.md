# Guardrails AI + OpenRouter basic feature test project

This project exercises the basic Guardrails AI features shown in the current docs:

- input guard validation before an LLM call
- output guard validation after an LLM call
- multiple validators in one guard
- custom validators
- `on_fail="fix"` auto-repair behavior
- Pydantic structured-output validation
- optional live OpenRouter call using the free model router: `openrouter/free`

Guardrails says its Python framework runs input/output guards and helps generate structured data. OpenRouter’s API is OpenAI-compatible and exposes `https://openrouter.ai/api/v1/chat/completions`; `openrouter/free` routes to currently available free models.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# edit .env and add your OpenRouter API key
```

## Run the demo against OpenRouter free router

```bash
export OPENROUTER_API_KEY="sk-or-..."
python -m exploring-guardrails.demo
```

## Run every test including the live OpenRouter smoke test

```bash
export OPENROUTER_API_KEY="sk-or-..."
pytest
```

The live test is intentionally small so you can verify integration without spending paid credits. OpenRouter still requires an API key/account for authentication.
