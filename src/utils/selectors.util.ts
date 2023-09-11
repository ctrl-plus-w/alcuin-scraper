import { ElementHandle, Page } from 'puppeteer';

import { ISelectorContent } from '../constants/selectors';

export const getSelector = (selector: ISelectorContent): string => {
  if ('origin' in selector) return selector.origin;

  return 'id' in selector ? `#${selector.id}` : `.${selector.class}`;
};

export interface IOption {
  _element: HTMLOptionElement;

  id: string;
  name: string;
}

export const retrieveSelectOptions = async (
  input: ElementHandle<Element>,
  idMapper?: (id: string) => string,
  nameMapper?: (name: string) => string
): Promise<IOption[]> => {
  const optionsElements = await input.$$('option');

  const options = await Promise.all(
    optionsElements.map((optionElement) =>
      optionElement.evaluate((el) => ({
        _element: el,

        id: el.value,
        name: el.innerText,
      }))
    )
  );

  if (!idMapper && !nameMapper) return options;

  return options.map((option) => ({
    _element: option._element,

    id: idMapper ? idMapper(option.id) : option.id,
    name: nameMapper ? nameMapper(option.name) : option.name,
  }));
};

export interface ISelectorsProp {
  [key: string]: ISelectorContent;
}

export const getElementsBySelector = async <T extends ISelectorsProp>(page: Page, selectors: T): Promise<{ [key in keyof T]: ElementHandle }> => {
  const elements = await Promise.all(
    Object.keys(selectors).map(async (key) => {
      const selector = getSelector(selectors[key]);

      const element = await page.waitForSelector(selector, { timeout: 10_000 });
      if (!element) throw new Error(`Element with selector ${selector} not found.`);

      return [key, element];
    })
  );

  return Object.fromEntries(elements);
};
