# led_board_pulse.py
# ============================================================
# Project: Project Project (SkillLab 2 — Embedded Systems)
# File:    led_board_pulse.py
# Purpose: Multiple Red LEDs breathing in unison using
#          gpiozero PWMLEDBoard on Raspberry Pi 3B
# Author:  Team Project^2 (Mrugendra Vasmatkar, Jyoti Bagate)
# Date:    April 2026
# ============================================================
#
# HARDWARE SETUP — PER LED (repeat for each):
# -----------------------------------------------
#  GPIO pin ──── R (1kΩ) ──── LED Anode (+)
#                                    │
#                              LED Cathode (-)
#                                    │
#                                   GND
#
# GPIO PINS USED: 17, 18, 27
# Add a 1kΩ resistor for EACH LED.
# Add a 100µF cap in parallel with each LED for smoothing.
#
# IMPORTANT: Do NOT share a single GPIO pin across multiple LEDs.
#            Each pin can only safely source ~16 mA max.
#            One LED per pin, one resistor per LED.
# -----------------------------------------------
#
# USAGE:
#   python3 led_board_pulse.py
#   Press Ctrl+C to stop.
# ============================================================

from gpiozero import LEDBoard
from signal import pause

# ── Initialise LED Board ─────────────────────────────────────
# LEDBoard groups multiple GPIO pins as a single controllable unit.
# pwm=True enables smooth PWM fading on each LED independently.
# Add more GPIO pin numbers here to extend to more LEDs.
leds = LEDBoard(17, 18, 27, pwm=True)

# ── Start pulsing all LEDs simultaneously ───────────────────
# All LEDs in the board fade in and out together in perfect sync.
leds.pulse(fade_in_time=1.5, fade_out_time=1.5)

print("=" * 55)
print("  Project Project — Multi-LED Board Breathing Active")
print("  GPIO 17, 18, 27 | fade_in: 1.5s | fade_out: 1.5s")
print("  All 3 LEDs pulsing in unison.")
print("  Press Ctrl+C to stop.")
print("=" * 55)

# Keep the script alive while LEDs pulse in background thread.
pause()
