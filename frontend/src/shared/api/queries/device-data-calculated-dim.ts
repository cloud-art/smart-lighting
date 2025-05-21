import type { PaginatedResponse, PaginationParams } from "~/shared/lib/api";
import type { BaseUseQueryOptions } from "./common";

import { queryOptions } from "@tanstack/react-query";

import {
  DeviceDataCalculatedDim,
  getDeviceDataCalculatedDimList,
} from "../services/device-data-calculated-dim";

export const deviceDataCalculatedDimQueries = {
  all: () => ["device-data-calculated-dim"],

  lists: (params: PaginationParams = {}) => [
    ...deviceDataCalculatedDimQueries.all(),
    "list",
    params,
  ],

  list: <TData extends object = PaginatedResponse<DeviceDataCalculatedDim>>({
    params,
    ...options
  }: BaseUseQueryOptions<
    PaginatedResponse<DeviceDataCalculatedDim>,
    TData,
    PaginationParams
  > = {}) =>
    queryOptions({
      queryKey: [...deviceDataCalculatedDimQueries.lists(params)],
      queryFn: async ({ signal }) =>
        getDeviceDataCalculatedDimList({ signal, params }),
      ...options,
    }),
};
