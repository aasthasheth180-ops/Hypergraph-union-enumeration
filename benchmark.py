import time
from naive_hash import generate_unions_hash
from efficient_enumeration import generate_unions_backtracking


def run_test(name, V, input_sets):
    print("=" * 70)
    print(f"TEST: {name}")
    print("=" * 70)

    print("\nInput sets:")
    for i, s in enumerate(input_sets, start=1):
        print(f"S{i} = {sorted(s)}")

    print("\nBase set V:")
    print(V)

    start = time.perf_counter()
    # Naive Hash-Set Approach
    naive_unions, candidate_checks = generate_unions_hash(input_sets)
    naive_time = time.perf_counter() - start

    start = time.perf_counter()
    # Backtracking Approach
    backtracking_unions, extension_checks, pruned_branches = (
        generate_unions_backtracking(V, input_sets)
    )
    backtracking_time = time.perf_counter() - start

    naive_set = set(naive_unions)
    backtracking_set = set(backtracking_unions)

    # -------------------------
    # Correctness Check
    # -------------------------
    same_output = naive_set == backtracking_set

    print("\nResults:")
    print(f"{'Metric':<30} {'Naive':<15} {'Backtracking':<15}")
    print("-" * 60)
    print(
        f"{'Distinct unions':<30} "
        f"{len(naive_unions):<15} "
        f"{len(backtracking_unions):<15}"
    )
    print(
        f"{'Candidate union checks':<30} "
        f"{candidate_checks:<15} "
        f"{'-':<15}"
    )
    print(
        f"{'Extension checks':<30} "
        f"{'-':<15} "
        f"{extension_checks:<15}"
    )
    print(
        f"{'Pruned branches':<30} "
        f"{'-':<15} "
        f"{pruned_branches:<15}"
    )
    print(
        f"{'Runtime (seconds)':<30} "
        f"{naive_time:<15.8f} "
        f"{backtracking_time:<15.8f}"
    )

    print("\nCorrectness:")
    print("Both algorithms produced same unions:", same_output)

    print("\nDistinct unions:")
    for union in sorted(
        naive_unions,
        key=lambda x: (len(x), sorted(x))
    ):
        print(sorted(union))

    print()


if __name__ == "__main__":

    # ============================================================
    # TEST 1
    # Basic overlapping example
    # ============================================================

    V1 = ["A", "B", "C", "D"]

    input_sets_1 = [
        {"A", "B"},
        {"B", "C"},
        {"C", "D"},
    ]

    run_test(
        "Basic Overlapping Sets",
        V1,
        input_sets_1
    )

    # ============================================================
    # TEST 2
    # Many duplicate-producing input sets
    # ============================================================

    V2 = ["A", "B"]

    input_sets_2 = [
        {"A"},
        {"B"},
        {"A", "B"},
        {"A", "B"},
        {"A", "B"},
        {"A", "B"},
    ]

    run_test(
        "Duplicate-Heavy Input",
        V2,
        input_sets_2
    )

    # ============================================================
    # TEST 3
    # Nested sets
    # ============================================================

    V3 = ["A", "B", "C", "D", "E", "F", "G", "H"]

    input_sets_3 = [
        {"A"},
        {"A", "B"},
        {"A", "B", "C"},
        {"A", "B", "C", "D"},
        {"A", "B", "C", "D", "E"},
        {"A", "B", "C", "D", "E", "F"},
        {"A", "B", "C", "D", "E", "F", "G"},
        {"A", "B", "C", "D", "E", "F", "G", "H"},
    ]

    run_test(
        "Nested Sets",
        V3,
        input_sets_3
    )

    # ============================================================
    # TEST 4
    # Disjoint sets
    # ============================================================

    V4 = ["A", "B", "C", "D"]

    input_sets_4 = [
        {"A"},
        {"B"},
        {"C"},
        {"D"},
    ]

    run_test(
        "Disjoint Sets",
        V4,
        input_sets_4
    )