"""Test to understand the Vilaine river path based on lock locations."""

import json
from pathlib import Path

# Load locks
with open('src/pdf_generator/locks.json', 'r') as f:
    locks_data = json.load(f)

print("Vilaine river path based on lock locations:")
print("=" * 50)

# Sort locks by longitude (west to east)
locks = sorted(locks_data['locks'], key=lambda x: x['longitude'])

for lock in locks:
    print(f"{lock['name']:<35} {lock['latitude']:.6f}, {lock['longitude']:.6f}")

print("\nThis shows the Vilaine flows from:")
print(f"  West: {locks[0]['name']} at {locks[0]['longitude']:.3f}")
print(f"  East: {locks[-1]['name']} at {locks[-1]['longitude']:.3f}")
print(f"  North: max latitude {max(l['latitude'] for l in locks):.3f}")
print(f"  South: min latitude {min(l['latitude'] for l in locks):.3f}")