# Quake3Arena Quick Reference

## Quick Start

```bash
# 1. Setup environment
./setup.sh

# 2. Generate all assets
cd Tools/ProceduralGeneration
python generate_all.py

# 3. Open in Unreal Engine
# Open Unreal3Arena.uproject in UE 5.7
```

## Common Commands

### Procedural Generation

```bash
# Generate everything
python generate_all.py

# Generate arena only
python arena_generator.py

# Generate weapons only
python weapon_generator.py

# Run tests
python -m pytest test_arena_generator.py -v
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes, then commit
git add .
git commit -m "feat: description"

# Push to fork
git push origin feature/my-feature
```

## File Locations

| What | Where |
|------|-------|
| Game Mode | `Plugins/GameFeatures/Quake3Arena/Source/.../Quake3GameMode.cpp` |
| Bot AI | `Plugins/GameFeatures/Quake3Arena/Source/.../Quake3Bot.cpp` |
| Geometry Importer | `Plugins/GameFeatures/Quake3Arena/Source/.../ArenaGeometryImporter.cpp` |
| Arena Generator | `Tools/ProceduralGeneration/arena_generator.py` |
| Weapon Generator | `Tools/ProceduralGeneration/weapon_generator.py` |
| CI/CD Config | `.github/workflows/` |

## Key Classes

### C++ Classes

| Class | Purpose |
|-------|---------|
| `AQuake3GameMode` | Main game mode with Q3A rules |
| `AQuake3Bot` | Bot AI controller |
| `AArenaGeometryImporter` | Imports JSON geometry to UE5 |

### Python Classes

| Class | Purpose |
|-------|---------|
| `ArenaGenerator` | Generates arena geometry |
| `WeaponGenerator` | Generates weapon meshes |
| `PickupGenerator` | Generates pickup items |

## Game Mode Settings

In Blueprint or C++:

```cpp
FragLimit = 25;           // Frags to win
TimeLimit = 600.0f;       // Time limit (seconds)
NumberOfBots = 3;         // Bots to spawn
RespawnDelay = 3.0f;      // Respawn delay
```

## Bot Settings

```cpp
SkillLevel = 2;           // 0-5 (5 = nightmare)
BotName = "Crash";        // Display name
AccuracyModifier = 0.7f;  // Aim accuracy
ReactionTime = 0.3f;      // Response time
```

## Geometry Import

In Blueprint:

```
1. Add ArenaGeometryImporter actor to level
2. Set JsonFilePath = "path/to/arena_geometry.json"
3. Set DefaultMaterial
4. Play - geometry loads automatically
```

Or call from Blueprint:
```cpp
ImportArenaFromJson("/Game/Data/arena_geometry.json");
```

## Arena Customization

Edit `arena_generator.py`:

```python
# Change size
generator = ArenaGenerator(size=10000.0, height=2000.0)

# Modify platforms in generate_platforms()
platform_configs = [
    (x, y, z, width, depth, height),
]
```

## Testing Checklist

- [ ] Python tests pass: `pytest test_*.py -v`
- [ ] Assets generate: `python generate_all.py`
- [ ] Project opens in UE5
- [ ] Plugin loads without errors
- [ ] Bots spawn in level
- [ ] Game mode functions

## Troubleshooting

**Geometry not appearing?**
- Check JsonFilePath is correct
- Verify JSON is valid
- Assign DefaultMaterial

**Bots not spawning?**
- Add Player Starts to level
- Set NumberOfBots > 0
- Check console for errors

**Build errors?**
- Verify UE5.7 is installed
- Check module dependencies in .Build.cs
- Regenerate project files

## Useful Links

- [Unreal Engine Documentation](https://docs.unrealengine.com/)
- [Lyra Sample Game](https://docs.unrealengine.com/5.0/en-US/lyra-sample-game-in-unreal-engine/)
- [Python API for UE5](https://docs.unrealengine.com/5.0/en-US/PythonAPI/)

## Project Status

✅ Implemented:
- Game mode with Q3A rules
- Bot AI with state machine
- Procedural arena generation
- Weapon/pickup generators
- Geometry importer
- CI/CD pipeline
- Unit tests

🚧 In Progress:
- Weapon system integration
- Pickup actors
- Enhanced bot behavior

📋 Planned:
- Movement mechanics
- HUD/Scoreboard
- Additional game modes
