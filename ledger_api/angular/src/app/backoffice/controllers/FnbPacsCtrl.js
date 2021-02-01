define([
    'backoffice/module',
    'notification'
], function (module, notification) {

    'use strict';

    module.controller('FnbPacsCtrl', ['$scope', '$http', '$state', '$stateParams', 'defaultgrid', function ($scope, $http, $state, $stateParams, defaultgrid) {

        var bank_accounts_url = $scope.appVariables.baseUrl + "/rest/fnb_bank_accounts/";
        var pacs_accounts_url = $scope.appVariables.baseUrl + "/rest/fnb_pacs_accounts/";
        var pacs_files_url = $scope.appVariables.baseUrl + "/rest/fnb_pacs_files/";
        var statement_files_url = $scope.appVariables.baseUrl + "/rest/fnb_statement_files/";

        $http.get(bank_accounts_url)
            .success(function(data, status, headers, config) {
                $scope.bank_accounts = data.results;
            })
            .error(function(data, status, headers, config) {
                notification.error(data.message);
            });

        $http.get(pacs_accounts_url)
            .success(function(data, status, headers, config) {
                $scope.pacs_accounts = data.results;
            })
            .error(function(data, status, headers, config) {
                notification.error(data.message);
            });

        var pacs_columns = [
            {
                field: "date_created",
                title: "Date Created",
                type: "date",
                format: $scope.appVariables.kendoColumnDatetimeFormat,
                filterable: {
                    extra: true,
                    cell: {
                        enabled: false
                    }
                }
            },
            {
                field: "user_gen_no",
                title: "User Gen No",
                filterable: false
            },
            {
                field: "hash_no",
                title: "Hash No",
                filterable: false
            },
            {
                field: "load_report_no",
                title: "Load Report No",
                filterable: false
            },
            {
                field: "rejected_no",
                title: "Rejected No",
                filterable: false
            },
            {
                field: "unpaid_no",
                title: "Unpaid No",
                filterable: false
            },
            {
                field: "pacs_account",
                title: "Packs Account",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            }
        ];
        $scope.pacsGridOptions = defaultgrid.setupGrid(pacs_files_url, pacs_columns);

        var statement_columns = [
            {
                field: "date_created",
                title: "Date Created",
                type: "date",
                format: $scope.appVariables.kendoColumnDatetimeFormat,
                filterable: {
                    extra: true,
                    cell: {
                        enabled: false
                    }
                }
            },
            {
                field: "statement_file_no",
                title: "Statement File No",
                filterable: false
            },
            {
                field: "file",
                title: "Statement File",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "pacs_account",
                title: "Packs Account",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            }
        ];
        $scope.statementGridOptions = defaultgrid.setupGrid(statement_files_url, statement_columns);

    }]);

});