# led_wave.py
# ============================================================
# Project: Project Project (SkillLab 2 — Embedded Systems)
# File:    led_wave.py
# Purpose: Cascading wave pulse — each LED fades in 0.2 s
#          after the previous, creating a flowing light wave
#          across 6 LEDs on Raspberry Pi 3B
# Author:  Team Project^2 (Mrugendra Vasmatkar, Jyoti Bagate)
# Date:    April 2026
# ============================================================
#
# HARDWARE SETUP — PER LED (repeat for all 6):
# -----------------------------------------------
#  GPIO pin ──── R (1kΩ) ──── LED Anode (+)
#                                    │
#                              LED Cathode (-)
#                                    │
#                                   GND
#
# GPIO PINS USED: 17, 18, 27, 22, 23, 24  (6 LEDs total)
# Each LED needs its own 1kΩ resistor.
# Optional: 100µF cap in parallel with each LED for smoothing.
# -----------------------------------------------
#
# WAVE EFFECT:
#   LED1 starts fading at t=0.0s
#   LED2 starts fading at t=0.2s
#   LED3 starts fading at t=0.4s
#   LED4 starts fading at t=0.6s
#   LED5 starts fading at t=0.8s
#   LED6 starts fading at t=1.0s
#   → Creates a visible cascading "breathing wave" effect.
#
# USAGE:
#   python3 led_wave.py
#   Press Ctrl+C to stop.
# ============================================================

from gpiozero import PWMLED
from signal import pause
import threading
import time

# ── Configuration ────────────────────────────────────────────
GPIO_PINS   = [17, 18, 27, 22, 23, 24]  # One pin per LED
FADE_IN     = 1.5   # seconds to fade from 0% → 100%
FADE_OUT    = 1.5   # seconds to fade from 100% → 0%
WAVE_DELAY  = 0.2   # seconds between each LED starting its pulse

# ── Initialise all LEDs ──────────────────────────────────────
leds = [PWMLED(pin) for pin in GPIO_PINS]

# ── Wave start function ──────────────────────────────────────
def start_wave():
    """Starts each LED's pulse with a staggered delay to create
    a flowing wave effect across the full LED array."""
    for i, led in enumerate(leds):
        led.pulse(fade_in_time=FADE_IN, fade_out_time=FADE_OUT)
        print(f"  LED on GPIO {GPIO_PINS[i]} → pulse started")
        time.sleep(WAVE_DELAY)

# ── Launch wave in background thread ─────────────────────────
# daemon=True ensures the thread exits cleanly when main script stops.
wave_thread = threading.Thread(target=start_wave, daemon=True)
wave_thread.start()

print("=" * 60)
print("  Project Project — LED Wave Pulse Active")
print(f"  GPIO pins: {GPIO_PINS}")
print(f"  Wave delay: {WAVE_DELAY}s | Fade in: {FADE_IN}s | Fade out: {FADE_OUT}s")
print("  Cascading breathing wave running across 6 LEDs.")
print("  Press Ctrl+C to stop.")
print("=" * 60)

# ── Keep alive ───────────────────────────────────────────────
pause()
