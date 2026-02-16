from app.services import optimization_service
import os

def test_greedy():
    positions = optimization_service.greedy_tower_placement(10,10,2,5)
    print('greedy positions:', positions)
    assert isinstance(positions, list)
    assert all(isinstance(pos, tuple) and len(pos)==2 for pos in positions)
    assert len(positions) <= 5

def test_generate_image():
    positions = [(1,1),(3,3),(5,5)]
    out = os.path.join('app','data','test_image.png')
    optimization_service.generate_placement_image(positions,10,10,2,out)
    print('image generated at', out)
    assert os.path.exists(out)

def test_optimize():
    res = optimization_service.optimize_tower_placement(10,10,2,5)
    print('optimize result keys:', res.keys())
    assert isinstance(res, dict)
    assert 'total_towers' in res

if __name__=='__main__':
    test_greedy()
    test_generate_image()
    test_optimize()
    print('Unit checks passed')
