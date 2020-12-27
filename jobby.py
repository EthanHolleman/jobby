#!/usr/bin/env python

# Problem is that organizing jobs is annoying and hard
# Often one job ends up making number of child jobs that are related
# but distinct and things end up overlapping 
import sys
from jobby.interface import JobbyInterface

def main():
    interface = JobbyInterface()
    sys.exit(interface.cmdloop())

if __name__ == "__main__":
    main()
