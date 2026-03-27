# Asset Manager - Desktop Application

A professional desktop application for managing and tracking your personal assets. Built with Python and PyQt5.

## Features

- **Asset Registry**: Track all your assets with detailed information
- **Location Tracking**: Monitor where each asset is located
- **Cost Tracking**: Record purchase prices and current values
- **Portfolio Summary**: View total purchase value, current value, and gain/loss
- **Search & Filter**: Easily find assets by name, category, or location
- **Data Persistence**: All data stored locally in SQLite database
- **Professional UI**: Clean, modern interface with color-coded indicators

## Asset Information Tracked

- Asset Name
- Category (Electronics, Furniture, Vehicle, Real Estate, etc.)
- Description
- Location
- Purchase Price
- Current Value
- Purchase Date
- Condition (Excellent, Good, Fair, Poor, Needs Repair)
- Additional Notes

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python main.py
```

Or double-click [`run.bat`](run.bat:1) on Windows.

### Building Standalone Executable and Installer

For distribution, you can build a standalone executable and Windows installer:

1. Run the complete build script:
   ```bash
   build_all.bat
   ```
   This will create `dist/AssetManager.exe` and `installer/AssetManagerSetup.exe`

2. Or build just the installer (after building the executable):
   ```bash
   build_installer.bat
   ```

**Note:** Building the installer requires [Inno Setup](https://jrsoftware.org/isinfo.php) to be installed.

## Testing

Before building, verify everything works:

```bash
python test_app.py
```

This will test all components and confirm the application is ready.

## Building Standalone Executable

To create a standalone executable that can be installed on any desktop:

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Build the Executable

**Option A: Use the automated build script (Recommended)**
```bash
build_all.bat
```

**Option B: Manual build**
```bash
pyinstaller --onefile --windowed --name=AssetManager main.py
```

The executable will be created in the `dist/` folder as `AssetManager.exe`.

### Step 3: Test the Executable

Run `dist\AssetManager.exe` to verify it works correctly.

### Step 4: Create Windows Installer (Optional)

If you want to create a professional Windows installer:

1. Download and install [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Open [`setup.iss`](setup.iss:1) in Inno Setup
3. Click "Build" → "Compile"
4. The installer will be created in the `installer/` folder

**Important**: You must build the executable (Step 2) before compiling the installer!

## Usage

### Adding an Asset

1. Click the "➕ Add Asset" button or press `Ctrl+N`
2. Fill in the asset details:
   - Asset Name (required)
   - Category
   - Description
   - Location (required)
   - Purchase Price
   - Current Value
   - Purchase Date
   - Condition
   - Notes
3. Click "OK" to save

### Editing an Asset

1. Select an asset from the table
2. Click "✏️ Edit Selected" or press `Ctrl+E`
3. Modify the details
4. Click "OK" to save changes

### Deleting an Asset

1. Select an asset from the table
2. Click "🗑️ Delete Selected" or press `Delete`
3. Confirm the deletion

### Searching and Filtering

- Use the search box to find assets by name, category, or location
- Use the Category dropdown to filter by category
- Use the Location dropdown to filter by location
- Click "Clear Filters" to reset all filters

### Portfolio Summary

The summary section at the top shows:
- Total number of assets
- Total purchase value (sum of all purchase prices)
- Total current value (sum of all current values)
- Gain/Loss (difference between current and purchase values)

## Database

The application uses SQLite for data storage. The database file (`assets.db`) is created automatically in the application directory.

## Keyboard Shortcuts

- `Ctrl+N`: Add new asset
- `Ctrl+E`: Edit selected asset
- `Delete`: Delete selected asset
- `F5`: Refresh asset list
- `Ctrl+Q`: Exit application

## File Structure

```
Asset_Manager/
├── main.py           # Application entry point
├── ui.py             # User interface components
├── database.py       # Database operations
├── test_app.py       # Test script
├── build.py          # PyInstaller build script
├── build_all.bat     # Automated build script
├── run.bat           # Quick launcher
├── setup.iss         # Inno Setup installer script
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── assets.db         # SQLite database (created automatically)
```

## Build Process Summary

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Test the app**: `python test_app.py`
3. **Run the app**: `python main.py` or `run.bat`
4. **Build executable**: `build_all.bat` or `pyinstaller --onefile --windowed --name=AssetManager main.py`
5. **Test executable**: Run `dist\AssetManager.exe`
6. **Create installer** (optional): Open `setup.iss` in Inno Setup and compile

## Troubleshooting

### "PyQt5 not found" error
```bash
pip install PyQt5
```

### "PyInstaller not found" error
```bash
pip install pyinstaller
```

### Executable doesn't start
- Make sure you built it with `--windowed` flag
- Check that all dependencies are installed
- Run `python test_app.py` to verify components

### Installer compilation fails
- Build the executable first using `build_all.bat`
- Ensure `dist\AssetManager.exe` exists before compiling installer

## Technology Stack

- **Python 3.x**: Programming language
- **PyQt5**: GUI framework
- **SQLite**: Database
- **PyInstaller**: Executable packaging
- **Inno Setup**: Windows installer (optional)

## License

This is a free application for personal use.

## Support

For issues or questions, please refer to the documentation or contact the developer.
