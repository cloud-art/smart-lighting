import type { PaginatedResponse } from "~/shared/lib/api";

import { AxiosRequestConfig } from "axios";
import { client } from "../client";

const ENDPOINT = "api/device_data/";

export enum LightingClass {
  A1 = "A1",
  B1 = "B1",
  C1 = "C1",
  D1 = "D1",
}

export enum WeatherType {
  CLEAR = "clear",
  CLOUDS = "clouds",
  RAIN = "rain",
  FOG = "fog",
}

export type DeviceData = {
  id: number;
  timestamp: string;
  serial_number: number;
  latitude: number;
  longitude: number;
  car_count: number;
  traffic_speed: number;
  traffic_density: number;
  pedestrian_count: number;
  pedestrian_density: number;
  ambient_light: number;
  dimming_level: number;
  lighting_class: LightingClass;
  lamp_power: number;
  weather: WeatherType;
};

export type DeviceDataAverages = {
  avg_car_count: number;
  avg_traffic_speed: number;
  avg_pedestrian_count: number;
  avg_dimming_level: number;
  avg_calculated_dim: number;
  avg_corrected_dim: number;
};

export type DeviceDataHourlyAverages = DeviceDataAverages & {
  hour: number;
};

export type DeviceDataWeekdayAverages = DeviceDataAverages & {
  day: number;
};

export type DeviceDataDayAverages = DeviceDataAverages & {
  day_of_month: number;
};

export const getDeviceDataList = (config?: AxiosRequestConfig) => {
  return client.get<PaginatedResponse<DeviceData>>(ENDPOINT, config);
};

export const getDeviceDataHourlyAverages = (config?: AxiosRequestConfig) => {
  return client.get<DeviceDataHourlyAverages[]>(
    ENDPOINT.concat("hourly_averages/"),
    config
  );
};

export const getDeviceDataWeekdayAverages = (config?: AxiosRequestConfig) => {
  return client.get<DeviceDataWeekdayAverages[]>(
    ENDPOINT.concat("weekday_averages/"),
    config
  );
};

export const getDeviceDataDailyAverages = (config?: AxiosRequestConfig) => {
  return client.get<DeviceDataDayAverages[]>(
    ENDPOINT.concat("daily_averages/"),
    config
  );
};
