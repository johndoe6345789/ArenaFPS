#!/usr/bin/env python3
"""
Master script to generate all procedural assets for Quake3Arena
Run this script to generate the complete asset set
"""

import sys
import os

# Import our generators
from arena_generator import ArenaGenerator
from weapon_generator import WeaponGenerator, PickupGenerator
import json


def generate_all_assets():
    """Generate all procedural assets"""
    print("=" * 60)
    print("Quake3Arena Procedural Asset Generator")
    print("=" * 60)
    
    success_count = 0
    total_count = 3
    
    # 1. Generate arena
    print("\n[1/3] Generating arena geometry...")
    try:
        arena_gen = ArenaGenerator(size=5000.0, height=1000.0)
        arena_gen.generate_arena()
        arena_gen.export_to_json("arena_geometry.json")
        print("✓ Arena generated successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ Failed to generate arena: {e}")
    
    # 2. Generate weapons
    print("\n[2/3] Generating weapon geometry...")
    try:
        weapon_gen = WeaponGenerator()
        weapon_gen.generate_all_weapons()
        weapon_gen.export_to_json("weapons_geometry.json")
        print("✓ Weapons generated successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ Failed to generate weapons: {e}")
    
    # 3. Generate pickups
    print("\n[3/3] Generating pickup geometry...")
    try:
        pickup_data = {
            "version": "1.0",
            "type": "pickups",
            "meshes": []
        }
        
        pickups = [
            PickupGenerator.generate_health_pack(),
            PickupGenerator.generate_armor(),
        ]
        
        for mesh in pickups:
            mesh_data = {
                "name": mesh.name,
                "vertices": [[v.x, v.y, v.z] for v in mesh.vertices],
                "triangles": mesh.triangles,
                "uvs": mesh.uvs
            }
            pickup_data["meshes"].append(mesh_data)
        
        with open("pickups_geometry.json", 'w') as f:
            json.dump(pickup_data, f, indent=2)
        
        print("✓ Pickups generated successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ Failed to generate pickups: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Generation Complete: {success_count}/{total_count} successful")
    print("=" * 60)
    
    # List generated files
    print("\nGenerated files:")
    files = [
        "arena_geometry.json",
        "weapons_geometry.json", 
        "pickups_geometry.json"
    ]
    
    for filename in files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  ✓ {filename} ({size:,} bytes)")
        else:
            print(f"  ✗ {filename} (missing)")
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Copy JSON files to Unreal Engine content directory")
    print("2. Use ArenaGeometryImporter to load geometry in-game")
    print("3. Assign materials to imported meshes")
    print("=" * 60)
    
    return success_count == total_count


if __name__ == "__main__":
    success = generate_all_assets()
    sys.exit(0 if success else 1)
