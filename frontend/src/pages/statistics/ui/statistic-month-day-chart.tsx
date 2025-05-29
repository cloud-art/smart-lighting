import { addDays, format, startOfMonth } from "date-fns";
import type { FC } from "react";
import { DeviceDataDayAverages } from "~/shared/api/services/device-data";
import { AppLineChart } from "~/shared/ui/charts";
import { StatisticChartBaseProps } from "./common";
import { StatisticChartTooltipContent } from "./statistic-chart-tooltip-content";

export type StatisticMonthDayChartProps = {
  data: DeviceDataDayAverages[];
} & StatisticChartBaseProps;

export const StatisticMonthDayChart: FC<StatisticMonthDayChartProps> = ({
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
              day_of_month,
              avg_dimming_level,
              avg_corrected_dim,
              avg_traffic_speed,
              avg_calculated_dim,
              avg_car_count,
              avg_pedestrian_count,
            ] = data.payload;

            return (
              <StatisticChartTooltipContent
                title={`День месяца: ${day_of_month}`}
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
          day_of_month,
          avg_dimming_level,
          avg_corrected_dim,
          avg_traffic_speed,
          avg_calculated_dim,
          avg_car_count,
          avg_pedestrian_count,
        }) => [
          day_of_month,
          avg_dimming_level,
          avg_corrected_dim,
          avg_traffic_speed,
          avg_calculated_dim,
          avg_car_count,
          avg_pedestrian_count,
        ]
      )}
      xAxis={{
        dataKey: ([day_of_month]) => {
          const date = addDays(startOfMonth(new Date()), day_of_month - 1);
          return format(date, "d");
        },
      }}
      {...props}
    />
  );
};
