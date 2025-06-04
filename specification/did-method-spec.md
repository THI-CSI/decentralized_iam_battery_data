
# did:batterypass Method Specification

**Version:** 1.0  
**Authors:** Project CSI-6 – TH Ingolstadt

---

## 1. Purpose

The `did:batterypass` method defines a role-based structure for decentralized identifiers (DIDs) in the context of the Battery Passport. It identifies entities such as OEMs, BMS systems, cloud nodes, service providers, and end users. It enables the issuance and verification of Verifiable Credentials (VCs) for identity and access management of battery data.

---

## 2. Method Name

```
did:batterypass
```

---

## 3. Target System

The `did:batterypass` method is independent of any specific public blockchain and is implemented in the project via a dedicated IAM blockchain.

This blockchain functions as a Verifiable Data Registry (VDR) as per W3C definition and supports:

- Storage of **DIDs**: Creation (`POST /dids`) and revocation (`DELETE /dids/<did>`) by authorized entities
- Storage of **Verifiable Credentials (VCs)**: Assignment and signing via (`POST /dids/<did>/vc`), and access via (`GET /vc/<urn>`)
- Access to **transactions and audit trails**: e.g., via `GET /blocks`, `GET /blocks/<id>/transactions`

The API is implemented with FastAPI, and data is stored per block with persistent recording of DIDs, VCs, and associated transactions.

Access is documented via Swagger at `http://localhost:8443/swagger/index.html`. The IAM blockchain runs containerized via Docker and can be controlled using the `tools.py` script:

```bash
python3 tools.py dev --build
```

This infrastructure anchors the `did:batterypass` method within a fully functional decentralized IAM system that natively supports all CRUD operations (Create, Read, Update, Deactivate).

---

## 4. Method-Specific Identifier Format

```
did:batterypass:<role>.<identifier>
```

### ABNF Specification

```abnf
method-name        = "batterypass"
method-specific-id = role "." identifier

role               = "oem" / "bms" / "cloud" / "service" / "user"
identifier         = 1*(ALPHA / DIGIT / "-")

; Examples:
; did:batterypass:oem.VW
; did:batterypass:bms.sn-987654321
; did:batterypass:cloud.eu-node-01
```

**Role examples:**

- `oem`: vehicle manufacturer (e.g., VW)
- `bms`: battery management system
- `cloud`: cloud node
- `service`: inspection/service provider
- `user`: end user

**Example DIDs:**

- `did:batterypass:oem.VW`
- `did:batterypass:bms.sn-987654321`

The `<identifier>` can contain letters, digits, and hyphens.

---

## 5. CRUD Operations

### 5.1 Create
- Generate key pair (e.g., Ed25519 or EC P-256)
- Create DID document with `id`, `verificationMethod`, optional `service`
- Register (centrally or decentrally)

### 5.2 Read (Resolve)
- Resolver recognizes `did:batterypass`
- Queries registry, returns JSON-based DID document

### 5.3 Update
- Allows key rotation or service endpoint change
- Authenticated via `authentication` entry in the document

### 5.4 Deactivate
- Can be deactivated by the controller
- Registry must mark DID as "revoked" or remove it

---

## 6. DID Document Example

```json
{
  "@context": "https://www.w3.org/ns/did/v1",
  "id": "did:batterypass:bms.sn-987654321",
  "verificationMethod": [{
    "id": "did:batterypass:bms.sn-987654321#key-1",
    "type": "JsonWebKey2020",
    "controller": "did:batterypass:bms.sn-987654321",
    "publicKeyMultibase": "z6Mkpz2xw9M3JMfqk3m7JRXetPL4Wwutb6X6bojq2nMid8Kd"
  }],
  "service": [{
    "id": "did:batterypass:bms.sn-987654321#batteryData",
    "type": "BatteryDataService",
    "serviceEndpoint": "https://cloud.example.com/bms/987654321"
  }],
  "timestamp": "2025-04-10T12:00:00Z",
  "revoked": false
}
```

---

## 7. Example Verifiable Credentials

### 7.1 BMSProduction VC

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "http://localhost:8443/docs/vc.schema.html"
  ],
  "id": "urn:uuid:982c43ee-3d16-419a-a2f4-5c61710f428b",
  "type": ["VerifiableCredential", "BMSProduction"],
  "issuer": "did:batterypass:bms.sn-987654321",
  "holder": "did:batterypass:oem.VW",
  "issuanceDate": "2025-06-10T12:01:00Z",
  "credentialSubject": {
    "id": "did:batterypass:oem.VW",
    "bmsDid": "did:batterypass:bms.sn-987654321",
    "producedOn": "2025-06-10",
    "lotNumber": "LOT-775533"
  },
  "proof": {
    "type": "EcdsaSecp256r1Signature2019",
    "created": "2025-06-10T12:01:03Z",
    "verificationMethod": "did:batterypass:bms.sn-987654321#device-key",
    "proofPurpose": "assertionMethod",
    "jws": "eyJhbGciOiJFUzI1NiJ9..BASE64_SIG"
  }
}
```

### 7.2 ServiceAccess VC

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "http://localhost:8443/docs/vc.schema.html"
  ],
  "id": "urn:uuid:cc4e69d7-b7f7-4155-ac8b-5af63df4472a",
  "type": ["VerifiableCredential", "ServiceAccess"],
  "issuer": "did:batterypass:bms.sn-987654321",
  "holder": "did:batterypass:service.tuv-sued-42",
  "issuanceDate": "2025-07-04T07:45:00Z",
  "expirationDate": "2027-07-04T07:45:00Z",
  "credentialSubject": {
    "id": "did:batterypass:service.tuv-sued-42",
    "bmsDid": "did:batterypass:bms.sn-987654321",
    "accessLevel": ["read"],
    "validFrom": "2025-07-04T07:45:00Z",
    "validUntil": "2027-07-04T07:45:00Z"
  },
  "proof": {
    "type": "EcdsaSecp256r1Signature2019",
    "created": "2025-07-04T07:45:05Z",
    "verificationMethod": "did:batterypass:bms.sn-987654321#device-key",
    "proofPurpose": "assertionMethod",
    "jws": "eyJhbGciOiJFUzI1NiJ9..BASE64_SIG"
  }
}
```

---

## 8. Security Considerations

- Cryptographic signatures are required for all operations
- Privacy is ensured through minimal data disclosure and optional encryption
- Key rotation and revocation (`revoked`) are supported

---

## 9. Compliance

- Conforms to W3C DID Core 1.0
- Conforms to Verifiable Credentials Data Model 1.1
- JSON-compatible and ABNF-compliant syntax

---

## 10. Additional Notes

- More examples (User, Cloud, EU Root Authority) can be found in the sample DIDs
- Optional future additions: `credentialStatus`, `vcHash`
- Version control can be managed via GitHub (README, JSON Schemas, etc.)

---

## 11. Service Types

The following `service.type` values can be used in DID documents for BatteryPass:

- `BatteryDataService`: interface to cloud DB (GET, PUT, POST via FastAPI)
- `IssueVC`: endpoint for issuing verifiable credentials
- `DiagnosticAPI`: access to diagnostics and logging

---

## 12. DID Resolution & Error Handling

BatteryPass uses HTTP-based resolvers. Error codes:

- `404 Not Found`: DID not found
- `410 Gone`: DID revoked (`revoked: true`)
- `400 Bad Request`: invalid signature or request
- `500+`: internal resolver error

Example error message:

```json
{
  "status": 400,
  "message": "Signature verification failed",
  "timestamp": "2025-05-29T10:30:00Z"
}
```

---

## 13. Retry Strategy (Data Transmission)

To secure cloud data transmission, the following retry strategies are applied:

- 3 retries per request
- 2 seconds wait between retries
- Retries only for network errors or HTTP 5xx
- No retry for HTTP 4xx
