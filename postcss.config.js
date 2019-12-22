const purgecss = require("@fullhuman/postcss-purgecss")({
  content: ["./*/templates/**/*.html", "./core/**/*.js"],
  defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
  whitelist: ['rich-text']
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
