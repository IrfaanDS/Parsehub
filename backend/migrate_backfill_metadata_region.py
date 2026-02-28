#!/usr/bin/env python3
"""
One-time migration: backfill metadata.region from project_name/title (trailing (APAC), (LATAM), (EMENA) etc.)
for rows where region IS NULL OR TRIM(region) = ''.

Run from backend directory:
  python migrate_backfill_metadata_region.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv()

from database import ParseHubDatabase


def main():
    print("Backfilling metadata.region from project_name/title...")
    db = ParseHubDatabase()
    result = db.backfill_metadata_region()
    print(f"Updated: {result['updated']}, Skipped: {result['skipped']}, Errors: {len(result['errors'])}")
    if result['errors']:
        for e in result['errors'][:10]:
            print(f"  - {e}")
        if len(result['errors']) > 10:
            print(f"  ... and {len(result['errors']) - 10} more")
    return 0 if not result['errors'] else 1


if __name__ == "__main__":
    sys.exit(main())
