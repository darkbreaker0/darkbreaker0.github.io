"""Pseudo-3D microtubule nucleation (polished): tilted, longer, rotating shaded
cylinder from a layered gamma-TuRC cone with a prominent purple GCP base.
Usage: python nucleation_v4.py sample | full
"""
import sys, os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.colors import to_rgb

OUT = os.path.join(os.environ["TEMP"], "nuc4_frames")
os.makedirs(OUT, exist_ok=True)

BG    = "#0a0a0a"
A_COL = "#a9d69b"   # alpha-tubulin (light green, less white -> uniform palette)
B_COL = "#34995a"   # beta-tubulin (mid-dark green)
GTUB  = "#cf2b2b"   # gamma-tubulin (red)
GCP   = "#e0922e"   # GCP staves (orange)
GCPB  = "#9b6fc7"   # GCP base (purple)
TXT   = "#f0f0f0"

N=13; R=1.55; YC=4.3; X0=4.6; DX=0.57; PITCH=0.13; RAD=0.34; NR=15; TILT=0.11

def ease(u):
    u=max(0,min(1,u)); return u*u*(3-2*u)
def shade(col,f):
    r,g,b=to_rgb(col); k=0.42+0.58*f; return (r*k,g*k,b*k)
def bead(ax,x,y,depth,col,zb=0.0):
    f=(depth+1)/2; rr=RAD*(0.80+0.20*f); z=100+depth*40+zb
    ax.add_patch(Circle((x,y),rr,fc=shade(col,f),ec="#00000055",lw=0.4,zorder=z))
    if depth>-0.2:
        ax.add_patch(Circle((x-0.33*rr,y+0.33*rr),rr*0.40,fc="white",ec="none",
                            alpha=0.20+0.18*f,zorder=z+0.1))

def draw(t):
    fig,ax=plt.subplots(figsize=(12.8,7.2),dpi=100)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(0,16); ax.set_ylim(0,9); ax.axis("off")

    grow=ease((t-0.08)/0.52)
    rot =ease((t-0.62)/0.38)*0.55
    nr=int(round(grow*NR))
    th=[2*math.pi*i/N+rot for i in range(N)]

    apex=(X0-2.9, YC-0.25)
    # prominent purple GCP base (larger, fanned)
    for k in range(7):
        a=math.pi*(k/6.0)-math.pi/2          # -90..+90 deg fan
        px=apex[0]-0.15+0.45*math.cos(a)
        py=YC+1.25*math.sin(a)
        d=0.4*math.cos(a); f=(d+1)/2
        ax.add_patch(Circle((px,py),0.60*(0.8+0.2*f),fc=shade(GCPB,f),
                            ec="#00000055",lw=0.4,zorder=38+d*5))
    # orange GCP staves + red gamma-tubulin caps (rotate with tube)
    order=sorted(range(N),key=lambda i:math.sin(th[i]))
    for i in order:
        vy=R*math.cos(th[i]); depth=math.sin(th[i]); f=(depth+1)/2
        s=i*PITCH-0.5*DX
        capx=X0+s; capy=YC+vy+TILT*s
        ax.plot([apex[0]+0.25,capx],[YC+0.4*vy-0.1,capy],
                color=shade(GCP,f),lw=7*(0.7+0.3*f),solid_capstyle="round",
                zorder=50+depth*40)
        bead(ax,capx,capy,depth,GTUB,zb=2)
    # microtubule cylinder (tilted), back->front
    dl=[]
    for i in range(N):
        for j in range(nr):
            s=i*PITCH+j*DX
            vy=R*math.cos(th[i]); depth=math.sin(th[i])
            col=A_COL if j%2==0 else B_COL
            dl.append((depth,X0+s,YC+vy+TILT*s,col))
    for depth,x,y,col in sorted(dl,key=lambda u:u[0]):
        bead(ax,x,y,depth,col)

    # labels
    ax.text(8,8.5,"The γ-tubulin ring complex nucleates a microtubule",
            ha="center",color=TXT,fontsize=20,fontweight="bold",family="DejaVu Sans")
    ax.text(apex[0]-0.3,YC+2.2,"γ-TuRC",ha="center",color=TXT,fontsize=14)
    ax.annotate("(−) end",xy=(X0-0.7,YC-2.0),xytext=(X0-2.6,YC-2.9),color=TXT,fontsize=13)
    if grow>0.3:
        s_end=(N-1)*PITCH+(nr-1)*DX
        xr=X0+s_end+RAD; yr=YC+TILT*s_end
        ax.text(min(15.0,xr+0.45),yr,"(+) end",va="center",color=TXT,fontsize=13,
                alpha=ease((grow-0.3)/0.4))
    for k,(c,lab) in enumerate([(B_COL,"β-tubulin"),(A_COL,"α-tubulin"),(GTUB,"γ-tubulin"),(GCP,"GCP"),(GCPB,"GCP base")]):
        ax.add_patch(Circle((0.8+k*2.7,0.55),0.18,fc=c,ec="#00000055"))
        ax.text(1.05+k*2.7,0.55,lab,va="center",color=TXT,fontsize=10)
    return fig

def save(t,idx):
    fig=draw(t); fig.savefig(os.path.join(OUT,f"f{idx:04d}.png"),facecolor=BG); plt.close(fig)

if __name__=="__main__":
    mode=sys.argv[1] if len(sys.argv)>1 else "sample"
    if mode=="sample":
        for idx,t in enumerate([0.35,0.62,0.85,1.0]): save(t,idx)
        print("samples done")
    else:
        NF=200
        for i in range(NF): save(i/(NF-1),i)
        for h in range(18): save(1.0,NF+h)
        print("rendered",NF+18)
