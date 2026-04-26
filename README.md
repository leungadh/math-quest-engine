
# Math Quest Engine

![Space Fraction Quest Preview](images/SpaceFractionQuest.png)

An interactive, web-based math learning platform designed for 5th-grade students. It uses **Anthropic Claude** to dynamically generate fraction word problems set in everyday daily life scenarios — cooking, shopping, sports, gardening, and more.

## ✨ Features
* **AI-Powered Problems:** Uses Claude Haiku to generate grade-appropriate fraction problems (addition, subtraction, multiplication, and division) with daily life themes.
* **Interactive UI:** Multiple-choice questions with real-time feedback and a star collection score tracker.
* **Congratulations Screen:** Firework burst animation and overlay when all problems are answered correctly.
* **Space Zoo Background:** A custom CSS-animated starfield featuring a drifting crew of animals (🐱, 🐶, 🦊, 🐰, 🐹).
* **Warp Drive Mode:** A high-speed visual effect that accelerates the background for a warp speed experience.
* **Mobile-Ready:** Built with Tailwind CSS for a fully responsive layout.

---

## 📂 Project Structure

```text
math-quest-engine/
├── app.py              # Flask routes & Jinja2 filter registration
├── engine.py           # Claude AI integration, prompt logic, & data persistence
├── templates.py        # Generates CSS starfield box-shadow strings
├── templates/
│   └── index.html      # Single-page UI (Jinja2 + vanilla JS)
├── .env                # API keys (ANTHROPIC_API_KEY)
├── .venv/              # Python virtual environment
└── output/
    └── quest_data.json # Locally cached AI-generated problems
```

---

## 🛠️ Getting Started

### 1. Prerequisites
* Python 3.10+
* An [Anthropic API key](https://console.anthropic.com/)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/leungadh/math-quest-engine.git
cd math-quest-engine

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 4. Run the App
```bash
python app.py
```
Open your browser and navigate to `http://localhost:5001`.

---

## 🧠 Technical Highlights
* **Dynamic Shuffling:** Uses a custom Flask/Jinja2 filter to scramble multiple-choice options on every page load.
* **Prompt Constraints:** The AI prompt enforces fraction-only answers, restricted denominators (2, 3, 4, 5, 6, 8, 10), and plausible distractors based on common procedural errors.
* **Cache Validation:** `engine.py` validates the cached JSON schema on startup and only re-fetches from the API when the data is missing or malformed.
* **State Management:** Client-side JavaScript handles score tracking and animations — no server round-trips after initial render.

---

## 📜 License
MIT License - Feel free to use this for your own kids or classrooms!
