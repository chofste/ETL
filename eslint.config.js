export default [
  {
    ignores: ["node_modules/", "dist/", "build/"], // Ignore these directories
  },
  {
    files: ["**/*.js", "**/*.jsx"], // Lint JS and JSX files
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
    },
    rules: {
      "no-unused-vars": "warn",
      "no-console": "warn",
      "semi": ["error", "always"],
    },
  },
];
