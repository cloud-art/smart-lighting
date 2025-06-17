import type { PaginatedResponse, PaginationParams } from "~/shared/lib/api";
import type { BaseUseQueryOptions } from "./common";

import { queryOptions } from "@tanstack/react-query";

import { Device, getDeviceById, getDeviceList } from "../services/device";

export const deviceQueries = {
  all: () => ["device"],

  lists: (params: PaginationParams = {}) => [
    ...deviceQueries.all(),
    "list",
    params,
  ],

  list: <TData extends object = PaginatedResponse<Device>>({
    params,
    ...options
  }: BaseUseQueryOptions<
    PaginatedResponse<Device>,
    TData,
    PaginationParams
  > = {}) =>
    queryOptions({
      queryKey: [...deviceQueries.lists(params)],
      queryFn: async ({ signal }) => getDeviceList({ signal, params }),
      ...options,
    }),

  details: (id: number) => [...deviceQueries.all(), "detail", id],

  byId: <TData extends object = Device>(
    id: number | undefined,
    { params, ...options }: BaseUseQueryOptions<Device, TData> = {}
  ) => {
    if (id === undefined) {
      throw new Error("Detail query should have `id` property");
    }
    return queryOptions({
      queryKey: [...deviceQueries.details(id)],
      queryFn: async ({ signal }) => getDeviceById(id, { signal, params }),
      ...options,
    });
  },
};
