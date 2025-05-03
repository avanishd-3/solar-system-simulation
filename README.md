# Solar System Simulation

This is a solar system simulation (accurate distances) built with Pygame.

## How to Run
Recommended: Use uv (it is much faster than Pip or other Python package managers).

### Installing UV
See [installation guide](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) for all options.

#### Unix/MacOS

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

or

```
brew install uv
```
#### Windows

```
winget install --id=astral-sh.uv  -e
```

### Running Code
```
uv sync # Only needed to install dependencies to venv

uv run src/main.py
```

## Commands

### Simulation Speed
| Key         | Action      |
| ----------- | ----------- |
| Left Arrow  | Slow down   |
| Right Arrow | Speed up    |
| t           | Reset speed |

### Simulation Scale
| Key                 | Action     |
| ------------------- | ---------- |
| Plus or Up Arrow | Zoom in   |
| Down or Minus Arrow    | Zoom out    |
| r                   | Reset zoom |

### Other
| Key   | Action            |
| ----- | ----------------- |
| space | pause/unpause     |
| f     | toggle fullscreen |
| s     | toggle FPS |