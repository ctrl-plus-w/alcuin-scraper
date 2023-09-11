export type ISelectorContent =
  | {
      id: string;
    }
  | {
      class: string;
    }
  | { origin: string };

export interface ISelectors {
  [name: string]: ISelectorContent;
}

const selectors = {
  // ! Put there your selectors for the app.
};

export default selectors;
