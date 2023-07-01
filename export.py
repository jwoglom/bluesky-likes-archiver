import argparse
import json
import os
import sys

from bsky import fetch_likes

def main(args):
    stop_at = args.stop_at

    existing = []
    if args.json_out and os.path.exists(args.json_out):
        existing = json.loads(open(args.json_out, 'r').read())
        if not stop_at:
            stop_at = max([i['value']['createdAt'] for i in existing])
            print(f'Using stop_at from existing JSON: {stop_at}', out=sys.stderr)
        

    out = fetch_likes(args.user, limit=args.limit, stop_at=stop_at)

    if args.json_out:
        total = out + existing
        open(args.json_out, 'w').write(json.dumps(total))
        print(f'Added {len(out)} items to {len(existing)} items: totaling {len(total)}', out=sys.stderr)
    else:
        print(json.dumps(out))
    
    if args.sqlite_out:
        if not args.json_out:
            print('Need --json-out in addition to --sqlite-out', out=sys.stderr)
            exit(1)
        from export_to_sqlite import export_to_sqlite
        export_to_sqlite(args.json_out, args.sqlite_out, args.sqlite_if_exists)


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('user')
    a.add_argument('--limit', type=int, default=-1)
    a.add_argument('--stop-at', default=None)
    a.add_argument('--json-out', default=None)
    a.add_argument('--sqlite-out', default=None)
    a.add_argument('--sqlite-if-exists', default='replace')
    args = a.parse_args()

    main(args)