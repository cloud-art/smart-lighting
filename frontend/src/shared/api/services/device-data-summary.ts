import type { PaginatedResponse } from "~/shared/lib/api";

import { AxiosRequestConfig } from "axios";
import { client } from "../client";
import { DeviceData } from "./device-data";
import { DeviceDataCalculatedDim } from "./device-data-calculated-dim";
import { DeviceDataCorrectedDim } from "./device-data-corrected-dim";

const ENDPOINT = "api/device-data-summary/";

export type DeviceDataSummary = DeviceData & {
  calculated_dimming_level: DeviceDataCalculatedDim | null;
  corrected_dimming_level: DeviceDataCorrectedDim | null;
};

export type DeviceDataSummaryUpdateData = {
  device_data_id: number;
  corrected_dimming_level: number;
};

export type DeviceDataSummaryUpdateBody = {
  corrected_dimming_level: number;
};

export type DeviceDataSummaryBulkUpdateBody = DeviceDataSummaryUpdateBody & {
  ids: number[];
};

export const getDeviceDataSummaryList = (config?: AxiosRequestConfig) => {
  return client.get<PaginatedResponse<DeviceDataSummary>>(ENDPOINT, config);
};

export const patchDeviceDataSummary = (
  id: number,
  data: DeviceDataSummaryUpdateBody,
  config?: AxiosRequestConfig
) => {
  return client.patch<DeviceDataSummary>(
    ENDPOINT.concat(`${id}/`),
    data,
    config
  );
};

export const deviceDataSummaryBulkUpdate = (
  data: DeviceDataSummaryUpdateBody,
  config?: AxiosRequestConfig
) => {
  return client.post<number>(ENDPOINT.concat("bulk_update/"), data, config);
};
