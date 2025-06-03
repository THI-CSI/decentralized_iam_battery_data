/* tslint:disable */
/* eslint-disable */
/**
 * 
 * @export
 * @interface BatterypassApiService
 */
export interface BatterypassApiService {
    /**
     * 
     * @type {string}
     * @memberof BatterypassApiService
     */
    id: string;
    /**
     * 
     * @type {any}
     * @memberof BatterypassApiService
     */
    type: any | null;
    /**
     * 
     * @type {string}
     * @memberof BatterypassApiService
     */
    serviceEndpoint: string;
}
/**
 * 
 * @export
 * @interface CreateOrModifyDid201Response
 */
export interface CreateOrModifyDid201Response {
    /**
     * 
     * @type {string}
     * @memberof CreateOrModifyDid201Response
     */
    message?: CreateOrModifyDid201ResponseMessageEnum;
}


/**
 * @export
 */
export const CreateOrModifyDid201ResponseMessageEnum = {
    DID_created: 'DID created',
    DID_modified: 'DID modified'
} as const;
export type CreateOrModifyDid201ResponseMessageEnum = typeof CreateOrModifyDid201ResponseMessageEnum[keyof typeof CreateOrModifyDid201ResponseMessageEnum];

/**
 * 
 * @export
 * @interface CreateVcRecord201Response
 */
export interface CreateVcRecord201Response {
    /**
     * 
     * @type {string}
     * @memberof CreateVcRecord201Response
     */
    message?: CreateVcRecord201ResponseMessageEnum;
}


/**
 * @export
 */
export const CreateVcRecord201ResponseMessageEnum = {
    VC_Record_written: 'VC Record written'
} as const;
export type CreateVcRecord201ResponseMessageEnum = typeof CreateVcRecord201ResponseMessageEnum[keyof typeof CreateVcRecord201ResponseMessageEnum];

/**
 * 
 * @export
 * @interface CreateVcRecord400Response
 */
export interface CreateVcRecord400Response {
    /**
     * 
     * @type {string}
     * @memberof CreateVcRecord400Response
     */
    error?: string;
}
/**
 * Minimal on-chain DID record with a revocation tag.
 * @export
 * @interface DidSchema
 */
export interface DidSchema {
    /**
     * 
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
     * 
     * @type {VerificationMethod}
     * @memberof DidSchema
     */
    verificationMethod: VerificationMethod;
    /**
     * 
     * @type {Array<DidSchemaServiceInner>}
     * @memberof DidSchema
     */
    service?: Array<DidSchemaServiceInner>;
    /**
     * 
     * @type {string}
     * @memberof DidSchema
     */
    timestamp: string;
    /**
     * A revoked flag indicating if an DID is no longer valid.
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
 * @type DidSchemaServiceInner
 * 
 * @export
 */
export type DidSchemaServiceInner = BatterypassApiService | HandleDidService;
/**
 * 
 * @export
 * @interface HandleDidService
 */
export interface HandleDidService {
    /**
     * 
     * @type {string}
     * @memberof HandleDidService
     */
    id: string;
    /**
     * 
     * @type {any}
     * @memberof HandleDidService
     */
    type: any | null;
    /**
     * 
     * @type {string}
     * @memberof HandleDidService
     */
    serviceEndpoint: string;
}
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
    [key: string]: any | any;
    /**
     * 
     * @type {RequestDidRevokeSchemaProof}
     * @memberof RequestDidRevokeSchema
     */
    proof: RequestDidRevokeSchemaProof;
    /**
     * DID string with the DID method `batterypass` followed by one of `eu, oem, cloud, bms, service` and then an identifier
     * @type {string}
     * @memberof RequestDidRevokeSchema
     */
    payload: string;
}
/**
 * 
 * @export
 * @interface RequestDidRevokeSchemaProof
 */
export interface RequestDidRevokeSchemaProof {
    /**
     * 
     * @type {string}
     * @memberof RequestDidRevokeSchemaProof
     */
    type: RequestDidRevokeSchemaProofTypeEnum;
    /**
     * 
     * @type {string}
     * @memberof RequestDidRevokeSchemaProof
     */
    created: string;
    /**
     * Reference to the key used to create the proof.
     * @type {string}
     * @memberof RequestDidRevokeSchemaProof
     */
    verificationMethod: string;
    /**
     * 
     * @type {string}
     * @memberof RequestDidRevokeSchemaProof
     */
    proofPurpose: RequestDidRevokeSchemaProofProofPurposeEnum;
    /**
     * The actual signature in JSON Web Signature format
     * @type {string}
     * @memberof RequestDidRevokeSchemaProof
     */
    jws: string;
    /**
     * Optional challenge to prevent replay attacks.
     * @type {string}
     * @memberof RequestDidRevokeSchemaProof
     */
    challenge: string;
}


/**
 * @export
 */
export const RequestDidRevokeSchemaProofTypeEnum = {
    EcdsaSecp256r1Signature2019: 'EcdsaSecp256r1Signature2019'
} as const;
export type RequestDidRevokeSchemaProofTypeEnum = typeof RequestDidRevokeSchemaProofTypeEnum[keyof typeof RequestDidRevokeSchemaProofTypeEnum];

/**
 * @export
 */
export const RequestDidRevokeSchemaProofProofPurposeEnum = {
    authentication: 'authentication'
} as const;
export type RequestDidRevokeSchemaProofProofPurposeEnum = typeof RequestDidRevokeSchemaProofProofPurposeEnum[keyof typeof RequestDidRevokeSchemaProofProofPurposeEnum];

/**
 * 
 * @export
 * @interface RequestVcCreateSchema
 */
export interface RequestVcCreateSchema {
    [key: string]: any | any;
    /**
     * 
     * @type {Proof}
     * @memberof RequestVcCreateSchema
     */
    proof: Proof;
    /**
     * 
     * @type {RequestVcCreateSchemaPayload}
     * @memberof RequestVcCreateSchema
     */
    payload: RequestVcCreateSchemaPayload;
}
/**
 * 
 * @export
 * @interface RequestVcCreateSchemaPayload
 */
export interface RequestVcCreateSchemaPayload {
    /**
     * An identifier in uri format for Verifiable Credentials
     * @type {string}
     * @memberof RequestVcCreateSchemaPayload
     */
    id: string;
    /**
     * A SHA-256 or Keccak-256 hash of the complete VC in hexadecimal format.
     * @type {string}
     * @memberof RequestVcCreateSchemaPayload
     */
    _256Hash?: string;
    /**
     * 
     * @type {string}
     * @memberof RequestVcCreateSchemaPayload
     */
    expirationDate?: string;
}
/**
 * 
 * @export
 * @interface RequestVcRevokeSchema
 */
export interface RequestVcRevokeSchema {
    /**
     * An identifier in uri format for Verifiable Credentials
     * @type {string}
     * @memberof RequestVcRevokeSchema
     */
    id: string;
    /**
     * A SHA-256 or Keccak-256 hash of the complete VC in hexadecimal format.
     * @type {string}
     * @memberof RequestVcRevokeSchema
     */
    _256Hash?: string;
}
/**
 * 
 * @export
 * @interface RequestVcVerifySchema
 */
export interface RequestVcVerifySchema {
    /**
     * DID string with the DID method `batterypass` followed by one of `eu, oem, cloud, bms, service` and then an identifier
     * @type {string}
     * @memberof RequestVcVerifySchema
     */
    issuerDID: string;
    /**
     * DID string with the DID method `batterypass` followed by one of `eu, oem, cloud, bms, service` and then an identifier
     * @type {string}
     * @memberof RequestVcVerifySchema
     */
    holderDID: string;
    /**
     * An identifier in uri format for Verifiable Credentials
     * @type {string}
     * @memberof RequestVcVerifySchema
     */
    id: string;
    /**
     * A SHA-256 or Keccak-256 hash of the complete VC in hexadecimal format.
     * @type {string}
     * @memberof RequestVcVerifySchema
     */
    _256Hash: string;
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
    _Index: number;
    /**
     * 
     * @type {string}
     * @memberof ResponseBlockSchema
     */
    Timestamp: string;
    /**
     * A SHA-256 or Keccak-256 hash of the complete VC in hexadecimal format.
     * @type {string}
     * @memberof ResponseBlockSchema
     */
    Hash: string;
    /**
     * A SHA-256 or Keccak-256 hash of the complete VC in hexadecimal format.
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
     * A SHA-256 or Keccak-256 hash of the complete VC in hexadecimal format.
     * @type {string}
     * @memberof ResponseBlockSchema
     */
    MerkleRoot: string;
}
/**
 * @type ResponseTransactionsSchemaInner
 * 
 * @export
 */
export type ResponseTransactionsSchemaInner = DidSchema | VcRecordSchema;
/**
 * 
 * @export
 * @interface ResponseVcVerifySchema
 */
export interface ResponseVcVerifySchema {
    /**
     * 
     * @type {DidSchema}
     * @memberof ResponseVcVerifySchema
     */
    issuerDID: DidSchema;
    /**
     * 
     * @type {DidSchema}
     * @memberof ResponseVcVerifySchema
     */
    holderDID: DidSchema;
    /**
     * Indicates weather the transmitted VC Record is valid.
     * @type {boolean}
     * @memberof ResponseVcVerifySchema
     */
    VCRecord: boolean;
}
/**
 * 
 * @export
 * @interface RevokeDid201Response
 */
export interface RevokeDid201Response {
    /**
     * 
     * @type {string}
     * @memberof RevokeDid201Response
     */
    message?: RevokeDid201ResponseMessageEnum;
}


/**
 * @export
 */
export const RevokeDid201ResponseMessageEnum = {
    DID_revoked: 'DID revoked'
} as const;
export type RevokeDid201ResponseMessageEnum = typeof RevokeDid201ResponseMessageEnum[keyof typeof RevokeDid201ResponseMessageEnum];

/**
 * 
 * @export
 * @interface RevokeVcRecord201Response
 */
export interface RevokeVcRecord201Response {
    /**
     * 
     * @type {string}
     * @memberof RevokeVcRecord201Response
     */
    message?: RevokeVcRecord201ResponseMessageEnum;
}


/**
 * @export
 */
export const RevokeVcRecord201ResponseMessageEnum = {
    VC_Record_revoked: 'VC Record revoked'
} as const;
export type RevokeVcRecord201ResponseMessageEnum = typeof RevokeVcRecord201ResponseMessageEnum[keyof typeof RevokeVcRecord201ResponseMessageEnum];

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
     * A SHA-256 or Keccak-256 hash of the complete VC in hexadecimal format.
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
 * 
 * @export
 * @interface VerificationMethod
 */
export interface VerificationMethod {
    /**
     * 
     * @type {string}
     * @memberof VerificationMethod
     */
    id: string;
    /**
     * 
     * @type {string}
     * @memberof VerificationMethod
     */
    type: string;
    /**
     * 
     * @type {string}
     * @memberof VerificationMethod
     */
    controller: string;
    /**
     * 
     * @type {string}
     * @memberof VerificationMethod
     */
    publicKeyMultibase: string;
}
