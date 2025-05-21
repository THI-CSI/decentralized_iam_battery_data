import { createFileRoute } from "@tanstack/react-router";
import { Api } from "@/api/api.tsx";
import { Table, TableBody, TableCell, TableRow } from "@/components/ui/table.tsx";

/**
 * The overview over a single Did
 */
export default function SingleDidOverview() {
    const data = Route.useLoaderData();
    if (!data) {
        return <h1>Loading ...</h1>;
    }
    return (
        <div className={"flex w-full flex-col gap-8"}>
            <div
                className={
                    "bg-primary/2 flex h-fit w-full items-center gap-2 rounded-lg p-6 shadow dark:bg-zinc-900 dark:text-white"
                }
            >
                <h3 className={"font-semibold"}>DID Details for:</h3>
                <span className={"text-lg font-bold"}>{data.id}</span>
            </div>
            <div>
                <h2 className={"text-primary text-2xl font-semibold"}>Related Transactions</h2>

                <div className={"bg-primary/2 h-fit w-full rounded-lg p-6 shadow dark:bg-zinc-900 dark:text-white"}>
                    <h3 className={"text-lg font-semibold"}>Public Key:</h3>
                    <Table>
                        <TableBody>
                            <TableRow>
                                <TableCell>Controller:</TableCell>
                                <TableCell>{data.verificationMethod!.controller}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Id:</TableCell>
                                <TableCell>{data.verificationMethod!.id}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Public key multi base:</TableCell>
                                <TableCell>{data.verificationMethod!.publicKeyMultibase}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Type:</TableCell>
                                <TableCell>{data.verificationMethod!.type}</TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </div>
                {data.service!.map((service, i) => (
                    <div
                        key={service.id}
                        className={"bg-primary/2 h-fit w-full rounded-lg p-6 shadow dark:bg-zinc-900 dark:text-white"}
                    >
                        <h3 className={"text-lg font-semibold"}>Service: {i + 1}</h3>
                        <Table>
                            <TableBody>
                                <>
                                    <TableRow>
                                        <TableCell>Id:</TableCell>
                                        <TableCell>{service.id}</TableCell>
                                    </TableRow>
                                    <TableRow>
                                        <TableCell>Service Endpoint:</TableCell>
                                        <TableCell>{service!.serviceEndpoint}</TableCell>
                                    </TableRow>
                                    <TableRow>
                                        <TableCell>Type:</TableCell>
                                        <TableCell>{service.type}</TableCell>
                                    </TableRow>
                                </>
                            </TableBody>
                        </Table>
                    </div>
                ))}
            </div>
        </div>
    );
}

export const Route = createFileRoute("/dids/$didId/")({
    component: SingleDidOverview,
    loader: async ({ params }) => {
        console.log(params.didId);
        return await Api.did.getSingle({ did: params.didId }).catch((err) => console.error(err));
    },
});
