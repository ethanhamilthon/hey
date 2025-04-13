# HeyAI - Personal AI Assistant in your terminal

Wrapper around the [Gemini](https://aistudio.google.com/) API to create a personal AI assistant in your terminal.
You can get free API key from Gemini and use it to get started.
It uses `gemini-2.0-flash` model to generate responses. All responses will be streamed to your terminal.

## Usage

To get started, first add your Gemini API key to the environment variable `HEY_GEMINI_API_KEY`.
Add it to your `.bashrc` or `.zshrc` file:

```bash
export HEY_GEMINI_API_KEY=YOUR_API_KEY
```

Just run `hey <prompt>`, for example: `hey how are you`. Everything after the `hey` will be considered the prompt.
Clean the chat with `hey --new`
The history json file can be found in `~/.heyai/history.json`

## Install locally

```bash
poetry build
pipx install --editable .
```

Enjoy it ✨
