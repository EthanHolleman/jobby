#!/usr/bin/env python
import sys
from jobby.interface import JobbyInterface

def main():
    interface = JobbyInterface()
    sys.exit(interface.cmdloop())

if __name__ == "__main__":
    main()
