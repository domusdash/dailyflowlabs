import os
import json
from PIL import Image

def validate():
    root = "/Users/benroberts/Sites/dailyflowlabs"
    
    # Files to check
    files_to_check = [
        "favicon.ico",
        "site.webmanifest",
        "assets/logo.svg",
        "assets/favicon.svg",
        "assets/favicon-16x16.png",
        "assets/favicon-32x32.png",
        "assets/apple-touch-icon.png",
        "assets/android-chrome-192x192.png",
        "assets/android-chrome-512x512.png",
        "assets/og-cover.png"
    ]
    
    print("=== File Existence & Size Check ===")
    for f in files_to_check:
        p = os.path.join(root, f)
        if not os.path.exists(p):
            raise FileNotFoundError(f"Missing file: {f}")
        size = os.path.getsize(p)
        print(f"[OK] {f} ({size} bytes)")
        
    print("\n=== Image Dimensions Check ===")
    dims = {
        "assets/favicon-16x16.png": (16, 16),
        "assets/favicon-32x32.png": (32, 32),
        "assets/apple-touch-icon.png": (180, 180),
        "assets/android-chrome-192x192.png": (192, 192),
        "assets/android-chrome-512x512.png": (512, 512),
        "assets/og-cover.png": (1200, 630)
    }
    for rel_path, expected in dims.items():
        p = os.path.join(root, rel_path)
        with Image.open(p) as img:
            if img.size != expected:
                raise ValueError(f"Dimension mismatch for {rel_path}: expected {expected}, got {img.size}")
            print(f"[OK] {rel_path} dimensions: {img.size}")
            
    print("\n=== Manifest Validation ===")
    with open(os.path.join(root, "site.webmanifest")) as f:
        data = json.load(f)
        if "name" not in data or "icons" not in data:
            raise ValueError("Invalid manifest format")
        print(f"[OK] site.webmanifest validated: App name '{data['name']}'")
        
    print("\nALL VALIDATIONS PASSED PERFECTLY!")

if __name__ == "__main__":
    validate()
