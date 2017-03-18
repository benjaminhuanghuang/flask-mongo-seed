var gulp = require('gulp'),
    gp_clean = require('gulp-clean'),
    gp_concat = require('gulp-concat'),
    gp_sourcemaps = require('gulp-sourcemaps'),
    gp_typescript = require('gulp-typescript'),
    gp_uglify = require('gulp-uglify');

/// Define paths
var srcPaths = {
    ts: ['app_client/**/*.ts'],
    template: ['app_client/**/*.html'],
    js_lib: [
        'app_client/**/*.js',

        'node_modules/core-js/client/shim.min.js',
        'node_modules/zone.js/dist/zone.js',
        'node_modules/reflect-metadata/Reflect.js',
        'node_modules/systemjs/dist/system.src.js',
        'node_modules/typescript/lib/typescript.js'
    ],
    js_angular: [
        'node_modules/@angular/**'
    ],
    js_rxjs: [
        'node_modules/rxjs/**'
    ]
};

var destPaths = {
    js_app: 'app/static/js_app/',
    js_lib: 'app/static/js_lib/',
    js_angular: 'app/static/js_lib/@angular/',
    js_rxjs: 'app/static/js_lib/rxjs/'
};
// Compile, minify and create sourcemaps all TypeScript files and place
// them to app/static/js_app, together with their js.map files.
// Run dependency task 'app_clean' before
gulp.task('ts', ['template'], function () {
    return gulp.src(srcPaths.ts)
        .pipe(gp_sourcemaps.init())
        .pipe(gp_typescript(require('./tsconfig.json').compilerOptions))
        .pipe(gp_uglify({
            mangle: false   // set false to skip mangling names.
        }))
        .pipe(gp_sourcemaps.write('/'))
        .pipe(gulp.dest(destPaths.js_app));
});
// Delete app/static/js_app contents
gulp.task('app_clean', function () {
    return gulp.src(destPaths.js_app + "*", {
            read: false
        })
        .pipe(gp_clean({
            force: true
        }));
});

// Copy all JS files from external libraries to app/static/js_lib
gulp.task('js_lib', function () {
    gulp.src(srcPaths.js_angular)
        .pipe(gulp.dest(destPaths.js_angular));

    gulp.src(srcPaths.js_rxjs)
        .pipe(gulp.dest(destPaths.js_rxjs));

    return gulp.src(srcPaths.js_lib)
        // .pipe(gp_uglify({ mangle: false })) // disable uglify
        // .pipe(gp_concat('all-js.min.js')) // disable concat
        .pipe(gulp.dest(destPaths.js_lib));
});

// Delete app/static/js_lib contents
gulp.task('js_clean', function () {
    return gulp.src(destPaths.js_lib + "*", {
            read: false
        })
        .pipe(gp_clean({
            force: true
        }));
});

// Copy all angular templates to js_app
gulp.task('template', function () {
    gulp.src(srcPaths.template)
        .pipe(gulp.dest(destPaths.js_app));
});

// Watch specified files and define what to do upon file changes
gulp.task('watch', function () {
    gulp.watch([srcPaths.app_client, srcPaths.js_lib] ['app', 'js']);
});

// Global cleanup task
gulp.task('cleanup', ['app_clean', 'js_clean']);

// Define the default task so it will launch all other tasks
gulp.task('default', ['ts', 'js_lib']);