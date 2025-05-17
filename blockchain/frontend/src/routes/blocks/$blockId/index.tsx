import { createFileRoute } from "@tanstack/react-router";
import { Api } from "@/api/api.tsx";
import BlockCard from "@/components/block-card.tsx";

/**
 * The overview over a single block of the application
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
                        className={
                            "bg-primary/2 h-fit w-full rounded-lg p-6 shadow-xl dark:bg-zinc-900 dark:text-white"
                        }
                    >
                        <pre className={"text-sm"}>{JSON.stringify(tx, null, 2)}</pre>
                    </div>
                ))}
            </div>
        </div>
    );
}

export const Route = createFileRoute("/blocks/$blockId/")({
    component: SingleBlockOverview,

    loader: async ({ params }) => {
        const blockId = parseInt(params.blockId);
        const block = await Api.block.getSingle({ blockId }).catch((err) => console.error(err));
        const transaction = await Api.block.getTransaction({ blockId }).catch((err) => console.error(err));
        return { block, transaction };
    },
});
