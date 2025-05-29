/* eslint-disable @typescript-eslint/no-explicit-any */
export function isDef<T = any>(val?: T): val is T {
  return typeof val !== "undefined";
}
export function notNullish<T = any>(val?: T | null | undefined): val is T {
  return val != null;
}
export function isNonEmptyArray<T>(arr: any): arr is T[] {
  return Array.isArray(arr) && arr.length > 0;
}

export const isFunction = <T extends (...args: any) => any>(
  value: any
): value is T => value instanceof Function;
/* eslint-enable @typescript-eslint/no-explicit-any */
