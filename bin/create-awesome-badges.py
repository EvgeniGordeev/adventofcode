#!/usr/bin/env python3
import argparse
import datetime
import json
import os
import re
import sys

import requests


def update_gist(gist_files: dict, secret, gist_id):
    """
    Courtesy of:
        * https://github.com/Schneegans/dynamic-badges-action
        * https://github.com/Schneegans/dynamic-badges-action/blob/master/index.js
    """
    headers = {"Authorization": f"Bearer {secret}"}
    url = f"https://api.github.com/gists/{gist_id}"

    gist = requests.get(url, headers=headers)
    if gist.status_code != 200:
        sys.exit(f"Gist not found {gist.text}")

    data = {"files": {path: {"content": json.dumps(content, ensure_ascii=False)}
                      for path, content in gist_files.items()}}
    patched_gist = requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data)
    if patched_gist.status_code != 200:
        sys.exit(f"Gist not updated {gist.text}")
    print(f"Uploaded {gist_files.keys()} to gist {gist_id}")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Parse benchmark results and upload them to a Github Gist')
    parser.add_argument('--gist', help='Github Gist id', default='13c6cac3c39702cdcb9cc169b66c3210')
    parser.add_argument('--secret', help='Github Secret with Gist permission or GIST_GITHUB_SECRET',
                        default=os.environ.get('GIST_GITHUB_SECRET'))
    parser.add_argument('--dir', default=f"../{datetime.date.today().year}", help='folder with py files to run')
    parser.add_argument('--dry-run', action='store_true', help='dry run')
    args = parser.parse_args()

    folder = os.path.join(os.getcwd(), args.dir)
    if not os.path.isdir(folder):
        sys.exit(f" --dir requires an existing folder. {folder} is not a directory. ")

    benchmark_results = sorted([f for f in os.listdir(folder) if re.match(r'.*benchmark\.txt$', f)])
    dir_name = folder.split('/')[-1]

    gist_files = dict()
    for benchmark in benchmark_results:
        with open(os.path.join(folder, benchmark), 'r', encoding='utf-8') as file_content:
            result = file_content.read()
            suffix = re.findall(r'(\d*).*', benchmark)[0]
            suffix = suffix if suffix else 'all'
            timing = re.findall(r'Time.*:\s*(.+ ±)', result)[0]
            badge = {"schemaVersion": 1, "label": "Runtime", "message": timing, "color": "blue"}
            gist_files[f"runtime-badge-{dir_name}-{suffix}.json"] = badge

    if gist_files:
        update_gist(gist_files, args.secret, args.gist)
