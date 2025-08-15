Paused — will revisit after some days. Current version has known errors.


# Notify Rohan 📱

A professional, cross-platform notification management application built with KivyMD. Create, manage, and organize your notifications with a beautiful Material Design interface.

![Notify Rohan Screenshot](assets/screenshot.png)

## ✨ Features

### Core Functionality
- 📝 **Create Notifications**: Add notifications with title, description, and date/time
- ✏️ **Edit & Delete**: Full CRUD operations for notification management
- 🔍 **Smart Search**: Filter notifications by title or description
- 📅 **Date/Time Pickers**: Intuitive date and time selection
- 💾 **Persistent Storage**: All data stored locally in JSON format

### User Interface
- 🎨 **Material Design**: Clean, modern interface following Material Design principles
- 🌓 **Dark/Light Theme**: Toggle between light and dark modes
- 📱 **Responsive Design**: Optimized for both mobile and desktop
- ✨ **Smooth Animations**: Fluid transitions and interactions
- 🎯 **Floating Action Button**: Quick access to create new notifications

### Advanced Features
- 🔄 **Sort Options**: Sort by date or title
- 📊 **Statistics**: View notification statistics in settings
- 🎨 **Theme Customization**: Multiple color palettes available
- 💫 **Smooth Transitions**: Animated screen transitions
- 🔔 **Status Indicators**: Visual indicators for overdue/upcoming notifications

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rohan/notify-rohan.git
   cd notify-rohan
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### Alternative Installation Methods

#### Using pip (when published):
```bash
pip install notify-rohan
notify-rohan
```

#### For development:
```bash
pip install -e .
```

## 📱 Usage

### Creating Notifications
1. Tap the **+** (plus) button or FAB
2. Enter notification title (required)
3. Add description (optional)
4. Select date and time using the pickers
5. Tap **Create** to save

### Managing Notifications
- **Edit**: Tap the pencil icon on any notification card
- **Delete**: Tap the delete icon and confirm
- **Search**: Use the search bar to filter notifications
- **Sort**: Tap the sort icon in the toolbar to change sort order

### Settings & Customization
- **Theme**: Toggle between light and dark modes
- **View Statistics**: See total, upcoming, and overdue notifications
- **App Information**: Version and storage details

## 🏗️ Project Structure

```
notify-rohan/
├── main.py              # Application entry point
├── screens.py           # Screen classes and UI logic
├── utils.py             # Utility classes and helpers
├── notify.kv            # KivyMD layout definitions
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup configuration
├── README.md           # This file
├── data/               # Data storage directory
│   ├── notifications.json  # Notifications data
│   └── settings.json      # App settings
└── assets/             # Application assets
    ├── icons/          # Icon files
    └── images/         # Image files
```

## 🛠️ Technical Details

### Architecture
- **Framework**: KivyMD 1.1.1+ with Kivy 2.3.0+
- **Pattern**: Screen-based navigation with ScreenManager
- **Storage**: JSON-based local storage
- **UI**: Material Design components with custom styling

### Key Components
- **NotificationManager**: Handles data persistence and CRUD operations
- **ThemeManager**: Manages application themes and settings
- **Screen Classes**: Separate screens for different app functions
- **Custom Widgets**: Enhanced KivyMD components with animations

### Data Storage
All data is stored locally in JSON format:
- `data/notifications.json`: Notification data with unique IDs
- `data/settings.json`: User preferences and theme settings

### Responsive Design
- Adapts to different screen sizes (mobile/tablet/desktop)
- Touch-friendly interface with appropriate spacing
- Optimized layouts for various aspect ratios

## 🎨 Customization

### Themes
The app supports multiple color schemes:
- **Primary Palettes**: Blue, Red, Green, Purple, Orange, etc.
- **Accent Colors**: Amber, Pink, Cyan, etc.
- **Theme Styles**: Light and Dark modes

### Configuration
Edit `utils.py` to modify:
- Default color schemes
- Storage locations
- Date/time formats
- Validation rules

## 🧪 Testing

Run tests (when available):
```bash
pytest tests/
```

For coverage reports:
```bash
pytest --cov=. tests/
```

## 📱 Platform Support

### Tested Platforms
- ✅ **Windows** 10/11
- ✅ **macOS** 10.15+
- ✅ **Linux** (Ubuntu, Fedora, etc.)
- ✅ **Android** 7.0+ (via Buildozer)
- 🚧 **iOS** (experimental support)

### Mobile Deployment

#### Android (using Buildozer):
1. Install Buildozer: `pip install buildozer`
2. Initialize: `buildozer init`
3. Build APK: `buildozer android debug`

#### iOS (using kivy-ios):
1. Install kivy-ios: `pip install kivy-ios`
2. Build dependencies: `toolchain build python3 kivy kivymd`
3. Create Xcode project: `toolchain create <appname> <directory>`

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup
```bash
git clone https://github.com/rohan/notify-rohan.git
cd notify-rohan
pip install -e ".[dev]"
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings for functions and classes
- Write unit tests for new features

## 🐛 Known Issues

- Time picker may not show correctly on some Android versions
- Large notification lists may cause performance issues
- Theme switching requires app restart on older Android versions

## 📋 Roadmap

### Upcoming Features
- 🔔 **Push Notifications**: System notifications for reminders
- 📤 **Export/Import**: Backup and restore functionality
- 🏷️ **Categories/Tags**: Organize notifications with labels
- 🔄 **Recurring Notifications**: Support for repeating reminders
- ☁️ **Cloud Sync**: Optional cloud backup and sync
- 🎵 **Custom Sounds**: Personalized notification sounds

### Long-term Goals
- Desktop widgets
- Web interface
- Team collaboration features
- Advanced scheduling options
- Integration with calendar apps

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **KivyMD Team** for the excellent Material Design framework
- **Kivy Community** for the cross-platform Python framework
- **Material Design** guidelines for UI/UX inspiration
- **Contributors** who help improve this project

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/rohan/notify-rohan/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rohan/notify-rohan/discussions)
- **Email**: rohan@example.com

## 📊 Statistics

![GitHub stars](https://img.shields.io/github/stars/rohan/notify-rohan?style=social)
![GitHub forks](https://img.shields.io/github/forks/rohan/notify-rohan?style=social)
![GitHub issues](https://img.shields.io/github/issues/rohan/notify-rohan)
![GitHub license](https://img.shields.io/github/license/rohan/notify-rohan)

---

**Made with ❤️ by Rohan using KivyMD**
