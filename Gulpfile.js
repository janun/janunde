/*global require*/

var gulp = require("gulp");
var gutil = require("gulp-util");
var sass = require("gulp-sass");
var autoprefixer = require("gulp-autoprefixer");
var csso = require("gulp-csso");
var concat = require("gulp-concat");
var uglify = require("gulp-uglify");
var sourcemaps = require("gulp-sourcemaps");
var isProd = gutil.env.production;


// styles
gulp.task("styles", function () {
  var includePaths = ["janunde/static/"];
  return gulp.src("core/static_src/core/scss/all.scss")
    .pipe(isProd ? gutil.noop() : sourcemaps.init())
    .pipe(sass({
      includePaths: includePaths
    }).on("error", sass.logError))
    .pipe(autoprefixer({
      cascade: false
    }))
    .pipe(isProd ? csso() : gutil.noop())
    .pipe(isProd ? gutil.noop() : sourcemaps.write())
    .pipe(gulp.dest("./core/static/core/css/"))
    .on("error", gutil.log);
});


// scripts
function scriptsBundle(scripts, bundleName) {
  return gulp.src(scripts)
    .pipe(isProd ? gutil.noop() : sourcemaps.init())
    .pipe(concat(bundleName))
    .pipe(isProd ? uglify() : gutil.noop())
    .pipe(isProd ? gutil.noop() : sourcemaps.write())
    .pipe(gulp.dest("core/static/core/js/"))
    .on("error", gutil.log);
}

gulp.task("jquery.js", function () {
  return scriptsBundle([
    "node_modules/jquery/dist/jquery.js",
  ], "jquery.js");
});

gulp.task("app.js", function () {
  return scriptsBundle([
    "core/static_src/core/js/*.js",
  ], "app.js");
});

gulp.task("form.js", function () {
  return scriptsBundle([
    "node_modules/pickadate/lib/picker.js",
    "node_modules/pickadate/lib/picker.date.js",
    "node_modules/pickadate/lib/picker.time.js",
    "node_modules/pickadate/lib/translations/de_DE.js",
    "core/static_src/core/js/form/*.js",
  ], "form.js");
});

gulp.task("scripts", gulp.parallel("app.js", "jquery.js", "form.js"));

// images
gulp.task("images", function () {
  return gulp.src("core/static_src/core/images/**/*")
    .pipe(gulp.dest("core/static/core/images/"));
});

// build
gulp.task("build", gulp.parallel("styles", "scripts", "images"));

// watch
gulp.task("watch", function () {
  gulp.watch("core/static_src/core/scss/**/*.scss", gulp.series("styles"));
  gulp.watch("core/static_src/core/js/**/*.js", gulp.series("scripts"));
  gulp.watch("core/static_src/core/images/**/*", gulp.series("images"));
});

// default
if (isProd) {
  gulp.task("default", gulp.series("build"));
} else {
  gulp.task("default", gulp.series("watch"));
}
