"""Independent symbolic/finite-difference checks and figures for integrated working paper v2.

Run with the bundled Python runtime. Outputs are generated artifacts, not inputs.
"""
from pathlib import Path
import json
import numpy as np
import sympy as sp
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]


def symbolic_checks():
    r, theta, lam, R, a, psi = sp.symbols("r theta lam R a psi", real=True)
    chi = r / a + psi
    C, S = sp.cos(chi), sp.sin(chi)
    n = sp.Matrix([sp.sin(theta) * sp.cos(lam), sp.sin(theta) * sp.sin(lam), sp.cos(theta)])
    et = sp.diff(n, theta)
    el = sp.Matrix([-sp.sin(lam), sp.cos(lam), 0])
    basis = sp.Matrix.hstack(n, et, el)
    u = C * et + S * el
    y = r * n + R * u
    coords = [r, theta, lam]
    D = r * sp.sin(theta) + R * C * sp.cos(theta)
    b = R / a
    expected_J = sp.Matrix([
        [1, -R * C, -R * S * sp.sin(theta)],
        [-b * S, r, -R * S * sp.cos(theta)],
        [b * C, 0, D],
    ])
    def zero(expression):
        assert sp.trigsimp(sp.expand_trig(expression)) == 0, expression

    for value in y.jacobian(coords) - basis * expected_J:
        zero(value)
    zero(expected_J.det() - r * D)
    zero(y.dot(y) - r**2 - R**2)
    expected_K = {
        (0, 0): -R / a**2 * u,
        (0, 1): et + b * S * n,
        (0, 2): -b * C * sp.sin(theta) * n - b * C * sp.cos(theta) * et
                + (sp.sin(theta) - b * S * sp.cos(theta)) * el,
        (1, 1): -r * n - R * C * et,
        (1, 2): (r * sp.cos(theta) - R * C * sp.sin(theta)) * el,
        (2, 2): -D * sp.sin(theta) * n - D * sp.cos(theta) * et - R * S * el,
    }
    for (i, j), expected in expected_K.items():
        for value in sp.diff(y, coords[i], coords[j]) - expected:
            zero(value)
    zero(expected_J[:, 0].dot(expected_J[:, 0]) - 1 - b**2)
    # A second construction of the metric from the moving coframe.
    coframe = sp.Matrix([[1, 0, 0], [0, C, S * sp.sin(theta)], [0, -S, C * sp.sin(theta)]])
    Au, Aw = S * sp.cot(theta), C * sp.cot(theta)
    moving = sp.Matrix([[1, -R, 0], [0, r, 0], [b, R * Au, r + R * Aw]])
    metric_difference = expected_J.T * expected_J - (moving * coframe).T * (moving * coframe)
    for value in metric_difference:
        zero(value)
    return "PASS: Cartesian differentiation verifies J, all six Hessians, determinant, norm, and coframe metric"


def geometry(xi, R, a, psi):
    r, theta, lam = np.asarray(xi)
    st, ct, sl, cl = np.sin(theta), np.cos(theta), np.sin(lam), np.cos(lam)
    C, S = np.cos(r / a + psi), np.sin(r / a + psi)
    n = np.array([st * cl, st * sl, ct])
    et = np.array([ct * cl, ct * sl, -st])
    el = np.array([-sl, cl, 0.0])
    u = C * et + S * el
    w = -S * et + C * el
    return n, et, el, u, w, C, S, r * st + R * C * ct


def forward(xi, R, a, psi):
    n, _, _, u, *_ = geometry(xi, R, a, psi)
    return xi[0] * n + R * u


def inverse(y, R, a, psi, theta0=np.pi / 4):
    norm2 = np.dot(y, y)
    if norm2 <= R**2:
        raise ValueError("Outside the positive-r realization")
    r = np.sqrt(norm2 - R**2)
    C, S = np.cos(r / a + psi), np.sin(r / a + psi)
    d = np.hypot(r, R * C)
    argument = y[2] / d
    if abs(argument) > 1 + 2e-14:
        raise ValueError("Outside the inverse branch")
    theta = np.arccos(np.clip(argument, -1, 1)) - np.arctan2(R * C, r)
    if not (r > R / np.tan(theta0) and theta0 < theta < np.pi - theta0):
        raise ValueError("Outside the chosen injective belt")
    D = r * np.sin(theta) + R * C * np.cos(theta)
    lam = np.arctan2(y[1], y[0]) - np.arctan2(R * S, D)
    return np.array([r, theta, (lam + np.pi) % (2 * np.pi) - np.pi])


def derivatives(xi, R, a, psi):
    r, theta, _ = xi
    n, et, el, u, _, C, S, D = geometry(xi, R, a, psi)
    st, ct, b = np.sin(theta), np.cos(theta), R / a
    basis = np.column_stack((n, et, el))
    J = basis @ np.array([[1, -R*C, -R*S*st], [-b*S, r, -R*S*ct], [b*C, 0, D]])
    K = np.zeros((3, 3, 3))  # Cartesian component, coordinate i, coordinate j
    entries = {
        (0, 0): -R/a**2*u,
        (0, 1): et+b*S*n,
        (0, 2): -b*C*st*n-b*C*ct*et+(st-b*S*ct)*el,
        (1, 1): -r*n-R*C*et,
        (1, 2): (r*ct-R*C*st)*el,
        (2, 2): -D*st*n-D*ct*et-R*S*el,
    }
    for (i, j), value in entries.items():
        K[:, i, j] = value
        K[:, j, i] = value
    return J, K


def five_point(f, h=0.002):
    fm2, fm1, f0, fp1, fp2 = [f(k*h) for k in [-2, -1, 0, 1, 2]]
    first = (fm2 - 8*fm1 + 8*fp1 - fp2) / (12*h)
    second = (-fp2 + 16*fp1 - 30*f0 + 16*fm1 - fm2) / (12*h*h)
    return first, second


def numerical_checks():
    rng = np.random.default_rng(20260925)
    maxima = dict(round_trip=0.0, jacobian=0.0, inverse_velocity=0.0,
                  acceleration=0.0, straight_velocity=0.0, straight_acceleration=0.0,
                  averaging=0.0)
    for _ in range(1200):
        R = np.exp(rng.uniform(-3, 2))
        a = R * np.exp(rng.uniform(-2, 1.5))
        psi = rng.uniform(-np.pi, np.pi)
        xi = np.array([R*rng.uniform(1.001, 18), rng.uniform(np.pi/4+0.001, 3*np.pi/4-0.001), rng.uniform(-np.pi, np.pi)])
        y = forward(xi, R, a, psi)
        recovered = inverse(y, R, a, psi)
        error = recovered-xi
        error[0] /= R
        error[2] = np.arctan2(np.sin(error[2]), np.cos(error[2]))
        maxima["round_trip"] = max(maxima["round_trip"], float(np.max(np.abs(error))))
        J, _ = derivatives(xi, R, a, psi)
        finite_J = np.column_stack([
            (forward(xi + np.eye(3)[i]*h, R, a, psi)-forward(xi - np.eye(3)[i]*h, R, a, psi))/(2*h)
            for i, h in enumerate([1e-5*a, 1e-5, 1e-5])
        ])
        maxima["jacobian"] = max(maxima["jacobian"], float(np.linalg.norm(J-finite_J)/max(1, np.linalg.norm(J))))
        V = rng.normal(size=3)
        r, theta, _ = xi
        _, _, el, _, _, C, S, D = geometry(xi, R, a, psi)
        rd = np.dot(y, V)/r
        direct = np.array([rd, ((np.cos(theta)+(R/a)*S*np.sin(theta))*rd-V[2])/D, (np.dot(V, el)-(R/a)*C*rd)/D])
        maxima["inverse_velocity"] = max(maxima["inverse_velocity"], float(np.linalg.norm(J@direct-V)/max(1, np.linalg.norm(V))))
    for _ in range(25):
        R, a, psi = 1.0, rng.uniform(0.5, 2.0), rng.uniform(-np.pi, np.pi)
        xi = np.array([rng.uniform(2, 8), rng.uniform(1.0, 2.0), rng.uniform(-2, 2)])
        velocity = rng.uniform(-0.3, 0.3, 3)
        acceleration = rng.uniform(-0.15, 0.15, 3)
        J, K = derivatives(xi, R, a, psi)
        expected = J@acceleration + np.einsum("kij,i,j->k", K, velocity, velocity)
        _, finite_accel = five_point(lambda t: forward(xi+velocity*t+acceleration*t*t/2, R, a, psi))
        maxima["acceleration"] = max(maxima["acceleration"], float(np.linalg.norm(expected-finite_accel)))
        y0 = forward(xi, R, a, psi)
        V = rng.uniform(-0.4, 0.4, 3)
        xdot, xddot = five_point(lambda t: inverse(y0+V*t, R, a, psi))
        reconstructed_V = J@xdot
        reconstructed_A = J@xddot+np.einsum("kij,i,j->k", K, xdot, xdot)
        maxima["straight_velocity"] = max(maxima["straight_velocity"], float(np.linalg.norm(reconstructed_V-V)))
        maxima["straight_acceleration"] = max(maxima["straight_acceleration"], float(np.linalg.norm(reconstructed_A)))
    p1 = forward([1, 2*np.pi/3, 0], 1, 1, -1)
    p2 = forward([1, 5*np.pi/6, np.pi], 1, 1, -1)
    assert np.linalg.norm(p1-p2) < 1e-14
    assert abs(np.linalg.det(derivatives([1, 3*np.pi/4, 0.7], 1, 1, -1)[0])) < 1e-14
    # Independent Gauss-Legendre quadrature of the time average.
    nodes, weights = np.polynomial.legendre.leggauss(256)
    R, a, v, psi = 1.0, 0.7, 0.8, 0.4
    xi = np.array([30.0, 1.2, 0.3])
    n, _, _, u, w, *_ = geometry(xi, R, a, psi)
    omega = v/a
    T = 2*np.pi/omega
    for fraction in [0.07, 0.5, 1.0, 1.3, 4.0, 8.1]:
        delta = fraction*T
        samples_X, samples_V, samples_A = [], [], []
        for t in nodes*delta/2:
            xt = xi + np.array([v*t, 0, 0])
            _, _, _, ut, wt, *_ = geometry(xt, R, a, psi)
            samples_X.append(forward(xt, R, a, psi))
            samples_V.append(v*n+R*omega*wt)
            samples_A.append(-R*omega**2*ut)
        fac = np.sinc(fraction)
        expected = [xi[0]*n+R*fac*u, v*n+R*omega*fac*w, -R*omega**2*fac*u]
        for samples, target in zip([samples_X, samples_V, samples_A], expected):
            observed = weights@np.array(samples)/2
            maxima["averaging"] = max(maxima["averaging"], float(np.linalg.norm(observed-target)))
    thresholds = dict(round_trip=1e-10, jacobian=2e-8, inverse_velocity=1e-11,
                      acceleration=2e-7, straight_velocity=2e-8, straight_acceleration=2e-7,
                      averaging=1e-10)
    for key, limit in thresholds.items():
        assert maxima[key] < limit, (key, maxima[key], limit)
    for bad in [np.zeros(3), np.array([0.5, 0, 0]), np.array([0, 0, 5.0])]:
        try:
            inverse(bad, 1, 1, 0)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid image point accepted")
    return {"sample_count": 1200, "trajectory_count": 25,
            "max_errors": maxima, "tolerances": thresholds,
            "fold_and_noninjectivity": "PASS", "image_rejection": "PASS"}


def figures():
    out = ROOT / "figures"
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 14, "axes.labelsize": 14, "axes.titlesize": 14,
                         "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 12,
                         "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.dpi": 170})
    fig = plt.figure(figsize=(11.5, 4.2), constrained_layout=True)
    ax = fig.add_subplot(121, projection="3d")
    colors = ["#1f657a", "#b9532a", "#675191"]
    for theta, lam, color in zip([np.pi/3, np.pi/2, 2*np.pi/3], [-0.75, 0, 0.75], colors):
        rs = np.linspace(1.05, 11, 600)
        points = np.array([forward([r, theta, lam], 1, 1, 0) for r in rs])
        n = geometry([2, theta, lam], 1, 1, 0)[0]
        ax.plot(*points.T, color=color, lw=1.7)
        axis = np.array([np.zeros(3), 11*n])
        ax.plot(*axis.T, color=color, lw=0.9, ls="--", alpha=0.7)
    ax.scatter([0], [0], [0], c="black", s=15)
    ax.text(0, 0, 0.7, "$O$")
    ax.set(xlabel="$x/R$", ylabel="$y/R$", zlabel="$z/R$", title="Common initial phase")
    ax.view_init(elev=23, azim=-58)
    ax.set_box_aspect((1, 1, 0.85))
    ax = fig.add_subplot(122)
    angles = np.linspace(15, 165, 500)
    radial = np.linspace(0.1, 4, 450)
    tt, rr = np.meshgrid(np.deg2rad(angles), radial)
    D = rr*np.sin(tt)+np.cos(rr)*np.cos(tt)
    im = ax.pcolormesh(angles, radial, D, shading="auto", cmap="RdBu_r", vmin=-4, vmax=4, rasterized=True)
    ax.contour(angles, radial, D, levels=[0], colors="white", linewidths=1.8)
    ax.add_patch(Rectangle((45, 1), 90, 2.9, fill=False, edgecolor="black", linestyle="--", linewidth=1.5))
    ax.text(90, 3.6, "guaranteed injective belt", ha="center", fontsize=12,
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=3))
    ax.set(xlabel="Polar angle $\\theta$ (degrees)", ylabel="Axial distance $r/R$", title="Section regularity $D/R$ ($q=1$)")
    fig.colorbar(im, ax=ax, shrink=0.85)
    fig.savefig(out/"coordinates_v2.pdf")
    fig.savefig(out/"coordinates_v2.png")
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 3.65), constrained_layout=True)
    x = np.geomspace(1, 1000, 400)
    axes[0].loglog(x, 1/x, color="#1f657a", lw=2, label="Position: $R/r$")
    axes[0].loglog(x, np.ones_like(x), color="#b9532a", lw=2, label="Tangent: $1/q$ with $q=1$")
    axes[0].set(xlabel="Axial distance $r/R$", ylabel="Dimensionless correction", title="Position and tangent limits")
    axes[0].legend(frameon=False, loc="lower left")
    axes[0].grid(alpha=0.18, which="major")
    x = np.linspace(0, 5, 1200)
    axes[1].plot(x, np.abs(np.sinc(x)), color="#1f657a", lw=2, label="Exact box-average factor")
    envelope = np.ones_like(x)
    np.divide(1, np.pi*x, out=envelope, where=x > 0)
    envelope = np.minimum(1, envelope)
    axes[1].plot(x, envelope, color="#b9532a", lw=1.3, ls="--", label="Envelope")
    axes[1].set(xlabel="Averaging duration $\\Delta/T$", ylabel="Normalized transverse amplitude", title="Finite-window suppression", ylim=(-0.02, 1.05))
    axes[1].legend(frameon=False)
    axes[1].grid(alpha=0.18)
    fig.savefig(out/"scales_v2.pdf")
    fig.savefig(out/"scales_v2.png")
    plt.close(fig)



def phase_checks():
    """Check the four-variable map independently of the manuscript's coframe."""
    r, th, la, psi, R, a = sp.symbols("r th la psi R a", real=True)
    chi = r/a + psi
    C, S = sp.cos(chi), sp.sin(chi)
    n = sp.Matrix([sp.sin(th)*sp.cos(la), sp.sin(th)*sp.sin(la), sp.cos(th)])
    et = n.diff(th)
    el = sp.Matrix([-sp.sin(la), sp.cos(la), 0])
    u, w = C*et+S*el, -S*et+C*el
    y = r*n+R*u
    coords = [r, th, la, psi]

    def zero(expr):
        assert sp.trigsimp(sp.expand_trig(expr)) == 0, expr

    extra = {
        (3,): R*w,
        (3, 3): -R*u,
        (0, 3): -R*u/a,
        (1, 3): R*S*n,
        (2, 3): -R*C*sp.sin(th)*n-R*C*sp.cos(th)*et-R*S*sp.cos(th)*el,
    }
    for indices, target in extra.items():
        actual = y
        for j in indices:
            actual = actual.diff(coords[j])
        for val in actual-target:
            zero(val)
    eta = sp.Matrix([[0, C, S*sp.sin(th), 0]])
    zeta = sp.Matrix([[0, -S, C*sp.sin(th), 0]])
    omega = sp.Matrix([[1/a, 0, sp.cos(th), 1]])
    dr = sp.Matrix([[1, 0, 0, 0]])
    for val in y.jacobian(coords) - (n*(dr-R*eta)+u*(r*eta)+w*(r*zeta+R*omega)):
        zero(val)

    # Coefficients of all four independent differentials in the frame identities.
    for actual, target in [
        (n.jacobian(coords), u*eta+w*zeta),
        (u.jacobian(coords), -n*eta+w*omega),
        (w.jacobian(coords), -n*zeta-u*omega),
    ]:
        for val in actual-target:
            zero(val)
    coframe = sp.Matrix.vstack(dr, eta, zeta, omega)
    zero(coframe.det()-sp.sin(th))
    matrix = sp.Matrix([[1, -R, 0, 0], [0, r, 0, 0], [0, 0, r, R]])
    assert matrix*sp.Matrix([0, 0, R, -r]) == sp.zeros(3, 1)
    assert matrix*sp.Matrix([0, 0, 0, 1]) == sp.Matrix([0, 0, R])
    assert matrix[:, [0, 1, 3]].det() == R*r
    assert (matrix.T*matrix).det() == 0

    # Cartesian Hessians are independent of the moving-frame acceleration formula.
    J = y.jacobian(coords)
    jf = sp.lambdify((coords, R, a), J, "numpy")
    kf = [sp.lambdify((coords, R, a), J[:, j].jacobian(coords), "numpy") for j in range(4)]
    rng = np.random.default_rng(29092026)
    max_fd = 0.0
    max_frame = 0.0
    for _ in range(60):
        radius = rng.uniform(0.4, 1.2)
        pitch = rng.uniform(0.5, 1.5)
        x = np.array([rng.uniform(2, 6), rng.uniform(0.6, 2.5),
                      rng.uniform(-2, 2), rng.uniform(-2, 2)])
        vel, acc = rng.uniform(-0.4, 0.4, 4), rng.uniform(-0.2, 0.2, 4)
        cart_acc = jf(x, radius, pitch)@acc
        for j in range(4):
            cart_acc += vel[j]*(kf[j](x, radius, pitch)@vel)
        _, finite_acc = five_point(lambda t: forward(
            (x+vel*t+acc*t*t/2)[:3], radius, pitch, (x+vel*t+acc*t*t/2)[3]))
        max_fd = max(max_fd, float(np.linalg.norm(cart_acc-finite_acc)))

        rv, tv, lv, pv = vel
        ra, ta, laa, pa = acc
        rr, theta = x[:2]
        nn, _, _, uu, ww, cc, ss, _ = geometry(x[:3], radius, pitch, x[3])
        chiv = rv/pitch+pv
        etat = cc*tv+ss*np.sin(theta)*lv
        zetat = -ss*tv+cc*np.sin(theta)*lv
        nu = chiv+np.cos(theta)*lv
        etad = (-ss*chiv*tv+cc*ta+cc*chiv*np.sin(theta)*lv
                +ss*np.cos(theta)*tv*lv+ss*np.sin(theta)*laa)
        zetad = (-cc*chiv*tv-ss*ta-ss*chiv*np.sin(theta)*lv
                 +cc*np.cos(theta)*tv*lv+cc*np.sin(theta)*laa)
        nud = ra/pitch+pa-np.sin(theta)*tv*lv+np.cos(theta)*laa
        vn, vu, vw = rv-radius*etat, rr*etat, rr*zetat+radius*nu
        vnd, vud, vwd = ra-radius*etad, rv*etat+rr*etad, rv*zetat+rr*zetad+radius*nud
        frame_acc = ((vnd-etat*vu-zetat*vw)*nn
                     +(vud+etat*vn-nu*vw)*uu
                     +(vwd+zetat*vn+nu*vu)*ww)
        max_frame = max(max_frame, float(np.linalg.norm(frame_acc-cart_acc)))

        # Passive change of transverse reference, including a varying alpha.
        alpha, alphad = rng.normal(size=2)
        _, ee1, ee2, *_ = geometry(x[:3], radius, pitch, x[3])
        e1p = np.cos(alpha)*ee1+np.sin(alpha)*ee2
        e2p = -np.sin(alpha)*ee1+np.cos(alpha)*ee2
        chip = rr/pitch+x[3]-alpha
        assert np.linalg.norm(np.cos(chip)*e1p+np.sin(chip)*e2p-uu) < 1e-13
        assert abs((chiv-alphad)+(np.cos(theta)*lv+alphad)-nu) < 1e-13
    assert max_fd < 2e-7
    assert max_frame < 1e-11

    # Frenet triad along a native member, using a fixed Cartesian axis.
    q, radius, phi = sp.symbols("q radius phi", positive=True)
    nn = sp.Matrix([0, 0, 1])
    uu = sp.Matrix([sp.cos(phi), sp.sin(phi), 0])
    ww = nn.cross(uu)
    T = (q*nn+ww)/sp.sqrt(1+q*q)
    N = -uu
    B = (nn-q*ww)/sp.sqrt(1+q*q)
    arc_per_phi = radius*sp.sqrt(1+q*q)
    curvature = 1/(radius*(1+q*q))
    torsion = q/(radius*(1+q*q))
    for expr in [T.cross(N)-B, T.diff(phi)/arc_per_phi-curvature*N,
                 N.diff(phi)/arc_per_phi+curvature*T-torsion*B,
                 B.diff(phi)/arc_per_phi+torsion*N]:
        for val in expr:
            zero(val)
    zero(B.dot(N.diff(phi))/arc_per_phi-torsion)
    return {"symbolic_phase_and_coframe": "PASS", "rank_and_distinct_kernels": "PASS",
            "reference_invariance": "PASS", "frenet_bridge": "PASS", "trajectory_count": 60,
            "max_acceleration_finite_difference_error": max_fd,
            "max_moving_frame_vs_cartesian_error": max_frame}


def graph_checks():
    phases = np.array([0.2, -0.8, 1.3, 0.6])
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
    links = np.array([phases[i]-phases[j] for i, j in edges])
    wrap = lambda x: np.angle(np.exp(1j*x))
    assert np.max(np.abs([wrap(phases[j]-phases[i]+v) for (i,j),v in zip(edges,links)])) < 1e-14
    assert abs(wrap(sum(links[:4]))) < 1e-14
    assert abs(wrap(links[0]+links[1]-links[4])) < 1e-14
    changed = links.copy()
    changed[4] += 0.37
    assert abs(wrap(changed[0]+changed[1]-changed[4])) > 0.36
    alpha = np.array([0.4, 0.9, -0.7, 0.3])
    pprime = phases-alpha
    aprime = links+np.array([alpha[j]-alpha[i] for i,j in edges])
    assert np.max(np.abs([wrap(pprime[j]-pprime[i]+v) for (i,j),v in zip(edges,aprime)])) < 1e-14
    return "PASS: compatible cycles, frustrated cycle, and local-reference invariance"


if __name__ == "__main__":
    report = {"version": "2", "symbolic": symbolic_checks(), "numerical": numerical_checks(),
              "independent_phase": phase_checks(), "graph": graph_checks()}
    figures()
    checks = ROOT / "checks"
    checks.mkdir(parents=True, exist_ok=True)
    (checks / "verification_v2.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
