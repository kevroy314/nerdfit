"""
GPU sweep kernel v2 -- one CUDA thread per simulation.
Each thread runs the full Euler integration loop independently (scalar ops).
Metrics accumulated sequentially to match CPU heatmap_sweep.py exactly.
"""

import os, sys, json, time

# Only set up CUDA paths if running on Windows
if sys.platform == 'win32':
    lib_bin = r'C:\Users\kevin\anaconda3\envs\nerdfit\Library\bin'
    os.environ['PATH'] = lib_bin + ';' + os.environ.get('PATH', '')
    os.environ['CUDA_PATH'] = r'C:\Users\kevin\anaconda3\envs\nerdfit\Library'
    os.add_dll_directory(lib_bin)

import numpy as np
import cupy as cp

T_END = 365
DT = 0.5
N_STEPS = int(T_END / DT)

_kernel_code = r'''
extern "C" __global__
void simulate(
    const double* H0, const double* M0, const double* E0,
    const double* I0, const double* C0,
    double* out_success, double* out_cog, double* out_act,
    double* out_path, double* out_settle, double* out_t2h,
    int N, int n_steps, double dt, int q3_start
) {
    int idx = blockDim.x * blockIdx.x + threadIdx.x;
    if (idx >= N) return;

    const double A_base=0.8, alpha_H=0.045, delta_H=0.01, H_min=0.02;
    const double beta_M=0.15, lambda_=0.2, gamma_=0.25, gamma_ind=0.1;
    const double f_0=0.3, phi_M=0.08, psi=0.15, epsilon_=0.03;
    const double phi_ind=0.05, kappa=0.3, E_crit=-1.5;
    const double kappa_wth=0.8, E_wth=1.5, tau=0.15, mu=0.1;
    const double alpha_I=0.005, delta_I=0.001;
    const double C_min=0.1, C_max=0.95;
    const double alpha_C_down=0.003, alpha_C_up=0.001;

    double H = H0[idx], M = M0[idx], E = E0[idx], I = I0[idx], C = C0[idx];
    double dE_prev = 0.0;
    double H_prev = H, M_prev = M, E_prev = E, I_prev = I, C_prev = C;

    double cum_cog = 0.0, cum_act = 0.0, cum_path = 0.0;
    double settle_acc = 0.0;
    int settle_n = 0;
    double t2h = (double)n_steps * dt;
    bool reached = false;
    if (H > 0.5) { t2h = 0.0; reached = true; }

    for (int step = 0; step < n_steps; step++) {
        double theta = C * (1.0 - H);
        double x1 = (M - theta) / tau;
        if (x1 < -500.0) x1 = -500.0; if (x1 > 500.0) x1 = 500.0;
        double B_goal = 1.0 / (1.0 + exp(-x1));

        double M_hf = 0.15 * (1.0 - H * 0.5);
        double x2 = (M - M_hf) / 0.08;
        if (x2 < -500.0) x2 = -500.0; if (x2 > 500.0) x2 = 500.0;
        double B_hab = H * (1.0 / (1.0 + exp(-x2)));

        double bl = H * sqrt(H);
        double B_raw = (1.0 - bl) * B_goal + bl * B_hab;

        double x3 = (M - 0.08) / 0.03;
        if (x3 < -500.0) x3 = -500.0; if (x3 > 500.0) x3 = 500.0;
        double act = 1.0 / (1.0 + exp(-x3));

        double B = B_raw * act;
        if (B < 0.0) B = 0.0; if (B > 1.0) B = 1.0;

        double F = f_0 * M * (1.0 - B);
        double A_eff = A_base + (1.0 - A_base) * I;

        double dr = delta_H * (1.0 + 2.0 * (1.0 - B) * H);
        double dH = alpha_H * B * (A_eff - H) - dr * (1.0 - B) * (H - H_min);

        double dec = -beta_M * M / (1.0 + M);
        double nov = 1.0 - H * H; if (nov < 0.0) nov = 0.0;
        double mhr = 1.0 - M / 2.0; if (mhr < 0.0) mhr = 0.0;
        double rew = gamma_ * B * nov * mhr;
        double eff = -lambda_ * C * (1.0 - H) * B;
        double ind = -gamma_ind * F * (1.0 - H);

        double fh_x = -E - 1.5;
        if (fh_x < -500.0) fh_x = -500.0; if (fh_x > 500.0) fh_x = 500.0;
        double fh = -kappa * log1p(exp(fh_x)) * M;

        double wth_x = (E - E_wth) / 0.2;
        if (wth_x < -500.0) wth_x = -500.0; if (wth_x > 500.0) wth_x = 500.0;
        double wth = -kappa_wth * (1.0 / (1.0 + exp(-wth_x))) * M;

        double vel = mu * (-dE_prev);
        double idr_v = 0.2 * I - M; if (idr_v < 0.0) idr_v = 0.0;
        double idr = 0.08 * idr_v;
        double hm = 0.02 * B * H;

        double dM = dec + rew + eff + ind + fh + wth + vel + idr + hm;

        double dE = phi_M * M * (1.0 - H) - psi * B * H - epsilon_ * E
                   + phi_ind * F - 0.3 * B * (1.0 - H) * (E > 0.0 ? 1.0 : 0.0);

        double dI = alpha_I * B * H * (1.0 - I) - delta_I * (1.0 - B) * I;

        double Ceq = C_min + (C_max - C_min) * H * (0.7 + 0.3 * I);
        double ov1 = C - Ceq; if (ov1 < 0.0) ov1 = 0.0;
        double ov2 = 0.3 - B; if (ov2 < 0.0) ov2 = 0.0;
        double fp = -alpha_C_down * ov1 * ov2;

        double er_x = -E - 0.75;
        if (er_x < -500.0) er_x = -500.0; if (er_x > 500.0) er_x = 500.0;
        double er = -alpha_C_down * 0.3 * log1p(exp(er_x)) * ov2;

        double ur1 = Ceq - C; if (ur1 < 0.0) ur1 = 0.0;
        double sp = alpha_C_up * ur1 * B;

        double ic_h = H - 0.3; if (ic_h < 0.0) ic_h = 0.0;
        double ic_c = Ceq - C; if (ic_c < 0.0) ic_c = 0.0;
        double ic = alpha_C_up * 0.3 * I * ic_h * ic_c;

        double dC = fp + er + sp + ic;

        double c_boost = -dC; if (c_boost < 0.0) c_boost = 0.0;
        dM += c_boost * 0.3;

        double Hn = H + dH * dt;
        if (Hn < H_min) Hn = H_min; if (Hn > 1.0) Hn = 1.0;
        double Mn = M + dM * dt;
        if (Mn < 0.0) Mn = 0.0;
        double En = E + dE * dt;
        double In = I + dI * dt;
        if (In < 0.0) In = 0.0; if (In > 1.0) In = 1.0;
        double Cn = C + dC * dt;
        if (Cn < C_min) Cn = C_min; if (Cn > C_max) Cn = C_max;

        // Update state
        H_prev = H; M_prev = M; E_prev = E; I_prev = I; C_prev = C;
        H = Hn; M = Mn; E = En; I = In; C = Cn;
        dE_prev = dE;

        // Accumulate metrics using post-update state (sequential += to match CPU)
        cum_cog += C * (1.0 - H) * B * dt;
        cum_act += C * B * dt;

        double dph = H - H_prev, dpm = M - M_prev, dpe = E - E_prev;
        double dpi = I - I_prev, dpc = C - C_prev;
        cum_path += sqrt(dph*dph + dpm*dpm + dpe*dpe + dpi*dpi + dpc*dpc);

        if (!reached && H > 0.5) {
            t2h = (double)(step + 1) * dt;
            reached = true;
        }

        if (step >= q3_start) {
            settle_acc += (fabs(H-H_prev) + fabs(M-M_prev) + fabs(E-E_prev) + fabs(I-I_prev) + fabs(C-C_prev)) / dt;
            settle_n++;
        }
    }

    out_success[idx] = (H > 0.5) ? 1.0 : 0.0;
    out_cog[idx] = cum_cog;
    out_act[idx] = cum_act;
    out_path[idx] = cum_path;
    out_settle[idx] = (settle_n > 0) ? settle_acc / (double)settle_n : 0.0;
    out_t2h[idx] = t2h;
}
'''

_kernel = None

def _get_kernel():
    global _kernel
    if _kernel is None:
        _kernel = cp.RawKernel(_kernel_code, 'simulate', options=('--fmad=false',))
    return _kernel


def batch_simulate(H0, M0, E0, I0, C0):
    N = len(H0)
    q3 = 3 * (N_STEPS + 1) // 4  # Match CPU: 3 * len(output_array) // 4

    d_H0 = cp.array(H0, dtype=cp.float64)
    d_M0 = cp.array(M0, dtype=cp.float64)
    d_E0 = cp.array(E0, dtype=cp.float64)
    d_I0 = cp.array(I0, dtype=cp.float64)
    d_C0 = cp.array(C0, dtype=cp.float64)

    outs = [cp.zeros(N, dtype=cp.float64) for _ in range(6)]

    block = 256
    grid = (N + block - 1) // block
    _get_kernel()((grid,), (block,), (
        d_H0, d_M0, d_E0, d_I0, d_C0,
        *outs,
        np.int32(N), np.int32(N_STEPS), np.float64(DT), np.int32(q3)
    ))
    cp.cuda.Stream.null.synchronize()

    return {k: cp.asnumpy(v).tolist() for k, v in
            zip(["success", "cognitive_load", "net_activity",
                 "path_length", "settling", "time_to_habit"], outs)}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python gpu_kernel_v2.py input.json output.json", file=sys.stderr)
        sys.exit(1)

    t0 = time.time()
    with open(sys.argv[1]) as f:
        data = json.load(f)

    N = len(data["H0"])
    BATCH = 20000
    print(f"Running {N} simulations...", file=sys.stderr)

    all_results = {k: [] for k in ["success", "cognitive_load", "net_activity",
                                    "path_length", "settling", "time_to_habit"]}
    for start in range(0, N, BATCH):
        end = min(start + BATCH, N)
        print(f"  Batch {start}-{end}...", file=sys.stderr)
        r = batch_simulate(
            data["H0"][start:end], data["M0"][start:end], data["E0"][start:end],
            data["I0"][start:end], data["C0"][start:end])
        for k in all_results:
            all_results[k].extend(r[k])

    t1 = time.time()
    print(f"Done: {N} sims in {t1-t0:.1f}s ({N/(t1-t0):.0f} sims/s)", file=sys.stderr)

    with open(sys.argv[2], "w") as f:
        json.dump(all_results, f)
