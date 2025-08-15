"""
Utility classes for Notify Rohan application
Contains helper functions and managers for data persistence and theme management
"""

import json
import os
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional


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
                # Merge with existing notifications
                existing_ids = {n.get('id') for n in self.notifications}
                
                for notification in imported_notifications:
                    # Generate new ID if conflict or missing
                    if 'id' not in notification or notification['id'] in existing_ids:
                        notification['id'] = str(uuid.uuid4())
                    
                    # Add import timestamp
                    notification['imported_at'] = datetime.now().isoformat()
                    self.notifications.append(notification)
            else:
                # Replace existing notifications
                for notification in imported_notifications:
                    if 'id' not in notification:
                        notification['id'] = str(uuid.uuid4())
                
                self.notifications = imported_notifications
            
            self.save_notifications()
            return True
            
        except (json.JSONDecodeError, IOError, KeyError) as e:
            print(f"Error importing notifications: {e}")
            return False

    def get_statistics(self) -> Dict:
        """Get statistics about notifications"""
        total = len(self.notifications)
        upcoming = len(self.get_upcoming_notifications())
        overdue = len(self.get_overdue_notifications())
        
        # Get creation dates for trend analysis
        creation_dates = []
        for notification in self.notifications:
            created_at = notification.get('created_at')
            if created_at:
                try:
                    creation_dates.append(datetime.fromisoformat(created_at).date())
                except ValueError:
                    continue
        
        return {
            'total_notifications': total,
            'upcoming_notifications': upcoming,
            'overdue_notifications': overdue,
            'completed_notifications': total - upcoming - overdue,
            'creation_dates': creation_dates
        }


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

    def save_settings(self) -> bool:
        """Save settings to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving settings: {e}")
            return False

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

    def get_setting(self, key: str, default=None):
        """Get a specific setting value"""
        return self.settings.get(key, default)

    def set_setting(self, key: str, value) -> bool:
        """Set a specific setting value"""
        self.settings[key] = value
        self.settings['last_updated'] = datetime.now().isoformat()
        return self.save_settings()

    def set_theme(self, theme_style: str) -> bool:
        """Set the theme style (Light/Dark)"""
        if theme_style in ['Light', 'Dark']:
            return self.set_setting('theme_style', theme_style)
        return False

    def get_theme(self) -> str:
        """Get the current theme style"""
        return self.get_setting('theme_style', 'Light')

    def set_primary_palette(self, palette: str) -> bool:
        """Set the primary color palette"""
        valid_palettes = [
            'Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue',
            'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime',
            'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray'
        ]
        
        if palette in valid_palettes:
            return self.set_setting('primary_palette', palette)
        return False

    def get_primary_palette(self) -> str:
        """Get the current primary palette"""
        return self.get_setting('primary_palette', 'Blue')

    def set_accent_palette(self, palette: str) -> bool:
        """Set the accent color palette"""
        valid_palettes = [
            'Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue',
            'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime',
            'Yellow', 'Amber', 'Orange', 'DeepOrange'
        ]
        
        if palette in valid_palettes:
            return self.set_setting('accent_palette', palette)
        return False

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