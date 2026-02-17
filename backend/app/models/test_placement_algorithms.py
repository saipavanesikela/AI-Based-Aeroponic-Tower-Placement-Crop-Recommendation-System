import time
from app.models.greedy_placement import optimize_tower_placement
import math


def valid_layout(positions, farm_length, farm_width, min_spacing):
    # all inside bounds
    for x, y in positions:
        if x < min_spacing/2.0 - 1e-6 or x > farm_width - min_spacing/2.0 + 1e-6:
            return False
        if y < min_spacing/2.0 - 1e-6 or y > farm_length - min_spacing/2.0 + 1e-6:
            return False
    # spacing
    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            if math.dist(positions[i], positions[j]) < min_spacing - 1e-6:
                return False
    return True


def test_algorithms_return_valid_layouts(tmp_path):
    farm_length = 10.0
    farm_width = 6.0
    min_spacing = 1.0
    max_towers = 100

    results = {}

    # hex lattice (deterministic)
    t0 = time.time()
    hex_positions = optimize_tower_placement(farm_length, farm_width, min_spacing, max_towers, method='hex')
    t_hex = time.time() - t0
    assert isinstance(hex_positions, list)
    assert valid_layout(hex_positions, farm_length, farm_width, min_spacing)
    results['hex'] = (len(hex_positions), t_hex)

    # simulated annealing
    t0 = time.time()
    sa_positions = optimize_tower_placement(farm_length, farm_width, min_spacing, max_towers, method='sa', sa_time_limit=1.0)
    t_sa = time.time() - t0
    assert isinstance(sa_positions, list)
    assert valid_layout(sa_positions, farm_length, farm_width, min_spacing)
    results['sa'] = (len(sa_positions), t_sa)

    # genetic algorithm
    t0 = time.time()
    ga_positions = optimize_tower_placement(farm_length, farm_width, min_spacing, max_towers, method='ga', ga_pop_size=40, ga_generations=100, ga_time_limit=1.5)
    t_ga = time.time() - t0
    assert isinstance(ga_positions, list)
    assert valid_layout(ga_positions, farm_length, farm_width, min_spacing)
    results['ga'] = (len(ga_positions), t_ga)

    # write brief benchmark summary
    out = tmp_path / "placement_benchmark.txt"
    with open(out, 'w') as f:
        for k, v in results.items():
            f.write(f"{k}: count={v[0]}, time={v[1]:.3f}s\n")

    # basic sanity: ensure counts are non-zero and not exceeding theoretical max
    assert results['hex'][0] > 0
    assert results['sa'][0] > 0
    assert results['ga'][0] > 0
    assert results['hex'][0] <= max_towers
    assert results['sa'][0] <= max_towers
    assert results['ga'][0] <= max_towers
