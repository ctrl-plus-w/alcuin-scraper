export const hasUndefinedValue = <T extends { [key: string]: any | undefined }>(obj: T): boolean => {
  return Object.keys(obj).every((key) => obj[key] !== undefined);
};
