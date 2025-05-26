import type { FC, PropsWithChildren } from "react";

import { Typography } from "antd";
import clsx from "clsx";
import { isDef } from "~/shared/lib/is";

const { Title } = Typography;

export type AppPageProps = PropsWithChildren<{
  title?: string;
  gap?: "lg" | "md";
  containerClassName?: string;
}>;

export const AppPage: FC<AppPageProps> = ({
  gap = "md",
  title,
  containerClassName,
  children,
}) => {
  return (
    <div
      className={clsx(
        "flex flex-col h-full overflow-auto",
        gap === "lg" ? 8 : 6
      )}
    >
      {isDef(title) && <Title level={3}>{title}</Title>}

      <div className={clsx(containerClassName, "min-h-0 h-full ")}>
        {children}
      </div>
    </div>
  );
};
