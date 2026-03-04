#!/usr/bin/env python3
"""
Skill wrapper for linkedin_drafter
Executes the LinkedIn drafter with HITL workflow
"""
import sys
from pathlib import Path

# Add skills directory to path
skills_dir = Path(__file__).parent.parent.parent.parent / 'skills'
sys.path.insert(0, str(skills_dir))

# Import and run the LinkedIn drafter
from linkedin_drafter import main

if __name__ == '__main__':
    main()
