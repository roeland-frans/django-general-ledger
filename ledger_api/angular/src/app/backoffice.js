/**
 * @fileoverview This defines the main entry point of our admin application.
 *
 * Requirejs loads main and main bootstraps the HTML with the angular app.
 *
 * Visit http://requirejs.org/ for more details.
 */


window.name = "NG_DEFER_BOOTSTRAP!";  // Defer AngularJS bootstrap


define([
    'require',
    'jquery',
    'angular',
    'domReady',

    'bootstrap',

    'backoffice/module',
    'backoffice/controllers/DashboardCtrl',
    'backoffice/controllers/EntitiesCtrl',
    'backoffice/controllers/UsersCtrl',
    'backoffice/controllers/AccountCtrl',
    'backoffice/controllers/JournalEntryCtrl',
    'backoffice/controllers/PaymentBatchesCtrl',
    'backoffice/controllers/PaymentLinesCtrl',
    'backoffice/controllers/StatementsCtrl',
    'backoffice/controllers/StatementLinesCtrl',
    'backoffice/controllers/AutoReconCtrl',
    'backoffice/controllers/ImportStatementCtrl',
    'backoffice/controllers/FnbPacsCtrl',
    'backoffice/controllers/TransactionCtrl'
], function (require, $, ng, domReady) {
    'use strict';

    domReady(function (document) {
        ng.bootstrap(document, ['app.backoffice']);
        ng.resumeBootstrap();
    });
});