const purgecss = require("@fullhuman/postcss-purgecss")({
  content: ["./*/templates/**/*.html"],
  defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
  whitelist: []
});

module.exports = {
  plugins: [
    require("postcss-import"),
    require("tailwindcss"),
    purgecss,
    require("autoprefixer"),
    require("cssnano")({
      preset: ['default', {
        discardComments: {
          removeAll: true,
        },
      }]
    })
  ]
};
