import type { DefaultError, UseQueryOptions } from "@tanstack/react-query";

export interface InfinityListData<D extends object> {
  pages: D[];
  pageParams: number[];
}

export interface BaseUseQueryOptions<
  TFnData extends object | null,
  TData extends object | undefined = TFnData extends null ? undefined : TFnData,
  TParams extends object | undefined = undefined,
> extends Omit<UseQueryOptions<TFnData, DefaultError, TData>, "queryKey"> {
  params?: TParams;
}
