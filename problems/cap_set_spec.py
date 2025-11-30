### SYSTEM PROMPT # if this is not present, the default system prompt from config.py will be used.
"""You are a state-of-the-art python code completion system that will be used as part of a genetic algorithm.
You will be given a list of functions, and you should improve the incomplete last function in the list.
1. Make only small changes but be sure to make some change.
2. Try to keep the code short and any comments concise.
3. Your response should be an implementation of the function priority_v# (where # is the current iteration number); do not include any examples or extraneous functions.
4. You may use numpy and itertools.
The code you generate will be appended to the user prompt and run as a python program."""
### END SYSTEM PROMPT
"""Finds large cap sets (sets of n-dimensional vectors over F_3 that do not contain 3 points on a line)."""

import itertools
import numpy as np
import funsearch

@funsearch.run
def evaluate(n: int) -> int:
  """Returns the size of an `n`-dimensional cap set."""
  capset = solve(n)
  return len(capset)

def solve(n: int) -> np.ndarray:
  """Returns a large cap set in `n` dimensions."""
  all_vectors = np.array(list(itertools.product((0, 1, 2), repeat=n)), dtype=np.int32)
  # Powers in decreasing order for compatibility with `itertools.product`, so
  # that the relationship `i = all_vectors[i] @ powers` holds for all `i`.
  powers = 3 ** np.arange(n - 1, -1, -1)
  # Precompute all priorities.
  priorities = np.array([priority(tuple(vector), n) for vector in all_vectors],dtype=float)
  # Build `capset` greedily, using priorities for prioritization.
  capset = np.empty(shape=(0, n), dtype=np.int32)
  while np.any(priorities != -np.inf):
    # Add a vector with maximum priority to `capset`, and set priorities of
    # invalidated vectors to `-inf`, so that they never get selected.
    max_index = np.argmax(priorities)
    vector = all_vectors[None, max_index]  # [1, n]
    blocking = np.einsum('cn,n->c', (- capset - vector) % 3, powers)  # [C]
    priorities[blocking] = -np.inf
    priorities[max_index] = -np.inf
    capset = np.concatenate([capset, vector], axis=0)
  return capset

@funsearch.evolve
def priority(v: tuple[int, ...], n: int) -> float:
  """
  Returns the priority, as a floating point number, of the vector `v` of length `n`. The vector 'v' is a tuple of values in {0,1,2}.
  The cap set will be constructed by adding vectors that do not create a line in order by priority.
  """
  return 0.0

