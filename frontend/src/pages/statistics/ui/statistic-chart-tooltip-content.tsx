import { Flex, Typography } from "antd";
import type { FC } from "react";

const { Title, Text } = Typography;

type StatisticChartTooltipContentData = {
  label: string;
  value?: string | number | null;
  color?: string;
};

export type StatisticChartTooltipContentProps = {
  title: string;
  data: StatisticChartTooltipContentData[];
};

export const StatisticChartTooltipContent: FC<
  StatisticChartTooltipContentProps
> = ({ title, data }) => {
  const renderValue = (value?: string | number | null) => {
    if (value === undefined || value === null) return "отсутствует";
    if (typeof value === "number") return value.toFixed(1);
    return value;
  };

  return (
    <Flex vertical gap={4} className="bg-primary-bg p-2 rounded-md">
      <Title level={4}>{title}</Title>

      {data.map(({ label, value, color }) => (
        <Flex gap={2} align="center">
          <Text color={color}>{label}:</Text>
          <Text>{renderValue(value)}</Text>
        </Flex>
      ))}
    </Flex>
  );
};
