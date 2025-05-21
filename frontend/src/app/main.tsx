import { createRoot } from "react-dom/client";
import "virtual:uno.css";
import App from "./App";

const rootElement = document.getElementById("root")!;

function main() {
  const root = createRoot(rootElement);
  root.render(<App />);
}

main();
