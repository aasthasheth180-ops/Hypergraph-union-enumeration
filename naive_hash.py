from collections  import deque

def generate_unions_hash(input_sets):
    """
    Original approach:
    Generate union from perviously discovered unions
    and use a hash set to avoid storing duplicates.
    """
    empty = frozenset()

    seen = {empty}
    queue = deque([empty])

    candidate_check = 0

    while queue:
        current = queue.popleft()

        for s in input_sets:
            candidate_check += 1
            new_union = current | frozenset(s)

            if new_union not in seen:
                seen.add(new_union)
                queue.append(new_union)

    return seen, candidate_check

if __name__ == "__main__":
    input_sets = [
        {"A"},
        {"A", "B"},
        {"A", "B","C"},
        {"A", "B","C","D"},
        {"A", "B","C","D","E"},
        {"A", "B","C","D","E","F"},
        {"A", "B","C","D","E","F","G"},
        {"A", "B","C","D","E","F","G","H"}
    ]
    

    unions, checks = generate_unions_hash(input_sets)

    print("Distinct unions:")
    for u in sorted(unions, key=lambda x: (len(x), sorted(x))):
        print(set(u))

    print()
    print("Number of distinct unions:", len(unions))
    print("Candidate checks performed:", checks)
    