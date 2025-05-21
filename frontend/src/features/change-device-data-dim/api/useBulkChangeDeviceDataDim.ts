import type { DefaultError, MutationOptions } from "@tanstack/react-query";

import { useMutation } from "@tanstack/react-query";

import {
  deviceDataSummaryBulkUpdate,
  DeviceDataSummaryBulkUpdateResponse,
  DeviceDataSummaryUpdateBody,
} from "~/shared/api/services/device-data-summary";
import { handleError } from "~/shared/lib/api";

export function useBulkChangeDeviceDataDim({
  onSuccess,
  onError,
  ...options
}: MutationOptions<
  DeviceDataSummaryBulkUpdateResponse,
  DefaultError,
  DeviceDataSummaryUpdateBody[]
>) {
  return useMutation({
    ...options,
    onSuccess: async (...args) => {
      onSuccess?.(...args);
    },
    onError: (e, ...args) => {
      handleError(e);
      onError?.(e, ...args);
    },
    mutationFn: deviceDataSummaryBulkUpdate,
  });
}
