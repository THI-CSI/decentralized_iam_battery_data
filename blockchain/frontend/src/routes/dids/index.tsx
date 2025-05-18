import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Api } from "@/api/api.tsx";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table.tsx";
import { Badge } from "@/components/ui/badge.tsx";

export function DidOverview() {
    const navigate = useNavigate();

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
                        <TableRow className={"bg-primary/10 hover:bg-primary/10"}>
                            <TableHead>Did</TableHead>
                            <TableHead>Status</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {data.map((did) => (
                            <TableRow
                                className={"hover:cursor-pointer"}
                                key={did.id}
                                onClick={() =>
                                    navigate({
                                        to: "/dids/$didId",
                                        params: { didId: encodeURI(did.id!) },
                                    })
                                }
                            >
                                <TableCell className={"text-sky-600"}>{did.id}</TableCell>
                                <TableCell>
                                    {did.revoked ? (
                                        <Badge variant={"destructive"}>revoked</Badge>
                                    ) : (
                                        <Badge variant={"secondary"}>active</Badge>
                                    )}
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
