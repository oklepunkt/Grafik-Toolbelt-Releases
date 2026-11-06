"""Reversibly withdraw an exact reviewed set of pre-password releases.

No assets, tags or commits are deleted. This cannot revoke downloaded copies or
remove historical public Git blobs. AE Tools are never eligible.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote

REPOSITORY = 'oklepunkt/Grafik-Toolbelt-Releases'


def predates_password(tag):
    plugin = re.fullmatch(r'keytween-v0\.1\.0-dev\.(\d+)', tag)
    if plugin:
        return int(plugin[1]) < 41
    app = re.fullmatch(r'toolbelt-v(\d+)\.(\d+)(?:\.(\d+))?', tag)
    return bool(app and tuple(int(n or 0) for n in app.groups()) < (0, 6, 7))


def validate_plan(plan):
    if plan.get('schema') != 1 or plan.get('repository') != REPOSITORY or not plan.get('releases'):
        raise ValueError('Invalid withdrawal plan')
    if predates_password(plan['expected_latest']) or not plan['expected_latest'].startswith('toolbelt-v'):
        raise ValueError('Latest must remain a protected Toolbelt release')
    ids, tags = set(), set()
    for row in plan['releases']:
        if not predates_password(row['tag']) or row['id'] in ids or row['tag'] in tags or not row['assets']:
            raise ValueError('Unsafe or duplicate withdrawal target')
        ids.add(row['id']); tags.add(row['tag'])
        expected = '.github/workflows/publish-' + row['tag'].replace('keytween-v0.1.0-dev.', 'keytween-dev') + '.yml'
        if row.get('publisher') not in (None, expected):
            raise ValueError('Publisher does not belong to the withdrawn release')


def asset_snapshot(release):
    return sorted([{key: a[key] for key in ['id', 'name', 'size', 'digest']} for a in release['assets']], key=lambda a: a['id'])


def apply_plan(plan, api, apply=False):
    validate_plan(plan)
    if api('GET', 'releases/latest')['tag_name'] != plan['expected_latest']:
        raise ValueError('Latest changed; review the plan again')
    # Finish all read-only checks before the first mutation.
    for row in plan['releases']:
        current = api('GET', 'releases/' + str(row['id']))
        if current['tag_name'] != row['tag'] or asset_snapshot(current) != sorted(row['assets'], key=lambda a: a['id']):
            raise ValueError('Release or asset changed: ' + row['tag'])
    if not apply:
        return {'verified': len(plan['releases']), 'changed': 0}
    for row in plan['releases']:
        if row.get('publisher'):
            api('PUT', 'actions/workflows/' + quote(row['publisher'].split('/')[-1], safe='') + '/disable')
    for row in plan['releases']:
        current = api('GET', 'releases/' + str(row['id']))
        if current['tag_name'] != row['tag'] or asset_snapshot(current) != sorted(row['assets'], key=lambda a: a['id']):
            raise ValueError('Release changed during withdrawal: ' + row['tag'])
        if not current['draft']:
            api('PATCH', 'releases/' + str(row['id']), {'draft': True, 'make_latest': 'false'})
        verified = api('GET', 'releases/' + str(row['id']))
        if not verified['draft'] or verified['tag_name'] != row['tag'] or asset_snapshot(verified) != asset_snapshot(current):
            raise ValueError('Withdrawal verification failed: ' + row['tag'])
        print('Withdrawn to draft: ' + row['tag'])
    if api('GET', 'releases/latest')['tag_name'] != plan['expected_latest']:
        raise ValueError('Latest changed during withdrawal')
    return {'verified': len(plan['releases']), 'changed': len(plan['releases'])}


def github(method, path, body=None):
    command = ['gh', 'api', '--method', method, 'repos/' + REPOSITORY + '/' + path]
    if body is not None:
        command += ['--input', '-']
    result = subprocess.run(command, input=json.dumps(body) if body is not None else None,
                            text=True, capture_output=True, check=True, timeout=60)
    return json.loads(result.stdout) if result.stdout.strip() else None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    print(json.dumps(apply_plan(json.loads(args.plan.read_text()), github, args.apply)))
