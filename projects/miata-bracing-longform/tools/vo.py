"""Narration lines as TTS text (numbers spelled the way they are read), from build.py NAR.  usage: vo.py  -> prints JSON list"""
import sys, re, json, importlib.util, os
sys.argv = [sys.argv[0], '/home/user/media/miata-bracing', '--script-only']
sp = importlib.util.spec_from_file_location('b', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build.py')); b = importlib.util.module_from_spec(sp); sp.loader.exec_module(b)
D = 'zero one two three four five six seven eight nine'.split()
SAY = {'960': 'nine sixty', '961': 'nine sixty-one', '962': 'nine sixty-two', '1': 'one', '0': 'zero'}
def num(m): a, c = m.group(1), m.group(2); return f"{SAY[a]} point {' '.join(D[int(x)] for x in c)}"
def tts(s):
    s = re.sub(r'\b(\d+)\.(\d+)\b', num, s)
    for a, c in (('86 percent', 'eighty-six percent'), ('57 percent', 'fifty-seven percent'), ('74 percent', 'seventy-four percent'), ('stock NB', 'stock N B')): s = s.replace(a, c)
    return s
L = [tts(n) for n in b.NAR]
if __name__ == '__main__': print(json.dumps(L, indent=0))
