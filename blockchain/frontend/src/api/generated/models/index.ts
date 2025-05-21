/* tslint:disable */
/* eslint-disable */

/**
 * 
 * @export
 */
export const CoreContext = {
    HTTPLocalhost8443DocsDidSchemaHTML: 'http://localhost:8443/docs/did.schema.html',
    HTTPSWWWW3Org2018CredentialsV1: 'https://www.w3.org/2018/credentials/v1'
} as const;
export type CoreContext = typeof CoreContext[keyof typeof CoreContext];

/**
 * 
 * @export
 * @interface CoreDid
 */
export interface CoreDid {
    /**
     * Defines the JSON-LD context, providing meaning to terms used in the did.
     * @type {Array<CoreContext>}
     * @memberof CoreDid
     */
    context?: Array<CoreContext>;
    /**
     * Decentralized Identifier (DID) for the entity, following the DID syntax.
     * @type {string}
     * @memberof CoreDid
     */
    id?: string;
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
    /**
     * Public key information used for verifying signatures and authentication.
     * @type {CoreVerificationMethod}
     * @memberof CoreDid
     */
    verificationMethod?: CoreVerificationMethod;
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
 * @interface CoreVerificationMethod
 */
export interface CoreVerificationMethod {
    /**
     * DID that has the ability to make changes to this DID-Document.
     * @type {string}
     * @memberof CoreVerificationMethod
     */
    controller?: string;
    /**
     * Identifier for the verification method, typically a DID fragment.
     * @type {string}
     * @memberof CoreVerificationMethod
     */
    id?: string;
    /**
     * The public key encoded in multibase format.
     * @type {string}
     * @memberof CoreVerificationMethod
     */
    publicKeyMultibase?: string;
    /**
     * Type of the verification method, e.g., 'Ed25519VerificationKey2020'.
     * @type {string}
     * @memberof CoreVerificationMethod
     */
    type?: string;
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
    publicKey: DomainPublicKey;
    /**
     * Optional array of service endpoints related to the DID subject, such as APIs or metadata
     * services.
     * @type {Array<DomainDidSchema>}
     * @memberof DomainCreateDid
     */
    service: Array<DomainDidSchema>;
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
    serviceEndpoint: string;
    /**
     * Type or category of the service, e.g., 'BatteryDataService'.
     * @type {string}
     * @memberof DomainDidSchema
     */
    type: string;
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
    controller: string;
    /**
     * The public key encoded in multibase format.
     * @type {string}
     * @memberof DomainPublicKey
     */
    publicKeyMultibase: string;
    /**
     * Type of the verification method, e.g., 'Ed25519VerificationKey2020'.
     * @type {string}
     * @memberof DomainPublicKey
     */
    type: string;
}
/**
 * 
 * @export
 * @interface DomainVCRequest
 */
export interface DomainVCRequest {
    /**
     * Expiration Date of the related Verifiable Credential
     * @type {string}
     * @memberof DomainVCRequest
     */
    expirationDate: string;
    /**
     * The identifier of the Verifiable Credential.
     * @type {string}
     * @memberof DomainVCRequest
     */
    id: string;
    /**
     * A SHA-256 hash of the complete VC in hexadecimal format.
     * @type {string}
     * @memberof DomainVCRequest
     */
    vcHash: string;
}
