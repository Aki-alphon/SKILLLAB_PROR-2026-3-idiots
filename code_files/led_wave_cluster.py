# led_wave_cluster.py
# ============================================================
# Project: Project Project (SkillLab 2 — Embedded Systems)
# File:    led_wave_cluster.py
# Effect:  SINE WAVE — smooth brightness wave ripples across
#          3 rows of LEDs. Each row has 6 parallel LEDs + one
#          100µF capacitor that acts as a hardware low-pass
#          filter, turning the PWM signal into a smooth analog
#          voltage. The result is an ultra-fluid glowing wave.
# Author:  Team Project^2 (Mrugendra Vasmatkar, Jyoti Bagate)
# Date:    April 2026
# ============================================================
#
# ─── HARDWARE STRUCTURE ─────────────────────────────────────
#
#  GPIO 17 (Pin 11) ─┬─[1kΩ]─ LED1─LED2─LED3─LED4─LED5─LED6 (all parallel, anodes)
#  ROW 1             └─[100µF (+)] ─── [100µF (−)] ─── GND
#                       └── All 6 LED cathodes ─── GND
#
#  GPIO 18 (Pin 12) ─┬─[1kΩ]─ LED7─LED8─LED9─LED10─LED11─LED12 (all parallel)
#  ROW 2             └─[100µF (+)] ─── [100µF (−)] ─── GND
#                       └── All 6 LED cathodes ─── GND
#
#  GPIO 27 (Pin 13) ─┬─[1kΩ]─ LED13─LED14─LED15─LED16─LED17─LED18 (all parallel)
#  ROW 3             └─[100µF (+)] ─── [100µF (−)] ─── GND
#                       └── All 6 LED cathodes ─── GND
#
#  Pi Pin 6 (GND) ─────── All GND rails connected together
#
# ─── COMPONENT COUNT ────────────────────────────────────────
#  GPIO pins  : 3   (GPIO 17, 18, 27)
#  LEDs       : 18  (6 per row × 3 rows, wired in parallel)
#  Resistors  : 18  (1kΩ each, one per LED)
#  Capacitors : 3   (100µF each, one per row as LPF)
#
# ─── HOW THE LPF CAPACITOR WORKS ───────────────────────────
#  PWM is a rapidly switching digital signal (0V ↔ 3.3V).
#  The 100µF capacitor across the signal node charges and
#  discharges slowly, averaging the switching into a smooth
#  continuous voltage. This means:
#    PWM 0%  duty → ~0V   at cap → all 6 row LEDs fully OFF
#    PWM 50% duty → ~1.65V at cap → all 6 row LEDs at HALF
#    PWM 100%duty → ~3.3V at cap → all 6 row LEDs FULL ON
#  The transitions between these states are smooth curves,
#  not digital steps — giving a silky wave effect.
#
# ─── CURRENT CALCULATION (safety check) ────────────────────
#  With 1kΩ per LED and Vf ≈ 2V:
#    I per LED = (3.3 − 2.0) / 1000 = 1.3 mA
#    I per row = 6 × 1.3 mA = 7.8 mA
#    Total (all 3 rows full) = 3 × 7.8 = 23.4 mA
#  Pi 3B GPIO bank limit = 50 mA → SAFE ✓
#  Pi 3B per-pin limit   = 16 mA → SAFE ✓ (7.8 mA < 16 mA)
#
# ─── WAVE PARAMETERS (edit to adjust feel) ──────────────────
#  WAVE_SPEED  : how fast the wave travels (Hz)
#  WAVE_SPREAD : phase difference between rows (higher = 
#                wider spatial gap between wave peaks)
#  UPDATE_RATE : frame period in seconds (0.03 ≈ 33 fps)
#  MIN_BRIGHT  : minimum row brightness (0.0 = fully off)
#  MAX_BRIGHT  : maximum row brightness (1.0 = full glow)
#
# ─── USAGE ──────────────────────────────────────────────────
#  python3 led_wave_cluster.py
#  Press Ctrl+C to stop
# ============================================================

from gpiozero import PWMLED
import time
import math

# ── GPIO → Row mapping ───────────────────────────────────────
# 3 GPIO pins, one per row of 6 LEDs
ROW_GPIO    = [17, 18, 27]       # Row 0 (top), Row 1 (mid), Row 2 (bottom)
NUM_ROWS    = len(ROW_GPIO)

# ── Wave parameters ──────────────────────────────────────────
WAVE_SPEED  = 1.0      # Hz — wave travel speed (cycles per second)
WAVE_SPREAD = 1.0      # spatial phase per row (1.0 = one full wave across 3 rows)
UPDATE_RATE = 0.03     # seconds per frame (~33 fps)
MIN_BRIGHT  = 0.0      # row minimum brightness
MAX_BRIGHT  = 1.0      # row maximum brightness

# ── Initialise rows ──────────────────────────────────────────
rows = [PWMLED(pin) for pin in ROW_GPIO]

def wave_brightness(row_index, t):
    """
    Brightness for a given row at time t.
    Computes a sine wave value spatially offset per row.
    Returns value clamped between MIN_BRIGHT and MAX_BRIGHT.
    """
    # Each row is phase-shifted by WAVE_SPREAD × (2π / NUM_ROWS)
    phase = (2 * math.pi * WAVE_SPREAD * row_index) / NUM_ROWS
    raw   = math.sin(2 * math.pi * WAVE_SPEED * t - phase)
    return MIN_BRIGHT + (MAX_BRIGHT - MIN_BRIGHT) * (0.5 + 0.5 * raw)

def clear_all():
    for row in rows:
        row.value = 0.0

# ── Main ─────────────────────────────────────────────────────
print("=" * 58)
print("  Project Project — 3-ROW SINE WAVE CLUSTER")
print("  18 LEDs | 3 rows × 6 LEDs | 3×100µF LPF per row")
print(f"  Speed: {WAVE_SPEED} Hz | Spread: {WAVE_SPREAD} | {1/UPDATE_RATE:.0f} fps")
print("  The capacitor per row smooths PWM → clean analog wave.")
print("  Press Ctrl+C to stop.")
print("=" * 58)

try:
    start_time = time.time()

    while True:
        t = time.time() - start_time

        for i, row in enumerate(rows):
            row.value = wave_brightness(i, t)

        time.sleep(UPDATE_RATE)

except KeyboardInterrupt:
    print("\nStopping wave...")
finally:
    clear_all()
    for row in rows:
        row.close()
    print("GPIO cleaned up. Bye!")
