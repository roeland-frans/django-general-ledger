define([
    'backoffice/module',
    'notification'
], function (module, notification) {

    'use strict';

    module.controller('TransactionCtrl', ['$scope', '$http', '$state', '$stateParams', '$filter', '$q', 'defaultgrid', function ($scope, $http, $state, $stateParams, $filter, $q, defaultgrid) {

        var url = $scope.appVariables.baseUrl + "/rest/transactions/";

        var columns = [
            {
                field: "ref_no",
                title: "Reference Number",
                template: '<a href="" ng-click="showGrid(\'#:ref_no#\');">#=ref_no#</a>',
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "start_date",
                title: "Start Date",
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
                field: "name",
                title: "Name",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "buyer__name",
                title: "Buyer",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "seller__name",
                title: "Seller",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "state",
                title: "State",
                values: [
                    { text: 'BUYER_CREATE', value: 'BUYER_CREATE' },
                    { text: 'SELLER_CREATE', value: 'SELLER_CREATE' },
                    { text: 'AGENT_CREATE', value: 'AGENT_CREATE' },
                    { text: 'PENDING', value: 'PENDING' },
                    { text: 'REJECTED', value: 'REJECTED' },
                    { text: 'LOCKED', value: 'LOCKED' },
                    { text: 'OPEN', value: 'OPEN' },
                    { text: 'PAYMENT_REQ', value: 'PAYMENT_REQ' },
                    { text: 'REFUND_REQ', value: 'REFUND_REQ' },
                    { text: 'AGENT_PROP', value: 'AGENT_PROP' },
                    { text: 'SELLER_PROP', value: 'SELLER_PROP' },
                    { text: 'BUYER_PROP', value: 'BUYER_PROP' },
                    { text: 'SETTLE', value: 'SETTLE' },
                    { text: 'PAY', value: 'PAY' },
                    { text: 'REFUND', value: 'REFUND' },
                    { text: 'CLOSED', value: 'CLOSED' }
                ],
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "value",
                title: "Value",
                template: '<div class="text-right">#=value#</div>',
                filterable: false
            },
            {
                field: "fee",
                title: "Fee",
                template: '<div class="text-right">#=fee#</div>',
                filterable: false
            }
        ];

        $scope.mainGridOptions = defaultgrid.setupGrid(url, columns);

        $scope.selectedTransaction = undefined;
        $scope.selectTransaction = function (id) {
            $scope.selectedTransaction = id;
            $http.get(url + id + '/')
                .success(function(data, status, headers, config) {
                    $scope.transaction = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
        };
        $scope.showGrid = function(id) {
            $state.go($state.current.name, {id: id})
        };
        $scope.goToAccount = function (id) {
            $state.go('app.accounts', {id: id})
        };

        if ($stateParams.id) {
            $scope.selectTransaction($stateParams.id);
        }

    }]);

});