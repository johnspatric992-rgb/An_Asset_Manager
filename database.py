"""
Database module for Asset Manager application.
Handles all database operations using SQLite.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class AssetDatabase:
    """Database manager for asset operations."""
    
    def __init__(self, db_path: str = "assets.db"):
        """Initialize database connection and create tables if needed."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create necessary tables if they don't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                location TEXT NOT NULL,
                purchase_price REAL NOT NULL,
                current_value REAL NOT NULL,
                purchase_date TEXT,
                condition TEXT DEFAULT 'Good',
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        self.conn.commit()
    
    def add_asset(self, name: str, category: str, description: str, location: str,
                  purchase_price: float, current_value: float, purchase_date: str = None,
                  condition: str = 'Good', notes: str = '') -> int:
        """Add a new asset to the database."""
        now = datetime.now().isoformat()
        self.cursor.execute('''
            INSERT INTO assets (name, category, description, location, purchase_price,
                              current_value, purchase_date, condition, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, description, location, purchase_price, current_value,
              purchase_date, condition, notes, now, now))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_all_assets(self) -> List[Dict]:
        """Retrieve all assets from the database."""
        self.cursor.execute('SELECT * FROM assets ORDER BY created_at DESC')
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_asset_by_id(self, asset_id: int) -> Optional[Dict]:
        """Retrieve a specific asset by ID."""
        self.cursor.execute('SELECT * FROM assets WHERE id = ?', (asset_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def update_asset(self, asset_id: int, name: str, category: str, description: str,
                     location: str, purchase_price: float, current_value: float,
                     purchase_date: str = None, condition: str = 'Good', notes: str = '') -> bool:
        """Update an existing asset."""
        now = datetime.now().isoformat()
        self.cursor.execute('''
            UPDATE assets
            SET name = ?, category = ?, description = ?, location = ?,
                purchase_price = ?, current_value = ?, purchase_date = ?,
                condition = ?, notes = ?, updated_at = ?
            WHERE id = ?
        ''', (name, category, description, location, purchase_price, current_value,
              purchase_date, condition, notes, now, asset_id))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def delete_asset(self, asset_id: int) -> bool:
        """Delete an asset from the database."""
        self.cursor.execute('DELETE FROM assets WHERE id = ?', (asset_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def search_assets(self, search_term: str) -> List[Dict]:
        """Search assets by name, category, or location."""
        search_pattern = f'%{search_term}%'
        self.cursor.execute('''
            SELECT * FROM assets
            WHERE name LIKE ? OR category LIKE ? OR location LIKE ?
            ORDER BY created_at DESC
        ''', (search_pattern, search_pattern, search_pattern))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_assets_by_category(self, category: str) -> List[Dict]:
        """Retrieve assets filtered by category."""
        self.cursor.execute('SELECT * FROM assets WHERE category = ? ORDER BY created_at DESC', (category,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_assets_by_location(self, location: str) -> List[Dict]:
        """Retrieve assets filtered by location."""
        self.cursor.execute('SELECT * FROM assets WHERE location = ? ORDER BY created_at DESC', (location,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_total_purchase_value(self) -> float:
        """Calculate total purchase value of all assets."""
        self.cursor.execute('SELECT SUM(purchase_price) FROM assets')
        result = self.cursor.fetchone()[0]
        return result if result else 0.0
    
    def get_total_current_value(self) -> float:
        """Calculate total current value of all assets."""
        self.cursor.execute('SELECT SUM(current_value) FROM assets')
        result = self.cursor.fetchone()[0]
        return result if result else 0.0
    
    def get_asset_count(self) -> int:
        """Get total number of assets."""
        self.cursor.execute('SELECT COUNT(*) FROM assets')
        return self.cursor.fetchone()[0]
    
    def get_categories(self) -> List[str]:
        """Get all unique categories."""
        self.cursor.execute('SELECT DISTINCT category FROM assets ORDER BY category')
        return [row[0] for row in self.cursor.fetchall()]
    
    def get_locations(self) -> List[str]:
        """Get all unique locations."""
        self.cursor.execute('SELECT DISTINCT location FROM assets ORDER BY location')
        return [row[0] for row in self.cursor.fetchall()]
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
