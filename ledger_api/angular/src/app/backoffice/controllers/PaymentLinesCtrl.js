define([
    'backoffice/module',
    'notification'
], function (module, notification) {

    'use strict';

    module.controller('PaymentLinesCtrl', ['$scope', '$http', '$state', '$stateParams', '$q', 'defaultgrid', function ($scope, $http, $state, $stateParams, $q, defaultgrid) {

        var url = $scope.appVariables.baseUrl + "/rest/bank_payment_lines/";

        var columns = [
            {
                field: "bank_ref",
                title: "Bank Reference",
                template: '<a href="" ng-click="showGrid(\'#=ref_no#\');">#=bank_ref#</a>',
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
                field: "bank_line_type",
                title: "Bank Line Type",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "debit_account_name",
                title: "Debit Account",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "amount",
                title: "Amount",
                template: '<div class="text-right">#=amount#</div>',
                filterable: false
            },
            {
                field: "dest_bank_acc_name",
                title: "Destination Account",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
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
        };
        $scope.isReloadable = function () {
            if ($scope.line) {
                return ($scope.line.state == 'ERROR' || $scope.line.state == 'FAILED');
            } else {
                return false;
            }
        };
        $scope.isActionDateUpdateable = function () {
            if ($scope.line) {
                return $scope.line.state == 'UNPOSTED';
            }
        };
        $scope.showGrid = function(id) {
            $state.go($state.current.name, {id: id})
        };
        $scope.mainGridOptions = defaultgrid.setupGrid(url, columns);
        $scope.goToPaymentBatch = function (id) {
            $state.go('app.payment_batches', {id: id})
        };
        $scope.goToJournalEntry = function (id) {
            $state.go('app.journal_entries', {id: id})
        };
        $scope.goToAccount = function (id) {
            $state.go('app.accounts', {id: id})
        };
        $scope.goToEntity = function (id) {
            $state.go('app.entities', {id: id})
        };

        $scope.datepickerVisible = false;
        $scope.makeDatepickerVisible = function (visible) {
            $scope.datepickerVisible = visible;
        };
        $scope.updateActionDate = function () {
            $scope.datepickerVisible = false;
            var data = {
                action_date: '' + $scope.line.action_date
            };
            var d = $q.defer();
            $http.patch(url + $scope.selectedLine + '/', data)
                .success(function(data, status, headers, config) {
                    d.resolve(true)
                })
                .error(function(data, status, headers, config){
                    d.resolve('' + data.state);
                });
            return d.promise;
        };
        $scope.reloadPayment = function () {
            var data = {
                action_date: '' + $scope.line.action_date
            };
            var d = $q.defer();
            $http.post(url + $scope.selectedLine + '/reload_payment/', data)
                .success(function(data, status, headers, config) {
                    $state.reload();
                    d.resolve(true);
                })
                .error(function(data, status, headers, config){
                    d.resolve('' + data.state);
                });
            return d.promise;
        };

        if ($stateParams.id) {
            $scope.selectLine($stateParams.id);
        }

    }]);

});