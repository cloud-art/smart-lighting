import type { DefaultError, MutationOptions } from "@tanstack/react-query";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deviceDataSummaryQueries } from "~/shared/api/queries/device-data-summary";

import {
  deviceDataSummaryBulkUpdate,
  DeviceDataSummaryBulkUpdateBody,
} from "~/shared/api/services/device-data-summary";
import { handleError } from "~/shared/lib/api";

export function useBulkChangeDeviceDataDim({
  onSuccess,
  onError,
  ...options
}: MutationOptions<number, DefaultError, DeviceDataSummaryBulkUpdateBody>) {
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
    mutationFn: deviceDataSummaryBulkUpdate,
  });
}
