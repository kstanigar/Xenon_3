
from PIL import Image
import os

input_path = "Alien fleet with futuristic designs.png"
output_path = "Alien fleet with futuristic designs_optimized.png"

try:
    with Image.open(input_path) as img:
        # Resize if overly large (e.g. > 2048px wide)
        if img.width > 2048:
             ratio = 2048 / img.width
             new_height = int(img.height * ratio)
             img = img.resize((2048, new_height), Image.Resampling.LANCZOS)
        
        # Save with optimization
        # PNG optimization in PIL is limited, but we can try optimize=True
        # Or convert to WebP? Browser support is good.
        # Let's try to save as PNG first with optimize=True to be safe compatibility-wise, 
        # or maybe just quality reduction if it was a JPEG (but it's PNG).
        # Actually, if it's a photo-like image, WebP or JPEG is better.
        # If it has transparency, WebP or PNG.
        
        # Let's try saving as WebP for max compression
        output_webp = "Alien fleet with futuristic designs.webp"
        img.save(output_webp, "WEBP", quality=80)
        
        print(f"Compressed to {output_webp}")
        
except Exception as e:
    print(f"Error: {e}")
