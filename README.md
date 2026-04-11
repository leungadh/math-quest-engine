# # Math Quest Engine 🚀

A containerized Python engine that leverages **Kimi (Moonshot AI)** to generate immersive 5th-grade math word problems. This version features a high-fidelity "Space Quest" web interface with interactive solutions and a parallax star field.

## 📖 Overview

The Math Quest Engine automates the creation of educational materials using modern infrastructure patterns.
* **Engine:** Python 3.12 + Moonshot AI (`v1-8k`).
* **UI:** Tailwind CSS + Parallax Star Field + Native HTML Reveal.
* **Deployment:** Fully Dockerized for environment parity.

## ✨ New Features
* **Interactive Web UI:** Generates a styled `index.html` mission log.
* **Warp Drive:** Integrated JavaScript toggle for high-speed star animations.
* **Secure Solutions:** Native `<details>` tags for "click-to-reveal" answers.

---

## 🖥️ Usage (via Docker)

The easiest way to run the engine is using Docker. This ensures all dependencies (like `random` and `webbrowser` logic) are handled correctly.

```bash
# 1. Build the image
docker build -t math-quest-engine .

# 2. Run the mission (mounts the output folder to your Mac)
docker run --env-file .env -v $(pwd)/output:/app/output math-quest-engine
