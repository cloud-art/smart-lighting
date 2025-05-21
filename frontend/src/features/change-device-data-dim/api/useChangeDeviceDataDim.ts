import type { DefaultError, MutationOptions } from "@tanstack/react-query";

import { useMutation } from "@tanstack/react-query";

import {
  DeviceDataSummaryUpdateBody,
  DeviceDataSummaryUpdateResponse,
  patchDeviceDataSummary,
} from "~/shared/api/services/device-data-summary";
import { handleError } from "~/shared/lib/api";

export function useChangeDeviceDataDim({
  onSuccess,
  onError,
  ...options
}: MutationOptions<
  DeviceDataSummaryUpdateResponse,
  DefaultError,
  DeviceDataSummaryUpdateBody & { id?: number }
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
    mutationFn: ({ id, ...data }) => {
      if (!id) throw new Error("id required");
      return patchDeviceDataSummary(id, data);
    },
  });
}
