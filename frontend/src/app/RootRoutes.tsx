import { HomeOutlined } from "@ant-design/icons";
import type { FC } from "react";
import { lazy } from "react";
import { Route, Routes } from "react-router";
import { pathKeys } from "~/shared/lib/router";
import { Layout } from "~/shared/ui/layout";

const HomePage = lazy(async () => import("~/pages/home-page"));

const RootRoutes: FC = () => {
  // #region Render
  return (
    <Routes>
      <Route
        element={
          <Layout
            menuItems={[
              { icon: <HomeOutlined />, text: "Главная", to: pathKeys.root },
            ]}
          />
        }
      >
        <Route index element={<HomePage />} />
      </Route>
    </Routes>
  );
  // #endregion
};

export default RootRoutes;
