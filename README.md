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
python -m exploring_guardrails.demo
```

## Run every test including the live OpenRouter smoke test

```bash
export OPENROUTER_API_KEY="sk-or-..."
python -m pytest
```

## Promptfoo latency testing

Promptfoo is used to compare OpenRouter responses with and without guardrails.

### Install Promptfoo

```bash
node --version
npm install -g promptfoo
promptfoo --version
```

### Run evaluation

Run from the project root:

```bash
source .venv/bin/activate
pip install -e ".[dev]"
promptfoo eval --no-cache --output results.json
```

Open results UI:

```bash
promptfoo view
```

### Run repeated latency tests

Use multiple runs because model/API latency fluctuates.

```bash
promptfoo eval --no-cache --output results-run-1.json
promptfoo eval --no-cache --output results-run-2.json
promptfoo eval --no-cache --output results-run-3.json
```

### Relevant test scenarios

The committed `promptfoo/payloads.yaml` covers:

```text
Normal safe prompt
PII/email blocking
Competitor mention blocking
JSON response validation
Prompt injection attempt
```


### Calculate added latency

```text
added latency = guarded latency_ms - unguarded latency_ms
```

Compare the `latency_ms` metadata in the result files.

### Common commands

```bash
promptfoo eval --no-cache --output results.json
promptfoo view
```
