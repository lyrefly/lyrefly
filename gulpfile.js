var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var imagemin = require('gulp-imagemin');
var sourcemaps = require('gulp-sourcemaps');
var del = require('del');
var sass = require('gulp-sass');

var paths = {
  scripts: 'src/js/**/*.js',
  images: 'src/img/**/*',
  sass: 'src/css/**/*.scss'
};

var dests = {
  scripts: 'static/js/',
  images: 'static/img/',
  sass: 'static/css/'
};

gulp.task('clean', function() {
  return del(['build']);
});

gulp.task('sass', function () {
  gulp.src(paths.sass)
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(concat('styles.min.css'))
    .pipe(gulp.dest(dests.sass));
});

gulp.task('scripts', ['clean'], function() {
  // Minify and copy all JavaScript (except vendor scripts)
  // with sourcemaps all the way down
  return gulp.src(paths.scripts)
    .pipe(sourcemaps.init())
      .pipe(uglify())
      .pipe(concat('all.min.js'))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(dests.scripts));
});

// Copy all static images
gulp.task('images', ['clean'], function() {
  return gulp.src(paths.images)
    // Pass in options to the task
    .pipe(imagemin({optimizationLevel: 5}))
    .pipe(gulp.dest(dests.images));
});

// Rerun the task when a file changes
gulp.task('watch', function() {
  gulp.watch(paths.scripts, ['scripts']);
  gulp.watch(paths.images, ['images']);
  gulp.watch(paths.sass, ['sass']);
});

// The default task (called when you run `gulp` from cli)
gulp.task('default', ['watch', 'scripts', 'images', 'sass']);
