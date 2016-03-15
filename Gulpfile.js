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
//var rev = require('gulp-rev'); // TODO


var isProd = gutil.env.production;


// styles
gulp.task('styles', function() {
  // bower_components lives here
  includePaths = ['janunde/static/']

  gulp.src('core/static_src/core/scss/all.scss')

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

    .pipe(gulp.dest('./core/static/core/css/'))
    .on('error', gutil.log);
});


// fonts
gulp.task('fonts', function(){
  gulp.src('core/static_src/core/fonts/**/*')
  .pipe(gulp.dest('core/static/core/fonts/'));
});


// scripts
gulp.task('scripts', function(){
  gulp.src([
    'janunde/static/bower_components/imagesloaded/imagesloaded.pkgd.js',
    'janunde/static/bower_components/isotope/dist/isotope.pkgd.js',
    'core/static_src/core/js/**/*'
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
  gulp.src('core/static_src/core/videos/**/*')
  .pipe(gulp.dest('core/static/core/videos/'));
});

// fonts
gulp.task('fonts', function(){
  gulp.src('core/static_src/core/fonts/**/*')
  .pipe(gulp.dest('core/static/core/fonts/'));
});

// images
gulp.task('images', function(){
  gulp.src('core/static_src/core/images/**/*')
  .pipe(gulp.dest('core/static/core/images/'));
});


// build
gulp.task('build', ['styles', 'fonts', 'videos', 'scripts', 'images']);

// watch
gulp.task('watch', function() {
    gulp.watch('core/static_src/core/scss/**/*.scss', ['styles']);
    gulp.watch('core/static_src/core/js/**/*.js', ['scripts']);
    gulp.watch('core/static_src/core/fonts/**/*', ['fonts']);
    gulp.watch('core/static_src/core/images/**/*', ['images']);
    gulp.watch('core/static_src/core/videos/**/*', ['videos']);
});

// default
gulp.task('default', ['build', 'watch']);
