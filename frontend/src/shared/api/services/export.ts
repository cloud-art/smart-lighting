import { AxiosRequestConfig } from "axios";
import { client } from "../client";

const ENDPOINT = "api/export/";

export type ExportDeviceDataParams = {
  device?: Number;
  start_date?: string;
  end_date?: string;
};

export const exportDeviceData = (config?: AxiosRequestConfig) => {
  return client.get<string>(ENDPOINT.concat("device_data_csv/"), config);
};
