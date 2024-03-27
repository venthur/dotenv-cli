"""Script to print all environment variables.

This is used internally for testing across all platforms.

"""


import os

for k, v in os.environ.items():
    print(f"{k}={v}")
