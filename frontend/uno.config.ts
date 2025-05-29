import { defineConfig } from "unocss";

export default defineConfig({
  theme: {
    colors: {
      ...["primary", "success", "error", "warning", "info"].reduce<
        Record<string, Record<string, string>>
      >((acc, color) => {
        acc[color] = {
          DEFAULT: `var(--ant-color-${color})`,
          bg: `var(--ant-color-${color}-bg)`,
          "bg-hover": `var(--ant-color-${color}-bg-hover)`,
          border: `var(--ant-color-${color}-border)`,
          "border-hover": `var(--ant-color-${color}-border-hover)`,
          hover: `var(--ant-color-${color}-hover)`,
          active: `var(--ant-color-${color}-active)`,
          "text-hover": `var(--ant-color-${color}-text-hover)`,
          text: `var(--ant-color-${color}-text)`,
          "text-active": `var(--ant-color-${color}-text-active)`,
        };
        return acc;
      }, {}),
      border: "var(--ant-color-border)",
    },
  },
});
