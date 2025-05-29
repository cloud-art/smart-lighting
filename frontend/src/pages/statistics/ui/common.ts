import { AppLineChartProps } from "~/shared/ui/charts";

export type StatisticChartBaseProps = Omit<
  AppLineChartProps,
  "tooltip" | "columns" | "lineProps" | "data" | "xAxis"
>;
