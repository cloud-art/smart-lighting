import type { PaginatedResponse, PaginationParams } from "~/shared/lib/api";
import type { BaseUseQueryOptions } from "./common";

import { queryOptions } from "@tanstack/react-query";

import { DeviceData, getDeviceDataList } from "../services/device-data";

export type DeviceDataListParams = PaginationParams & {
  device?: Number;
  start_date?: string;
  end_date?: string;
};

export const deviceDataQueries = {
  all: () => ["device-data"],

  lists: (params: DeviceDataListParams = {}) => [
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
    DeviceDataListParams
  > = {}) =>
    queryOptions({
      queryKey: [...deviceDataQueries.lists(params)],
      queryFn: async ({ signal }) => getDeviceDataList({ signal, params }),
      ...options,
    }),
};
