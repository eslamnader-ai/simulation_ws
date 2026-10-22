"""
Find the rotation axis of a thruster rotor (3+ blades) and re-centre it.

usage: python3 fix_thruster_axis.py thruster_rotor.obj thruster_housing.obj [more.obj ...]

The FIRST file must be the rotor. Its axis (the symmetry axis of the blades) is found,
then the same rigid transform is applied to every file given:
  1. translate sideways so the axis passes through the origin (axial position is kept),
  2. rotate so the axis points along +X.
Outputs are written as <name>_fixed.obj. Vertex normals are rotated too.
"""
import sys
import numpy as np

def read_obj(path):
    lines = open(path).read().split("\n")
    v = [[float(t) for t in l.split()[1:4]] for l in lines if l.startswith("v ")]
    return lines, np.array(v)

def rotation_to_x(a):
    a = a / np.linalg.norm(a)
    x = np.array([1.0, 0.0, 0.0])
    v = np.cross(a, x); s = np.linalg.norm(v); c = float(np.dot(a, x))
    if s < 1e-12:
        return np.eye(3) if c > 0 else np.diag([-1.0, -1.0, 1.0])
    k = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + k + k @ k * ((1 - c) / (s * s))

def main(files):
    _, rv = read_obj(files[0])
    c = rv.mean(axis=0)
    w, vec = np.linalg.eigh(np.cov((rv - c).T))
    # the symmetry axis is the eigenvector whose eigenvalue differs from the other two,
    # which are nearly equal for a 3-blade propeller
    gaps = [abs(w[(i + 1) % 3] - w[(i + 2) % 3]) for i in range(3)]
    i = int(np.argmin(gaps))
    axis = vec[:, i]
    if axis[np.argmax(np.abs(axis))] < 0:
        axis = -axis
    pair = sorted(w[[(i + 1) % 3, (i + 2) % 3]])
    print("rotor eigenvalues:", [float(f"{x:.3e}") for x in w])
    print("axis direction (before):", np.round(axis, 4))
    if abs(pair[0] - pair[1]) > 0.15 * max(pair):
        print("WARNING: the two 'equal' eigenvalues differ by more than 15%; the axis may be wrong.")
    t = c - np.dot(c, axis) * axis          # sideways offset of the axis from the origin
    print("sideways offset of rotor axis from origin (file units):", np.round(t, 5), "|t| =", round(float(np.linalg.norm(t)), 5))
    R = rotation_to_x(axis)
    for path in files:
        lines, _ = read_obj(path)
        out = []
        for l in lines:
            p = l.split()
            if l.startswith("v ") and len(p) >= 4:
                q = R @ (np.array([float(p[1]), float(p[2]), float(p[3])]) - t)
                out.append("v %.6f %.6f %.6f" % tuple(q) + ((" " + " ".join(p[4:])) if len(p) > 4 else ""))
            elif l.startswith("vn ") and len(p) >= 4:
                q = R @ np.array([float(p[1]), float(p[2]), float(p[3])])
                out.append("vn %.6f %.6f %.6f" % tuple(q))
            else:
                out.append(l)
        new = path[:-4] + "_fixed.obj"
        open(new, "w").write("\n".join(out))
        _, nv = read_obj(new)
        print(f"{new}: min {np.round(nv.min(0), 4)}  max {np.round(nv.max(0), 4)}")

main(sys.argv[1:])
