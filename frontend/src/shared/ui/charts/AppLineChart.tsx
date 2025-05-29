import { Grid } from "antd";
import type { FC } from "react";
import { useMemo } from "react";
import type { LineProps } from "recharts";
import {
  CartesianGrid,
  Label,
  Legend,
  Line,
  LineChart,
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
  calculateYDomain,
  getYAxisTickFormatter,
  normalizeChartLegendProps,
} from "./common";

const { useBreakpoint } = Grid;

export type AppLineChartProps = {
  lineChart?: Omit<CategoricalChartProps, "ref" | "children">;
  lineProps?:
    | Omit<LineProps, "ref">
    | ((column: AppChartColumn, index: number) => Omit<LineProps, "ref">);
} & AppCartesianChartProps;

export const AppLineChart: FC<AppLineChartProps> = ({
  name,
  data,
  columns,
  lineChart,
  lineProps,
  referenceLines,
  children,
  legend,
  tooltip,
  xAxis,
  yAxis,
  ...props
}) => {
  //#region Bindings
  const breakpoints = useBreakpoint();
  //#endregion

  //region Computed
  const yDomain = useMemo(
    () => calculateYDomain(referenceLines),
    [referenceLines]
  );
  //endregion

  //#region Render
  return (
    <ResponsiveContainer {...props}>
      <LineChart data={data} {...lineChart}>
        {children}

        <CartesianGrid stroke="#ECEEF1" strokeDasharray="3 3" strokeWidth={1} />
        <XAxis {...xAxis} />

        <YAxis
          domain={yDomain}
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
            <Line
              key={column.name}
              dataKey={(row: (string | number)[]) => row[index]}
              name={column.name}
              stroke={column.color}
              strokeWidth={4}
              {...(isFunction(lineProps)
                ? lineProps(column, index)
                : lineProps)}
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
        <Tooltip {...tooltip} />
      </LineChart>
    </ResponsiveContainer>
  );
  //#endregion
};
