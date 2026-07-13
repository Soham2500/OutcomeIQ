import { Modal } from "./Modal";

interface ConfirmationDialogProps {
  open: boolean;
  title: string;
  description: string;
  confirmLabel?: string;
  cancelLabel?: string;
  busy?: boolean;
  onCancel: () => void;
  onConfirm: () => void;
}

export function ConfirmationDialog({
  open,
  title,
  description,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  busy = false,
  onCancel,
  onConfirm,
}: ConfirmationDialogProps) {
  return (
    <Modal
      description={description}
      footer={
        <>
          <button className="secondary-button" disabled={busy} onClick={onCancel} type="button">
            {cancelLabel}
          </button>
          <button className="danger-button" disabled={busy} onClick={onConfirm} type="button">
            {busy ? "Working…" : confirmLabel}
          </button>
        </>
      }
      onClose={onCancel}
      open={open}
      title={title}
    >
      <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
        This action updates billing state through the backend only. No payment secrets are exposed.
      </div>
    </Modal>
  );
}
