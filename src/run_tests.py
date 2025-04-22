#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

def find_repo_root():
    """
    Walk upwards from this script's directory until we find a folder
    containing both src/main/python and src/test/python.
    """
    dir_ = Path(__file__).resolve().parent
    while dir_ != dir_.parent:
        if (dir_ / 'src' / 'main'  / 'python').is_dir() and \
           (dir_ / 'src' / 'test'  / 'python').is_dir():
            return dir_
        dir_ = dir_.parent
    return None

def main():
    repo_root = find_repo_root()
    if not repo_root:
        print("ERROR: Could not locate src/main/python and src/test/python in any ancestor of", __file__)
        sys.exit(1)

    src_main = repo_root / 'src' / 'main'  / 'python'
    src_test = repo_root / 'src' / 'test'  / 'python'

    # Insert application and test roots onto sys.path
    sys.path.insert(0, str(src_main))
    sys.path.insert(0, str(src_test))

    # Discover and run all test_*.py under src_test
    loader = unittest.TestLoader()
    suite  = loader.discover(start_dir=str(src_test), pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)

if __name__ == "__main__":
    main()
