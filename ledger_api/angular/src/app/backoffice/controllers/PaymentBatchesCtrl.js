define([
    'backoffice/module',
    'notification'
], function (module, notification) {

    'use strict';

    module.controller('PaymentBatchesCtrl', ['$scope', '$http', '$state', '$stateParams', 'defaultgrid', function ($scope, $http, $state, $stateParams, defaultgrid) {

        var url = $scope.appVariables.baseUrl + "/rest/bank_payment_batches/";

        var columns = [
            {
                field: "ref_no",
                title: "Reference",
                template: '<a href="" ng-click="showGrid(\'#=ref_no#\');">#=ref_no#</a>',
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "date_submitted",
                title: "Date Submitted",
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
                field: "bank_account__acc_no",
                title: "Bank Account",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "bank_account__bank__name",
                title: "Bank",
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
            },
            {
                field: "total_amount",
                title: "Total Amount",
                template: '<div class="text-right">#=total_amount#</div>',
                filterable: false
            }
        ];

        $scope.selectedBatch = undefined;
        $scope.selectBatch = function (id) {
            $scope.selectedBatch = id;
            $http.get(url + id + '/')
                .success(function(data, status, headers, config) {
                    $scope.batch = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
            $http.get(url + id + "/payment_lines/")
                .success(function(data, status, headers, config) {
                    $scope.paymentLines = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
            $http.get(url + id + "/entry_lines/")
                .success(function(data, status, headers, config) {
                    $scope.entryLines = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
        };
        $scope.goToPaymentLine = function(id) {
            $state.go('app.payment_lines', {id: id})
        };
        $scope.goToAccount = function(id) {
            $state.go('app.accounts', {id: id})
        };
        $scope.showGrid = function(id) {
            $state.go($state.current.name, {id: id})
        };
        $scope.mainGridOptions = defaultgrid.setupGrid(url, columns);

        if ($stateParams.id) {
            $scope.selectBatch($stateParams.id);
        }

    }]);

});