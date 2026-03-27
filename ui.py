"""
User Interface module for Asset Manager application.
Built with PyQt5 for a professional desktop experience.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QLabel, QComboBox,
    QTextEdit, QDateEdit, QGroupBox, QFormLayout, QMessageBox,
    QDialog, QDialogButtonBox, QHeaderView, QAbstractItemView,
    QStatusBar, QMenuBar, QMenu, QAction, QSplitter, QFrame
)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QColor
from database import AssetDatabase
from typing import Optional, Dict


class AssetDialog(QDialog):
    """Dialog for adding/editing assets."""
    
    def __init__(self, parent=None, asset_data: Optional[Dict] = None):
        super().__init__(parent)
        self.asset_data = asset_data
        self.setWindowTitle("Add Asset" if not asset_data else "Edit Asset")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.init_ui()
        if asset_data:
            self.populate_fields(asset_data)
    
    def init_ui(self):
        """Initialize the dialog UI."""
        layout = QVBoxLayout()
        
        # Form layout
        form_layout = QFormLayout()
        
        # Asset Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter asset name")
        form_layout.addRow("Asset Name:", self.name_input)
        
        # Category
        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        self.category_combo.addItems([
            "Electronics", "Furniture", "Vehicle", "Real Estate",
            "Jewelry", "Art", "Equipment", "Tools", "Appliances",
            "Sports", "Musical Instruments", "Collectibles", "Other"
        ])
        form_layout.addRow("Category:", self.category_combo)
        
        # Description
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(80)
        self.description_input.setPlaceholderText("Enter description")
        form_layout.addRow("Description:", self.description_input)
        
        # Location
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Enter location (e.g., Home, Office, Storage)")
        form_layout.addRow("Location:", self.location_input)
        
        # Purchase Price
        self.purchase_price_input = QLineEdit()
        self.purchase_price_input.setPlaceholderText("0.00")
        form_layout.addRow("Purchase Price ($):", self.purchase_price_input)
        
        # Current Value
        self.current_value_input = QLineEdit()
        self.current_value_input.setPlaceholderText("0.00")
        form_layout.addRow("Current Value ($):", self.current_value_input)
        
        # Purchase Date
        self.purchase_date_input = QDateEdit()
        self.purchase_date_input.setCalendarPopup(True)
        self.purchase_date_input.setDate(QDate.currentDate())
        form_layout.addRow("Purchase Date:", self.purchase_date_input)
        
        # Condition
        self.condition_combo = QComboBox()
        self.condition_combo.addItems(["Excellent", "Good", "Fair", "Poor", "Needs Repair"])
        form_layout.addRow("Condition:", self.condition_combo)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setPlaceholderText("Additional notes")
        form_layout.addRow("Notes:", self.notes_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def populate_fields(self, asset_data: Dict):
        """Populate fields with existing asset data."""
        self.name_input.setText(asset_data.get('name', ''))
        
        # Set category
        category = asset_data.get('category', '')
        index = self.category_combo.findText(category)
        if index >= 0:
            self.category_combo.setCurrentIndex(index)
        else:
            self.category_combo.setCurrentText(category)
        
        self.description_input.setText(asset_data.get('description', ''))
        self.location_input.setText(asset_data.get('location', ''))
        self.purchase_price_input.setText(str(asset_data.get('purchase_price', 0)))
        self.current_value_input.setText(str(asset_data.get('current_value', 0)))
        
        # Set purchase date
        purchase_date = asset_data.get('purchase_date', '')
        if purchase_date:
            self.purchase_date_input.setDate(QDate.fromString(purchase_date, Qt.ISODate))
        
        # Set condition
        condition = asset_data.get('condition', 'Good')
        index = self.condition_combo.findText(condition)
        if index >= 0:
            self.condition_combo.setCurrentIndex(index)
        
        self.notes_input.setText(asset_data.get('notes', ''))
    
    def validate_and_accept(self):
        """Validate input before accepting."""
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Asset name is required.")
            return
        
        if not self.location_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Location is required.")
            return
        
        try:
            purchase_price = float(self.purchase_price_input.text() or 0)
            if purchase_price < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid purchase price.")
            return
        
        try:
            current_value = float(self.current_value_input.text() or 0)
            if current_value < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid current value.")
            return
        
        self.accept()
    
    def get_data(self) -> Dict:
        """Get the entered data."""
        return {
            'name': self.name_input.text().strip(),
            'category': self.category_combo.currentText(),
            'description': self.description_input.toPlainText().strip(),
            'location': self.location_input.text().strip(),
            'purchase_price': float(self.purchase_price_input.text() or 0),
            'current_value': float(self.current_value_input.text() or 0),
            'purchase_date': self.purchase_date_input.date().toString(Qt.ISODate),
            'condition': self.condition_combo.currentText(),
            'notes': self.notes_input.toPlainText().strip()
        }


class AssetManagerUI(QMainWindow):
    """Main application window for Asset Manager."""
    
    def __init__(self):
        super().__init__()
        self.db = AssetDatabase()
        self.init_ui()
        self.load_assets()
        self.update_summary()
    
    def init_ui(self):
        """Initialize the main UI."""
        self.setWindowTitle("Asset Manager - Track Your Valuables")
        self.setMinimumSize(1200, 700)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar(main_layout)
        
        # Create summary section
        self.create_summary_section(main_layout)
        
        # Create search and filter section
        self.create_search_filter_section(main_layout)
        
        # Create assets table
        self.create_assets_table(main_layout)
        
        # Create action buttons
        self.create_action_buttons(main_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        add_action = QAction("Add Asset", self)
        add_action.setShortcut("Ctrl+N")
        add_action.triggered.connect(self.add_asset)
        file_menu.addAction(add_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        edit_action = QAction("Edit Selected", self)
        edit_action.setShortcut("Ctrl+E")
        edit_action.triggered.connect(self.edit_asset)
        edit_menu.addAction(edit_action)
        
        delete_action = QAction("Delete Selected", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self.delete_asset)
        edit_menu.addAction(delete_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        refresh_action = QAction("Refresh", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.load_assets)
        view_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self, parent_layout):
        """Create the toolbar."""
        toolbar_layout = QHBoxLayout()
        
        # App title
        title_label = QLabel("Asset Manager")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        toolbar_layout.addWidget(title_label)
        
        toolbar_layout.addStretch()
        
        # Quick action buttons
        add_btn = QPushButton("➕ Add Asset")
        add_btn.setStyleSheet("QPushButton { padding: 8px 16px; font-weight: bold; }")
        add_btn.clicked.connect(self.add_asset)
        toolbar_layout.addWidget(add_btn)
        
        parent_layout.addLayout(toolbar_layout)
    
    def create_summary_section(self, parent_layout):
        """Create the summary section showing totals."""
        summary_group = QGroupBox("Portfolio Summary")
        summary_layout = QHBoxLayout()
        
        # Total Assets
        self.total_assets_label = QLabel("Total Assets: 0")
        self.total_assets_label.setFont(QFont("Arial", 12))
        summary_layout.addWidget(self.total_assets_label)
        
        summary_layout.addStretch()
        
        # Total Purchase Value
        self.total_purchase_label = QLabel("Total Purchase Value: $0.00")
        self.total_purchase_label.setFont(QFont("Arial", 12))
        summary_layout.addWidget(self.total_purchase_label)
        
        summary_layout.addStretch()
        
        # Total Current Value
        self.total_current_label = QLabel("Total Current Value: $0.00")
        self.total_current_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.total_current_label.setStyleSheet("color: #2e7d32;")
        summary_layout.addWidget(self.total_current_label)
        
        summary_layout.addStretch()
        
        # Gain/Loss
        self.gain_loss_label = QLabel("Gain/Loss: $0.00")
        self.gain_loss_label.setFont(QFont("Arial", 12, QFont.Bold))
        summary_layout.addWidget(self.gain_loss_label)
        
        summary_group.setLayout(summary_layout)
        parent_layout.addWidget(summary_group)
    
    def create_search_filter_section(self, parent_layout):
        """Create search and filter controls."""
        filter_layout = QHBoxLayout()
        
        # Search
        search_label = QLabel("Search:")
        filter_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, category, or location...")
        self.search_input.textChanged.connect(self.filter_assets)
        filter_layout.addWidget(self.search_input)
        
        # Category filter
        category_label = QLabel("Category:")
        filter_layout.addWidget(category_label)
        
        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories")
        self.category_filter.currentTextChanged.connect(self.filter_assets)
        filter_layout.addWidget(self.category_filter)
        
        # Location filter
        location_label = QLabel("Location:")
        filter_layout.addWidget(location_label)
        
        self.location_filter = QComboBox()
        self.location_filter.addItem("All Locations")
        self.location_filter.currentTextChanged.connect(self.filter_assets)
        filter_layout.addWidget(self.location_filter)
        
        # Clear filters button
        clear_btn = QPushButton("Clear Filters")
        clear_btn.clicked.connect(self.clear_filters)
        filter_layout.addWidget(clear_btn)
        
        parent_layout.addLayout(filter_layout)
    
    def create_assets_table(self, parent_layout):
        """Create the assets table."""
        self.assets_table = QTableWidget()
        self.assets_table.setColumnCount(9)
        self.assets_table.setHorizontalHeaderLabels([
            "ID", "Name", "Category", "Location", "Purchase Price",
            "Current Value", "Condition", "Purchase Date", "Actions"
        ])
        
        # Set table properties
        self.assets_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.assets_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.assets_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.assets_table.setAlternatingRowColors(True)
        
        # Set column widths
        header = self.assets_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)  # Actions
        
        # Connect double-click to edit
        self.assets_table.doubleClicked.connect(self.edit_asset)
        
        parent_layout.addWidget(self.assets_table)
    
    def create_action_buttons(self, parent_layout):
        """Create action buttons."""
        button_layout = QHBoxLayout()
        
        edit_btn = QPushButton("✏️ Edit Selected")
        edit_btn.clicked.connect(self.edit_asset)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ Delete Selected")
        delete_btn.clicked.connect(self.delete_asset)
        button_layout.addWidget(delete_btn)
        
        button_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_assets)
        button_layout.addWidget(refresh_btn)
        
        parent_layout.addLayout(button_layout)
    
    def load_assets(self):
        """Load all assets into the table."""
        assets = self.db.get_all_assets()
        self.populate_table(assets)
        self.update_filters()
        self.update_summary()
        self.statusBar().showMessage(f"Loaded {len(assets)} assets")
    
    def populate_table(self, assets):
        """Populate the table with asset data."""
        self.assets_table.setRowCount(len(assets))
        
        for row, asset in enumerate(assets):
            # ID
            self.assets_table.setItem(row, 0, QTableWidgetItem(str(asset['id'])))
            
            # Name
            self.assets_table.setItem(row, 1, QTableWidgetItem(asset['name']))
            
            # Category
            self.assets_table.setItem(row, 2, QTableWidgetItem(asset['category']))
            
            # Location
            self.assets_table.setItem(row, 3, QTableWidgetItem(asset['location']))
            
            # Purchase Price
            price_item = QTableWidgetItem(f"${asset['purchase_price']:,.2f}")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.assets_table.setItem(row, 4, price_item)
            
            # Current Value
            value_item = QTableWidgetItem(f"${asset['current_value']:,.2f}")
            value_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Color code based on gain/loss
            if asset['current_value'] > asset['purchase_price']:
                value_item.setForeground(QColor("#2e7d32"))  # Green for gain
            elif asset['current_value'] < asset['purchase_price']:
                value_item.setForeground(QColor("#c62828"))  # Red for loss
            
            self.assets_table.setItem(row, 5, value_item)
            
            # Condition
            condition_item = QTableWidgetItem(asset['condition'])
            # Color code condition
            condition_colors = {
                "Excellent": "#2e7d32",
                "Good": "#388e3c",
                "Fair": "#f57c00",
                "Poor": "#d32f2f",
                "Needs Repair": "#b71c1c"
            }
            condition_item.setForeground(QColor(condition_colors.get(asset['condition'], "black")))
            self.assets_table.setItem(row, 6, condition_item)
            
            # Purchase Date
            purchase_date = asset.get('purchase_date', '')
            if purchase_date:
                date_item = QTableWidgetItem(purchase_date.split('T')[0])
            else:
                date_item = QTableWidgetItem("N/A")
            self.assets_table.setItem(row, 7, date_item)
            
            # Actions (hidden, but used for reference)
            self.assets_table.setItem(row, 8, QTableWidgetItem(""))
    
    def update_filters(self):
        """Update filter combo boxes with current data."""
        # Save current selections
        current_category = self.category_filter.currentText()
        current_location = self.location_filter.currentText()
        
        # Update category filter
        categories = self.db.get_categories()
        self.category_filter.blockSignals(True)
        self.category_filter.clear()
        self.category_filter.addItem("All Categories")
        self.category_filter.addItems(categories)
        
        # Restore selection if still valid
        index = self.category_filter.findText(current_category)
        if index >= 0:
            self.category_filter.setCurrentIndex(index)
        self.category_filter.blockSignals(False)
        
        # Update location filter
        locations = self.db.get_locations()
        self.location_filter.blockSignals(True)
        self.location_filter.clear()
        self.location_filter.addItem("All Locations")
        self.location_filter.addItems(locations)
        
        # Restore selection if still valid
        index = self.location_filter.findText(current_location)
        if index >= 0:
            self.location_filter.setCurrentIndex(index)
        self.location_filter.blockSignals(False)
    
    def update_summary(self):
        """Update the summary section."""
        total_count = self.db.get_asset_count()
        total_purchase = self.db.get_total_purchase_value()
        total_current = self.db.get_total_current_value()
        gain_loss = total_current - total_purchase
        
        self.total_assets_label.setText(f"Total Assets: {total_count}")
        self.total_purchase_label.setText(f"Total Purchase Value: ${total_purchase:,.2f}")
        self.total_current_label.setText(f"Total Current Value: ${total_current:,.2f}")
        
        # Color code gain/loss
        if gain_loss >= 0:
            self.gain_loss_label.setText(f"Gain: +${gain_loss:,.2f}")
            self.gain_loss_label.setStyleSheet("color: #2e7d32; font-weight: bold;")
        else:
            self.gain_loss_label.setText(f"Loss: -${abs(gain_loss):,.2f}")
            self.gain_loss_label.setStyleSheet("color: #c62828; font-weight: bold;")
    
    def filter_assets(self):
        """Filter assets based on search and filter criteria."""
        search_term = self.search_input.text().strip()
        category = self.category_filter.currentText()
        location = self.location_filter.currentText()
        
        # Start with all assets
        if search_term:
            assets = self.db.search_assets(search_term)
        else:
            assets = self.db.get_all_assets()
        
        # Apply category filter
        if category != "All Categories":
            assets = [a for a in assets if a['category'] == category]
        
        # Apply location filter
        if location != "All Locations":
            assets = [a for a in assets if a['location'] == location]
        
        self.populate_table(assets)
        self.statusBar().showMessage(f"Showing {len(assets)} assets")
    
    def clear_filters(self):
        """Clear all filters."""
        self.search_input.clear()
        self.category_filter.setCurrentIndex(0)
        self.location_filter.setCurrentIndex(0)
        self.load_assets()
    
    def add_asset(self):
        """Open dialog to add a new asset."""
        dialog = AssetDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.db.add_asset(**data)
            self.load_assets()
            self.statusBar().showMessage(f"Added asset: {data['name']}")
    
    def edit_asset(self):
        """Open dialog to edit selected asset."""
        selected_rows = self.assets_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select an asset to edit.")
            return
        
        # Get asset ID from first column
        row = selected_rows[0].row()
        asset_id = int(self.assets_table.item(row, 0).text())
        
        # Get asset data
        asset_data = self.db.get_asset_by_id(asset_id)
        if not asset_data:
            QMessageBox.warning(self, "Error", "Asset not found.")
            return
        
        # Open edit dialog
        dialog = AssetDialog(self, asset_data)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.db.update_asset(asset_id, **data)
            self.load_assets()
            self.statusBar().showMessage(f"Updated asset: {data['name']}")
    
    def delete_asset(self):
        """Delete selected asset."""
        selected_rows = self.assets_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select an asset to delete.")
            return
        
        # Get asset ID and name
        row = selected_rows[0].row()
        asset_id = int(self.assets_table.item(row, 0).text())
        asset_name = self.assets_table.item(row, 1).text()
        
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete '{asset_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_asset(asset_id)
            self.load_assets()
            self.statusBar().showMessage(f"Deleted asset: {asset_name}")
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self, "About Asset Manager",
            "<h2>Asset Manager</h2>"
            "<p>Version 1.0</p>"
            "<p>A desktop application for managing and tracking your personal assets.</p>"
            "<p>Features:</p>"
            "<ul>"
            "<li>Track asset registry with detailed information</li>"
            "<li>Monitor asset locations</li>"
            "<li>Track purchase costs and current values</li>"
            "<li>Calculate portfolio gains/losses</li>"
            "<li>Search and filter capabilities</li>"
            "</ul>"
            "<p>Built with Python and PyQt5</p>"
        )
    
    def closeEvent(self, event):
        """Handle application close."""
        self.db.close()
        event.accept()
