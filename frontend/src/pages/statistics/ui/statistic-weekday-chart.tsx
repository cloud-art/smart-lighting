import { addDays, format, startOfWeek } from "date-fns";
import type { FC } from "react";
import { DeviceDataWeekdayAverages } from "~/shared/api/services/device-stats";
import { AppLineChart } from "~/shared/ui/charts";
import { StatisticChartBaseProps } from "./common";
import { StatisticChartTooltipContent } from "./statistic-chart-tooltip-content";

export type StatisticWeekdayChartProps = {
  data: DeviceDataWeekdayAverages[];
} & StatisticChartBaseProps;

export const StatisticWeekdayChart: FC<StatisticWeekdayChartProps> = ({
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
              day,
              avg_dimming_level,
              avg_calculated_dim,
              avg_corrected_dim,
              avg_traffic_speed,
              avg_car_count,
              avg_pedestrian_count,
            ] = data.payload;

            const parsedDay = addDays(
              startOfWeek(new Date(), { weekStartsOn: 1 }),
              day
            );
            const weekdayName = format(parsedDay, "EEEE");

            return (
              <StatisticChartTooltipContent
                title={`День недели: ${weekdayName}`}
                data={[
                  {
                    label: "Уровень диммирования",
                    value: avg_dimming_level,
                  },
                  {
                    label: "Вычисленное значение",
                    value: avg_calculated_dim,
                  },
                  {
                    label: "Экспертная оценка",
                    value: avg_corrected_dim,
                  },
                  { label: "Скорость трафика", value: avg_traffic_speed },
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
        { color: "green", name: "Вычисленное значение" },
        { color: "red", name: "Оценка эксперта" },
      ]}
      lineProps={{ type: "monotone" }}
      data={data.map(
        ({
          day,
          avg_dimming_level,
          avg_calculated_dim,
          avg_corrected_dim,
          avg_traffic_speed,
          avg_car_count,
          avg_pedestrian_count,
        }) => [
          day,
          avg_dimming_level,
          avg_calculated_dim,
          avg_corrected_dim,
          avg_traffic_speed,
          avg_car_count,
          avg_pedestrian_count,
        ]
      )}
      xAxis={{
        dataKey: ([day]) => {
          const date = addDays(
            startOfWeek(new Date(), { weekStartsOn: 1 }),
            day
          );
          return format(date, "EEEE");
        },
      }}
      {...props}
    />
  );
};
