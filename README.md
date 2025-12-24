# ArenaFPS

A Arena FPS clone built in Unreal Engine 5 with procedurally generated assets and CI/CD pipeline.

## Overview

This project recreates the classic Arena FPS experience in Unreal Engine 5, featuring:
- **Procedural Level Generation**: Levels generated from Python code for testability
- **Bot AI**: Bot AI implementation with combat and navigation logic
- **Deathmatch Game Mode**: Classic Arena FPS deathmatch rules
- **CI/CD Pipeline**: Automated testing and validation

## Features

### Game Systems
- **Arena FPS Game Mode** (`Plugins/GameFeatures/ArenaFPS`)
  - Deathmatch with frag limit and time limit
  - Bot spawning and management
  - Respawn system
  
- **Crash Bot AI**
  - State-based behavior (Combat, Roaming, Seeking Items)
  - Navigation using UE5's Navigation System
  - Configurable skill levels

### Procedural Generation
- **Arena Level Generator** (`Tools/ProceduralGeneration`)
  - Code-based geometry generation
  - Exports to JSON format
  - Unit tested with pytest
  - Inspired by DM17 "The Longest Yard"

### CI/CD
- **Automated Testing**: Python unit tests for procedural generators
- **Project Validation**: JSON validation, structure checks
- **Artifact Generation**: Automated arena geometry generation

## Getting Started

### Prerequisites
- Unreal Engine 5.7
- Python 3.11+ (for procedural generation)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/johndoe6345789/Unreal3Arena.git
   cd Unreal3Arena
   ```

2. Install Python dependencies:
   ```bash
   cd Tools/ProceduralGeneration
   pip install -r requirements.txt
   ```

3. Generate arena geometry:
   ```bash
   python arena_generator.py
   ```

4. Open `Unreal3Arena.uproject` in Unreal Engine 5.7

### Running Tests

#### Python Tests
```bash
cd Tools/ProceduralGeneration
python -m pytest test_arena_generator.py -v
```

## Project Structure

```
Unreal3Arena/
├── .github/workflows/          # CI/CD pipelines
│   ├── procedural-tests.yml   # Python procedural generation tests
│   └── unreal-ci.yml          # Unreal Engine project validation
├── Content/                    # Unreal Engine content
├── Plugins/
│   └── GameFeatures/
│       └── ArenaFPS/       # Arena FPS game mode plugin
│           ├── Content/       # Assets and blueprints
│           └── Source/        # C++ source code
├── Source/                     # Main game source (Lyra-based)
├── Tools/
│   └── ProceduralGeneration/  # Python procedural generators
│       ├── arena_generator.py
│       ├── test_arena_generator.py
│       └── requirements.txt
└── Unreal3Arena.uproject      # UE5 project file
```

## Key Components

### ArenaFPS Plugin
Located in `Plugins/GameFeatures/ArenaFPS/`:
- `ArenaGameMode`: Deathmatch game mode with Arena FPS rules
- `ArenaBot`: AI controller for bot players (Bot AI)

### Procedural Generation
Located in `Tools/ProceduralGeneration/`:
- `arena_generator.py`: Generates arena geometry procedurally
- Exports JSON data for import into Unreal Engine
- Full unit test coverage for reliability

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure nothing breaks
5. Submit a pull request

## License

Developed with Unreal Engine 5

## Acknowledgments

- Based on Epic Games' Lyra Sample Game
- Inspired by classic arena-style FPS games
- Uses Unreal Engine 5.7
