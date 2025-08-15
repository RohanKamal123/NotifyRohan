"""
Asset creation script for Notify Rohan
Generates required icons and images for the application
"""

import os
from PIL import Image, ImageDraw, ImageFont
import json
from datetime import datetime

def create_directory_structure():
    """Create the assets directory structure"""
    directories = [
        'assets',
        'assets/icons',
        'assets/images',
        'data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def create_app_icon(size=512):
    """Create the main application icon"""
    # Create a new image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define colors
    primary_color = (33, 150, 243, 255)  # Material Blue
    accent_color = (255, 193, 7, 255)    # Material Amber
    white = (255, 255, 255, 255)
    
    # Draw main circle background
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], fill=primary_color)
    
    # Draw bell icon (simplified)
    bell_margin = size // 4
    bell_width = size - (bell_margin * 2)
    bell_height = int(bell_width * 0.8)
    
    # Bell body
    bell_top = int(bell_margin + bell_height * 0.2)
    bell_bottom = bell_margin + bell_height
    bell_left = int(bell_margin + bell_width * 0.2)
    bell_right = int(bell_margin + bell_width * 0.8)
    
    # Draw bell shape
    points = [
        (bell_left, bell_bottom),
        (bell_left, int(bell_top + bell_height * 0.3)),
        (int(bell_left + bell_width * 0.1), bell_top),
        (int(bell_right - bell_width * 0.1), bell_top),
        (bell_right, int(bell_top + bell_height * 0.3)),
        (bell_right, bell_bottom)
    ]
    draw.polygon(points, fill=white)
    
    # Bell handle/top
    handle_width = int(bell_width * 0.15)
    handle_height = int(bell_height * 0.2)
    handle_x = size // 2 - handle_width // 2
    handle_y = bell_margin
    draw.rectangle([handle_x, handle_y, handle_x + handle_width, handle_y + handle_height], fill=white)
    
    # Notification dot
    dot_size = size // 8
    dot_x = size - margin - dot_size // 2
    dot_y = margin + dot_size // 2
    draw.ellipse([dot_x - dot_size//2, dot_y - dot_size//2, dot_x + dot_size//2, dot_y + dot_size//2], fill=accent_color)
    
    return img

def create_presplash(size=(512, 512)):
    """Create the presplash screen image"""
    img = Image.new('RGB', size, (33, 150, 243))  # Material Blue background
    draw = ImageDraw.Draw(img)
    
    # Create centered icon
    icon_size = min(size) // 3
    icon = create_app_icon(icon_size)
    
    # Paste icon in center
    x = (size[0] - icon_size) // 2
    y = (size[1] - icon_size) // 2
    img.paste(icon, (x, y), icon)
    
    # Add app name text
    try:
        # Try to use a nice font, fall back to default if not available
        font_size = size[1] // 20
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except OSError:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
            except OSError:
                font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()
    
    text = "Notify Rohan"
    
    # Get text dimensions using textbbox
    try:
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
    except AttributeError:
        # Fallback for older PIL versions
        text_width, text_height = draw.textsize(text, font=font)
    
    text_x = (size[0] - text_width) // 2
    text_y = y + icon_size + size[1] // 20
    
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
    
    return img

def create_notification_icons():
    """Create various notification state icons"""
    icons = {
        'bell': create_bell_icon(),
        'bell_ring': create_bell_ring_icon(),
        'check': create_check_icon(),
        'warning': create_warning_icon(),
    }
    
    return icons

def create_bell_icon(size=128):
    """Create a bell icon"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color = (97, 97, 97, 255)  # Gray color
    
    # Bell shape
    margin = size // 6
    bell_width = size - (margin * 2)
    bell_height = int(bell_width * 0.8)
    
    bell_top = int(margin + bell_height * 0.2)
    bell_bottom = margin + bell_height
    bell_left = int(margin + bell_width * 0.2)
    bell_right = int(margin + bell_width * 0.8)
    
    points = [
        (bell_left, bell_bottom),
        (bell_left, int(bell_top + bell_height * 0.3)),
        (int(bell_left + bell_width * 0.1), bell_top),
        (int(bell_right - bell_width * 0.1), bell_top),
        (bell_right, int(bell_top + bell_height * 0.3)),
        (bell_right, bell_bottom)
    ]
    draw.polygon(points, fill=color)
    
    return img

def create_bell_ring_icon(size=128):
    """Create a ringing bell icon"""
    img = create_bell_icon(size)
    draw = ImageDraw.Draw(img)
    
    # Add ring lines
    color = (255, 193, 7, 255)  # Amber
    line_width = max(1, size // 32)
    
    # Left ring lines
    for i in range(3):
        x = size // 8 - (i * size // 16)
        y1 = size // 3 + (i * size // 16)
        y2 = y1 + size // 8
        draw.line([(x, y1), (x, y2)], fill=color, width=line_width)
    
    # Right ring lines  
    for i in range(3):
        x = size - size // 8 + (i * size // 16)
        y1 = size // 3 + (i * size // 16)
        y2 = y1 + size // 8
        draw.line([(x, y1), (x, y2)], fill=color, width=line_width)
    
    return img

def create_check_icon(size=128):
    """Create a checkmark icon"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Green circle background
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], fill=(76, 175, 80, 255))
    
    # White checkmark
    line_width = max(1, size // 16)
    check_points = [
        (int(size * 0.3), int(size * 0.5)),
        (int(size * 0.45), int(size * 0.65)),
        (int(size * 0.7), int(size * 0.35))
    ]
    
    # Draw checkmark lines
    draw.line([check_points[0], check_points[1]], fill=(255, 255, 255), width=line_width)
    draw.line([check_points[1], check_points[2]], fill=(255, 255, 255), width=line_width)
    
    return img

def create_warning_icon(size=128):
    """Create a warning icon"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Orange triangle background
    color = (255, 152, 0, 255)  # Orange
    margin = size // 8
    
    # Triangle points
    top = (size // 2, margin)
    bottom_left = (margin, size - margin)
    bottom_right = (size - margin, size - margin)
    
    draw.polygon([top, bottom_left, bottom_right], fill=color)
    
    # White exclamation mark
    exc_width = max(1, size // 16)
    exc_height = size // 3
    exc_x = size // 2 - exc_width // 2
    exc_y = size // 3
    
    # Exclamation line
    draw.rectangle([exc_x, exc_y, exc_x + exc_width, exc_y + exc_height], fill=(255, 255, 255))
    
    # Exclamation dot
    dot_size = exc_width
    dot_y = exc_y + exc_height + size // 20
    draw.ellipse([exc_x, dot_y, exc_x + dot_size, dot_y + dot_size], fill=(255, 255, 255))
    
    return img

def save_icons_multiple_sizes(base_icon, name, sizes=[16, 24, 32, 48, 64, 128, 256, 512]):
    """Save icon in multiple sizes"""
    for size in sizes:
        resized = base_icon.resize((size, size), Image.Resampling.LANCZOS)
        filename = f"assets/icons/{name}_{size}.png"
        resized.save(filename)
        print(f"Created: {filename}")

def create_sample_data():
    """Create sample notification data"""
    sample_notifications = [
        {
            "id": "sample-1",
            "title": "Welcome to Notify Rohan!",
            "description": "This is your first notification. Tap to edit or delete it.",
            "datetime": (datetime.now() + datetime.timedelta(hours=2)).isoformat(),
            "created_at": datetime.now().isoformat()
        },
        {
            "id": "sample-2", 
            "title": "Meeting with Team",
            "description": "Discuss project progress and next milestones",
            "datetime": (datetime.now() + datetime.timedelta(days=1)).isoformat(),
            "created_at": datetime.now().isoformat()
        },
        {
            "id": "sample-3",
            "title": "Grocery Shopping",
            "description": "Buy milk, bread, eggs, and vegetables",
            "datetime": (datetime.now() + datetime.timedelta(days=2, hours=3)).isoformat(),
            "created_at": datetime.now().isoformat()
        }
    ]
    
    # Only create if file doesn't exist to avoid overwriting user data
    notifications_file = 'data/notifications.json'
    if not os.path.exists(notifications_file):
        with open(notifications_file, 'w') as f:
            json.dump(sample_notifications, f, indent=2)
        print("Created sample notifications data")
    else:
        print("Notifications file already exists, skipping sample data creation")

def create_default_settings():
    """Create default settings file"""
    default_settings = {
        "theme_style": "Light",
        "primary_palette": "Blue", 
        "accent_palette": "Amber",
        "font_size": "Medium",
        "notifications_enabled": True,
        "auto_save": True,
        "last_updated": datetime.now().isoformat()
    }
    
    # Only create if file doesn't exist to avoid overwriting user settings
    settings_file = 'data/settings.json'
    if not os.path.exists(settings_file):
        with open(settings_file, 'w') as f:
            json.dump(default_settings, f, indent=2)
        print("Created default settings")
    else:
        print("Settings file already exists, skipping default settings creation")

def main():
    """Main function to create all assets"""
    print("Creating Notify Rohan assets...")
    
    # Create directory structure
    create_directory_structure()
    
    # Create main app icon
    print("\nCreating app icons...")
    main_icon = create_app_icon(512)
    save_icons_multiple_sizes(main_icon, "icon")
    
    # Save main sizes specifically needed
    main_icon.save("assets/icon.png")
    main_icon.resize((72, 72), Image.Resampling.LANCZOS).save("assets/icon_72.png")
    main_icon.resize((96, 96), Image.Resampling.LANCZOS).save("assets/icon_96.png")
    main_icon.resize((144, 144), Image.Resampling.LANCZOS).save("assets/icon_144.png")
    main_icon.resize((192, 192), Image.Resampling.LANCZOS).save("assets/icon_192.png")
    
    # Create presplash
    print("\nCreating presplash...")
    presplash = create_presplash()
    presplash.save("assets/presplash.png")
    
    # Create notification state icons
    print("\nCreating notification icons...")
    notification_icons = create_notification_icons()
    
    for name, icon in notification_icons.items():
        save_icons_multiple_sizes(icon, name, sizes=[24, 32, 48, 64])
    
    # Create sample data
    print("\nCreating sample data...")
    create_sample_data()
    create_default_settings()
    
    print("\n✅ All assets created successfully!")
    print("\nGenerated files:")
    print("- assets/icon.png (main app icon)")
    print("- assets/presplash.png (startup screen)")
    print("- assets/icons/ (various icon sizes)")
    print("- data/notifications.json (sample data)")
    print("- data/settings.json (default settings)")

if __name__ == "__main__":
    main()