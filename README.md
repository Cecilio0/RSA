# RSA Encryption Implementation

## Overview

RSA (Rivest-Shamir-Adleman) is one of the most widely used public-key cryptographic algorithms. It was first published in 1977 by Ron Rivest, Adi Shamir, and Leonard Adleman at MIT. RSA enables secure communication over insecure channels and forms the foundation of modern internet security protocols.

## How RSA Works

RSA is an asymmetric encryption algorithm, meaning it uses two different keys: a **public key** for encryption and a **private key** for decryption. The security of RSA is based on the computational difficulty of factoring large composite numbers.

### Mathematical Foundation

RSA relies on several mathematical concepts:

1. **Prime Numbers**: Numbers greater than 1 that have no positive divisors other than 1 and themselves
2. **Modular Arithmetic**: Arithmetic performed with respect to a modulus
3. **Euler's Totient Function**: φ(n) counts the positive integers up to n that are relatively prime to n
4. **Modular Exponentiation**: Computing (base^exponent) mod modulus efficiently

### Key Generation Process

The RSA key generation process involves the following steps:

#### Step 1: Choose Two Large Prime Numbers
- Select two distinct large prime numbers `p` and `q`
- These should be randomly chosen and kept secret
- For security, each prime should be at least 1024 bits (preferably 2048+ bits)

#### Step 2: Compute n = p × q
- `n` is called the **modulus**
- `n` will be part of both the public and private keys
- The length of `n` in bits determines the key size

#### Step 3: Calculate Euler's Totient Function
- φ(n) = φ(p × q) = (p-1) × (q-1)
- This represents the number of integers less than n that are coprime to n
- φ(n) is kept secret and used in private key generation

#### Step 4: Choose the Public Exponent e
- Select an integer `e` such that 1 < e < φ(n)
- `e` must be coprime to φ(n), meaning gcd(e, φ(n)) = 1
- Common choices are 3, 17, or 65537 (2^16 + 1)
- 65537 is most commonly used as it provides good security and efficiency

#### Step 5: Calculate the Private Exponent d
- Find `d` such that (d × e) ≡ 1 (mod φ(n))
- In other words, `d` is the modular multiplicative inverse of `e` modulo φ(n)
- This is computed using the Extended Euclidean Algorithm
- `d` must be kept secret

#### Step 6: Form the Key Pair
- **Public Key**: (n, e) - can be shared publicly
- **Private Key**: (n, d) - must be kept secret
- Note: `p`, `q`, and φ(n) should also be kept secret or destroyed

### Encryption Process

To encrypt a message `M`:

1. **Message Preparation**: Convert the message to a numerical representation
2. **Padding**: Apply padding scheme (like PKCS#1) for security
3. **Encryption**: Compute ciphertext `C` using the formula:
   ```
   C ≡ M^e (mod n)
   ```
4. The encrypted message `C` can now be safely transmitted

### Decryption Process

To decrypt a ciphertext `C`:

1. **Decryption**: Compute the original message `M` using the formula:
   ```
   M ≡ C^d (mod n)
   ```
2. **Remove Padding**: Strip the padding to recover the original message
3. **Message Recovery**: Convert the numerical result back to the original format

### Mathematical Proof of Correctness

The RSA algorithm works because of Euler's theorem. For any message `M` coprime to `n`:

```
M^φ(n) ≡ 1 (mod n)
```

Since `e × d ≡ 1 (mod φ(n))`, we can write `e × d = k × φ(n) + 1` for some integer `k`.

Therefore:
```
C^d ≡ (M^e)^d ≡ M^(e×d) ≡ M^(k×φ(n)+1) ≡ M^(k×φ(n)) × M^1 ≡ (M^φ(n))^k × M ≡ 1^k × M ≡ M (mod n)
```

This proves that decryption recovers the original message.

## Security Considerations

### Key Length
- **1024-bit keys**: Considered weak, deprecated
- **2048-bit keys**: Current minimum recommendation
- **3072-bit keys**: Good long-term security
- **4096-bit keys**: High security but slower performance

### Vulnerabilities and Attacks

1. **Factorization Attack**: If an attacker can factor `n` into `p` and `q`, they can compute the private key
2. **Small Exponent Attack**: Using small values of `e` without proper padding can be vulnerable
3. **Common Modulus Attack**: Reusing the same `n` with different key pairs
4. **Timing Attacks**: Side-channel attacks based on execution time
5. **Padding Oracle Attacks**: Attacks on improper padding implementations

### Best Practices

1. **Use Proper Padding**: Always use secure padding schemes like OAEP
2. **Random Prime Generation**: Use cryptographically secure random number generators
3. **Key Size**: Use at least 2048-bit keys for new applications
4. **Constant-Time Implementation**: Implement operations in constant time to prevent timing attacks
5. **Key Management**: Properly protect and manage private keys

## Applications

RSA is used in many security applications:

1. **Digital Signatures**: Proving authenticity and non-repudiation
2. **Key Exchange**: Securely exchanging symmetric keys
3. **SSL/TLS**: Securing web communications
4. **SSH**: Secure shell access
5. **Email Encryption**: PGP/GPG email security
6. **Code Signing**: Verifying software integrity

## Limitations

1. **Performance**: RSA is much slower than symmetric encryption
2. **Message Size**: Can only encrypt messages smaller than the key size
3. **Quantum Vulnerability**: Vulnerable to quantum computers running Shor's algorithm
4. **Key Size Growth**: Requires increasingly larger keys for future security

## File Structure

The implementation is organized into multiple modules for better code organization:

### Core Modules

- **`prime_utils.py`** - Prime number utilities and operations
  - Miller-Rabin primality testing
  - Prime number generation (standard, safe, and strong primes)
  - Prime pair generation for RSA
  - Utility functions for prime operations

- **`rsa_implementation.py`** - Core RSA cryptographic functions
  - RSA key pair generation
  - Encryption and decryption algorithms
  - Modular arithmetic utilities (GCD, extended GCD, modular inverse)
  - String-to-integer conversion utilities

- **`main.py`** - Demonstration and interactive functionality
  - RSA algorithm demonstration with examples
  - Interactive mode for testing encryption/decryption
  - User-friendly menu system

## Usage

### Running the Demonstration

```bash
python main.py
```

This will launch the main menu with options for:
1. RSA demonstration with examples
2. Interactive mode for custom testing
3. Performance benchmarking
4. Exit

### Using as a Library

You can import and use the RSA functions directly:

```python
from rsa_implementation import generate_keypair, encrypt_string, decrypt_string
from prime_utils import generate_prime, is_prime

# Generate RSA key pair
public_key, private_key = generate_keypair(2048)

# Encrypt a message
message = "Hello, RSA!"
ciphertext = encrypt_string(message, public_key)

# Decrypt the message
decrypted = decrypt_string(ciphertext, private_key)

# Generate prime numbers
prime = generate_prime(512)  # 512-bit prime
```

## Implementation Notes

The included Python implementation demonstrates:

- Miller-Rabin probabilistic primality testing
- Cryptographically secure prime number generation
- Complete RSA key pair generation process
- Modular exponentiation and arithmetic operations
- String encoding/decoding for message processing
- Interactive testing and benchmarking tools

### Key Features

- **Modular Design**: Separated concerns with dedicated modules for primes, RSA core, and demonstrations
- **Educational Focus**: Comprehensive comments and step-by-step implementation
- **Interactive Testing**: Built-in tools for experimenting with different key sizes and messages
- **Performance Analysis**: Benchmarking tools to compare different key sizes
- **Security Considerations**: Implements best practices for educational cryptographic code

This implementation is for educational purposes. Production systems should use well-tested cryptographic libraries like `cryptography` or `pycryptodome`.

## References

1. Rivest, R. L., Shamir, A., & Adleman, L. (1978). A method for obtaining digital signatures and public-key cryptosystems. Communications of the ACM, 21(2), 120-126.
2. PKCS #1 v2.1: RSA Cryptography Standard (RFC 3447)
3. NIST Special Publication 800-56B: Recommendation for Pair-Wise Key Establishment Schemes