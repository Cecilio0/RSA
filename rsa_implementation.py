#!/usr/bin/env python3
"""
RSA Encryption Implementation from Scratch

This module implements the RSA cryptographic algorithm from scratch for educational purposes.
It includes key generation, encryption, decryption, and utility functions.

Author: Educational Implementation
Date: 2025
"""

import random
import math
from typing import Tuple, Optional


def is_prime(n: int, k: int = 5) -> bool:
    """
    Test if a number is prime using Miller-Rabin primality test.
    
    Args:
        n: Number to test for primality
        k: Number of rounds for testing (higher = more accurate)
    
    Returns:
        True if n is probably prime, False if n is composite
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as d * 2^r
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Miller-Rabin test
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True


def generate_prime(bits: int) -> int:
    """
    Generate a prime number with specified bit length.
    
    Args:
        bits: Desired bit length of the prime
        
    Returns:
        A prime number with the specified bit length
    """
    while True:
        # Generate random odd number in the desired range
        n = random.getrandbits(bits)
        # Ensure it's odd and has the right bit length
        n |= (1 << bits - 1) | 1
        
        if is_prime(n):
            return n


def gcd(a: int, b: int) -> int:
    """
    Calculate the Greatest Common Divisor using Euclidean algorithm.
    
    Args:
        a, b: Two integers
        
    Returns:
        The GCD of a and b
    """
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.
    
    Args:
        a, b: Two integers
        
    Returns:
        Tuple (gcd, x, y) where gcd = a*x + b*y
    """
    if a == 0:
        return b, 0, 1
    
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd_val, x, y


def mod_inverse(e: int, phi: int) -> Optional[int]:
    """
    Calculate modular multiplicative inverse of e modulo phi.
    
    Args:
        e: The number to find inverse of
        phi: The modulus
        
    Returns:
        The modular inverse of e mod phi, or None if it doesn't exist
    """
    gcd_val, x, _ = extended_gcd(e, phi)
    
    if gcd_val != 1:
        return None  # Modular inverse doesn't exist
    
    return (x % phi + phi) % phi


def generate_keypair(keysize: int = 2048) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Generate RSA public and private key pair.
    
    Args:
        keysize: Size of the key in bits
        
    Returns:
        Tuple containing ((n, e), (n, d)) where:
        - (n, e) is the public key
        - (n, d) is the private key
    """
    # Step 1: Generate two large prime numbers
    print(f"Generating {keysize}-bit RSA key pair...")
    p = generate_prime(keysize // 2)
    q = generate_prime(keysize // 2)
    
    # Ensure p and q are different
    while p == q:
        q = generate_prime(keysize // 2)
    
    # Step 2: Compute n = p * q
    n = p * q
    
    # Step 3: Compute Euler's totient function φ(n) = (p-1)(q-1)
    phi = (p - 1) * (q - 1)
    
    # Step 4: Choose e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1
    e = 65537  # Common choice for e
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    
    # Step 5: Calculate d, the modular multiplicative inverse of e
    d = mod_inverse(e, phi)
    if d is None:
        raise ValueError("Cannot compute modular inverse")
    
    print(f"Key generation complete!")
    print(f"Key size: {n.bit_length()} bits")
    
    return ((n, e), (n, d))


def encrypt(message: int, public_key: Tuple[int, int]) -> int:
    """
    Encrypt a message using RSA public key.
    
    Args:
        message: The message as an integer (must be < n)
        public_key: Tuple (n, e) representing the public key
        
    Returns:
        The encrypted message as an integer
    """
    n, e = public_key
    
    if message >= n:
        raise ValueError(f"Message too large. Must be less than {n}")
    
    return pow(message, e, n)


def decrypt(ciphertext: int, private_key: Tuple[int, int]) -> int:
    """
    Decrypt a message using RSA private key.
    
    Args:
        ciphertext: The encrypted message as an integer
        private_key: Tuple (n, d) representing the private key
        
    Returns:
        The decrypted message as an integer
    """
    n, d = private_key
    return pow(ciphertext, d, n)


def string_to_int(message: str) -> int:
    """
    Convert a string message to an integer for RSA processing.
    
    Args:
        message: String message to convert
        
    Returns:
        Integer representation of the message
    """
    return int.from_bytes(message.encode('utf-8'), byteorder='big')


def int_to_string(number: int) -> str:
    """
    Convert an integer back to a string message.
    
    Args:
        number: Integer to convert back to string
        
    Returns:
        String representation of the number
    """
    # Calculate the number of bytes needed
    byte_length = (number.bit_length() + 7) // 8
    return number.to_bytes(byte_length, byteorder='big').decode('utf-8')


def encrypt_string(message: str, public_key: Tuple[int, int]) -> int:
    """
    Encrypt a string message using RSA.
    
    Args:
        message: String message to encrypt
        public_key: RSA public key (n, e)
        
    Returns:
        Encrypted message as integer
    """
    message_int = string_to_int(message)
    return encrypt(message_int, public_key)


def decrypt_string(ciphertext: int, private_key: Tuple[int, int]) -> str:
    """
    Decrypt an integer ciphertext back to string using RSA.
    
    Args:
        ciphertext: Encrypted message as integer
        private_key: RSA private key (n, d)
        
    Returns:
        Decrypted string message
    """
    decrypted_int = decrypt(ciphertext, private_key)
    return int_to_string(decrypted_int)


def demonstrate_rsa():
    """
    Demonstrate RSA encryption and decryption with examples.
    """
    print("=" * 60)
    print("RSA Encryption Demonstration")
    print("=" * 60)
    
    # Generate key pair
    keysize = 1024  # Smaller key for demo speed
    public_key, private_key = generate_keypair(keysize)
    
    n, e = public_key
    _, d = private_key
    
    print(f"\nPublic Key (n, e):")
    print(f"n = {n}")
    print(f"e = {e}")
    print(f"\nPrivate Key (n, d):")
    print(f"n = {n}")
    print(f"d = {d}")
    
    # Test with a simple message
    original_message = "Hello, RSA!"
    print(f"\nOriginal message: '{original_message}'")
    
    # Encrypt the message
    ciphertext = encrypt_string(original_message, public_key)
    print(f"Encrypted message: {ciphertext}")
    
    # Decrypt the message
    decrypted_message = decrypt_string(ciphertext, private_key)
    print(f"Decrypted message: '{decrypted_message}'")
    
    # Verify
    print(f"\nVerification: {'SUCCESS' if original_message == decrypted_message else 'FAILED'}")
    
    # Test with numbers
    print(f"\n" + "-" * 40)
    print("Testing with numerical message:")
    
    original_number = 42
    print(f"Original number: {original_number}")
    
    encrypted_number = encrypt(original_number, public_key)
    print(f"Encrypted number: {encrypted_number}")
    
    decrypted_number = decrypt(encrypted_number, private_key)
    print(f"Decrypted number: {decrypted_number}")
    
    print(f"Verification: {'SUCCESS' if original_number == decrypted_number else 'FAILED'}")


if __name__ == "__main__":
    # Set seed for reproducible results (remove in production)
    random.seed(42)
    
    demonstrate_rsa()
    
    print(f"\n" + "=" * 60)
    print("Interactive Mode")
    print("=" * 60)
    
    try:
        # Generate keys for interactive mode
        print("\nGenerating new key pair for interactive use...")
        public_key, private_key = generate_keypair(1024)
        
        while True:
            print("\nOptions:")
            print("1. Encrypt a message")
            print("2. Decrypt a message (enter ciphertext as integer)")
            print("3. Generate new key pair")
            print("4. Show current public key")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                message = input("Enter message to encrypt: ")
                try:
                    ciphertext = encrypt_string(message, public_key)
                    print(f"Encrypted message: {ciphertext}")
                except Exception as e:
                    print(f"Error: {e}")
            
            elif choice == '2':
                try:
                    ciphertext = int(input("Enter ciphertext (as integer): "))
                    decrypted = decrypt_string(ciphertext, private_key)
                    print(f"Decrypted message: '{decrypted}'")
                except Exception as e:
                    print(f"Error: {e}")
            
            elif choice == '3':
                keysize = int(input("Enter key size in bits (e.g., 1024, 2048): ") or "1024")
                public_key, private_key = generate_keypair(keysize)
                print("New key pair generated!")
            
            elif choice == '4':
                n, e = public_key
                print(f"Public key (n, e):")
                print(f"n = {n}")
                print(f"e = {e}")
            
            elif choice == '5':
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")