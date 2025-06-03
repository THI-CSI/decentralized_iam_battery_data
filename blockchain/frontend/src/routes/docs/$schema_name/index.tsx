import { createFileRoute } from "@tanstack/react-router";

/**
 * The properties for {@link DocsIframe}
 */
export type DocsIframeProps = {};

/**
 * Route component that renders an iframe to display schema documentation.
 *
 * @remarks
 * Extracts the `schema_name` param from the URL and embeds the relevant
 * schema documentation using an iframe. This is useful for server-hosted
 * static docs or Swagger/OpenAPI UI served from a backend.
 *
 * @param _props - Props for the component (currently unused)
 * @returns A full-size iframe rendering the schema docs for the given schema name
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
