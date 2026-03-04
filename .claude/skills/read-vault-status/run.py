#!/usr/bin/env python3
"""
Skill wrapper for read_vault_status
Displays current vault status
"""
import sys
from pathlib import Path

# Add skills directory to path
skills_dir = Path(__file__).parent.parent.parent.parent / 'skills'
sys.path.insert(0, str(skills_dir))

# Import and run read_vault_status
from read_vault_status import main

if __name__ == '__main__':
    main()
