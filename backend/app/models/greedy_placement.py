from typing import List, Tuple
import math
import random
import time


def is_valid(point, placed, min_dist):
    """Check minimum spacing constraint"""
    for p in placed:
        if math.dist(point, p) < min_dist:
            return False
    return True


def optimize_tower_placement(
    farm_length: float,
    farm_width: float,
    min_spacing: float,
    max_towers: int,
    method: str = "ga",
    # GA parameters
    ga_pop_size: int = 60,
    ga_generations: int = 200,
    ga_time_limit: float = 2.0,
    # SA parameters
    sa_time_limit: float = 2.0,
    sa_max_iters: int = 5000,
) -> List[Tuple[float, float]]:
    """
    Optimized placement using a hexagonal (close) packing lattice.

    Hexagonal packing yields higher density than a square grid while
    respecting the minimum center-to-center spacing constraint. This
    implementation generates a hex lattice clipped to the farm boundary
    and stops when `max_towers` is reached.
    """

    if farm_length <= 0 or farm_width <= 0:
        raise ValueError("Invalid farm dimensions")

    if min_spacing <= 0:
        raise ValueError("Minimum spacing must be positive")

    if farm_length <= 0 or farm_width <= 0:
        raise ValueError("Invalid farm dimensions")

    # Helper: generate initial hex-lattice solution
    def hex_lattice() -> List[Tuple[float, float]]:
        s = min_spacing
        row_spacing = s * math.sqrt(3) / 2
        row = 0
        y = s / 2.0
        placed: List[Tuple[float, float]] = []
        while y <= farm_length - s / 2.0:
            x_offset = (s / 2.0) if (row % 2 == 1) else 0.0
            x = s / 2.0 + x_offset
            while x <= farm_width - s / 2.0:
                candidate = (round(x, 2), round(y, 2))
                if is_valid(candidate, placed, s):
                    placed.append(candidate)
                    if len(placed) >= max_towers:
                        return placed
                x += s
            row += 1
            y += row_spacing
        return placed

    # Simulated annealing local improvement to try to increase tower count
    def simulated_annealing(initial: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        start_time = time.time()
        best = list(initial)
        best_score = len(best)

        # state is a list of positions
        state = list(initial)
        score = len(state)

        T = 1.0
        Tmin = 1e-3
        alpha = 0.995
        iters = 0
        max_iters = 5000

        def random_point():
            x = random.uniform(min_spacing / 2.0, farm_width - min_spacing / 2.0)
            y = random.uniform(min_spacing / 2.0, farm_length - min_spacing / 2.0)
            return (round(x, 2), round(y, 2))

        while T > Tmin and iters < max_iters and (time.time() - start_time) < 2.0:
            iters += 1
            # propose a neighbor: add / move / remove
            choice = random.random()
            new_state = list(state)

            if choice < 0.5:
                # try to add a random point
                p = random_point()
                if is_valid(p, new_state, min_spacing):
                    new_state.append(p)
                else:
                    # try replacing conflicting neighbors (if it yields net gain)
                    conflicts = [i for i, q in enumerate(new_state) if math.dist(p, q) < min_spacing]
                    if len(conflicts) > 0 and len(conflicts) < 2:
                        # remove small number of conflicts and add p
                        for idx in sorted(conflicts, reverse=True):
                            new_state.pop(idx)
                        new_state.append(p)
            elif choice < 0.8 and len(new_state) > 0:
                # move a random tower slightly
                idx = random.randrange(len(new_state))
                old = new_state[idx]
                nx = max(min_spacing / 2.0, min(farm_width - min_spacing / 2.0, old[0] + random.uniform(-min_spacing / 4.0, min_spacing / 4.0)))
                ny = max(min_spacing / 2.0, min(farm_length - min_spacing / 2.0, old[1] + random.uniform(-min_spacing / 4.0, min_spacing / 4.0)))
                candidate = (round(nx, 2), round(ny, 2))
                # remove old and check validity
                tmp = new_state[:idx] + new_state[idx+1:]
                if is_valid(candidate, tmp, min_spacing):
                    new_state[idx] = candidate
            else:
                # remove a random tower to allow denser re-placement
                if len(new_state) > 0:
                    idx = random.randrange(len(new_state))
                    new_state.pop(idx)

            # enforce bounds and uniqueness
            uniq = []
            for p in new_state:
                if p not in uniq:
                    uniq.append(p)
            new_state = uniq

            new_score = len(new_state)

            # acceptance
            if new_score > score:
                state = new_state
                score = new_score
                if score > best_score:
                    best = list(state)
                    best_score = score
            else:
                # accept worse with probability
                delta = new_score - score
                prob = math.exp(delta / T) if T > 0 else 0
                if random.random() < prob:
                    state = new_state
                    score = new_score

            T *= alpha

            # early stop if reached max_towers
            if best_score >= max_towers:
                return best[:max_towers]

        return best

    # Genetic algorithm: operate on an ordering of candidate points (indices into pool)
    def genetic_optimize(candidates: List[Tuple[float, float]],
                         pop_size: int = 50,
                         generations: int = 200,
                         time_limit: float = 2.0) -> List[Tuple[float, float]]:
        start = time.time()

        # decode a chromosome (ordering) into feasible placement via greedy scan
        def decode(order: List[int]) -> List[Tuple[float, float]]:
            placed: List[Tuple[float, float]] = []
            for idx in order:
                p = candidates[idx]
                if is_valid(p, placed, min_spacing):
                    placed.append(p)
                    if len(placed) >= max_towers:
                        break
            return placed

        # fitness = number of placed towers (higher is better)
        def fitness(order: List[int]) -> int:
            return len(decode(order))

        # population: list of permutations (represented as lists of indices)
        n = len(candidates)
        base_order = list(range(n))
        population: List[List[int]] = []

        # seed population: some seeded with natural order, some shuffled
        population.append(base_order[:])
        for _ in range(min(pop_size - 1, 5)):
            population.append(base_order[:])
        while len(population) < pop_size:
            order = base_order[:]
            random.shuffle(order)
            population.append(order)

        best_order = population[0]
        best_score = fitness(best_order)

        generation = 0
        elite_size = max(1, pop_size // 10)
        mutation_rate = 0.2

        while generation < generations and (time.time() - start) < time_limit:
            # evaluate
            scored = [(fitness(o), o) for o in population]
            scored.sort(key=lambda x: x[0], reverse=True)
            if scored[0][0] > best_score:
                best_score, best_order = scored[0][0], scored[0][1][:]
            # early stop if optimal
            if best_score >= max_towers:
                break

            # selection (elitism + tournament)
            new_pop: List[List[int]] = [o[:] for (_, o) in scored[:elite_size]]

            def tournament_select() -> List[int]:
                a = population[random.randrange(pop_size)]
                b = population[random.randrange(pop_size)]
                return a[:] if fitness(a) > fitness(b) else b[:]

            # crossover (ordered crossover)
            while len(new_pop) < pop_size:
                parent1 = tournament_select()
                parent2 = tournament_select()
                # ordered crossover
                i, j = sorted(random.sample(range(n), 2)) if n > 1 else (0, 0)
                child = [-1] * n
                child[i:j+1] = parent1[i:j+1]
                fill_pos = 0
                for gene in parent2:
                    if gene not in child:
                        while child[fill_pos] != -1:
                            fill_pos += 1
                        child[fill_pos] = gene
                # mutation: swap mutation
                if random.random() < mutation_rate:
                    a, b = random.sample(range(n), 2)
                    child[a], child[b] = child[b], child[a]
                new_pop.append(child)

            population = new_pop
            generation += 1

        # return decoded best solution
        return decode(best_order)

    # prepare candidate pool: hex lattice plus a few jittered random points
    candidates = hex_lattice()
    # add jittered variants to increase search space
    for _ in range(max(0, min(50, int((farm_length * farm_width) // (min_spacing ** 2)) - len(candidates)))):
        x = random.uniform(min_spacing / 2.0, farm_width - min_spacing / 2.0)
        y = random.uniform(min_spacing / 2.0, farm_length - min_spacing / 2.0)
        candidates.append((round(x, 2), round(y, 2)))

    # ensure candidate pool is unique
    uniq_candidates: List[Tuple[float, float]] = []
    for c in candidates:
        if c not in uniq_candidates:
            uniq_candidates.append(c)
    candidates = uniq_candidates

    # choose algorithm
    if method == "hex":
        return hex_lattice()
    elif method == "sa":
        initial = hex_lattice()
        return simulated_annealing(initial)
    elif method == "ga":
        result = genetic_optimize(candidates, pop_size=ga_pop_size, generations=ga_generations, time_limit=ga_time_limit)
    else:
        # unknown method: default to GA
        result = genetic_optimize(candidates, pop_size=ga_pop_size, generations=ga_generations, time_limit=ga_time_limit)
    # fallback: if GA returned nothing, use simulated annealing result
    if not result:
        initial = hex_lattice()
        result = simulated_annealing(initial)

    # final cleanup to ensure spacing/order and respect max_towers
    final: List[Tuple[float, float]] = []
    for p in result:
        if is_valid(p, final, min_spacing):
            final.append(p)
            if len(final) >= max_towers:
                break
    return final
