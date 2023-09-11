export const sleep = async (duration: number) => new Promise((r) => setTimeout(r, duration));

export const same = <T>(el: T): T => el;
