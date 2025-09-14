#!/usr/bin/env python3
"""
RSA Encryption Implementation from Scratch

This module implements the RSA cryptographic algorithm from scratch for educational purposes.
It includes key generation, encryption, decryption, and utility functions.

Author: Educational Implementation
Date: 2025
"""

import random
from typing import Tuple, Optional
from prime_utils import generate_prime



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
    
    print(gcd_val, x, y, a, b)
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
    d = mod_inverse(e, phi) # d = e^(-1) mod φ(n)
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
    
    return pow(message, e, n) # c = m^e mod n


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
    return pow(ciphertext, d, n) # m' = c^d mod n


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

def int_to_hex(number: int) -> str:
    """
    Convert an integer to a hexadecimal string representation.
    
    Args:
        message: Integer message to convert

    Returns:
        Integer representation of the message
    """
    hex_string = number.to_bytes((number.bit_length() + 7) // 8, byteorder='big').hex()
    return hex_string

def hex_to_int(hex_string: str) -> int:
    """
    Convert a hexadecimal string representation back to an integer.

    Args:
        hex_string: Hexadecimal string to convert

    Returns:
        Integer representation of the hexadecimal string
    """
    return int.from_bytes(bytes.fromhex(hex_string), byteorder='big')


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

def encrypt_hex(message: str, public_key: Tuple[int, int]) -> int:
    """
    Encrypt a string message using RSA.
    
    Args:
        message: String message to encrypt
        public_key: RSA public key (n, e)
        
    Returns:
        Encrypted message as integer
    """
    message_int = string_to_int(message)
    cipher_text = encrypt(message_int, public_key)
    return int_to_hex(cipher_text)


def decrypt_hex(ciphertext: str, private_key: Tuple[int, int]) -> str:
    """
    Decrypt an integer ciphertext back to hex string using RSA.

    Args:
        ciphertext: Encrypted message as integer
        private_key: RSA private key (n, d)
        
    Returns:
        Decrypted string message
    """
    ciphertext = hex_to_int(ciphertext)
    decrypted_int = decrypt(ciphertext, private_key)
    hex_string = int_to_hex(decrypted_int)
    return hex_string


