import type { BaseUseQueryOptions } from "./common";

import { queryOptions } from "@tanstack/react-query";

import {
  DeviceDataDayAverages,
  DeviceDataHourlyAverages,
  DeviceDataWeekdayAverages,
  getDeviceDataDailyAverages,
  getDeviceDataHourlyAverages,
  getDeviceDataWeekdayAverages,
} from "../services/device-stats";

export type DeviceStatsParams = {
  device?: number;
};

export const deviceStatsQueries = {
  all: () => ["device-stats"],

  averages: (key?: string, params?: DeviceStatsParams) => [
    ...deviceStatsQueries.all(),
    "averages",
    key,
    params,
  ],

  hourlyAverages: <TData extends object = DeviceDataHourlyAverages[]>({
    params,
    ...options
  }: BaseUseQueryOptions<
    DeviceDataHourlyAverages[],
    TData,
    DeviceStatsParams
  > = {}) =>
    queryOptions({
      queryKey: [...deviceStatsQueries.averages("hourly")],
      queryFn: async ({ signal }) => getDeviceDataHourlyAverages({ signal }),
      ...options,
    }),

  weekdayAverages: <TData extends object = DeviceDataWeekdayAverages[]>({
    params,
    ...options
  }: BaseUseQueryOptions<
    DeviceDataWeekdayAverages[],
    TData,
    DeviceStatsParams
  > = {}) =>
    queryOptions({
      queryKey: [...deviceStatsQueries.averages("weekday")],
      queryFn: async ({ signal }) => getDeviceDataWeekdayAverages({ signal }),
      ...options,
    }),

  dailyAverages: <TData extends object = DeviceDataDayAverages[]>({
    params,
    ...options
  }: BaseUseQueryOptions<
    DeviceDataDayAverages[],
    TData,
    DeviceStatsParams
  > = {}) =>
    queryOptions({
      queryKey: [...deviceStatsQueries.averages("daily")],
      queryFn: async ({ signal }) => getDeviceDataDailyAverages({ signal }),
      ...options,
    }),
};
