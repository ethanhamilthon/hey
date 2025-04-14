# HeyAI - Personal AI Assistant in your terminal

Wrapper around the [Gemini](https://aistudio.google.com/) API to create a personal AI assistant in your terminal.
You can get free API key from Gemini and use it to get started.
It uses `gemini-2.0-flash` model to generate responses. All responses will be streamed to your terminal.

## Install locally

```bash
poetry build
pipx install --editable .
```

## Usage

1. Set your Gemini API key as an environment variable:

```bash
export HEY_GEMINI_API_KEY=YOUR_API_KEY
```

2. Start a conversation:

```bash
hey what is the capital of France
```

3. Start a new conversation:

```bash
hey --new what is best package manager for Python
```

Enjoy it ✨
