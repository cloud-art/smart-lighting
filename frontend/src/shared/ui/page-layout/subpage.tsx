import type { FC, PropsWithChildren, ReactNode } from "react";
import { useNavigate } from "react-router";

import { ArrowLeftOutlined } from "@ant-design/icons";
import { Button, Typography } from "antd";
import { isDef } from "~/shared/lib/is";

const { Title } = Typography;

export type AppSubPageProps = PropsWithChildren<{
  title?: string;
  hasBackButton?: boolean;
  backButton?: ReactNode;
  containerClassName?: string;
}>;

export const AppSubPage: FC<AppSubPageProps> = ({
  title,
  hasBackButton,
  backButton,
  containerClassName,
  children,
}) => {
  const navigate = useNavigate();

  const backButtonElement = backButton ?? (
    <Button
      variant="link"
      className="w-fit"
      icon={<ArrowLeftOutlined />}
      onClick={async () => navigate(-1)}
    >
      Назад
    </Button>
  );

  return (
    <div className="flex flex-col gap-6">
      {hasBackButton && backButtonElement}
      {isDef(title) && <Title level={2}>{title}</Title>}

      <div className={containerClassName}>{children}</div>
    </div>
  );
};
