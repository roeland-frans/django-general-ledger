define([
    'backoffice/module',
    'notification'
], function (module, notification) {

    'use strict';

    module.controller('StatementLinesCtrl', ['$scope', '$http', '$state', '$stateParams', '$q', 'defaultgrid', function ($scope, $http, $state, $stateParams, $q, defaultgrid) {

        var url = $scope.appVariables.baseUrl + "/rest/bank_statement_lines/";
        var accountTradersUrl = $scope.appVariables.baseUrl + "/rest/account_traders/";
        var accountGeneralUrl = $scope.appVariables.baseUrl + "/rest/account_general/";

        $scope.recon = {};

        var columns = [
            {
                field: "uuid",
                title: "Internal Ref",
                template: '<a href="" ng-click="showGrid(\'#=uuid#\');">#=uuid#</a>',
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "ref_no",
                title: "Reference",
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
            },
            {
                field: "line_type",
                title: "Line Type",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "amount",
                title: "Amount",
                template: '<div class="text-right">#=amount#</div>',
                filterable: false
            },
            {
                field: "state",
                title: "State",
                values: [
                    { text: 'Posted', value: 'POSTED' },
                    { text: 'Un-posted', value: 'UNPOSTED' },
                    { text: 'Failed', value: 'FAILED' },
                    { text: 'Reconciled', value: 'RECONCILE' },
                    { text: 'Error', value: 'ERROR' },
                    { text: 'Re-loaded', value: 'RELOADED' }
                ],
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            }
        ];

        /*
         * Setup account drop down options.
         */
        $scope.accountDropDownDataSource = new kendo.data.DataSource(defaultgrid.defaultDataSource(accountGeneralUrl));
        $scope.accountDropDownOptions = {
            filter: "contains",
            template:"(#=acc_no#) #=name#",
            valueTemplate:"(#=acc_no#) #=name#",
            optionLabel: "---",
            dataTextField: "acc_no",
            dataValueField: "id",
            delay: 0,
            dataSource: $scope.accountDropDownDataSource
        };

        /*
         * Setup accountType drop down options.
         */
        $scope.accountTypes = [
            {name: 'General Account', url: accountGeneralUrl},
            {name: 'Traders Account', url: accountTradersUrl}
        ];
        $scope.accountTypeDropDownOnSelect = function (e) {
            var item = this.dataItem(e.item.index());
            $scope.accountDropDownDataSource.transport.options.read.url = item.url;
            $scope.recon.account = undefined;
            $scope.accountDropDownDataSource.read();
        };
        $scope.accountTypeDropDownOptions = {
            dataTextField: "name",
            dataValueField: "url",
            delay: 0,
            select: $scope.accountTypeDropDownOnSelect,
            dataSource: $scope.accountTypes
        };

        $scope.selectedLine = undefined;
        $scope.selectLine = function (id) {
            $scope.selectedLine = id;
            $http.get(url + id + '/')
                .success(function(data, status, headers, config) {
                    $scope.line = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
            $http.get(url + id + '/journal_entry_lines/')
                .success(function(data, status, headers, config) {
                    $scope.journalEntryLines = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
        };
        $scope.allowManualRecon = function () {
            if ($scope.line) {
                return $scope.line.state == "FAILED";
            } else {
                return false;
            }
        };
        $scope.goToAutoRecon = function () {
            $state.go('app.auto_recon')
        };
        $scope.doManualRecon = function () {
            var data = {
                acc_no: '' + $scope.recon.account.acc_no,
                description: '' + $scope.recon.description
            };
            var d = $q.defer();
            $http.post(url + $scope.selectedLine + '/manual_recon/', data)
                .success(function(data, status, headers, config) {
                    $state.reload();
                    d.resolve(true);
                })
                .error(function(data, status, headers, config){
                    d.resolve('' + data.state);
                });
            return d.promise;
        };
        $scope.showGrid = function(id) {
            $state.go($state.current.name, {id: id})
        };
        $scope.mainGridOptions = defaultgrid.setupGrid(url, columns);
        $scope.goToAccount = function (id) {
            $state.go('app.accounts', {id: id})
        };
        $scope.goToStatement = function (id) {
            $state.go('app.statements', {id: id})
        };

        if ($stateParams.id) {
            $scope.selectLine($stateParams.id);
        }

    }]);

});