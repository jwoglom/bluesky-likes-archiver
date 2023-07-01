#!/usr/bin/env python3
import pandas as pd
import numpy as np

import argparse
import sqlite3
import json

def export_to_sqlite(json_file, output_file, if_exists='replace'):
    df = pd.json_normalize(json.loads(open(json_file).read()))
    df = df.astype(str)
    df['value.createdAt', 'value.subject.value.createdAt'] = pd.to_datetime(df['value.createdAt', 'value.subject.value.createdAt'])

    conn = sqlite3.connect(output_file)
    df.to_sql('tweets', conn, if_exists=if_exists)
    conn.close()


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="Converts a JSON file containing bluesky likes into a sqlite3 database")
    ap.add_argument('--json-input-file', default='skeets.json')
    ap.add_argument('--sqlite-output-file', default='skeets.sqlite3')
    ap.add_argument('--if-exists', default='replace')
    args = ap.parse_args()

    export_to_sqlite(args.json_input_file, args.sqlite_output_file, if_exists=args.if_exists)