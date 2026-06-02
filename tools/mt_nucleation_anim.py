"""Microtubule nucleation animation, Bio-peak style:
black bg, horizontal MT, 3D-shaded staggered alpha/beta lattice, red gamma-TuRC at (-) end.
Usage: python nucleation_v2.py sample | full
"""
import sys, os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

OUT = os.path.join(os.environ["TEMP"], "nuc2_frames")
os.makedirs(OUT, exist_ok=True)

BG      = "#000000"
C_BETA  = "#1f7a3d"   # beta-tubulin (dark green)
C_ALPHA = "#b9c7b0"   # alpha-tubulin (pale grey-green)
C_GCP   = "#6f1420"   # GCP rods (dark red)
C_GTUB  = "#9e1b27"   # gamma-tubulin caps (red)
C_TXT   = "#f0f0f0"
HI      = "white"

ROWS = 7
RES_X0 = 1.7          # gamma-TuRC rod left
CAP_X  = 3.45         # gamma-tubulin cap x
GREEN0 = 4.05         # first green column x
DX     = 0.60         # column spacing
RY     = 0.70         # row spacing
RAD    = 0.34
CMAX   = 14

def ease(u):
    u = max(0.0, min(1.0, u)); return u*u*(3-2*u)

_z = [10]
def sphere(ax, x, y, r, color, z):
    ax.add_patch(Circle((x, y), r, fc=color, ec="#00000066", lw=0.5, zorder=z))
    ax.add_patch(Circle((x-0.34*r, y+0.34*r), r*0.42, fc=HI, ec="none", alpha=0.30, zorder=z+0.1))

def row_y(r):  return 6.3 - r*RY
def row_sx(r): return r*0.16        # diagonal stagger (helical nesting)

def draw(t):
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis("off")

    aturc = ease(t/0.30)
    grow  = ease((t-0.30)/0.70)
    ncols = int(round(grow * CMAX))

    z = 10
    for r in range(ROWS):                     # top->bottom so lower rows draw in front
        y = row_y(r); sx = row_sx(r)
        # gamma-TuRC: GCP rod + gamma-tubulin cap
        rod = FancyBboxPatch((RES_X0+sx, y-0.22), 1.35, 0.44,
                             boxstyle="round,pad=0.02,rounding_size=0.22",
                             fc=C_GCP, ec="#00000066", lw=0.5, alpha=aturc, zorder=z); ax.add_patch(rod)
        if aturc > 0.05:
            sphere(ax, CAP_X+sx, y, RAD, C_GTUB, z+1)
            ax.patches[-2].set_alpha(aturc)   # base of cap sphere
        # green alpha/beta lattice marching to +end
        for c in range(ncols):
            x = GREEN0 + sx + c*DX
            col = C_BETA if c % 2 == 0 else C_ALPHA
            sphere(ax, x, y, RAD, col, z+2+c*0.01)
        z += 5

    # labels
    ax.text(8, 8.45, "The γ-tubulin ring complex nucleates a microtubule",
            ha="center", va="center", color=C_TXT, fontsize=20, fontweight="bold",
            family="DejaVu Sans")
    if aturc > 0.4:
        # brace over gamma-TuRC
        bx0, bx1, by = RES_X0-0.1, CAP_X+0.5, 6.95
        ax.plot([bx0,bx0,bx1,bx1],[by-0.15,by,by,by-0.15], color=C_TXT, lw=1.4, alpha=aturc)
        ax.text((bx0+bx1)/2, by+0.32, "γ-TuRC", ha="center", color=C_TXT, fontsize=14, alpha=aturc)
        ax.text(0.9, row_y(3), "(−) end", ha="center", va="center", color=C_TXT, fontsize=13, alpha=aturc)
    if grow > 0.25:
        xend = GREEN0 + row_sx(3) + (ncols-0.3)*DX
        ax.text(min(15.2, xend+0.7), row_y(3), "(+) end", ha="left", va="center",
                color=C_TXT, fontsize=13, alpha=ease((grow-0.25)/0.4))

    # legend
    sphere(ax, 0.7, 0.85, 0.20, C_BETA, 50); ax.text(1.05, 0.85, "β-tubulin", va="center", color=C_TXT, fontsize=11)
    sphere(ax, 0.7, 0.40, 0.20, C_ALPHA, 50); ax.text(1.05, 0.40, "α-tubulin", va="center", color=C_TXT, fontsize=11)
    sphere(ax, 4.2, 0.62, 0.20, C_GTUB, 50); ax.text(4.55, 0.62, "γ-tubulin", va="center", color=C_TXT, fontsize=11)
    return fig

def save(t, idx):
    fig = draw(t)
    fig.savefig(os.path.join(OUT, f"f{idx:04d}.png"), facecolor=BG)
    plt.close(fig)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "sample"
    if mode == "sample":
        for idx, t in enumerate([0.15, 0.45, 0.75, 1.0]):
            save(t, idx)
        print("samples:", sorted(os.listdir(OUT))[:6])
    else:
        N = 170
        for i in range(N): save(i/(N-1), i)
        for h in range(16): save(1.0, N+h)
        print("rendered", N+16, "frames")
