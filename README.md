# Facility Layout Optimization via From-To Chart Analysis

A Python program that evaluates department-arrangement permutations
against a **From-To flow matrix** to identify the layout minimizing total
material-handling cost.

**Status:** Course Project, Facilities Planning (2025)

## Background

The From-To chart is a classic topic from my **Facility Planning** course
(*طرحریزی واحدهای صنعتی*) during university. This repository contains a
script I originally wrote at the time simply to solve a given From-To chart
programmatically, rather than by hand — trying out every possible
department ordering and picking the one with the lowest total material
flow cost.

The program evaluates **every possible ordering** of the locations
(brute-force permutation search) and scores each ordering using a
distance-weighted cost function, then reports the ordering with the
**lowest total flow cost** — i.e. the layout in which material travels the
least, and backward flows (which are more disruptive) are penalized more
heavily than forward flows.

## How it works

Given a From-To matrix `M`, where `M[i, j]` is the amount of flow from
location `i` to location `j` in a candidate ordering:

- If `i < j` (a **forward** flow), the cost contribution is `(j - i) * M[i, j]`.
- If `i > j` (a **backward** flow), the cost contribution is `2 * (i - j) * M[i, j]`.
- If `i == j`, there is no contribution.

The total cost of an ordering is the sum of these contributions across all
location pairs. The script tries all `n!` permutations of the `n` locations
and keeps the one with the smallest total cost.

> This is a classic (simplified) formulation used in facility layout /
> plant layout optimization, related to the Quadratic Assignment Problem
> (QAP). Brute force is only practical for a small number of locations
> (this repo's example uses 5); for larger problems, a heuristic or
> metaheuristic search (e.g. simulated annealing, genetic algorithms) would
> be used instead.

## Files

| File | Description |
|---|---|
| `from_to_layout_optimizer.py` | Clean, documented Python script — build a From-To table, score orderings, and find the best one. |
| `From-to_Table_3.ipynb` | Original Jupyter notebook version of the analysis. |
| `LICENSE` | MIT License. |

## Requirements

- Python 3.8+
- [pandas](https://pandas.pydata.org/)

Install the dependency with:

```bash
pip install pandas
```

## Usage

Run the script directly to reproduce the example 5-location (`A`–`E`)
From-To chart included in this repo:

```bash
python from_to_layout_optimizer.py
```

This prints:
1. The original From-To table.
2. The total flow cost of every permutation of the 5 locations.
3. The best (lowest-cost) permutation and its cost.
4. The From-To table reordered according to the best permutation.

### Using your own data

Import the reusable functions and pass in your own From-To table as a
`pandas.DataFrame` (square matrix, locations as both the index and the
columns):

```python
import pandas as pd
from from_to_layout_optimizer import find_best_layout

locations = ["A", "B", "C"]
from_to = pd.DataFrame(0, index=locations, columns=locations)
from_to.loc["A", "B"] = 15
from_to.loc["B", "C"] = 30
from_to.loc["C", "A"] = 5
# ... fill in the rest of the flows ...

best_order, best_cost, all_results = find_best_layout(from_to)
print("Best order:", best_order, "Cost:", best_cost)
```

Alternatively, open and run `From-to_Table_3.ipynb` in Jupyter for the
original notebook walkthrough.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE)
for details.
