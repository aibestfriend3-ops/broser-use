# Self-Hosting Browser Use with Ollama

This guide explains how to self-host **Browser Use** on your local machine or server using [Ollama](https://ollama.com/) as the local LLM inference provider.

---

## Architecture Overview

When self-hosting locally, Browser Use connects to an Ollama server running locally or inside a Docker container.

```
+-------------------------------------------------------------+
|                        Local Machine                        |
|                                                             |
|   +-----------------------+     +-----------------------+   |
|   |   Browser Use App     |     |     Ollama Server     |   |
|   |  (Python / CLI / Docker) |--->| (localhost:11434)     |   |
|   +-----------+-----------+     +-----------+-----------+   |
|               |                             |               |
|               v                             v               |
|   +-----------------------+     +-----------------------+   |
|   |  Chromium Browser     |     | Local Model Weights   |   |
|   |  (Headless or Local)  |     | (llama3.1, qwen2.5)   |   |
|   +-----------------------+     +-----------------------+   |
+-------------------------------------------------------------+
```

---

## Model Recommendations

Browser agents require strong reasoning and function calling capabilities. Vision capabilities are also highly recommended when web pages need visual understanding (screenshots, canvas elements, complex layouts).

| Model | Size | Vision Support | Notes / Best For |
|---|---|---|---|
| **`qwen2.5:7b`** / **`qwen2.5:14b`** | 4.7GB - 9GB | No | Excellent reasoning and structured output for lightweight local setups. |
| **`llama3.1:8b`** | 4.9GB | No | Fast, general-purpose text model. Good starting point. |
| **`llama3.2-vision:11b`** | 7.9GB | **Yes** | Recommended for visual browser tasks on machines with GPU/Apple Silicon. |
| **`qwen2-vl:7b`** | 4.5GB | **Yes** | Strong open vision-language model for UI element detection. |

---

## Option 1: Docker Compose (Recommended)

Docker Compose sets up both Ollama and Browser Use in isolated containers.

### 1. Start Services

```bash
docker compose up -d
```

### 2. Pull an LLM Model into Ollama

Before running agent tasks, pull your preferred model:

```bash
docker exec -it browser-use-ollama ollama pull llama3.1:8b
# Or for vision capabilities:
# docker exec -it browser-use-ollama ollama pull llama3.2-vision:11b
```

### 3. Run Browser Use via CLI in Docker

```bash
docker exec -it browser-use-app browser-use --help
```

---

## Option 2: Native Python Setup

If you prefer running Python code directly on your host machine:

### 1. Install & Start Ollama

1. Download and install Ollama from [ollama.com](https://ollama.com/).
2. Start the Ollama server:
   ```bash
   ollama serve
   ```
3. Pull the required model in a new terminal:
   ```bash
   ollama pull llama3.1:8b
   ```

### 2. Set Up Python Environment

Using `uv` (recommended):

```bash
# Clone the repository and navigate into it
git clone https://github.com/browser-use/browser-use.git
cd browser-use

# Setup virtual environment and install dependencies
uv venv --python 3.11
source .venv/bin/activate
uv sync
```

### 3. Run Python Script

Create or run `examples/models/ollama_self_hosted.py`:

```python
import asyncio
from browser_use import Agent, ChatOllama

async def main():
	# Connect to local Ollama instance
	llm = ChatOllama(
		model='llama3.1:8b',
		num_ctx=32768,  # Larger context window recommended for web pages
	)

	agent = Agent(
		task='Go to https://news.ycombinator.com and give me the top headline',
		llm=llm,
	)

	result = await agent.run()
	print(result.final_result())

if __name__ == '__main__':
	asyncio.run(main())
```

Execute:

```bash
uv run python examples/models/ollama_self_hosted.py
```

---

## Option 3: Browser Use CLI with Ollama

You can also use the `browser-use` CLI directly with Ollama.

```bash
# Specify model provider and model name
uv run browser-use --llm-provider ollama --llm-model llama3.1:8b "Search for recent news on AI"
```

---

## Tips & Troubleshooting

1. **Context Window Length (`num_ctx`):** Web page DOMs and agent action histories can be large. Increasing `num_ctx` (e.g., to 16384 or 32768) in `ChatOllama` helps prevent context trimming.
2. **GPU Acceleration:** When running Docker on Linux, pass GPU flags (`--gpus all`) to the `ollama` container service in `docker-compose.yml` for faster inference times.
3. **Vision Models:** If your task requires clicking specific visual targets or interpreting dynamic web elements, use vision models like `llama3.2-vision:11b` or `qwen2-vl:7b`.
