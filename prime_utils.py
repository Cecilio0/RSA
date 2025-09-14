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
