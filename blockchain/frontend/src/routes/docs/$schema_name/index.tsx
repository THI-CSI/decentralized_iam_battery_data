import { createFileRoute } from "@tanstack/react-router";

/**
 * The properties for {@link DocsIframe}
 */
export type DocsIframeProps = {};

/**
 * The docs iframe for the schemas
 */
export default function DocsIframe(_props: DocsIframeProps) {
    const { schema_name } = Route.useParams();
    console.log(schema_name);

    return (
        <div className={"h-full w-full"}>
            <iframe src={`/api/v1/docs/schema/${schema_name}`} className={"h-full w-full"}></iframe>
        </div>
    );
}

export const Route = createFileRoute("/docs/$schema_name/")({
    component: DocsIframe,
});
