import { DataType } from "./data-type";

export const dateFormat: Record<
  DataType.DATE | DataType.TIME | DataType.DATETIME,
  string
> = {
  [DataType.DATE]: "dd.MM.yyyy",
  [DataType.TIME]: "HH:mm:ss",
  [DataType.DATETIME]: `dd.MM.yyyy, HH:mm:ss`,
};
