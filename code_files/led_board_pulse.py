# led_board_pulse.py
# ============================================================
# Project: Project Project (SkillLab 2 — Embedded Systems)
# File:    led_board_pulse.py
# Purpose: ALL 3 ROWS BREATHING TOGETHER — All 18 LEDs across
#          all 3 rows pulse in perfect unison using gpiozero
#          LEDBoard. The 100µF LPF cap on each row smooths
#          the PWM so every row-band glows like a single lamp.
#
#          Use this AFTER led_pulse.py passes, to verify all
#          3 rows respond correctly before running motion effects.
#
# Author:  Team Project^2 (Mrugendra Vasmatkar, Jyoti Bagate)
# Date:    April 2026
# ============================================================
#
# ─── HARDWARE SETUP (3-Row Cluster — all rows active) ────────
#
#              1kΩ
#  GPIO 17 ──[===]──┬── LED1─LED2─LED3─LED4─LED5─LED6 (+) ── all cathodes ── GND
#  ROW 1            └── [100µF LPF (+)→(−)] → GND
#
#              1kΩ
#  GPIO 18 ──[===]──┬── LED7─LED8─LED9─LED10─LED11─LED12 (+) ── all cathodes ── GND
#  ROW 2            └── [100µF LPF (+)→(−)] → GND
#
#              1kΩ
#  GPIO 27 ──[===]──┬── LED13─LED14─LED15─LED16─LED17─LED18 (+) ── all cathodes ── GND
#  ROW 3            └── [100µF LPF (+)→(−)] → GND
#
#  Pi Pin 6 (GND) ─── All 3 GND rails joined
#
# ─── COMPONENT SUMMARY ───────────────────────────────────────
#  GPIO pins  : 3   (GPIO 17, 18, 27)
#  LEDs       : 18  (6 per row × 3 rows, parallel per row)
#  Resistors  : 18  (1kΩ each — one per LED, mandatory)
#  Capacitors : 3   (100µF each — one per row as LPF, polarised)
#
# ─── HOW LEDBoard WORKS ──────────────────────────────────────
#  LEDBoard(17, 18, 27, pwm=True) groups the 3 GPIO pins
#  into one object. Calling .pulse() triggers the same
#  PWM fade pattern on all 3 pins simultaneously.
#  Each GPIO drives its entire row of 6 LEDs as one unit.
#  The 100µF cap on each row smooths the PWM into a clean
#  analog voltage — all 18 LEDs breathe as a single lamp.
#
# ─── CURRENT SAFETY ──────────────────────────────────────────
#  1 shared 1kΩ resistor per row (6 parallel LEDs):
#  I per row = (3.3V − 2.0V) / 1kΩ = 1.3 mA per row
#  I per LED = 1.3 mA / 6 = ~0.22 mA  → soft atmospheric glow
#  All 3 rows = 3.9 mA total  (Pi GPIO bank limit: 50 mA ✓)
#
# ─── USAGE ───────────────────────────────────────────────────
#  python3 led_board_pulse.py
#  Press Ctrl+C to stop.
# ============================================================

from gpiozero import LEDBoard
from signal import pause

# ── Initialise all 3 rows via LEDBoard ───────────────────────
# pwm=True enables smooth PWM control on all 3 GPIO pins.
# Each GPIO controls 6 parallel LEDs + 1 LPF cap in its row.
rows = LEDBoard(17, 18, 27, pwm=True)

# ── Breathe all 3 rows together ──────────────────────────────
# pulse() runs in a gpiozero background daemon thread.
# All 3 rows fade in and out in perfect sync.
rows.pulse(fade_in_time=1.5, fade_out_time=1.5)

print("=" * 60)
print("  Project Project — ALL 3 ROWS BREATHING TOGETHER")
print("  GPIO 17 → Row 1 (LED 1–6)   + 100µF LPF")
print("  GPIO 18 → Row 2 (LED 7–12)  + 100µF LPF")
print("  GPIO 27 → Row 3 (LED 13–18) + 100µF LPF")
print("  18 LEDs total | fade_in: 1.5s | fade_out: 1.5s")
print("  All 3 row-bands should glow and fade as one unit.")
print("  Press Ctrl+C to stop.")
print("=" * 60)

# Keep the script alive while all rows pulse in background.
pause()
