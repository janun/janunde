// This "compiles" our static assets from
// static_src to static
// currently only for the 'core' app
//
// TODO: reduce images here instead of manually
// TODO: reduce videos...

var gulp = require('gulp');
var gutil = require('gulp-util');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var csso = require('gulp-csso');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var modernizr = require('gulp-modernizr');
//var rev = require('gulp-rev'); // TODO


var isProd = gutil.env.production;


// styles
gulp.task('styles', function() {
  // bower_components lives here
  includePaths = ['janunde/static/']

  gulp.src('core/static_src/core/scss/all.scss')

  // init sourcemap
  .pipe(isProd ? gutil.noop() : sourcemaps.init())

  // compile sass
  .pipe(sass({
    includePaths: includePaths
  }).on('error', sass.logError))

  // use autoprefixer
  .pipe(autoprefixer({
    browsers: ['> 5% in DE',],
    cascade: false
  }))

  // minify in production
  .pipe( isProd ? csso() : gutil.noop())

  // write sourcemap
  .pipe(isProd ? gutil.noop() : sourcemaps.write())

  .pipe(gulp.dest('./core/static/core/css/'))
  .on('error', gutil.log);
});


// fonts
gulp.task('fonts', function(){
  gulp.src('core/static_src/core/fonts/**/*')
  .pipe(gulp.dest('core/static/core/fonts/'));
});


// modernizr
gulp.task('modernizr', function() {
  return gulp.src('core/static_src/core/js/**/*.js')
    .pipe(modernizr({
      "options" : [
        "setClasses",
        "addTest",
        "html5printshiv",
        "testProp",
        "fnBind"
      ],
      tests: ['']
    }))
    .pipe(gulp.dest('core/static/core/js/'));
});


// scripts
gulp.task('scripts', ['modernizr'], function(){
  return gulp.src([
    'core/static/core/js/modernizr.js',
    'janunde/static/bower_components/jquery/dist/jquery.js',
    'janunde/static/bower_components/sticky-kit/jquery.sticky-kit.js',
    'core/static_src/core/js/**/*.js',
    'janunde/static/bower_components/a11y-toggle/a11y-toggle.js',
  ])

  // init sourcemap
  .pipe(isProd ? gutil.noop() : sourcemaps.init())

  // concat
  .pipe(concat('app.js'))

  // minify
  .pipe(isProd ? uglify() : gutil.noop())

  // write sourcemap
  .pipe(isProd ? gutil.noop() : sourcemaps.write())

  // write output
  .pipe(gulp.dest('core/static/core/js/'))
  .on('error', gutil.log);
});


// videos
gulp.task('videos', function(){
  return gulp.src('core/static_src/core/videos/**/*')
  .pipe(gulp.dest('core/static/core/videos/'));
});

// fonts
gulp.task('fonts', function(){
  return gulp.src('core/static_src/core/fonts/**/*')
  .pipe(gulp.dest('core/static/core/fonts/'));
});

// images
gulp.task('images', function(){
  return gulp.src('core/static_src/core/images/**/*')
  .pipe(gulp.dest('core/static/core/images/'));
});


// build
gulp.task('build', ['styles', 'fonts', 'videos', 'scripts', 'images']);

// watch
gulp.task('watch', ['build'], function() {
    gulp.watch('core/static_src/core/scss/**/*.scss', ['styles']);
    gulp.watch('core/static_src/core/js/**/*.js', ['scripts',]);
    gulp.watch('core/static_src/core/fonts/**/*', ['fonts']);
    gulp.watch('core/static_src/core/images/**/*', ['images']);
    gulp.watch('core/static_src/core/videos/**/*', ['videos']);
});

// default
if (isProd) {
  gulp.task('default', ['build']);
} else {
  gulp.task('default', ['watch']);
}
