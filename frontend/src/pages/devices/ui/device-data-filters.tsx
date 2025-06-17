import { useQuery } from "@tanstack/react-query";
import { Flex, Form, Select } from "antd";
import { type FC } from "react";
import { deviceQueries } from "~/shared/api/queries/device";
import { DatePicker } from "~/shared/ui/date-picker";

export type DeviceDataFilterValues = {
  device?: number;
  start_date?: Date;
  end_date?: Date;
};

export type DeviceDataFiltersProps = {
  value: DeviceDataFilterValues;
  onChange: (value: DeviceDataFilterValues) => void;
};

export const DeviceDataFilters: FC<DeviceDataFiltersProps> = ({
  value,
  onChange,
}) => {
  const devices = useQuery(
    deviceQueries.list({
      select: (data) =>
        data.results.map(({ id: value, serial_number: label }) => ({
          label,
          value,
        })),
    })
  );

  return (
    <Flex gap={12} align="center">
      <Form.Item layout="vertical" label="Устройство">
        <Select
          allowClear
          showSearch
          optionFilterProp="label"
          value={value.device}
          onChange={(device) => onChange({ ...value, device })}
          loading={devices.isLoading}
          options={devices.data}
          placeholder="Выберите устройство"
        />
      </Form.Item>

      <Form.Item layout="vertical" label="Дата начала">
        <DatePicker
          showTime
          className="w-full"
          value={value.start_date}
          onChange={(start_date) => onChange({ ...value, start_date })}
          allowClear
        />
      </Form.Item>

      <Form.Item layout="vertical" label="Дата окончания">
        <DatePicker
          showTime
          className="w-full"
          value={value.end_date}
          onChange={(end_date) => onChange({ ...value, end_date })}
          allowClear
        />
      </Form.Item>
    </Flex>
  );
};
