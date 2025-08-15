"""
Setup script for Notify Rohan application
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Notify Rohan - A professional notification management application"

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements = []
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
    return requirements

setup(
    name="notify-rohan",
    version="1.0.0",
    description="A professional notification management application built with KivyMD",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Rohan",
    author_email="rohan@example.com",
    url="https://github.com/rohan/notify-rohan",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=22.0.0',
            'flake8>=5.0.0',
            'mypy>=0.991',
        ],
        'notifications': [
            'plyer>=2.0.0',
            'win10toast>=0.9.0',
            'pync>=2.0.0',
            'notify2>=0.3.0',
        ]
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Utilities",
    ],
    keywords="notifications, reminders, kivymd, mobile, desktop, cross-platform",
    entry_points={
        'console_scripts': [
            'notify-rohan=main:main',
        ],
        'gui_scripts': [
            'notify-rohan-gui=main:NotifyRohanApp',
        ]
    },
    package_data={
        'notify_rohan': [
            'assets/*.png',
            'assets/*.jpg', 
            'assets/*.svg',
            'assets/icons/*.png',
            'data/*.json',
            '*.kv',
        ]
    },
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/rohan/notify-rohan/issues",
        "Source": "https://github.com/rohan/notify-rohan",
        "Documentation": "https://github.com/rohan/notify-rohan/wiki",
    },
)