import argparse
from bsky import fetch_likes

def main(args):
    print(fetch_likes(args.user, limit=args.limit, stop_at=args.stop_at))


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('user')
    a.add_argument('--limit', type=int, default=-1)
    a.add_argument('--stop-at', default=None)
    args = a.parse_args()

    main(args)