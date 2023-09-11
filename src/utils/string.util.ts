export const fillStartChars = (str: string, expectedLength: number, char: string): string => {
  if (str.length >= expectedLength) return str;
  return str.padStart(expectedLength, char);
};

export const stringifyNumber = (num: number, expectedLength: number = 2): string => {
  return fillStartChars(num.toString(), expectedLength, '0');
};

export const oneSpaceFormat = (str: string): string => {
  return str.replace(/\ +/g, ' ');
};

export const capitalize = (str: string): string => {
  return str[0].toUpperCase() + str.slice(1);
};

export const trim = (str: string): string => str.trim();

export const formatWhitespaces = (str: string) => trim(oneSpaceFormat(str));
