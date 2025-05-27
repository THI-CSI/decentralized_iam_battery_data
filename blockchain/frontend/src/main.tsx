import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider, createRouter } from "@tanstack/react-router";

// Import the generated route tree
import { routeTree } from "./routeTree.gen";

// @ts-ignore
import "./styles.css";
import reportWebVitals from "./reportWebVitals.ts";

/**
 * Create a new router instance with application-specific configuration.
 *
 * @remarks
 * - `routeTree` is auto-generated from route definitions.
 * - `context` can be used to pass global data like auth or config.
 * - `defaultPreload`: Determines when route data should preload (e.g., on hover or intent).
 * - `scrollRestoration`: Maintains scroll position between navigations.
 * - `defaultStructuralSharing`: Enables optimized re-rendering when route data changes.
 * - `defaultPreloadStaleTime`: Caches preload data for this duration in ms (0 = no caching).
 */
const router = createRouter({
    routeTree,
    context: {},
    defaultPreload: "intent",
    scrollRestoration: true,
    defaultStructuralSharing: true,
    defaultPreloadStaleTime: 0
});

/**
 * Type registration hook for the router instance to enable type-safe navigation and hooks.
 */
declare module "@tanstack/react-router" {
    interface Register {
        router: typeof router;
    }
}

/**
 * Render the root React application using `RouterProvider` for routing.
 *
 * @remarks
 * Rendering is only done if the root element exists and has no existing content.
 */
const rootElement = document.getElementById("app");
if (rootElement && !rootElement.innerHTML) {
    const root = ReactDOM.createRoot(rootElement);
    root.render(
        <StrictMode>
            <RouterProvider router={router} />
        </StrictMode>
    );
}

/**
 * Optional performance measurement.
 *
 * @remarks
 * Use `reportWebVitals` to track core web vitals. For example:
 * ```ts
 * reportWebVitals(console.log);
 * ```
 * or send metrics to a backend or analytics provider.
 * Learn more: https://bit.ly/CRA-vitals
 */
reportWebVitals();
