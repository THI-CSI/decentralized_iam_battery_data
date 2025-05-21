import { Outlet, createRootRoute } from "@tanstack/react-router";
import { BaseLayout } from "@/components/BaseLayout.tsx";
import HeaderLayout from "@/components/header.tsx";
import { Suspense } from "react";

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
