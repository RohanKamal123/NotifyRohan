"""
Notify Rohan - Full Self-Contained Main Application Entry Point
A professional KivyMD notification management application
"""

import os
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFloatingActionButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.material_resources import dp
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock

from kivy.uix.screenmanager import SlideTransition, FadeTransition

# Load KV string (from notify.kv document)
kv_string = """
#:kivy 2.0

<NotifyRohanApp>:
    
    primary_palette: "Blue"
    primary_hue: "600"
    accent_palette: "Amber"
    theme_style: "Light"

# Enhanced Material Design Components

<CustomMDCard@MDCard>:
    elevation: 3
    radius: [12, 12, 12, 12]
    md_bg_color: app.theme_cls.surfaceColor
    ripple_behavior: True
    
<CustomMDButton@MDRaisedButton>:
    elevation: 2
    radius: [8, 8, 8, 8]
    
<CustomMDTextField@MDTextField>:
    mode: "outlined"
    radius: [8, 8, 8, 8]
    
# Animation definitions for screen transitions
<MDScreenManager>:
    transition: 
        SlideTransition(direction='left', duration=0.3)

# Custom List Item for notifications
<NotificationListItem@MDListItem>:
    theme_text_color: "Primary"
    radius: 8
    height: dp(80)
    
    IconLeftWidget:
        icon: "bell-outline"
        theme_icon_color: "Primary"
    
    IconRightWidget:
        icon: "chevron-right"
        theme_icon_color: "Secondary"

# Floating Action Button with enhanced styling
<CustomFAB@MDFloatingActionButton>:
    md_bg_color: app.theme_cls.primary_color
    elevation: 8
    
# Enhanced Toolbar
<CustomToolbar@MDTopAppBar>:
    elevation: 4
    left_action_items: []
    right_action_items: []
    md_bg_color: app.theme_cls.primary_color

# Dialog styling
<CustomDialog@MDDialog>:
    radius: [16, 16, 16, 16]
    elevation: 8

# Snackbar styling  
<CustomSnackbar@MDSnackbar>:
    radius: [8, 8, 8, 8]
    elevation: 6
    
# Search field styling
<SearchField@MDTextField>:
    mode: "outlined"
    hint_text: "Search notifications..."
    icon_left: "magnify"
    radius: [12, 12, 12, 12]
    size_hint_y: None
    height: dp(48)

# Settings card styling
<SettingsCard@MDCard>:
    elevation: 2
    radius: [12, 12, 12, 12]
    md_bg_color: app.theme_cls.surfaceColor
    padding: dp(16)
    size_hint_y: None
    
# Date/Time picker button styling
<DateTimeButton@MDRaisedButton>:
    radius: [8, 8, 8, 8]
    elevation: 2
    md_bg_color: app.theme_cls.surfaceColor
    theme_text_color: "Primary"

# Enhanced switch styling
<CustomSwitch@MDSwitch>:
    width: dp(48)
    active_color: app.theme_cls.primary_color
    
# Icon button with enhanced ripple
<CustomIconButton@MDIconButton>:
    theme_icon_color: "Primary"
    ripple_scale: 2.0

# Progress indicator
<CustomProgressBar@MDProgressBar>:
    color: app.theme_cls.primary_color
    
# Divider styling
<CustomDivider@MDDivider>:
    color: app.theme_cls.dividerColor
    height: dp(1)

# Enhanced card for empty states
<EmptyStateCard@MDCard>:
    elevation: 1
    radius: [16, 16, 16, 16]
    md_bg_color: app.theme_cls.surfaceColor
    padding: dp(24)
    size_hint_y: None
    height: dp(120)
    
# Loading spinner
<LoadingSpinner@MDSpinner>:
    size_hint: None, None
    size: dp(32), dp(32)
    color: app.theme_cls.primary_color
    
# Enhanced menu styling
<CustomMenu@MDDropdownMenu>:
    radius: [8, 8, 8, 8]
    elevation: 8
    
# Form section styling
<FormSection@MDBoxLayout>:
    orientation: "vertical"
    spacing: dp(12)
    padding: [0, dp(8)]
    
# Action button row
<ActionButtonRow@MDBoxLayout>:
    orientation: "horizontal" 
    spacing: dp(12)
    size_hint_y: None
    height: dp(48)
    padding: [dp(16), 0]
    
# Stats card styling
<StatsCard@MDCard>:
    elevation: 3
    radius: [12, 12, 12, 12]
    md_bg_color: app.theme_cls.surfaceColor
    padding: dp(16)
    size_hint_y: None
    height: dp(100)
    
# Error text styling
<ErrorText@MDLabel>:
    theme_text_color: "Error"
    font_style: "Caption"
    
# Success text styling  
<SuccessText@MDLabel>:
    theme_text_color: "Primary"
    font_style: "Caption"
    
# Section header styling
<SectionHeader@MDLabel>:
    font_style: "H6"
    theme_text_color: "Primary"
    size_hint_y: None
    height: dp(32)
    
# Subtitle text styling
<SubtitleText@MDLabel>:
    font_style: "Subtitle1"
    theme_text_color: "Secondary"
    
# Body text styling
<BodyText@MDLabel>:
    font_style: "Body1"
    theme_text_color: "Primary"
    text_size: self.width, None
    
# Caption text styling
<CaptionText@MDLabel>:
    font_style: "Caption"
    theme_text_color: "Hint"
    
# Notification status indicators
<OverdueIndicator@MDIcon>:
    icon: "clock-alert"
    theme_icon_color: "Error"
    
<UpcomingIndicator@MDIcon>:
    icon: "clock-outline"  
    theme_icon_color: "Primary"
    
<CompletedIndicator@MDIcon>:
    icon: "check-circle"
    theme_icon_color: "Custom"
    theme_icon_color_custom: "#4CAF50"

# Spacing helpers
<SmallSpacer@Widget>:
    size_hint_y: None
    height: dp(8)
    
<MediumSpacer@Widget>:
    size_hint_y: None
    height: dp(16)
    
<LargeSpacer@Widget>:
    size_hint_y: None
    height: dp(24)

# Container layouts
<ScrollContainer@MDScrollView>:
    do_scroll_x: False
    do_scroll_y: True
    scroll_type: ['bars']
    bar_width: dp(4)
    bar_color: app.theme_cls.primary_color
    
<ContentContainer@MDBoxLayout>:
    orientation: "vertical"
    spacing: dp(16)
    padding: dp(16)
    size_hint_y: None
    adaptive_height: True
    
# Enhanced ripple effects
<RippleCard@MDCard>:
    ripple_behavior: True
    ripple_color: app.theme_cls.primary_color
    ripple_alpha: 0.2
    
# Animated elements
<AnimatedButton@MDRaisedButton>:
    elevation: 2
    on_press: 
        Animation(elevation=6, duration=0.1).start(self)
    on_release:
        Animation(elevation=2, duration=0.1).start(self)
        
<AnimatedFAB@MDFloatingActionButton>:
    elevation: 8
    on_press:
        Animation(elevation=12, duration=0.1).start(self)
    on_release:
        Animation(elevation=8, duration=0.1).start(self)

# Theme-aware colors
<ThemeCard@MDCard>:
    md_bg_color: app.theme_cls.surfaceColor if app.theme_cls.theme_style == "Light" else app.theme_cls.bg_dark
    
<ThemeLabel@MDLabel>:
    theme_text_color: "Primary" if app.theme_cls.theme_style == "Light" else "Primary"
    
# Responsive sizing
<ResponsiveCard@MDCard>:
    size_hint_x: 1 if root.width < dp(600) else 0.8
    pos_hint: {"center_x": 0.5} if root.width >= dp(600) else {}
    
# Custom transitions
<FadeTransition@FadeTransition>:
    duration: 0.3
    
<SlideTransition@SlideTransition>:
    duration: 0.3
"""

Builder.load_string(kv_string)

# Additional KV string from screens.py for NotificationCard and SearchBar
additional_kv = """
<NotificationCard>:
    elevation: 2
    radius: [10]
    md_bg_color: app.theme_cls.bg_normal
    size_hint_y: None
    height: dp(120)
    padding: dp(16)
    spacing: dp(8)
    
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(4)
        
        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: dp(40)
            spacing: dp(8)
            
            MDLabel:
                id: title_label
                text: ""
                font_style: "H6"
                theme_text_color: "Primary"
                size_hint_x: 0.8
                
            MDIconButton:
                icon: "pencil"
                theme_icon_color: "Primary"
                size_hint_x: None
                width: dp(40)
                on_release: root.edit_notification()
                
            MDIconButton:
                icon: "delete"
                theme_icon_color: "Error"
                size_hint_x: None
                width: dp(40)
                on_release: root.delete_notification()
        
        MDLabel:
            id: description_label
            text: ""
            font_style: "Body2"
            theme_text_color: "Secondary"
            text_size: self.width, None
            
        MDLabel:
            id: datetime_label
            text: ""
            font_style: "Caption"
            theme_text_color: "Hint"
            size_hint_y: None
            height: dp(20)

<SearchBar>:
    size_hint_y: None
    height: dp(56)
    padding: [dp(16), dp(8)]
    
    MDTextField:
        id: search_field
        hint_text: "Search notifications..."
        mode: "outlined"
        icon_left: "magnify"
        size_hint_y: None
        height: dp(40)
"""

Builder.load_string(additional_kv)

# Classes from utils.py
class NotificationManager:
    """Manages notification data persistence and operations"""
    
    def __init__(self, data_file="data/notifications.json"):
        self.data_file = data_file
        self.notifications = []
        self.ensure_data_directory()

    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

    def load_notifications(self) -> List[Dict]:
        """Load notifications from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Ensure each notification has an ID
                    for notification in data:
                        if 'id' not in notification:
                            notification['id'] = str(uuid.uuid4())
                    self.notifications = data
            else:
                self.notifications = []
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading notifications: {e}")
            self.notifications = []
        
        return self.notifications

    def save_notifications(self) -> bool:
        """Save notifications to JSON file"""
        try:
            self.ensure_data_directory()
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.notifications, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving notifications: {e}")
            return False

    def get_notifications(self) -> List[Dict]:
        """Get all notifications"""
        return self.notifications.copy()

    def add_notification(self, notification_data: Dict) -> str:
        """Add a new notification"""
        # Generate unique ID
        notification_id = str(uuid.uuid4())
        notification_data['id'] = notification_id
        
        # Add creation timestamp if not present
        if 'created_at' not in notification_data:
            notification_data['created_at'] = datetime.now().isoformat()
        
        # Add to notifications list
        self.notifications.append(notification_data)
        
        # Save to file
        self.save_notifications()
        
        return notification_id

    def update_notification(self, updated_data: Dict) -> bool:
        """Update an existing notification"""
        notification_id = updated_data.get('id')
        if not notification_id:
            return False
        
        # Find and update the notification
        for i, notification in enumerate(self.notifications):
            if notification.get('id') == notification_id:
                # Add update timestamp
                updated_data['updated_at'] = datetime.now().isoformat()
                self.notifications[i] = updated_data
                self.save_notifications()
                return True
        
        return False

    def delete_notification(self, notification_id: str) -> bool:
        """Delete a notification by ID"""
        original_count = len(self.notifications)
        self.notifications = [
            n for n in self.notifications 
            if n.get('id') != notification_id
        ]
        
        if len(self.notifications) < original_count:
            self.save_notifications()
            return True
        
        return False

    def get_notification_by_id(self, notification_id: str) -> Optional[Dict]:
        """Get a specific notification by ID"""
        for notification in self.notifications:
            if notification.get('id') == notification_id:
                return notification.copy()
        return None

    def search_notifications(self, query: str) -> List[Dict]:
        """Search notifications by title or description"""
        query = query.lower().strip()
        if not query:
            return self.get_notifications()
        
        results = []
        for notification in self.notifications:
            title = notification.get('title', '').lower()
            description = notification.get('description', '').lower()
            
            if query in title or query in description:
                results.append(notification.copy())
        
        return results

    def get_upcoming_notifications(self, hours_ahead: int = 24) -> List[Dict]:
        """Get notifications due within the specified hours"""
        now = datetime.now()
        cutoff_time = now + timedelta(hours=hours_ahead)
        
        upcoming = []
        for notification in self.notifications:
            datetime_str = notification.get('datetime')
            if datetime_str:
                try:
                    notification_time = datetime.fromisoformat(datetime_str)
                    if now <= notification_time <= cutoff_time:
                        upcoming.append(notification.copy())
                except ValueError:
                    continue
        
        # Sort by datetime
        upcoming.sort(key=lambda x: x.get('datetime', ''))
        return upcoming

    def get_overdue_notifications(self) -> List[Dict]:
        """Get notifications that are overdue"""
        now = datetime.now()
        overdue = []
        
        for notification in self.notifications:
            datetime_str = notification.get('datetime')
            if datetime_str:
                try:
                    notification_time = datetime.fromisoformat(datetime_str)
                    if notification_time < now:
                        overdue.append(notification.copy())
                except ValueError:
                    continue
        
        # Sort by datetime (most recent first)
        overdue.sort(key=lambda x: x.get('datetime', ''), reverse=True)
        return overdue

    def export_notifications(self, export_path: str) -> bool:
        """Export all notifications to a specified path"""
        try:
            export_data = {
                'notifications': self.notifications,
                'exported_at': datetime.now().isoformat(),
                'version': '1.0.0'
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
        except IOError as e:
            print(f"Error exporting notifications: {e}")
            return False

    def import_notifications(self, import_path: str, merge: bool = True) -> bool:
        """Import notifications from a specified path"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            imported_notifications = import_data.get('notifications', [])
            
            if merge:
                # Merge with existing, avoiding duplicates by ID
                existing_ids = {n['id'] for n in self.notifications}
                new_notifications = [n for n in imported_notifications if n.get('id') not in existing_ids]
                self.notifications.extend(new_notifications)
            else:
                self.notifications = imported_notifications
            
            # Add import timestamp
            for n in self.notifications:
                if 'imported_at' not in n:
                    n['imported_at'] = datetime.now().isoformat()
            
            return self.save_notifications()
            
        except (json.JSONDecodeError, IOError, KeyError) as e:
            print(f"Error importing notifications: {e}")
            return False


class ThemeManager:
    """Manages application theme and appearance settings"""
    
    def __init__(self, settings_file="data/settings.json"):
        self.settings_file = settings_file
        self.settings = self.load_settings()

    def load_settings(self) -> Dict:
        """Load settings from JSON file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.get_default_settings()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading settings: {e}")
            return self.get_default_settings()

    def get_default_settings(self) -> Dict:
        """Get default application settings"""
        return {
            'theme_style': 'Light',
            'primary_palette': 'Blue',
            'accent_palette': 'Amber',
            'font_size': 'Medium',
            'notifications_enabled': True,
            'auto_save': True,
            'last_updated': datetime.now().isoformat()
        }

    def save_settings(self) -> bool:
        """Save settings to JSON file"""
        try:
            self.settings['last_updated'] = datetime.now().isoformat()
            self.ensure_data_directory()
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving settings: {e}")
            return False

    def get_setting(self, key: str, default=None):
        """Get a specific setting value"""
        return self.settings.get(key, default)

    def set_setting(self, key: str, value):
        """Set a specific setting value"""
        self.settings[key] = value
        self.save_settings()

    def get_theme(self) -> str:
        """Get the current theme style"""
        return self.get_setting('theme_style', 'Light')

    def set_theme(self, theme_style: str):
        """Set the theme style"""
        if theme_style in ['Light', 'Dark']:
            self.set_setting('theme_style', theme_style)

    def get_primary_palette(self) -> str:
        """Get the current primary palette"""
        return self.get_setting('primary_palette', 'Blue')

    def get_accent_palette(self) -> str:
        """Get the current accent palette"""
        return self.get_setting('accent_palette', 'Amber')

    def apply_theme(self, theme_cls):
        """Apply the current theme settings to the app"""
        theme_cls.theme_style = self.get_theme()
        theme_cls.primary_palette = self.get_primary_palette()
        theme_cls.accent_palette = self.get_accent_palette()

    def apply_saved_theme(self, theme_cls):
        """Apply saved theme settings when app starts"""
        self.apply_theme(theme_cls)

    def reset_to_defaults(self) -> bool:
        """Reset all settings to default values"""
        self.settings = self.get_default_settings()
        return self.save_settings()

    def export_settings(self, export_path: str) -> bool:
        """Export settings to a specified path"""
        try:
            export_data = {
                'settings': self.settings,
                'exported_at': datetime.now().isoformat(),
                'version': '1.0.0'
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
        except IOError as e:
            print(f"Error exporting settings: {e}")
            return False

    def import_settings(self, import_path: str) -> bool:
        """Import settings from a specified path"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            imported_settings = import_data.get('settings', {})
            
            # Validate imported settings
            default_settings = self.get_default_settings()
            for key, value in imported_settings.items():
                if key in default_settings:
                    self.settings[key] = value
            
            # Add import timestamp
            self.settings['imported_at'] = datetime.now().isoformat()
            self.settings['last_updated'] = datetime.now().isoformat()
            
            return self.save_settings()
            
        except (json.JSONDecodeError, IOError, KeyError) as e:
            print(f"Error importing settings: {e}")
            return False

class DateTimeHelper:
    """Helper class for date and time operations"""
    
    @staticmethod
    def format_datetime(datetime_str: str, format_style='full') -> str:
        """Format datetime string for display"""
        try:
            dt = datetime.fromisoformat(datetime_str)
            
            if format_style == 'full':
                return dt.strftime("%Y-%m-%d at %H:%M")
            elif format_style == 'date':
                return dt.strftime("%Y-%m-%d")
            elif format_style == 'time':
                return dt.strftime("%H:%M")
            elif format_style == 'friendly':
                now = datetime.now()
                diff = dt - now
                
                if diff.days == 0:
                    if diff.seconds < 3600:  # Less than 1 hour
                        minutes = diff.seconds // 60
                        return f"in {minutes} minutes"
                    else:
                        hours = diff.seconds // 3600
                        return f"in {hours} hours"
                elif diff.days == 1:
                    return "tomorrow"
                elif diff.days > 1:
                    return f"in {diff.days} days"
                elif diff.days == -1:
                    return "yesterday"
                else:
                    return f"{abs(diff.days)} days ago"
            
            return dt.strftime("%Y-%m-%d %H:%M")
            
        except ValueError:
            return datetime_str

    @staticmethod
    def is_overdue(datetime_str: str) -> bool:
        """Check if a datetime is overdue"""
        try:
            dt = datetime.fromisoformat(datetime_str)
            return dt < datetime.now()
        except ValueError:
            return False

    @staticmethod
    def is_upcoming(datetime_str: str, hours_ahead: int = 24) -> bool:
        """Check if a datetime is upcoming within specified hours"""
        try:
            dt = datetime.fromisoformat(datetime_str)
            now = datetime.now()
            cutoff = now + timedelta(hours=hours_ahead)
            return now <= dt <= cutoff
        except ValueError:
            return False

    @staticmethod
    def get_time_until(datetime_str: str) -> str:
        """Get human-readable time until the datetime"""
        try:
            dt = datetime.fromisoformat(datetime_str)
            now = datetime.now()
            diff = dt - now
            
            if diff.total_seconds() < 0:
                return "Overdue"
            
            days = diff.days
            hours, remainder = divmod(diff.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            if days > 0:
                return f"{days}d {hours}h"
            elif hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
                
        except ValueError:
            return "Unknown"


class ValidationHelper:
    """Helper class for input validation"""
    
    @staticmethod
    def validate_notification_title(title: str) -> tuple:
        """Validate notification title"""
        title = title.strip()
        
        if not title:
            return False, "Title is required"
        
        if len(title) < 3:
            return False, "Title must be at least 3 characters long"
        
        if len(title) > 100:
            return False, "Title must be less than 100 characters"
        
        return True, ""

    @staticmethod
    def validate_notification_description(description: str) -> tuple:
        """Validate notification description"""
        description = description.strip()
        
        if len(description) > 500:
            return False, "Description must be less than 500 characters"
        
        return True, ""

    @staticmethod
    def validate_datetime(datetime_str: str) -> tuple:
        """Validate datetime string"""
        try:
            datetime.fromisoformat(datetime_str)
            return True, ""
        except ValueError:
            return False, "Invalid date/time format"

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe file operations"""
        import re
        
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        
        # Remove leading/trailing spaces and dots
        filename = filename.strip(' .')
        
        # Limit length
        if len(filename) > 255:
            filename = filename[:255]
        
        # Ensure not empty
        if not filename:
            filename = "untitled"
        
        return filename

# Classes from screens.py
class NotificationCard(MDCard):
    """Custom card widget for displaying notifications"""
    
    def __init__(self, notification_data, screen_instance, **kwargs):
        super().__init__(**kwargs)
        self.notification_data = notification_data
        self.screen_instance = screen_instance
        self.update_display()

    def update_display(self):
        """Update the card display with notification data"""
        self.ids.title_label.text = self.notification_data.get('title', 'No Title')
        self.ids.description_label.text = self.notification_data.get('description', 'No Description')
        
        # Format datetime
        datetime_str = self.notification_data.get('datetime', '')
        if datetime_str:
            try:
                dt = datetime.fromisoformat(datetime_str)
                formatted_dt = dt.strftime("%Y-%m-%d at %H:%M")
                self.ids.datetime_label.text = f"📅 {formatted_dt}"
            except ValueError:
                self.ids.datetime_label.text = f"📅 {datetime_str}"
        else:
            self.ids.datetime_label.text = "📅 No date set"

    def edit_notification(self):
        """Handle edit notification action"""
        self.screen_instance.edit_notification(self.notification_data)

    def delete_notification(self):
        """Handle delete notification action"""
        self.screen_instance.show_delete_confirmation(self.notification_data)


class SearchBar(MDBoxLayout):
    """Custom search bar widget"""
    
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        
    def on_kv_post(self, base_widget):
        """Called after KV properties are applied"""
        self.ids.search_field.bind(text=self.on_search_text)
    
    def on_search_text(self, instance, text):
        """Handle search text changes"""
        if self.callback:
            self.callback(text)


class NotificationListScreen(MDScreen):
    """Main screen showing list of notifications"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.notifications = []
        self.filtered_notifications = []
        self.sort_mode = "date"  # "date" or "title"
        self.build_ui()

    def build_ui(self):
        """Build the user interface"""
        layout = MDFloatLayout()
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="Notify Rohan",
            pos_hint={"top": 1},
            elevation=2
        )
        
        # Add menu button
        toolbar.right_action_items = [
            ["sort", lambda x: self.show_sort_menu()],
            ["cog", lambda x: self.app.switch_screen("settings")]
        ]
        
        # Main content
        content_layout = MDBoxLayout(
            orientation="vertical",
            pos_hint={"top": 0.92},
            size_hint=(1, 0.92),
            spacing=dp(8),
            padding=[dp(16), dp(8)]
        )
        
        # Search bar
        self.search_bar = SearchBar(callback=self.filter_notifications)
        content_layout.add_widget(self.search_bar)
        
        # Notifications list
        scroll = MDScrollView()
        self.notifications_list = MDList(spacing=dp(8))
        scroll.add_widget(self.notifications_list)
        content_layout.add_widget(scroll)
        
        # Floating Action Button
        fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"center_x": 0.9, "center_y": 0.1},
            on_release=self.add_notification
        )
        
        layout.add_widget(toolbar)
        layout.add_widget(content_layout)
        layout.add_widget(fab)
        self.add_widget(layout)

    def on_enter(self):
        """Called when entering this screen"""
        self.refresh_notifications()

    def refresh_notifications(self):
        """Refresh the notifications list"""
        self.notifications = self.app.notification_manager.load_notifications()
        self.filter_notifications(self.search_bar.ids.search_field.text)
        self.sort_notifications()

    def filter_notifications(self, query):
        """Filter notifications based on search query"""
        self.filtered_notifications = self.app.notification_manager.search_notifications(query)
        self.update_list()

    def sort_notifications(self):
        """Sort the filtered notifications"""
        if self.sort_mode == "date":
            self.filtered_notifications.sort(key=lambda x: x.get('datetime', ''), reverse=True)
        elif self.sort_mode == "title":
            self.filtered_notifications.sort(key=lambda x: x.get('title', '').lower())
        self.update_list()

    def update_list(self):
        """Update the notifications list display"""
        self.notifications_list.clear_widgets()
        for notification in self.filtered_notifications:
            card = NotificationCard(notification, self)
            self.notifications_list.add_widget(card)

    def show_sort_menu(self):
        """Show sort options menu"""
        menu_items = [
            {"text": "Sort by Date", "on_release": lambda: self.set_sort("date")},
            {"text": "Sort by Title", "on_release": lambda: self.set_sort("title")},
        ]
        menu = MDDropdownMenu(items=menu_items, width_mult=4)
        menu.open()

    def set_sort(self, mode):
        """Set sort mode and refresh"""
        self.sort_mode = mode
        self.sort_notifications()
        Snackbar(text=f"Sorted by {mode.capitalize()}").open()

    def add_notification(self, *args):
        """Navigate to create notification screen"""
        self.app.switch_screen("create_notification", "left")

    def edit_notification(self, notification_data):
        """Navigate to edit notification screen"""
        edit_screen = self.app.root.get_screen("edit_notification")
        edit_screen.set_notification_data(notification_data)
        self.app.switch_screen("edit_notification", "left")

    def show_delete_confirmation(self, notification_data):
        """Show confirmation dialog for deletion"""
        dialog = MDDialog(
            title="Delete Notification",
            text="Are you sure you want to delete this notification?",
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Delete",
                    md_bg_color=self.app.theme_cls.error_color,
                    on_release=lambda x: self.confirm_delete(dialog, notification_data)
                ),
            ]
        )
        dialog.open()

    def confirm_delete(self, dialog, notification_data):
        """Confirm and perform deletion"""
        dialog.dismiss()
        notification_id = notification_data.get('id')
        if self.app.notification_manager.delete_notification(notification_id):
            Snackbar(text="Notification deleted successfully!").open()
            self.refresh_notifications()
        else:
            Snackbar(text="Error deleting notification").open()


class CreateNotificationScreen(MDScreen):
    """Screen for creating new notifications"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.selected_date = datetime.now().date()
        self.selected_time = datetime.now().time()
        self.build_ui()

    def build_ui(self):
        """Build the user interface"""
        layout = MDFloatLayout()
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="Create Notification",
            pos_hint={"top": 1},
            left_action_items=[["arrow-left", lambda x: self.app.switch_screen("notification_list", "right")]],
            elevation=2
        )
        
        # Main content
        content = MDScrollView(
            pos_hint={"top": 0.92},
            size_hint=(1, 0.92)
        )
        
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(16),
            padding=dp(16),
            size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Title field
        self.title_field = MDTextField(
            hint_text="Title (required)",
            mode="outlined",
            required=True
        )
        content_layout.add_widget(self.title_field)
        
        # Description field
        self.description_field = MDTextField(
            hint_text="Description",
            mode="outlined",
            multiline=True,
            max_height=dp(120)
        )
        content_layout.add_widget(self.description_field)
        
        # Date and time buttons
        datetime_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(48)
        )
        
        self.date_button = MDRaisedButton(
            text=f"📅 {self.selected_date.strftime('%Y-%m-%d')}",
            on_release=self.show_date_picker
        )
        
        self.time_button = MDRaisedButton(
            text=f"🕐 {self.selected_time.strftime('%H:%M')}",
            on_release=self.show_time_picker
        )
        
        datetime_layout.add_widget(self.date_button)
        datetime_layout.add_widget(self.time_button)
        content_layout.add_widget(datetime_layout)
        
        # Create button
        create_button = MDRaisedButton(
            text="Create",
            md_bg_color=self.app.theme_cls.primary_color,
            size_hint_y=None,
            height=dp(48),
            on_release=self.create_notification
        )
        content_layout.add_widget(create_button)
        
        content.add_widget(content_layout)
        layout.add_widget(toolbar)
        layout.add_widget(content)
        self.add_widget(layout)

    def show_date_picker(self, *args):
        """Show date picker dialog"""
        date_picker = MDDatePicker(
            year=self.selected_date.year,
            month=self.selected_date.month,
            day=self.selected_date.day,
        )
        date_picker.bind(on_save=self.on_date_save)
        date_picker.open()

    def on_date_save(self, instance, value, date_range):
        """Handle date selection"""
        self.selected_date = value
        self.update_datetime_buttons()
        instance.dismiss()

    def show_time_picker(self, *args):
        """Show time picker dialog"""
        time_picker = MDTimePicker()
        time_picker.set_time(self.selected_time)
        time_picker.bind(on_save=self.on_time_save)
        time_picker.open()

    def on_time_save(self, instance, time):
        """Handle time selection"""
        self.selected_time = time
        self.update_datetime_buttons()
        instance.dismiss()

    def update_datetime_buttons(self):
        """Update date and time button texts"""
        self.date_button.text = f"📅 {self.selected_date.strftime('%Y-%m-%d')}"
        self.time_button.text = f"🕐 {self.selected_time.strftime('%H:%M')}"

    def create_notification(self, *args):
        """Create new notification"""
        title = self.title_field.text.strip()
        description = self.description_field.text.strip()
        
        if not title:
            Snackbar(text="Title is required").open()
            return
        
        notification_datetime = datetime.combine(self.selected_date, self.selected_time)
        
        notification_data = {
            'title': title,
            'description': description,
            'datetime': notification_datetime.isoformat(),
            'created_at': datetime.now().isoformat()
        }
        
        self.app.notification_manager.add_notification(notification_data)
        
        Snackbar(text="Notification created successfully!").open()
        self.app.switch_screen("notification_list", "right")


class EditNotificationScreen(MDScreen):
    """Screen for editing existing notifications"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.notification_data = None
        self.selected_date = datetime.now().date()
        self.selected_time = datetime.now().time()
        self.build_ui()

    def build_ui(self):
        """Build the user interface"""
        layout = MDFloatLayout()
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="Edit Notification",
            pos_hint={"top": 1},
            left_action_items=[["arrow-left", lambda x: self.app.switch_screen("notification_list", "right")]],
            elevation=2
        )
        
        # Main content
        content = MDScrollView(
            pos_hint={"top": 0.92},
            size_hint=(1, 0.92)
        )
        
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(16),
            padding=dp(16),
            size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Title field
        self.title_field = MDTextField(
            hint_text="Title (required)",
            mode="outlined",
            required=True
        )
        content_layout.add_widget(self.title_field)
        
        # Description field
        self.description_field = MDTextField(
            hint_text="Description",
            mode="outlined",
            multiline=True,
            max_height=dp(120)
        )
        content_layout.add_widget(self.description_field)
        
        # Date and time buttons
        datetime_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(48)
        )
        
        self.date_button = MDRaisedButton(
            text=f"📅 {self.selected_date.strftime('%Y-%m-%d')}",
            on_release=self.show_date_picker
        )
        
        self.time_button = MDRaisedButton(
            text=f"🕐 {self.selected_time.strftime('%H:%M')}",
            on_release=self.show_time_picker
        )
        
        datetime_layout.add_widget(self.date_button)
        datetime_layout.add_widget(self.time_button)
        content_layout.add_widget(datetime_layout)
        
        # Action buttons
        button_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(16),
            size_hint_y=None,
            height=dp(48)
        )
        
        cancel_button = MDRaisedButton(
            text="Cancel",
            size_hint_x=0.5,
            on_release=self.cancel_edit
        )
        
        save_button = MDRaisedButton(
            text="Save",
            size_hint_x=0.5,
            md_bg_color=self.app.theme_cls.primary_color,
            on_release=self.save_notification
        )
        
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(save_button)
        content_layout.add_widget(button_layout)
        
        content.add_widget(content_layout)
        layout.add_widget(toolbar)
        layout.add_widget(content)
        self.add_widget(layout)

    def set_notification_data(self, notification_data):
        """Set the notification data to edit"""
        self.notification_data = notification_data
        
        self.title_field.text = notification_data.get('title', '')
        self.description_field.text = notification_data.get('description', '')
        
        datetime_str = notification_data.get('datetime', '')
        if datetime_str:
            try:
                dt = datetime.fromisoformat(datetime_str)
                self.selected_date = dt.date()
                self.selected_time = dt.time()
            except ValueError:
                self.selected_date = datetime.now().date()
                self.selected_time = datetime.now().time()
        
        self.update_datetime_buttons()

    def show_date_picker(self, *args):
        """Show date picker dialog"""
        date_picker = MDDatePicker(
            year=self.selected_date.year,
            month=self.selected_date.month,
            day=self.selected_date.day,
        )
        date_picker.bind(on_save=self.on_date_save)
        date_picker.open()

    def on_date_save(self, instance, value, date_range):
        """Handle date selection"""
        self.selected_date = value
        self.update_datetime_buttons()
        instance.dismiss()

    def show_time_picker(self, *args):
        """Show time picker dialog"""
        time_picker = MDTimePicker()
        time_picker.set_time(self.selected_time)
        time_picker.bind(on_save=self.on_time_save)
        time_picker.open()

    def on_time_save(self, instance, time):
        """Handle time selection"""
        self.selected_time = time
        self.update_datetime_buttons()
        instance.dismiss()

    def update_datetime_buttons(self):
        """Update date and time button texts"""
        self.date_button.text = f"📅 {self.selected_date.strftime('%Y-%m-%d')}"
        self.time_button.text = f"🕐 {self.selected_time.strftime('%H:%M')}"

    def save_notification(self, *args):
        """Save the edited notification"""
        if not self.notification_data:
            return
            
        title = self.title_field.text.strip()
        description = self.description_field.text.strip()
        
        if not title:
            Snackbar(text="Title is required").open()
            return
        
        notification_datetime = datetime.combine(self.selected_date, self.selected_time)
        
        updated_data = self.notification_data.copy()
        updated_data.update({
            'title': title,
            'description': description,
            'datetime': notification_datetime.isoformat(),
            'updated_at': datetime.now().isoformat()
        })
        
        self.app.notification_manager.update_notification(updated_data)
        
        Snackbar(text="Notification updated successfully!").open()
        self.app.switch_screen("notification_list", "right")

    def cancel_edit(self, *args):
        """Cancel notification editing"""
        self.app.switch_screen("notification_list", "right")


class SettingsScreen(MDScreen):
    """Settings screen for theme and preferences"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        """Build the user interface"""
        layout = MDFloatLayout()
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="Settings",
            pos_hint={"top": 1},
            left_action_items=[["arrow-left", lambda x: self.app.switch_screen("notification_list", "right")]],
            elevation=2
        )
        
        # Main content
        content = MDScrollView(
            pos_hint={"top": 0.92},
            size_hint=(1, 0.92)
        )
        
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(16),
            padding=dp(16),
            size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Theme section
        theme_card = MDCard(
            size_hint_y=None,
            height=dp(120),
            padding=dp(16),
            radius=[10],
            md_bg_color=self.app.theme_cls.bg_normal
        )
        
        theme_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12)
        )
        
        theme_layout.add_widget(MDLabel(
            text="Appearance",
            font_style="H6",
            size_hint_y=None,
            height=dp(32),
            theme_text_color="Primary"
        ))
        
        # Dark mode switch
        switch_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40),
            spacing=dp(12)
        )
        
        switch_layout.add_widget(MDLabel(
            text="Dark Mode",
            font_style="Body1",
            size_hint_x=0.8,
            theme_text_color="Primary"
        ))
        
        self.dark_mode_switch = MDSwitch(
            size_hint_x=None,
            width=dp(50),
            active=self.app.theme_cls.theme_style == "Dark",
            on_active=self.toggle_theme
        )
        switch_layout.add_widget(self.dark_mode_switch)
        
        theme_layout.add_widget(switch_layout)
        theme_card.add_widget(theme_layout)
        content_layout.add_widget(theme_card)
        
        # Statistics section
        stats_card = MDCard(
            size_hint_y=None,
            height=dp(160),
            padding=dp(16),
            radius=[10],
            md_bg_color=self.app.theme_cls.bg_normal
        )
        
        stats_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(8)
        )
        
        stats_layout.add_widget(MDLabel(
            text="Statistics",
            font_style="H6",
            size_hint_y=None,
            height=dp(32),
            theme_text_color="Primary"
        ))
        
        # Calculate notification count
        notification_manager = self.app.notification_manager
        stats = {}  # Simplified; in full code, use notification_manager.get_statistics() if defined
        total = len(notification_manager.notifications)
        upcoming = len(notification_manager.get_upcoming_notifications())
        overdue = len(notification_manager.get_overdue_notifications())
        
        stats_layout.add_widget(MDLabel(
            text=f"Total Notifications: {total}",
            font_style="Body1",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(24)
        ))
        
        stats_layout.add_widget(MDLabel(
            text=f"Upcoming: {upcoming}",
            font_style="Body2",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(20)
        ))
        
        stats_layout.add_widget(MDLabel(
            text=f"Overdue: {overdue}",
            font_style="Body2",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(20)
        ))
        
        stats_layout.add_widget(MDLabel(
            text="Data stored locally in JSON format",
            font_style="Caption",
            theme_text_color="Hint",
            size_hint_y=None,
            height=dp(20)
        ))
        
        stats_card.add_widget(stats_layout)
        content_layout.add_widget(stats_card)
        
        # About section
        about_card = MDCard(
            size_hint_y=None,
            height=dp(160),
            padding=dp(16),
            radius=[10],
            md_bg_color=self.app.theme_cls.bg_normal
        )
        
        about_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(8)
        )
        
        about_layout.add_widget(MDLabel(
            text="About",
            font_style="H6",
            size_hint_y=None,
            height=dp(32),
            theme_text_color="Primary"
        ))
        
        about_layout.add_widget(MDLabel(
            text="Notify Rohan",
            font_style="H5",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(32)
        ))
        
        about_layout.add_widget(MDLabel(
            text="Version 1.0.0",
            font_style="Body2",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(24)
        ))
        
        about_layout.add_widget(MDLabel(
            text="A professional notification management app built with KivyMD",
            font_style="Caption",
            theme_text_color="Hint",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(40)
        ))
        
        about_card.add_widget(about_layout)
        content_layout.add_widget(about_card)
        
        content.add_widget(content_layout)
        layout.add_widget(toolbar)
        layout.add_widget(content)
        self.add_widget(layout)

    def on_enter(self):
        """Called when entering this screen"""
        # Update dark mode switch state
        self.dark_mode_switch.active = self.app.theme_cls.theme_style == "Dark"

    def toggle_theme(self, switch, active):
        """Toggle between light and dark theme"""
        theme_manager = self.app.theme_manager
        if active:
            theme_manager.set_theme("Dark")
            self.app.theme_cls.theme_style = "Dark"
        else:
            theme_manager.set_theme("Light")
            self.app.theme_cls.theme_style = "Light"
        
        # Apply theme immediately
        theme_manager.apply_theme(self.app.theme_cls)
        
        # Show confirmation
        Snackbar(text=f"Switched to {'Dark' if active else 'Light'} theme").open()


class NotifyRohanApp(MDApp):
    """Main application class for Notify Rohan"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notification_manager = NotificationManager()
        self.theme_manager = ThemeManager()

    def build(self):
        """Build the application UI"""
        # Apply saved theme settings
        self.theme_cls.theme_style = self.theme_manager.get_theme()
        self.theme_cls.primary_palette = self.theme_manager.get_primary_palette()
        self.theme_cls.accent_palette = self.theme_manager.get_accent_palette()

        # Create screen manager
        sm = MDScreenManager()

        # Add screens
        sm.add_widget(NotificationListScreen(name="notification_list", app=self))
        sm.add_widget(CreateNotificationScreen(name="create_notification", app=self))
        sm.add_widget(EditNotificationScreen(name="edit_notification", app=self))
        sm.add_widget(SettingsScreen(name="settings", app=self))

        # Set initial screen
        sm.current = "notification_list"

        return sm

    def switch_screen(self, screen_name, transition_direction="left"):
        """Switch between screens with transition"""
        self.root.transition.direction = transition_direction
        self.root.current = screen_name

    def get_notification_manager(self):
        """Get the notification manager instance"""
        return self.notification_manager

    def get_theme_manager(self):
        """Get the theme manager instance"""
        return self.theme_manager

if __name__ == "__main__":
    NotifyRohanApp().run()