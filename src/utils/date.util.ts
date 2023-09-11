import { stringifyNumber } from './string.util';

export const getDateForFilename = (): string => {
  const now = new Date();
  return [now.getDate(), now.getMonth(), now.getFullYear(), now.getHours(), now.getMinutes(), now.getSeconds()]
    .map((el) => stringifyNumber(el, 2))
    .join('_');
};
