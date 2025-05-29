import { Grid } from "antd";
import type { FC } from "react";
import type { BarProps } from "recharts";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Label,
  Legend,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { CategoricalChartProps } from "recharts/types/chart/generateCategoricalChart";

import { isFunction } from "~/shared/lib/is";
import { AppLegend } from "./AppLegend";
import {
  AppCartesianChartProps,
  AppChartColumn,
  getYAxisTickFormatter,
  normalizeChartLegendProps,
} from "./common";

const { useBreakpoint } = Grid;

export type AppBarChartProps = {
  barChart?: Omit<CategoricalChartProps, "ref" | "children">;
  barProps?:
    | Omit<BarProps, "ref">
    | ((column: AppChartColumn, index: number) => Omit<BarProps, "ref">);
} & AppCartesianChartProps;

export const AppBarChart: FC<AppBarChartProps> = ({
  name,
  data,
  columns,
  barChart,
  barProps,
  referenceLines,
  children,
  legend,
  tooltip,
  xAxis,
  yAxis,
  ...props
}) => {
  const breakpoints = useBreakpoint();

  return (
    <ResponsiveContainer {...props}>
      <BarChart data={data} {...barChart}>
        {children}

        <CartesianGrid stroke="#ECEEF1" strokeDasharray="3 3" strokeWidth={1} />
        <XAxis {...xAxis} />
        <YAxis
          tickFormatter={getYAxisTickFormatter(yAxis?.tickDisplaySymbols ?? 6)}
          {...yAxis}
        />
        {name && <Label position="top" value={name} />}

        {referenceLines?.map((referenceLine) => (
          // @ts-expect-error TODO
          <ReferenceLine
            key={referenceLine.name}
            strokeDasharray="5 3"
            {...referenceLine}
          />
        ))}

        {columns.map((column, index) =>
          column !== null ? (
            <Bar
              key={column.name}
              dataKey={(row: (string | number)[]) => row[index]}
              fill={column.color}
              name={column.name}
              {...(isFunction(barProps) ? barProps(column, index) : barProps)}
            />
          ) : undefined
        )}

        <Legend
          align={breakpoints.sm ? "right" : "center"}
          iconType="square"
          layout={breakpoints.sm ? "vertical" : "horizontal"}
          style={{ padding: 3 }}
          verticalAlign={breakpoints.sm ? "middle" : "bottom"}
          content={(props) => {
            const legendProps = normalizeChartLegendProps(props);
            return (
              <AppLegend
                {...legendProps}
                {...(isFunction(legend) ? legend(legendProps) : legend)}
              />
            );
          }}
        />
        <Tooltip cursor={{ opacity: 0 }} {...tooltip} />
      </BarChart>
    </ResponsiveContainer>
  );
};
