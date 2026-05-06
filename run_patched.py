
#!/usr/bin/env python3
"""
Patched launcher for main.py that bypasses macOS version checks
"""
import warnings
import sys
import os

# Suppress all warnings
warnings.filterwarnings('ignore')

# Patch platform module to report a compatible macOS version
import platform
_original_mac_ver = platform.mac_ver

def patched_mac_ver(release='', versioninfo=('', '', ''), machine=''):
    """Return a patched macOS version"""
    original_release, original_versioninfo, original_machine = _original_mac_ver(release, versioninfo, machine)
    # Report macOS 15.0.7 (1507) instead of the actual version
    patched_release = '15.0.7'
    patched_versioninfo = ('15', '0', '7')
    return patched_release, patched_versioninfo, original_machine or machine

platform.mac_ver = patched_mac_ver

# Also patch sys.platform if needed
os.environ['SYSTEM_VERSION_COMPAT'] = '0'

# Now import and run main
if __name__ == '__main__':
    print("Starting Nifty Auto Trader with patched macOS version...")
    with open('main.py', 'r', encoding='utf-8') as f:
        code = compile(f.read(), 'main.py', 'exec')
        exec(code, {'__name__': '__main__', '__file__': 'main.py'})