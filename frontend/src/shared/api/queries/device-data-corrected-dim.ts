import type { PaginatedResponse, PaginationParams } from "~/shared/lib/api";
import type { BaseUseQueryOptions } from "./common";

import { queryOptions } from "@tanstack/react-query";

import {
  DeviceDataCorrectedDim,
  getDeviceDataCorrectedDimList,
} from "../services/device-data-corrected-dim";

export const deviceDataCorrectedDimQueries = {
  all: () => ["device-data-corrected-dim"],

  lists: (params: PaginationParams = {}) => [
    ...deviceDataCorrectedDimQueries.all(),
    "list",
    params,
  ],

  list: <TData extends object = PaginatedResponse<DeviceDataCorrectedDim>>({
    params,
    ...options
  }: BaseUseQueryOptions<
    PaginatedResponse<DeviceDataCorrectedDim>,
    TData,
    PaginationParams
  > = {}) =>
    queryOptions({
      queryKey: [...deviceDataCorrectedDimQueries.lists(params)],
      queryFn: async ({ signal }) =>
        getDeviceDataCorrectedDimList({ signal, params }),
      ...options,
    }),
};
