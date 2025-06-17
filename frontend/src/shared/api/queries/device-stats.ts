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
  start_date?: string;
  end_date?: string;
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
      queryKey: [...deviceStatsQueries.averages("hourly", params)],
      queryFn: async ({ signal }) =>
        getDeviceDataHourlyAverages({ signal, params }),
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
      queryKey: [...deviceStatsQueries.averages("weekday", params)],
      queryFn: async ({ signal }) =>
        getDeviceDataWeekdayAverages({ signal, params }),
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
      queryKey: [...deviceStatsQueries.averages("daily", params)],
      queryFn: async ({ signal }) =>
        getDeviceDataDailyAverages({ signal, params }),
      ...options,
    }),
};
