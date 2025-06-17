import { App, ModalProps } from "antd";
import type { FC, ReactNode } from "react";

import { useRef, useState } from "react";
import { ModalButton, ModalButtonRef } from "~/shared/ui/modal-button";
import {
  ExportDeviceDataFilters,
  ExportDeviceDataFilterValues,
} from "./export-device-data-filters";
import { exportDeviceData } from "~/shared/api/services/export";
import { formatISO } from "date-fns";
import { download } from "~/shared/lib/download";

export type ExportDeviceDataModalProps = {
  renderButton?: (onClick: () => void) => ReactNode;
  modal?: ModalProps;
};

export const ExportDeviceDataModal: FC<ExportDeviceDataModalProps> = ({
  renderButton,
  modal,
}) => {
  const { message } = App.useApp();
  const modalButtonRef = useRef<ModalButtonRef>(null);
  const [isPending, setIsPending] = useState(false);
  const [filters, setFilters] = useState<ExportDeviceDataFilterValues>({});

  const handleExport = async () => {
    try {
      setIsPending(true);
      const data = await exportDeviceData({
        params: {
          device: filters.device,
          start_date: filters.start_date
            ? formatISO(filters.start_date)
            : undefined,
          end_date: filters.end_date ? formatISO(filters.end_date) : undefined,
        },
      });
      const url = window.URL.createObjectURL(new Blob([data]));
      download("exported_data.csv", url);

      modalButtonRef.current?.close();
    } catch {
      message.error("Ошибка валидации формы");
    } finally {
      setIsPending(false);
    }
  };

  return (
    <ModalButton
      destroyOnHidden
      ref={modalButtonRef}
      title="Экспорт данных об устройствах"
      onOk={handleExport}
      okText={"Выгрузить"}
      renderButton={renderButton}
      onCancel={modalButtonRef.current?.close}
      okButtonProps={{
        loading: isPending,
      }}
      {...modal}
    >
      <ExportDeviceDataFilters value={filters} onChange={setFilters} />
    </ModalButton>
  );
};
