import { type FC, type ReactNode } from "react";

import { useLocation, useNavigate } from "react-router";

import { CloseOutlined } from "@ant-design/icons";
import {
  Button,
  Grid,
  Layout,
  Menu,
  MenuProps,
  SiderProps,
  Typography,
} from "antd";

const { useBreakpoint } = Grid;
const { Sider } = Layout;
const { Text } = Typography;

type AntMenuItem = Required<MenuProps>["items"][number];

export interface MenuItem {
  text: string;
  icon: ReactNode;
  to: string;
}

export interface SideBarProps extends SiderProps {
  menuItems: MenuItem[];
  className?: string;
  isDrawerOpen?: boolean;
  onDrawerClose?: () => void;
}

export const SideBar: FC<SideBarProps> = ({
  menuItems,
  className,
  isDrawerOpen,
  onDrawerClose,
  ...props
}) => {
  const navigate = useNavigate();
  const location = useLocation();

  const { lg: isLaptopScreen } = useBreakpoint();

  const getSelectedItem = () => {
    const currentItem = menuItems.find((item) => item.to === location.pathname);
    return currentItem?.text;
  };

  return (
    <Sider
      trigger={null}
      collapsedWidth={0}
      collapsed={isLaptopScreen ? false : !isDrawerOpen}
      collapsible={isLaptopScreen ? false : true}
      onCollapse={onDrawerClose}
      className={className}
      width={isLaptopScreen ? 200 : "100%"}
      {...props}
    >
      <div className="flex flex-col gap-3 overflow-auto lg:pt-2">
        <div className="flex justify-between items-center gap-2">
          <Text className="pl-3" type="secondary">
            Меню
          </Text>

          <Button
            type="text"
            icon={<CloseOutlined />}
            className="lg:hidden"
            onClick={onDrawerClose}
          />
        </div>

        <Menu
          selectedKeys={[getSelectedItem()].filter(Boolean) as string[]}
          items={menuItems.map(
            ({ icon, text, to }) =>
              ({
                key: text,
                icon: icon,
                label: text,
                onClick: navigate(to),
              }) as AntMenuItem
          )}
        />
      </div>
    </Sider>
  );
};
