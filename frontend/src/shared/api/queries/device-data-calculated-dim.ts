import type { PaginatedResponse, PaginationParams } from "~/shared/lib/api";
import type { BaseUseQueryOptions } from "./common";

import { queryOptions } from "@tanstack/react-query";

import {
  DeviceDataCalculatedDim,
  getDeviceDataCalculatedDimList,
} from "../services/device-data-calculated-dim";

export type DeviceDataCalculatedDimListParams = PaginationParams & {
  device?: Number;
};

export const deviceDataCalculatedDimQueries = {
  all: () => ["device-data-calculated-dim"],

  lists: (params: DeviceDataCalculatedDimListParams = {}) => [
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
    DeviceDataCalculatedDimListParams
  > = {}) =>
    queryOptions({
      queryKey: [...deviceDataCalculatedDimQueries.lists(params)],
      queryFn: async ({ signal }) =>
        getDeviceDataCalculatedDimList({ signal, params }),
      ...options,
    }),
};
