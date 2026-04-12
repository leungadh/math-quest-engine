import random

def gen_stars(count):
    """Generates random coordinates for the CSS box-shadow stars."""
    stars = []
    for _ in range(count):
        stars.append(f"{random.randint(0, 8000)}px {random.randint(0, 8000)}px #FFF")
    return ", ".join(stars)

