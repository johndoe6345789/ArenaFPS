# Procedural Arena Generator

This directory contains Python scripts for procedurally generating Arena FPS style levels and assets.

## Features

- **Code-based generation**: All assets are generated from code, making them testable
- **Parametric design**: Easy to adjust arena size, platform placement, etc.
- **Unit tested**: Full test coverage for geometry generation
- **JSON export**: Geometry exported to JSON for import into Unreal Engine

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Generate an arena:

```bash
python arena_generator.py
```

This will create `arena_geometry.json` with the complete arena geometry.

### Run tests:

```bash
python -m pytest test_arena_generator.py -v
```

Or using unittest:

```bash
python test_arena_generator.py
```

## Generated Geometry

The generator creates:

1. **Main Floor**: The base arena floor
2. **Walls**: Perimeter walls around the arena
3. **Platforms**: Floating platforms (similar to DM17 "The Longest Yard")
4. **Jump Pads**: Launch pad positions (geometry for placement)

## Integration with Unreal Engine

The JSON output can be imported into Unreal Engine using:
1. Blueprint scripts that read the JSON
2. Python scripts in UE5 Editor
3. Custom C++ importers using GeometryScripting API

## Future Enhancements

- CADQuery integration for more complex geometry
- Weapon pickup generation
- Health/Armor pack generation
- Texture coordinate optimization
- LOD generation
- Collision mesh generation
