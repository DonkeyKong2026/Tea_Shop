# Tea_Shop: Diddy Kong Instrumentation Co.

Our final project for Scientific Instrumentation (PHYS-351). It's a Raspberry Pi tea station with:
- a stepper-driven turntable
- a liquid dispenser
- a heated plate with a temperature-status LED
- a servo claw
- a speaker system that plays music for the destination you pick

Our project journal is published with GitHub Pages at <https://donkeykong2026.github.io/Tea_Shop/>, served from `index.html`.

## Repository layout

```
index.html              Project journal website (served by GitHub Pages; keep it at the root)
src/
  music/                Speaker system: destination selector that plays an mp3 per country
  turntable/            Stepper motor control for the turntable
  temperature/          Heating pad, MCP9808 temperature sensor, RGB status LED
  claw/                 Servo claw / gripper (to be repurposed for the salt shaker)
docs/cad/               CAD drawings (PDF)
assets/images/          Images used by the website, plus build and lab photos
archive/                Old website template copies and test files, kept for reference
```

## Subsystems

### Music (`src/music/`)
All three scripts let you choose a country and play that country's mp3 with `mpg123`. The mp3 files are expected in `/home/pi/Downloads/`.
- `country_selector_cli.py`: terminal version that asks you to type a country.
- `country_selector_gui.py`: small Tkinter window with a dropdown menu.
- `country_selector_fullscreen.py`: fullscreen Tkinter touch interface with a button per country. Picking a new country stops the previous track.

### Turntable (`src/turntable/`)
- `stepper_rotate.py`: rotates the turntable stepper (NEMA 17 through a DRV8833 driver). It turns the table 90 degrees, then stops and waits idle. Steps are in place so that when a task finishes (for example, dispensing), the table turns to the next station. Until those functions are complete, the code only rotates the turntable 90 degrees.

### Temperature (`src/temperature/`)
- `heater.py`: drives the heating pads using a 12 W power supply, the Pi, and the DM3 driver. It switches the pads, which are wired in series, on and off.
- `rgb.py`: changes the LED color to show the surrounding temperature: green for cold, yellow for warm, red for hot. It uses a single 4-prong multicolor LED and the MCP9808 temperature sensor.
- `mcp9808_mod.py`: driver class for the MCP9808 sensor. It must stay in the same folder as `rgb.py` so `rgb.py` can import it.

### Claw (`src/claw/`)
- `claw.py`: rotates the first claw design with a servo. It will be repurposed for the salt shaker code but stays here for now for further editing.

### CAD (`docs/cad/`)
- `liquid_dispenser.pdf`: liquid dispenser drawing.
- `gripper_intake.pdf`: gripper intake drawing.

## Running code on the Pi
Run scripts from their own folder so local imports resolve:
```bash
cd src/temperature
python3 rgb.py
```
Dependencies: `RPi.GPIO`, `gpiozero`, `smbus2`, `tkinter`, and the `mpg123` command-line player.

## Renamed files
When the repo was reorganized, files moved as follows:

| Old name | New location |
|---|---|
| `musicwithstyle.py` | `src/music/country_selector_cli.py` |
| `vibecode.py` | `src/music/country_selector_gui.py` |
| `vibescode.py` | `src/music/country_selector_fullscreen.py` |
| `stepperrotate.py` | `src/turntable/stepper_rotate.py` |
| `HEATER.PY` | `src/temperature/heater.py` |
| `RGB.py` | `src/temperature/rgb.py` |
| `mcp9808_mod (1).py` | `src/temperature/mcp9808_mod.py` |
| `claw.py` | `src/claw/claw.py` |
| `Diddy_Liquid_Dispenser (1).pdf` | `docs/cad/liquid_dispenser.pdf` |
| `GRIPPER INTAKE (1).pdf` | `docs/cad/gripper_intake.pdf` |
| `Diddy_Kong.png` | `assets/images/diddy-kong.png` |
| `Didylogo.jpg` | `assets/images/diddy-logo.jpg` |
| `StepperMotorNema17_2.png` | `assets/images/stepper-motor-nema17.png` |
| `Screenshot 2026-11-02 154707(1).png` | `assets/images/circuit-diagram.png` |
| `Screenshot 2026-11-03 015238.png` | `assets/images/chalkboard-design-notes.png` |
| `IMG_7697 (1).jpeg` | `assets/images/lab-bench-wiring.jpg` |
| `IMG_7698 (1).jpeg` | `assets/images/cad-modeling.jpg` |
| `IMG_9211 (1).jpeg` | `assets/images/3d-printed-gripper-parts.jpg` |
| `IMG_9225 (1).PNG` | `assets/images/pi-breadboard-circuit.png` |
| `DiddyKongWeb`, `Classes/.../dk_jungle_journal.html`, `Classes/.../README.md` | `archive/old-website/` |
| `demo` | `archive/demo.txt` |

When you add an image to the website, put it in `assets/images/` and reference it as `src="assets/images/<name>"`. GitHub Pages is case-sensitive, so the filename must match exactly.

## Weekly updates

**Week 1:** `vibescode.py`, `vibecode.py` and `musicwithstyle.py` are the music code for the output setup. They are now in `src/music/`.

**Week 2:** Added `stepperrotate.py`, `RGB.py`, `mcp9808_mod.py`, `HEATER.py` and `claw.py`. They are now in `src/turntable/`, `src/temperature/` and `src/claw/`, described above.
