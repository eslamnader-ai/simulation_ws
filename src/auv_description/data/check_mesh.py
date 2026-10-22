import sys

def load(path):
    v, f = [], []
    for line in open(path):
        if line.startswith('v '):
            v.append(tuple(float(t) for t in line.split()[1:4]))
        elif line.startswith('f '):
            idx = [int(t.split('/')[0]) for t in line.split()[1:]]
            idx = [i - 1 if i > 0 else len(v) + i for i in idx]
            for k in range(1, len(idx) - 1):
                f.append((idx[0], idx[k], idx[k + 1]))
    return v, f

SCALE = 0.58  # the scale used in the scenario
for path in sys.argv[1:]:
    v, f = load(path)
    xs, ys, zs = zip(*v)
    vol = 0.0
    for a, b, c in f:
        p, q, r = v[a], v[b], v[c]
        vol += (p[0]*(q[1]*r[2]-q[2]*r[1]) - p[1]*(q[0]*r[2]-q[2]*r[0]) + p[2]*(q[0]*r[1]-q[1]*r[0])) / 6.0
    print(path)
    print("  faces:", len(f))
    print("  min xyz (file units):", [round(min(a), 4) for a in (xs, ys, zs)])
    print("  max xyz (file units):", [round(max(a), 4) for a in (xs, ys, zs)])
    print("  min xyz x scale:", [round(min(a) * SCALE, 4) for a in (xs, ys, zs)])
    print("  max xyz x scale:", [round(max(a) * SCALE, 4) for a in (xs, ys, zs)])
    print("  volume x scale^3 (m^3):", round(abs(vol) * SCALE ** 3, 5))
