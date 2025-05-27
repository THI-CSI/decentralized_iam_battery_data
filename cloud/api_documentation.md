#API Documentation - BatteryPass Cloud API

##Overview
This is the current state of our BatteryPass cloud API. The API is written in FastAPI and handles encrypted battery data stored by DIDs. It supports reading, writing, and updating data, plus some small utility features like timestamping and listing all entries. Encryption uses ECC and the DB is based on TinyDB.

---

##BaseURL
`http://localhost:8000`

---

##Endpoints

###GET `/`
simple health check to test if api works

**Response**
```json
{
  "message": "API is working"
}
```

---

###GET `/batterypass/{did}`
returns the encrypted db entry for that specific DID

**Path Parameter**
- `did` = Decentralized ID used as unique key

**Response**
- 200 OK = returns the entry
- 404 = if nothing found

---

###PUT `/batterypass/{did}`
adds new data for a DID. fails if already in db

**Path Parameter**
- `did` = unique string id

**Body**
must be of type `EncryptedPayload`, includes:
- `encrypted_data`
- `signature`

**Response**
- 200 OK = success
- 400 = already exists or verify failed

---

###POST `/batterypass/{did}`
updates an existing db entry. decrypts the old one, updates values, then re-encrypts

**Path Parameter**
- `did` = target entry

**Body**
same type as PUT request (EncryptedPayload)

**Response**
- 200 OK = update successful
- 404 = not found
- 400 = verify/decrypt failed

---

###GET `/batterypass/`
lists all DIDs that exist in the db

**Response**
```json
[
  "did:example:001",
  "did:example:abc",
  ...
]
```

---

##Error Format
if something fails, api returns this format:
```json
{
  "status": 400,
  "message": "Something went wrong",
  "timestamp": "2025-05-27T10:30:00Z"
}
```

---

##Notes
- db = TinyDB stored locally
- data is encrypted with ECC and signed
- keys from `.env` file using PASSPHRASE
- on PUT, new entries get timestamp added
- on duplicate insert (same DID), warning gets logged
- API supports basic logging and diagnostic info for devs/testers
- data structure / encryption logic not touched
