define([
    'backoffice/module',
    'notification'
], function (module, notification) {

    'use strict';

    module.controller('StatementsCtrl', ['$scope', '$http', '$state', '$stateParams', 'defaultgrid', function ($scope, $http, $state, $stateParams, defaultgrid) {

        var url = $scope.appVariables.baseUrl + "/rest/bank_statements/";

        var columns = [
            {
                field: "ref_no",
                title: "Reference",
                template: '<a href="" ng-click="showGrid(\'#=ref_no#\');">#=ref_no#</a>',
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
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
                field: "bank_account_acc_no",
                title: "Bank Account",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "bank_account_bank_name",
                title: "Bank",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            }
        ];

        $scope.selectedStatement = undefined;
        $scope.selectStatement = function (id) {
            $scope.selectedStatement = id;
            $http.get(url + id + '/')
                .success(function(data, status, headers, config) {
                    $scope.statement = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
            $http.get(url + id + '/statement_lines/')
                .success(function(data, status, headers, config) {
                    $scope.statementLines = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
        };
        $scope.showGrid = function(id) {
            $state.go($state.current.name, {id: id})
        };
        $scope.mainGridOptions = defaultgrid.setupGrid(url, columns);
        $scope.goToAccount = function (id) {
            $state.go('app.accounts', {id: id})
        };
        $scope.goToStatementLine = function (id) {
            $state.go('app.statement_lines', {id: id})
        };

        if ($stateParams.id) {
            $scope.selectStatement($stateParams.id);
        }

    }]);

});