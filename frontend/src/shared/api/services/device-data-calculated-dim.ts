import type { PaginatedResponse } from "~/shared/lib/api";

import { AxiosRequestConfig } from "axios";
import { client } from "../client";

const ENDPOINT = "api/device_data_calculated_dim/";

export type DeviceDataCalculatedDim = {
  id: number;
  dimming_level: number;
};

export const getDeviceDataCalculatedDimList = (config?: AxiosRequestConfig) => {
  return client.get<PaginatedResponse<DeviceDataCalculatedDim>>(
    ENDPOINT,
    config
  );
};
