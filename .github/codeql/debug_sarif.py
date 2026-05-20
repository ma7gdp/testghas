#!/usr/bin/env python3
import json

with open('results/python.sarif', encoding='utf-8') as f:
    data = json.load(f)

print("\n=== SARIF Results Debug ===\n")
for run in data.get('runs', []):
    for i, r in enumerate(run.get('results', [])):
        print(f"Result {i}:")
        print(f"  ruleId: {r.get('ruleId')}")
        print(f"  message: {r.get('message')}")
        print()
