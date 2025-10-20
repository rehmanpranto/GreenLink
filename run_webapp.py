#!/usr/bin/env python3
"""
GreenLink Campus Social Network - Quick Start Script
====================================================

This script automatically sets up and runs the GreenLink webapp.
It handles virtual environment creation, dependency installation,
database setup, and starts the development server.

Usage:
    python run_webapp.py

Requirements:
    - Python 3.8+
    - pip (Python package manager)
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class Colors:
    """ANSI color codes for colored terminal output"""
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

class GreenLinkRunner:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.venv_dir = self.project_dir / '.venv'
        self.is_windows = platform.system() == 'Windows'
        self.python_exe = self.get_python_executable()
        self.pip_exe = self.get_pip_executable()
        
    def print_header(self):
        """Print the GreenLink header"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}")
        print("=" * 60)
        print("🌿 GreenLink - Campus Social Network 🌿")
        print("   Facebook-Style University Platform")
        print("=" * 60)
        print(f"{Colors.END}")
        
    def print_step(self, step_num, total_steps, message):
        """Print a formatted step message"""
        print(f"\n{Colors.BLUE}[{step_num}/{total_steps}] {Colors.BOLD}{message}{Colors.END}")
        
    def print_success(self, message):
        """Print a success message"""
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
        
    def print_warning(self, message):
        """Print a warning message"""
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")
        
    def print_error(self, message):
        """Print an error message"""
        print(f"{Colors.RED}❌ {message}{Colors.END}")
        
    def check_python_version(self):
        """Check if Python version is compatible"""
        self.print_step(1, 8, "Checking Python version...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.print_error(f"Python 3.8+ required. Found: {version.major}.{version.minor}")
            sys.exit(1)
            
        self.print_success(f"Python {version.major}.{version.minor}.{version.micro} ✓")
        
    def get_python_executable(self):
        """Get the appropriate Python executable path"""
        if self.venv_dir.exists():
            if self.is_windows:
                return str(self.venv_dir / 'Scripts' / 'python.exe')
            else:
                return str(self.venv_dir / 'bin' / 'python')
        return sys.executable
        
    def get_pip_executable(self):
        """Get the appropriate pip executable path"""
        if self.venv_dir.exists():
            if self.is_windows:
                return str(self.venv_dir / 'Scripts' / 'pip.exe')
            else:
                return str(self.venv_dir / 'bin' / 'pip')
        return 'pip'
        
    def create_virtual_environment(self):
        """Create virtual environment if it doesn't exist"""
        self.print_step(2, 8, "Setting up virtual environment...")
        
        if self.venv_dir.exists():
            self.print_success("Virtual environment already exists")
            return
            
        try:
            subprocess.run([sys.executable, '-m', 'venv', str(self.venv_dir)], 
                         check=True, capture_output=True, text=True)
            self.print_success("Virtual environment created")
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to create virtual environment: {e}")
            sys.exit(1)
            
        # Update executables after creating venv
        self.python_exe = self.get_python_executable()
        self.pip_exe = self.get_pip_executable()
        
    def install_dependencies(self):
        """Install required Python packages"""
        self.print_step(3, 8, "Installing dependencies...")
        
        requirements_file = self.project_dir / 'requirements.txt'
        if not requirements_file.exists():
            self.print_error("requirements.txt not found")
            sys.exit(1)
            
        try:
            # Upgrade pip first
            subprocess.run([self.pip_exe, 'install', '--upgrade', 'pip'], 
                         check=True, capture_output=True, text=True)
            
            # Check if packages are already installed
            result = subprocess.run([self.pip_exe, 'list'], 
                                  check=True, capture_output=True, text=True)
            installed_packages = result.stdout.lower()
            
            # Check for Django (main package)
            if 'django' in installed_packages:
                self.print_success("Dependencies already installed")
                return
            
            # Install requirements
            subprocess.run([self.pip_exe, 'install', '-r', str(requirements_file)], 
                         check=True, capture_output=True, text=True)
            self.print_success("Dependencies installed")
        except subprocess.CalledProcessError as e:
            # If installation fails, check if Django is available anyway
            try:
                subprocess.run([self.python_exe, '-c', 'import django; print("Django available")'], 
                             check=True, capture_output=True, text=True)
                self.print_warning("Some dependency installation issues, but Django is available")
            except subprocess.CalledProcessError:
                self.print_error(f"Failed to install dependencies: {e}")
                sys.exit(1)
            
    def setup_environment_file(self):
        """Create .env file if it doesn't exist"""
        self.print_step(4, 8, "Setting up environment configuration...")
        
        env_file = self.project_dir / '.env'
        env_example = self.project_dir / '.env.example'
        
        if env_file.exists():
            self.print_success("Environment file already exists")
            return
            
        if env_example.exists():
            shutil.copy(env_example, env_file)
            self.print_success("Environment file created from example")
        else:
            # Create basic .env file
            env_content = """# GreenLink Environment Configuration
SECRET_KEY=django-insecure-development-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
"""
            with open(env_file, 'w') as f:
                f.write(env_content)
            self.print_success("Basic environment file created")
            
    def check_manage_py(self):
        """Check if manage.py exists"""
        manage_py = self.project_dir / 'manage.py'
        if not manage_py.exists():
            self.print_error("manage.py not found. Are you in the correct directory?")
            sys.exit(1)
            
    def run_migrations(self):
        """Run Django database migrations"""
        self.print_step(5, 8, "Setting up database...")
        
        try:
            # Make migrations
            subprocess.run([self.python_exe, 'manage.py', 'makemigrations'], 
                         check=True, capture_output=True, text=True, cwd=self.project_dir)
            
            # Apply migrations
            subprocess.run([self.python_exe, 'manage.py', 'migrate'], 
                         check=True, capture_output=True, text=True, cwd=self.project_dir)
            
            self.print_success("Database setup complete")
        except subprocess.CalledProcessError as e:
            self.print_error(f"Database setup failed: {e}")
            sys.exit(1)
            
    def collect_static_files(self):
        """Collect static files"""
        self.print_step(6, 8, "Collecting static files...")
        
        try:
            subprocess.run([self.python_exe, 'manage.py', 'collectstatic', '--noinput'], 
                         check=True, capture_output=True, text=True, cwd=self.project_dir)
            self.print_success("Static files collected")
        except subprocess.CalledProcessError:
            self.print_warning("Static files collection failed (this is usually okay for development)")
            
    def create_superuser_prompt(self):
        """Prompt to create superuser"""
        self.print_step(7, 8, "Admin user setup...")
        
        print(f"\n{Colors.YELLOW}Would you like to create an admin user? (y/n): {Colors.END}", end='')
        response = input().strip().lower()
        
        if response in ['y', 'yes']:
            try:
                subprocess.run([self.python_exe, 'manage.py', 'createsuperuser'], 
                             cwd=self.project_dir)
                self.print_success("Admin user created")
            except subprocess.CalledProcessError:
                self.print_warning("Admin user creation cancelled or failed")
        else:
            self.print_success("Skipped admin user creation")
            
    def start_server(self):
        """Start the Django development server"""
        self.print_step(8, 8, "Starting development server...")
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}")
        print("🚀 GreenLink is starting up!")
        print("📱 Opening at: http://127.0.0.1:8000")
        print("🔧 Admin panel: http://127.0.0.1:8000/admin")
        print(f"\n{Colors.YELLOW}Press Ctrl+C to stop the server{Colors.END}")
        print("=" * 50)
        
        try:
            # Try to open browser
            import webbrowser
            webbrowser.open('http://127.0.0.1:8000')
        except:
            pass
            
        try:
            subprocess.run([self.python_exe, 'manage.py', 'runserver'], 
                         cwd=self.project_dir)
        except KeyboardInterrupt:
            print(f"\n\n{Colors.GREEN}👋 GreenLink server stopped. Thanks for using GreenLink!{Colors.END}")
        except subprocess.CalledProcessError as e:
            self.print_error(f"Server failed to start: {e}")
            
    def run(self):
        """Main execution method"""
        try:
            self.print_header()
            self.check_python_version()
            self.check_manage_py()
            self.create_virtual_environment()
            self.install_dependencies()
            self.setup_environment_file()
            self.run_migrations()
            self.collect_static_files()
            self.create_superuser_prompt()
            self.start_server()
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Setup cancelled by user{Colors.END}")
            sys.exit(1)
        except Exception as e:
            self.print_error(f"Unexpected error: {e}")
            sys.exit(1)

def main():
    """Entry point"""
    runner = GreenLinkRunner()
    runner.run()

if __name__ == '__main__':
    main()
