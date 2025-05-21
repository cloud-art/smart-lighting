import type { PaginatedResponse, PaginationParams } from "~/shared/lib/api";
import type { BaseUseQueryOptions } from "./common";

import { queryOptions } from "@tanstack/react-query";

import {
  DeviceData,
  DeviceDataDayAverages,
  DeviceDataHourlyAverages,
  getDeviceDataDailyAverages,
  getDeviceDataHourlyAverages,
  getDeviceDataList,
  getDeviceDataWeekdayAverages,
} from "../services/device-data";

export const deviceDataQueries = {
  all: () => ["device-data"],

  lists: (params: PaginationParams = {}) => [
    ...deviceDataQueries.all(),
    "list",
    params,
  ],

  list: <TData extends object = PaginatedResponse<DeviceData>>({
    params,
    ...options
  }: BaseUseQueryOptions<
    PaginatedResponse<DeviceData>,
    TData,
    PaginationParams
  > = {}) =>
    queryOptions({
      queryKey: [...deviceDataQueries.lists(params)],
      queryFn: async ({ signal }) => getDeviceDataList({ signal, params }),
      ...options,
    }),

  averages: () => [...deviceDataQueries.all(), "averages"],

  hourlyAverages: <TData extends object = DeviceDataHourlyAverages>({
    params,
    ...options
  }: BaseUseQueryOptions<DeviceDataHourlyAverages, TData> = {}) =>
    queryOptions({
      queryKey: [...deviceDataQueries.averages()],
      queryFn: async ({ signal }) => getDeviceDataHourlyAverages({ signal }),
      ...options,
    }),

  weekdayAverages: <TData extends object = DeviceDataDayAverages>({
    params,
    ...options
  }: BaseUseQueryOptions<DeviceDataDayAverages, TData> = {}) =>
    queryOptions({
      queryKey: [...deviceDataQueries.averages()],
      queryFn: async ({ signal }) => getDeviceDataWeekdayAverages({ signal }),
      ...options,
    }),

  dailyAverages: <TData extends object = DeviceDataDayAverages>({
    params,
    ...options
  }: BaseUseQueryOptions<DeviceDataDayAverages, TData> = {}) =>
    queryOptions({
      queryKey: [...deviceDataQueries.averages()],
      queryFn: async ({ signal }) => getDeviceDataDailyAverages({ signal }),
      ...options,
    }),
};
