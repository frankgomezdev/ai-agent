# ai-agent

A small Python CLI agent that takes a natural-language prompt, uses an LLM (via [OpenRouter](https://openrouter.ai)) with function calling, and can list, read, write, and execute Python files inside a sandboxed working directory (`calculator/`).

The bundled `calculator/` app is the sandbox the agent operates on. Point it at a bug or a feature request and let it work.

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- An OpenRouter API key

## Setup

```bash
git clone https://github.com/frankgomezdev/ai-agent.git
cd ai-agent

uv sync

echo "OPENROUTER_API_KEY=your_key_here" > .env
```

## Usage

```bash
uv run main.py "<prompt>" [--verbose]
```

`--verbose` prints each tool call and its result as the agent works.

Examples against the bundled calculator:

```bash
uv run main.py "how does the calculator render its output?"
uv run main.py "add support for exponents" --verbose
uv run main.py "the calculator returns the wrong result for '3 + 7 * 2', fix it"
```

## How it works

`main.py` seeds a `messages` list with the system prompt and the user's prompt, then runs the agent loop:

1. Send `messages` and the tool schemas to the model.
2. If the response contains tool calls, dispatch each through `call_function.call_function`, append the results back into `messages`, and loop.
3. If the response has no tool calls, print the final text answer and exit.

The loop is capped at 20 iterations. If it hits the cap without a final answer, it exits with code 1 and an error.

`call_function.py` is the dispatcher. It holds the four tool schemas passed to the model, looks up the requested function by name in a local `function_map`, and injects the hardcoded `working_directory = "./calculator"` (the model never supplies it). The result comes back wrapped as an OpenAI-style tool message.

## Available tools

Each tool lives in `functions/` and pairs a JSON-Schema declaration with its implementation:

- `get_files_info` — lists a directory's contents (name, size, is-dir) as a formatted string.
- `get_file_content` — reads a file, truncating at `MAX_CHARS` (10,000) with a notice appended.
- `write_file` — writes or overwrites a file, creating parent directories as needed.
- `run_python_file` — runs a `.py` file via `subprocess.run`, optionally with CLI args, returning stdout, stderr, and exit info.

## Sandboxing

All four tools share the same path-validation pattern:

1. Resolve the target to an absolute path.
2. Confirm it lives inside the working directory using `os.path.commonpath`.
3. On anything invalid, return a descriptive `Error: ...` string. Nothing raises past the function boundary, so the agent sees the error as a normal tool result and can react.

That said, `run_python_file` still executes arbitrary code. Only point the agent at directories you're okay with it modifying and running.

## Project structure

```
.
├── main.py                       # entry point, agent loop
├── call_function.py              # tool dispatcher + schemas
├── prompts.py                    # system prompt
├── functions/                    # sandboxed tools (schema + impl)
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── calculator/                   # target app the agent operates on
│   ├── main.py
│   ├── tests.py
│   ├── lorem.txt                 # fixture for truncation tests
│   └── pkg/
│       ├── calculator.py         # arithmetic and parsing
│       ├── render.py             # output formatting
│       └── morelorem.txt         # fixture
├── test_get_files_info.py        # manual test scripts, one per tool
├── test_get_file_content.py
├── test_write_file.py
├── test_run_python_file.py
├── pyproject.toml
└── uv.lock
```

## Tests

The `test_*.py` scripts at the root are standalone manual runners, not a `pytest` suite. Each one imports its tool directly and calls it against `calculator/` with a handful of hardcoded cases (valid path, out of bounds, missing file, etc.), printing results for inspection.

Run any of them directly:

```bash
uv run test_get_files_info.py
```

## Dependencies

- [`openai`](https://pypi.org/project/openai/) (client pointed at OpenRouter's endpoint)
- [`python-dotenv`](https://pypi.org/project/python-dotenv/)