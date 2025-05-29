import type { ReactNode } from "react";
import type {
  ReferenceLineProps,
  ResponsiveContainerProps,
  TooltipProps,
  XAxisProps,
  YAxisProps,
} from "recharts";
import type { Props as LegendProps } from "recharts/types/component/DefaultLegendContent";
import type { AxisDomain } from "recharts/types/util/types";
import { AppLegendProps } from "./AppLegend";

export type AppChartColumn = { name: string; color: string };

export type AppChartProps = {
  name?: string;
  legend?: AppLegendProps | ((props: AppLegendProps) => AppLegendProps);
  tooltip?: TooltipProps<string, string>;
  children?: ReactNode;
} & Omit<ResponsiveContainerProps, "children">;

export type AppCartesianChartProps = {
  data: (string | number | null)[][];
  columns: (AppChartColumn | null)[];
  referenceLines?: ReferenceLineProps[];
  xAxis?: XAxisProps;
  yAxis?: { tickDisplaySymbols?: number } & YAxisProps;
} & AppChartProps;

export const normalizeChartLegendProps = (
  legendProps: LegendProps,
  appLegendProps?: AppLegendProps
): AppLegendProps => ({
  layout: legendProps.layout,
  values: legendProps.payload?.map(
    ({ color, value: label, payload: entry }) => ({
      label: label as string,
      color,
      value: entry?.value as string | undefined,
    })
  ),
  ...appLegendProps,
});

export const calculateYDomain = (
  referenceLines: ReferenceLineProps[] | undefined
) => {
  if (referenceLines?.length) {
    const maxY = referenceLines?.length
      ? referenceLines
          .filter((line) => line.y !== undefined)
          .reduce((max, obj) => Math.max(max, Number(obj.y)), -Infinity)
      : 0;
    const adjustedMaxY = (maxY + maxY * 0.1).toFixed(2);

    return [0, parseFloat(adjustedMaxY)] as AxisDomain;
  }
};

/**
 * Размер ширины у YAxis фиксированный. Данная функция
 * ограничивает количество символов у 'Tick'.
 * https://github.com/recharts/recharts/issues/2027
 */
export const getYAxisTickFormatter =
  (tickDisplaySymbols: number): YAxisProps["tickFormatter"] =>
  (tickValue: string | number) => {
    const value =
      typeof tickValue === "number" ? tickValue.toString() : tickValue;
    return value.slice(0, tickDisplaySymbols);
  };
