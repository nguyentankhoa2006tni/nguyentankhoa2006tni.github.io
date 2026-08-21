"""
==========================================================================
 MÔ PHỎNG MẠCH KHUẾCH ĐẠI BJT KIỂU E CHUNG (Common Emitter Amplifier)
 Transistor: C1815 (NPN) — Phân cực cầu phân áp
==========================================================================
 Chạy: python ce_amplifier_simulation.py
 Yêu cầu: numpy, matplotlib
==========================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# 1. THÔNG SỐ MẠCH
# ============================================================

# Nguồn cung cấp
Vcc = 12.0       # V

# Phân cực cầu phân áp
R1  = 10e3       # Ω  (Vcc → Base)
R2  = 1e3        # Ω  (Base → GND)

# Collector
RC  = 4.7e3      # Ω  (Vcc → Collector)

# Emitter (nối tiếp)
RE1 = 470.0      # Ω  (bypassed bởi CE)
RE2 = 10.0       # Ω  (không bypass)
RE  = RE1 + RE2  # Tổng RE cho DC

# Tụ điện
Ci  = 1e-6       # F  (Input coupling)
Co  = 0.22e-6    # F  (Output coupling)
CE  = 100e-6     # F  (Emitter bypass)

# Nguồn tín hiệu
Rs  = 1e3        # Ω  (Source resistance)
Vs_peak = 0.15   # V  (0.3Vpp → 0.15V peak)
f_sig   = 1e3    # Hz (1 kHz)

# Transistor C1815
beta = 150.0     # hFE
VBE  = 0.7       # V
VT   = 26e-3     # V  (Thermal voltage @ 25°C)
VA   = 100.0     # V  (Early voltage)
fT   = 80e6      # Hz (Transition frequency)
Cmu  = 2e-12     # F  (Collector-Base capacitance, Cob)

# ============================================================
# 2. PHÂN TÍCH DC — ĐIỂM LÀM VIỆC TĨNH (Q-Point)
# ============================================================

print("=" * 60)
print("  PHÂN TÍCH DC — ĐIỂM LÀM VIỆC TĨNH (Q-Point)")
print("=" * 60)

Vth  = Vcc * R2 / (R1 + R2)
Rth  = R1 * R2 / (R1 + R2)

IB = (Vth - VBE) / (Rth + (beta + 1) * RE)
IC = beta * IB
IE = (beta + 1) * IB

VE  = IE * RE
VC  = Vcc - IC * RC
VCE = VC - VE

re = VT / IC
gm = IC / VT

print(f"  Vth       = {Vth:.3f} V")
print(f"  Rth       = {Rth:.1f} Ohm")
print(f"  IB        = {IB*1e6:.2f} uA")
print(f"  IC        = {IC*1e3:.3f} mA")
print(f"  IE        = {IE*1e3:.3f} mA")
print(f"  VB        = {Vth:.3f} V")
print(f"  VE        = {VE:.3f} V")
print(f"  VC        = {VC:.3f} V")
print(f"  VCE       = {VCE:.3f} V  {'Active' if VCE > 0.3 else 'Saturated!'}")
print(f"  re        = {re:.2f} Ohm")
print(f"  gm        = {gm*1e3:.2f} mS")

# ============================================================
# 3. PHÂN TÍCH AC — CÓ TỤ CE
# ============================================================

print("\n" + "=" * 60)
print("  PHÂN TÍCH AC — CÓ TỤ CE (Mid-band)")
print("=" * 60)

RE_ac_ce = RE2
Ze_ac_ce = re + RE_ac_ce

Av_ce       = -RC / Ze_ac_ce
Zi_base_ce  = beta * Ze_ac_ce
Zi_ce       = 1 / (1/R1 + 1/R2 + 1/Zi_base_ce)
Zo_ce       = RC
Ai_ce       = Zi_ce / Ze_ac_ce

print(f"  RE_ac     = {RE_ac_ce:.1f} Ohm")
print(f"  Av        = {Av_ce:.1f}  (|Av| = {abs(Av_ce):.1f})")
print(f"  Zi_base   = {Zi_base_ce:.0f} Ohm")
print(f"  Zi        = {Zi_ce:.1f} Ohm")
print(f"  Zo        = {Zo_ce:.0f} Ohm")
print(f"  Ai        = {Ai_ce:.1f}")

# ============================================================
# 4. PHÂN TÍCH AC — KHÔNG CÓ TỤ CE
# ============================================================

print("\n" + "=" * 60)
print("  PHÂN TÍCH AC — KHÔNG CÓ TỤ CE (Mid-band)")
print("=" * 60)

RE_ac_noce = RE
Ze_ac_noce = re + RE_ac_noce

Av_noce       = -RC / Ze_ac_noce
Zi_base_noce  = beta * Ze_ac_noce
Zi_noce       = 1 / (1/R1 + 1/R2 + 1/Zi_base_noce)
Zo_noce       = RC
Ai_noce       = Zi_noce / Ze_ac_noce

print(f"  RE_ac     = {RE_ac_noce:.1f} Ohm")
print(f"  Av        = {Av_noce:.2f}  (|Av| = {abs(Av_noce):.2f})")
print(f"  Zi_base   = {Zi_base_noce:.0f} Ohm")
print(f"  Zi        = {Zi_noce:.1f} Ohm")
print(f"  Zo        = {Zo_noce:.0f} Ohm")
print(f"  Ai        = {Ai_noce:.2f}")

# ============================================================
# 5. ĐÁP ỨNG TẦN SỐ
# ============================================================

print("\n" + "=" * 60)
print("  DAP UNG TAN SO")
print("=" * 60)

# fL components
fL_Ci = 1 / (2 * np.pi * Ci * (Rs + Zi_ce))

R_base_th = 1 / (1/R1 + 1/R2 + 1/Rs)
R_CE_thevenin = 1 / (1/RE1 + 1/(re + RE2 + R_base_th/(beta+1)))
fL_CE = 1 / (2 * np.pi * CE * R_CE_thevenin)

R_load_scope = 1e6
fL_Co = 1 / (2 * np.pi * Co * (Zo_ce + R_load_scope))

fL = np.sqrt(fL_Ci**2 + fL_CE**2 + fL_Co**2)

print(f"  fL,Ci     = {fL_Ci:.1f} Hz")
print(f"  fL,CE     = {fL_CE:.1f} Hz")
print(f"  fL,Co     = {fL_Co:.1f} Hz (no load)")
print(f"  fL (total)= {fL:.1f} Hz")

# fH components
Cpi = gm / (2 * np.pi * fT) - Cmu
Av_miller = abs(Av_ce)
CM  = Cmu * (1 + Av_miller)
Cin = Cpi + CM

fH = 1 / (2 * np.pi * Cin * R_base_th)

print(f"\n  Cpi       = {Cpi*1e12:.1f} pF")
print(f"  C_Miller  = {CM*1e12:.1f} pF")
print(f"  Cin       = {Cin*1e12:.1f} pF")
print(f"  fH        = {fH/1e6:.2f} MHz")

# fH without CE
CM_noce  = Cmu * (1 + abs(Av_noce))
Cin_noce = Cpi + CM_noce
fH_noce  = 1 / (2 * np.pi * Cin_noce * R_base_th)
fL_noce  = 1 / (2 * np.pi * Ci * (Rs + Zi_noce))

print(f"\n  --- Khong co CE ---")
print(f"  C_Miller  = {CM_noce*1e12:.1f} pF")
print(f"  fH        = {fH_noce/1e6:.2f} MHz")
print(f"  fL        = {fL_noce:.1f} Hz")

# ============================================================
# 6. VẼ ĐỒ THỊ
# ============================================================

plt.rcParams.update({
    'figure.facecolor': '#1a1a2e',
    'axes.facecolor':   '#16213e',
    'axes.edgecolor':   '#e0e0e0',
    'axes.labelcolor':  '#e0e0e0',
    'text.color':       '#e0e0e0',
    'xtick.color':      '#e0e0e0',
    'ytick.color':      '#e0e0e0',
    'grid.color':       '#333366',
    'grid.alpha':       0.5,
    'font.size':        11,
    'figure.dpi':       120,
})

output_dir = os.path.dirname(os.path.abspath(__file__))

# ===========================================================
# FIGURE 1: TRANSIENT RESPONSE
# ===========================================================

fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
fig1.suptitle('MACH KHUECH DAI E CHUNG - C1815\nDap ung Transient (f = 1 kHz)',
              fontsize=14, fontweight='bold', color='#00d4ff')

t = np.linspace(0, 4e-3, 10000)
w_sig = 2 * np.pi * f_sig

Vi_peak = Vs_peak * Zi_ce / (Rs + Zi_ce)
Vi_t = Vi_peak * np.sin(w_sig * t)

Vo_peak = abs(Av_ce) * Vi_peak
Vo_max_pos = Vcc - VC
Vo_max_neg = VC - (VE + 0.2)
Vo_peak_limited = min(Vo_peak, Vo_max_pos, Vo_max_neg)

if Vo_peak > min(Vo_max_pos, Vo_max_neg):
    print(f"\n  WARNING: Vo_peak ({Vo_peak:.2f}V) > max swing ({min(Vo_max_pos, Vo_max_neg):.2f}V)")
    Vo_t = np.clip(-abs(Av_ce) * Vi_t, -Vo_max_neg, Vo_max_pos)
else:
    Vo_t = -abs(Av_ce) * Vi_t

ax1.plot(t * 1e3, Vi_t * 1e3, color='#00ff88', linewidth=1.8,
         label=f'Vi (peak = {Vi_peak*1e3:.1f} mV)')
ax1.axhline(y=0, color='#555588', linewidth=0.5, linestyle='--')
ax1.set_ylabel('Vi (mV)', fontsize=12)
ax1.legend(loc='upper right', facecolor='#1a1a2e', edgecolor='#555588')
ax1.grid(True, alpha=0.3)
ax1.set_title('Tin hieu vao Vi', fontsize=11, color='#00ff88')

ax2.plot(t * 1e3, Vo_t, color='#ff6b6b', linewidth=1.8,
         label=f'Vo (peak = {Vo_peak_limited:.2f} V)')
ax2.axhline(y=0, color='#555588', linewidth=0.5, linestyle='--')
ax2.set_xlabel('Time (ms)', fontsize=12)
ax2.set_ylabel('Vo (V)', fontsize=12)
ax2.legend(loc='upper right', facecolor='#1a1a2e', edgecolor='#555588')
ax2.grid(True, alpha=0.3)
ax2.set_title('Tin hieu ra Vo (dao pha 180 do)', fontsize=11, color='#ff6b6b')

plt.tight_layout()
fig1_path = os.path.join(output_dir, 'transient_response.png')
plt.savefig(fig1_path, bbox_inches='tight', facecolor=fig1.get_facecolor())
print(f"\n  [SAVED] {fig1_path}")

# ===========================================================
# FIGURE 2: BODE PLOT
# ===========================================================

fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(12, 9))
fig2.suptitle('MACH KHUECH DAI E CHUNG - C1815\nDap tuyen Bode (Bien do & Pha)',
              fontsize=14, fontweight='bold', color='#00d4ff')

f_range = np.logspace(0, 7, 2000)
w_range = 2 * np.pi * f_range

# --- Có CE ---
ZE1_f = RE1 / (1 + 1j * w_range * CE * RE1)
Ze_total_ce = re + RE2 + ZE1_f
Av_f_ce = -RC / Ze_total_ce

H_HF_ce = 1 / (1 + 1j * w_range / (2 * np.pi * fH))
Av_total_ce = Av_f_ce * H_HF_ce
Av_plot_ce = np.abs(Av_total_ce)
Av_dB_ce = 20 * np.log10(Av_plot_ce + 1e-20)
Phase_ce = np.angle(Av_total_ce, deg=True)

# --- Không có CE ---
Av_f_noce = -RC / Ze_ac_noce * np.ones_like(w_range)
H_HF_noce = 1 / (1 + 1j * w_range / (2 * np.pi * fH_noce))
Av_total_noce = Av_f_noce * H_HF_noce
Av_plot_noce = np.abs(Av_total_noce)
Av_dB_noce = 20 * np.log10(Av_plot_noce + 1e-20)
Phase_noce = np.angle(Av_total_noce, deg=True)

# === Magnitude Plot ===
ax3.semilogx(f_range, Av_dB_ce, color='#00d4ff', linewidth=2,
             label=f'Co CE (|Av|_mid = {abs(Av_ce):.0f})')
ax3.semilogx(f_range, Av_dB_noce, color='#ff9f43', linewidth=2, linestyle='--',
             label=f'Khong co CE (|Av|_mid = {abs(Av_noce):.1f})')

Av_mid_dB_ce = 20 * np.log10(abs(Av_ce))
Av_mid_dB_noce = 20 * np.log10(abs(Av_noce))
ax3.axhline(y=Av_mid_dB_ce - 3, color='#00d4ff', linewidth=0.8, linestyle=':', alpha=0.6,
            label=f'-3dB (co CE): {Av_mid_dB_ce-3:.1f} dB')
ax3.axhline(y=Av_mid_dB_noce - 3, color='#ff9f43', linewidth=0.8, linestyle=':', alpha=0.6,
            label=f'-3dB (khong CE): {Av_mid_dB_noce-3:.1f} dB')

ax3.axvline(x=fL, color='#00ff88', linewidth=0.8, linestyle='-.', alpha=0.7)
ax3.text(fL * 1.2, Av_mid_dB_ce - 8, f'fL~{fL:.0f}Hz', color='#00ff88', fontsize=9)

ax3.axvline(x=fH, color='#ff6b6b', linewidth=0.8, linestyle='-.', alpha=0.7)
ax3.text(fH * 0.3, Av_mid_dB_ce - 8, f'fH~{fH/1e6:.2f}MHz', color='#ff6b6b', fontsize=9)

ax3.set_ylabel('|Av| (dB)', fontsize=12)
ax3.set_title('Dap tuyen Bien do (Magnitude Response)', fontsize=11)
ax3.legend(loc='lower left', facecolor='#1a1a2e', edgecolor='#555588', fontsize=9)
ax3.grid(True, which='both', alpha=0.3)
ax3.set_xlim(1, 1e7)
ax3.set_ylim(-5, 50)

# === Phase Plot ===
ax4.semilogx(f_range, Phase_ce, color='#00d4ff', linewidth=2, label='Co CE')
ax4.semilogx(f_range, Phase_noce, color='#ff9f43', linewidth=2, linestyle='--', label='Khong co CE')
ax4.axhline(y=-180, color='#555588', linewidth=0.8, linestyle=':')
ax4.set_xlabel('Tan so (Hz)', fontsize=12)
ax4.set_ylabel('Pha (degree)', fontsize=12)
ax4.set_title('Dap tuyen Pha (Phase Response)', fontsize=11)
ax4.legend(loc='upper right', facecolor='#1a1a2e', edgecolor='#555588', fontsize=9)
ax4.grid(True, which='both', alpha=0.3)
ax4.set_xlim(1, 1e7)

plt.tight_layout()
fig2_path = os.path.join(output_dir, 'bode_plot.png')
plt.savefig(fig2_path, bbox_inches='tight', facecolor=fig2.get_facecolor())
print(f"  [SAVED] {fig2_path}")

# ===========================================================
# FIGURE 3: SO SÁNH CÓ/KHÔNG CE
# ===========================================================

fig3, axes = plt.subplots(1, 2, figsize=(14, 5))
fig3.suptitle('SO SANH CO/KHONG TU CE - Transient @ 1 kHz',
              fontsize=14, fontweight='bold', color='#00d4ff')

t_short = np.linspace(0, 2e-3, 5000)

for idx, (ax, title, av, color) in enumerate([
    (axes[0], 'CO TU CE', Av_ce, '#00d4ff'),
    (axes[1], 'KHONG CO TU CE', Av_noce, '#ff9f43'),
]):
    vi_t = Vi_peak * np.sin(w_sig * t_short)
    vo_ac = -abs(av) * Vi_peak * np.sin(w_sig * t_short)

    ax.plot(t_short * 1e3, vi_t * 1e3, color='#00ff88', linewidth=1.5, label='Vi')
    ax_right = ax.twinx()
    ax_right.plot(t_short * 1e3, vo_ac, color=color, linewidth=1.5, label='Vo')

    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Vi (mV)', color='#00ff88')
    ax_right.set_ylabel('Vo (V)', color=color)
    ax.set_title(f'{title}\n|Av| = {abs(av):.1f}', fontsize=11, color=color)
    ax.grid(True, alpha=0.3)
    ax_right.tick_params(axis='y', labelcolor=color)
    ax.tick_params(axis='y', labelcolor='#00ff88')

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax_right.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right',
              facecolor='#1a1a2e', edgecolor='#555588', fontsize=9)

plt.tight_layout()
fig3_path = os.path.join(output_dir, 'comparison_ce.png')
plt.savefig(fig3_path, bbox_inches='tight', facecolor=fig3.get_facecolor())
print(f"  [SAVED] {fig3_path}")

# ===========================================================
# BẢNG TẦN SỐ
# ===========================================================

print("\n" + "=" * 60)
print("  BANG BIEN DO - TAN SO (Co CE, khong tai)")
print("=" * 60)
print(f"  {'f(Hz)':>8} | {'|Av|':>8} | {'Av(dB)':>8} | {'Vo (mVpp)':>10}")
print("  " + "-" * 45)

test_freqs = [10, 50, 200, 500, 1000, 10000, 50000, 100000, 500000, 1000000]
for f_test in test_freqs:
    w_test = 2 * np.pi * f_test
    ZE1 = RE1 / (1 + 1j * w_test * CE * RE1)
    Ze_test = re + RE2 + ZE1
    Av_test = -RC / Ze_test
    H_hf = 1 / (1 + 1j * w_test / (2 * np.pi * fH))
    Av_combined = Av_test * H_hf
    Av_mag = abs(Av_combined)
    Av_db = 20 * np.log10(Av_mag + 1e-20)
    Vo_pp = 2 * Av_mag * Vi_peak * 1e3
    freq_str = f"{f_test/1e3:.0f}K" if f_test >= 1000 else f"{f_test}"
    print(f"  {freq_str:>8} | {Av_mag:>8.1f} | {Av_db:>8.1f} | {Vo_pp:>10.1f}")

# ===========================================================
# BẢNG SO SÁNH
# ===========================================================

print("\n" + "=" * 60)
print("  BANG SO SANH: CO CE vs KHONG CO CE")
print("=" * 60)
print(f"  {'Thong so':>12} | {'Co CE':>12} | {'Khong CE':>12} | {'Thay doi':>15}")
print("  " + "-" * 60)
print(f"  {'Av':>12} | {Av_ce:>12.1f} | {Av_noce:>12.2f} | Giam {abs(Av_ce/Av_noce):.1f}x")
print(f"  {'|Av|':>12} | {abs(Av_ce):>12.1f} | {abs(Av_noce):>12.2f} | Giam {abs(Av_ce/Av_noce):.1f}x")
print(f"  {'Ai':>12} | {Ai_ce:>12.1f} | {Ai_noce:>12.2f} | Giam {Ai_ce/Ai_noce:.1f}x")
print(f"  {'Zi (Ohm)':>12} | {Zi_ce:>12.0f} | {Zi_noce:>12.0f} | Tang {(Zi_noce-Zi_ce)/Zi_ce*100:.1f}%")
print(f"  {'Zo (Ohm)':>12} | {Zo_ce:>12.0f} | {Zo_noce:>12.0f} | Khong doi")
print(f"  {'fL (Hz)':>12} | {fL:>12.0f} | {fL_noce:>12.0f} | Giam {(fL-fL_noce)/fL*100:.1f}%")
print(f"  {'fH (MHz)':>12} | {fH/1e6:>12.2f} | {fH_noce/1e6:>12.2f} | Tang {fH_noce/fH:.1f}x")
print(f"  {'BW (MHz)':>12} | {fH/1e6:>12.2f} | {fH_noce/1e6:>12.2f} | Tang {fH_noce/fH:.1f}x")
print(f"  {'Pha (do)':>12} | {'180':>12} | {'180':>12} | Khong doi")

print("\n" + "=" * 60)
print("  MO PHONG HOAN TAT!")
print("=" * 60)

plt.show()
