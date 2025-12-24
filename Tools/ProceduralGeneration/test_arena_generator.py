#!/usr/bin/env python3
"""
Unit tests for the procedural arena generator
"""

import unittest
import json
import os
import sys
from arena_generator import ArenaGenerator, Vector3, Mesh


class TestArenaGenerator(unittest.TestCase):
    """Test cases for ArenaGenerator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = ArenaGenerator(size=5000.0, height=1000.0)
    
    def test_initialization(self):
        """Test that generator initializes with correct parameters"""
        self.assertEqual(self.generator.size, 5000.0)
        self.assertEqual(self.generator.height, 1000.0)
        self.assertEqual(len(self.generator.meshes), 0)
    
    def test_generate_arena_creates_meshes(self):
        """Test that generate_arena creates mesh objects"""
        meshes = self.generator.generate_arena()
        self.assertGreater(len(meshes), 0)
        self.assertIsInstance(meshes[0], Mesh)
    
    def test_generate_floor(self):
        """Test floor generation"""
        self.generator.generate_floor()
        self.assertEqual(len(self.generator.meshes), 1)
        
        floor = self.generator.meshes[0]
        self.assertEqual(floor.name, "Arena_Floor")
        self.assertEqual(len(floor.vertices), 8)  # Box has 8 vertices
        self.assertGreater(len(floor.triangles), 0)
    
    def test_generate_walls(self):
        """Test wall generation"""
        self.generator.generate_walls()
        self.assertEqual(len(self.generator.meshes), 4)  # 4 walls
        
        for mesh in self.generator.meshes:
            self.assertTrue(mesh.name.startswith("Arena_Wall_"))
            self.assertEqual(len(mesh.vertices), 8)
    
    def test_generate_platforms(self):
        """Test platform generation"""
        initial_count = len(self.generator.meshes)
        self.generator.generate_platforms()
        
        # Should have created 5 platforms (1 central + 4 corners)
        self.assertEqual(len(self.generator.meshes) - initial_count, 5)
    
    def test_generate_jump_pads(self):
        """Test jump pad generation"""
        initial_count = len(self.generator.meshes)
        self.generator.generate_jump_pads()
        
        # Should have created 4 jump pads
        self.assertEqual(len(self.generator.meshes) - initial_count, 4)
    
    def test_box_vertices(self):
        """Test box vertex generation"""
        vertices = self.generator._create_box_vertices(0, 0, 0, 100, 100, 100)
        self.assertEqual(len(vertices), 8)
        
        # Check that vertices form a proper box
        for v in vertices:
            self.assertIsInstance(v, Vector3)
            self.assertTrue(-50 <= v.x <= 50)
            self.assertTrue(-50 <= v.y <= 50)
            self.assertTrue(-50 <= v.z <= 50)
    
    def test_box_triangles(self):
        """Test box triangle generation"""
        triangles = self.generator._create_box_triangles()
        self.assertEqual(len(triangles), 12)  # 6 faces * 2 triangles
        
        # Check that all triangle indices are valid
        for tri in triangles:
            self.assertEqual(len(tri), 3)
            for idx in tri:
                self.assertTrue(0 <= idx < 8)
    
    def test_cylinder_vertices(self):
        """Test cylinder vertex generation"""
        segments = 8
        vertices = self.generator._create_cylinder_vertices(0, 0, 0, 100, 50, segments)
        expected_count = segments * 2 + 2  # Bottom + Top circles + 2 centers
        self.assertEqual(len(vertices), expected_count)
    
    def test_cylinder_triangles(self):
        """Test cylinder triangle generation"""
        segments = 8
        triangles = self.generator._create_cylinder_triangles(segments)
        
        # Sides + Bottom cap + Top cap
        expected_count = segments * 2 + segments + segments
        self.assertEqual(len(triangles), expected_count)
    
    def test_export_to_json(self):
        """Test JSON export functionality"""
        self.generator.generate_arena()
        
        test_file = "test_arena_output.json"
        try:
            self.generator.export_to_json(test_file)
            self.assertTrue(os.path.exists(test_file))
            
            # Verify JSON structure
            with open(test_file, 'r') as f:
                data = json.load(f)
            
            self.assertIn("version", data)
            self.assertIn("arena_size", data)
            self.assertIn("arena_height", data)
            self.assertIn("meshes", data)
            self.assertEqual(data["arena_size"], 5000.0)
            self.assertGreater(len(data["meshes"]), 0)
            
            # Verify mesh structure
            mesh_data = data["meshes"][0]
            self.assertIn("name", mesh_data)
            self.assertIn("vertices", mesh_data)
            self.assertIn("triangles", mesh_data)
            self.assertIn("uvs", mesh_data)
            
        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)
    
    def test_mesh_integrity(self):
        """Test that generated meshes have valid data"""
        meshes = self.generator.generate_arena()
        
        for mesh in meshes:
            # Check name
            self.assertIsNotNone(mesh.name)
            self.assertGreater(len(mesh.name), 0)
            
            # Check vertices
            self.assertGreater(len(mesh.vertices), 0)
            for v in mesh.vertices:
                self.assertIsInstance(v, Vector3)
            
            # Check triangles
            self.assertGreater(len(mesh.triangles), 0)
            max_vertex_idx = len(mesh.vertices) - 1
            for tri in mesh.triangles:
                self.assertEqual(len(tri), 3)
                for idx in tri:
                    self.assertTrue(0 <= idx <= max_vertex_idx,
                                  f"Triangle index {idx} out of bounds for mesh {mesh.name}")
    
    def test_different_arena_sizes(self):
        """Test generation with different arena sizes"""
        sizes = [1000.0, 5000.0, 10000.0]
        
        for size in sizes:
            gen = ArenaGenerator(size=size, height=1000.0)
            meshes = gen.generate_arena()
            
            self.assertGreater(len(meshes), 0)
            self.assertEqual(gen.size, size)


class TestVector3(unittest.TestCase):
    """Test cases for Vector3"""
    
    def test_creation(self):
        """Test Vector3 creation"""
        v = Vector3(1.0, 2.0, 3.0)
        self.assertEqual(v.x, 1.0)
        self.assertEqual(v.y, 2.0)
        self.assertEqual(v.z, 3.0)


class TestMesh(unittest.TestCase):
    """Test cases for Mesh"""
    
    def test_creation(self):
        """Test Mesh creation"""
        vertices = [Vector3(0, 0, 0), Vector3(1, 0, 0), Vector3(0, 1, 0)]
        triangles = [(0, 1, 2)]
        uvs = [(0, 0), (1, 0), (0, 1)]
        
        mesh = Mesh(name="TestMesh", vertices=vertices, triangles=triangles, uvs=uvs)
        
        self.assertEqual(mesh.name, "TestMesh")
        self.assertEqual(len(mesh.vertices), 3)
        self.assertEqual(len(mesh.triangles), 1)
        self.assertEqual(len(mesh.uvs), 3)


if __name__ == "__main__":
    unittest.main()
