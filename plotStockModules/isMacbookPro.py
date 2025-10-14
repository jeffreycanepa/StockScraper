# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   isMacbootPro.py
-       This script looks up the Mac model identifier to determine
-       if the script is running on a MacBook Pro. This can be used
-       to adjust the DPI settings for matplotlib to improve the
-       appearance of plots on high-resolution MacBook Pro displays.
-
-   Required Packages (required in imported Modules):
-       platform: built-in
-       subprocess: built-in
-
-   Required Modules:
-
-   Methods:
-       get_mac_model()
-       is_macbook_pro()
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Oct 2025
--------------------------------------------------------------
'''
import platform
import subprocess
 
def get_mac_model():
    """
    Returns the Mac model identifier (e.g., 'MacBookPro16,1') if on macOS, 
    otherwise returns None.
    """
    if platform.system() == 'Darwin':
        # Command to get the Model Identifier (e.g., "MacBookPro16,1")
        cmd = ["system_profiler", "SPHardwareDataType"]
        try:
            output = subprocess.check_output(cmd, encoding='utf-8').strip()
            for line in output.splitlines():
                if "Model Identifier" in line:
                    # Extract the identifier part
                    model_identifier = line.split(":")[-1].strip()
                    return model_identifier
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Handle cases where the command fails (unlikely on a standard Mac)
            return None
    return None

def is_macbook_pro():
    """Checks if the script is running on a MacBook Pro."""
    model = get_mac_model()
    if model and model.startswith('MacBookPro'):
        return True
    return False

