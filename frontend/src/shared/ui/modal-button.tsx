import { Button, Modal, ModalProps } from "antd";
import type { FC, ReactNode, Ref } from "react";

import { useImperativeHandle, useState } from "react";
import { isDef } from "~/shared/lib/is";

export type ModalButtonRef = {
  close: () => void;
  open: () => void;
};

export type ModalButtonProps = {
  renderButton?: (onClick: () => void) => ReactNode;
  ref?: Ref<ModalButtonRef>;
} & ModalProps;

export const ModalButton: FC<ModalButtonProps> = ({
  renderButton,
  onCancel,
  ref,
  ...props
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const handleOpen = () => setIsOpen(true);
  const handleClose = () => setIsOpen(false);

  useImperativeHandle(ref, () => ({
    open: handleOpen,
    close: handleClose,
  }));

  return (
    <>
      {isDef(renderButton) ? (
        renderButton(handleOpen)
      ) : (
        <Button onClick={handleOpen}>Открыть</Button>
      )}

      <Modal
        open={isOpen}
        onCancel={(e) => {
          handleClose();
          onCancel?.(e);
        }}
        {...props}
      />
    </>
  );
};
