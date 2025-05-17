/* tslint:disable */
/* eslint-disable */

/**
 * 
 * @export
 */
export const CoreAccessLevel = {
    Read: 'read',
    Write: 'write'
} as const;
export type CoreAccessLevel = typeof CoreAccessLevel[keyof typeof CoreAccessLevel];

/**
 * 
 * @export
 * @interface CoreBmsProduction
 */
export interface CoreBmsProduction {
    /**
     * Level of access granted (read or write).
     * @type {Array<CoreAccessLevel>}
     * @memberof CoreBmsProduction
     */
    accessLevel?: Array<CoreAccessLevel>;
    /**
     * DID of the Battery Management System.
     * 
     * DID of the BMS to which access is granted.
     * @type {string}
     * @memberof CoreBmsProduction
     */
    bmsDid?: string;
    /**
     * Unique identifier for the BMS production credential.
     * 
     * Unique identifier for the service access credential.
     * @type {string}
     * @memberof CoreBmsProduction
     */
    id?: string;
    /**
     * Optional lot number for the BMS production.
     * @type {string}
     * @memberof CoreBmsProduction
     */
    lotNumber?: string;
    /**
     * Date when the BMS was produced.
     * @type {string}
     * @memberof CoreBmsProduction
     */
    producedOn?: string;
    /**
     * Type indicator for a BMS production event.
     * 
     * Type indicator for a service access permission.
     * @type {CoreCredentialSubjectType}
     * @memberof CoreBmsProduction
     */
    type?: CoreCredentialSubjectType;
    /**
     * Start of the validity period for service access.
     * @type {string}
     * @memberof CoreBmsProduction
     */
    validFrom?: string;
    /**
     * End of the validity period for service access.
     * @type {string}
     * @memberof CoreBmsProduction
     */
    validUntil?: string;
}


/**
 * 
 * @export
 * @interface CoreContext
 */
export interface CoreContext {
    /**
     * 
     * @type {string}
     * @memberof CoreContext
     */
    string?: string;
    /**
     * 
     * @type {Array<string>}
     * @memberof CoreContext
     */
    stringArray?: Array<string>;
}

/**
 * 
 * @export
 */
export const CoreCredentialSubjectType = {
    BMSProduction: 'BMSProduction',
    ServiceAccess: 'ServiceAccess'
} as const;
export type CoreCredentialSubjectType = typeof CoreCredentialSubjectType[keyof typeof CoreCredentialSubjectType];

/**
 * 
 * @export
 * @interface CoreDid
 */
export interface CoreDid {
    /**
     * Decentralized Identifier (DID) for the entity, following the DID syntax.
     * @type {string}
     * @memberof CoreDid
     */
    id?: string;
    /**
     * Public key information used for verifying signatures and authentication.
     * @type {CorePublicKey}
     * @memberof CoreDid
     */
    publicKey?: CorePublicKey;
    /**
     * Boolean flag indicating whether this DID has been revoked.
     * @type {boolean}
     * @memberof CoreDid
     */
    revoked?: boolean;
    /**
     * Optional array of service endpoints related to the DID subject, such as APIs or metadata
     * services.
     * @type {Array<CoreDidSchema>}
     * @memberof CoreDid
     */
    service?: Array<CoreDidSchema>;
    /**
     * Timestamp indicating when the DID document was created/modified.
     * @type {string}
     * @memberof CoreDid
     */
    timestamp?: string;
}
/**
 * 
 * @export
 * @interface CoreDidSchema
 */
export interface CoreDidSchema {
    /**
     * Identifier for the service endpoint, typically a DID fragment.
     * @type {string}
     * @memberof CoreDidSchema
     */
    id?: string;
    /**
     * The actual service endpoint, which can be a URL.
     * @type {string}
     * @memberof CoreDidSchema
     */
    serviceEndpoint?: string;
    /**
     * Type or category of the service, e.g., 'BatteryDataService'.
     * @type {string}
     * @memberof CoreDidSchema
     */
    type?: string;
}
/**
 * 
 * @export
 * @interface CoreProof
 */
export interface CoreProof {
    /**
     * The timestamp, when the proof was created.
     * @type {string}
     * @memberof CoreProof
     */
    created?: string;
    /**
     * Signature of the Verifiable Credential.
     * @type {string}
     * @memberof CoreProof
     */
    jws?: string;
    /**
     * The purpose for which the proof is provided
     * @type {CoreProofPurpose}
     * @memberof CoreProof
     */
    proofPurpose?: CoreProofPurpose;
    /**
     * The type of the digital signature used.
     * @type {CoreProofType}
     * @memberof CoreProof
     */
    type?: CoreProofType;
    /**
     * The DID that identifies the public key used to verify the signature.
     * @type {string}
     * @memberof CoreProof
     */
    verificationMethod?: string;
}



/**
 * 
 * @export
 */
export const CoreProofPurpose = {
    AssertionMethod: 'assertionMethod'
} as const;
export type CoreProofPurpose = typeof CoreProofPurpose[keyof typeof CoreProofPurpose];


/**
 * 
 * @export
 */
export const CoreProofType = {
    EcdsaSecp256R1Signature2019: 'EcdsaSecp256r1Signature2019'
} as const;
export type CoreProofType = typeof CoreProofType[keyof typeof CoreProofType];

/**
 * 
 * @export
 * @interface CorePublicKey
 */
export interface CorePublicKey {
    /**
     * DID that has the ability to make changes to this DID-Document.
     * @type {string}
     * @memberof CorePublicKey
     */
    controller?: string;
    /**
     * Identifier for the verification method, typically a DID fragment.
     * @type {string}
     * @memberof CorePublicKey
     */
    id?: string;
    /**
     * The public key encoded in multibase format.
     * @type {string}
     * @memberof CorePublicKey
     */
    publicKeyMultibase?: string;
    /**
     * Type of the verification method, e.g., 'Ed25519VerificationKey2020'.
     * @type {string}
     * @memberof CorePublicKey
     */
    type?: string;
}
/**
 * 
 * @export
 * @interface CoreVCRecord
 */
export interface CoreVCRecord {
    /**
     * Expiration Date of the related Verifiable Credential
     * @type {string}
     * @memberof CoreVCRecord
     */
    expirationDate?: string;
    /**
     * The identifier of the Verifiable Credential.
     * @type {string}
     * @memberof CoreVCRecord
     */
    id?: string;
    /**
     * Timestamp when the record was created or updated.
     * @type {string}
     * @memberof CoreVCRecord
     */
    timestamp?: string;
    /**
     * A SHA-256 hash of the complete VC in hexadecimal format.
     * @type {string}
     * @memberof CoreVCRecord
     */
    vcHash?: string;
}
/**
 * 
 * @export
 * @interface CoreVc
 */
export interface CoreVc {
    /**
     * Defines the JSON-LD context, providing meaning to terms used in the credential.
     * @type {CoreContext}
     * @memberof CoreVc
     */
    context?: CoreContext;
    /**
     * The subject of the credential, which must match one of the predefined claim types.
     * @type {CoreBmsProduction}
     * @memberof CoreVc
     */
    credentialSubject?: CoreBmsProduction;
    /**
     * The date and time after which the credential is no longer valid.
     * @type {string}
     * @memberof CoreVc
     */
    expirationDate?: string;
    /**
     * Identifier of the entity that holds the credential.
     * @type {string}
     * @memberof CoreVc
     */
    holder?: string;
    /**
     * Unique identifier for the Verifiable Credential.
     * @type {string}
     * @memberof CoreVc
     */
    id?: string;
    /**
     * The date and time the credential was issued.
     * @type {string}
     * @memberof CoreVc
     */
    issuanceDate?: string;
    /**
     * Identifier representing the entity that issued the credential.
     * @type {string}
     * @memberof CoreVc
     */
    issuer?: string;
    /**
     * Cryptographic proof that makes the credential verifiable.
     * @type {CoreProof}
     * @memberof CoreVc
     */
    proof?: CoreProof;
    /**
     * Specifies the type(s) of the credential, must include 'VerifiableCredential'.
     * @type {Array<string>}
     * @memberof CoreVc
     */
    type?: Array<string>;
}
/**
 * 
 * @export
 * @interface DomainBlockResponse
 */
export interface DomainBlockResponse {
    /**
     * Hash is the cryptographic hash of this block.
     * @type {string}
     * @memberof DomainBlockResponse
     */
    hash?: string;
    /**
     * Index is the position of the block in the chain.
     * @type {number}
     * @memberof DomainBlockResponse
     */
    id?: number;
    /**
     * MerkleRoot holds the fingerprint of the whole merkle tree
     * @type {string}
     * @memberof DomainBlockResponse
     */
    merkleRoot?: string;
    /**
     * PreviousBlockHash is the hash of the prior block.
     * @type {string}
     * @memberof DomainBlockResponse
     */
    previousBlockHash?: string;
    /**
     * Timestamp is when the block was created.
     * @type {string}
     * @memberof DomainBlockResponse
     */
    timestamp?: string;
}
/**
 * 
 * @export
 * @interface DomainCreateDid
 */
export interface DomainCreateDid {
    /**
     * Public key information used for verifying signatures and authentication.
     * @type {DomainPublicKey}
     * @memberof DomainCreateDid
     */
    publicKey?: DomainPublicKey;
    /**
     * Optional array of service endpoints related to the DID subject, such as APIs or metadata
     * services.
     * @type {Array<DomainDidSchema>}
     * @memberof DomainCreateDid
     */
    service?: Array<DomainDidSchema>;
}
/**
 * 
 * @export
 * @interface DomainDidSchema
 */
export interface DomainDidSchema {
    /**
     * The actual service endpoint, which can be a URL.
     * @type {string}
     * @memberof DomainDidSchema
     */
    serviceEndpoint?: string;
    /**
     * Type or category of the service, e.g., 'BatteryDataService'.
     * @type {string}
     * @memberof DomainDidSchema
     */
    type?: string;
}
/**
 * 
 * @export
 * @interface DomainErrorResponseHTTP
 */
export interface DomainErrorResponseHTTP {
    /**
     * Message contains the human-readable error message.
     * @type {string}
     * @memberof DomainErrorResponseHTTP
     */
    message?: string;
}
/**
 * 
 * @export
 * @interface DomainPublicKey
 */
export interface DomainPublicKey {
    /**
     * DID that have the ability to make changes to this DID-Document.
     * @type {string}
     * @memberof DomainPublicKey
     */
    controller?: string;
    /**
     * The public key encoded in multibase format.
     * @type {string}
     * @memberof DomainPublicKey
     */
    publicKeyMultibase?: string;
    /**
     * Type of the verification method, e.g., 'Ed25519VerificationKey2020'.
     * @type {string}
     * @memberof DomainPublicKey
     */
    type?: string;
}
