import argparse
import json
import os

from bsky import fetch_likes

def main(args):
    stop_at = args.stop_at

    existing = []
    if args.json_out and os.path.exists(args.json_out):
        existing = json.loads(open(args.json_out, 'r').read())
        if not stop_at:
            stop_at = max([i['value']['createdAt'] for i in existing])
            print(f'Using stop_at from existing JSON: {stop_at}')
        

    out = fetch_likes(args.user, limit=args.limit, stop_at=stop_at)

    if args.json_out:
        total = out + existing
        open(args.json_out, 'w').write(json.dumps(total))
        print(f'Added {len(out)} items to {len(existing)} items: totaling {len(total)}')
    else:
        print(json.dumps(out))


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('user')
    a.add_argument('--limit', type=int, default=-1)
    a.add_argument('--stop-at', default=None)
    a.add_argument('--json-out', default=None)
    args = a.parse_args()

    main(args)