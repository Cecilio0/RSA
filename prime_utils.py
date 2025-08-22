#!/usr/bin/env python3
"""
Prime Number Utilities Module

This module provides utilities for working with prime numbers, including
primality testing and prime number generation for cryptographic applications.

Author: Educational Implementation
Date: 2025
"""

import random


def is_prime(n: int, k: int = 5) -> bool:
    """
    Test if a number is prime using Miller-Rabin primality test.
    
    The Miller-Rabin test is a probabilistic primality test that is widely
    used in cryptographic applications due to its efficiency with large numbers.
    
    Args:
        n: Number to test for primality
        k: Number of rounds for testing (higher = more accurate)
    
    Returns:
        True if n is probably prime, False if n is composite
        
    Note:
        The probability of error is at most 4^(-k), so k=5 gives
        error probability ≤ 1/1024
    """
    # Handle simple cases
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as d * 2^r where d is odd
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Perform k rounds of Miller-Rabin test
    for _ in range(k):
        # Choose random base a in range [2, n-2]
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)  # Compute a^d mod n
        
        # If x = 1 or x = n-1, continue to next round
        if x == 1 or x == n - 1:
            continue
        
        # Square x repeatedly r-1 times
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            # If we never found x = n-1, n is composite
            return False
    
    # All rounds passed, n is probably prime
    return True


def generate_prime(bits: int) -> int:
    """
    Generate a prime number with specified bit length.
    
    This function generates random numbers of the specified bit length
    and tests them for primality until a prime is found.
    
    Args:
        bits: Desired bit length of the prime (must be > 1)
        
    Returns:
        A prime number with the specified bit length
        
    Raises:
        ValueError: If bits <= 1
    """
    if bits <= 1:
        raise ValueError("Bit length must be greater than 1")
    
    while True:
        # Generate random number with specified bit length
        n = random.getrandbits(bits)
        
        # Ensure the number has exactly 'bits' bits by setting MSB
        # and ensure it's odd by setting LSB
        n |= (1 << (bits - 1)) | 1
        
        # Test for primality
        if is_prime(n):
            return n


def generate_safe_prime(bits: int) -> int:
    """
    Generate a safe prime of specified bit length.
    
    A safe prime is a prime p such that (p-1)/2 is also prime.
    The prime (p-1)/2 is called a Sophie Germain prime.
    Safe primes are sometimes preferred in cryptographic applications.
    
    Args:
        bits: Desired bit length of the safe prime
        
    Returns:
        A safe prime with the specified bit length
    """
    while True:
        # Generate a prime q (Sophie Germain prime)
        q = generate_prime(bits - 1)
        # Check if p = 2q + 1 is also prime
        p = 2 * q + 1
        if is_prime(p):
            return p


def next_prime(n: int) -> int:
    """
    Find the next prime number greater than or equal to n.
    
    Args:
        n: Starting number
        
    Returns:
        The smallest prime >= n
    """
    if n < 2:
        return 2
    
    # Make n odd if it's even (except for 2)
    if n > 2 and n % 2 == 0:
        n += 1
    
    while not is_prime(n):
        n += 2 if n > 2 else 1
    
    return n


def generate_prime_pair(bits: int) -> tuple[int, int]:
    """
    Generate a pair of distinct primes with specified bit length.
    
    This is useful for RSA key generation where we need two different
    primes p and q.
    
    Args:
        bits: Desired bit length for each prime
        
    Returns:
        Tuple of two distinct primes (p, q)
    """
    p = generate_prime(bits)
    q = generate_prime(bits)
    
    # Ensure they are different
    while p == q:
        q = generate_prime(bits)
    
    return p, q


def is_strong_prime(p: int) -> bool:
    """
    Check if a prime is a strong prime.
    
    A strong prime p satisfies:
    1. p-1 has a large prime factor r
    2. p+1 has a large prime factor s  
    3. r-1 has a large prime factor t
    
    Strong primes were once thought to be more secure for RSA,
    but modern factoring algorithms have made this distinction less important.
    
    Args:
        p: Prime number to test
        
    Returns:
        True if p is a strong prime
    """
    if not is_prime(p):
        return False
    
    # For simplicity, we'll use a basic check:
    # p-1 should have a prime factor > sqrt(p-1)
    # This is a simplified version of the strong prime definition
    
    n = p - 1
    # Find largest prime factor of p-1
    largest_factor = 1
    temp = n
    
    # Check for factor 2
    while temp % 2 == 0:
        largest_factor = 2
        temp //= 2
    
    # Check for odd factors
    factor = 3
    while factor * factor <= temp:
        while temp % factor == 0:
            largest_factor = factor
            temp //= factor
        factor += 2
    
    if temp > 1:
        largest_factor = temp
    
    # Check if largest prime factor is greater than sqrt(p-1)
    return largest_factor * largest_factor > n


if __name__ == "__main__":
    """
    Demonstration of prime utilities.
    """
    print("Prime Number Utilities Demonstration")
    print("=" * 40)
    
    # Test primality of some known numbers
    test_numbers = [2, 3, 4, 17, 25, 97, 101, 1009, 1013]
    print("Primality testing:")
    for num in test_numbers:
        result = is_prime(num)
        print(f"{num}: {'Prime' if result else 'Composite'}")
    
    print(f"\n" + "-" * 40)
    
    # Generate some primes
    print("Generating primes of different bit lengths:")
    for bits in [8, 16, 32]:
        prime = generate_prime(bits)
        print(f"{bits}-bit prime: {prime} (actual bits: {prime.bit_length()})")
    
    print(f"\n" + "-" * 40)
    
    # Generate prime pairs
    print("Generating prime pairs for RSA:")
    p, q = generate_prime_pair(64)  # Small for demonstration
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"n = p * q = {p * q}")
    
    print(f"\n" + "-" * 40)
    
    # Find next primes
    print("Finding next primes:")
    test_starts = [100, 200, 1000]
    for start in test_starts:
        next_p = next_prime(start)
        print(f"Next prime after {start}: {next_p}")