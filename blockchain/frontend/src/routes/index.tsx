import { createFileRoute, Navigate } from "@tanstack/react-router";

/**
 * Root route definition (`/`) that immediately redirects to `/blocks`.
 *
 * @remarks
 * This is commonly used as a landing redirect when the app's root path
 * shouldn't render its own content.
 */
export const Route = createFileRoute("/")({
    component: () => <Navigate to={"/blocks"} />,
});
