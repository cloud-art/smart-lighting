import type { DefaultError, MutationOptions } from "@tanstack/react-query";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deviceDataSummaryQueries } from "~/shared/api/queries/device-data-summary";

import {
  DeviceDataSummary,
  DeviceDataSummaryUpdateBody,
  patchDeviceDataSummary,
} from "~/shared/api/services/device-data-summary";
import { handleError } from "~/shared/lib/api";

export function useChangeDeviceDataDim({
  onSuccess,
  onError,
  ...options
}: MutationOptions<
  DeviceDataSummary,
  DefaultError,
  DeviceDataSummaryUpdateBody & { id?: number }
>) {
  const queryClient = useQueryClient();

  return useMutation({
    ...options,
    onSuccess: async (...args) => {
      onSuccess?.(...args);
      await queryClient.invalidateQueries({
        queryKey: deviceDataSummaryQueries.lists(),
      });
    },
    onError: (e, ...args) => {
      handleError(e);
      onError?.(e, ...args);
    },
    mutationFn: ({ id, ...data }) => {
      if (!id) throw new Error("id required");
      return patchDeviceDataSummary(id, data);
    },
  });
}
