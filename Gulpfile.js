// This "compiles" our static assets from
// static_src to static
// currently only for the 'core' app
//
// TODO: 'watch' should also watch fonts, images etc.
// TODO: reduce images here instead of manually
// TODO: reduce videos...
// TODO: minify css
// TODO: combine js and minify

var gulp = require('gulp');
var gutil = require('gulp-util');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');


// styles
gulp.task('styles', function() {
  includePaths = ['janunde/static/'] // bower_components lives here

  gulp.src('core/static_src/core/scss/all.scss')
    .pipe(sass({
      includePaths: includePaths
    }).on('error', sass.logError))
    .pipe(autoprefixer({
      browsers: ['last 3 versions', 'not ie <= 8'],
      cascade: false
    }))
    .pipe(gulp.dest('./core/static/core/css/'))
    .on('error', gutil.log);

});


// fonts
gulp.task('fonts', function(){
  gulp.src('core/static_src/core/fonts/**/*')
  .pipe(gulp.dest('core/static/core/fonts/'));
});

// js
gulp.task('js', function(){
  gulp.src('core/static_src/core/js/**/*')
  .pipe(gulp.dest('core/static/core/js/'));
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
gulp.task('build', ['styles', 'fonts', 'videos', 'js', 'images']);

// watch
gulp.task('watch', function() {
    gulp.watch('core/static_src/core/scss/**/*.scss', ['styles']);
    // TODO...
});

// default
gulp.task('default', ['build', 'watch']);
