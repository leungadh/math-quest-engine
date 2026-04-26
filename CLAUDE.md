# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the dev server (port 5001)
python app.py

# Install/sync dependencies
pip install -r requirements.txt
```

The app runs at `http://localhost:5001`. Port 5001 is intentional — avoids macOS AirPlay conflicts.

Set `FLASK_DEBUG=true` in `.env` to enable Flask debug mode.

## Architecture

This is a minimal 3-file Flask app:

- **`engine.py`** — All AI logic. Calls Moonshot AI (Kimi) via the OpenAI-compatible SDK (`moonshot-v1-8k` model) to generate 5 fraction word problems. Results are cached to `output/quest_data.json`. On load, `get_current_missions()` validates the cache against `_is_valid_mission()` and re-fetches only if invalid or missing.

- **`app.py`** — Flask routes. Two routes: `/` renders missions, `/generate` triggers a fresh AI fetch then redirects home. Registers a custom `shuffle` Jinja2 filter used in the template to randomize answer choices on every page load.

- **`templates/index.html`** — Single-page UI. Jinja2 renders all missions server-side. Client-side JS (`checkAnswer`, `toggleWarp`) handles score tracking and the warp animation — no AJAX, no state server-side after initial render.

- **`templates.py`** — Generates CSS `box-shadow` strings for the 3-layer parallax starfield (400/150/50 dots passed as template variables).

## Data shape

Each mission in `quest_data.json` / returned by the AI must have:
```json
{ "question": "...", "correct": "...", "distractors": ["...", "...", "..."], "explanation": "..." }
```
`_is_valid_mission()` in `engine.py` enforces this schema before using cached data.

## Environment

Requires `ANTHROPIC_API_KEY` in `.env`. The key is loaded via `python-dotenv`.
