# Enigma Protocol

**Date**: July 8, 2024  
**Version**: 0.3.0

This document describes the protocol/algorithm for encrypting and decrypting messages, independent of how the keys are generated and the messages are transmitted. For message transmission, see the [Specification](SPECIFICATION.md).

## Overview

The protocol specifies the algorithm used for encrypting and decrypting messages.

## Motivation

Standard asymmetric encryption algorithms like RSA are slow and unsuitable for encrypting large messages. They also fail to encrypt messages larger than the key size. To overcome these limitations, the protocol uses a combination of symmetric and asymmetric encryption algorithms.

## Encryption

Encryption involves two different algorithms: symmetric and asymmetric encryption. Symmetric encryption is used to encrypt the message, and asymmetric encryption is used to encrypt the symmetric key, resulting in a fully encrypted message.

![Encryption](/images/encryption.png)

Steps to encrypt a message:

1. **Encrypting the Message**: Symmetric encryption must be used to encrypt the message. A unique symmetric key must be generated for each message and used to encrypt the message.
2. **Encrypting the Key**: Asymmetric encryption must be used to encrypt the symmetric key. The receiver's public key must be used to encrypt the symmetric key.
3. **Combining the Encrypted Key and Message**: The encrypted symmetric key and the encrypted message must be combined to form a complete encrypted message.

## Decryption

Decryption follows similar steps as encryption, but in reverse order. Asymmetric decryption is used to decrypt the symmetric key, and symmetric decryption is used to decrypt the message.

![Decryption](/images/decryption.png)

Steps to decrypt a message:

1. **Decrypting the Key**: Asymmetric decryption must be used to decrypt the symmetric key. The receiver's private key must be used to decrypt the symmetric key.
2. **Decrypting the Message**: Symmetric decryption must be used to decrypt the message. The symmetric key must be used to decrypt the message.
