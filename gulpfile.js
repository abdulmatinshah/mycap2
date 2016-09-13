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

var o_images = './xplore/static/img/';

var paths = {
    'css': './xplore/static/css/',
    'js': './xplore/static/js/',
    'sass': './sass/',
    'images': './gfx/',
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
        paths.css + 'screen.css'
    ],
    'images': [
        paths.images + '*',
    ]
};


gulp.task('compass', function() {
    gulp.src(patterns.sass)
        .pipe(compass({
            style: 'expanded',
            comments: false,
            sourcemap:true,
            force: true,
            css: paths.css,
            sass: paths.sass
        }))
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

gulp.task('build', function() {});

gulp.task('default', function () {
    gulp.start('jslint');
    gulp.start('scsslint');
    gulp.start('compass');
    gulp.start('imagemin');

    gulp.watch(patterns.css, ['size']);
    gulp.watch(patterns.js, ['jslint']);
    gulp.watch(patterns.sass, ['scsslint']);
    gulp.watch(patterns.sass, ['compass']);
    gulp.watch(patterns.images, ['imagemin']);
});

// end of gulpfile.js
}());

