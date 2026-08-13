# Output-Efficient Generation of Unions of a Set System

## 1. Problem

Given a collection of sets

S1, S2, ..., Sm

where every Si is a subset of a base set V, the goal is to generate all
distinct sets that can be obtained as unions of some of the input sets.

Different selections of the input sets may produce the same union.

For example, it is possible that

S1 ∪ S2 = S4 ∪ S5 ∪ S19.

Therefore, enumerating all subsets of the input family and removing
duplicates afterward may perform a large amount of unnecessary work.

The goal is to generate the distinct unions without repeatedly generating
the same result through different combinations.


## 2. Initial Approach: Hash Set

My initial approach was to start with the empty set and repeatedly union
already discovered sets with each input set.

A Python hash set stores the unions that have already been discovered.

The basic idea is:

1. Start with the empty set.
2. Take a previously discovered union X.
3. Compute X ∪ Si for every input set Si.
4. Check whether the resulting union has already been seen.
5. If it is new, store it and continue from it.

This approach produces the correct distinct unions.

However, the hash set only detects a duplicate after the candidate union
has already been constructed.

For example, if

S1 ∪ S3 = S1 ∪ S2 ∪ S3,

the same final union can still be constructed through multiple paths.
The hash set prevents the duplicate from being stored or output twice,
but it does not prevent the repeated computation.


## 3. Improved Approach: Backtracking Over the Output

I then looked into output-efficient enumeration of unions of a set system.

Instead of searching over combinations of the input sets, the improved
approach searches over the possible final subset of V.

For every element of V, there are two decisions:

- 0: the element must not occur in the final union
- 1: the element must occur in the final union

For example, if

V = {A, B, C, D},

then

0110

represents the target set

{B, C}.

Each subset of V has one Boolean representation. Therefore, different
ways of constructing the same union do not correspond to different
leaves of the search tree.


## 4. Extension Test

Searching the entire binary tree would still examine all subsets of V.

To avoid this, I use an extension test at every partial assignment.

A partial assignment contains:

- required elements: elements already assigned 1
- forbidden elements: elements already assigned 0
- undecided elements

The extension question is:

Can some union of the original sets contain every required element while
containing none of the forbidden elements?

To answer this:

1. Ignore every input set containing a forbidden element.
2. Take the union of all remaining usable input sets.
3. Check whether this union contains every required element.

If it does not, no solution can exist below the current branch, so the
entire branch can be pruned.


### Example

Consider

S1 = {A, B}
S2 = {B, C}
S3 = {C, D}

and the partial assignment

010?

This means:

- A is forbidden
- B is required
- C is forbidden
- D is undecided

S1 cannot be used because it contains A.

S2 cannot be used because it contains C.

S3 cannot be used because it contains C.

Therefore, no usable set can provide the required element B.

The branch 010? can be pruned without examining either 0100 or 0101.

### Backtracking Tree Example

For the example

```text
S1 = {A, B}
S2 = {B, C}
S3 = {C, D}

V = {A, B, C, D}
```

the search tree makes one decision for each element of `V`.

```text
                         ????
                       /      \
                    0???      1???
                   /   \      /   \
                00??   01?? 10??   11??
                /       / \    X     / \
             000?    010? 011?     110? 111?
             /  \      X   / \      / \   / \
          0000 001?       0110 0111 1100 1101 1110 1111
           ✓    / \         ✓    ✓    ✓    X    ✓    ✓
              0010 0011
                X    ✓
```

Here:

```text
✓ = valid union
X = branch is impossible and is pruned
? = element has not been decided yet
```

For example, consider the branch:

```text
010?
```

Using the element order

```text
A B C D
0 1 0 ?
```

this means:

- `A` is forbidden
- `B` is required
- `C` is forbidden
- `D` is undecided

The extension test determines that this branch is impossible:

```text
S1 = {A, B}  -> cannot use because A is forbidden
S2 = {B, C}  -> cannot use because C is forbidden
S3 = {C, D}  -> cannot use because C is forbidden
```

No remaining input set can provide the required element `B`.

Therefore the algorithm stops at:

```text
010?  X
```

and does not explore:

```text
0100
0101
```

Similarly,

```text
10??
```

is pruned because it requires `A` while forbidding `B`. The only input
set containing `A` is `S1 = {A, B}`, which cannot be used because it
would also introduce the forbidden element `B`.

The valid leaves correspond exactly to the distinct unions:

```text
0000 -> {}
0011 -> {C, D}
0110 -> {B, C}
0111 -> {B, C, D}
1100 -> {A, B}
1110 -> {A, B, C}
1111 -> {A, B, C, D}
```

Thus, each valid union is represented by one leaf, while impossible
groups of candidate subsets can be eliminated before reaching the leaves.


## 5. Backtracking Algorithm

The enumeration procedure is:

1. Start with no elements decided.
2. Choose the next element of V.
3. Explore the branch where the element is forbidden.
4. Explore the branch where the element is required.
5. Before continuing down either branch, run the extension test.
6. If the extension test fails, prune the branch.
7. When every element has been decided, output the resulting valid union.

This searches over the output itself rather than over all possible
recipes for constructing the output.


## 6. Implementations

The repository contains:

- `naive_hash.py`
  - Implements my original hash-set approach.
  - Counts how many candidate unions are generated and checked.

- `efficient_enumeration.py`
  - Implements the backtracking approach.
  - Uses the extension test to prune impossible branches.
  - Counts extension checks and pruned branches.

- `benchmark.py`
  - Runs both implementations on several examples.
  - Checks that both implementations produce exactly the same unions.


## 7. Experiments

I tested four different structures.

| Test | Distinct Unions | Naive Candidate Checks | Backtracking Extension Checks | Pruned Branches |
|---|---:|---:|---:|---:|
| Basic overlapping sets | 7 | 21 | 23 | 5 |
| Duplicate-heavy input | 4 | 24 | 7 | 0 |
| Nested sets | 9 | 72 | 73 | 28 |
| Disjoint sets | 16 | 64 | 31 | 0 |

Both implementations produced exactly the same collection of unions in
all four tests.


## 8. Observations

The experiments show the different behavior of the two approaches.

The hash-set implementation correctly removes duplicate outputs, but it
can still repeatedly construct candidate unions that have already been
seen.

The backtracking implementation instead gives each possible final subset
of V a unique representation and uses the extension test to stop
searching branches that cannot contain a valid union.

The usefulness of pruning depends on the structure of the input.

For the nested-set example, 28 branches were pruned.

For the disjoint-set example, no branches were pruned because every
subset of V was a valid union.

The candidate-check and extension-check counts measure different
operations, so they should not be compared directly as runtime
measurements. The small runtime measurements in the benchmark are also
too small to draw meaningful performance conclusions.


## 9. Complexity / Further Work

The enumeration literature describes this type of approach using
backtracking (also called flashlight search) together with an extension
test.

For a set family with m input sets over a base set of n elements, the
extension test can be implemented in polynomial time by filtering sets
that intersect the forbidden elements and checking whether the remaining
sets cover the required elements.

The literature gives polynomial-delay bounds for enumeration using this
approach. This means that the work between consecutive generated outputs
is polynomial in the input size.

As a next step, I would like to investigate the precise output-sensitive
running-time bound and possible implementation improvements for larger
hypergraphs.
