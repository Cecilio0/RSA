#!/usr/bin/env python3
"""
RSA Encryption Demonstration and Interactive Mode

This module provides demonstration and interactive functionality for the RSA implementation.
It includes examples of key generation, encryption, decryption, and an interactive mode
for testing the RSA implementation.

Author: Educational Implementation
Date: 2025
"""

import random
from rsa_implementation import (
    generate_keypair,
    encrypt,
    decrypt,
    encrypt_string,
    decrypt_string
)


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


def interactive_mode():
    """
    Interactive mode for testing RSA encryption and decryption.
    """
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


def run_benchmark():
    """
    Benchmark RSA operations with different key sizes.
    """
    import time
    
    print(f"\n" + "=" * 60)
    print("RSA Performance Benchmark")
    print("=" * 60)
    
    key_sizes = [512, 1024, 2048]
    message = "Benchmark message for RSA performance testing!"
    
    for keysize in key_sizes:
        print(f"\nTesting {keysize}-bit keys:")
        print("-" * 30)
        
        # Time key generation
        start_time = time.time()
        public_key, private_key = generate_keypair(keysize)
        key_gen_time = time.time() - start_time
        print(f"Key generation: {key_gen_time:.3f} seconds")
        
        # Time encryption
        start_time = time.time()
        ciphertext = encrypt_string(message, public_key)
        encrypt_time = time.time() - start_time
        print(f"Encryption: {encrypt_time:.6f} seconds")
        
        # Time decryption
        start_time = time.time()
        decrypted = decrypt_string(ciphertext, private_key)
        decrypt_time = time.time() - start_time
        print(f"Decryption: {decrypt_time:.6f} seconds")
        
        # Verify correctness
        success = message == decrypted
        print(f"Verification: {'SUCCESS' if success else 'FAILED'}")


def main():
    """
    Main function to run demonstrations and interactive mode.
    """
    print("RSA Encryption Implementation")
    print("Educational demonstration of RSA cryptography")
    print("=" * 60)
    
    while True:
        print("\nMain Menu:")
        print("1. Run RSA demonstration")
        print("2. Enter interactive mode") 
        print("3. Run performance benchmark")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            # Set seed for reproducible results in demonstration
            random.seed(42)
            demonstrate_rsa()
            
        elif choice == '2':
            interactive_mode()
            
        elif choice == '3':
            run_benchmark()
            
        elif choice == '4':
            print("Thank you for using the RSA implementation!")
            break
            
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")