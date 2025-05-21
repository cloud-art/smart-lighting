import axios, { AxiosRequestConfig } from "axios";
import { BACKEND_URL } from "../config";

export const instance = axios.create({
  baseURL: BACKEND_URL,
});

export const client = {
  // eslint-disable-next-line @typescript-eslint/no-unnecessary-type-constraint, @typescript-eslint/no-explicit-any
  request: async <T extends any>(
    url: string,
    config?: AxiosRequestConfig
  ): Promise<T> => {
    const response = await instance<T>(url, config);

    return response.data;
  },
  options<T = unknown>(url: string, config?: AxiosRequestConfig) {
    return this.request<T>(url, { ...config, method: "OPTIONS" });
  },
  get<T = unknown>(url: string, config?: AxiosRequestConfig) {
    return this.request<T>(url, { ...config, method: "GET" });
  },
  post<T = unknown>(
    url: string,
    data: AxiosRequestConfig["data"],
    config?: AxiosRequestConfig
  ) {
    return this.request<T>(url, {
      ...config,
      method: "POST",
      data,
    });
  },
  put<T = unknown>(
    url: string,
    data: AxiosRequestConfig["data"],
    config?: AxiosRequestConfig
  ) {
    return this.request<T>(url, {
      ...config,
      method: "PUT",
      data,
    });
  },
  patch<T = unknown>(
    url: string,
    data: AxiosRequestConfig["data"],
    config?: AxiosRequestConfig
  ) {
    return this.request<T>(url, {
      ...config,
      method: "PATCH",
      data,
    });
  },
  delete<T = unknown>(url: string, config?: AxiosRequestConfig) {
    return this.request<T>(url, {
      ...config,
      method: "DELETE",
    });
  },
};
