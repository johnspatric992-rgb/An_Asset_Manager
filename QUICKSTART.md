# Asset Manager - Quick Start Guide

## Fastest Way to Get Started

### Option 1: Run Directly (No Installation)

1. Open Command Prompt or PowerShell
2. Navigate to the Asset Manager folder
3. Run:
   ```bash
   python main.py
   ```

### Option 2: Use the Launcher (Windows)

Double-click [`run.bat`](run.bat:1) in the Asset Manager folder.

## First Time Setup

### Step 1: Install Python Dependencies

Open Command Prompt in the Asset Manager folder and run:

```bash
pip install -r requirements.txt
```

### Step 2: Test the Application

```bash
python test_app.py
```

You should see: "All tests passed! ✓"

### Step 3: Run the Application

```bash
python main.py
```

## Building for Distribution

### Create Standalone Executable

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build the executable:
   ```bash
   build_all.bat
   ```

3. Find your executable at: `dist\AssetManager.exe`

4. This executable can be copied to any Windows computer and run without Python installed!

### Create Windows Installer (Optional)

1. Install [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Build the executable first (see above)
3. Open [`setup.iss`](setup.iss:1) in Inno Setup
4. Click "Build" → "Compile"
5. Find installer at: `installer\AssetManager_Setup.exe`

## Using the Application

### Add Your First Asset

1. Click "➕ Add Asset" (or press `Ctrl+N`)
2. Fill in:
   - **Asset Name**: e.g., "MacBook Pro"
   - **Category**: Select from dropdown (e.g., "Electronics")
   - **Location**: e.g., "Home Office"
   - **Purchase Price**: e.g., 1500.00
   - **Current Value**: e.g., 1200.00
3. Click "OK"

### View Your Portfolio

The top section shows:
- **Total Assets**: Number of items
- **Total Purchase Value**: What you paid
- **Total Current Value**: What they're worth now
- **Gain/Loss**: Profit or loss

### Find Assets

- Type in the search box to find by name, category, or location
- Use dropdown filters to narrow by category or location
- Click "Clear Filters" to show all

### Edit or Delete

- Select an asset in the table
- Click "✏️ Edit" to modify
- Click "🗑️ Delete" to remove

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | Add new asset |
| `Ctrl+E` | Edit selected asset |
| `Delete` | Delete selected asset |
| `F5` | Refresh list |
| `Ctrl+Q` | Exit |

## Troubleshooting

### "python is not recognized"
- Install Python from https://python.org
- Check "Add Python to PATH" during installation

### "No module named PyQt5"
```bash
pip install PyQt5
```

### Application won't start
- Run `python test_app.py` to check for errors
- Ensure all dependencies are installed

### Need Help?
- Check [`README.md`](README.md:1) for detailed documentation
- Run `python test_app.py` to diagnose issues

## What's Next?

1. Add all your assets
2. Track their values over time
3. Build the executable for easy distribution
4. Create an installer for professional deployment

Enjoy managing your assets! 🎉
