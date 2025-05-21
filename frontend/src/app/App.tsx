import { QueryClientProvider } from "@tanstack/react-query";
import { StrictMode } from "react";
import { BrowserRouter } from "react-router";
import { queryClient } from "~/shared/api/query-client";
import RootRoutes from "./RootRoutes";

function App() {
  return (
    <StrictMode>
      <BrowserRouter>
        <QueryClientProvider client={queryClient}>
          <RootRoutes />
        </QueryClientProvider>
      </BrowserRouter>
    </StrictMode>
  );
}

export default App;
