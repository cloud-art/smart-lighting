import type { PaginatedResponse, PaginationParams } from "~/shared/lib/api";
import type { BaseUseQueryOptions } from "./common";

import { queryOptions } from "@tanstack/react-query";

import {
  DeviceDataCorrectedDim,
  getDeviceDataCorrectedDimList,
} from "../services/device-data-corrected-dim";

export type DeviceDataCorrectedDimListParams = PaginationParams & {
  device?: Number
}

export const deviceDataCorrectedDimQueries = {
  all: () => ["device-data-corrected-dim"],

  lists: (params: DeviceDataCorrectedDimListParams = {}) => [
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
    DeviceDataCorrectedDimListParams
  > = {}) =>
    queryOptions({
      queryKey: [...deviceDataCorrectedDimQueries.lists(params)],
      queryFn: async ({ signal }) =>
        getDeviceDataCorrectedDimList({ signal, params }),
      ...options,
    }),
};
