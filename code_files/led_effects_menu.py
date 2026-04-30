# led_effects_menu.py
# ============================================================
# Project: Project Project (SkillLab 2 — Embedded Systems)
# File:    led_effects_menu.py
# Purpose: Interactive menu — switch between LED effects live.
#          Designed for 3-row cluster (18 LEDs total):
#          3 rows × 6 parallel LEDs + 1×100µF LPF cap per row.
# Author:  Team Project^2 (Mrugendra Vasmatkar, Jyoti Bagate)
# Date:    April 2026
# ============================================================
#
# ─── HARDWARE (same for all effects) ────────────────────────
#  GPIO 17 → 6×[1kΩ→LED] in parallel + 100µF LPF → ROW 1
#  GPIO 18 → 6×[1kΩ→LED] in parallel + 100µF LPF → ROW 2
#  GPIO 27 → 6×[1kΩ→LED] in parallel + 100µF LPF → ROW 3
#  All GND rails → Pi Pin 6 (GND)
#
# ─── EFFECTS ────────────────────────────────────────────────
#   [1] Comet → Loop      head sweeps R1→R2→R3, resets to R1
#   [2] Comet ↔ Bounce    head sweeps and bounces back
#   [3] Sine Wave         smooth phase-shifted wave per row
#   [4] Double Wave       two overlapping waves (interference)
#   [5] Theatre Chase     one row ON at a time, rotating
#   [6] Pulse All         all 3 rows breathe together
#   [7] Cascade Up        rows light up from bottom to top
#   [8] Meteor Shower     randomized comet-like bursts
#   [Q] Quit
#
# USAGE:
#   python3 led_effects_menu.py
# ============================================================

from gpiozero import PWMLED
import time
import math
import threading
import random

# ── GPIO row configuration ───────────────────────────────────
ROW_GPIO = [17, 18, 27]
NUM_ROWS = len(ROW_GPIO)

rows = [PWMLED(pin) for pin in ROW_GPIO]
stop_flag = threading.Event()

def clear_all():
    for row in rows:
        row.value = 0.0

# ════════════════════════════════════════════════════════════
# EFFECT 1 & 2: COMET TAIL (sweeps across 3 rows)
# ════════════════════════════════════════════════════════════
# Visual: HEAD 100% → MID 45% → TAIL 10%
TAIL_PROFILE = [1.0, 0.45, 0.10]

def effect_comet(bounce=True, step=0.15):
    direction = 1
    head = 0
    while not stop_flag.is_set():
        for i, row in enumerate(rows):
            d = (head - i) * direction
            row.value = TAIL_PROFILE[d] if 0 <= d < len(TAIL_PROFILE) else 0.0
        time.sleep(step)
        head += direction
        if direction == 1 and head >= NUM_ROWS:
            time.sleep(0.2)
            if bounce:
                direction = -1; head = NUM_ROWS - 1
            else:
                clear_all(); time.sleep(0.2); head = 0
        elif direction == -1 and head < 0:
            time.sleep(0.2); direction = 1; head = 0
    clear_all()

# ════════════════════════════════════════════════════════════
# EFFECT 3: SINE WAVE (phase-shifted per row)
# ════════════════════════════════════════════════════════════
def effect_sine_wave(speed=1.0, spread=1.0, dt=0.03):
    t0 = time.time()
    while not stop_flag.is_set():
        t = time.time() - t0
        for i, row in enumerate(rows):
            phase = (2 * math.pi * spread * i) / NUM_ROWS
            row.value = max(0.0, 0.5 + 0.5 * math.sin(2 * math.pi * speed * t - phase))
        time.sleep(dt)
    clear_all()

# ════════════════════════════════════════════════════════════
# EFFECT 4: DOUBLE WAVE (interference pattern)
# Two waves at different speeds create complex moiré effect.
# ════════════════════════════════════════════════════════════
def effect_double_wave(s1=0.8, s2=1.5, spread=1.0, dt=0.03):
    t0 = time.time()
    while not stop_flag.is_set():
        t = time.time() - t0
        for i, row in enumerate(rows):
            phase = (2 * math.pi * spread * i) / NUM_ROWS
            w1 = 0.5 + 0.5 * math.sin(2 * math.pi * s1 * t - phase)
            w2 = 0.5 + 0.5 * math.sin(2 * math.pi * s2 * t - phase)
            row.value = min(1.0, max(0.0, (w1 + w2) / 2))
        time.sleep(dt)
    clear_all()

# ════════════════════════════════════════════════════════════
# EFFECT 5: THEATRE CHASE (one row on at a time, rotating)
# ════════════════════════════════════════════════════════════
def effect_theatre_chase(step=0.2):
    pos = 0
    while not stop_flag.is_set():
        for i, row in enumerate(rows):
            row.value = 1.0 if i == pos else 0.0
        time.sleep(step)
        pos = (pos + 1) % NUM_ROWS
    clear_all()

# ════════════════════════════════════════════════════════════
# EFFECT 6: PULSE ALL (all 3 rows breathe together)
# ════════════════════════════════════════════════════════════
def effect_pulse_all(speed=0.8, dt=0.03):
    t0 = time.time()
    while not stop_flag.is_set():
        t = time.time() - t0
        v = 0.5 + 0.5 * math.sin(2 * math.pi * speed * t)
        for row in rows:
            row.value = v
        time.sleep(dt)
    clear_all()

# ════════════════════════════════════════════════════════════
# EFFECT 7: CASCADE UP (rows fill bottom to top, then clear)
# ════════════════════════════════════════════════════════════
def effect_cascade_up(step=0.18, hold=0.3):
    while not stop_flag.is_set():
        # Fill up from bottom row to top
        for i in range(NUM_ROWS - 1, -1, -1):
            if stop_flag.is_set(): break
            rows[i].value = 1.0
            time.sleep(step)
        time.sleep(hold)
        # Clear from top to bottom
        for i in range(NUM_ROWS):
            if stop_flag.is_set(): break
            rows[i].value = 0.0
            time.sleep(step)
        time.sleep(hold)
    clear_all()

# ════════════════════════════════════════════════════════════
# EFFECT 8: METEOR SHOWER (random flashes with decay)
# ════════════════════════════════════════════════════════════
def effect_meteor(dt=0.04):
    brightness = [0.0] * NUM_ROWS
    while not stop_flag.is_set():
        # Random row gets a new meteor hit
        if random.random() < 0.15:
            brightness[random.randint(0, NUM_ROWS - 1)] = 1.0
        # Decay all rows
        for i in range(NUM_ROWS):
            brightness[i] = max(0.0, brightness[i] - 0.07)
            rows[i].value = brightness[i]
        time.sleep(dt)
    clear_all()

# ════════════════════════════════════════════════════════════
# MENU RUNNER
# ════════════════════════════════════════════════════════════
EFFECTS = {
    "1": ("Comet  →  Loop",       lambda: effect_comet(bounce=False)),
    "2": ("Comet  ↔  Bounce",     lambda: effect_comet(bounce=True)),
    "3": ("Sine Wave",            lambda: effect_sine_wave()),
    "4": ("Double Wave",          lambda: effect_double_wave()),
    "5": ("Theatre Chase",        lambda: effect_theatre_chase()),
    "6": ("Pulse All",            lambda: effect_pulse_all()),
    "7": ("Cascade Up",           lambda: effect_cascade_up()),
    "8": ("Meteor Shower",        lambda: effect_meteor()),
}

current_thread = None

def run_effect(func):
    global current_thread
    stop_flag.set()
    if current_thread and current_thread.is_alive():
        current_thread.join(timeout=1.0)
    stop_flag.clear()
    current_thread = threading.Thread(target=func, daemon=True)
    current_thread.start()

def print_menu():
    print("\n" + "═" * 50)
    print("  Project Project — 3-ROW LED EFFECTS CLUSTER")
    print("  GPIO 17→ROW1 | GPIO 18→ROW2 | GPIO 27→ROW3")
    print("  18 LEDs total | 3×100µF LPF smoothing")
    print("═" * 50)
    for key, (name, _) in EFFECTS.items():
        print(f"  [{key}] {name}")
    print("  [Q] Quit")
    print("═" * 50)
    print("  Select effect: ", end="", flush=True)

try:
    print_menu()
    while True:
        choice = input().strip().upper()
        if choice == "Q":
            break
        elif choice in EFFECTS:
            name, func = EFFECTS[choice]
            print(f"  ▶ {name}")
            run_effect(func)
        else:
            print("  Invalid. Try again: ", end="", flush=True)
            continue
        print_menu()

except KeyboardInterrupt:
    pass
finally:
    stop_flag.set()
    if current_thread and current_thread.is_alive():
        current_thread.join(timeout=1.0)
    clear_all()
    for row in rows:
        row.close()
    print("\nGPIO cleaned up. Bye!")
