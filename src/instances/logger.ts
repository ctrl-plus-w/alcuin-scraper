import { Logger } from 'tslog';

const logger = new Logger({
  prettyLogTemplate: '{{dateIsoStr}} {{logLevelName}}\t',
});

export default logger;
