import { format, parse } from "date-fns";
import type { FC } from "react";
import { DeviceDataHourlyAverages } from "~/shared/api/services/device-stats";
import { AppLineChart } from "~/shared/ui/charts";
import { StatisticChartBaseProps } from "./common";
import { StatisticChartTooltipContent } from "./statistic-chart-tooltip-content";

export type StatisticHourlyChartProps = {
  data: DeviceDataHourlyAverages[];
} & StatisticChartBaseProps;

export const StatisticHourlyChart: FC<StatisticHourlyChartProps> = ({
  data,
  ...props
}) => {
  return (
    <AppLineChart
      tooltip={{
        content: ({ active, payload }) => {
          if (active && payload && payload.length) {
            const data = payload.at(0);
            if (!data) return;
            const [
              hour,
              avg_dimming_level,
              avg_corrected_dim,
              avg_traffic_speed,
              avg_calculated_dim,
              avg_car_count,
              avg_pedestrian_count,
            ] = data.payload;

            return (
              <StatisticChartTooltipContent
                title={`Час: ${hour}`}
                data={[
                  {
                    label: "Уровень диммирования",
                    value: avg_dimming_level,
                  },
                  {
                    label: "Экспертная оценка",
                    value: avg_corrected_dim,
                  },
                  { label: "Скорость трафика", value: avg_traffic_speed },
                  {
                    label: "Вычисленное значение",
                    value: avg_calculated_dim,
                  },
                  { label: "Количество машин", value: avg_car_count },
                  {
                    label: "Количество пешеходов",
                    value: avg_pedestrian_count,
                  },
                ]}
              />
            );
          }
        },
      }}
      columns={[
        null,
        { color: "blue", name: "Уровень диммирования" },
        { color: "red", name: "Оценка эксперта" },
      ]}
      lineProps={{ type: "monotone" }}
      data={data.map(
        ({
          hour,
          avg_dimming_level,
          avg_corrected_dim,
          avg_traffic_speed,
          avg_calculated_dim,
          avg_car_count,
          avg_pedestrian_count,
        }) => [
          hour,
          avg_dimming_level,
          avg_corrected_dim,
          avg_traffic_speed,
          avg_calculated_dim,
          avg_car_count,
          avg_pedestrian_count,
        ]
      )}
      xAxis={{
        dataKey: ([hour]) => {
          const parsedDate = parse(String(hour), "H", new Date());
          return format(parsedDate, "HH:00");
        },
      }}
      {...props}
    />
  );
};
