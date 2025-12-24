#!/usr/bin/env python3
"""
Procedural Arena Generator for Quake 3 Arena clone
Generates arena geometry using code that can be unit tested
Uses simple geometric primitives that can be exported to FBX/OBJ
"""

import json
import math
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict


@dataclass
class Vector3:
    """3D Vector representation"""
    x: float
    y: float
    z: float


@dataclass
class Mesh:
    """Simple mesh representation"""
    name: str
    vertices: List[Vector3]
    triangles: List[Tuple[int, int, int]]  # Indices into vertices
    uvs: List[Tuple[float, float]]


class ArenaGenerator:
    """
    Generates a Quake 3 style arena level procedurally
    This is a simplified version that generates platform layouts
    """
    
    def __init__(self, size: float = 5000.0, height: float = 1000.0):
        self.size = size  # Arena size in UE units (cm)
        self.height = height
        self.meshes: List[Mesh] = []
        
    def generate_arena(self) -> List[Mesh]:
        """Generate a complete arena with platforms and walkways"""
        self.meshes = []
        
        # Generate main floor
        self.generate_floor()
        
        # Generate walls
        self.generate_walls()
        
        # Generate platforms (like Q3DM17 "The Longest Yard")
        self.generate_platforms()
        
        # Generate jump pads
        self.generate_jump_pads()
        
        return self.meshes
    
    def generate_floor(self):
        """Generate the main floor plane"""
        half_size = self.size / 2
        thickness = 50.0
        
        vertices = [
            Vector3(-half_size, -half_size, 0),
            Vector3(half_size, -half_size, 0),
            Vector3(half_size, half_size, 0),
            Vector3(-half_size, half_size, 0),
            Vector3(-half_size, -half_size, -thickness),
            Vector3(half_size, -half_size, -thickness),
            Vector3(half_size, half_size, -thickness),
            Vector3(-half_size, half_size, -thickness),
        ]
        
        # Create quads (as two triangles each)
        triangles = [
            # Top face
            (0, 1, 2), (0, 2, 3),
            # Bottom face
            (4, 6, 5), (4, 7, 6),
            # Sides
            (0, 4, 5), (0, 5, 1),
            (1, 5, 6), (1, 6, 2),
            (2, 6, 7), (2, 7, 3),
            (3, 7, 4), (3, 4, 0),
        ]
        
        uvs = [(0, 0), (1, 0), (1, 1), (0, 1)] * 2
        
        mesh = Mesh(
            name="Arena_Floor",
            vertices=vertices,
            triangles=triangles,
            uvs=uvs
        )
        self.meshes.append(mesh)
    
    def generate_walls(self):
        """Generate perimeter walls"""
        half_size = self.size / 2
        wall_thickness = 100.0
        wall_height = self.height
        
        # Four walls (simplified as boxes)
        walls = [
            ("Arena_Wall_North", -half_size, half_size, half_size, half_size + wall_thickness),
            ("Arena_Wall_South", -half_size, -half_size - wall_thickness, half_size, -half_size),
            ("Arena_Wall_East", half_size, -half_size, half_size + wall_thickness, half_size),
            ("Arena_Wall_West", -half_size - wall_thickness, -half_size, -half_size, half_size),
        ]
        
        for wall_name, x_min, y_min, x_max, y_max in walls:
            vertices = [
                Vector3(x_min, y_min, 0),
                Vector3(x_max, y_min, 0),
                Vector3(x_max, y_max, 0),
                Vector3(x_min, y_max, 0),
                Vector3(x_min, y_min, wall_height),
                Vector3(x_max, y_min, wall_height),
                Vector3(x_max, y_max, wall_height),
                Vector3(x_min, y_max, wall_height),
            ]
            
            triangles = [
                (0, 1, 2), (0, 2, 3),
                (4, 6, 5), (4, 7, 6),
                (0, 4, 5), (0, 5, 1),
                (1, 5, 6), (1, 6, 2),
                (2, 6, 7), (2, 7, 3),
                (3, 7, 4), (3, 4, 0),
            ]
            
            uvs = [(0, 0), (1, 0), (1, 1), (0, 1)] * 2
            
            mesh = Mesh(name=wall_name, vertices=vertices, triangles=triangles, uvs=uvs)
            self.meshes.append(mesh)
    
    def generate_platforms(self):
        """Generate floating platforms (Q3DM17 style)"""
        platform_configs = [
            # Central platform
            (0, 0, 300, 800, 800, 100),
            # Corner platforms
            (1500, 1500, 200, 600, 600, 100),
            (-1500, 1500, 200, 600, 600, 100),
            (1500, -1500, 200, 600, 600, 100),
            (-1500, -1500, 200, 600, 600, 100),
        ]
        
        for idx, (x, y, z, width, depth, height) in enumerate(platform_configs):
            vertices = self._create_box_vertices(x, y, z, width, depth, height)
            triangles = self._create_box_triangles()
            uvs = [(0, 0), (1, 0), (1, 1), (0, 1)] * 2
            
            mesh = Mesh(
                name=f"Arena_Platform_{idx}",
                vertices=vertices,
                triangles=triangles,
                uvs=uvs
            )
            self.meshes.append(mesh)
    
    def generate_jump_pads(self):
        """Generate jump pad positions (as simple cylinders)"""
        jump_pad_positions = [
            (0, 1500, 0),
            (0, -1500, 0),
            (1500, 0, 0),
            (-1500, 0, 0),
        ]
        
        for idx, (x, y, z) in enumerate(jump_pad_positions):
            vertices = self._create_cylinder_vertices(x, y, z, 200, 50, 8)
            triangles = self._create_cylinder_triangles(8)
            uvs = [(0, 0)] * len(vertices)
            
            mesh = Mesh(
                name=f"Arena_JumpPad_{idx}",
                vertices=vertices,
                triangles=triangles,
                uvs=uvs
            )
            self.meshes.append(mesh)
    
    def _create_box_vertices(self, x: float, y: float, z: float, 
                            width: float, depth: float, height: float) -> List[Vector3]:
        """Create vertices for a box"""
        hw, hd, hh = width / 2, depth / 2, height / 2
        return [
            Vector3(x - hw, y - hd, z - hh),
            Vector3(x + hw, y - hd, z - hh),
            Vector3(x + hw, y + hd, z - hh),
            Vector3(x - hw, y + hd, z - hh),
            Vector3(x - hw, y - hd, z + hh),
            Vector3(x + hw, y - hd, z + hh),
            Vector3(x + hw, y + hd, z + hh),
            Vector3(x - hw, y + hd, z + hh),
        ]
    
    def _create_box_triangles(self) -> List[Tuple[int, int, int]]:
        """Create triangle indices for a box"""
        return [
            (0, 1, 2), (0, 2, 3),
            (4, 6, 5), (4, 7, 6),
            (0, 4, 5), (0, 5, 1),
            (1, 5, 6), (1, 6, 2),
            (2, 6, 7), (2, 7, 3),
            (3, 7, 4), (3, 4, 0),
        ]
    
    def _create_cylinder_vertices(self, x: float, y: float, z: float,
                                  radius: float, height: float, segments: int) -> List[Vector3]:
        """Create vertices for a cylinder"""
        vertices = []
        
        # Bottom circle
        for i in range(segments):
            angle = (2 * math.pi * i) / segments
            vx = x + radius * math.cos(angle)
            vy = y + radius * math.sin(angle)
            vertices.append(Vector3(vx, vy, z))
        
        # Top circle
        for i in range(segments):
            angle = (2 * math.pi * i) / segments
            vx = x + radius * math.cos(angle)
            vy = y + radius * math.sin(angle)
            vertices.append(Vector3(vx, vy, z + height))
        
        # Center points
        vertices.append(Vector3(x, y, z))  # Bottom center
        vertices.append(Vector3(x, y, z + height))  # Top center
        
        return vertices
    
    def _create_cylinder_triangles(self, segments: int) -> List[Tuple[int, int, int]]:
        """Create triangle indices for a cylinder"""
        triangles = []
        
        # Side faces
        for i in range(segments):
            next_i = (i + 1) % segments
            triangles.append((i, next_i, segments + i))
            triangles.append((next_i, segments + next_i, segments + i))
        
        # Bottom cap
        bottom_center = segments * 2
        for i in range(segments):
            next_i = (i + 1) % segments
            triangles.append((bottom_center, next_i, i))
        
        # Top cap
        top_center = segments * 2 + 1
        for i in range(segments):
            next_i = (i + 1) % segments
            triangles.append((top_center, segments + i, segments + next_i))
        
        return triangles
    
    def export_to_json(self, filename: str):
        """Export the arena data to JSON format"""
        data = {
            "version": "1.0",
            "arena_size": self.size,
            "arena_height": self.height,
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
        
        print(f"Exported arena to {filename}")
        print(f"Generated {len(self.meshes)} meshes")


def main():
    """Generate a Quake 3 style arena"""
    generator = ArenaGenerator(size=5000.0, height=1000.0)
    generator.generate_arena()
    generator.export_to_json("arena_geometry.json")
    
    print("\nGenerated meshes:")
    for mesh in generator.meshes:
        print(f"  - {mesh.name}: {len(mesh.vertices)} vertices, {len(mesh.triangles)} triangles")


if __name__ == "__main__":
    main()
