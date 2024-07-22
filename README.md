# Enigma Protocol

An encrypted chat application using RSA encryption and Diffie-Hellman key exchange built with WebSockets.

To learn more about the protocol, see the [Protocol](PROTOCOL.md) and [Specification](SPECIFICATION.md). This repository contains the client application of engima-protocol project implemented with Vue.js. The server side implementation is engima-protocol-python, which is a Python implementation of the protocol.

![Client App](/images/client.png)

## Getting Started

### Development

To run the client application in development mode, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/PradyumnaKrishna/enigma-protocol.git
   ```

2. Install the dependencies:

   ```bash
   npm ci
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

## Specification

The [PROTOCOL](PROTOCOL.md) document describes the protocol used for encrypting and decrypting messages, and [SPECIFICATION](SPECIFICATION.md) document describes the specification of the project, including the client and server implementations.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
