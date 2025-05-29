export function isDef<T = unknown>(val?: T): val is T {
  return typeof val !== "undefined";
}
export function notNullish<T = unknown>(val?: T | null | undefined): val is T {
  return val != null;
}
export function isNonEmptyArray<T>(arr: unknown): arr is T[] {
  return Array.isArray(arr) && arr.length > 0;
}
