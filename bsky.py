import requests
import arrow
import math
import time
import urllib.parse
from dataclasses import dataclass

def list_likes(user, limit=100, cursor=None):
    params = {
        'repo': user,
        'collection': 'app.bsky.feed.like',
        'limit': str(limit)
    }
    if cursor:
        params['cursor'] = cursor

    r = requests.get('https://bsky.social/xrpc/com.atproto.repo.listRecords?' + urllib.parse.urlencode(params))
    if r.status_code // 100 != 2:
        raise Exception(f'error status code: {r.status_code} {r.text} {params}')
    
    return r.json()

@dataclass
class AtUri:
    repo: str
    collection: str
    rkey: str

    @staticmethod
    def parse(uri):
        if not uri.startswith('at://'):
            return None
        parts = uri[len('at://'):]
        parts = parts.split('/', 2)
        return AtUri(repo=parts[0], collection=parts[1], rkey=parts[2])

def get_post(uri, cid):
    ref = AtUri.parse(uri)
    params = {
        'repo': ref.repo,
        'collection': ref.collection,
        'rkey': ref.rkey,
        'cid': cid
    }

    r = requests.get('https://bsky.social/xrpc/com.atproto.repo.getRecord?' + urllib.parse.urlencode(params))
    if r.status_code // 100 != 2:
        raise Exception(f'error status code: {r.status_code} {r.text} {params}')
    
    return r.json()

def fetch_likes(user, limit=100, stop_at=None):
    if limit <= 0:
        limit = math.inf
    chunk_size = min(limit, 100)
    stop_time = arrow.get(stop_at) if stop_at else None

    likes = []
    cursor = None

    remaining = limit
    while remaining > 0:
        out = list_likes(user, chunk_size, cursor=cursor)
        new_likes = out.get('records', [])

        exit = False
        for like in new_likes:
            created_ts = arrow.get(like['value']['createdAt'])
            if stop_time and created_ts <= stop_time:
                exit = True
                break
            post = get_post(like['value']['subject']['uri'], like['value']['subject']['cid'])
            if post:
                like['value']['subject'] = post
            likes.append(like)
            remaining -= 1
            time.sleep(0.0005 * limit)
        
        if 'cursor' not in out or out['cursor'] == cursor:
            exit = True
        
        if exit:
            break

        cursor = out['cursor']
    
    return likes


