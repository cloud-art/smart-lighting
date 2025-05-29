import {
  BulbOutlined,
  HomeOutlined,
  LineChartOutlined,
} from "@ant-design/icons";
import type { FC } from "react";
import { lazy } from "react";
import { Outlet, Route, Routes } from "react-router";
import { pathKeys } from "~/shared/lib/router";
import { Layout, MenuItem } from "~/shared/ui/layout";

const HomePage = lazy(async () => import("~/pages/home"));
const DevicesPage = lazy(async () => import("~/pages/devices"));
const StatisticPage = lazy(async () => import("~/pages/statistics"));

const RootRoutes: FC = () => {
  const sidebarMenuItems: MenuItem[] = [
    { icon: <HomeOutlined />, text: "Главная", to: pathKeys.root },
    {
      icon: <BulbOutlined />,
      text: "Устройства",
      to: pathKeys.devices(),
    },
    {
      icon: <LineChartOutlined />,
      text: "Статистика",
      to: pathKeys.statistics(),
    },
  ];

  return (
    <Routes>
      <Route
        element={
          <Layout menuItems={sidebarMenuItems}>
            <Outlet />
          </Layout>
        }
      >
        <Route path={pathKeys.root} element={<HomePage />} />
        <Route path={pathKeys.devices()} element={<DevicesPage />} />
        <Route path={pathKeys.statistics()} element={<StatisticPage />} />
      </Route>
    </Routes>
  );
};

export default RootRoutes;
