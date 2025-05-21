type ENV_VARIABLES = {
  BACKEND_URL: string;
};

const env = import.meta.env;

if (!("BACKEND_URL" in env)) {
  throw new Error("provide BACKEND_URL env variable");
}

export const { BACKEND_URL } = env as unknown as ENV_VARIABLES;
