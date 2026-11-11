"""prep_photos.py CAR : download the 3 finished photos (full res) + rembg car masks."""
import sys, json, os, subprocess
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
car = sys.argv[1]; c = json.load(open(os.path.join(os.path.dirname(__file__), 'cars.json')))[car]
D = f'/home/user/media/cars/{car}/match'; os.makedirs(D, exist_ok=True)
from rembg import remove, new_session
sess = new_session('isnet-general-use')
for a, url in c['photos'].items():
    p = f'{D}/{a}.jpg'
    if not os.path.exists(p): subprocess.run(['curl', '-sS', '-m', '120', '-A', 'Mozilla/5.0', '-o', p, url], check=True)
    im = Image.open(p).convert('RGB')
    from PIL import ImageOps; im = ImageOps.exif_transpose(im); im.save(p, quality=95)
    w = 1400; sm = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    m = remove(sm, session=sess, only_mask=True); m.save(f'{D}/{a}_mask.png')
    print(car, a, im.size)
