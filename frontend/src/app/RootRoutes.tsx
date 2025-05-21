import type { FC } from "react";
import { lazy } from "react";
import { Route, Routes } from "react-router";

const HomePage = lazy(async () => import("~/pages/home-page"));

const RootRoutes: FC = () => {
  // #region Render
  return (
    <Routes>
      <Route index element={<HomePage />} />
    </Routes>
  );
  // #endregion
};

export default RootRoutes;
