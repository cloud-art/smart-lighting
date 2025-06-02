import { EditOutlined } from "@ant-design/icons";
import { useQuery } from "@tanstack/react-query";
import { Button, Flex, Table, TableColumnsType, TableProps } from "antd";
import { format, parseISO } from "date-fns";
import { Key, useEffect, useState, type FC } from "react";
import { DeviceCorrectedDimmingUpdateModal } from "~/features/change-device-data-dim";
import { DeviceCorrectedDimmingBulkUpdateModal } from "~/features/change-device-data-dim/ui/DeviceCorrectedDimmingBulkUpdateModal";
import { deviceDataSummaryQueries } from "~/shared/api/queries/device-data-summary";
import { DeviceDataSummary } from "~/shared/api/services/device-data-summary";
import { PaginationParams } from "~/shared/lib/api";
import { dateFormat } from "~/shared/lib/date";

import { AppPage } from "~/shared/ui/page-layout";

const PAGE_SIZE = 20;

const DevicesPage: FC = () => {
  const [pagination, setPagination] = useState<PaginationParams>({
    page_size: PAGE_SIZE,
    page: 1,
  });

  const [isMultipleMode, setIsMultipleMode] = useState(false);
  const [selectedDevices, setSelectedDevices] = useState<number[]>([]);

  const deviceDataSummaryQuery = useQuery({
    ...deviceDataSummaryQueries.list({
      params: pagination,
    }),
    placeholderData: (data) => data,
  });

  const tableColumns: TableColumnsType<DeviceDataSummary> = [
    {
      dataIndex: "timestamp",
      title: "Время",
      fixed: "left",
      align: "left",
      render: (datetime: string) => {
        const parsedDate = parseISO(datetime);
        return format(parsedDate, dateFormat.datetime);
      },
    },
    { dataIndex: "serial_number", title: "Серийный номер" },
    { dataIndex: "latitude", title: "Широта" },
    { dataIndex: "longitude", title: "Долгота" },
    { dataIndex: "car_count", title: "Кол-во машин" },
    { dataIndex: "traffic_speed", title: "Скорость страфика" },
    { dataIndex: "traffic_density", title: "Плотность трафика" },
    {
      dataIndex: "pedestrian_count",
      title: "Количество пешеходов",
    },
    {
      dataIndex: "pedestrian_density",
      title: "Плотность пешеходов",
    },
    { dataIndex: "ambient_light", title: "Внешнее освещение" },
    {
      dataIndex: "lighting_class",
      title: "Класс освещения дороги",
    },
    { dataIndex: "lamp_power", title: "Мощность лампы" },
    { dataIndex: "weather", title: "Погода" },
    {
      dataIndex: "dimming_level",
      title: "Уровень диммирования",
      fixed: "right",
    },
    {
      dataIndex: "calculated_dimming_level",
      title: "Вычисленное значение",
      fixed: "right",
    },
    {
      dataIndex: "corrected_dimming_level",
      title: "Экспертное значение",
      fixed: "right",
      render: (value: string | null | undefined, record) => {
        let formatedValue = value;
        if (value === undefined || value === null) {
          formatedValue = "-";
        }

        return (
          <Flex gap={8} justify="space-around" align="center">
            {formatedValue}

            <DeviceCorrectedDimmingUpdateModal
              form={{
                initialValues: {
                  id: record.id,
                  corrected_dimming_level: record.corrected_dimming_level,
                },
              }}
              idFormItem={{ hidden: true }}
              renderButton={(onClick) => (
                <Button type="text" icon={<EditOutlined />} onClick={onClick} />
              )}
            />
          </Flex>
        );
      },
    },
  ];

  const rowSelection: TableProps<DeviceDataSummary>["rowSelection"] =
    isMultipleMode
      ? {
          selectedRowKeys: selectedDevices,
          onChange: (keys: Key[]) => {
            const newSelectedDevices = keys.filter(
              (key) => typeof key === "number"
            );
            setSelectedDevices(newSelectedDevices);
          },
        }
      : undefined;

  const renderDeviceTableColumns = (
    columns: TableColumnsType<DeviceDataSummary>
  ): TableColumnsType<DeviceDataSummary> =>
    columns.map((column) => ({
      align: "center",
      width: 100,
      render: (value: unknown) => {
        if (value === null || value === undefined) return "-";
        return value;
      },
      ...column,
    }));

  useEffect(() => {
    setSelectedDevices([]);
  }, [isMultipleMode]);

  return (
    <AppPage title="Устройства" containerClassName="flex flex-col gap-2">
      <Flex gap={8} align="center" justify="space-between">
        <Button onClick={() => setIsMultipleMode((v) => !v)}>
          {isMultipleMode
            ? "Выключить режим изменения"
            : "Включить режим изменения"}
        </Button>

        {isMultipleMode === true && (
          <DeviceCorrectedDimmingBulkUpdateModal
            onSuccess={() => setIsMultipleMode(false)}
            renderButton={(onClick) => (
              <Button onClick={onClick} type="primary">
                Изменить
              </Button>
            )}
            deviceDataIds={selectedDevices}
          />
        )}
      </Flex>

      <Table
        sticky
        size="small"
        columns={renderDeviceTableColumns(tableColumns)}
        dataSource={deviceDataSummaryQuery.data?.results}
        loading={deviceDataSummaryQuery.isFetching}
        rowKey={(record) => record.id}
        rowSelection={rowSelection}
        pagination={{
          current: pagination.page,
          pageSize: pagination.page_size,
          hideOnSinglePage: true,
          total: deviceDataSummaryQuery.data?.count,
          onChange: (page, page_size) => setPagination({ page, page_size }),
        }}
        scroll={{ x: "max-content", y: 600 }}
      />
    </AppPage>
  );
};

export default DevicesPage;
