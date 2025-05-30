export const DEFAULT_PAGE_SIZE = 20;

export interface PaginatedResponse<T> {
  results: T[];
  count: number;
  next: string | null;
  previous: string | null;
}

export interface PaginationParams {
  page?: number;
  page_size?: number;
}

export const handleError = (error: Error) => {
  console.error(error.message);
};
