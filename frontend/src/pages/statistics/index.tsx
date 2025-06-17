import { useQuery } from "@tanstack/react-query";
import { Card, Empty, Spin } from "antd";
import { useState, type FC } from "react";

import { AppPage } from "~/shared/ui/page-layout";
import { StatisticHourlyChart } from "./ui/statistic-hourly-chart";
import { StatisticMonthDayChart } from "./ui/statistic-month-day-chart";
import { StatisticWeekdayChart } from "./ui/statistic-weekday-chart";
import { deviceStatsQueries } from "~/shared/api/queries/device-stats";
import {
  StatisticFilters,
  StatisticFilterValues,
} from "./ui/statistic-filters";
import { formatISO } from "date-fns";

const StatisticsPage: FC = () => {
  const [filters, setFilters] = useState<StatisticFilterValues>({});

  const hourlyAveragesQuery = useQuery(
    deviceStatsQueries.hourlyAverages({
      params: {
        device: filters.device,
        start_date: filters.start_date
          ? formatISO(filters.start_date)
          : undefined,
        end_date: filters.end_date ? formatISO(filters.end_date) : undefined,
      },
    })
  );
  const weekdayAveragesQuery = useQuery(
    deviceStatsQueries.weekdayAverages({
      params: {
        device: filters.device,
        start_date: filters.start_date
          ? formatISO(filters.start_date)
          : undefined,
        end_date: filters.end_date ? formatISO(filters.end_date) : undefined,
      },
    })
  );
  const dailyAveragesQuery = useQuery(
    deviceStatsQueries.dailyAverages({
      params: {
        device: filters.device,
        start_date: filters.start_date
          ? formatISO(filters.start_date)
          : undefined,
        end_date: filters.end_date ? formatISO(filters.end_date) : undefined,
      },
    })
  );

  return (
    <AppPage title="Статистика" containerClassName="flex flex-col gap-3">
      <StatisticFilters value={filters} onChange={setFilters} />

      <Card
        title="Статистика по часам"
        classNames={{ body: "flex justify-center" }}
      >
        {hourlyAveragesQuery.isLoading ? (
          <Spin />
        ) : hourlyAveragesQuery.isSuccess ? (
          <StatisticHourlyChart data={hourlyAveragesQuery.data} height={400} />
        ) : (
          <Empty description="Ошибка загрузки" />
        )}
      </Card>

      <Card
        title="Статистика по дням недели"
        classNames={{ body: "flex justify-center" }}
      >
        {weekdayAveragesQuery.isLoading ? (
          <Spin />
        ) : weekdayAveragesQuery.isSuccess ? (
          <StatisticWeekdayChart
            data={weekdayAveragesQuery.data}
            height={400}
          />
        ) : (
          <Empty description="Ошибка загрузки" />
        )}
      </Card>

      <Card
        title="Статистика по дням месяца"
        classNames={{ body: "flex justify-center" }}
      >
        {dailyAveragesQuery.isLoading ? (
          <Spin />
        ) : dailyAveragesQuery.isSuccess ? (
          <StatisticMonthDayChart data={dailyAveragesQuery.data} height={400} />
        ) : (
          <Empty description="Ошибка загрузки" />
        )}
      </Card>
    </AppPage>
  );
};

export default StatisticsPage;
