from itertools import product

# Each polynomial term:
# (coefficient, set of variables)

polynomial = [
    (5, {"A"}),
    (3, {"A", "B"}),
    (4, {"A", "C"}),
    (2, {"D"})
]

# Variables to eliminate
X = {"A"}

# Automatically find V
V = set()

for coefficient, variables in polynomial:
    V.update(variables)

print("V =", V)

Y = V - X

print("X =", X)
print("Y =", Y)





# Split the polynomial terms into P, Q, and R

P = []
Q = []
R = []

for coefficient, variables in polynomial:

    # Term contains only X variables
    if variables <= X:
        P.append((coefficient, variables))

    # Term contains only Y variables
    elif variables <= Y:
        R.append((coefficient, variables))

    # Term contains variables from both X and Y
    else:
        Q.append((coefficient, variables))

print("\nP =", P)
print("Q =", Q)
print("R =", R)



# Build T from the Y-parts of the crossing terms in Q

T = []

for _, variables in Q:
    y_part = variables & Y

    if y_part not in T:
        T.append(y_part)

print("T =", T)


# Generate all distinct signatures of T

signatures = set()

for values in product([0, 1], repeat=len(Y)):

    assignment = dict(zip(Y, values))

    signature = []

    for t_set in T:

        value = 1

        for variable in t_set:
            value *= assignment[variable]

        signature.append(value)

    signatures.add(tuple(signature))

print("Signatures =", signatures)







# Build the union associated with each signature

signature_unions = {}

for signature in signatures:

    union_set = set()

    for index, bit in enumerate(signature):

        if bit == 1:
            union_set.update(T[index])

    signature_unions[signature] = union_set


print("\nSignature -> Union")

for signature, union_set in signature_unions.items():
    print(signature, "->", union_set)


#Step 5 — Evaluate polynomial terms
def evaluate_terms(terms, assignment):
    total = 0

    for coefficient, variables in terms:
        term_value = coefficient

        for variable in variables:
            term_value *= assignment[variable]

        total += term_value

    return total



# Compute mu(y) for every signature

mu = {}

X_list = list(X)

for signature in signatures:

    best_value = float("-inf")

    # Create the Y-values represented by this signature.
    # For this example T = [{'B'}, {'C'}],
    # so the signature directly gives B and C.
    signature_assignment = {}

    for index, bit in enumerate(signature):
        t_set = T[index]

        if len(t_set) == 1:
            variable = next(iter(t_set))
            signature_assignment[variable] = bit

    # Try every possible assignment of X
    for x_values in product([0, 1], repeat=len(X_list)):

        x_assignment = dict(zip(X_list, x_values))

        assignment = {
            **x_assignment,
            **signature_assignment
        }

        # alpha = P terms
        alpha_value = evaluate_terms(P, assignment)

        # beta = Q terms
        beta_value = evaluate_terms(Q, assignment)

        value = alpha_value + beta_value

        if value > best_value:
            best_value = value

    mu[signature] = best_value


print("\nmu(y) values")

for signature, value in mu.items():
    print(signature, "->", value)



# ---------------------------------------------------------
# STEP 6: Reconstruct a polynomial from the mu(y) values
# ---------------------------------------------------------

# The positions in the signature correspond to the sets in T.
# In our current example:
#
# T[0] = {'B'}
# T[1] = {'C'}
#
# So the polynomial reconstructed from mu will use B and C.

signature_variables = []

for t_set in T:
    if len(t_set) == 1:
        signature_variables.append(next(iter(t_set)))

print("\nSignature variables =", signature_variables)


# We will store the polynomial as:
# (coefficient, set_of_variables)

mu_polynomial = []


# For every possible subset S of the signature variables,
# calculate its multilinear polynomial coefficient.

n = len(signature_variables)

for mask in product([0, 1], repeat=n):

    active_indices = [
        i for i, bit in enumerate(mask)
        if bit == 1
    ]

    coefficient = 0

    # Look at every subset of the active indices
    for subset_mask in product([0, 1], repeat=len(active_indices)):

        signature = [0] * n
        subset_size = 0

        for j, use_index in enumerate(subset_mask):

            if use_index == 1:
                index = active_indices[j]
                signature[index] = 1
                subset_size += 1

        signature = tuple(signature)

        sign = (-1) ** (len(active_indices) - subset_size)

        coefficient += sign * mu[signature]

    if coefficient != 0:

        variables = {
            signature_variables[i]
            for i, bit in enumerate(mask)
            if bit == 1
        }

        mu_polynomial.append((coefficient, variables))


print("\nPolynomial obtained from mu:")

for term in mu_polynomial:
    print(term)


# ---------------------------------------------------------
# STEP 7: Add gamma (the R terms)
# ---------------------------------------------------------

projection_polynomial = mu_polynomial + R


print("\nProjection polynomial:")

for term in projection_polynomial:
    print(term)


# ---------------------------------------------------------
# STEP 8: Verify the projection
# ---------------------------------------------------------

Y_list = list(Y)

print("\nVerification:")

all_correct = True

for y_values in product([0, 1], repeat=len(Y_list)):

    y_assignment = dict(zip(Y_list, y_values))

    # Directly maximize the ORIGINAL polynomial over X
    best_original_value = float("-inf")

    for x_values in product([0, 1], repeat=len(X_list)):

        x_assignment = dict(zip(X_list, x_values))

        full_assignment = {
            **x_assignment,
            **y_assignment
        }

        original_value = evaluate_terms(
            polynomial,
            full_assignment
        )

        if original_value > best_original_value:
            best_original_value = original_value


    # Evaluate our new projection polynomial
    projected_value = evaluate_terms(
        projection_polynomial,
        y_assignment
    )


    print(
        "Y =", y_assignment,
        "| original max =", best_original_value,
        "| projection =", projected_value
    )


    if best_original_value != projected_value:
        all_correct = False


print("\nProjection verified:", all_correct)