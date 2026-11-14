#!/usr/bin/env python3
# Dr. Denys Dutykh (Mathematics Department, Khalifa University of Science and Technology, Abu Dhabi, UAE)
"""Figure of the README: a sine-Gordon kink crossing the Y junction, computed by sG_solver.edp.

Run the FreeFem++ script first, from this folder (it writes its results in the current folder),
    FreeFem++ -nw ../../script/sG_solver.edp
then
    python3 plot_readme_figure.py [FOLDER]
which reads Junction.msh, Solution*.bb and EnergyCons.txt from FOLDER (by default this folder) and
writes sg-y-junction.png beside this script. The style is the stamped copy manuscript_style.py.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import manuscript_style as hs  # noqa: E402

RUN = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE
TF, M = 18.0, 3500                    # final time and number of steps of sG_solver.edp
STEPS = (0, 700, 1050, 1400, 2100, 3500)   # stored steps shown: t = 0, 3.6, 5.4, 7.2, 10.8, 18


def read_mesh(path):
    """Vertices, triangles (from 0) and boundary edges of a FreeFem++ .msh file."""
    lines = path.read_text().split("\n")
    nv, nt, nbe = (int(k) for k in lines[0].split())
    xy = np.array([[float(v) for v in lines[1 + i].split()[:2]] for i in range(nv)])
    tri = np.array([[int(v) - 1 for v in lines[1 + nv + i].split()[:3]] for i in range(nt)])
    edges = np.array([[int(v) - 1 for v in lines[1 + nv + nt + i].split()[:2]]
                      for i in range(nbe)])
    return xy, tri, edges


def read_solution(path, n):
    """Nodal values of a P1 field written by sG_solver.edp (medit .bb format)."""
    values = np.loadtxt(path, skiprows=1)
    if values.size != n:
        raise ValueError(f"{path.name}: {values.size} values for {n} vertices")
    return values


xy, tri, edges = read_mesh(RUN / "Junction.msh")
triangulation = mtri.Triangulation(xy[:, 0], xy[:, 1], tri)
energy = np.loadtxt(RUN / "EnergyCons.txt")

hs.configure(family="libertine")
plt.rcParams["savefig.dpi"] = 265
plt.rcParams["figure.facecolor"] = hs.PAPER
plt.rcParams["savefig.facecolor"] = hs.PAPER

norm = Normalize(0.0, 2.0 * np.pi)
fig, axes = plt.subplots(2, 3, figsize=(hs.WIDTH, 4.6))
fig.get_layout_engine().set(wspace=0.03, hspace=0.05)
outline = np.stack([xy[edges[:, 0]], xy[edges[:, 1]]], axis=1)
for n, (axis, step) in enumerate(zip(axes.flat, STEPS)):
    u = read_solution(RUN / f"Solution{step}.bb", len(xy))
    image = axis.tripcolor(triangulation, u, shading="gouraud", cmap=hs.DENSITY_COLORMAP,
                           norm=norm, rasterized=True)
    axis.add_collection(LineCollection(outline, colors=hs.INK, linewidths=0.5, capstyle="round"))
    axis.set_xlim(-8.6, 8.6)
    axis.set_ylim(-10.6, 9.0)
    axis.set_aspect("equal")
    axis.set_xticks([])
    axis.set_yticks([])
    axis.axis("off")
    hs.panel(axis, rf"({'abcdef'[n]}) $t = {step * TF / M:.1f}$")

bar = hs.colorbar(fig, image, list(axes.flat), r"solution $u$", shrink=0.6)
bar.set_ticks([0.0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi],
              labels=[r"$0$", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
out = HERE / "sg-y-junction.png"
hs.save(fig, out)
# The background is opaque: without its alpha channel, and compressed a second time without
# loss, the file is smaller.
Image.open(out).convert("RGB").save(out, optimize=True)

gamma = 1.0 / np.sqrt(1.0 - 0.96 ** 2)
total = energy[:, 1]
print("written", out)
print(f"energy 8 w0 gamma = {8 * gamma:.6f}; computed: first {total[0]:.6f} (t = {energy[0, 0]:.4f}), "
      f"last {total[-1]:.6f} (t = {energy[-1, 0]:.4f}), min {total.min():.6f}, max {total.max():.6f}")
for k in (0, len(energy) // 4, len(energy) // 2, len(energy) - 1):
    print(f"t = {energy[k, 0]:.3f}: bottom {energy[k, 2]:.4f}, left {energy[k, 3]:.4f}, right {energy[k, 4]:.4f}")
