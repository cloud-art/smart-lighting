import type { PaginatedResponse } from "~/shared/lib/api";

import { AxiosRequestConfig } from "axios";
import { client } from "../client";

const ENDPOINT = "api/device_data_corrected_dim/";

export type DeviceDataCorrectedDim = {
  id: number;
  dimming_level: number;
};

export const getDeviceDataCorrectedDimList = (config?: AxiosRequestConfig) => {
  return client.get<PaginatedResponse<DeviceDataCorrectedDim>>(
    ENDPOINT,
    config
  );
};
