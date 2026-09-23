#!/usr/bin/env python3
"""Reproduce the TEF U1 radial joint solution used in paper v2.1.

Canonical effective action:
    L_EM = -1/4 F^2
    L_z  = 1/2 |D z|^2 - U(|z|)
    D_mu = partial_mu + i zeta A_mu
    E_R  = 1/2 ∫ [A(u^2)e2 + B e4] d^3x

The script solves the R=40 stationary radial boundary-value problem
by continuation in chi and zeta and prints Q, E, degree, and Gauss closure.
"""

import numpy as np
from scipy.integrate import solve_ivp, solve_bvp, simpson
from scipy.optimize import brentq

Omega0 = 1.0
lam = 2.0
g6 = 1.0
omega = 0.8
A0 = 1.0
B = 2.0
chi_final = 0.35
z0 = 1.0
zeta_final = 0.10
r0 = 1.0e-3
R = 40.0

def scalar_seed(grid):
    delta = Omega0**2 - omega**2
    def integrate(a):
        rhs0 = delta*a - lam*a**3 + g6*a**5
        def ode(r, y):
            u, up = y
            return [up, delta*u - lam*u**3 + g6*u**5 - 2.0*up/r]
        return solve_ivp(
            ode, [r0, R], [a, rhs0*r0/3.0],
            t_eval=grid, rtol=1e-9, atol=1e-11, max_step=0.04
        )
    scan = np.linspace(1.18, 1.34, 17)
    vals = [(a, integrate(a).y[0, -1]) for a in scan]
    bracket = None
    for (a1, f1), (a2, f2) in zip(vals[:-1], vals[1:]):
        if f1*f2 < 0:
            bracket = (a1, a2)
            break
    if bracket is None:
        raise RuntimeError("No nontrivial scalar shooting bracket found.")
    a_star = brentq(lambda a: integrate(a).y[0, -1], *bracket, xtol=1e-13)
    return integrate(a_star)

def frame_seed(grid, tol=1e-7):
    def ode(r, y):
        f, fp = y
        s, c = np.sin(f), np.cos(f)
        K = r*r*A0 + 2.0*B*s*s
        fpp = (
            2.0*A0*s*c
            - 2.0*B*s*c*fp*fp
            + 2.0*B*s**3*c/(r*r)
            - 2.0*r*A0*fp
        ) / K
        return np.vstack((fp, fpp))
    def bc(ya, yb):
        return np.array([ya[0] - np.pi, yb[0]])
    f0 = 2.0*np.arctan(1.5/grid)
    fp0 = np.gradient(f0, grid)
    return solve_bvp(
        ode, bc, grid, np.vstack((f0, fp0)),
        tol=tol, max_nodes=100000
    )

def joint_ode(r, y, chi, zeta):
    u, up, phi, phip, f, fp = y
    s, c = np.sin(f), np.cos(f)
    usq = u*u

    A = A0 - chi*usq/(z0*z0 + usq)
    Au = -2.0*chi*z0*z0*u/(z0*z0 + usq)**2

    e2 = fp*fp + 2.0*s*s/(r*r)
    Omega = omega - zeta*phi

    upp = (
        (Omega0**2 - Omega**2)*u
        - lam*u**3 + g6*u**5
        + 0.5*Au*e2
        - 2.0*up/r
    )
    phipp = -zeta*Omega*u*u - 2.0*phip/r

    K = r*r*A + 2.0*B*s*s
    fpp = (
        2.0*A*s*c
        - 2.0*B*s*c*fp*fp
        + 2.0*B*s**3*c/(r*r)
        - 2.0*r*A*fp
        - r*r*Au*up*fp
    ) / K

    return np.vstack((up, upp, phip, phipp, fp, fpp))

def bc(ya, yb):
    return np.array([
        ya[1],          # u'(0)=0
        ya[3],          # phi'(0)=0
        ya[4]-np.pi,    # f(0)=pi
        yb[0],          # u(R)=0
        yb[2],          # phi(R)=0
        yb[4],          # f(R)=0
    ])

def diagnostics(sol):
    r = np.linspace(r0, R, 12000)
    u, up, phi, phip, f, fp = sol.sol(r)
    s = np.sin(f)
    usq = u*u

    A = A0 - chi_final*usq/(z0*z0 + usq)
    e2 = fp*fp + 2.0*s*s/(r*r)
    e4 = 2.0*s*s*fp*fp/(r*r) + s**4/(r**4)
    Omega = omega - zeta_final*phi
    U = 0.5*Omega0**2*u*u - 0.25*lam*u**4 + (g6/6.0)*u**6

    shell = 4.0*np.pi*r*r
    integ = lambda x: float(simpson(shell*x, x=r))

    Q = integ(Omega*u*u)
    E = integ(
        0.5*Omega**2*u*u
        + 0.5*up*up
        + U
        + 0.5*phip*phip
        + 0.5*(A*e2 + B*e4)
    )
    degree = float(-(2.0/np.pi)*simpson(np.sin(f)**2*fp, x=r))

    y0 = sol.sol(np.array([r0]))[:, 0]
    yR = sol.sol(np.array([R]))[:, 0]
    flux = -4.0*np.pi*(R**2*yR[3] - r0**2*y0[3])
    gauss_rel = abs(flux-zeta_final*Q)/abs(zeta_final*Q)

    return Q, E, degree, gauss_rel

def main():
    grid = np.linspace(r0, R, 1000)

    ss = scalar_seed(grid)
    sf = frame_seed(grid)

    init = np.vstack((
        ss.y[0], ss.y[1],
        np.zeros_like(grid), np.zeros_like(grid),
        sf.sol(grid)[0], sf.sol(grid)[1]
    ))

    sol = solve_bvp(
        lambda r, y: joint_ode(r, y, 0.0, 0.0),
        bc, grid, init, tol=1e-6, max_nodes=150000
    )

    for chi in (0.10, 0.20, 0.35):
        sol = solve_bvp(
            lambda r, y, chi=chi: joint_ode(r, y, chi, 0.0),
            bc, grid, sol.sol(grid), tol=1e-6, max_nodes=150000
        )

    for zeta in (0.025, 0.050, 0.075, 0.100):
        sol = solve_bvp(
            lambda r, y, zeta=zeta: joint_ode(r, y, chi_final, zeta),
            bc, grid, sol.sol(grid), tol=1e-6, max_nodes=150000
        )

    Q, E, degree, gauss_rel = diagnostics(sol)

    print(f"status={sol.status}")
    print(f"adaptive_nodes={sol.x.size}")
    print(f"max_rms_residual={np.max(sol.rms_residuals):.6e}")
    print(f"Q={Q:.12f}")
    print(f"E={E:.12f}")
    print(f"degree={degree:.12f}")
    print(f"gauss_relative_mismatch={gauss_rel:.6e}")

if __name__ == "__main__":
    main()
