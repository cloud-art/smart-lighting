import { QueryClientProvider } from "@tanstack/react-query";
import { ConfigProvider } from "antd";
import ru from "antd/locale/ru_RU";
import { StrictMode } from "react";
import { BrowserRouter } from "react-router";
import { queryClient } from "~/shared/api/query-client";
import RootRoutes from "./RootRoutes";
import { themeConfig } from "./theme";

function App() {
  return (
    <StrictMode>
      <BrowserRouter>
        <QueryClientProvider client={queryClient}>
          <ConfigProvider locale={ru} theme={themeConfig}>
            <RootRoutes />
          </ConfigProvider>
        </QueryClientProvider>
      </BrowserRouter>
    </StrictMode>
  );
}

export default App;
