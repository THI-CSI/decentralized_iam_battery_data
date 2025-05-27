import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Api } from "@/api/api.tsx";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table.tsx";

/**
 * Component that renders an overview of recent blocks.
 *
 * @remarks
 * - Displays block index, timestamp, and hash in a table.
 * - Each row is clickable and navigates to a detailed block view.
 * - Uses a route loader to fetch data from the backend.
 *
 * @returns A table listing blockchain blocks.
 */
export default function BlockOverview() {
    const navigate = useNavigate();

    const data = Route.useLoaderData();
    if (!data) {
        return <h1>Loading ...</h1>;
    }
    return (
        <div className={"w-full"}>
            <h2 className={"text-primary mb-6 text-2xl font-semibold"}>Recent Blocks</h2>
            <div className={"overflow-hidden shadow"}>
                <Table>
                    <TableHeader className={"w-full divide-y divide-gray-200"}>
                        <TableRow className={"bg-primary/10 hover:bg-primary/10"}>
                            <TableHead>Index</TableHead>
                            <TableHead>Timestamp</TableHead>
                            <TableHead>Hash</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {data.map((block) => (
                            <TableRow
                                className={"hover:cursor-pointer"}
                                key={block.id}
                                onClick={() =>
                                    navigate({
                                        to: "/blocks/$blockId",
                                        params: { blockId: block.id!.toString() },
                                    })
                                }
                            >
                                <TableCell className={"text-sky-600"}>{block.id}</TableCell>
                                <TableCell>{block.timestamp}</TableCell>
                                <TableCell>{block.hash}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        </div>
    );
}

/**
 * Route definition for `/blocks/`.
 *
 * @remarks
 * - Loads recent blocks via `Api.block.getAll()`.
 * - Logs fetch errors but does not recover from them (no fallback).
 */
export const Route = createFileRoute("/blocks/")({
    component: BlockOverview,
    loader: async () => await Api.block.getAll().catch((err) => console.error(err)),
});
