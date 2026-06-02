"""Pseudo-3D microtubule nucleation (evokes BioRender image-3 style):
shaded cylindrical MT of alpha/beta beads emerging from a layered gamma-TuRC cone.
Usage: python nucleation_v3.py sample | full
"""
import sys, os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
from matplotlib.colors import to_rgb

OUT = os.path.join(os.environ["TEMP"], "nuc3_frames")
os.makedirs(OUT, exist_ok=True)

BG     = "#0a0a0a"
A_COL  = "#dff0cf"   # alpha-tubulin (pale green)
B_COL  = "#2f9e54"   # beta-tubulin (dark green)
GTUB   = "#cf2b2b"   # gamma-tubulin (red)
GCP    = "#e08a2e"   # GCP staves (orange)
GCPB   = "#9b6fc7"   # GCP base (purple)
TXT    = "#f0f0f0"

N   = 13            # protofilaments
R   = 1.6           # tube radius (screen)
YC  = 4.7           # tube axis y
X0  = 5.0           # +x start of green lattice (minus end of tube)
DX  = 0.60          # axial dimer spacing
PITCH = 0.135       # helical x-offset per protofilament
RAD = 0.35
NR  = 12            # rings at full growth

def ease(u):
    u=max(0,min(1,u)); return u*u*(3-2*u)

def shade(col, f):                       # f in 0..1, 1=front/bright
    r,g,b = to_rgb(col); k = 0.42+0.58*f
    return (r*k, g*k, b*k)

def bead(ax, x, y, depth, base_col, zbias=0.0):
    f = (depth+1)/2.0
    rr = RAD*(0.80+0.20*f)
    z  = 100 + depth*40 + zbias
    ax.add_patch(Circle((x,y), rr, fc=shade(base_col,f), ec="#00000055", lw=0.4, zorder=z))
    if depth > -0.2:                     # highlight on front-facing beads
        ax.add_patch(Circle((x-0.33*rr, y+0.33*rr), rr*0.40, fc="white",
                            ec="none", alpha=0.22+0.18*f, zorder=z+0.1))

def draw(grow):
    fig, ax = plt.subplots(figsize=(12.8,7.2), dpi=100)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0,16); ax.set_ylim(0,9); ax.axis("off")

    nr = int(round(grow*NR))
    th = [2*math.pi*i/N for i in range(N)]

    # ---- gamma-TuRC cone (left of tube) ----
    apex = (X0-3.0, YC)
    # purple GCP base blobs near apex
    for k in range(6):
        a = 2*math.pi*k/6
        px = apex[0]-0.25 + 0.30*math.cos(a)
        py = YC + 0.95*math.sin(a)
        d  = math.cos(a)                  # crude depth
        f  = (d+1)/2
        ax.add_patch(Circle((px,py), 0.42*(0.8+0.2*f), fc=shade(GCPB,f),
                            ec="#00000055", lw=0.4, zorder=40+d*5))
    # orange GCP staves + red gamma-tubulin caps, one per protofilament
    order = sorted(range(N), key=lambda i: math.sin(th[i]))   # back first
    for i in order:
        vy = R*math.cos(th[i]); depth = math.sin(th[i]); f=(depth+1)/2
        capx, capy = X0-0.45 + i*PITCH, YC+vy
        ax.plot([apex[0]+0.2, capx], [YC + 0.45*vy, capy],
                color=shade(GCP,f), lw=7*(0.7+0.3*f), solid_capstyle="round",
                zorder=50+depth*40)
        bead(ax, capx, capy, depth, GTUB, zbias=2)

    # ---- microtubule cylinder ----
    draw_list = []
    for i in range(N):
        vy = R*math.cos(th[i]); depth = math.sin(th[i])
        for j in range(nr):
            x = X0 + i*PITCH + j*DX
            col = A_COL if (j % 2 == 0) else B_COL
            draw_list.append((depth, x, YC+vy, col))
    for depth,x,y,col in sorted(draw_list, key=lambda t:t[0]):   # back->front
        bead(ax, x, y, depth, col)

    # ---- labels ----
    ax.text(8, 8.5, "The γ-tubulin ring complex nucleates a microtubule",
            ha="center", color=TXT, fontsize=20, fontweight="bold", family="DejaVu Sans")
    ax.text(apex[0]-0.6, 7.0, "γ-TuRC", ha="center", color=TXT, fontsize=14)
    ax.annotate("(−) end", xy=(X0-0.6, YC-2.4), xytext=(X0-2.2, YC-3.1),
                color=TXT, fontsize=13)
    if grow > 0.3:
        xr = X0 + (N-1)*PITCH + (nr-1)*DX + RAD
        ax.text(min(14.9, xr+0.5), YC, "(+) end", va="center", color=TXT, fontsize=13,
                alpha=ease((grow-0.3)/0.4))
    # legend
    for k,(c,lab) in enumerate([(B_COL,"β-tubulin"),(A_COL,"α-tubulin"),(GTUB,"γ-tubulin"),(GCP,"GCP"),(GCPB,"GCP base")]):
        ax.add_patch(Circle((0.8+k*2.7, 0.6), 0.18, fc=c, ec="#00000055"))
        ax.text(1.05+k*2.7, 0.6, lab, va="center", color=TXT, fontsize=10)
    return fig

def save(grow, idx):
    fig=draw(grow); fig.savefig(os.path.join(OUT,f"f{idx:04d}.png"), facecolor=BG); plt.close(fig)

if __name__=="__main__":
    mode = sys.argv[1] if len(sys.argv)>1 else "sample"
    if mode=="sample":
        for idx,g in enumerate([0.45, 1.0]): save(g, idx)
        print("samples done")
    else:
        N_F=170
        for i in range(N_F): save(ease(i/(N_F-1))*0.0 + i/(N_F-1), i)  # linear grow; cone always present
        for h in range(16): save(1.0, N_F+h)
        print("rendered", N_F+16)
