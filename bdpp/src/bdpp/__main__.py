"""BD++ CLI entry point.

Subcommands:
  search     Run a discovery search and append results to the queue.
  enrich     Process DISCOVERED rows in the queue, mark ENRICHED. Budget-capped.
  export     Export ENRICHED rows to CSV.
  queue      Show queue status.
  all        Convenience: search + enrich + export in one go.
"""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from .config import Credentials, SearchConfig, CONFIG_DIR
from .engine import run_search, stage_search, stage_enrich, stage_output
from . import queue as q


def cmd_search(args):
    creds = Credentials.load(Path(args.credentials))
    search = SearchConfig.load(Path(args.config))
    result = asyncio.run(stage_search(search, creds))
    print(json.dumps(result, indent=2))


def cmd_enrich(args):
    creds = Credentials.load(Path(args.credentials))
    result = asyncio.run(stage_enrich(creds, max_companies=args.max_companies, max_spend_usd=args.max_spend))
    print(json.dumps(result, indent=2))


def cmd_export(args):
    search = SearchConfig.load(Path(args.config))
    status = args.status
    result = stage_output(search, status_filter=status, mark_as_exported=not args.keep_status)
    print(json.dumps(result, indent=2))


def cmd_queue(args):
    print(json.dumps(q.queue_counts(), indent=2))
    if args.show:
        rows = q.list_queue(status=args.status, limit=args.show)
        for r in rows:
            print(f"  [{r['status']:10s}] #{r['id']:4d} {r['company_name'][:30]:30s} | {(r['bd_job_title'] or '')[:35]:35s} | {r['bd_job_location'] or ''}")


def cmd_clear(args):
    if args.confirm == "YES":
        q.clear_all()
        print("Queue cleared.")
    else:
        print("Pass --confirm YES to actually clear.")


def cmd_all(args):
    creds = Credentials.load(Path(args.credentials))
    search = SearchConfig.load(Path(args.config))
    csv_path, summary = asyncio.run(run_search(search, creds, max_rows_companies=args.max_companies))
    print(json.dumps(summary, indent=2))
    print(f"\nCSV: {csv_path}")


def main():
    p = argparse.ArgumentParser(prog="bdpp")
    p.add_argument("--credentials", default=str(CONFIG_DIR / "credentials.toml"))
    sub = p.add_subparsers(dest="cmd", required=False)

    sp = sub.add_parser("search", help="Discovery only")
    sp.add_argument("--config", required=True)
    sp.set_defaults(fn=cmd_search)

    sp = sub.add_parser("enrich", help="Enrich queue")
    sp.add_argument("--max-companies", type=int, default=50)
    sp.add_argument("--max-spend", type=float, default=6.0)
    sp.set_defaults(fn=cmd_enrich)

    sp = sub.add_parser("export", help="Export queue to CSV")
    sp.add_argument("--config", required=True)
    sp.add_argument("--status", default="ENRICHED",
                    choices=["DISCOVERED", "ENRICHED", "EXPORTED", "ENRICHED_AND_DISCOVERED"])
    sp.add_argument("--keep-status", action="store_true", help="Don't mark as EXPORTED")
    sp.set_defaults(fn=cmd_export)

    sp = sub.add_parser("queue", help="Show queue status")
    sp.add_argument("--show", type=int, default=0, help="Show N rows (default 0)")
    sp.add_argument("--status", default=None)
    sp.set_defaults(fn=cmd_queue)

    sp = sub.add_parser("clear", help="Clear the queue (admin)")
    sp.add_argument("--confirm", default="")
    sp.set_defaults(fn=cmd_clear)

    sp = sub.add_parser("all", help="Search + Enrich + Export")
    sp.add_argument("--config", required=True)
    sp.add_argument("--max-companies", type=int, default=50)
    sp.set_defaults(fn=cmd_all)

    # Backwards-compat: if no subcommand, treat as 'all' if --config is given
    p.add_argument("--config", help=argparse.SUPPRESS)
    p.add_argument("--max-companies", type=int, default=50, help=argparse.SUPPRESS)
    args = p.parse_args()

    if args.cmd is None:
        if args.config:
            args.fn = cmd_all
        else:
            p.print_help()
            return
    args.fn(args)


if __name__ == "__main__":
    main()
