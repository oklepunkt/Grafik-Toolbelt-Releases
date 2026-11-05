#!/usr/bin/env python3
"""Publish one reviewed AE Tools ZIP using the public repository's scoped Actions token."""
import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import zipfile

PUBLIC = 'oklepunkt/Grafik-Toolbelt-Releases'
VERSION = re.compile(r'^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?(?:\+[0-9A-Za-z.-]+)?$')

def validate_request(request):
    m = request['manifest']
    if not (request.get('schema') == 1 and m.get('schema') == 1
            and re.fullmatch(r'grafik\.[a-z][a-z0-9-]{0,47}', m.get('id', ''))
            and re.fullmatch(r'[A-Za-z][A-Za-z0-9 -]{0,63}', m.get('name', ''))
            and VERSION.fullmatch(m.get('version', '')) and m.get('host') == 'aftereffects'
            and m.get('format') == 'scriptui-jsx' and type(m.get('apiVersion')) is int and m['apiVersion'] > 0
            and re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,63}\.jsx', m.get('entry', ''))
            and m['entry'].lower() == m['id'][7:] + '.jsx'
            and re.fullmatch(r'[a-f0-9]{64}', m.get('sha256', ''))
            and type(m.get('bytes')) is int and 0 < m['bytes'] <= 16 * 1024 * 1024
            and re.fullmatch(r'[a-f0-9]{40}', request.get('sourceCommit', ''))
            and re.fullmatch(r'[a-f0-9]{40}', request.get('payloadBlob', ''))
            and re.fullmatch(r'[a-f0-9]{64}', request.get('assetSHA256', ''))
            and type(request.get('assetBytes')) is int and 0 < request['assetBytes'] <= 32 * 1024 * 1024):
        raise ValueError('Invalid publication request')
    tag = m['id'][7:] + '-v' + m['version']
    name = m['entry'][:-4] + '-' + m['version'] + '.zip'
    notes = '.github/ae-tools/releases/' + tag + '.md'
    if request.get('assetName') != name or request.get('notes') != notes:
        raise ValueError('Unexpected asset or release notes path')
    return tag, name

def validate_package(data, request):
    validate_request(request)
    if len(data) != request['assetBytes'] or hashlib.sha256(data).hexdigest() != request['assetSHA256']:
        raise ValueError('ZIP differs from the reviewed artifact')
    m = request['manifest']; prefix = m['entry'][:-4] + '/'
    required = {prefix+'manifest.json', prefix+m['entry'], prefix+'INSTALLATION.md'}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        items = archive.infolist()
        if len(items) != 3 or {item.filename for item in items} != required:
            raise ValueError('ZIP contains missing, duplicate or unexpected files')
        for item in items:
            mode = (item.external_attr >> 16) & 0o170000
            limit = 16 * 1024 * 1024 if item.filename == prefix+m['entry'] else 131072
            if mode not in (0, 0o100000) or item.flag_bits & 1 or item.compress_type not in (0, 8) or item.file_size > limit:
                raise ValueError('Unsafe or oversized ZIP member')
        if archive.testzip() is not None: raise ValueError('ZIP CRC mismatch')
        if json.loads(archive.read(prefix+'manifest.json')) != m: raise ValueError('Manifest differs from release metadata')
        jsx = archive.read(prefix+m['entry'])
        if len(jsx) != m['bytes'] or hashlib.sha256(jsx).hexdigest() != m['sha256'] or not jsx.startswith(b'#target aftereffects'):
            raise ValueError('JSX integrity mismatch')

def gh(*arguments):
    return subprocess.check_output(['gh', *map(str, arguments)])

def api(path):
    return json.loads(gh('api', 'repos/'+PUBLIC+'/'+path))

def find_release(tag):
    matches = []
    for page in range(1, 11):
        batch = api('releases?per_page=100&page='+str(page))
        matches.extend(r for r in batch if r['tag_name'] == tag)
        if len(batch) < 100: break
    else: raise RuntimeError('Release list exceeds the supported limit')
    if len(matches) > 1: raise RuntimeError('Ambiguous release tag')
    return matches[0] if matches else None

def publish(request_file):
    if os.environ.get('GITHUB_REPOSITORY') != PUBLIC or not re.fullmatch(r'[a-f0-9]{40}', os.environ.get('GITHUB_SHA', '')):
        raise RuntimeError('Run this publisher in the reviewed public repository workflow')
    request = json.loads(Path(request_file).read_text())
    tag, name = validate_request(request)
    blob = api('git/blobs/'+request['payloadBlob'])
    data = base64.b64decode(blob['content'].replace('\n', ''), validate=True)
    validate_package(data, request)
    notes_path = Path(request['notes'])
    if notes_path.is_symlink() or notes_path.stat().st_size > 32768: raise ValueError('Invalid notes file')
    notes = notes_path.read_text().strip()
    if '<!-- toolbelt-ae-tool ' in notes or '<!-- ae-tool-source ' in notes:
        raise ValueError('Publisher owns the hidden metadata markers')
    notes += '\n\n<!-- toolbelt-ae-tool '+json.dumps(request['manifest'],separators=(',', ':'))+' -->\n'
    notes += '<!-- ae-tool-source revision='+request['sourceCommit']+' -->\n'
    latest = api('releases/latest')['tag_name']
    prerelease = '-' in request['manifest']['version'].split('+', 1)[0]
    with tempfile.TemporaryDirectory(prefix='ae-tools-publication-') as temp:
        asset = Path(temp)/name; asset.write_bytes(data)
        body = Path(temp)/'notes.md'; body.write_text(notes)
        release = find_release(tag)
        if release is None:
            command = ['release','create',tag,'--repo',PUBLIC,'--target',os.environ['GITHUB_SHA'],'--draft','--latest=false',
                       '--title',request['manifest']['name']+' '+request['manifest']['version'],'--notes-file',str(body),str(asset)]
            if prerelease: command.append('--prerelease')
            gh(*command)
        for attempt in range(6):
            release = find_release(tag)
            if release is not None: break
            time.sleep(2)
        if release is None: raise RuntimeError('The new draft is not visible yet; retry the same request')
        release = api('releases/'+str(release['id']))
        assets = release['assets']
        if ((release.get('body') or '').strip() != notes.strip() or release['prerelease'] != prerelease
                or len(assets) != 1 or assets[0]['name'] != name or assets[0]['size'] != len(data)
                or assets[0].get('digest') != 'sha256:'+request['assetSHA256']):
            raise RuntimeError('Existing release differs; no assets or published bytes were replaced')
        downloaded = gh('api','repos/'+PUBLIC+'/releases/assets/'+str(assets[0]['id']),'-H','Accept: application/octet-stream')
        validate_package(downloaded, request)
        if release['draft']:
            gh('api','--method','PATCH','repos/'+PUBLIC+'/releases/'+str(release['id']),'-F','draft=false','-f','make_latest=false')
        published = api('releases/tags/'+tag)
        if published['draft'] or published['prerelease'] != prerelease or published['tag_name'] != tag:
            raise RuntimeError('Unexpected final release state')
        if api('releases/latest')['tag_name'] != latest: raise RuntimeError('Latest Toolbelt app changed; inspect without replacing releases')
        print(json.dumps({'url':published['html_url'],'release':published['id'],'asset':assets[0]['id'],'sha256':request['assetSHA256']}))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--request',required=True)
    publish(parser.parse_args().request)
