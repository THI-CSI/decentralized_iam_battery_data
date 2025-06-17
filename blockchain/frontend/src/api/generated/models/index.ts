/* tslint:disable */
/* eslint-disable */
/**
 * Minimal on-chain DID record with a revocation tag.
 * @export
 * @interface DidSchema
 */
export interface DidSchema {
    /**
     * Defines the JSON-LD context, providing meaning to terms used in the did.
     * @type {Set<string>}
     * @memberof DidSchema
     */
    context: Set<DidSchemaContextEnum>;
    /**
     * DID string with the DID method `batterypass` followed by one of `eu, oem, cloud, bms, service` and then an identifier
     * @type {string}
     * @memberof DidSchema
     */
    id: string;
    /**
     * Public key information used for verifying signatures and authentication.
     * @type {VerificationMethod}
     * @memberof DidSchema
     */
    verificationMethod: VerificationMethod;
    /**
     * Optional array of service endpoints related to the DID subject, such as APIs or metadata services.
     * @type {Array<ServiceEndpoint>}
     * @memberof DidSchema
     */
    service?: Array<ServiceEndpoint>;
    /**
     * 
     * @type {string}
     * @memberof DidSchema
     */
    timestamp: string;
    /**
     * Boolean flag indicating whether this DID has been revoked.
     * @type {boolean}
     * @memberof DidSchema
     */
    revoked: boolean;
}


/**
 * @export
 */
export const DidSchemaContextEnum = {
    https___www_w3_org_2018_credentials_v1: 'https://www.w3.org/2018/credentials/v1',
    http___localhost_8443_docs_did_schema_html: 'http://localhost:8443/docs/did.schema.html'
} as const;
export type DidSchemaContextEnum = typeof DidSchemaContextEnum[keyof typeof DidSchemaContextEnum];

/**
 * Cryptographic proof that makes the subject verifiable.
 * @export
 * @interface Proof
 */
export interface Proof {
    /**
     * 
     * @type {string}
     * @memberof Proof
     */
    type: ProofTypeEnum;
    /**
     * 
     * @type {string}
     * @memberof Proof
     */
    created: string;
    /**
     * Reference to the key used to create the proof.
     * @type {string}
     * @memberof Proof
     */
    verificationMethod: string;
    /**
     * 
     * @type {string}
     * @memberof Proof
     */
    proofPurpose: ProofProofPurposeEnum;
    /**
     * The actual signature in JSON Web Signature format
     * @type {string}
     * @memberof Proof
     */
    jws: string;
    /**
     * Optional challenge to prevent replay attacks.
     * @type {string}
     * @memberof Proof
     */
    challenge?: string;
}


/**
 * @export
 */
export const ProofTypeEnum = {
    EcdsaSecp256r1Signature2019: 'EcdsaSecp256r1Signature2019'
} as const;
export type ProofTypeEnum = typeof ProofTypeEnum[keyof typeof ProofTypeEnum];

/**
 * @export
 */
export const ProofProofPurposeEnum = {
    authentication: 'authentication'
} as const;
export type ProofProofPurposeEnum = typeof ProofProofPurposeEnum[keyof typeof ProofProofPurposeEnum];

/**
 * 
 * @export
 * @interface RequestDidCreateormodifySchema
 */
export interface RequestDidCreateormodifySchema {
    /**
     * 
     * @type {Proof}
     * @memberof RequestDidCreateormodifySchema
     */
    proof: Proof;
    /**
     * 
     * @type {DidSchema}
     * @memberof RequestDidCreateormodifySchema
     */
    payload: DidSchema;
}
/**
 * 
 * @export
 * @interface RequestDidRevokeSchema
 */
export interface RequestDidRevokeSchema {
    /**
     * 
     * @type {Proof}
     * @memberof RequestDidRevokeSchema
     */
    proof: Proof;
    /**
     * DID string with the DID method `batterypass` followed by one of `eu, oem, cloud, bms, service` and then an identifier
     * @type {string}
     * @memberof RequestDidRevokeSchema
     */
    payload: string;
}
/**
 * @type RequestVcCreateSchema
 * Schema for creating a new Verifiable Credential, supporting different credential types.
 * @export
 */
export type RequestVcCreateSchema = VcBmsProducedSchema | VcCloudInstanceSchema | VcServiceAccessSchema;
/**
 * 
 * @export
 * @interface RequestVcRevokeSchema
 */
export interface RequestVcRevokeSchema {
    /**
     * 
     * @type {Proof}
     * @memberof RequestVcRevokeSchema
     */
    proof: Proof;
    /**
     * An identifier in uri format for Verifiable Credentials
     * @type {string}
     * @memberof RequestVcRevokeSchema
     */
    payload: string;
}
/**
 * 
 * @export
 * @interface ResponseBlockSchema
 */
export interface ResponseBlockSchema {
    /**
     * 
     * @type {number}
     * @memberof ResponseBlockSchema
     */
    Index: number;
    /**
     * 
     * @type {string}
     * @memberof ResponseBlockSchema
     */
    Timestamp: string;
    /**
     * A SHA-256 hash of the complete VC in hexadecimal format.
     * @type {string}
     * @memberof ResponseBlockSchema
     */
    Hash: string;
    /**
     * A SHA-256 hash of the complete VC in hexadecimal format.
     * @type {string}
     * @memberof ResponseBlockSchema
     */
    PreviousBlockHash: string;
    /**
     * An array holding transactions contained in a block (DID Documents, VC Records)
     * @type {Array<ResponseTransactionsSchemaInner>}
     * @memberof ResponseBlockSchema
     */
    Transactions: Array<ResponseTransactionsSchemaInner>;
    /**
     * A SHA-256 hash of the complete VC in hexadecimal format.
     * @type {string}
     * @memberof ResponseBlockSchema
     */
    MerkleRoot: string;
}
/**
 * A standard error response structure for HTTP APIs.
 * @export
 * @interface ResponseErrorSchema
 */
export interface ResponseErrorSchema {
    /**
     * A human-readable error message.
     * @type {string}
     * @memberof ResponseErrorSchema
     */
    message: string;
    /**
     * Optional detailed information about the error, typically for validation failures.
     * @type {Array<ResponseErrorSchemaDetailsInner>}
     * @memberof ResponseErrorSchema
     */
    details?: Array<ResponseErrorSchemaDetailsInner>;
}
/**
 * 
 * @export
 * @interface ResponseErrorSchemaDetailsInner
 */
export interface ResponseErrorSchemaDetailsInner {
    /**
     * The specific field or path in the request/response that caused the error (e.g., 'name', '/address/street').
     * @type {string}
     * @memberof ResponseErrorSchemaDetailsInner
     */
    field: string;
    /**
     * A specific description of the validation error.
     * @type {string}
     * @memberof ResponseErrorSchemaDetailsInner
     */
    description: string;
    /**
     * The type of validation rule that failed (e.g., 'pattern', 'required', 'minimum').
     * @type {string}
     * @memberof ResponseErrorSchemaDetailsInner
     */
    type?: string;
    /**
     * The problematic value that caused the validation error, formatted as a string.
     * @type {string}
     * @memberof ResponseErrorSchemaDetailsInner
     */
    value?: string;
    /**
     * The JSON pointer to the location within the data structure where the error occurred (e.g., '/items/0/properties/amount').
     * @type {string}
     * @memberof ResponseErrorSchemaDetailsInner
     */
    context?: string;
}
/**
 * A standard OK response structure for HTTP APIs.
 * @export
 * @interface ResponseOkSchema
 */
export interface ResponseOkSchema {
    /**
     * A human-readable confirmation message.
     * @type {string}
     * @memberof ResponseOkSchema
     */
    message: string;
}
/**
 * @type ResponseTransactionsSchemaInner
 * 
 * @export
 */
export type ResponseTransactionsSchemaInner = DidSchema | VcRecordSchema;
/**
 * Represents a service associated with the DID subject, such as a metadata or data access point.
 * @export
 * @interface ServiceEndpoint
 */
export interface ServiceEndpoint {
    /**
     * Identifier for the service endpoint, typically a DID fragment.
     * @type {string}
     * @memberof ServiceEndpoint
     */
    id: string;
    /**
     * Type or category of the service, e.g., 'BatteryDataService'.
     * @type {string}
     * @memberof ServiceEndpoint
     */
    type: string;
    /**
     * The actual service endpoint, which can be a URL.
     * @type {string}
     * @memberof ServiceEndpoint
     */
    serviceEndpoint: string;
}
/**
 * Schema for verifying BMS Production claims.
 * @export
 * @interface VcBmsProducedSchema
 */
export interface VcBmsProducedSchema {
    [key: string]: any | any;
    /**
     * Defines the JSON-LD context, providing meaning to terms used in the credential.
     * @type {Set<string>}
     * @memberof VcBmsProducedSchema
     */
    context: Set<VcBmsProducedSchemaContextEnum>;
    /**
     * 
     * @type {string}
     * @memberof VcBmsProducedSchema
     */
    id: string;
    /**
     * 
     * @type {Set<string>}
     * @memberof VcBmsProducedSchema
     */
    type: Set<string>;
    /**
     * DID string with the DID method `batterypass` for a specific bms and then an identifier
     * @type {string}
     * @memberof VcBmsProducedSchema
     */
    issuer: string;
    /**
     * DID string with the DID method `batterypass` for a specific oem and then an identifier
     * @type {string}
     * @memberof VcBmsProducedSchema
     */
    holder: string;
    /**
     * 
     * @type {string}
     * @memberof VcBmsProducedSchema
     */
    issuanceDate: string;
    /**
     * 
     * @type {string}
     * @memberof VcBmsProducedSchema
     */
    expirationDate: string;
    /**
     * 
     * @type {VcBmsProducedSchemaCredentialSubject}
     * @memberof VcBmsProducedSchema
     */
    credentialSubject: VcBmsProducedSchemaCredentialSubject;
    /**
     * 
     * @type {Proof}
     * @memberof VcBmsProducedSchema
     */
    proof: Proof;
}


/**
 * @export
 */
export const VcBmsProducedSchemaContextEnum = {
    https___www_w3_org_2018_credentials_v1: 'https://www.w3.org/2018/credentials/v1',
    http___localhost_8443_docs_vc_bmsProduction_schema_html: 'http://localhost:8443/docs/vc.bmsProduction.schema.html'
} as const;
export type VcBmsProducedSchemaContextEnum = typeof VcBmsProducedSchemaContextEnum[keyof typeof VcBmsProducedSchemaContextEnum];

/**
 * 
 * @export
 * @interface VcBmsProducedSchemaCredentialSubject
 */
export interface VcBmsProducedSchemaCredentialSubject {
    /**
     * An identifier in uri format for Verifiable Credentials
     * @type {string}
     * @memberof VcBmsProducedSchemaCredentialSubject
     */
    id: string;
    /**
     * 
     * @type {string}
     * @memberof VcBmsProducedSchemaCredentialSubject
     */
    type: string;
    /**
     * DID string with the DID method `batterypass` for a specific bms and then an identifier
     * @type {string}
     * @memberof VcBmsProducedSchemaCredentialSubject
     */
    bmsDid: string;
    /**
     * 
     * @type {string}
     * @memberof VcBmsProducedSchemaCredentialSubject
     */
    timestamp: string;
    /**
     * 
     * @type {string}
     * @memberof VcBmsProducedSchemaCredentialSubject
     */
    lotNumber: string;
}
/**
 * Schema for verifying which cloud instances a BMS should send its battery data to.
 * @export
 * @interface VcCloudInstanceSchema
 */
export interface VcCloudInstanceSchema {
    [key: string]: any | any;
    /**
     * Defines the JSON-LD context, providing meaning to terms used in the credential.
     * @type {Set<string>}
     * @memberof VcCloudInstanceSchema
     */
    context: Set<VcCloudInstanceSchemaContextEnum>;
    /**
     * 
     * @type {string}
     * @memberof VcCloudInstanceSchema
     */
    id: string;
    /**
     * 
     * @type {Set<string>}
     * @memberof VcCloudInstanceSchema
     */
    type: Set<string>;
    /**
     * DID string with the DID method `batterypass` for a specific oem and then an identifier
     * @type {string}
     * @memberof VcCloudInstanceSchema
     */
    issuer: string;
    /**
     * DID string with the DID method `batterypass` for a specific bms and then an identifier
     * @type {string}
     * @memberof VcCloudInstanceSchema
     */
    holder: string;
    /**
     * 
     * @type {string}
     * @memberof VcCloudInstanceSchema
     */
    issuanceDate: string;
    /**
     * 
     * @type {string}
     * @memberof VcCloudInstanceSchema
     */
    expirationDate: string;
    /**
     * 
     * @type {VcCloudInstanceSchemaCredentialSubject}
     * @memberof VcCloudInstanceSchema
     */
    credentialSubject: VcCloudInstanceSchemaCredentialSubject;
    /**
     * 
     * @type {Proof}
     * @memberof VcCloudInstanceSchema
     */
    proof: Proof;
}


/**
 * @export
 */
export const VcCloudInstanceSchemaContextEnum = {
    https___www_w3_org_2018_credentials_v1: 'https://www.w3.org/2018/credentials/v1',
    http___localhost_8443_docs_vc_cloudInstance_schema_html: 'http://localhost:8443/docs/vc.cloudInstance.schema.html'
} as const;
export type VcCloudInstanceSchemaContextEnum = typeof VcCloudInstanceSchemaContextEnum[keyof typeof VcCloudInstanceSchemaContextEnum];

/**
 * 
 * @export
 * @interface VcCloudInstanceSchemaCredentialSubject
 */
export interface VcCloudInstanceSchemaCredentialSubject {
    /**
     * An identifier in uri format for Verifiable Credentials
     * @type {string}
     * @memberof VcCloudInstanceSchemaCredentialSubject
     */
    id: string;
    /**
     * 
     * @type {string}
     * @memberof VcCloudInstanceSchemaCredentialSubject
     */
    type: string;
    /**
     * DID string with the DID method `batterypass` for a specific cloud and then an identifier
     * @type {string}
     * @memberof VcCloudInstanceSchemaCredentialSubject
     */
    cloudDid: string;
    /**
     * 
     * @type {string}
     * @memberof VcCloudInstanceSchemaCredentialSubject
     */
    timestamp: string;
}
/**
 * Minimal record of a Verifiable Credential containing only its ID, a hash of the VC, a timestamp, and expiration date.
 * @export
 * @interface VcRecordSchema
 */
export interface VcRecordSchema {
    /**
     * An identifier in uri format for Verifiable Credentials
     * @type {string}
     * @memberof VcRecordSchema
     */
    id: string;
    /**
     * A SHA-256 hash of the complete VC in hexadecimal format.
     * @type {string}
     * @memberof VcRecordSchema
     */
    vcHash: string;
    /**
     * 
     * @type {string}
     * @memberof VcRecordSchema
     */
    timestamp: string;
    /**
     * 
     * @type {string}
     * @memberof VcRecordSchema
     */
    expirationDate?: string;
}
/**
 * Schema for verifying Service Access claims.
 * @export
 * @interface VcServiceAccessSchema
 */
export interface VcServiceAccessSchema {
    [key: string]: any | any;
    /**
     * Defines the JSON-LD context, providing meaning to terms used in the credential.
     * @type {Set<string>}
     * @memberof VcServiceAccessSchema
     */
    context: Set<VcServiceAccessSchemaContextEnum>;
    /**
     * 
     * @type {string}
     * @memberof VcServiceAccessSchema
     */
    id: string;
    /**
     * 
     * @type {Set<string>}
     * @memberof VcServiceAccessSchema
     */
    type: Set<string>;
    /**
     * DID string with the DID method `batterypass` for a specific bms and then an identifier
     * @type {string}
     * @memberof VcServiceAccessSchema
     */
    issuer: string;
    /**
     * DID string with the DID method `batterypass` for a specific service and then an identifier
     * @type {string}
     * @memberof VcServiceAccessSchema
     */
    holder: string;
    /**
     * 
     * @type {string}
     * @memberof VcServiceAccessSchema
     */
    issuanceDate: string;
    /**
     * 
     * @type {string}
     * @memberof VcServiceAccessSchema
     */
    expirationDate: string;
    /**
     * 
     * @type {VcServiceAccessSchemaCredentialSubject}
     * @memberof VcServiceAccessSchema
     */
    credentialSubject: VcServiceAccessSchemaCredentialSubject;
    /**
     * 
     * @type {Proof}
     * @memberof VcServiceAccessSchema
     */
    proof: Proof;
}


/**
 * @export
 */
export const VcServiceAccessSchemaContextEnum = {
    https___www_w3_org_2018_credentials_v1: 'https://www.w3.org/2018/credentials/v1',
    http___localhost_8443_docs_vc_serviceAccess_schema_html: 'http://localhost:8443/docs/vc.serviceAccess.schema.html'
} as const;
export type VcServiceAccessSchemaContextEnum = typeof VcServiceAccessSchemaContextEnum[keyof typeof VcServiceAccessSchemaContextEnum];

/**
 * 
 * @export
 * @interface VcServiceAccessSchemaCredentialSubject
 */
export interface VcServiceAccessSchemaCredentialSubject {
    /**
     * An identifier in uri format for Verifiable Credentials
     * @type {string}
     * @memberof VcServiceAccessSchemaCredentialSubject
     */
    id: string;
    /**
     * 
     * @type {string}
     * @memberof VcServiceAccessSchemaCredentialSubject
     */
    type: string;
    /**
     * DID string with the DID method `batterypass` for a specific bms and then an identifier
     * @type {string}
     * @memberof VcServiceAccessSchemaCredentialSubject
     */
    bmsDid: string;
    /**
     * 
     * @type {Array<string>}
     * @memberof VcServiceAccessSchemaCredentialSubject
     */
    accessLevel: Array<VcServiceAccessSchemaCredentialSubjectAccessLevelEnum>;
    /**
     * 
     * @type {string}
     * @memberof VcServiceAccessSchemaCredentialSubject
     */
    validFrom: string;
    /**
     * 
     * @type {string}
     * @memberof VcServiceAccessSchemaCredentialSubject
     */
    validUntil: string;
}


/**
 * @export
 */
export const VcServiceAccessSchemaCredentialSubjectAccessLevelEnum = {
    read: 'read',
    write: 'write'
} as const;
export type VcServiceAccessSchemaCredentialSubjectAccessLevelEnum = typeof VcServiceAccessSchemaCredentialSubjectAccessLevelEnum[keyof typeof VcServiceAccessSchemaCredentialSubjectAccessLevelEnum];

/**
 * A method by which a DID subject can be authenticated, typically using cryptographic keys.
 * @export
 * @interface VerificationMethod
 */
export interface VerificationMethod {
    /**
     * Identifier for the verification method, typically a DID fragment.
     * @type {string}
     * @memberof VerificationMethod
     */
    id: string;
    /**
     * Type of the verification method, e.g., 'Ed25519VerificationKey2020'.
     * @type {string}
     * @memberof VerificationMethod
     */
    type: string;
    /**
     * DID that has the ability to make changes to this DID-Document.
     * @type {string}
     * @memberof VerificationMethod
     */
    controller: string;
    /**
     * The public key encoded in multibase format.
     * @type {string}
     * @memberof VerificationMethod
     */
    publicKeyMultibase: string;
}
/**
 * Schema for verifying presentations of VCs with holder proof.
 * @export
 * @interface VpSchema
 */
export interface VpSchema {
    /**
     * Defines the JSON-LD context, providing meaning to terms used in the credential.
     * @type {Set<string>}
     * @memberof VpSchema
     */
    context: Set<VpSchemaContextEnum>;
    /**
     * 
     * @type {Array<string>}
     * @memberof VpSchema
     */
    type: Array<string>;
    /**
     * 
     * @type {Array<RequestVcCreateSchema>}
     * @memberof VpSchema
     */
    verifiableCredential: Array<RequestVcCreateSchema>;
    /**
     * DID string with the DID method `batterypass` followed by one of `eu, oem, cloud, bms, service` and then an identifier
     * @type {string}
     * @memberof VpSchema
     */
    holder: string;
    /**
     * 
     * @type {Proof}
     * @memberof VpSchema
     */
    proof: Proof;
}


/**
 * @export
 */
export const VpSchemaContextEnum = {
    https___www_w3_org_2018_credentials_v1: 'https://www.w3.org/2018/credentials/v1',
    http___localhost_8443_docs_vp_schema_html: 'http://localhost:8443/docs/vp.schema.html'
} as const;
export type VpSchemaContextEnum = typeof VpSchemaContextEnum[keyof typeof VpSchemaContextEnum];

