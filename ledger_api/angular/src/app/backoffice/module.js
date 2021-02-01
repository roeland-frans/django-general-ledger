define([
    'angular',
    'angular-ui-router',
    'angular-bootstrap',
    'angular-cookies',
    'angular-xeditable',
    'kendo',

    'common/services/defaultgrid',
    'templates'
], function (ng) {

    'use strict';

    var module = ng.module('app.backoffice', [
        'ui.router',
        'ui.bootstrap',
        'ngCookies',
        'xeditable',
        'kendo.directives',

        'app.common',
        'templates'
    ]);

    module.config(['$stateProvider', '$urlRouterProvider', '$provide', '$httpProvider', function ($stateProvider, $urlRouterProvider, $provide, $httpProvider) {

        $provide.factory('ErrorHttpInterceptor', ['$q', function ($q) {
            return {
                // On request failure
                requestError: function (rejection) {
                    if (rejection.status == '403') {
                        window.location = 'login';
                    }
                    return $q.reject(rejection);
                },

                // On response failure
                responseError: function (rejection) {
                    if (rejection.status == '403') {
                        window.location = 'login';
                    }
                    return $q.reject(rejection);
                }
            };
        }]);


        $httpProvider.interceptors.push('ErrorHttpInterceptor');

        $stateProvider
            // Abstract state for all app states.
            .state('app', {
                abstract: true,
                views: {
                    root: {
                        templateUrl: 'templates/backoffice/views/base.tpl.html'
                    }
                }
            })

            // State for dashboard.
            .state('app.dashboard', {
                url: '/dashboard',
                views: {
                    'content@app': {
                        controller: 'DashboardCtrl',
                        templateUrl: 'templates/backoffice/views/dashboard.tpl.html'
                    }
                }
            })

            // State for users.
            .state('app.users', {
                url: '/users/:id',
                views: {
                    'content@app': {
                        controller: 'UsersCtrl',
                        templateUrl: 'templates/backoffice/views/users.tpl.html'
                    }
                }
            })

            // State for entities.
            .state('app.entities', {
                url: '/entities/:id',
                views: {
                    'content@app': {
                        controller: 'EntitiesCtrl',
                        templateUrl: 'templates/backoffice/views/entities.tpl.html'
                    }
                }
            })

            // State for transactions.
            .state('app.transactions', {
                url: '/transactions/:id',
                views: {
                    'content@app': {
                        controller: 'TransactionCtrl',
                        templateUrl: 'templates/backoffice/views/transactions.tpl.html'
                    }
                }
            })

            // State for accounts.
            .state('app.accounts', {
                url: '/accounts/:id',
                views: {
                    'content@app': {
                        controller: 'AccountCtrl',
                        templateUrl: 'templates/backoffice/views/accounts.tpl.html'
                    }
                }
            })

            // State for traders accounts.
            .state('app.account_traders', {
                url: '/account_traders/:id',
                views: {
                    'content@app': {
                        controller: 'AccountCtrl',
                        templateUrl: 'templates/backoffice/views/accounts.tpl.html'
                    }
                }
            })

            // State for general accounts.
            .state('app.account_general', {
                url: '/account_general/:id',
                views: {
                    'content@app': {
                        controller: 'AccountCtrl',
                        templateUrl: 'templates/backoffice/views/accounts.tpl.html'
                    }
                }
            })

            // State for bank accounts.
            .state('app.account_bank', {
                url: '/account_bank/:id',
                views: {
                    'content@app': {
                        controller: 'AccountCtrl',
                        templateUrl: 'templates/backoffice/views/accounts.tpl.html'
                    }
                }
            })

            // State for journal entries.
            .state('app.journal_entries', {
                url: '/journal_entries/:id',
                views: {
                    'content@app': {
                        controller: 'JournalEntryCtrl',
                        templateUrl: 'templates/backoffice/views/journal_entries.tpl.html'
                    }
                }
            })

             // State for payment batches.
            .state('app.payment_batches', {
                url: '/payment_batches/:id',
                views: {
                    'content@app': {
                        controller: 'PaymentBatchesCtrl',
                        templateUrl: 'templates/backoffice/views/payment_batches.tpl.html'
                    }
                }
            })

            // State for payment lines.
            .state('app.payment_lines', {
                url: '/payment_lines/:id',
                views: {
                    'content@app': {
                        controller: 'PaymentLinesCtrl',
                        templateUrl: 'templates/backoffice/views/payment_lines.tpl.html'
                    }
                }
            })

            // State for statements.
            .state('app.statements', {
                url: '/statements/:id',
                views: {
                    'content@app': {
                        controller: 'StatementsCtrl',
                        templateUrl: 'templates/backoffice/views/statements.tpl.html'
                    }
                }
            })

            // State for statement lines.
            .state('app.statement_lines', {
                url: '/statement_lines/:id',
                views: {
                    'content@app': {
                        controller: 'StatementLinesCtrl',
                        templateUrl: 'templates/backoffice/views/statement_lines.tpl.html'
                    }
                }
            })

            // State for statement lines auto recon.
            .state('app.auto_recon', {
                url: '/auto_recon/',
                views: {
                    'content@app': {
                        controller: 'AutoReconCtrl',
                        templateUrl: 'templates/backoffice/views/auto_recon.tpl.html'
                    }
                }
            })

            // State for statement lines import statement.
            .state('app.import_statement', {
                url: '/import_statement/',
                views: {
                    'content@app': {
                        controller: 'ImportStatementCtrl',
                        templateUrl: 'templates/backoffice/views/import_statement.tpl.html'
                    }
                }
            })

            // State for FNB Pacs.
            .state('app.fnb_pacs', {
                url: '/fnb_pacs',
                views: {
                    'content@app': {
                        controller: 'FnbPacsCtrl',
                        templateUrl: 'templates/backoffice/views/fnb_pacs.tpl.html'
                    }
                }
            });

        $urlRouterProvider.otherwise('/dashboard');

    }]);

    module.run(['$rootScope', '$state', '$stateParams', '$http', '$cookies', 'editableOptions', function ($rootScope, $state, $stateParams, $http, $cookies, editableOptions) {
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
        $rootScope.appVariables = angular.fromJson(appVariables);
        $rootScope.appVariables.ngDatetimeFormat = 'MMMM d, yyyy, h:mm a';
        $rootScope.appVariables.ngDateFormat = 'MMMM d, yyyy';
        $rootScope.appVariables.kendoColumnDatetimeFormat = '{0:MMM d, yyyy, h:mm tt}';

        editableOptions.theme = 'bs3'; // Can be 'bs3', 'bs2', 'default'

        // Assign CSRF token to headers.
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
        $http.defaults.headers.patch['X-CSRFToken'] = $cookies.csrftoken;
    }]);

    return module;

});