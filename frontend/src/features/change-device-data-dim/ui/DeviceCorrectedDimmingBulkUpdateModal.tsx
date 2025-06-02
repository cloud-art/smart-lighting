import {
  App,
  Form,
  FormItemProps,
  FormProps,
  InputNumber,
  ModalProps,
} from "antd";
import type { FC, ReactNode } from "react";

import { useRef } from "react";
import { useApiErrorHandler } from "~/shared/api/error";
import {
  DeviceDataSummaryBulkUpdateBody,
  DeviceDataSummaryBulkUpdateResponse,
} from "~/shared/api/services/device-data-summary";
import { ModalButton, ModalButtonRef } from "~/shared/ui/modal-button";
import { useBulkChangeDeviceDataDim } from "../api/useBulkChangeDeviceDataDim";

export type DeviceCorrectedDimmingBulkUpdateFormInstance = Pick<
  DeviceDataSummaryBulkUpdateBody,
  "corrected_dimming_level"
>;

export type DeviceCorrectedDimmingBulkUpdateModalProps = {
  deviceDataIds: number[];
  modal?: ModalProps;
  form?: FormProps<DeviceCorrectedDimmingBulkUpdateFormInstance>;
  dimFormItem?: FormItemProps;
  renderButton?: (onClick: () => void) => ReactNode;
  onSuccess?: (data: DeviceDataSummaryBulkUpdateResponse) => void;
};

export const DeviceCorrectedDimmingBulkUpdateModal: FC<
  DeviceCorrectedDimmingBulkUpdateModalProps
> = ({
  deviceDataIds,
  modal,
  form: formProps,
  dimFormItem,
  renderButton,
  onSuccess,
}) => {
  const { message } = App.useApp();
  const [form] = Form.useForm<DeviceCorrectedDimmingBulkUpdateFormInstance>();
  const modalButtonRef = useRef<ModalButtonRef>(null);

  const handleClose = () => {
    modalButtonRef.current?.close();
    form.resetFields();
  };

  const { handleApiFormError } = useApiErrorHandler();
  const editCorrectedDimmingMutation = useBulkChangeDeviceDataDim({
    onSuccess: (data) => {
      onSuccess?.(data);
      handleClose();
    },
    onError: (error) => handleApiFormError(form, error),
  });

  const handleSubmit = async () => {
    try {
      const data = await form.validateFields();
      editCorrectedDimmingMutation.mutateAsync(
        deviceDataIds.map((deviceData) => ({
          device_data_id: deviceData,
          corrected_dimming_level: data.corrected_dimming_level,
        }))
      );
    } catch {
      message.error("Ошибка валидации формы");
    }
  };

  return (
    <ModalButton
      destroyOnHidden
      ref={modalButtonRef}
      title="Изменение данных устройств"
      onOk={handleSubmit}
      okText={"Сохранить"}
      renderButton={renderButton}
      onCancel={handleClose}
      okButtonProps={{
        loading: editCorrectedDimmingMutation.isPending,
      }}
      modalRender={(node) => (
        <Form form={form} layout="vertical" {...formProps}>
          {node}
        </Form>
      )}
      {...modal}
    >
      <Form.Item
        label="Экспертное значение диммирования"
        name="corrected_dimming_level"
        rules={[{ required: true }]}
        {...dimFormItem}
      >
        <InputNumber
          className="w-full"
          placeholder="Введите значение"
          min={0}
          max={100}
        />
      </Form.Item>
    </ModalButton>
  );
};
