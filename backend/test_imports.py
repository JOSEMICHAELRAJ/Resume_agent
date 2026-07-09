#!/usr/bin/env python
"""Test which module is hanging on import"""

import sys
import time

print("Testing module imports...")

modules_to_test = [
    'routes.resume_routes',
    'routes.job_routes',
    'routes.matching_routes',
    'routes.candidate_routes',
]

for module in modules_to_test:
    print(f"\nImporting {module}...", flush=True)
    start = time.time()
    try:
        __import__(module)
        elapsed = time.time() - start
        print(f"✓ {module} imported in {elapsed:.2f}s", flush=True)
    except Exception as e:
        elapsed = time.time() - start
        print(f"✗ {module} failed after {elapsed:.2f}s: {e}", flush=True)

print("\n✓ All modules tested!")
