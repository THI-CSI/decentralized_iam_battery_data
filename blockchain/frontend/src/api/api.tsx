import {
    type ApiV1BlocksBlockIdGetRequest,
    type ApiV1BlocksBlockIdTransactionsGetRequest,
    type ApiV1DidsDidGetRequest,
    type ApiV1VcUrnGetRequest,
    BlocksApi,
    Configuration,
    DIDsApi,
    VCsApi,
} from "@/api/generated";

const configuration = new Configuration({
    basePath: window.location.origin,
});

const didApi = new DIDsApi(configuration);
const vcApi = new VCsApi(configuration);
const blockApi = new BlocksApi(configuration);

export const Api = {
    did: {
        getAll: () => didApi.apiV1DidsGet(),
        getSingle: (request: ApiV1DidsDidGetRequest) => didApi.apiV1DidsDidGet(request),
    },
    vc: {
        get: (request: ApiV1VcUrnGetRequest) => vcApi.apiV1VcUrnGet(request),
    },
    block: {
        getAll: () => blockApi.apiV1BlocksGet(),
        getSingle: (request: ApiV1BlocksBlockIdGetRequest) => blockApi.apiV1BlocksBlockIdGet(request),
        getTransaction: (request: ApiV1BlocksBlockIdTransactionsGetRequest) =>
            blockApi.apiV1BlocksBlockIdTransactionsGet(request),
    },
};
