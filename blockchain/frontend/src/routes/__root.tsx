import { Outlet, createRootRoute } from "@tanstack/react-router";
import { BaseLayout } from "@/components/BaseLayout.tsx";
import HeaderLayout from "@/components/header.tsx";
import { Suspense } from "react";

/**
 * Root route configuration for the application.
 *
 * @remarks
 * This sets the top-level layout for all nested routes.
 * It wraps content with a shared `BaseLayout`, injects the common header,
 * and enables lazy loading of route content using `Suspense`.
 */
export const Route = createRootRoute({
    component: () => (
        <BaseLayout
            navbar={<HeaderLayout />}
            children={
                <Suspense>
                    <Outlet />
                </Suspense>
            }
        />
    ),
});
