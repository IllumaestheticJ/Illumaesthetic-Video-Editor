"""Detach images from the GT Wing listing by file name (files stay in Shopify Files, so this is reversible). usage: listing_remove.py name1 name2 ... [--dry]"""
import os, sys, json, time, requests
SHOP = 'bmspec.myshopify.com'; API = f'https://{SHOP}/admin/api/2025-10/graphql.json'; PID = 'gid://shopify/Product/8593416028204'
names = [a for a in sys.argv[1:] if not a.startswith('--')]
tok = requests.post(f'https://{SHOP}/admin/oauth/access_token', data={'grant_type': 'client_credentials', 'client_id': os.environ['SHOPIFY_CLIENT_ID'], 'client_secret': os.environ['SHOPIFY_CLIENT_SECRET']}, timeout=30).json()['access_token']
def gql(q, v=None):
    r = requests.post(API, headers={'X-Shopify-Access-Token': tok}, json={'query': q, 'variables': v or {}}, timeout=60).json()
    if r.get('errors'): raise SystemExit(json.dumps(r['errors'])[:800])
    return r['data']
Q = 'query($id: ID!) { product(id: $id) { title media(first: 40) { nodes { id ... on MediaImage { image { url } } } } } }'
fn = lambda m: (m.get('image') or {}).get('url', '').split('/files/')[-1].split('?')[0]
nodes = gql(Q, {'id': PID})['product']['media']['nodes']; by = {fn(m): m['id'] for m in nodes}
missing = [n for n in names if n not in by]; assert not missing, f'not on the listing: {missing}'
print('before:', len(nodes)); [print('  remove' if fn(m) in names else '  keep  ', fn(m)) for m in nodes]
if '--dry' in sys.argv: sys.exit()
r = gql('mutation($f: [FileUpdateInput!]!) { fileUpdate(files: $f) { files { id } userErrors { message } } }', {'f': [{'id': by[n], 'referencesToRemove': [PID]} for n in names]})['fileUpdate']
assert not r['userErrors'], r['userErrors']; time.sleep(5)
after = gql(Q, {'id': PID})['product']['media']['nodes']; print('after:', len(after)); [print('  ', fn(m)) for m in after]
