# API Testing Documentation

This documentation provides guidance on how to test the API for the decentralized IAM battery data system.

## Overview

In the `test-examples` folder, you will find several example JSON files and key pairs that can be used for testing. The script [create_jws_signature.py](../scripts/create_jws_signature.py) (located in the `scripts` folder) can be used to generate JWS (JSON Web Signature) signatures, which are required to verify that DIDs are correctly created by their rightful owners.

## Usage

### Creating new RSA key pairs:

First, you have to create the private key:

```bash
openssl genpkey -algorithm RSA -out file_private_key.pem -pkeyopt rsa_keygen_bits:2048
```

After that, you can extract the public key out of the private key:

```bash
openssl rsa -pubout -in file_private_key.pem -out file_public_key.pem
```

### DID Document

The example file [oem-did.json](./test-examples/oem-did.json) demonstrates the structure of a DID document. 
Currently, only RSA signatures are supported. You can see an example of how to generate such a token in the [create_jws_signature.py](../scripts/create_jws_signature.py) script. 

### Creating an OEM DID

To create an OEM (Original Equipment Manufacturer) DID, use the following command:

```bash
curl -X POST http://localhost:8443/api/v1/dids/createormodify \
      -H "Content-Type: application/json" \
      -d @./docs/test-examples/oem-did.json
```

### Creating a BMS DID

To create a BMS (Battery Management System) DID, use the following command:

```bash
curl -X POST http://localhost:8443/api/v1/dids/createormodify \
      -H "Content-Type: application/json" \
      -d @./docs/test-examples/bms-did.json
```

### Creating a OEM VC

To create an OEM VC, use the following command:

```bash
curl -X POST http://localhost:8443/api/v1/vcs/create \
      -H "Content-Type: application/json" \
      -d @./docs/test-examples/oem-vc.json
```

## Additional Resources

For more comprehensive information about the API, including all available endpoints and their usage, please refer to the [API Documentation](./api.md).