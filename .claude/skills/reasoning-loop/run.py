#!/usr/bin/env python3
"""
Skill wrapper for reasoning_loop
Executes the reasoning loop to generate plans
"""
import sys
from pathlib import Path

# Add skills directory to path
skills_dir = Path(__file__).parent.parent.parent.parent / 'skills'
sys.path.insert(0, str(skills_dir))

# Import and run the reasoning loop
from reasoning_loop import main

if __name__ == '__main__':
    main()
