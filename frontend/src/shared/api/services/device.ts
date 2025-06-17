import type { PaginatedResponse } from "~/shared/lib/api";

import { AxiosRequestConfig } from "axios";
import { client } from "../client";

const ENDPOINT = "api/device/";

export enum LightingClass {
    A1 = "A1",
    B1 = "B1",
    C1 = "C1",
    D1 = "D1",
}

export enum DeviceControlType {
    SIMPLE_RULES = "simple_rules",
    AI_MODEL = "ai_model",
}

export type Device = {
    control_type: DeviceControlType,
    serial_number: string,
    lighting_class: LightingClass,
    latitude: number,
    longitude: number,
};

export const getDeviceList = (config?: AxiosRequestConfig) => {
    return client.get<PaginatedResponse<Device>>(ENDPOINT, config);
};

export const getDeviceById = (id: number, config?: AxiosRequestConfig) => {
    return client.get<Device>(ENDPOINT.concat(`${id}/`), config);
};