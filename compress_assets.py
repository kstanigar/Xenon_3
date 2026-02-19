
from PIL import Image
import os

# List of used assets based on game_mobile.html
assets = [
    "player.png",
    "enemy.png",
    "enemy2.png",
    "enemy3.png",
    "enemy4.png",
    "Boss.png",
    "enemy1_Red.png",
    "enemy2_Red.png",
    "enemy3_Red.png",
    "enemy4_Red.png",
    "boss_Red.png",
    "enemy1_purple.png",
    "enemy2_purple.png",
    "enemy3_purple.png",
    "enemy4_purple.png",
    "boss_purple.png"
]

total_savings = 0

for filename in assets:
    if os.path.exists(filename):
        try:
            with Image.open(filename) as img:
                webp_filename = os.path.splitext(filename)[0] + ".webp"
                # Save as WebP with quality 85 (good balance)
                img.save(webp_filename, "WEBP", quality=85)
                
                original_size = os.path.getsize(filename)
                new_size = os.path.getsize(webp_filename)
                savings = original_size - new_size
                total_savings += savings
                
                print(f"Compressed {filename}: {original_size/1024:.1f}KB -> {new_size/1024:.1f}KB")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    else:
        print(f"Warning: {filename} not found")

print(f"Total savings: {total_savings/1024:.1f}KB")
