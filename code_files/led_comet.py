# led_comet.py
# ============================================================
# Project: Project Project (SkillLab 2 — Embedded Systems)
# File:    led_comet.py
# Effect:  COMET TAIL — sweeps brightness across 3 rows.
#          Each row contains 6 parallel LEDs sharing a signal.
#          The capacitor per row smooths the PWM into a clean
#          analog glow, so the brightness gradient between rows
#          looks fluid and cinematic.
# Author:  Team Project^2 (Mrugendra Vasmatkar, Jyoti Bagate)
# Date:    April 2026
# ============================================================
#
# ─── HARDWARE STRUCTURE ─────────────────────────────────────
#
#  GPIO 17 (Pin 11) ─┬─[1kΩ]─ LED1 (+) ── LED1 (−) ─┐
#                    ├─[1kΩ]─ LED2 (+) ── LED2 (−) ─┤
#                    ├─[1kΩ]─ LED3 (+) ── LED3 (−) ─┤─ GND
#  ROW 1             ├─[1kΩ]─ LED4 (+) ── LED4 (−) ─┤
#  (6 LEDs)          ├─[1kΩ]─ LED5 (+) ── LED5 (−) ─┤
#                    ├─[1kΩ]─ LED6 (+) ── LED6 (−) ─┤
#                    └─[100µF (+)] ─────── [100µF (−)] ─ GND
#                       ▲ LOW-PASS FILTER ▲
#
#  GPIO 18 (Pin 12) ─┬─[1kΩ]─ LED7  (+) ── LED7  (−) ─┐
#                    ├─[1kΩ]─ LED8  (+) ── LED8  (−) ─┤
#  ROW 2             ├─[1kΩ]─ LED9  (+) ── LED9  (−) ─┤─ GND
#  (6 LEDs)          ├─[1kΩ]─ LED10 (+) ── LED10 (−) ─┤
#                    ├─[1kΩ]─ LED11 (+) ── LED11 (−) ─┤
#                    ├─[1kΩ]─ LED12 (+) ── LED12 (−) ─┤
#                    └─[100µF (+)] ─────── [100µF (−)] ─ GND
#
#  GPIO 27 (Pin 13) ─┬─[1kΩ]─ LED13 (+) ── LED13 (−) ─┐
#                    ├─[1kΩ]─ LED14 (+) ── LED14 (−) ─┤
#  ROW 3             ├─[1kΩ]─ LED15 (+) ── LED15 (−) ─┤─ GND
#  (6 LEDs)          ├─[1kΩ]─ LED16 (+) ── LED16 (−) ─┤
#                    ├─[1kΩ]─ LED17 (+) ── LED17 (−) ─┤
#                    ├─[1kΩ]─ LED18 (+) ── LED18 (−) ─┤
#                    └─[100µF (+)] ─────── [100µF (−)] ─ GND
#
#  Pi Pin 6 (GND) ──────────────── All GND rails common
#
# ─── COMPONENT COUNT ────────────────────────────────────────
#  GPIO pins  : 3  (GPIO 17, 18, 27)
#  LEDs       : 18 (6 per row × 3 rows)
#  Resistors  : 18 (1kΩ, one per LED)
#  Capacitors : 3  (100µF, one per row — low-pass filter)
#
# ─── WHY THE CAPACITOR MATTERS HERE ────────────────────────
#  Each row's 6 LEDs are in parallel — they all share the same
#  PWM signal from their GPIO pin. The 100µF cap across the
#  row's signal node and GND smooths the digital switching into
#  a slow-rising / slow-falling analog voltage. This means:
#   ✓ All 6 LEDs in a row fade together smoothly as one unit.
#   ✓ The brightness transitions between rows look fluid.
#   ✓ The comet tail glow blends naturally instead of stepping.
#
# ─── COMET VISUAL ───────────────────────────────────────────
#  HEAD  (current row)  →  100% brightness  (all 6 LEDs full)
#  MID   (row behind)   →   45% brightness  (dim glow)
#  TAIL  (2 rows back)  →   10% brightness  (barely glowing)
#  The head sweeps: ROW1 → ROW2 → ROW3 → ROW2 → ROW1 → ...
#
# ─── USAGE ──────────────────────────────────────────────────
#  python3 led_comet.py             (default: bounce mode)
#  python3 led_comet.py --loop      (reset to start each time)
#  python3 led_comet.py --fast      (faster comet speed)
#  Press Ctrl+C to stop
# ============================================================

from gpiozero import PWMLED
import time
import sys

# ── GPIO → Row mapping ───────────────────────────────────────
# Each GPIO controls all 6 LEDs in its row simultaneously.
ROW_GPIO = [17, 18, 27]          # Row 0, Row 1, Row 2
NUM_ROWS = len(ROW_GPIO)

# ── Tail brightness profile ──────────────────────────────────
# Index 0 = HEAD (full), 1 = first tail step, 2 = second, etc.
# With only 3 rows, we have exactly 3 brightness levels:
TAIL_PROFILE = [1.0, 0.45, 0.10]

# ── Speed settings ───────────────────────────────────────────
STEP_DELAY  = 0.06 if "--fast" in sys.argv else 0.15
RESET_PAUSE = 0.25   # pause at end before reversing

# ── Run mode ─────────────────────────────────────────────────
BOUNCE = "--loop" not in sys.argv   # True = bounce, False = loop reset

# ── Initialise row LEDs ──────────────────────────────────────
rows = [PWMLED(pin) for pin in ROW_GPIO]

def set_frame(head_pos, direction=1):
    """Set all 3 rows to comet brightness for current head position."""
    for i, row in enumerate(rows):
        tail_dist = (head_pos - i) * direction
        if 0 <= tail_dist < len(TAIL_PROFILE):
            row.value = TAIL_PROFILE[tail_dist]
        else:
            row.value = 0.0

def clear_all():
    for row in rows:
        row.value = 0.0

# ── Main ─────────────────────────────────────────────────────
print("=" * 55)
print("  Project Project — 3-ROW COMET TAIL")
print("  18 LEDs | 3 rows × 6 LEDs | 3×100µF LPF")
print(f"  Mode: {'BOUNCE' if BOUNCE else 'LOOP'} | Step: {STEP_DELAY}s")
print("  Press Ctrl+C to stop.")
print("=" * 55)

try:
    direction = 1
    head = 0

    while True:
        set_frame(head, direction)
        time.sleep(STEP_DELAY)
        head += direction

        if direction == 1 and head >= NUM_ROWS:
            time.sleep(RESET_PAUSE)
            if BOUNCE:
                direction = -1
                head = NUM_ROWS - 1
            else:
                clear_all()
                time.sleep(RESET_PAUSE)
                head = 0

        elif direction == -1 and head < 0:
            time.sleep(RESET_PAUSE)
            direction = 1
            head = 0

except KeyboardInterrupt:
    print("\nStopping...")
finally:
    clear_all()
    for row in rows:
        row.close()
    print("GPIO cleaned up. Bye!")
