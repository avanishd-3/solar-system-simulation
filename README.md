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