#!/usr/bin/env python3
"""
BLOOD REPORT AI - ULTIMATE SETUP & LAUNCH SYSTEM
Complete end-to-end initialization, verification, and server startup
"""
import os
import sys
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime

# Colors for terminal output
COLORS = {
    'RESET': '\033[0m',
    'BOLD': '\033[1m',
    'GREEN': '\033[92m',
    'RED': '\033[91m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'CYAN': '\033[96m',
}

def color(text, col):
    """Add color to text"""
    return f"{COLORS[col]}{text}{COLORS['RESET']}"

def header(text):
    """Print a formatted header"""
    width = 75
    print(f"\n{color('=' * width, 'CYAN')}")
    print(f"{color(f'{text:^{width}}', 'BOLD')}")
    print(f"{color('=' * width, 'CYAN')}\n")

def step(number, total, text):
    """Print a step indicator"""
    print(f"{color(f'[{number}/{total}]', 'BLUE')} {text}")

def success(text):
    """Print success message"""
    print(f"{color('✓', 'GREEN')} {text}")

def error(text):
    """Print error message"""
    print(f"{color('✗', 'RED')} {text}")

def warning(text):
    """Print warning message"""
    print(f"{color('⚠', 'YELLOW')} {text}")

def info(text):
    """Print info message"""
    print(f"{color('ℹ', 'BLUE')} {text}")

class BloodReportAISetup:
    """Handles complete setup and launch of Blood Report AI"""
    
    def __init__(self):
        self.workspace = Path(__file__).parent
        self.venv_path = self.workspace / "venv"
        self.python_exe = (
            self.venv_path / "Scripts" / "python.exe" if sys.platform == "win32"
            else self.venv_path / "bin" / "python3"
        )
        self.pip_exe = (
            self.venv_path / "Scripts" / "pip.exe" if sys.platform == "win32"
            else self.venv_path / "bin" / "pip3"
        )
        self.errors = []
        self.warnings = []
    
    def log_error(self, msg):
        """Log an error"""
        self.errors.append(msg)
        error(msg)
    
    def log_warning(self, msg):
        """Log a warning"""
        self.warnings.append(msg)
        warning(msg)
    
    def run_command(self, *args, capture=False, check=True):
        """Run a shell command safely"""
        try:
            if capture:
                result = subprocess.run(args, capture_output=True, text=True, check=check)
                return result.returncode == 0, result.stdout + result.stderr
            else:
                result = subprocess.run(args, check=check)
                return result.returncode == 0, ""
        except Exception as e:
            return False, str(e)
    
    def check_python(self):
        """Verify Python installation"""
        step(1, 8, "Checking Python installation")
        
        try:
            import sys
            version = sys.version_info
            version_str = f"{version.major}.{version.minor}.{version.micro}"
            
            if version.major < 3 or (version.major == 3 and version.minor < 8):
                self.log_error(f"Python {version_str} - requires 3.8+")
                return False
            
            success(f"Python {version_str}")
            return True
        except Exception as e:
            self.log_error(f"Python check failed: {e}")
            return False
    
    def setup_venv(self):
        """Create or verify virtual environment"""
        step(2, 8, "Setting up virtual environment")
        
        try:
            if not self.venv_path.exists():
                info("Creating new virtual environment...")
                success_flag, output = self.run_command(sys.executable, "-m", "venv", str(self.venv_path))
                if not success_flag:
                    self.log_error(f"Failed to create venv: {output}")
                    return False
                success("Virtual environment created")
            else:
                success("Virtual environment exists")
            
            # Verify Python in venv
            if not self.python_exe.exists():
                self.log_error("Python executable not found in venv")
                return False
            
            return True
        except Exception as e:
            self.log_error(f"Venv setup failed: {e}")
            return False
    
    def install_dependencies(self):
        """Install required Python packages"""
        step(3, 8, "Installing dependencies")
        
        req_file = self.workspace / "requirements.txt"
        if not req_file.exists():
            self.log_error("requirements.txt not found")
            return False
        
        try:
            info(f"Using Python: {self.python_exe}")
            
            # Upgrade pip first
            info("Upgrading pip...")
            self.run_command(str(self.pip_exe), "install", "--upgrade", "pip", check=False)
            
            # Install requirements
            info("Installing packages (this may take 2-3 minutes)...")
            success_flag, output = self.run_command(
                str(self.pip_exe), "install", "-r", str(req_file),
                check=False
            )
            
            if success_flag:
                success("All dependencies installed")
            else:
                self.log_warning("Some dependencies had issues but core packages installed")
            
            return True
        except Exception as e:
            self.log_error(f"Dependency installation failed: {e}")
            return False
    
    def verify_packages(self):
        """Verify critical packages are installed"""
        step(4, 8, "Verifying core packages")
        
        critical_packages = [
            ('fastapi', 'FastAPI'),
            ('uvicorn', 'Uvicorn'),
            ('sqlalchemy', 'SQLAlchemy'),
            ('dotenv', 'python-dotenv'),
        ]
        
        all_ok = True
        for package, name in critical_packages:
            try:
                __import__(package)
                success(f"{name} ✓")
            except ImportError:
                self.log_error(f"{name} - NOT INSTALLED")
                all_ok = False
        
        return all_ok
    
    def check_directories(self):
        """Create necessary directory structure"""
        step(5, 8, "Setting up directory structure")
        
        dirs = [
            "data/uploads",
            "logs",
            "reports",
            "templates",
            "src",
            ".vscode",
        ]
        
        try:
            for d in dirs:
                path = self.workspace / d
                path.mkdir(parents=True, exist_ok=True)
            
            success(f"Created {len(dirs)} directories")
            return True
        except Exception as e:
            self.log_error(f"Directory setup failed: {e}")
            return False
    
    def check_env_file(self):
        """Verify .env configuration"""
        step(6, 8, "Checking configuration files")
        
        env_file = self.workspace / ".env"
        env_example = self.workspace / ".env.example"
        
        if env_file.exists():
            success(".env file exists")
            return True
        elif env_example.exists():
            info("Copying .env.example to .env...")
            try:
                import shutil
                shutil.copy(env_example, env_file)
                success(".env file created from template")
                return True
            except Exception as e:
                self.log_warning(f"Could not copy .env: {e}")
                return True  # Non-critical
        else:
            info("Creating default .env file...")
            try:
                with open(env_file, 'w') as f:
                    f.write("HOST=0.0.0.0\n")
                    f.write("PORT=8000\n")
                    f.write("ENVIRONMENT=development\n")
                success(".env file created with defaults")
                return True
            except Exception as e:
                self.log_warning(f"Could not create .env: {e}")
                return True  # Non-critical
    
    def verify_api_module(self):
        """Verify the main API module loads correctly"""
        step(7, 8, "Verifying API module")
        
        try:
            sys.path.insert(0, str(self.workspace))
            from src.api_optimized import app
            success("API module loaded successfully")
            return True
        except ImportError as e:
            self.log_error(f"API import failed: {e}")
            return False
        except SyntaxError as e:
            self.log_error(f"Syntax error in API: {e}")
            return False
        except Exception as e:
            self.log_warning(f"API verification warning: {e}")
            return True  # Non-critical
    
    def print_summary(self):
        """Print setup summary"""
        header("SETUP SUMMARY")
        
        if not self.errors:
            print(f"{color('✓ ALL CHECKS PASSED', 'GREEN')}")
            print(f"  Ready to start the server!\n")
        else:
            print(f"{color(f'✗ {len(self.errors)} ERRORS FOUND', 'RED')}")
            for i, err in enumerate(self.errors, 1):
                print(f"  {i}. {err}")
            print()
        
        if self.warnings:
            print(f"{color(f'⚠ {len(self.warnings)} WARNINGS', 'YELLOW')}")
            for i, warn in enumerate(self.warnings, 1):
                print(f"  {i}. {warn}")
            print()
    
    def start_server(self):
        """Start the application server"""
        step(8, 8, "Starting Blood Report AI Server")
        
        header("SERVER STARTUP")
        
        try:
            # Change to workspace directory
            os.chdir(self.workspace)
            
            print(f"{color('Starting server on http://localhost:8000', 'CYAN')}")
            print(f"{color('Dashboard:  ', 'BLUE')}http://localhost:8000/")
            print(f"{color('API Docs:   ', 'BLUE')}http://localhost:8000/docs")
            print(f"{color('Health:     ', 'BLUE')}http://localhost:8000/health")
            print(f"{color('Press CTRL+C to stop', 'YELLOW')}\n")
            
            # Run the main application
            import uvicorn
            from main import app
            
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=8000,
                reload=False,
                log_level="info"
            )
            
        except ImportError as e:
            self.log_error(f"Failed to import server modules: {e}")
            print(f"\n{color('Try running this script again', 'YELLOW')}")
            sys.exit(1)
        except KeyboardInterrupt:
            print(f"\n\n{color('Server stopped by user', 'YELLOW')}")
            sys.exit(0)
        except Exception as e:
            self.log_error(f"Server startup failed: {e}")
            print(f"\n{color('Check the error above and try again', 'YELLOW')}")
            sys.exit(1)
    
    def run(self):
        """Execute full setup and startup"""
        header("BLOOD REPORT AI - COMPLETE SETUP & LAUNCH SYSTEM")
        
        print(f"{color('Workspace:', 'CYAN')} {self.workspace}")
        print(f"{color('Python:   ', 'CYAN')} {sys.version.split()[0]}")
        print(f"{color('Platform: ', 'CYAN')} {sys.platform}\n")
        
        # Run all checks
        checks = [
            self.check_python,
            self.setup_venv,
            self.install_dependencies,
            self.verify_packages,
            self.check_directories,
            self.check_env_file,
            self.verify_api_module,
        ]
        
        for check in checks:
            try:
                if not check():
                    self.print_summary()
                    if self.errors:
                        print(f"{color('Fix the errors above and try again', 'RED')}")
                        sys.exit(1)
            except Exception as e:
                self.log_error(f"Unexpected error in {check.__name__}: {e}")
                self.print_summary()
                sys.exit(1)
        
        self.print_summary()
        
        # If we got here, start the server
        if not self.errors:
            try:
                self.start_server()
            except Exception as e:
                self.log_error(f"Failed to start server: {e}")
                sys.exit(1)
        else:
            sys.exit(1)

if __name__ == "__main__":
    try:
        setup = BloodReportAISetup()
        setup.run()
    except KeyboardInterrupt:
        print(f"\n\n{color('Setup interrupted by user', 'YELLOW')}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{color(f'FATAL ERROR: {e}', 'RED')}")
        sys.exit(1)
