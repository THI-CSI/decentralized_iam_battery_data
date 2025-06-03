import { createFileRoute } from "@tanstack/react-router";
import { Api } from "@/api/api.tsx";
import BlockCard from "@/components/block-card.tsx";

/**
 * Displays detailed information for a single block, including all transactions.
 *
 * @remarks
 * - Uses route loader to fetch both the block metadata and associated transactions.
 * - Renders the block info via {@link BlockCard}.
 * - Transactions are shown in raw JSON format using `<pre>`.
 *
 * @returns A detailed view of a blockchain block.
 */
export default function SingleBlockOverview() {
    const { block, transaction } = Route.useLoaderData();
    if (!block || !transaction) {
        return <h1>Loading ...</h1>;
    }

    return (
        <div className={"flex w-full flex-col gap-8"}>
            <BlockCard block={block} />
            <div className={"flex flex-col gap-2"}>
                <h2 className={"text-primary text-2xl font-semibold"}>Transactions in this Block</h2>
                {transaction.map((tx, i) => (
                    <div
                        key={i}
                        className={"bg-primary/2 h-fit w-full rounded-lg p-6 shadow dark:bg-zinc-900 dark:text-white"}
                    >
                        <pre className={"text-sm"}>{JSON.stringify(tx, null, 2)}</pre>
                    </div>
                ))}
            </div>
        </div>
    );
}

/**
 * Route definition for `/blocks/$blockId/`.
 *
 * @remarks
 * - Parses the `blockId` from route params.
 * - Fetches both the block details and associated transactions in parallel.
 * - Logs any errors to the console but does not prevent rendering.
 */
export const Route = createFileRoute("/blocks/$blockId/")({
    component: SingleBlockOverview,

    loader: async ({ params }) => {
        const blockId = parseInt(params.blockId);
        const block = await Api.block.getSingle({ blockId }).catch((err) => console.error(err));
        const transaction = await Api.block.getTransaction({ blockId }).catch((err) => console.error(err));
        return { block, transaction };
    },
});
