# VS Code Configuration & Python Interpreter Setup Guide

## Problem Resolved
Fixed: "Unable to handle c:\Users\rakes\Downloads\blood report ai\_archive\BACKEND\.venv\Scripts\python.exe"

This error occurred because VS Code was configured to use a Python interpreter from an archived/old folder that no longer exists or is not accessible.

## Solution Applied

### 1. Updated VS Code Settings
Created `.vscode/settings.json` with:
- Correct Python interpreter path (system Python or venv)
- Proper linting and formatting configuration
- Correct Python path analysis settings

### 2. Added Launch Configuration
Created `.vscode/launch.json` with:
- FastAPI server launch configuration
- Main server launch configuration
- Current file debugging option

### 3. Current Environment
```
Python Version: 3.13.5
Active Interpreter: System Python
Status: ✅ Working correctly
```

## How to Fix the Archive Folder Reference

### Option 1: Clean Up Archive Folder (Recommended)
```powershell
cd "c:\Users\rakes\Downloads\blood report ai"
Remove-Item -Path "_archive" -Recurse -Force
```

### Option 2: Manually Configure Python in VS Code
1. Open Command Palette: `Ctrl+Shift+P`
2. Type: "Python: Select Interpreter"
3. Choose the system Python or create a new venv:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Option 3: Reset VS Code Settings
1. Delete `.vscode` folder
2. Restart VS Code
3. VS Code will auto-detect Python interpreter

## Verification

Run this to verify everything is working:
```powershell
python verify_vercel_deployment.py
python app.py  # Should start without errors
```

## Recommended Python Setup

### Using System Python (Current)
✅ Already configured and working
- Python: 3.13.5
- No virtual environment needed

### Creating Virtual Environment (Optional)
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Then update `.vscode/settings.json`:
```json
"python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe"
```

## Troubleshooting

### Still Getting Archive Path Error?
1. **Check Global VS Code Settings**
   - File → Preferences → Settings
   - Search: "python.defaultInterpreterPath"
   - Remove any references to _archive or old paths

2. **Check Workspace File**
   - If a `.code-workspace` file exists, delete it
   - VS Code will use `.vscode/settings.json` instead

3. **Clear VS Code Cache**
   ```powershell
   Remove-Item -Path "$env:APPDATA\..\Local\Code\User\workspaceStorage" -Recurse -Force
   ```

4. **Restart VS Code**
   - Close completely
   - Reopen the workspace

### Python Not Found?
```powershell
# Verify Python is installed
python --version

# Or specify full path
C:\Users\rakes\AppData\Local\Programs\Python\Python313\python.exe --version
```

## Files Modified
- ✅ `.vscode/settings.json` - Created with correct Python path
- ✅ `.vscode/launch.json` - Created with debug configurations

## Next Steps
1. Close and reopen VS Code
2. Verify no errors in Python extension
3. Try running: `python app.py`
4. Optional: Delete `_archive` folder if it's no longer needed

---

**Status:** ✅ VS Code Python configuration fixed and ready to use
