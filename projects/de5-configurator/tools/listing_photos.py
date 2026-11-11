"""Upload the new DE5 GT Wing photos to the GT Wing listing (staged uploads -> productCreateMedia), detach the old 50/50 hero (file stays in Files),
and put the new media first. Uses the store app credentials from the environment (SHOPIFY_CLIENT_ID / SHOPIFY_CLIENT_SECRET). usage: listing_photos.py [--dry]"""
import os, sys, json, time, requests
SHOP = 'bmspec.myshopify.com'; API = f'https://{SHOP}/admin/api/2025-10/graphql.json'; D = '/home/user/media/de5-configurator/listing'
PID = 'gid://shopify/Product/8593416028204'; OLD_HERO = 'gid://shopify/MediaImage/39093126103084'
FILES = [
 ('acura-integra-de5-gt-wing-kit-overview.jpg', "Epsilon+ GT wing for the Acura Integra Type S (DE5): a white Integra Type S with the swan-neck kit, above the kit's wing, endplates and Integra Type S swan uprights"),
 ('acura-integra-de5-gt-wing-rear-quarter-parking-deck.jpg', 'Epsilon+ GT wing installed on a white Acura Integra Type S (DE5), rear three-quarter view on a parking deck showing the swan-neck uprights and full wingspan'),
 ('acura-integra-de5-gt-wing-swan-neck-closeup.jpg', 'Close-up of the Epsilon+ GT wing on a white Acura Integra Type S (DE5): wing element, endplates and swan-neck uprights above the hatch'),
 ('acura-integra-de5-gt-wing-rear-quarter-sunlight.jpg', 'White Acura Integra Type S (DE5) with the Epsilon+ GT wing in low sunlight, rear three-quarter view from the passenger side'),
 ('acura-integra-de5-gt-wing-rear-high-angle.jpg', 'High-angle rear view of a white Acura Integra Type S (DE5) showing the span of the Epsilon+ GT wing over the hatch'),
 ('acura-integra-de5-gt-wing-rear-quarter-dusk.jpg', 'White Acura Integra Type S (DE5) with the Epsilon+ GT wing at dusk, rear three-quarter view from the passenger side'),
]
tok = requests.post(f'https://{SHOP}/admin/oauth/access_token', data={'grant_type': 'client_credentials', 'client_id': os.environ['SHOPIFY_CLIENT_ID'], 'client_secret': os.environ['SHOPIFY_CLIENT_SECRET']}, timeout=30).json()['access_token']
def gql(q, v=None):
    r = requests.post(API, headers={'X-Shopify-Access-Token': tok}, json={'query': q, 'variables': v or {}}, timeout=60).json()
    if r.get('errors'): raise SystemExit(json.dumps(r['errors'])[:800])
    return r['data']
MEDIA = 'media(first: 40) { nodes { id alt status ... on MediaImage { image { url } } } }'
before = gql('query($id: ID!) { product(id: $id) { title ' + MEDIA + ' } }', {'id': PID})['product']
print(before['title'], len(before['media']['nodes']), 'media before'); assert before['media']['nodes'][0]['id'] == OLD_HERO
if '--dry' in sys.argv: sys.exit()
st = gql('mutation($i: [StagedUploadInput!]!) { stagedUploadsCreate(input: $i) { stagedTargets { url resourceUrl parameters { name value } } userErrors { message } } }',
         {'i': [{'filename': f, 'mimeType': 'image/jpeg', 'resource': 'IMAGE', 'httpMethod': 'POST', 'fileSize': str(os.path.getsize(f'{D}/{f}'))} for f, _ in FILES]})['stagedUploadsCreate']
assert not st['userErrors'], st['userErrors']
for (f, _), t in zip(FILES, st['stagedTargets']):
    r = requests.post(t['url'], data={p['name']: p['value'] for p in t['parameters']}, files={'file': (f, open(f'{D}/{f}', 'rb'), 'image/jpeg')}, timeout=300); print(f, r.status_code); assert r.status_code in (200, 201, 204), r.text[:300]
cm = gql('mutation($id: ID!, $m: [CreateMediaInput!]!) { productCreateMedia(productId: $id, media: $m) { media { id status } mediaUserErrors { message } } }',
         {'id': PID, 'm': [{'originalSource': t['resourceUrl'], 'alt': a, 'mediaContentType': 'IMAGE'} for (_, a), t in zip(FILES, st['stagedTargets'])]})['productCreateMedia']
assert not cm['mediaUserErrors'], cm['mediaUserErrors']; new = [m['id'] for m in cm['media']]; print('created', new)
for _ in range(30):
    time.sleep(3); s = [m['status'] for m in gql('query($ids: [ID!]!) { nodes(ids: $ids) { ... on MediaImage { status } } }', {'ids': new})['nodes']]
    if all(x == 'READY' for x in s): break
print('status', s)
fu = gql('mutation($f: [FileUpdateInput!]!) { fileUpdate(files: $f) { files { id } userErrors { message } } }', {'f': [{'id': OLD_HERO, 'referencesToRemove': [PID]}]})['fileUpdate']; print('detach old hero', fu)
ro = gql('mutation($id: ID!, $m: [MoveInput!]!) { productReorderMedia(id: $id, moves: $m) { job { id } mediaUserErrors { message } } }', {'id': PID, 'm': [{'id': i, 'newPosition': str(k)} for k, i in enumerate(new)]})['productReorderMedia']; print('reorder', ro)
time.sleep(6)
after = gql('query($id: ID!) { product(id: $id) { ' + MEDIA + ' } }', {'id': PID})['product']['media']['nodes']
json.dump({'before': before['media']['nodes'], 'after': after}, open('/home/user/media/work/de5/listing_media.json', 'w'), indent=1)
for m in after: print(m['status'], (m.get('image') or {}).get('url', '')[-70:])
