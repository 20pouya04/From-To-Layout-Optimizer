"""
From-To Chart Layout Optimizer
================================

Solves a small facility-layout problem using a From-To chart (a matrix that
records the flow / traffic intensity between pairs of locations, e.g.
departments in a factory or workstations on a shop floor).

The script brute-forces every possible ordering (permutation) of the given
locations and scores each ordering with a simple distance-weighted cost
function:

    - Moving material "forward" (from an earlier location to a later one)
      costs 1 unit of penalty per position skipped.
    - Moving material "backward" (from a later location to an earlier one)
      costs 2 units of penalty per position skipped, since backward flows
      are typically more expensive/disruptive in real layouts (e.g. they
      cross the forward flow of other material).

The permutation that minimizes total weighted flow cost is reported as the
best layout ordering.

Usage
-----
Run directly to reproduce the example in the accompanying notebook:

    python from_to_layout_optimizer.py

Or import the functions to use your own From-To matrix:

    from from_to_layout_optimizer import calculate_total_value, find_best_layout
    best_order, best_cost, all_results = find_best_layout(my_dataframe)
"""

from itertools import permutations

import pandas as pd


def build_example_from_to_table() -> pd.DataFrame:
    """Return the example 5-location From-To chart used in the notebook."""
    locations = ["A", "B", "C", "D", "E"]
    from_to = pd.DataFrame(0, index=locations, columns=locations)

    from_to.loc["A", "B"] = 22
    from_to.loc["A", "C"] = 55
    from_to.loc["A", "D"] = 0
    from_to.loc["A", "E"] = 0
    from_to.loc["B", "A"] = 10
    from_to.loc["B", "C"] = 0
    from_to.loc["B", "D"] = 62
    from_to.loc["B", "E"] = 5
    from_to.loc["C", "A"] = 0
    from_to.loc["C", "B"] = 40
    from_to.loc["C", "D"] = 5
    from_to.loc["C", "E"] = 10
    from_to.loc["D", "A"] = 0
    from_to.loc["D", "B"] = 5
    from_to.loc["D", "C"] = 0
    from_to.loc["D", "E"] = 62
    from_to.loc["E", "A"] = 0
    from_to.loc["E", "B"] = 0
    from_to.loc["E", "C"] = 0
    from_to.loc["E", "D"] = 10

    return from_to


def calculate_total_value(matrix: pd.DataFrame) -> float:
    """
    Compute the weighted flow cost of a given location ordering.

    Forward flows (i < j) are weighted by the distance (j - i).
    Backward flows (i > j) are weighted by twice the distance (2 * (i - j)).
    Diagonal entries (i == j) are ignored.
    """
    total_value = 0
    n = len(matrix)

    for i in range(n):
        for j in range(n):
            if i < j:
                coefficient = j - i
            elif i > j:
                coefficient = 2 * (i - j)
            else:
                coefficient = 0

            total_value += coefficient * matrix.iloc[i, j]

    return total_value


def find_best_layout(from_to: pd.DataFrame):
    """
    Try every permutation of the locations in `from_to` and return the
    ordering with the lowest total weighted flow cost.

    Returns
    -------
    best_permutation : tuple
        The best-found ordering of location labels.
    best_value : float
        The total weighted flow cost of that ordering.
    results : list[tuple[tuple, float]]
        The (permutation, cost) pair for every permutation that was tried.
    """
    locations = list(from_to.index)
    best_value = float("inf")
    best_permutation = None
    results = []

    for perm in permutations(locations):
        permuted_table = from_to.loc[list(perm), list(perm)]
        current_value = calculate_total_value(permuted_table)
        results.append((perm, current_value))

        if current_value < best_value:
            best_value = current_value
            best_permutation = perm

    return best_permutation, best_value, results


def main():
    pd.set_option("display.max_columns", None)
    pd.set_option("display.expand_frame_repr", False)
    pd.set_option("display.max_rows", None)

    from_to = build_example_from_to_table()

    print("Original From-To Table:")
    print(from_to)
    print()

    best_permutation, best_value, results = find_best_layout(from_to)

    for perm, value in results:
        print(f"Permutation: {perm}, Total Value: {value}")

    print("\nBest Permutation:", best_permutation)
    print("Lowest Total Value:", best_value)

    best_from_to_table = from_to.loc[list(best_permutation), list(best_permutation)]
    print("\nFrom-To Table with Lowest Total Value:")
    print(best_from_to_table)


if __name__ == "__main__":
    main()
