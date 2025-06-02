import { FormInstance } from "antd";
import { useCallback } from "react";

export type ApiFormErrorResponse<T extends object = object> = Partial<
  Record<keyof T, string | string[]>
>;

export function useApiErrorHandler() {
  const setFormWithServerErrors = useCallback(
    (form: FormInstance, errorValues: ApiFormErrorResponse) => {
      const errorFieldValues = Object.entries(errorValues).map(
        ([key, value]) => ({
          name: key,
          errors: Array.isArray(value) ? value : [value],
        })
      );

      form.setFields(errorFieldValues);
    },
    []
  );

  const handleApiFormError = (form: FormInstance, error: Error) => {
    if ("data" in error && error.data !== undefined) {
      const errorFields = error.data as ApiFormErrorResponse;
      setFormWithServerErrors(form, errorFields);
    }
  };

  return { handleApiFormError };
}
