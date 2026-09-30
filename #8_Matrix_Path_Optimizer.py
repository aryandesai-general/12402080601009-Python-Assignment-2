"""Q8: Maximum-score path with right, down and diagonal moves.

Uses O(m) memory. A blocked start or finish, or an unreachable finish, prints
IMPOSSIBLE. Counts optimal paths modulo 1_000_000_007.
"""
import sys

MOD = 1_000_000_007
NEG_INF = -10**30


def main():
    try:
        n, m = map(int, sys.stdin.readline().split())
        if not 1 <= n <= 2000 or not 1 <= m <= 2000:
            raise ValueError
        grid = []
        for _ in range(n):
            row = sys.stdin.readline().split()
            if len(row) != m:
                raise ValueError
            grid.append([None if x.upper() == "X" else int(x) for x in row])
    except ValueError:
        print("Invalid input."); return

    best = [NEG_INF] * m
    ways = [0] * m
    for i in range(n):
        diag_best, diag_ways = NEG_INF, 0
        for j in range(m):
            old_best, old_ways = best[j], ways[j]  # path from above
            if grid[i][j] is None:
                best[j], ways[j] = NEG_INF, 0
            elif i == 0 and j == 0:
                best[j], ways[j] = grid[i][j], 1
            else:
                candidates = []
                if j > 0 and best[j - 1] != NEG_INF:
                    candidates.append((best[j - 1], ways[j - 1]))  # left
                if old_best != NEG_INF:
                    candidates.append((old_best, old_ways))       # above
                if diag_best != NEG_INF:
                    candidates.append((diag_best, diag_ways))     # diagonal
                if not candidates:
                    best[j], ways[j] = NEG_INF, 0
                else:
                    maximum = max(score for score, _ in candidates)
                    best[j] = maximum + grid[i][j]
                    ways[j] = sum(count for score, count in candidates if score == maximum) % MOD
            diag_best, diag_ways = old_best, old_ways

    if best[-1] == NEG_INF:
        print("IMPOSSIBLE")
    else:
        print(best[-1], ways[-1])


if __name__ == "__main__":
    main()
