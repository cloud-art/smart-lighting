import type { FC, PropsWithChildren } from "react";

import { Layout as AntLayout } from "antd";
import type { HeaderProps } from "./header";
import type { SideBarProps } from "./sidebar";

import { useState } from "react";

import { Header } from "./header";
import { SideBar } from "./sidebar";

export interface LayoutProps
  extends PropsWithChildren,
    SideBarProps,
    Pick<HeaderProps, "onLogoClick"> {}

export const Layout: FC<LayoutProps> = ({
  menuItems,
  onLogoClick,
  children,
}) => {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  // #region Render
  return (
    <AntLayout className="h-100dvh w-100dvw flex flex-col!">
      <Header
        className="border-b-1 border-border border-b-solid"
        onLogoClick={onLogoClick}
        onBurgerMenuClick={() => setIsDrawerOpen((value) => !value)}
      />

      <div className="flex h-full w-full min-h-0">
        <SideBar
          className={"lg-border-r-1 lg-border-border lg-border-r-solid"}
          isDrawerOpen={isDrawerOpen}
          onDrawerClose={() => setIsDrawerOpen(false)}
          menuItems={menuItems}
        />

        <main className="flex flex-1 flex-col h-full w-full min-w-0">
          <div className="h-full min-h-0 overflow-auto w-full">{children}</div>
        </main>
      </div>
    </AntLayout>
  );
  // #endregion
};
