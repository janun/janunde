/*global require*/

var gulp = require("gulp");
var gutil = require("gulp-util");
var sass = require("gulp-sass");
var autoprefixer = require("gulp-autoprefixer");
var csso = require("gulp-csso");
var concat = require("gulp-concat");
var uglify = require("gulp-uglify");
var sourcemaps = require("gulp-sourcemaps");
var svgmin = require("gulp-svgmin");
var fs = require("fs");
var isProd = gutil.env.production;


// styles
gulp.task("styles", function () {
  var includePaths = ["janunde/static/"];
  gulp.src("core/static_src/core/scss/all.scss")
    .pipe(isProd ? gutil.noop() : sourcemaps.init())
    .pipe(sass({
      includePaths: includePaths
    }).on("error", sass.logError))
    .pipe(autoprefixer({
      browsers: ["> 5% in DE",],
      cascade: false
    }))
    .pipe(isProd ? csso() : gutil.noop())
    .pipe(isProd ? gutil.noop() : sourcemaps.write())
    .pipe(gulp.dest("./core/static/core/css/"))
    .on("error", gutil.log);
});


// fonts
gulp.task("fonts", function () {
  gulp.src("core/static_src/core/fonts/**/*")
    .pipe(gulp.dest("core/static/core/fonts/"));
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

gulp.task("scripts", function () {
  scriptsBundle([
    "janunde/static/bower_components/vue/dist/vue.min.js",
  ], "start.js");

  scriptsBundle([
    "janunde/static/bower_components/jquery/dist/jquery.js",
    "janunde/static/bower_components/jQuery.dotdotdot/src/jquery.dotdotdot.js",
    "core/static_src/core/js/*.js",
  ], "app.js");

  scriptsBundle([
    "janunde/static/bower_components/pickadate/lib/picker.js",
    "janunde/static/bower_components/pickadate/lib/picker.date.js",
    "janunde/static/bower_components/pickadate/lib/picker.time.js",
    "janunde/static/bower_components/pickadate/lib/translations/de_DE.js",
    "core/static_src/core/js/form/*.js",
  ], "form.js");
});


// fonts
gulp.task("fonts", function () {
  return gulp.src("core/static_src/core/fonts/**/*")
    .pipe(gulp.dest("core/static/core/fonts/"));
});


// images
gulp.task("images", function () {
  return gulp.src("core/static_src/core/images/**/*")
    .pipe(gulp.dest("core/static/core/images/"));
});


gulp.task("svgmin", function () {
  return gulp.src("core/templates/icons/*.svg")
    .pipe(svgmin({
      floatPrecision: 1,
      plugins: [
        { cleanupNumericValues: { floatPrecision: 1 } }
      ]
    }))
    .pipe(gulp.dest("core/templates/icons/"));
});

// build
gulp.task("build", ["styles", "fonts", "scripts", "images"]);

// watch
gulp.task("watch", ["build"], function () {
  gulp.watch("core/static_src/core/scss/**/*.scss", ["styles"]);
  gulp.watch("core/static_src/core/js/**/*.js", ["scripts",]);
  gulp.watch("core/static_src/core/fonts/**/*", ["fonts"]);
  gulp.watch("core/static_src/core/images/**/*", ["images"]);
});

// default
if (isProd) {
  gulp.task("default", ["build"]);
} else {
  gulp.task("default", ["watch"]);
}
