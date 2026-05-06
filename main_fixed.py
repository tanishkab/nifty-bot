#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSL Certificate Fix Wrapper for main.py
This script fixes SSL certificate verification issues on macOS
"""
import os
import ssl
import warnings

# Disable SSL warnings
warnings.filterwarnings('ignore')

# Fix SSL certificate verification by disabling it
os.environ['PYTHONHTTPSVERIFY'] = '0'
ssl._create_default_https_context = ssl._create_unverified_context

# Disable urllib3 warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Monkey patch requests to disable SSL verification globally
import requests
from functools import partialmethod

# Save original methods
_original_request = requests.Session.request
_original_get = requests.get
_original_post = requests.post

# Create patched versions that disable verify
def patched_request(self, method, url, **kwargs):
    kwargs['verify'] = False
    return _original_request(self, method, url, **kwargs)

def patched_get(url, **kwargs):
    kwargs['verify'] = False
    return _original_get(url, **kwargs)

def patched_post(url, **kwargs):
    kwargs['verify'] = False
    return _original_post(url, **kwargs)

# Apply patches
requests.Session.request = patched_request
requests.get = patched_get
requests.post = patched_post

# Now run the main application
if __name__ == '__main__':
    with open('main.py', 'r', encoding='utf-8') as f:
        code = compile(f.read(), 'main.py', 'exec')
        exec(code, {'__name__': '__main__', '__file__': 'main.py'})