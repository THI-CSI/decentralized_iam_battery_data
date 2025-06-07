import {
    BlocksApi,
    Configuration,
    DIDsApi,
    type GetBlockByIdRequest,
    type GetBlockTransactionsRequest,
    type GetDidByIdRequest,
    type GetVcRecordByIdRequest,
    VCApi
} from "@/api/generated";

const configuration = new Configuration({
    basePath: window.location.origin
});

const didApi = new DIDsApi(configuration);
const blockApi = new BlocksApi(configuration);
const vcApi = new VCApi(configuration);

export const Api = {
    did: {
        getAll: () => didApi.getAllDids(),
        getSingle: (request: GetDidByIdRequest) => didApi.getDidById(request)
    },
    vc: {
        get: (request: GetVcRecordByIdRequest) => vcApi.getVcRecordById(request)
    },
    block: {
        getAll: () => blockApi.getAllBlocks(),
        getSingle: (request: GetBlockByIdRequest) => blockApi.getBlockById(request),
        getTransaction: (request: GetBlockTransactionsRequest) =>
            blockApi.getBlockTransactions(request)
    }
};
