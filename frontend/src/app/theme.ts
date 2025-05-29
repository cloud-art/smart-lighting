import { ThemeConfig } from "antd";

export const themeConfig: ThemeConfig = {
  cssVar: true,
  token: {
    fontSize: 16,
    fontWeightStrong: 600,
    fontSizeHeading1: 22,
    fontSizeHeading2: 20,
    fontSizeHeading3: 18,
    fontSizeHeading4: 16,
    fontSizeHeading5: 14,
    colorPrimary: "#0055FF",
    colorTextDisabled: "#005CFF",
    colorTextLightSolid: "#1C1E20",
    colorBgContainerDisabled: "#005CFF",
    colorBorder: "#ECEEF1",
    colorText: "#1C1E20",
  },
  components: {
    Layout: {
      bodyBg: "#FFFFFF",
      headerBg: "#FFFFFF",
      footerBg: "#FFFFFF",
      siderBg: "#F6F6F8",
      headerPadding: 0,
      headerHeight: "auto",
    },
    Menu: {
      activeBarBorderWidth: 0,
      colorBgContainer: "transparent",
      itemHeight: 36,
      itemMarginBlock: 2,
      itemMarginInline: 2,
      iconMarginInlineEnd: 8,
      padding: 12,
      itemSelectedColor: "#1C1E20",
      itemColor: "#1C1E20",
      itemSelectedBg: "#0055FF33",
      fontSize: 14,
      iconSize: 20,
    },
  },
};
