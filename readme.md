## Installation & Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
   *(Note 1: On Linux/macOS, you may need to use `python3` instead of `python`)*  
   *(Note 2: On Windows, if `python` is not recognized, try using `py` instead)*

2. **Activate the virtual environment:**
   * **Windows (PowerShell):**
     ```powershell
     venv\Scripts\Activate.ps1
     ```
   * **Windows (CMD):**
     ```cmd
     venv\Scripts\activate.bat
     ```
   * **Linux / macOS:**
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
