import random

def gen_stars(count):
    """Generates random coordinates for the CSS box-shadow stars."""
    stars = []
    for _ in range(count):
        stars.append(f"{random.randint(0, 3000)}px {random.randint(0, 3000)}px #FFF")
    return ", ".join(stars)

def get_ui_template():
    """Returns the Interactive Space Quest template with a Space Zoo and Score Tracker."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Space Fraction Quest</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body { background: #090A0F; margin: 0; overflow-x: hidden; color: white; }
            
            /* Background Layers */
            .stars-container {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                z-index: -1; pointer-events: none;
            }
            .star {
                position: absolute; background: transparent; border-radius: 50%;
                animation: move-stars linear infinite;
            }
            .star-sm { width: 1px; height: 1px; animation-duration: 150s; }
            .star-md { width: 2px; height: 2px; animation-duration: 100s; }
            .star-lg { width: 3px; height: 3px; animation-duration: 50s; }

            /* 🦊 Space Zoo Styling */
            .space-animal {
                position: absolute;
                top: 100%;
                z-index: -1;
                opacity: 0.6;
                filter: drop-shadow(0 0 10px rgba(255,255,255,0.2));
            }
            .animal-fast { font-size: 3.5rem; animation: move-stars 18s linear infinite; }
            .animal-mid { font-size: 2.5rem; animation: move-stars 25s linear infinite; }
            .animal-slow { font-size: 2rem; animation: move-stars 35s linear infinite; }

            .warp { animation-duration: 1.5s !important; filter: blur(4px) brightness(2); }

            @keyframes move-stars {
                from { transform: translateY(0) rotate(0deg); }
                to { transform: translateY(-2000px) rotate(20deg); }
            }

            /* Reward Star Animation */
            @keyframes star-pop {
                0% { transform: scale(0) rotate(-45deg); opacity: 0; }
                100% { transform: scale(1) rotate(0deg); opacity: 1; }
            }
            .reward-star { 
                display: none; 
                font-size: 2.5rem; 
                animation: star-pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; 
            }

            details summary::-webkit-details-marker { display:none; }
        </style>
    </head>
    <body class="min-h-screen py-12 px-4 font-sans">
        
        <div class="stars-container">
            <div class="star star-sm" style="box-shadow: {{ stars_css }}"></div>
            <div class="star star-md" style="box-shadow: {{ stars_css_md }}"></div>
            <div class="star star-lg" style="box-shadow: {{ stars_css_lg }}"></div>
            
            <div class="space-animal animal-mid" style="left: 10%;">🐱</div>
            <div class="space-animal animal-fast" style="left: 80%; animation-delay: 5s;">🐶</div>
            <div class="space-animal animal-slow" style="left: 45%; animation-delay: 12s;">🦊</div>
            <div class="space-animal animal-mid" style="left: 65%; animation-delay: 2s;">🐰</div>
            <div class="space-animal animal-fast" style="left: 25%; animation-delay: 8s;">🐹</div>
        </div>

        <div class="relative max-w-2xl mx-auto z-10">
            <header class="text-center mb-12">
                <h1 class="text-5xl font-black text-white tracking-tighter mb-4 italic drop-shadow-[0_5px_15px_rgba(99,102,241,0.5)]">SPACE QUEST</h1>
                
                <div class="inline-flex items-center gap-2 bg-indigo-950/50 border border-indigo-500/50 px-5 py-2 rounded-full mb-8 shadow-lg">
                    <span class="text-xs font-bold uppercase tracking-widest text-indigo-300">Stars Collected:</span>
                    <span id="score" class="text-2xl font-black text-white">0</span>
                    <span class="text-indigo-400">/ {{ missions|length }} ⭐</span>
                </div>

                <div class="flex justify-center gap-4">
                    <a href="/generate" class="bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-2 px-6 rounded-full transition-all text-xs tracking-widest uppercase shadow-lg">🚀 New Mission</a>
                    <button onclick="toggleWarp()" id="warpBtn" class="bg-gray-800/50 border border-indigo-500 hover:bg-indigo-500/20 text-indigo-300 font-bold py-2 px-6 rounded-full transition-all text-xs tracking-widest uppercase">Engage Warp</button>
                </div>
            </header>

            <div id="quest-container">
                {% for entry in missions %}
                {% set mission_id = loop.index %}
                <div class="bg-gray-900/60 backdrop-blur-md border border-indigo-500/30 p-8 rounded-2xl shadow-2xl mb-8">
                    <div class="flex justify-between items-start mb-4">
                        <h2 class="text-indigo-400 font-bold uppercase tracking-tighter text-xs">Mission Log #{{ mission_id }}</h2>
                        <div id="star-{{ mission_id }}" class="reward-star">⭐</div>
                    </div>
                    
                    <p class="text-gray-100 text-xl leading-relaxed mb-8">{{ entry.question }}</p>

                    <div class="grid grid-cols-1 gap-3 mb-8">
                        {% set choices = (entry.distractors + [entry.correct]) | shuffle %}
                        {% for choice in choices %}
                        <button 
                            onclick="checkAnswer(this, '{{ entry.correct }}', 'star-{{ mission_id }}')"
                            class="choice-btn text-left p-4 rounded-xl border border-gray-700 bg-gray-800/40 hover:border-indigo-500 transition-all text-lg">
                            {{ choice }}
                        </button>
                        {% endfor %}
                    </div>

                    <details class="group border-t border-gray-800 pt-4">
                        <summary class="list-none cursor-pointer text-gray-500 hover:text-indigo-300 text-xs font-bold uppercase tracking-widest">🛰️ Access Data Node</summary>
                        <div class="mt-4 bg-indigo-950/20 p-4 rounded-lg border border-indigo-500/20 text-indigo-200 text-sm">
                            {{ entry.explanation }}
                        </div>
                    </details>
                </div>
                {% endfor %}
            </div>
        </div>

        <script>
            let currentScore = 0;

            function toggleWarp() {
                // Includes stars and animals in the warp effect
                const elements = document.querySelectorAll('.star, .space-animal');
                elements.forEach(el => el.classList.toggle('warp'));
                const isWarping = elements[0].classList.contains('warp');
                document.getElementById('warpBtn').innerText = isWarping ? "🛑 Disengage" : "Engage Warp";
            }

            function checkAnswer(btn, correct, starId) {
                const isCorrect = btn.innerText.trim() === correct.trim();
                const star = document.getElementById(starId);
                const siblings = btn.parentElement.querySelectorAll('.choice-btn');

                if (isCorrect) {
                    btn.classList.add('bg-green-600/30', 'border-green-500', 'text-green-100');
                    star.style.display = 'block';
                    currentScore++;
                    document.getElementById('score').innerText = currentScore;
                    siblings.forEach(s => s.onclick = null);
                } else {
                    btn.classList.add('bg-red-600/30', 'border-red-500');
                    setTimeout(() => { btn.classList.remove('bg-red-600/30', 'border-red-500'); }, 1000);
                }
            }
        </script>
    </body>
    </html>
    """
