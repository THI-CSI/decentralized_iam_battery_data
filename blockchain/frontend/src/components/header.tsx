import { useNavigate, useRouterState } from "@tanstack/react-router";
import { Button } from "@/components/ui/button.tsx";

/**
 * The header layout for the application
 */
export default function HeaderLayout() {
    const navigate = useNavigate();
    const pathname = useRouterState().location.pathname;

    return (
        <header className={"bg-sidebar-primary sticky top-0 z-50 flex p-6 text-white shadow-lg"}>
            <div className={"container mx-auto flex flex-row items-center justify-between"}>
                <div
                    className={"mb-4 flex cursor-pointer items-center sm:mb-0"}
                    onClick={() => navigate({ to: "/blocks" })}
                >
                    <h1 className={"text-2xl font-bold tracking-tight md:text-3xl"}>Blockchain Explorer</h1>
                </div>
            </div>
            <nav className={"flex space-x-2 sm:space-x-3"}>
                <Button
                    navbar={pathname === "/blocks" ? "default" : "outline"}
                    onClick={() => navigate({ to: "/blocks" })}
                >
                    Blocks
                </Button>
                <Button navbar={pathname === "/dids" ? "default" : "outline"} onClick={() => navigate({ to: "/dids" })}>
                    DIDs
                </Button>
                {pathname !== "/blocks" && pathname !== "/dids" && (
                    <Button
                        navbar={"ghost"}
                        onClick={() => navigate(pathname.includes("blocks") ? { to: "/blocks" } : { to: "/dids" })}
                    >
                        Back
                    </Button>
                )}
            </nav>
        </header>
    );
}
