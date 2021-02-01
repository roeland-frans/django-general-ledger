define([
    'backoffice/module',
    'notification'
], function (module, notification) {

    'use strict';

    module.controller('AccountCtrl', ['$scope', '$http', '$state', '$stateParams', '$filter', '$q', 'defaultgrid', function ($scope, $http, $state, $stateParams, $filter, $q, defaultgrid) {

        var url;

        if ($state.current.name == 'app.account_traders') {
            url = $scope.appVariables.baseUrl + "/rest/account_traders/";
        } else if ($state.current.name == 'app.account_general') {
            url = $scope.appVariables.baseUrl + "/rest/account_general/";
        } else if ($state.current.name == 'app.account_bank') {
            url = $scope.appVariables.baseUrl + "/rest/account_bank/";
        } else {
            url = $scope.appVariables.baseUrl + "/rest/account_all/";
        }

        var columns = [
            {
                field: "acc_no",
                title: "Account Number",
                template: '<a href="" ng-click="showGrid(\'#:acc_no#\');">#=acc_no#</a>',
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "name",
                title: "Name",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "accounting_type",
                title: "Accounting Type",
                values: [
                    { text: 'ASSET', value: 'ASSET' },
                    { text: 'LIABILITY', value: 'LIABILITY' },
                    { text: 'INCOME', value: 'INCOME' },
                    { text: 'EXPENSE', value: 'EXPENSE' },
                    { text: 'CAPITAL', value: 'CAPITAL' }
                ],
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "state",
                title: "Account State",
                values: [
                    { text: 'OPEN', value: 'OPEN' },
                    { text: 'CLOSED', value: 'CLOSED' },
                    { text: 'SUSPENDED', value: 'SUSPENDED' },
                    { text: 'LIMITED', value: 'LIMITED' }
                ],
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "debit",
                title: "Total Debit",
                template: '<div class="text-right">#=debit#</div>',
                filterable: false
            },
            {
                field: "credit",
                title: "Total Credit",
                template: '<div class="text-right">#=credit#</div>',
                filterable: false
            },
            {
                field: "pending_balance",
                title: "Pending Balance",
                template: '<div class="text-right">#=pending_balance#</div>',
                filterable: false
            },
            {
                field: "available_balance",
                title: "Available Balance",
                template: '<div class="text-right">#=available_balance#</div>',
                filterable: false
            },
            {
                field: "balance",
                title: "Current Balance",
                template: '<div class="text-right">#=balance#</div>',
                filterable: false
            }
        ];

        var statementColumns = [
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
                field: "ref_no",
                title: "Ref No",
                filterable: false
            },
            {
                field: "name",
                title: "Name",
                filterable: false
            },
            {
                field: "journal_entry",
                title: "Journal Entry",
                template: '<a ui-sref="app.journal_entries({id: \'#=journal_entry#\'})">Journal Entry</a>',
                filterable: false
            },
            {
                field: "debit",
                title: "Debit",
                template: '<div class="text-right">#=debit#</div>',
                filterable: false
            },
            {
                field: "credit",
                title: "Credit",
                template: '<div class="text-right">#=credit#</div>',
                filterable: false
            },
            {
                field: "account_balance",
                title: "Available Balance",
                template: '<div class="text-right">#=account_balance#</div>',
                filterable: false
            }
        ];

        $scope.mainGridOptions = defaultgrid.setupGrid(url, columns);

        var statementUrl = function () {
            return url + $scope.selectedAccount + '/statement/';
        };

        $scope.statementGridOptions = defaultgrid.setupGrid(statementUrl, statementColumns);
        $scope.statementGridOptions.dataSource.pageSize = 25;
        $scope.statementGridOptions.sortable = false;

        $scope.selectedAccount = undefined;
        $scope.selectAccount = function (id) {
            $scope.selectedAccount = id;
            $http.get(url + id + '/')
                .success(function(data, status, headers, config) {
                    $scope.account = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
        };
        $scope.showGrid = function(id) {
            $state.go($state.current.name, {id: id})
        };

        if ($stateParams.id) {
            $scope.selectAccount($stateParams.id);
        }

        $scope.states = [
            {value: "OPEN", text: "OPEN"},
            {value: "CLOSED", text: "CLOSED"},
            {value: "SUSPENDED", text: "SUSPENDED"}
        ];
        $scope.updateState = function(state) {
            var data = {
                state: state
            };
            var d = $q.defer();
            $http.put($scope.appVariables.baseUrl + "/rest/account_all/" + $scope.selectedAccount + '/', data)
                .success(function(data, status, headers, config) {
                    d.resolve(true)
                })
                .error(function(data, status, headers, config){
                    d.resolve('' + data.state);
                });
            return d.promise;
        };

    }]);

});