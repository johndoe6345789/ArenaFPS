#!/usr/bin/env python3
"""
Procedural weapon generator for Arena FPS
Generates simple weapon meshes that can be imported into Unreal Engine
"""

import json
import math
from typing import List, Tuple
from dataclasses import dataclass

from arena_generator import Vector3, Mesh


class WeaponGenerator:
    """
    Generates procedural weapon meshes
    Simple geometric representations for Arena FPS weapons
    """
    
    def __init__(self):
        self.meshes: List[Mesh] = []
    
    def generate_rocket_launcher(self) -> Mesh:
        """Generate a simple rocket launcher mesh"""
        vertices = []
        
        # Main tube (simplified cylinder)
        length = 100.0
        radius = 10.0
        segments = 8
        
        # Front circle
        for i in range(segments):
            angle = (2 * math.pi * i) / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append(Vector3(x, y, 0))
        
        # Back circle
        for i in range(segments):
            angle = (2 * math.pi * i) / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append(Vector3(x, y, length))
        
        # Create triangles
        triangles = []
        for i in range(segments):
            next_i = (i + 1) % segments
            # Side faces
            triangles.append((i, next_i, segments + i))
            triangles.append((next_i, segments + next_i, segments + i))
        
        # Front cap (center point)
        center_front = len(vertices)
        vertices.append(Vector3(0, 0, 0))
        for i in range(segments):
            next_i = (i + 1) % segments
            triangles.append((center_front, next_i, i))
        
        # Back cap
        center_back = len(vertices)
        vertices.append(Vector3(0, 0, length))
        for i in range(segments):
            next_i = (i + 1) % segments
            triangles.append((center_back, segments + i, segments + next_i))
        
        uvs = [(0, 0)] * len(vertices)
        
        return Mesh(
            name="Weapon_RocketLauncher",
            vertices=vertices,
            triangles=triangles,
            uvs=uvs
        )
    
    def generate_railgun(self) -> Mesh:
        """Generate a simple railgun mesh"""
        # Railgun as a long thin cylinder
        vertices = []
        length = 150.0
        radius = 5.0
        segments = 6
        
        for i in range(segments):
            angle = (2 * math.pi * i) / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append(Vector3(x, y, 0))
        
        for i in range(segments):
            angle = (2 * math.pi * i) / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append(Vector3(x, y, length))
        
        triangles = []
        for i in range(segments):
            next_i = (i + 1) % segments
            triangles.append((i, next_i, segments + i))
            triangles.append((next_i, segments + next_i, segments + i))
        
        uvs = [(0, 0)] * len(vertices)
        
        return Mesh(
            name="Weapon_Railgun",
            vertices=vertices,
            triangles=triangles,
            uvs=uvs
        )
    
    def generate_all_weapons(self) -> List[Mesh]:
        """Generate all weapon meshes"""
        self.meshes = [
            self.generate_rocket_launcher(),
            self.generate_railgun(),
        ]
        return self.meshes
    
    def export_to_json(self, filename: str):
        """Export weapons to JSON"""
        data = {
            "version": "1.0",
            "type": "weapons",
            "meshes": []
        }
        
        for mesh in self.meshes:
            mesh_data = {
                "name": mesh.name,
                "vertices": [[v.x, v.y, v.z] for v in mesh.vertices],
                "triangles": mesh.triangles,
                "uvs": mesh.uvs
            }
            data["meshes"].append(mesh_data)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Exported {len(self.meshes)} weapons to {filename}")


@dataclass
class PickupGenerator:
    """Generates pickup item meshes (health, armor, ammo)"""
    
    @staticmethod
    def generate_health_pack() -> Mesh:
        """Generate a health pack (simple cross shape)"""
        size = 30.0
        thickness = 5.0
        
        # Simple box representing a health pack
        vertices = [
            Vector3(-size, -thickness, 0),
            Vector3(size, -thickness, 0),
            Vector3(size, thickness, 0),
            Vector3(-size, thickness, 0),
            Vector3(-size, -thickness, size * 0.5),
            Vector3(size, -thickness, size * 0.5),
            Vector3(size, thickness, size * 0.5),
            Vector3(-size, thickness, size * 0.5),
        ]
        
        triangles = [
            (0, 1, 2), (0, 2, 3),
            (4, 6, 5), (4, 7, 6),
            (0, 4, 5), (0, 5, 1),
            (1, 5, 6), (1, 6, 2),
            (2, 6, 7), (2, 7, 3),
            (3, 7, 4), (3, 4, 0),
        ]
        
        uvs = [(0, 0)] * len(vertices)
        
        return Mesh(
            name="Pickup_Health",
            vertices=vertices,
            triangles=triangles,
            uvs=uvs
        )
    
    @staticmethod
    def generate_armor() -> Mesh:
        """Generate an armor shard"""
        size = 20.0
        
        # Triangle-based armor shard
        vertices = [
            Vector3(-size, 0, 0),
            Vector3(size, 0, 0),
            Vector3(0, 0, size * 1.5),
            Vector3(0, size * 0.3, size * 0.75),
        ]
        
        triangles = [
            (0, 1, 2),
            (0, 2, 3),
            (1, 0, 3),
            (2, 1, 3),
        ]
        
        uvs = [(0, 0)] * len(vertices)
        
        return Mesh(
            name="Pickup_Armor",
            vertices=vertices,
            triangles=triangles,
            uvs=uvs
        )


def main():
    """Generate weapons and pickups"""
    print("Generating procedural weapons...")
    weapon_gen = WeaponGenerator()
    weapon_gen.generate_all_weapons()
    weapon_gen.export_to_json("weapons_geometry.json")
    
    print("\nGenerated weapons:")
    for mesh in weapon_gen.meshes:
        print(f"  - {mesh.name}: {len(mesh.vertices)} vertices, {len(mesh.triangles)} triangles")
    
    print("\nGenerating procedural pickups...")
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
    
    print(f"Exported {len(pickups)} pickups to pickups_geometry.json")
    print("\nGenerated pickups:")
    for mesh in pickups:
        print(f"  - {mesh.name}: {len(mesh.vertices)} vertices, {len(mesh.triangles)} triangles")


if __name__ == "__main__":
    main()
