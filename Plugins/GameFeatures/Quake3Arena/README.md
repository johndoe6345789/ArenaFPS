# Quake3Arena Plugin Documentation

## Overview

The Quake3Arena plugin provides a complete Quake 3 Arena-style deathmatch experience for Unreal Engine 5, including:
- Game mode implementation
- Bot AI (Crash bot)
- Procedural geometry import system

## Components

### Game Mode: AQuake3GameMode

The main game mode class that implements Q3A deathmatch rules.

**Key Properties:**
- `FragLimit` (int32): Number of frags needed to win (default: 25)
- `TimeLimit` (float): Time limit in seconds (default: 600.0 = 10 minutes)
- `NumberOfBots` (int32): Number of bots to spawn (default: 3)
- `RespawnDelay` (float): Delay before respawning in seconds (default: 3.0)

**Usage in Blueprint:**
1. Create a new Blueprint based on `AQuake3GameMode`
2. Configure game settings (frag limit, time limit, etc.)
3. Set as the default game mode in World Settings

### Bot AI: AQuake3Bot

AI controller for bot players, implementing Crash bot behavior.

**Key Properties:**
- `SkillLevel` (int32): Bot skill level from 0-5 (5 = nightmare difficulty)
- `BotName` (string): Display name for the bot (default: "Crash")
- `AccuracyModifier` (float): Affects bot aim accuracy (default: 0.7)
- `ReactionTime` (float): Bot reaction time in seconds (default: 0.3)

**Behavior States:**
- `Idle`: Looking for something to do
- `Combat`: Engaging an enemy
- `SeekingWeapon`: Moving to pick up a weapon
- `SeekingHealth`: Moving to pick up health
- `Roaming`: Random exploration when no other goals

### Geometry Importer: AArenaGeometryImporter

Actor that imports procedurally generated geometry from JSON files.

**Key Properties:**
- `JsonFilePath` (string): Path to the JSON geometry file
- `DefaultMaterial` (UMaterial*): Material to apply to imported meshes

**Usage:**
1. Place `AArenaGeometryImporter` in your level
2. Set `JsonFilePath` to the generated JSON (e.g., "arena_geometry.json")
3. Assign a material to `DefaultMaterial`
4. The geometry will be imported automatically on BeginPlay

**Blueprint Usage:**
```cpp
// In Blueprint, call:
bool Success = ArenaGeometryImporter->ImportArenaFromJson("/Game/Data/arena_geometry.json");
```

## Procedural Generation Workflow

### 1. Generate Geometry

Run the Python script to generate arena geometry:

```bash
cd Tools/ProceduralGeneration
python arena_generator.py
```

This creates `arena_geometry.json` with the complete arena layout.

### 2. Copy to Content Directory

Copy the JSON file to your Unreal project's content directory:

```bash
# Example:
cp arena_geometry.json ../../Content/Maps/ArenaData/
```

### 3. Import in Unreal

**Method A: Using ArenaGeometryImporter Actor**
1. Drag `ArenaGeometryImporter` into your level
2. Set the `JsonFilePath` property
3. Assign a material
4. Play to see the geometry load

**Method B: Using Blueprint**
1. Create a Blueprint
2. Add `ArenaGeometryImporter` component
3. Call `ImportArenaFromJson` with the file path
4. Handle success/failure

### 4. Test and Iterate

- Modify parameters in `arena_generator.py`
- Regenerate geometry
- Reload in Unreal Engine
- Iterate until satisfied

## Customization

### Modifying the Arena

Edit `Tools/ProceduralGeneration/arena_generator.py`:

```python
# Change arena size
generator = ArenaGenerator(size=10000.0, height=2000.0)

# Modify platform positions in generate_platforms()
platform_configs = [
    (x, y, z, width, depth, height),
    # Add more platforms
]
```

### Creating Custom Bot Behavior

Extend `AQuake3Bot` in C++ or Blueprint:

```cpp
UCLASS()
class AMyCustomBot : public AQuake3Bot
{
    // Override UpdateBehavior() for custom AI
    virtual void UpdateBehavior() override;
};
```

### Adding Weapons and Pickups

The plugin is designed to work with Lyra's weapon system. To add Q3A-style weapons:

1. Create weapon data assets based on Lyra's weapon system
2. Place weapon spawners in the level
3. Configure bot behavior to seek specific weapons

## Testing

### Python Tests

Test the procedural generator:

```bash
cd Tools/ProceduralGeneration
python -m pytest test_arena_generator.py -v
```

### In-Engine Testing

1. Open the level with Quake3Arena game mode
2. PIE (Play In Editor)
3. Verify bots spawn and behave correctly
4. Test game rules (frag limit, time limit)

## Performance Considerations

- **Mesh Complexity**: Keep triangle counts reasonable (use LODs for complex geometry)
- **Collision**: The importer creates collision automatically - optimize as needed
- **Bot Count**: More bots = more CPU usage. Test with different counts
- **Material Complexity**: Use optimized materials for procedural geometry

## Integration with Lyra

This plugin is designed to work alongside Lyra's systems:

- Uses Lyra's character system
- Compatible with Lyra's weapon framework
- Works with Lyra's input system
- Integrates with Gameplay Abilities

You can mix and match Quake3Arena features with Lyra's existing game modes.

## Troubleshooting

**Geometry not appearing:**
- Check the JsonFilePath is correct
- Verify the JSON file is valid (use a JSON validator)
- Check the log for import errors
- Ensure DefaultMaterial is assigned

**Bots not spawning:**
- Verify Player Starts exist in the level
- Check NumberOfBots is > 0
- Look for errors in the log

**Performance issues:**
- Reduce number of bots
- Simplify procedural geometry
- Optimize materials
- Enable level streaming for large arenas

## Future Enhancements

Planned features:
- Advanced weapon system (Rocket Launcher, Railgun, etc.)
- Health and armor pickups
- Quad damage and other powerups
- Strafe jumping mechanics
- Scoreboards and HUD
- More bot personalities
- Team deathmatch mode
- Capture the Flag mode
