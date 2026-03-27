"""
Asset Manager - Desktop Application
Main entry point for the application.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui import AssetManagerUI


def main():
    """Main application entry point."""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Asset Manager")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("AssetManager")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = AssetManagerUI()
    window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
