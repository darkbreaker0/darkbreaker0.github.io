"""Schematic animation: gamma-TuSC -> gamma-TuRC ring template -> microtubule nucleation.
Renders PNG frames; encode to MP4 with ffmpeg afterwards.
Usage:  python nucleation_anim.py sample   (5 keyframes)
        python nucleation_anim.py full      (all frames)
"""
import sys, os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

OUT = os.path.join(os.environ["TEMP"], "nuc_frames")
os.makedirs(OUT, exist_ok=True)

# ---- palette ----
C_GTUB   = "#e0a92e"   # gamma-tubulin (gold)
C_GCP    = "#9aa0a6"   # GCP2/3 stalk (gray)
C_MZT    = "#d6336c"   # MOZART1 (magenta)
C_ALPHA  = "#8fcf9f"   # alpha-tubulin (light green)
C_BETA   = "#3f8f5b"   # beta-tubulin (dark green)
C_TEXT   = "#2c2a25"
C_ACCENT = "#7c5cd6"   # site violet (titles)

N_PF = 13                       # protofilaments / template subunits
MAX_BEADS = 8                   # dimers per protofilament at full growth
import random; random.seed(7)

# template (ring-rim) target positions
TX = [4.0 + 6.0 * i/(N_PF-1) for i in range(N_PF)]          # x 4..10
TY = [2.15 + 0.30*((x-7.0)/3.0)**2 for x in TX]              # gentle smile (ring rim)
# scattered start positions (pre-assembly), deterministic
SX = [x + random.uniform(-2.4, 2.4) for x in TX]
SY = [TY[i] + random.uniform(1.6, 4.2) for i in range(N_PF)]

def ease(u):
    u = max(0.0, min(1.0, u))
    return u*u*(3-2*u)                       # smoothstep

def lerp(a, b, u): return a + (b-a)*u

def draw(t):
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
    ax.set_xlim(0, 14); ax.set_ylim(0, 9); ax.axis("off")

    # phase fractions
    asm  = ease(t/0.42)                       # assembly 0..1 over t<0.42
    mzt  = ease((t-0.40)/0.15)                # MOZART1 fade-in
    grow = ease((t-0.55)/0.45)                # MT growth

    # current subunit positions (scatter -> rim)
    cx = [lerp(SX[i], TX[i], asm) for i in range(N_PF)]
    cy = [lerp(SY[i], TY[i], asm) for i in range(N_PF)]

    # --- GCP stalks (appear as units settle) ---
    for i in range(N_PF):
        ax.plot([cx[i], cx[i]], [cy[i]-0.55, cy[i]-0.02],
                color=C_GCP, lw=3, alpha=0.55*asm, solid_capstyle="round", zorder=1)
    # base ring band under template
    if asm > 0.05:
        ax.plot(cx, [y-0.62 for y in cy], color=C_GCP, lw=6, alpha=0.35*asm,
                solid_capstyle="round", zorder=0)

    # --- microtubule protofilaments (grow upward from each gamma-tubulin) ---
    for i in range(N_PF):
        stagger = (i % 3) * 0.06
        g = ease((grow - stagger) / max(1e-6, 1 - stagger))
        nb = int(round(g * MAX_BEADS))
        for b in range(nb):
            yb = TY[i] + 0.55 + b*0.52
            col = C_ALPHA if b % 2 == 0 else C_BETA
            ax.add_patch(Circle((TX[i], yb), 0.20, fc=col, ec="white", lw=0.6, zorder=4))

    # --- gamma-tubulin template circles (on top) ---
    for i in range(N_PF):
        ax.add_patch(Circle((cx[i], cy[i]), 0.27, fc=C_GTUB, ec="white", lw=1.0, zorder=5))

    # --- MOZART1 dots stapling the seams ---
    for i in range(N_PF-1):
        mx = (TX[i]+TX[i+1])/2; my = (TY[i]+TY[i+1])/2 - 0.28
        ax.add_patch(Circle((mx, my), 0.12, fc=C_MZT, ec="white", lw=0.5,
                            alpha=mzt, zorder=6))

    # --- title (phase-dependent) ---
    if t < 0.42:   title = "γ-tubulin small complexes (γ-TuSC) assemble"
    elif t < 0.55: title = "MOZART1 completes the γ-TuRC ring template"
    else:          title = "The ring templates microtubule nucleation"
    ax.text(7, 8.4, title, ha="center", va="center", fontsize=21, fontweight="bold",
            color=C_ACCENT, family="DejaVu Sans")

    # --- annotations ---
    if asm < 0.9 and t < 0.42:
        # label one scattered pair as gamma-TuSC
        ax.annotate("γ-TuSC", xy=(cx[2], cy[2]), xytext=(cx[2]-1.6, cy[2]+1.1),
                    fontsize=13, color=C_TEXT,
                    arrowprops=dict(arrowstyle="->", color=C_TEXT, lw=1.2))
    if 0.42 <= t < 0.62:
        ax.annotate("γ-TuRC template", xy=(7, TY[6]-0.1), xytext=(9.6, 1.0),
                    fontsize=13, color=C_TEXT,
                    arrowprops=dict(arrowstyle="->", color=C_TEXT, lw=1.2))
        if mzt > 0.3:
            ax.annotate("MOZART1", xy=((TX[3]+TX[4])/2, (TY[3]+TY[4])/2-0.28),
                        xytext=(2.0, 1.0), fontsize=13, color=C_MZT,
                        arrowprops=dict(arrowstyle="->", color=C_MZT, lw=1.2))
    if grow > 0.5:
        ax.annotate("microtubule", xy=(TX[6], TY[6]+0.55+ (MAX_BEADS-1)*0.52),
                    xytext=(10.2, 7.4), fontsize=13, color=C_BETA,
                    arrowprops=dict(arrowstyle="->", color=C_BETA, lw=1.2))

    # legend
    lx = 0.7
    ax.add_patch(Circle((lx, 0.7), 0.16, fc=C_GTUB, ec="white")); ax.text(lx+0.3, 0.7, "γ-tubulin", va="center", fontsize=11, color=C_TEXT)
    ax.add_patch(Circle((lx, 0.25), 0.16, fc=C_BETA, ec="white")); ax.text(lx+0.3, 0.25, "α/β-tubulin", va="center", fontsize=11, color=C_TEXT)

    return fig

def save(t, idx):
    fig = draw(t)
    fig.savefig(os.path.join(OUT, f"f{idx:04d}.png"), facecolor="white")
    plt.close(fig)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "sample"
    if mode == "sample":
        for idx, t in enumerate([0.12, 0.40, 0.52, 0.80, 1.0]):
            save(t, idx)
        print("sample frames:", sorted(os.listdir(OUT))[:10])
    else:
        N = 170
        for i in range(N):
            save(i/(N-1), i)
        for h in range(14):                  # hold last frame
            save(1.0, N+h)
        print("rendered", N+14, "frames to", OUT)
