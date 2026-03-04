#!/usr/bin/env python3
"""
Skill wrapper for process_needs_action
Executes task processing from Needs_Action queue
"""
import sys
from pathlib import Path

# Add skills directory to path
skills_dir = Path(__file__).parent.parent.parent.parent / 'skills'
sys.path.insert(0, str(skills_dir))

# Import and run process_needs_action
from process_needs_action import main

if __name__ == '__main__':
    main()
