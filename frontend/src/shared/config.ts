type ENV_VARIABLES = {
  SL__BACKEND_URL: string;
};

const env = import.meta.env;

if (!("SL__BACKEND_URL" in env)) {
  throw new Error("provide SL__BACKEND_URL env variable");
}

export const { SL__BACKEND_URL } = env as unknown as ENV_VARIABLES;
