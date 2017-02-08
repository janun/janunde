/*global require*/

var gulp = require("gulp");
var gutil = require("gulp-util");
var sass = require("gulp-sass");
var autoprefixer = require("gulp-autoprefixer");
var csso = require("gulp-csso");
var concat = require("gulp-concat");
var uglify = require("gulp-uglify");
var sourcemaps = require("gulp-sourcemaps");
var realFavicon = require ("gulp-real-favicon");
var svgmin = require("gulp-svgmin");
var fs = require("fs");
var isProd = gutil.env.production;


// styles
gulp.task("styles", function() {
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
  .pipe( isProd ? csso() : gutil.noop())
  .pipe(isProd ? gutil.noop() : sourcemaps.write())
  .pipe(gulp.dest("./core/static/core/css/"))
  .on("error", gutil.log);
});


// fonts
gulp.task("fonts", function(){
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

gulp.task("scripts", function(){
  scriptsBundle([
    "janunde/static/bower_components/jquery/dist/jquery.js",
    "janunde/static/bower_components/sticky-kit/jquery.sticky-kit.js",
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


// videos
gulp.task("videos", function(){
  return gulp.src("core/static_src/core/videos/**/*")
  .pipe(gulp.dest("core/static/core/videos/"));
});


// fonts
gulp.task("fonts", function(){
  return gulp.src("core/static_src/core/fonts/**/*")
  .pipe(gulp.dest("core/static/core/fonts/"));
});


// images
gulp.task("images", function(){
  return gulp.src("core/static_src/core/images/**/*")
  .pipe(gulp.dest("core/static/core/images/"));
});



// Favicons
// File where the favicon markups are stored
var FAVICON_DATA_FILE = "faviconData.json";

// Generate the icons. This task takes a few seconds to complete.
// You should run it at least once to create the icons. Then,
// you should run it whenever RealFaviconGenerator updates its
// package (see the check-for-favicon-update task below).
gulp.task("generate-favicon", function(done) {
  realFavicon.generateFavicon({
    masterPicture: "core/static_src/core/images/janun_logo_whitebg.svg",
    dest: "core/static_src/core/images/favicons/",
    iconsPath: "/static_src/core/images/favicons/",
    design: {
      ios: {
        pictureAspect: "backgroundAndMargin",
        backgroundColor: "#ffffff",
        margin: "0%"
      },
      desktopBrowser: {},
      windows: {
        pictureAspect: "noChange",
        backgroundColor: "#da532c",
        onConflict: "override"
      },
      androidChrome: {
        pictureAspect: "noChange",
        themeColor: "#ffffff",
        manifest: {
          name: "JANUN e.V.",
          display: "standalone",
          orientation: "notSet",
          onConflict: "override",
          declared: true
        }
      },
      safariPinnedTab: {
        pictureAspect: "silhouette",
        themeColor: "#3a9d00"
      }
    },
    settings: {
      compression: 1,
      scalingAlgorithm: "Mitchell",
      errorOnImageTooSmall: false
    },
    versioning: {
      paramName: "v",
      paramValue: "asdasdaksd"
    },
    markupFile: FAVICON_DATA_FILE
  }, function() {
    done();
  });
});

// Inject the favicon markups in your HTML pages. You should run
// this task whenever you modify a page. You can keep this task
// as is or refactor your existing HTML pipeline.
gulp.task("inject-favicon-markups", function() {
  gulp.src([ "_favicons.html" ])
    .pipe(realFavicon.injectFaviconMarkups(JSON.parse(fs.readFileSync(FAVICON_DATA_FILE)).favicon.html_code))
    .pipe(gulp.dest("janunde/templates/"));
});

// Check for updates on RealFaviconGenerator (think: Apple has just
// released a new Touch icon along with the latest version of iOS).
// Run this task from time to time. Ideally, make it part of your
// continuous integration system.
gulp.task("check-for-favicon-update", function() {
  var currentVersion = JSON.parse(fs.readFileSync(FAVICON_DATA_FILE)).version;
  realFavicon.checkForUpdates(currentVersion, function(err) {
    if (err) {
      throw err;
    }
  });
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
gulp.task("build", ["styles", "fonts", "videos", "scripts", "images"]);

// watch
gulp.task("watch", ["build"], function() {
  gulp.watch("core/static_src/core/scss/**/*.scss", ["styles"]);
  gulp.watch("core/static_src/core/js/**/*.js", ["scripts",]);
  gulp.watch("core/static_src/core/fonts/**/*", ["fonts"]);
  gulp.watch("core/static_src/core/images/**/*", ["images"]);
  gulp.watch("core/static_src/core/videos/**/*", ["videos"]);
});

// default
if (isProd) {
  gulp.task("default", ["build"]);
} else {
  gulp.task("default", ["watch"]);
}
