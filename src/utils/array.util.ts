export const includesFilter = <T>(els: Array<T>) => {
  return (el: any): el is T => {
    return els.includes(el);
  };
};

export const areDefinedNumbers = (arr: any[]): arr is number[] => {
  return arr.every((el) => el && !isNaN(el));
};
