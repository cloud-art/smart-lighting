export const pathKeys = {
  root: "/",
  devices: () => pathKeys.root.concat("devices/"),
  statistics: () => pathKeys.root.concat("statistics/"),
};
