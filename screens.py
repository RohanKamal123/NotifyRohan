"""
Screen classes for Notify Rohan application
Contains all screen definitions and their logic
"""

from datetime import datetime, timedelta
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFabButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.menu import MDDropdownMenu


# Load KV string for layouts
kv_string = """
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

Builder.load_string(kv_string)


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
        fab = MDFabButton(
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
        self.notifications = self.app.get_notification_manager().get_notifications()
        self.filtered_notifications = self.notifications.copy()
        self.sort_notifications()
        self.update_display()

    def filter_notifications(self, search_text):
        """Filter notifications based on search text"""
        if not search_text.strip():
            self.filtered_notifications = self.notifications.copy()
        else:
            search_text = search_text.lower()
            self.filtered_notifications = [
                notif for notif in self.notifications
                if search_text in notif.get('title', '').lower() or
                   search_text in notif.get('description', '').lower()
            ]
        self.sort_notifications()
        self.update_display()

    def sort_notifications(self):
        """Sort notifications based on current sort mode"""
        if self.sort_mode == "date":
            self.filtered_notifications.sort(
                key=lambda x: x.get('datetime', ''),
                reverse=True
            )
        elif self.sort_mode == "title":
            self.filtered_notifications.sort(
                key=lambda x: x.get('title', '').lower()
            )

    def update_display(self):
        """Update the notifications display"""
        self.notifications_list.clear_widgets()
        
        if not self.filtered_notifications:
            # Show empty state
            empty_card = MDCard(
                size_hint_y=None,
                height=dp(100),
                radius=[10],
                md_bg_color=self.app.theme_cls.bg_normal,
                padding=dp(20)
            )
            empty_label = MDLabel(
                text="No notifications found.\nTap the + button to create one!",
                halign="center",
                theme_text_color="Secondary",
                font_style="Body1"
            )
            empty_card.add_widget(empty_label)
            self.notifications_list.add_widget(empty_card)
        else:
            # Add notification cards
            for notification in self.filtered_notifications:
                card = NotificationCard(notification, self)
                self.notifications_list.add_widget(card)

    def add_notification(self, *args):
        """Navigate to create notification screen"""
        self.app.switch_screen("create_notification")

    def edit_notification(self, notification_data):
        """Navigate to edit notification screen"""
        edit_screen = self.app.screen_manager.get_screen("edit_notification")
        edit_screen.set_notification_data(notification_data)
        self.app.switch_screen("edit_notification")

    def show_delete_confirmation(self, notification_data):
        """Show confirmation dialog for deletion"""
        dialog = MDDialog(
            title="Delete Notification",
            text=f"Are you sure you want to delete '{notification_data.get('title', 'this notification')}'?",
            buttons=[
                MDRaisedButton(
                    text="CANCEL",
                    theme_bg_color="Primary",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=self.app.theme_cls.error_color if hasattr(self.app.theme_cls, 'error_color') else [1, 0, 0, 1],
                    on_release=lambda x: self.delete_notification(notification_data, dialog)
                ),
            ],
        )
        dialog.open()

    def delete_notification(self, notification_data, dialog):
        """Delete a notification"""
        self.app.get_notification_manager().delete_notification(notification_data.get('id'))
        dialog.dismiss()
        self.refresh_notifications()
        
        # Show snackbar
        Snackbar(text="Notification deleted").open()

    def show_sort_menu(self):
        """Show sort options menu"""
        menu_items = [
            {
                "text": "Sort by Date",
                "leading_icon": "calendar",
                "on_release": lambda: self.set_sort_mode("date")
            },
            {
                "text": "Sort by Title",
                "leading_icon": "format-title",
                "on_release": lambda: self.set_sort_mode("title")
            }
        ]
        
        self.sort_menu = MDDropdownMenu(
            caller=self,
            items=menu_items,
            width_mult=4,
        )
        self.sort_menu.open()

    def set_sort_mode(self, mode):
        """Set the sort mode and refresh"""
        self.sort_mode = mode
        self.sort_menu.dismiss()
        self.sort_notifications()
        self.update_display()


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
            hint_text="Notification Title",
            mode="outlined",
            required=True,
            helper_text="Required field",
            helper_text_mode="on_error"
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
        
        # Date and time selection
        datetime_card = MDCard(
            size_hint_y=None,
            height=dp(120),
            padding=dp(16),
            radius=[10],
            md_bg_color=self.app.theme_cls.bg_normal
        )
        
        datetime_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(8)
        )
        
        datetime_layout.add_widget(MDLabel(
            text="Date & Time",
            font_style="H6",
            size_hint_y=None,
            height=dp(32),
            theme_text_color="Primary"
        ))
        
        buttons_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(40)
        )
        
        self.date_button = MDRaisedButton(
            text=f"📅 {self.selected_date.strftime('%Y-%m-%d')}",
            on_release=self.show_date_picker,
            size_hint_x=0.5
        )
        
        self.time_button = MDRaisedButton(
            text=f"🕒 {self.selected_time.strftime('%H:%M')}",
            on_release=self.show_time_picker,
            size_hint_x=0.5
        )
        
        buttons_layout.add_widget(self.date_button)
        buttons_layout.add_widget(self.time_button)
        datetime_layout.add_widget(buttons_layout)
        datetime_card.add_widget(datetime_layout)
        content_layout.add_widget(datetime_card)
        
        # Action buttons
        button_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(16),
            size_hint_y=None,
            height=dp(48)
        )
        
        cancel_button = MDRaisedButton(
            text="Cancel",
            theme_bg_color="Primary",
            size_hint_x=0.5,
            on_release=self.cancel_creation
        )
        
        create_button = MDRaisedButton(
            text="Create",
            theme_bg_color="Primary",
            size_hint_x=0.5,
            on_release=self.create_notification
        )
        
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(create_button)
        content_layout.add_widget(button_layout)
        
        content.add_widget(content_layout)
        layout.add_widget(toolbar)
        layout.add_widget(content)
        self.add_widget(layout)

    def on_enter(self):
        """Called when entering this screen"""
        # Reset form
        self.title_field.text = ""
        self.description_field.text = ""
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
        time_picker = MDTimePicker(
            hour=self.selected_time.hour,
            minute=self.selected_time.minute,
        )
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
        self.time_button.text = f"🕒 {self.selected_time.strftime('%H:%M')}"

    def create_notification(self, *args):
        """Create a new notification"""
        title = self.title_field.text.strip()
        description = self.description_field.text.strip()
        
        if not title:
            self.title_field.error = True
            self.title_field.helper_text = "Title is required"
            return
        
        # Combine date and time
        notification_datetime = datetime.combine(self.selected_date, self.selected_time)
        
        # Create notification data
        notification_data = {
            'title': title,
            'description': description,
            'datetime': notification_datetime.isoformat(),
            'created_at': datetime.now().isoformat()
        }
        
        # Save notification
        self.app.get_notification_manager().add_notification(notification_data)
        
        # Show success message
        Snackbar(text="Notification created successfully!").open()
        
        # Go back to list
        self.app.switch_screen("notification_list", "right")

    def cancel_creation(self, *args):
        """Cancel notification creation"""
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
        
        # Main content (similar to create screen)
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
            hint_text="Notification Title",
            mode="outlined",
            required=True,
            helper_text="Required field",
            helper_text_mode="on_error"
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
        
        # Date and time selection
        datetime_card = MDCard(
            size_hint_y=None,
            height=dp(120),
            padding=dp(16),
            radius=[10],
            md_bg_color=self.app.theme_cls.bg_normal
        )
        
        datetime_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(8)
        )
        
        datetime_layout.add_widget(MDLabel(
            text="Date & Time",
            font_style="H6",
            size_hint_y=None,
            height=dp(32),
            theme_text_color="Primary"
        ))
        
        buttons_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(40)
        )
        
        self.date_button = MDRaisedButton(
            text=f"📅 {self.selected_date.strftime('%Y-%m-%d')}",
            on_release=self.show_date_picker,
            size_hint_x=0.5
        )
        
        self.time_button = MDRaisedButton(
            text=f"🕒 {self.selected_time.strftime('%H:%M')}",
            on_release=self.show_time_picker,
            size_hint_x=0.5
        )
        
        buttons_layout.add_widget(self.date_button)
        buttons_layout.add_widget(self.time_button)
        datetime_layout.add_widget(buttons_layout)
        datetime_card.add_widget(datetime_layout)
        content_layout.add_widget(datetime_card)
        
        # Action buttons
        button_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(16),
            size_hint_y=None,
            height=dp(48)
        )
        
        cancel_button = MDRaisedButton(
            text="Cancel",
            theme_bg_color="Primary",
            size_hint_x=0.5,
            on_release=self.cancel_edit
        )
        
        save_button = MDRaisedButton(
            text="Save",
            theme_bg_color="Primary",
            size_hint_x=0.5,
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
        
        # Populate fields
        self.title_field.text = notification_data.get('title', '')
        self.description_field.text = notification_data.get('description', '')
        
        # Parse datetime
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
        time_picker = MDTimePicker(
            hour=self.selected_time.hour,
            minute=self.selected_time.minute,
        )
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
        self.time_button.text = f"🕒 {self.selected_time.strftime('%H:%M')}"

    def save_notification(self, *args):
        """Save the edited notification"""
        if not self.notification_data:
            return
            
        title = self.title_field.text.strip()
        description = self.description_field.text.strip()
        
        if not title:
            self.title_field.error = True
            self.title_field.helper_text = "Title is required"
            return
        
        # Combine date and time
        notification_datetime = datetime.combine(self.selected_date, self.selected_time)
        
        # Update notification data
        updated_data = self.notification_data.copy()
        updated_data.update({
            'title': title,
            'description': description,
            'datetime': notification_datetime.isoformat(),
            'updated_at': datetime.now().isoformat()
        })
        
        # Save notification
        self.app.get_notification_manager().update_notification(updated_data)
        
        # Show success message
        Snackbar(text="Notification updated successfully!").open()
        
        # Go back to list
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
        notification_manager = self.app.get_notification_manager()
        stats = notification_manager.get_statistics()
        
        stats_layout.add_widget(MDLabel(
            text=f"Total Notifications: {stats.get('total_notifications', 0)}",
            font_style="Body1",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(24)
        ))
        
        stats_layout.add_widget(MDLabel(
            text=f"Upcoming: {stats.get('upcoming_notifications', 0)}",
            font_style="Body2",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(20)
        ))
        
        stats_layout.add_widget(MDLabel(
            text=f"Overdue: {stats.get('overdue_notifications', 0)}",
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
        theme_manager = self.app.get_theme_manager()
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