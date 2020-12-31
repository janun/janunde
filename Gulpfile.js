/*global require*/

var gulp = require("gulp");
var gutil = require("gulp-util");
var concat = require("gulp-concat");
var uglify = require("gulp-uglify");
var sourcemaps = require("gulp-sourcemaps");
var isProd = gutil.env.production;

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
  return scriptsBundle([
    "core/static_src/core/js/*.js",
  ], "app.js");
});

// images
gulp.task("images", function () {
  return gulp.src("core/static_src/core/images/**/*")
    .pipe(gulp.dest("core/static/core/images/"));
});

// build
gulp.task("build", gulp.parallel("scripts", "images"));

// watch
gulp.task("watch", function () {
  gulp.watch("core/static_src/core/js/**/*.js", gulp.series("scripts"));
  gulp.watch("core/static_src/core/images/**/*", gulp.series("images"));
});

// default
if (isProd) {
  gulp.task("default", gulp.series("build"));
} else {
  gulp.task("default", gulp.series("watch"));
}
