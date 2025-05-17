import type { DomainBlockResponse } from "@/api/generated";

/**
 * The properties for {@link BlockCard}
 */
export type BlockCardProps = {
    block: DomainBlockResponse;
};

/**
 * Card for block
 */
export default function BlockCard(props: BlockCardProps) {
    return (
        <div className={"bg-primary/2 h-fit w-full rounded-lg p-6 shadow dark:bg-zinc-900 dark:text-white"}>
            <h2 className={"text-primary mb-6 text-2xl font-semibold"}>Block #{props.block.id}</h2>
            <div className={"grid grid-cols-2 gap-4"}>
                <div>
                    <h3 className={"text-lg font-semibold"}>Block Hash:</h3>
                    <span>{props.block.hash}</span>
                </div>
                <div>
                    <h3 className={"text-lg font-semibold"}>Previous Block Hash:</h3>
                    <span>{props.block.previousBlockHash}</span>
                </div>
                <div>
                    <h3 className={"text-lg font-semibold"}>Timestamp:</h3>
                    <span>{props.block.timestamp}</span>
                </div>
                <div>
                    <h3 className={"text-lg font-semibold"}>MerkleRoot:</h3>
                    <span>{props.block.merkleRoot}</span>
                </div>
            </div>
        </div>
    );
}
