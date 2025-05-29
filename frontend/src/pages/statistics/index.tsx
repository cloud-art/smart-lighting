import { useQuery } from "@tanstack/react-query";
import { Card, Empty, Spin } from "antd";
import type { FC } from "react";
import { deviceDataQueries } from "~/shared/api/queries/device-data";

import { AppPage } from "~/shared/ui/page-layout";
import { StatisticHourlyChart } from "./ui/statistic-hourly-chart";
import { StatisticMonthDayChart } from "./ui/statistic-month-day-chart";
import { StatisticWeekdayChart } from "./ui/statistic-weekday-chart";

const StatisticsPage: FC = () => {
  const hourlyAveragesQuery = useQuery(deviceDataQueries.hourlyAverages());
  const weekdayAveragesQuery = useQuery(deviceDataQueries.weekdayAverages());
  const dailyAveragesQuery = useQuery(deviceDataQueries.dailyAverages());

  return (
    <AppPage title="Статистика" containerClassName="flex flex-col gap-3">
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
