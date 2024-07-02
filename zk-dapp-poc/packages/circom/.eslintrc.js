const baseConfig = require('../../.eslintrc.base.js');

module.exports = {
  ...baseConfig,
  parserOptions: {
    project: ['./tsconfig.json'],
    tsconfigRootDir: __dirname,
    sourceType: 'module',
  },
};
