# led_pulse.py
# ============================================================
# Project: Project Project (SkillLab 2 — Embedded Systems)
# File:    led_pulse.py
# Purpose: Single Red LED smooth breathing effect using PWM
#          on Raspberry Pi 3B GPIO 18 via gpiozero library
# Author:  Team Project^2 (Mrugendra Vasmatkar, Jyoti Bagate)
# Date:    April 2026
# ============================================================
#
# HARDWARE SETUP (wire BEFORE running):
# -----------------------------------------------
#  Raspberry Pi 3B
#  Pin 12 (GPIO 18) ──── R1 (1kΩ) ──── SHARED NODE ──── LED Anode (+, long leg)
#                                           │                   │
#                                      C1 (+) 100µF        LED Cathode (-, short leg)
#                                      C1 (-) 100µF             │
#                                           └───────────────────┘
#                                                     │
#  Pin 14 (GND)     ──────────────────────────────────┘
#
# NOTE: 100µF capacitor is POLARISED (electrolytic).
#       Always connect + leg to signal node, - leg to GND.
#       Do NOT reverse polarity.
#
# WHY a capacitor?
#   GPIO PWM is a digital signal switching 0V ↔ 3.3V rapidly.
#   The 100µF cap averages this into a smooth analog voltage,
#   eliminating any visible flicker for a cinematic glow effect.
#
# WHY 1kΩ and NOT 100kΩ?
#   At 100kΩ the current would be ~0.013 mA — LED is invisible.
#   At 1kΩ the current is ~1.3 mA — LED glows visibly and safely.
# -----------------------------------------------
#
# REQUIREMENTS:
#   - Raspberry Pi OS (gpiozero pre-installed)
#   - Python 3
#
# USAGE:
#   python3 led_pulse.py
#   Press Ctrl+C to stop.
# ============================================================

from gpiozero import PWMLED
from signal import pause

# ── Initialise ──────────────────────────────────────────────
# PWMLED configures GPIO 18 as a software PWM output.
# gpiozero handles all pin setup automatically.
led = PWMLED(18)

# ── Start pulsing ────────────────────────────────────────────
# pulse() runs in a background daemon thread — no manual loop needed.
#   fade_in_time  : seconds to go from 0% → 100% brightness
#   fade_out_time : seconds to go from 100% → 0% brightness
#   n             : number of pulses (default None = loop forever)
led.pulse(fade_in_time=1.5, fade_out_time=1.5)

print("=" * 50)
print("  Project Project — LED Breathing Active")
print("  GPIO 18 | fade_in: 1.5s | fade_out: 1.5s")
print("  100µF capacitor smoothing PWM signal")
print("  Press Ctrl+C to stop.")
print("=" * 50)

# ── Keep alive ───────────────────────────────────────────────
# signal.pause() blocks the main thread without consuming CPU.
# The LED continues pulsing in gpiozero's background thread.
pause()
