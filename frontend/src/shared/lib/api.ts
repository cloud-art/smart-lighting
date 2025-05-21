import { notNullish } from "./is";

export const DEFAULT_PAGE_SIZE = 20;

export interface PaginatedResponse<T> {
  results: T[];
  count: number;
  next: string | null;
  previous: string | null;
}

export interface PaginationParams {
  page?: number;
  pageSize?: number;
}

export const handleError = (error: Error) => {
  console.error(error.message);
};

export function adaptPaginationParams({ pageSize, page }: PaginationParams) {
  return {
    page,
    page_size: pageSize,
  };
}

export function getPaginatedResponseNextPageParam({
  next,
}: PaginatedResponse<unknown>) {
  return notNullish(next)
    ? (new URL(next).searchParams.get("page") ?? undefined)
    : undefined;
}
