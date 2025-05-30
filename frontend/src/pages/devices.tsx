import { useQuery } from "@tanstack/react-query";
import { Table, TableColumnsType } from "antd";
import { format, parseISO } from "date-fns";
import { useState, type FC } from "react";
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

  const deviceDataSummaryQuery = useQuery(
    deviceDataSummaryQueries.list({
      params: pagination,
    })
  );

  const tableColumns: TableColumnsType<DeviceDataSummary> = [
    {
      dataIndex: "timestamp",
      title: "Время",
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
    },
  ];

  const renderDeviceTableColumns = (
    columns: TableColumnsType<DeviceDataSummary>
  ): TableColumnsType<DeviceDataSummary> =>
    columns.map((column) => ({
      align: "center",
      width: 100,
      ...column,
    }));

  return (
    <AppPage title="Устройства">
      <Table
        sticky
        size="small"
        columns={renderDeviceTableColumns(tableColumns)}
        dataSource={deviceDataSummaryQuery.data?.results}
        loading={deviceDataSummaryQuery.isLoading}
        rowKey={(record) => record.id}
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
