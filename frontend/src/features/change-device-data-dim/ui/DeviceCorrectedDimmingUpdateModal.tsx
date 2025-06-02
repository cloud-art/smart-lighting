import {
  App,
  Form,
  FormItemProps,
  FormProps,
  Input,
  InputNumber,
  ModalProps,
} from "antd";
import type { FC, ReactNode } from "react";

import { useRef } from "react";
import { useApiErrorHandler } from "~/shared/api/error";
import { DeviceDataSummaryUpdateBody } from "~/shared/api/services/device-data-summary";
import { ModalButton, ModalButtonRef } from "~/shared/ui/modal-button";
import { useChangeDeviceDataDim } from "../api/useChangeDeviceDataDim";

export type DeviceCorrectedDimmingUpdateFormInstance =
  DeviceDataSummaryUpdateBody & { id: number };

export type DeviceCorrectedDimmingUpdateModalProps = {
  renderButton?: (onClick: () => void) => ReactNode;
  modal?: ModalProps;
  form?: FormProps<DeviceCorrectedDimmingUpdateFormInstance>;
  idFormItem?: FormItemProps;
  dimFormItem?: FormItemProps;
};

export const DeviceCorrectedDimmingUpdateModal: FC<
  DeviceCorrectedDimmingUpdateModalProps
> = ({ renderButton, modal, form: formProps, idFormItem, dimFormItem }) => {
  const { message } = App.useApp();
  const [form] = Form.useForm<DeviceCorrectedDimmingUpdateFormInstance>();
  const modalButtonRef = useRef<ModalButtonRef>(null);

  const handleClose = () => {
    modalButtonRef.current?.close();
    form.resetFields();
  };

  const { handleApiFormError } = useApiErrorHandler();
  const editCorrectedDimmingMutation = useChangeDeviceDataDim({
    onSuccess: handleClose,
    onError: (error) => handleApiFormError(form, error),
  });

  const handleSubmit = async () => {
    try {
      const data = await form.validateFields();
      editCorrectedDimmingMutation.mutateAsync(data);
    } catch {
      message.error("Ошибка валидации формы");
    }
  };

  return (
    <ModalButton
      ref={modalButtonRef}
      title="Изменение данных устройства"
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
        label="ID"
        name="id"
        rules={[{ required: true }]}
        {...idFormItem}
      >
        <Input placeholder="Введите идентификатор" />
      </Form.Item>

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
