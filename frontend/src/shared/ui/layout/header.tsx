import type { FC, ReactNode } from "react";

import { MenuOutlined } from "@ant-design/icons";
import { Button, Grid, Layout } from "antd";
import clsx from "clsx";

const { Header: AntHeader } = Layout;
const { useBreakpoint } = Grid;

export interface HeaderProps {
  content?: ReactNode;
  className?: string;
  onLogoClick?: () => void;
  onBurgerMenuClick?: () => void;
}

export const Header: FC<HeaderProps> = ({
  className,
  onLogoClick,
  onBurgerMenuClick,
}) => {
  const { lg: isLaptopScreen } = useBreakpoint();

  return (
    <AntHeader className={clsx("p-2 flex items-center gap-4", className)}>
      {!isLaptopScreen && (
        <Button
          type="text"
          icon={<MenuOutlined />}
          onClick={onBurgerMenuClick}
        />
      )}

      <div
        className={clsx(
          "rounded bg-primary-bg h-6.25 w-9.5",
          onLogoClick && "cursor-pointer"
        )}
        onClick={onLogoClick}
      />
    </AntHeader>
  );
};
