#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from scripts.build_references import build

def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build NC-250 study references.")
    parser.add_argument("--source", default="Data Structures & Algorithms")
    parser.add_argument("--references", default="references")
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--no-export", action="store_true")
    return parser.parse_args()

def main() -> int:
    args = arguments()
    root = Path(__file__).resolve().parent
    try:
        result = build(
            repo_root=root,
            source_root=root / args.source,
            references_root=root / args.references,
            clean_first=args.clean,
            combined=not args.no_export,
        )
    except (OSError, ValueError, SyntaxError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1

    records = result["records"]
    print("NC-250 reference build complete.")
    print(f"  Problems discovered:       {len(records)}")
    print(f"  Solution references built: {len(result['solutions'])}")
    print(f"  Interview pages built:     {len(result['interviews'])}")
    print(f"  Missing solution refs:     {sum(r.solution_reference is None for r in records)}")
    print(f"  Missing interview refs:    {sum(r.interview_reference is None for r in records)}")
    print(f"  Study index:               {result['index']}")
    print(f"  Manifest:                  {result['manifest']}")
    if result["export"]:
        print(f"  Combined export:           {result['export']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
