import type React from "react";

/**
 * A base layout component that structures the overall page with a navbar and main content area.
 *
 * @remarks
 * This layout is responsive and adapts styling based on light/dark themes.
 * It includes a fixed navbar at the top and a scrollable main content region.
 * The main area is styled with padding, background colors, and conditional shadows/rings for larger screens.
 *
 * @param props - The props for the BaseLayout component.
 * @param props.navbar - A React node representing the top navigation bar.
 * @param props.children - The main content to be displayed within the layout.
 *
 * @returns A structured layout with a navbar and content container.
 */
export function BaseLayout({
    navbar,
    children,
}: React.PropsWithChildren<{
    navbar: React.ReactNode;
}>) {
    return (
        <div className="relative isolate flex h-svh w-full flex-col bg-white lg:overflow-x-hidden lg:bg-zinc-100 dark:bg-zinc-900 dark:lg:bg-zinc-950">
            <div>{navbar}</div>

            <div className="dark:lg:rind-white/10 m-2 flex grow p-3 md:p-8 lg:rounded-lg lg:bg-white lg:shadow-xs lg:ring-1 lg:ring-zinc-950/5 dark:lg:bg-zinc-900">
                <div className={"mx-auto w-full max-w-6xl"}>{children}</div>
            </div>
        </div>
    );
}
