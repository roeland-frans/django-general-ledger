/**
 * @fileoverview Config for requirejs.
 *
 * Visit http://requirejs.org/ for more details.
 */


var require = {
    waitSeconds: 0,
    paths: {
        'angular': '../vendor/angular/angular.min',
        'angular-bootstrap': '../vendor/angular-bootstrap/ui-bootstrap-tpls.min',
        'angular-cookies': '../vendor/angular-cookies/angular-cookies.min',
        'angular-resource': '../vendor/angular-resource/angular-resource.min',
        'angular-ui-router': '../vendor/angular-ui-router/release/angular-ui-router.min',
        'angular-xeditable': '../vendor/angular-xeditable/dist/js/xeditable.min',
        'bootstrap': '../vendor/bootstrap/dist/js/bootstrap.min',
        'domReady': '../vendor/requirejs-domready/domReady',
        'kendo': '../kendo/kendo.all.min',
        'lodash': '../vendor/lodash/dist/lodash.min',
        'moment': '../vendor/moment/min/moment.min',
        'jquery': '../vendor/jquery/jquery.min'
    },
    shim: {
        'angular': {'exports': 'angular', deps: ['jquery']},
        'angular-resource': { deps: ['angular'] },
        'angular-cookies': { deps: ['angular'] },
        'angular-bootstrap': { deps: ['angular'] },
        'angular-ui-router': { deps: ['angular'] },
        'angular-xeditable': { deps: ['angular'] },
        'bootstrap':{deps: ['jquery']},
        'kendo': { deps: ['angular']}
    },
    priority: [
        'jquery',
        'bootstrap',
        'angular',
        'kendo'
    ]
};