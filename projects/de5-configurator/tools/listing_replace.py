"""Replace listing images IN PLACE with brightened versions (same media id, position and alt text): staged upload -> fileUpdate(originalSource).
usage: listing_replace.py <media gid>=<local jpg> ..."""
import os, sys, json, time, requests
SHOP = 'bmspec.myshopify.com'; API = f'https://{SHOP}/admin/api/2025-10/graphql.json'
pairs = [a.split('=', 1) for a in sys.argv[1:]]
tok = requests.post(f'https://{SHOP}/admin/oauth/access_token', data={'grant_type': 'client_credentials', 'client_id': os.environ['SHOPIFY_CLIENT_ID'], 'client_secret': os.environ['SHOPIFY_CLIENT_SECRET']}, timeout=30).json()['access_token']
def gql(q, v=None):
    r = requests.post(API, headers={'X-Shopify-Access-Token': tok}, json={'query': q, 'variables': v or {}}, timeout=60).json()
    if r.get('errors'): raise SystemExit(json.dumps(r['errors'])[:800])
    return r['data']
st = gql('mutation($i: [StagedUploadInput!]!) { stagedUploadsCreate(input: $i) { stagedTargets { url resourceUrl parameters { name value } } userErrors { message } } }',
         {'i': [{'filename': os.path.basename(f), 'mimeType': 'image/jpeg', 'resource': 'IMAGE', 'httpMethod': 'POST', 'fileSize': str(os.path.getsize(f))} for _, f in pairs]})['stagedUploadsCreate']['stagedTargets']
for (_, f), t in zip(pairs, st):
    r = requests.post(t['url'], data={p['name']: p['value'] for p in t['parameters']}, files={'file': (os.path.basename(f), open(f, 'rb'), 'image/jpeg')}, timeout=300); assert r.status_code == 201, r.text[:300]
u = gql('mutation($f: [FileUpdateInput!]!) { fileUpdate(files: $f) { files { id fileStatus } userErrors { field message code } } }', {'f': [{'id': g, 'originalSource': t['resourceUrl']} for (g, _), t in zip(pairs, st)]})['fileUpdate']; print(u)
for _ in range(30):
    time.sleep(3); n = gql('query($ids: [ID!]!) { nodes(ids: $ids) { ... on MediaImage { id fileStatus image { url width height } } } }', {'ids': [g for g, _ in pairs]})['nodes']
    if all(x['fileStatus'] == 'READY' for x in n): break
for x in n: print(x['fileStatus'], x['image'])
