import { AxiosRequestConfig } from "axios";
import { client } from "../client";

const ENDPOINT = "api/device-stats/";

export type DeviceStatsAverages = {
  avg_car_count: number | null;
  avg_traffic_speed: number | null;
  avg_pedestrian_count: number | null;
  avg_dimming_level: number | null;
  avg_calculated_dim: number | null;
  avg_corrected_dim: number | null;
};

export type DeviceDataHourlyAverages = DeviceStatsAverages & {
  hour: number;
};

export type DeviceDataWeekdayAverages = DeviceStatsAverages & {
  day: number;
  day_name: string;
};

export type DeviceDataDayAverages = DeviceStatsAverages & {
  day_of_month: number;
};

export const getDeviceDataHourlyAverages = (config?: AxiosRequestConfig) => {
  return client.get<DeviceDataHourlyAverages[]>(
    ENDPOINT.concat("hourly-averages/"),
    config
  );
};

export const getDeviceDataWeekdayAverages = (config?: AxiosRequestConfig) => {
  return client.get<DeviceDataWeekdayAverages[]>(
    ENDPOINT.concat("weekday-averages/"),
    config
  );
};

export const getDeviceDataDailyAverages = (config?: AxiosRequestConfig) => {
  return client.get<DeviceDataDayAverages[]>(
    ENDPOINT.concat("daily-averages/"),
    config
  );
};
