import pytest
from app.services import optimization_service

def test_greedy_tower_placement_basic():
    positions = optimization_service.greedy_tower_placement(10, 10, 2, 5)
    assert isinstance(positions, list)
    assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in positions)
    assert len(positions) <= 5

def test_generate_placement_image(tmp_path):
    positions = [(1, 1), (3, 3), (5, 5)]
    output_path = tmp_path / "test_image.png"
    # Should not raise
    optimization_service.generate_placement_image(positions, 10, 10, 2, str(output_path))
    assert output_path.exists()

def test_optimize_tower_placement():
    result = optimization_service.optimize_tower_placement(10, 10, 2, 5)
    assert isinstance(result, dict)
    assert "total_towers" in result
    assert "tower_positions" in result
    assert "image_path" in result
    assert result["total_towers"] <= 5
    assert isinstance(result["tower_positions"], list)
    assert isinstance(result["image_path"], str)
