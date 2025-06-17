import type { PaginatedResponse, PaginationParams } from "~/shared/lib/api";
import type { BaseUseQueryOptions } from "./common";

import { queryOptions } from "@tanstack/react-query";

import {
  DeviceDataSummary,
  getDeviceDataSummaryList,
} from "../services/device-data-summary";

export type DeviceDataSummaryListParams = PaginationParams & {
  device?: Number;
  start_date?: string;
  end_date?: string;
};

export const deviceDataSummaryQueries = {
  all: () => ["device-data-calculated-dim"],

  lists: (params: DeviceDataSummaryListParams = {}) => [
    ...deviceDataSummaryQueries.all(),
    "list",
    params,
  ],

  list: <TData extends object = PaginatedResponse<DeviceDataSummary>>({
    params,
    ...options
  }: BaseUseQueryOptions<
    PaginatedResponse<DeviceDataSummary>,
    TData,
    DeviceDataSummaryListParams
  > = {}) =>
    queryOptions({
      queryKey: [...deviceDataSummaryQueries.lists(params)],
      queryFn: async ({ signal }) =>
        getDeviceDataSummaryList({ signal, params }),
      ...options,
    }),
};
