"""Add the brightened side profile (Drive P1036200, wing separated from the wall) to the GT Wing listing in place of the driveway side profile
(detached, file kept in Files); new image goes third, after the hero and the rear three-quarter."""
import os, json, time, requests
SHOP = 'bmspec.myshopify.com'; API = f'https://{SHOP}/admin/api/2025-10/graphql.json'
PID = 'gid://shopify/Product/8593416028204'; OLD = 'gid://shopify/MediaImage/39092229734444'
F = '/home/user/media/de5-configurator/listing/acura-integra-de5-gt-wing-side-profile-parking-garage.jpg'
ALT = 'Side profile of a white Acura Integra Type S (DE5) fitted with the Epsilon+ GT wing in a parking garage, showing wing height, swan-neck uprights and stance'
tok = requests.post(f'https://{SHOP}/admin/oauth/access_token', data={'grant_type': 'client_credentials', 'client_id': os.environ['SHOPIFY_CLIENT_ID'], 'client_secret': os.environ['SHOPIFY_CLIENT_SECRET']}, timeout=30).json()['access_token']
def gql(q, v=None):
    r = requests.post(API, headers={'X-Shopify-Access-Token': tok}, json={'query': q, 'variables': v or {}}, timeout=60).json()
    if r.get('errors'): raise SystemExit(json.dumps(r['errors'])[:800])
    return r['data']
Q = 'query($id: ID!) { product(id: $id) { media(first: 40) { nodes { id status ... on MediaImage { image { url } } } } } }'
ids = [m['id'] for m in gql(Q, {'id': PID})['product']['media']['nodes']]; assert OLD in ids, 'driveway side profile not on the product'
t = gql('mutation($i: [StagedUploadInput!]!) { stagedUploadsCreate(input: $i) { stagedTargets { url resourceUrl parameters { name value } } userErrors { message } } }',
        {'i': [{'filename': os.path.basename(F), 'mimeType': 'image/jpeg', 'resource': 'IMAGE', 'httpMethod': 'POST', 'fileSize': str(os.path.getsize(F))}]})['stagedUploadsCreate']['stagedTargets'][0]
r = requests.post(t['url'], data={p['name']: p['value'] for p in t['parameters']}, files={'file': (os.path.basename(F), open(F, 'rb'), 'image/jpeg')}, timeout=300); assert r.status_code == 201, r.text[:300]
cm = gql('mutation($id: ID!, $m: [CreateMediaInput!]!) { productCreateMedia(productId: $id, media: $m) { media { id } mediaUserErrors { message } } }', {'id': PID, 'm': [{'originalSource': t['resourceUrl'], 'alt': ALT, 'mediaContentType': 'IMAGE'}]})['productCreateMedia']
assert not cm['mediaUserErrors'], cm; new = cm['media'][0]['id']
for _ in range(30):
    time.sleep(3)
    if gql('query($id: ID!) { node(id: $id) { ... on MediaImage { status } } }', {'id': new})['node']['status'] == 'READY': break
print('detach', gql('mutation($f: [FileUpdateInput!]!) { fileUpdate(files: $f) { userErrors { message } } }', {'f': [{'id': OLD, 'referencesToRemove': [PID]}]}))
print('reorder', gql('mutation($id: ID!, $m: [MoveInput!]!) { productReorderMedia(id: $id, moves: $m) { mediaUserErrors { message } } }', {'id': PID, 'm': [{'id': new, 'newPosition': '2'}]}))
time.sleep(6)
for m in gql(Q, {'id': PID})['product']['media']['nodes']: print(m['status'], (m.get('image') or {}).get('url', '').split('/files/')[-1].split('?')[0])
