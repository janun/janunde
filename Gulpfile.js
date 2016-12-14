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
var realFavicon = require ('gulp-real-favicon');
var fs = require('fs');


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
    'janunde/static/bower_components/jQuery.dotdotdot/src/jquery.dotdotdot.js',
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



// Favicons
// File where the favicon markups are stored
var FAVICON_DATA_FILE = 'faviconData.json';

// Generate the icons. This task takes a few seconds to complete.
// You should run it at least once to create the icons. Then,
// you should run it whenever RealFaviconGenerator updates its
// package (see the check-for-favicon-update task below).
gulp.task('generate-favicon', function(done) {
	realFavicon.generateFavicon({
		masterPicture: 'core/static_src/core/images/janun_logo_whitebg.svg',
		dest: 'core/static_src/core/images/favicons/',
		iconsPath: '/static_src/core/images/favicons/',
		design: {
			ios: {
				pictureAspect: 'backgroundAndMargin',
				backgroundColor: '#ffffff',
				margin: '0%'
			},
			desktopBrowser: {},
			windows: {
				pictureAspect: 'noChange',
				backgroundColor: '#da532c',
				onConflict: 'override'
			},
			androidChrome: {
				pictureAspect: 'noChange',
				themeColor: '#ffffff',
				manifest: {
					name: 'JANUN e.V.',
					display: 'standalone',
					orientation: 'notSet',
					onConflict: 'override',
					declared: true
				}
			},
			safariPinnedTab: {
				pictureAspect: 'silhouette',
				themeColor: '#3a9d00'
			}
		},
		settings: {
      compression: 1,
			scalingAlgorithm: 'Mitchell',
			errorOnImageTooSmall: false
		},
    versioning: {
      paramName: 'v',
      paramValue: 'asdasdaksd'
    },
		markupFile: FAVICON_DATA_FILE
	}, function() {
		done();
	});
});

// Inject the favicon markups in your HTML pages. You should run
// this task whenever you modify a page. You can keep this task
// as is or refactor your existing HTML pipeline.
gulp.task('inject-favicon-markups', function() {
	gulp.src([ '_favicons.html' ])
		.pipe(realFavicon.injectFaviconMarkups(JSON.parse(fs.readFileSync(FAVICON_DATA_FILE)).favicon.html_code))
		.pipe(gulp.dest('janunde/templates/'));
});

// Check for updates on RealFaviconGenerator (think: Apple has just
// released a new Touch icon along with the latest version of iOS).
// Run this task from time to time. Ideally, make it part of your
// continuous integration system.
gulp.task('check-for-favicon-update', function(done) {
	var currentVersion = JSON.parse(fs.readFileSync(FAVICON_DATA_FILE)).version;
	realFavicon.checkForUpdates(currentVersion, function(err) {
		if (err) {
			throw err;
		}
	});
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
