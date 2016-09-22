(function () {
'use strict';


var gulp = require('gulp');
var gutil = require('gulp-util');
var spawn = require('child_process').spawn;
var compass = require('gulp-compass');
var scsslint = require('gulp-scss-lint');
var jshint = require('gulp-jshint');
var size = require('gulp-size');
var imagemin = require('gulp-imagemin');
// var browserSync = require('browser-sync').create();
var browserSync = require('browser-sync');
var reload      = browserSync.reload;
var o_images = './mycap/static/images/';

var paths = {
    'css': './mycap/static/css/',
    'js': './mycap/static/js/',
    'sass': './sass/',
    'images': './mycap/static/images/'
};


var patterns = {
    'sass': [
        paths.sass + '*.scss',
        paths.sass + '_*.scss',
        paths.sass + '**/*.scss'
    ],
    'js': [
        paths.js + '*.js',
        paths.js + '**/*.js',
        '!' + paths.js + '*.min.js',
        '!' + paths.js + '**/*.min.js'
    ],
    'css': [
        paths.css + '*.css',
        paths.css + '**/*.css',

    ],
    'images': [
        paths.images + '*',
    ],
    'html': ['./**/*.html']
};

gulp.task('browser-sync', function() {
    browserSync({
        proxy: 'localhost:8000',
        port: 8001
    });
});

gulp.task('watch', function() {
    gulp.watch(paths.css+'styles.css').on("change", function(file) {
        browserSync.reload(file.path);
    });
});

gulp.task('compass', function() {
    gulp.src(paths.sass)
        .pipe(compass({
            // style: 'expanded',
            style: 'compressed',
            comments: false,
            sourcemap:true,
            force: true,
            css: paths.css,
            sass: paths.sass,
            // task: 'watch'

        })).pipe(browserSync.reload({stream:true}))
        .on('error', function(error) {
            gutil.log(error);
        });
});

gulp.task('size', function() {
    return gulp.src(patterns.css)
        .pipe(size({
            title: 'CSS SIZE',
            showFiles: true,
            showTotal: false
        }));
});

gulp.task('imagemin', function() {
    gulp.src(patterns.images)
        .pipe(imagemin())
        .pipe(gulp.dest(o_images));
});

gulp.task('scsslint', function() {
    if(gutil.env.exitonerror === 1)
        gulp.src(patterns.sass)
            .pipe(scsslint({
                'config': 'scss-lint.yml',
            }))
            .pipe(scsslint.failReporter());
    else
        gulp.src(patterns.sass)
            .pipe(scsslint({
                'config': 'scss-lint.yml',
            }))
            .on('error', function(error) {
                gutil.log(error);
            });
});

gulp.task('jslint', function() {
    gulp.src(patterns.js)
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

gulp.task('styles', function () {
    gulp.start('scsslint');
    gulp.start('compass');

});

gulp.task('html', function () {
    gulp.src(patterns.html)
    .pipe(browserSync.reload({stream: true}))
    .on('error', function(error) {
            gutil.log(error);
        });
})

gulp.task('build', function() {});

gulp.task('default', [ 'browser-sync', 'compass' ],function () {
    gulp.start('jslint');
    gulp.start('scsslint');
    gulp.start('compass');
    gulp.start('imagemin');
    gulp.start('html');

    gulp.watch(patterns.css, ['size']);
    gulp.watch(patterns.js, ['jslint']);
    gulp.watch(patterns.sass, ['scsslint']);
    gulp.watch(patterns.sass, ['compass']);
    gulp.watch(patterns.css, ['watch']);
    gulp.watch(patterns.images, ['imagemin']);
    gulp.watch(patterns.html, ['html']);

});

// end of gulpfile.js
}());



/*
// Assuming you already have NodeJS, npm and gulp installed
// and followed instructions at:
// https://www.browsersync.io/docs/gulp/
//
// save this file at <<DJANGO PROJECT ROOT>>
// on your terminal:
// $ cd <<DJANGO PROJECT ROOT>>
// $ gulp

// this will open a browser window with your project
// and reload it whenever a file with the extensions scss,css,html,py,js
// is changed

/!*
var gulp        = require('gulp');
var browserSync = require('browser-sync');
var reload      = browserSync.reload;

gulp.task('default', function() {
    browserSync.init({
        notify: false,
        proxy: "localhost:8000"
    });
    gulp.watch(['./!**!/!*.{scss,css,html,py,js}'], reload);
});*!/
*/
