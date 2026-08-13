def can_extend(required, forbidden,input_sets):
    """
    Return True if the current partial assignment can still
    be extended to at least one valid union.
    """
    possible_union = set()

    for s in input_sets:

        # A set containing a forbidden element cannot be used.

        if not s.isdisjoint(forbidden):
            continue

        # add elements from usable sets
        possible_union.update(s)


    #Every required element must be obtainable.

    return required.issubset(possible_union)

def generate_unions_backtracking(V,input_sets):
    """
    Generate all the distinct unions using backtracking
    and extension tests.
    """
    results = []

    # Counters so we can later compare with the naive algorithm

    extension_check = 0
    pruned_branches = 0


    def backtrack(index, required, forbidden):
        nonlocal extension_check, pruned_branches

        # ----------------------
        # 1. Run the extension test
        # ----------------------

        extension_check += 1

        if not can_extend(required, forbidden, input_sets):
            pruned_branches += 1
            return

        # ----------------------
        # 2. Have we decided every element?
        # ----------------------
        if index == len(V):
            results.append(frozenset(required))
            return

        element = V[index]

        # ----------------------
        # 3. Branch 0:
        #     element is forbidden
        # ----------------------

        backtrack(
            index + 1,
            required,
            forbidden | {element}
        )

        # ----------------------
        # 4. Branch 1:
        #     element is required
        # ----------------------

        backtrack(
            index + 1,
            required | {element},
            forbidden
        )

        # Start at ????
    backtrack(0, set(), set())

    return results, extension_check, pruned_branches

#--------------------
# Test
#----------------------

if __name__ == "__main__":
    V = ["A", "B", "C", "D", "E", "F", "G", "H"]

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

    unions, checks, pruned = generate_unions_backtracking(V,input_sets)

    print("Distinct unions:")

    for u in sorted(unions, key=lambda x: (len(x), sorted(x))):
        print(sorted(u))

    print()
    print("Number of distinct unions:", len(unions))
    print("Extension checks:",checks)
    print("Pruned branches:", pruned)