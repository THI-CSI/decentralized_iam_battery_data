import { createFileRoute, Link } from "@tanstack/react-router";
import { Api } from "@/api/api.tsx";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table.tsx";
import { Badge } from "@/components/ui/badge.tsx";

/**
 * The DID overview of the application
 */
export default function DidOverview() {
    const data = Route.useLoaderData();
    if (!data) {
        return <h1>Loading ...</h1>;
    }
    return (
        <div className={"w-full"}>
            <h2 className={"text-primary mb-6 text-2xl font-semibold"}>All Unique DIDs</h2>
            <div className={"overflow-hidden shadow"}>
                <Table>
                    <TableHeader className={"w-full divide-y divide-gray-200"}>
                        <TableRow className={"bg-primary/10"}>
                            <TableHead>Did</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Details</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {data.map((did) => (
                            <TableRow key={did.id}>
                                <TableCell className={"text-sky-600"}>{did.id}</TableCell>
                                <TableCell>
                                    {did.revoked ? (
                                        <Badge>active</Badge>
                                    ) : (
                                        <Badge variant={"destructive"}>revoked</Badge>
                                    )}
                                </TableCell>
                                <TableCell>
                                    <Link
                                        className={"text-sky-600 hover:text-sky-800"}
                                        to={"/dids/$didId"}
                                        params={{ didId: encodeURI(did.id!) }}
                                    >
                                        Details
                                    </Link>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        </div>
    );
}

export const Route = createFileRoute("/dids/")({
    component: DidOverview,
    loader: async () => await Api.did.getAll().catch((err) => console.error(err)),
});
