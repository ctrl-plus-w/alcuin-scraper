import fs from 'fs';
import path from 'path';

import { Page } from 'puppeteer';

import { getDateForFilename } from './date.util';

export const getPathFromDirAndName = (dir: string, name: string, extension: string, addDate = true): string => {
  const fileName = addDate ? `${name}_${getDateForFilename()}.${extension}` : `${name}.${extension}`;

  const dirPath = path.join('.', dir);
  const filePath = path.join(dirPath, fileName);

  if (!fs.existsSync(path.join('.', dir))) fs.mkdirSync(path.join('.', dir), { recursive: true });

  return filePath;
};

export const saveResults = (dir: string, name: string, content: object, addDate = true): void => {
  const path = getPathFromDirAndName(dir, name, 'json', addDate);

  fs.writeFileSync(path, JSON.stringify(content, null, 2));
};

export const savePdf = async (dir: string, name: string, page: Page, addDate = true): Promise<void> => {
  const path = getPathFromDirAndName(dir, name, 'pdf', addDate);

  await page.pdf({ path });
};
