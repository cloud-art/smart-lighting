import type { PaginatedResponse } from "~/shared/lib/api";

import { AxiosRequestConfig } from "axios";
import { client } from "../client";
import { Device } from "./device";

const ENDPOINT = "api/device-data/";

export enum WeatherType {
  CLEAR = "clear",
  CLOUDS = "clouds",
  RAIN = "rain",
  FOG = "fog",
}

export type DeviceData = {
  id: number;
  timestamp: string;
  device: Device;
  car_count: number;
  traffic_speed: number;
  traffic_density: number;
  pedestrian_count: number;
  pedestrian_density: number;
  ambient_light: number;
  dimming_level: number;
  lamp_power: number;
  weather: WeatherType;
};

export const getDeviceDataList = (config?: AxiosRequestConfig) => {
  return client.get<PaginatedResponse<DeviceData>>(ENDPOINT, config);
};
