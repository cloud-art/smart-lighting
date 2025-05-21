import type { PaginatedResponse } from "~/shared/lib/api";

import { AxiosRequestConfig } from "axios";
import { client } from "../client";
import { DeviceData } from "./device-data";

const ENDPOINT = "api/device_data_summary/";

export type DeviceDataSummary = DeviceData & {
  calculated_dimming_level: number;
  corrected_dimming_level: number;
};

export type DeviceDataSummaryUpdateData = {
  device_data_id: number;
  corrected_dimming_level: number;
};

export type DeviceDataSummaryUpdateResponse = DeviceDataSummaryUpdateData & {
  success: boolean;
};

export type DeviceDataSummaryBulkErrorData = {
  device_data_id: number | null;
  error: string;
};

export type DeviceDataSummaryUpdateBody = {
  corrected_dimming_level: number;
};

export type DeviceDataSummaryBulkUpdateResponse = {
  total_requests: number;
  successful_updates: DeviceDataSummaryUpdateData[];
  failed_updates: DeviceDataSummaryBulkErrorData[];
};

export const getDeviceDataSummaryList = (config?: AxiosRequestConfig) => {
  return client.get<PaginatedResponse<DeviceDataSummary>>(ENDPOINT, config);
};

export const patchDeviceDataSummary = (
  id: number,
  data: DeviceDataSummaryUpdateBody,
  config?: AxiosRequestConfig
) => {
  return client.patch<DeviceDataSummaryUpdateResponse>(
    ENDPOINT.concat(`device_data_summary/${id}/`),
    data,
    config
  );
};

export const deviceDataSummaryBulkUpdate = (
  data: DeviceDataSummaryUpdateBody[],
  config?: AxiosRequestConfig
) => {
  return client.post<DeviceDataSummaryBulkUpdateResponse>(
    ENDPOINT.concat("device_data_summary/bulk_update/"),
    data,
    config
  );
};
