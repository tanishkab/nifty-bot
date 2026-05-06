#!/usr/bin/env python3
"""
Wrapper script to run main.py with warnings suppressed
"""
import warnings
import os
import sys

# Suppress SSL warnings
warnings.filterwarnings('ignore', category=UserWarning, module='urllib3')
warnings.filterwarnings('ignore')

# Set environment variables to suppress version checks
os.environ['SYSTEM_VERSION_COMPAT'] = '0'

# Import and run the main app
try:
    # Execute main.py in the current namespace
    with open('main.py', 'r', encoding='utf-8') as f:
        code = f.read()
    exec(code)
except Exception as e:
    print(f"Error running application: {e}")
    sys.exit(1)