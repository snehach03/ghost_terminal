import math, os, random, struct, wave

def write_wav(fn, samples, rate=22050):
    os.makedirs(os.path.dirname(os.path.abspath(fn)), exist_ok=True)
    with wave.open(fn, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        pk = max((abs(s) for s in samples), default=1.0)
        gn = 0.9 / pk if pk > 0.9 else 1.0
        b = bytearray()
        for s in samples:
            val = int(max(-32767, min(32767, s * gn * 32767)))
            b.extend(struct.pack("<h", val))
        w.writeframes(b)

def gen_all(d):
    os.makedirs(d, exist_ok=True)
    r = 22050
    # 1. door creak
    s = [math.sin(2*math.pi*(110-30*(i/26460)+math.sin(28*math.pi*i/r)*15)*(i/r))*math.sin(math.pi*i/26460)**0.8*0.7 for i in range(26460)]
    write_wav(os.path.join(d, "door_creak.wav"), s, r)
    # 2. chains
    s = [0.0]*28665; rng = random.Random(42)
    for st in [0.05, 0.22, 0.45, 0.70, 0.95]:
        si = int(st*r); rf = rng.choice([880, 1174, 1480, 1760])
        for j in range(int(0.28*r)):
            if si+j < len(s):
                t = j/r
                s[si+j] += ((rng.random()*2-1)*0.4 + math.sin(2*math.pi*rf*t)*0.6)*math.exp(-14*t)*0.6
    write_wav(os.path.join(d, "chains.wav"), s, r)
    # 3. wail
    s = [math.sin(2*math.pi*(380+180*math.sin(math.pi*i/35280)+math.sin(11*math.pi*i/r)*18)*(i/r))*math.sin(math.pi*i/35280)*0.7 for i in range(35280)]
    write_wav(os.path.join(d, "wail.wav"), s, r)
    # 4. footsteps
    s = [0.0]*30870
    for st in [0.08, 0.70]:
        si = int(st*r)
        for j in range(int(0.55*r)):
            if si+j < len(s):
                t = j/r
                s[si+j] += (math.sin(150*math.pi*t)*math.exp(-18*t) + math.sin(240*math.pi*t)*math.exp(-6*t)*0.4)*0.8
    write_wav(os.path.join(d, "footsteps.wav"), s, r)
    # 5. bell
    s = [(math.sin(180*math.pi*i/r)*math.exp(-1.8*i/r) + 0.6*math.sin(2*math.pi*248*i/r)*math.exp(-2.5*i/r))*0.75 for i in range(39690)]
    write_wav(os.path.join(d, "bell.wav"), s, r)
    # 6. chime
    s = [sum(math.sin(2*math.pi*n*i/r)*math.exp(-3.2*i/r) for n in [659.25, 830.61, 987.77])*0.3 for i in range(26460)]
    write_wav(os.path.join(d, "chime.wav"), s, r)
    # 7. moan
    s = [math.sin(2*math.pi*(130+35*math.sin(3*math.pi*i/r))*(i/r))*(math.sin(math.pi*i/33075)**1.5)*0.7 for i in range(33075)]
    write_wav(os.path.join(d, "moan.wav"), s, r)

if __name__ == "__main__":
    gen_all(os.path.dirname(os.path.abspath(__file__)))
    print("Sounds created.")
