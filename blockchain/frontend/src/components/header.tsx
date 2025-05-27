import { Link, useNavigate, useRouterState } from "@tanstack/react-router";
import { Button } from "@/components/ui/button.tsx";
import {
    NavigationMenu,
    NavigationMenuContent,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    NavigationMenuTrigger,
    navigationMenuTriggerStyle,
} from "./ui/navigation-menu";


/**
 * The main navigation header for the application.
 *
 * @remarks
 * - Stays sticky at the top of the viewport.
 * - Includes branding, route links, and schema doc shortcuts.
 * - Uses a conditional "Back" button depending on route context.
 *
 * @returns JSX for the application header.
 */
export default function HeaderLayout() {
    const navigate = useNavigate();
    const pathname = useRouterState().location.pathname;

    return (
        <header className={"bg-sidebar-primary sticky top-0 z-50 flex justify-center p-6 text-white shadow-lg"}>
            <div className={"flex w-full max-w-6xl"}>
                <div className={"container mx-auto flex flex-row items-center justify-between"}>
                    <div
                        className={"mb-4 flex cursor-pointer items-center sm:mb-0"}
                        onClick={() => navigate({ to: "/blocks" })}
                    >
                        <h1 className={"text-2xl font-bold tracking-tight md:text-3xl"}>Blockchain Explorer</h1>
                    </div>
                </div>
                <nav className={"flex gap-8 space-x-2 sm:space-x-3"}>
                    <NavigationMenu>
                        <NavigationMenuList className={"gap-4"}>
                            <NavigationMenuItem>
                                <NavigationMenuTrigger className={"bg-sidebar-primary text-white duration-0"}>
                                    Docs
                                </NavigationMenuTrigger>
                                <NavigationMenuContent>
                                    <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                                        <Link
                                            className={"h-full w-full"}
                                            to={"/docs/$schema_name"}
                                            params={{ schema_name: "did.schema.html" }}
                                        >
                                            DID
                                        </Link>
                                    </NavigationMenuLink>
                                    <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                                        <Link
                                            className={"h-full w-full"}
                                            to={"/docs/$schema_name"}
                                            params={{ schema_name: "vc.record.schema.html" }}
                                        >
                                            VC Records
                                        </Link>
                                    </NavigationMenuLink>
                                    <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                                        <Link
                                            className={"h-full w-full"}
                                            to={"/docs/$schema_name"}
                                            params={{ schema_name: "vc.schema.html" }}
                                        >
                                            VC Schema
                                        </Link>
                                    </NavigationMenuLink>
                                </NavigationMenuContent>
                            </NavigationMenuItem>
                            <NavigationMenuItem>
                                <Link to={"/blocks"}>
                                    <NavigationMenuLink>Blocks</NavigationMenuLink>
                                </Link>
                            </NavigationMenuItem>
                            <NavigationMenuItem>
                                <Link to={"/dids"}>
                                    <NavigationMenuLink>Dids</NavigationMenuLink>
                                </Link>
                            </NavigationMenuItem>
                        </NavigationMenuList>
                    </NavigationMenu>
                    {pathname !== "/blocks" && pathname !== "/dids" && (
                        <Button
                            navbar={"outline"}
                            onClick={() =>
                                navigate(
                                    pathname.includes("blocks") || pathname.includes("docs")
                                        ? { to: "/blocks" }
                                        : { to: "/dids" },
                                )
                            }
                        >
                            Back
                        </Button>
                    )}
                </nav>
            </div>
        </header>
    );
}
