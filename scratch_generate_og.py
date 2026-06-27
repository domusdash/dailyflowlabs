import os
import math
from PIL import Image, ImageDraw, ImageFont

COLOR_BG = (3, 3, 3, 255)
COLOR_INDIGO = (99, 102, 241)
COLOR_CYAN = (6, 182, 212)

def get_gradient_color(t):
    r = int(99 + t * (6 - 99))
    g = int(102 + t * (182 - 102))
    b = int(241 + t * (212 - 241))
    return (r, g, b)

def draw_radial_glow(img, center_x, center_y, radius, color_rgb, max_alpha=100):
    # Create a radial gradient overlay
    width, height = img.size
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = overlay.load()
    
    x_min = max(0, int(center_x - radius))
    x_max = min(width, int(center_x + radius))
    y_min = max(0, int(center_y - radius))
    y_max = min(height, int(center_y + radius))
    
    r_sq = radius ** 2
    cr, cg, cb = color_rgb
    
    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            dist_sq = (x - center_x)**2 + (y - center_y)**2
            if dist_sq < r_sq:
                dist = math.sqrt(dist_sq)
                t = dist / radius
                # Smooth cosine decay
                alpha = int(max_alpha * (0.5 * (1 + math.cos(math.pi * t))))
                pixels[x, y] = (cr, cg, cb, alpha)
                
    img.alpha_composite(overlay)

def generate_logo_layer(size):
    scale = 2
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
                
            t = (x + y) / (2.0 * canvas_size)
            t = max(0.0, min(1.0, t))
            r, g, b = get_gradient_color(t)
            
            if in_c1 and in_c2:
                rn, gn, bn = r / 255.0, g / 255.0, b / 255.0
                ro = 2 * rn - rn**2
                go = 2 * gn - gn**2
                bo = 2 * bn - bn**2
                alpha = int((0.85 + 0.85 - 0.85 * 0.85) * 255)
                pixels[x, y] = (int(ro * 255), int(go * 255), int(bo * 255), alpha)
            else:
                pixels[x, y] = (r, g, b, int(0.85 * 255))
                
    return img.resize((size, size), Image.Resampling.LANCZOS)

def main():
    W, H = 1200, 630
    base = Image.new("RGBA", (W, H), COLOR_BG)
    
    # Add floating background glow orbs
    draw_radial_glow(base, 350, 150, 450, COLOR_INDIGO, max_alpha=70)
    draw_radial_glow(base, 850, 450, 400, COLOR_CYAN, max_alpha=60)
    
    draw = ImageDraw.Draw(base)
    
    # Try loading a system font (e.g. Helvetica, Arial, SF Pro, DejaVuSans)
    font_large = None
    font_title = None
    font_sub = None
    font_badge = None
    
    font_paths = [
        "/System/Library/Fonts/SFPro-ExpandedBold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf"
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                font_title = ImageFont.truetype(path, 72)
                font_sub = ImageFont.truetype(path, 28)
                font_badge = ImageFont.truetype(path, 18)
                break
            except Exception:
                pass
                
    if font_title is None:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        
    # Draw Logo Icon
    logo_size = 110
    logo_img = generate_logo_layer(logo_size)
    logo_x = (W - logo_size) // 2
    logo_y = 120
    base.alpha_composite(logo_img, (logo_x, logo_y))
    
    # Draw Title "dailyflowlabs"
    title_text = "dailyflowlabs"
    bbox = draw.textbbox((0, 0), title_text, font=font_title)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    title_x = (W - tw) // 2
    title_y = logo_y + logo_size + 25
    draw.text((title_x, title_y), title_text, fill=(248, 250, 252, 255), font=font_title)
    
    # Draw Subtitle / Tagline
    sub_text = "Software crafted for your daily flow."
    bbox_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
    sw, sh = bbox_sub[2] - bbox_sub[0], bbox_sub[3] - bbox_sub[1]
    sub_x = (W - sw) // 2
    sub_y = title_y + th + 25
    draw.text((sub_x, sub_y), sub_text, fill=(148, 163, 184, 255), font=font_sub)
    
    # Draw Product Badges at the bottom
    products = [
        ("DomusDash", (245, 158, 11)),
        ("IronDial", (14, 165, 233)),
        ("ThumbVerify", (167, 139, 250)),
        ("LocalRedactPDF", (16, 185, 129)),
        ("ShortCodeIcons", (244, 63, 94)),
        ("Blueprint Converter", (56, 189, 248)),
        ("of the world", (255, 42, 95))
    ]
    
    # Calculate widths for centering product badges
    badge_height = 38
    padding_x = 16
    gap = 12
    
    badge_widths = []
    for name, _ in products:
        b_box = draw.textbbox((0, 0), name, font=font_badge)
        bw = (b_box[2] - b_box[0]) + (padding_x * 2)
        badge_widths.append(bw)
        
    total_badge_width = sum(badge_widths) + gap * (len(products) - 1)
    
    # If total width exceeds 1100, split into 2 rows
    row1 = products[:4]
    row2 = products[4:]
    
    def draw_badge_row(prods, start_y):
        row_widths = []
        for name, _ in prods:
            bb = draw.textbbox((0, 0), name, font=font_badge)
            row_widths.append((bb[2] - bb[0]) + padding_x * 2)
        row_total = sum(row_widths) + gap * (len(prods) - 1)
        curr_x = (W - row_total) // 2
        
        for idx, (name, color) in enumerate(prods):
            bw = row_widths[idx]
            # Draw rounded background card
            card_bg = (15, 20, 28, 200)
            draw.rounded_rectangle([curr_x, start_y, curr_x + bw, start_y + badge_height], radius=10, fill=card_bg, outline=(255, 255, 255, 25), width=1)
            
            # Draw colored dot indicator
            dot_r = 4
            dot_x = curr_x + padding_x - 4
            dot_y = start_y + badge_height // 2
            draw.ellipse([dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r], fill=(color[0], color[1], color[2], 255))
            
            # Draw text
            tb = draw.textbbox((0, 0), name, font=font_badge)
            th_b = tb[3] - tb[1]
            text_x = dot_x + dot_r + 8
            text_y = start_y + (badge_height - th_b) // 2 - 2
            draw.text((text_x, text_y), name, fill=(226, 232, 240, 255), font=font_badge)
            
            curr_x += bw + gap

    draw_badge_row(row1, H - 120)
    draw_badge_row(row2, H - 70)
    
    output_path = "/Users/benroberts/Sites/dailyflowlabs/assets/og-cover.png"
    base.convert("RGB").save(output_path, "PNG")
    print("Generated og-cover.png successfully.")

if __name__ == "__main__":
    main()
