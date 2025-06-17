import type { ResponseBlockSchema } from "@/api/generated";

/**
 * The properties for {@link BlockCard}
 */
export type BlockCardProps = {
    block: ResponseBlockSchema;
};

/**
 * A UI card component that displays details for a single blockchain block.
 *
 * @remarks
 * This component shows:
 * - Block ID
 * - Block Hash
 * - Previous Block Hash
 * - Timestamp
 * - Merkle Root
 *
 * It's designed for both light and dark themes and uses a responsive layout.
 *
 * @param props - Component props containing block metadata
 * @returns A styled block info card
 */
export default function BlockCard(props: BlockCardProps) {
    return (
        <div className={"bg-primary/2 h-fit w-full rounded-lg p-6 shadow dark:bg-zinc-900 dark:text-white"}>
            <h2 className={"text-primary mb-6 text-2xl font-semibold"}>Block #{props.block.Index}</h2>
            <div className={"grid grid-cols-1 gap-2 xl:grid-cols-2 xl:gap-4"}>
                <div className={"flex items-center gap-2 xl:flex-col xl:items-start xl:gap-0"}>
                    <h3 className={"text-lg font-semibold"}>Block Hash:</h3>
                    <span className={"text-sm"}>{props.block.Hash}</span>
                </div>
                <div className={"flex items-center gap-2 xl:flex-col xl:items-start xl:gap-0"}>
                    <h3 className={"text-lg font-semibold"}>Previous Block Hash:</h3>
                    <span className={"text-sm"}>{props.block.PreviousBlockHash}</span>
                </div>
                <div className={"flex items-center gap-2 xl:flex-col xl:items-start xl:gap-0"}>
                    <h3 className={"text-lg font-semibold"}>Timestamp:</h3>
                    <span className={"text-sm"}>{props.block.Timestamp}</span>
                </div>
                <div className={"flex items-center gap-2 xl:flex-col xl:items-start xl:gap-0"}>
                    <h3 className={"text-lg font-semibold"}>MerkleRoot:</h3>
                    <span className={"text-sm"}>{props.block.MerkleRoot}</span>
                </div>
            </div>
        </div>
    );
}
