"""
Environment setup script for the African Medical Chatbot
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_virtual_environment():
    """Create virtual environment"""
    print("🔧 Creating virtual environment...")
    
    if not os.path.exists("venv"):
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment already exists")

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    
    # Determine pip command based on OS
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix-like
        pip_cmd = "venv/bin/pip"
    
    # Install requirements
    subprocess.run([pip_cmd, "install", "-r", "requirements.txt"])
    print("✅ Requirements installed")

def setup_database():
    """Set up the database"""
    print("🗄️ Setting up database...")
    
    # Create database directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # The database will be created automatically when the app runs
    print("✅ Database setup complete")

def setup_environment_file():
    """Set up environment configuration"""
    print("⚙️ Setting up environment configuration...")
    
    if not os.path.exists(".env"):
        shutil.copy(".env.example", ".env")
        print("✅ Environment file created from example")
        print("🔧 Please edit .env file with your configuration")
    else:
        print("✅ Environment file already exists")

def download_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    
    try:
        import nltk
        nltk.download('vader_lexicon', quiet=True)
        print("✅ NLTK data downloaded")
    except ImportError:
        print("⚠️ NLTK not installed, skipping data download")

def setup_directories():
    """Create necessary directories"""
    print("📁 Setting up directories...")
    
    directories = [
        "data",
        "logs",
        "models",
        "backend",
        "frontend_streamlit",
        "tests"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Directories created")

def check_system_requirements():
    """Check system requirements"""
    print("🔍 Checking system requirements...")
    
    requirements_met = True
    
    # Check available memory
    try:
        import psutil
        memory_gb = psutil.virtual_memory().total / (1024**3)
        if memory_gb < 8:
            print(f"⚠️ Warning: Only {memory_gb:.1f}GB RAM available. 8GB+ recommended for LLM.")
        else:
            print(f"✅ Memory: {memory_gb:.1f}GB available")
    except ImportError:
        print("⚠️ Cannot check memory requirements (psutil not installed)")
    
    # Check for GPU
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️ No GPU detected. CPU inference will be slower.")
    except ImportError:
        print("⚠️ Cannot check GPU availability (torch not installed)")
    
    return requirements_met

def main():
    """Main setup function"""
    print("🚀 Setting up African Medical Chatbot Environment")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup steps
    setup_directories()
    create_virtual_environment()
    install_requirements()
    setup_environment_file()
    setup_database()
    download_nltk_data()
    check_system_requirements()
    
    print("\n" + "="*50)
    print("🎉 Setup complete!")
    print("="*50)
    
    print("\n📋 Next steps:")
    print("1. Edit .env file with your Hugging Face API token")
    print("2. Activate virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("3. Start the backend server:")
    print("   python -m backend.main")
    print("4. In another terminal, start the frontend:")
    print("   streamlit run frontend_streamlit/app.py")
    print("   # OR for React frontend:")
    print("   npm run dev")

if __name__ == "__main__":
    main()