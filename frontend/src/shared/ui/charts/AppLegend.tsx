import { Tooltip } from "antd";
import clsx from "clsx";
import type { FC } from "react";
import type { Props as LegendProps } from "recharts/types/component/DefaultLegendContent";

export type LegendValue = {
  id?: string | number;
  label?: string;
  value?: string;
  color?: string;
};

export type AppLegendProps = {
  values?: LegendValue[];
  hasValue?: boolean;
  layout?: LegendProps["layout"];
};

export const AppLegend: FC<AppLegendProps> = ({ values, hasValue, layout }) => {
  //#region Render
  return (
    <ul className={clsx("v-stack list-none gap-4", "max-md:m-0 max-md:p-0")}>
      {values?.map(({ label, color, value }) => (
        <Tooltip key={label} title={label}>
          <li
            className={clsx(
              "h-stack items-center gap-2",
              layout === "horizontal" ? "max-w-auto" : "max-w-80"
            )}
          >
            <div
              className="h-5 w-5 shrink-0 rounded-sm"
              style={{ backgroundColor: color }}
            ></div>

            <div className="h-stack min-w-0">
              <span className="truncate text-[#445371]">{label}</span>
              {hasValue && <span>:</span>}
            </div>

            {hasValue && (
              <>
                <span className="flex-1"></span>
                <span className="font-medium text-[#1C1E20]">{value}</span>
              </>
            )}
          </li>
        </Tooltip>
      ))}
    </ul>
  );
  //#endregion
};
