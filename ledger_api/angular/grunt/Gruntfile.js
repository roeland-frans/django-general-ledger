/**
 * @fileoverview This file configures grunt.
 */


var requirejsCompileSkip = {
    "angular": "empty:",
    "angular-bootstrap": "empty:",
    "angular-cookies": "empty:",
    "angular-resource": "empty:",
    "angular-ui-router": "empty:",
    "angular-xeditable": "empty:",
    "bootstrap": "empty:",
    "domReady": "empty:",
    "jquery": "empty:",
    "kendo": "empty:",
    "lodash": "empty:",
    "moment": "empty:",
    "require": "empty:"
};

module.exports = function (grunt) {

    // Project configuration.
    grunt.initConfig({

        /**
         * @task html2js
         * @desc Convert all *.tpl.html files to js and pack them
         * into the templates module (`templates.js). The templates
         * module then loads all templates into the $templateCache
         * so that the templates are readily available once the app
         * has been loaded client side.
         */
        html2js: {
            options: {
                base: '../src/app/',
                module: 'templates',
                singleModule: true,
                rename: function (moduleName) {
                    return 'templates/' + moduleName;
                }
            },
            main: {
                src: ['../src/**/*.tpl.html'],
                dest: '../src/app/templates.js'
            }
        },

        /**
         * @task wrapDefine
         * @desc Wraps the templates module with a requirejs define.
         */
        wrapDefine: {
            options: {dependencies: [
                {name: 'angular', extern: 'angular'}
            ]},
            files: {
                src: ['../src/app/templates.js'],
                dest: '../src/app/templates.js'
            }
        },

        /**
         * @task requirejs
         * @desc Compile all js code into a single file `main.js`
         * and copy it to `../../public/angular_app/js/main.js`.
         */
        requirejs: {
            compile: {
                options: {
                    findNestedDependencies: true,
                    baseUrl: '../src/app/',
                    paths: requirejsCompileSkip,
                    mainConfigFile: '../src/app/rconfig.js',
                    name: 'backoffice',
                    optimize: 'uglify',  // set to uglify to optimize js. set to none to turn off.
                    out: '../../static/backoffice/js/backoffice.js',
                    done: function (done, output) {
                        console.log('done requirejs');
                        done();
                    }
                }
            }
        },

        /**
         * @task copy
         * @desc config: Copy rconfig to `../../public/angular_app/js/rconfig.js`
         *       vendor: Copy vendor dir to `../../public/angular_app/vendor`
         */
        copy: {
            config: {
                src: ['../src/app/rconfig.js'],
                dest: '../../static/backoffice/js/rconfig.js'
            },
            vendor: {
                expand: true,
                cwd: '../src/',
                src: ['vendor/**'],
                dest: '../../static/backoffice/'
            },
            kendo: {
                expand: true,
                cwd: '../src/',
                src: ['kendo/**'],
                dest: '../../static/backoffice/'
            }
        }

    });


    // Load Npm tasks.
    grunt.loadNpmTasks('grunt-html2js');
    grunt.loadNpmTasks('grunt-wrap-define');
    grunt.loadNpmTasks('grunt-contrib-requirejs');
    grunt.loadNpmTasks('grunt-contrib-copy');


    // Register default task.
    grunt.registerTask('default', [
        'html2js',
        'wrapDefine',
        'requirejs',
        'copy:config'
    ]);

    // Register vendor task.
    grunt.registerTask('vendor', [
        'copy:vendor',
        'copy:kendo'
    ])

};