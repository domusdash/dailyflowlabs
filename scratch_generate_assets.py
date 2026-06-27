import os
from PIL import Image

# Brand colors
# Indigo: #6366f1 -> (99, 102, 241)
# Cyan: #06b6d4 -> (6, 182, 212)
COLOR_INDIGO = (99, 102, 241)
COLOR_CYAN = (6, 182, 212)

def get_gradient_color(t):
    r = int(99 + t * (6 - 99))
    g = int(102 + t * (182 - 102))
    b = int(241 + t * (212 - 241))
    return (r, g, b)

def generate_logo_image(size):
    # Use 4x supersampling for high-quality anti-aliasing
    scale = 4
    canvas_size = size * scale
    img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    
    c1_x, c1_y = 0.375 * canvas_size, 0.5 * canvas_size
    c2_x, c2_y = 0.625 * canvas_size, 0.5 * canvas_size
    radius = 0.3125 * canvas_size
    r_sq = radius ** 2
    
    pixels = img.load()
    for y in range(canvas_size):
        for x in range(canvas_size):
            d1_sq = (x - c1_x)**2 + (y - c1_y)**2
            d2_sq = (x - c2_x)**2 + (y - c2_y)**2
            in_c1 = d1_sq <= r_sq
            in_c2 = d2_sq <= r_sq
            
            if not in_c1 and not in_c2:
                continue
                
            # Diagonal gradient coordinate from top-left to bottom-right
            t = (x + y) / (2.0 * canvas_size)
            t = max(0.0, min(1.0, t))
            r, g, b = get_gradient_color(t)
            
            if in_c1 and in_c2:
                # Overlap: screen blend mode
                rn, gn, bn = r / 255.0, g / 255.0, b / 255.0
                ro = 2 * rn - rn**2
                go = 2 * gn - gn**2
                bo = 2 * bn - bn**2
                
                # Combined alpha: 0.85 + 0.85 - 0.85*0.85 = 0.9775
                alpha = int((0.85 + 0.85 - 0.85 * 0.85) * 255)
                pixels[x, y] = (int(ro * 255), int(go * 255), int(bo * 255), alpha)
            else:
                # Single circle
                pixels[x, y] = (r, g, b, int(0.85 * 255))
                
    return img.resize((size, size), Image.Resampling.LANCZOS)

def generate_apple_touch_icon(size=180):
    # Apple touch icon has a solid #030303 background, with logo centered
    bg = Image.new("RGBA", (size, size), (3, 3, 3, 255))
    logo_size = int(size * 0.65) # 117px
    logo = generate_logo_image(logo_size)
    
    # Center the logo
    offset = (size - logo_size) // 2
    bg.alpha_composite(logo, (offset, offset))
    # Convert to RGB since apple touch icons don't need alpha
    return bg.convert("RGB")

def main():
    assets_dir = "/Users/benroberts/Sites/dailyflowlabs/assets"
    os.makedirs(assets_dir, exist_ok=True)
    
    print("Generating favicons...")
    # 16x16 PNG
    fav_16 = generate_logo_image(16)
    fav_16.save(os.path.join(assets_dir, "favicon-16x16.png"), "PNG")
    print("Generated favicon-16x16.png")
    
    # 32x32 PNG
    fav_32 = generate_logo_image(32)
    fav_32.save(os.path.join(assets_dir, "favicon-32x32.png"), "PNG")
    print("Generated favicon-32x32.png")
    
    # ICO (multi-resolution: 16x16, 32x32, 48x48)
    fav_48 = generate_logo_image(48)
    root_dir = "/Users/benroberts/Sites/dailyflowlabs"
    fav_32.save(os.path.join(root_dir, "favicon.ico"), format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print("Generated favicon.ico in root")
    
    # Android Chrome icons
    chrome_192 = generate_logo_image(192)
    chrome_192.save(os.path.join(assets_dir, "android-chrome-192x192.png"), "PNG")
    print("Generated android-chrome-192x192.png")
    
    chrome_512 = generate_logo_image(512)
    chrome_512.save(os.path.join(assets_dir, "android-chrome-512x512.png"), "PNG")
    print("Generated android-chrome-512x512.png")
    
    # Apple Touch Icon
    apple_touch = generate_apple_touch_icon(180)
    apple_touch.save(os.path.join(assets_dir, "apple-touch-icon.png"), "PNG")
    print("Generated apple-touch-icon.png")

if __name__ == "__main__":
    main()
