import random

# Prime number (p) and generator (g) for the finite field
p = 23  # A small prime number for simplicity
g = 5   # A generator for the finite field

# Prover's secret (x)
x = random.randint(1, p - 2)  # Secret value
y = pow(g, x, p)  # Public value

print(f"Prover's secret (x): {x}")
print(f"Prover's public value (y): {y}")

# Zero-Knowledge Proof
def zero_knowledge_proof():
    # Prover picks a random number (r) and calculates a commitment (t)
    r = random.randint(1, p - 2)
    t = pow(g, r, p)

    # Verifier sends a challenge (c), which is a random bit (0 or 1)
    c = random.randint(0, 1)

    # Prover calculates the response (z) using the challenge and their secret
    z = (r + c * x) % (p - 1)

    # Verifier checks if the proof is valid by comparing two values
    left = pow(g, z, p)  # This is what the prover claims
    right = (t * pow(y, c, p)) % p  # This is what the verifier computes

    # Print intermediate values for clarity
    print(f"Commitment (t): {t}")
    print(f"Challenge (c): {c}")
    print(f"Response (z): {z}")
    print(f"Verifier checks: {left} == {right}")

    # If both sides match, the proof is valid
    return left == right

# Run the Zero-Knowledge Proof
if zero_knowledge_proof():
    print("Proof verified successfully!")
else:
    print("Proof verification failed.")