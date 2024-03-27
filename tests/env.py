"""Script to print all environment variables.

This is used internally for testing across all platforms.

"""


import os

for k, v in os.environ.items():
    # python set's this variable on startup
    if k == "LC_CTYPE":
        continue
    print(f"{k}={v}")
