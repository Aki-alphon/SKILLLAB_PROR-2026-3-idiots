# SkillLab 2 — Embedded Systems
## LED Cluster Project · Code Files Documentation

---

## Project Information

| Field            | Details                                       |
|------------------|-----------------------------------------------|
| **Group Number** | 37                                            |
| **Group Name**   | 3-Idiots                                      |
| **Lab**          | SkillLab 2 — Embedded Systems                 |
| **Platform**     | Raspberry Pi 3B                               |
| **Language**     | Python 3 (gpiozero)                           |
| **Submitted**    | May 2026                                      |

### Group Members

| Name                  | Roll No.  | Division |
|-----------------------|-----------|----------|
| Ajaykumar Nagpure     | D14A - 25 | D14A     |
| Shrinath Pattewar     | D14A - 33 | D14A     |
| Mayuresh Panhalkar    | D14B - 35 | D14B     |

---

## Hardware Architecture

**3-Row × 6-LED Cluster** driven by 3 GPIO pins.
Each row has **1 shared 1kΩ resistor**, **6 LEDs in parallel**, and
**one 100µF electrolytic capacitor** as a **hardware low-pass filter (LPF)**.

```
                     1kΩ
Pi GPIO 17 ────────[===]──┬── LED1  (+) ──LED1  (−) ──┐
(Pin 11)                  ├── LED2  (+) ──LED2  (−) ──┤
ROW 1                     ├── LED3  (+) ──LED3  (−) ──┤
                          ├── LED4  (+) ──LED4  (−) ──┤─── GND rail
                          ├── LED5  (+) ──LED5  (−) ──┤
                          ├── LED6  (+) ──LED6  (−) ──┤
                          └── [100µF (+)]──[100µF (−)]┘  ← LPF

                     1kΩ
Pi GPIO 18 ────────[===]──┬── LED7  (+) ──LED7  (−) ──┐
(Pin 12)                  ├── LED8  (+) ──LED8  (−) ──┤
ROW 2                     ├── LED9  (+) ──LED9  (−) ──┤
                          ├── LED10 (+) ──LED10 (−) ──┤─── GND rail
                          ├── LED11 (+) ──LED11 (−) ──┤
                          ├── LED12 (+) ──LED12 (−) ──┤
                          └── [100µF (+)]──[100µF (−)]┘  ← LPF

                     1kΩ
Pi GPIO 27 ────────[===]──┬── LED13 (+) ──LED13 (−) ──┐
(Pin 13)                  ├── LED14 (+) ──LED14 (−) ──┤
ROW 3                     ├── LED15 (+) ──LED15 (−) ──┤
                          ├── LED16 (+) ──LED16 (−) ──┤─── GND rail
                          ├── LED17 (+) ──LED17 (−) ──┤
                          ├── LED18 (+) ──LED18 (−) ──┤
                          └── [100µF (+)]──[100µF (−)]┘  ← LPF

Pi Pin 6 (GND) ──────── All 3 GND rails connected together
```

### Component Count

| Component       | Qty |  Spec             | Purpose                                          |
|-----------------|----:|-------------------|--------------------------------------------------|
| GPIO pins       |   3 | GPIO 17, 18, 27   | One PWM control channel per row                  |
| Red LEDs        |  18 | Standard 5mm      | 6 per row, all wired in parallel                 |
| Resistors       |   3 | 1kΩ               | One per row — shared current limiter             |
| Capacitors      |   3 | 100µF, 16V+       | One per row — low-pass filter (LPF)              |
| Jumper wires    |  —  | M-M / M-F         | GPIO → breadboard connections                    |
| Breadboard      |   1 | Full/Half size     | Component mounting                               |

> **Current per row:** (3.3V − 2.0V) / 1kΩ = **1.3 mA per row** (≈ 0.22 mA per LED).
> LEDs glow softly — ideal for atmospheric / cinematic lighting.
> For brighter output: replace 1kΩ with **220Ω** (≈ 5.9 mA per row, ~1 mA per LED).

---

### Why the 100µF Capacitor (LPF)?

PWM is a digital signal rapidly switching between 0V and 3.3V.
The 100µF cap charges/discharges slowly, **averaging** the switching
into a smooth, continuous analogue voltage across all 6 row LEDs:

| PWM Duty Cycle | Voltage at cap | Row brightness |
|----------------|----------------|----------------|
| 0%             | ~0 V           | OFF            |
| 25%            | ~0.8 V         | Faint glow     |
| 50%            | ~1.65 V        | Half glow      |
| 75%            | ~2.5 V         | Bright glow    |
| 100%           | ~3.3 V         | Full on        |

All 6 LEDs in the row **rise and fall together as one smooth band**.

> **Capacitor polarity is critical:**
> **(+) leg → signal node** (between resistor and LED anodes)
> **(−) leg → GND rail**
> Reversing polarity will damage the capacitor.

### Current Safety

```
I per row  = (3.3V − 2.0V) / 1kΩ = 1.3 mA   ← Pi per-pin limit: 16 mA ✓
Per LED    = 1.3 mA / 6 = 0.22 mA            ← LED max: 20 mA ✓
All rows   = 3 × 1.3 mA = 3.9 mA total       ← Pi GPIO bank limit: 50 mA ✓
```

---

## File List & Run Order

Run in this order when setting up for the first time:

| Step | File                   | Purpose                                              | GPIO Used       | Command                        |
|------|------------------------|------------------------------------------------------|-----------------|--------------------------------|
| 1    | `led_pulse.py`         | TEST: Row 1 only breathing — verify wiring           | GPIO 17         | `python3 led_pulse.py`         |
| 2    | `led_board_pulse.py`   | TEST: All 3 rows breathing in unison                 | GPIO 17, 18, 27 | `python3 led_board_pulse.py`   |
| 3    | `led_wave.py`          | Staggered row start — cascading forward wave         | GPIO 17, 18, 27 | `python3 led_wave.py`          |
| 4    | `led_pingpong.py`      | Ping-pong glow — Gaussian spotlight bounces 1↔3     | GPIO 17, 18, 27 | `python3 led_pingpong.py`      |
| 5    | `led_comet.py`         | Comet tail sweeping across rows (bounce/loop)        | GPIO 17, 18, 27 | `python3 led_comet.py`         |
| 6    | `led_wave_cluster.py`  | Sine wave ripple — real-time math per row            | GPIO 17, 18, 27 | `python3 led_wave_cluster.py`  |
| 7    | `led_effects_menu.py`  | Interactive menu: 8 effects switchable live          | GPIO 17, 18, 27 | `python3 led_effects_menu.py`  |

---

## File Descriptions

### `led_pulse.py` — Row 1 Single Test
Breathes Row 1 only (GPIO 17 → 1kΩ → 6 LEDs + 100µF LPF).
Run this **first**. If all 6 LEDs in Row 1 fade smoothly with no flicker → wiring OK.
Flicker visible? → check capacitor polarity (+ to signal node, − to GND).

### `led_board_pulse.py` — All 3 Rows Together
Uses `LEDBoard(17, 18, 27, pwm=True).pulse()` — all 3 rows breathe in sync.
Run this **second**. All 3 row-bands should glow and fade identically and simultaneously.

### `led_wave.py` — Staggered Row Wave ⭐
Starts each row's `pulse()` 0.5s after the previous row.
Glow cascades top-to-bottom: Row 1 → Row 2 → Row 3 → (loops forever).
Edit `ROW_DELAY` to control wave speed. Edit `FADE_IN` / `FADE_OUT` for breath pace.

### `led_pingpong.py` — Ping-Pong Glow ⭐ *(new)*
A Gaussian "spotlight" travels forward across rows (1→2→3), then bounces back (3→2→1),
repeating infinitely. Direction reversal is perfectly smooth — no brightness jump —
because the Gaussian function is continuous and symmetric at boundaries.
Edit `WAVE_SPEED`, `SIGMA`, and `MIN_BRIGHT` to change feel.
> See `HOW_IT_WORKS.md` for a full technical explanation of the Gaussian math.

### `led_comet.py` — Comet Tail
Sweeps brightness across rows: HEAD = 100%, MID = 45%, TAIL = 10%.
Default: bounce mode (R1→R2→R3→R2→R1).
`--loop` flag: reset mode (R1→R2→R3, restart). `--fast` flag: faster speed.

### `led_wave_cluster.py` — Sine Wave
Per-row brightness: `0.5 + 0.5 × sin(2π × speed × t − phase × i)`
Each row is phase-shifted, creating a smooth sine ripple across the 3 row-bands.
Edit `WAVE_SPEED` and `WAVE_SPREAD` to adjust feel.

### `led_effects_menu.py` — Interactive Effects Menu
Press a number to switch effect live (no restart needed):

| Key | Effect          | Description                                            |
|-----|-----------------|--------------------------------------------------------|
| 1   | Comet Loop      | Head R1→R2→R3 at 100%/45%/10%, resets                 |
| 2   | Comet Bounce    | Same but bounces R3→R2→R1→R2→R3 continuously          |
| 3   | Sine Wave       | Phase-shifted sine ripple across 3 rows                |
| 4   | Double Wave     | Two overlapping waves → interference pattern           |
| 5   | Theatre Chase   | One row fully ON at a time, rotating                   |
| 6   | Pulse All       | All 3 rows breathe together as one unit                |
| 7   | Cascade Up      | Rows fill bottom → top, then clear top → bottom        |
| 8   | Meteor Shower   | Random rows flash and decay — comet burst effect       |
| Q   | Quit            | Cleans up GPIO and exits safely                        |

---

## Wiring Checklist

Before running any script:

- [ ] Pi is **powered OFF** while wiring
- [ ] GPIO 17 (Pin 11) → 1kΩ resistor → Row 1 signal node
- [ ] GPIO 18 (Pin 12) → 1kΩ resistor → Row 2 signal node
- [ ] GPIO 27 (Pin 13) → 1kΩ resistor → Row 3 signal node
- [ ] Each row has **6 LEDs** with all anodes (+) connected to signal node
- [ ] Each row has one 100µF cap: **(+) to signal node, (−) to GND**
- [ ] All LED cathodes (−) connected to the GND rail
- [ ] All 3 GND rails joined → one wire to Pi Pin 6 (GND)
- [ ] Run `led_pulse.py` first to verify Row 1 before full cluster

---

## Dependencies

```bash
# All pre-installed on Raspberry Pi OS — no pip install needed
python3 --version                                   # needs 3.7+
python3 -c "import gpiozero; print(gpiozero.__version__)"
```

If gpiozero is missing (unlikely on Pi OS):
```bash
sudo apt update && sudo apt install python3-gpiozero
```

---

## Additional Documentation

| File               | Contents                                                      |
|--------------------|---------------------------------------------------------------|
| `HOW_IT_WORKS.md`  | Deep-dive: Gaussian math, PWM, capacitor physics, threading  |

---

*Group: 3-Idiots · SkillLab 2 — Embedded Systems · May 2026*
*Ajaykumar Nagpure (D14A-25) · Shrinath Pattewar (D14A-33) · Mayuresh Panhalkar (D14B-35)*
