# this program is to install all required libraries using pip
# if you know how to install the required libraries, you can ignore this program

import subprocess
import sys

def install(pkg):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])

def main():
    packages = ['numpy',
        'matplotlib',
        'open3d',
        'wxPython',
        'pynrrd',
        'typing-extensions']
    for pkg in packages:
        install(pkg)

if __name__ == '__main__':
    main()
