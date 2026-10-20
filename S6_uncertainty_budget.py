#!/usr/bin/env python3

import math

PHI = lambda z: 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


params = {
    "pH":        (0.17, 16.0, 0.5,  "pH unit"),
    "DO":        (0.27, 14.0, 0.7,  "mg/L"),
    "Turbidity": (0.12, 0.8,  2.5,  "NTU"),
    "EC":        (0.11, 0.05, 15.0, "uS/cm"),
    "Temp":      (0.16, 2.0,  0.4,  "degC"),
}  

rho = 0.9          
uB3 = 1.5          
uB4_inf = 2.5      
uB4_wt = 2.0       
WQI0, THR = 55.0, 50.0  

def compose(rho=rho, scale_B1=1.0, uB3=uB3, uB4_inf=uB4_inf, uB4_wt=uB4_wt, r_intra=0.0):
    cs = {p: w * s * u * scale_B1 for p, (w, s, u, _) in params.items()}
    uB1sq = sum(c * c for c in cs.values())
    if r_intra:  
        uB1sq += 2.0 * r_intra * cs["pH"] * cs["DO"]
    tot = uB1sq / rho + uB3 ** 2 + uB4_inf ** 2 + uB4_wt ** 2
    u = math.sqrt(tot)
    pwrong = PHI(-(WQI0 - THR) / u)
    return math.sqrt(uB1sq), tot, u, pwrong

print("Per-parameter contributions c_i = w_i * s_i * u(x_i)  [WQI points]:")
for p, (w, s, u, unit) in params.items():
    c = w * s * u
    print(f"  {p:9s} w={w:.2f} s={s:5.2f}/{unit:7s} u={u:5.2f} -> c={c:.3f}  c^2={c*c:.3f}")

uB1, tot, u, pw = compose()
print(f"\nBASELINE: u_B1={uB1:.2f} -> u_B1^2/rho={uB1**2/rho:.2f}; "
      f"u^2 total={tot:.2f}; u(WQI)={u:.2f}; P(wrong call)={100*pw:.1f}%")
_, _, u_b3perf, pw_b3 = compose(uB3=0.0)
print(f"B3 perfected only: u={u_b3perf:.2f}, P={100*pw_b3:.1f}%")
_, _, u_co, pw_co = compose(rho=0.98, scale_B1=0.5, uB4_inf=1.25, uB4_wt=1.0)
print(f"Co-design (B1,B4 halved; rho=0.98): u={u_co:.2f}, P={100*pw_co:.1f}%")

print("\nSENSITIVITY (one factor at a time; others at baseline):")
rows = []
for lbl, kw in [
    ("baseline", {}),
    ("sensing/drift term -50%", {"scale_B1": 0.5}),
    ("sensing/drift term +50%", {"scale_B1": 1.5}),
    ("delivery rho=0.7", {"rho": 0.7}),
    ("delivery rho=0.98", {"rho": 0.98}),
    ("calibration residual x2 (uB3=3.0)", {"uB3": 3.0}),
    ("soft-sensing error x2 (uB4,inf=5.0)", {"uB4_inf": 5.0}),
    ("weighting unc. x2 (uB4,wt=4.0)", {"uB4_wt": 4.0}),
    ("correlated pH-DO drift r=0.5", {"r_intra": 0.5}),
]:
    _, _, uu, pp = compose(**kw)
    rows.append((lbl, uu, pp))
    print(f"  {lbl:38s} u(WQI)={uu:4.2f}  P={100*pp:4.1f}%")
