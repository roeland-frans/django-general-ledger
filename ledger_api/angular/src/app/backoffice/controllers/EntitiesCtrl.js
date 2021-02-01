define([
    'backoffice/module',
    'notification'
], function (module, notification) {

    'use strict';

    module.controller('EntitiesCtrl', ['$scope', '$http', '$state', '$stateParams', 'defaultgrid', function ($scope, $http, $state, $stateParams, defaultgrid) {

        var url = $scope.appVariables.baseUrl + "/rest/entities/";

        var columns = [
            {
                field: "name",
                title: "Name",
                template: '<a href="" ng-click="showGrid(#=id#);">#=name#</a>',
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "entity_no",
                title: "Entity Number",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "email",
                title: "Email Address",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "entity_type",
                title: "Entity Type",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            }
        ];

        $scope.selectedEntity = undefined;
        $scope.$on("kendoRendered", function(e) {
            var grid = $('#grid2').data("kendoGrid");
            if (grid && $scope.selectedEntity) {
                grid.dataSource.filter({field: "entity", operator: "startswith", value: $scope.selectedEntity});
            }
        });
        $scope.selectEntity = function (id) {
            $scope.selectedEntity = id;
            $http.get(url + id + '/')
                .success(function(data, status, headers, config) {
                    $scope.entity = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
            $http.get($scope.appVariables.baseUrl + "/rest/users_for_entity/" + id + '/')
                .success(function(data, status, headers, config) {
                    $scope.users = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
        };
        $scope.showGrid = function(id) {
            $state.go($state.current.name, {id: id})
        };
        $scope.goToUser = function(id) {
            $state.go('app.users', {id: id})
        };
        $scope.mainGridOptions = defaultgrid.setupGrid(url, columns);

        var transactionsUrl = $scope.appVariables.baseUrl + "/rest/transactions/";
        var transactionsColumns = [
            {
                field: "ref_no",
                title: "Reference Number",
                template: '<a href="" ng-click="goToTransaction(\'#:ref_no#\');">#=ref_no#</a>',
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "start_date",
                title: "Start Date",
                type: "date",
                format: "{0:MMM d, yyyy, h:mm tt}",
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
        $scope.goToTransaction = function(id) {
            $state.go('app.transactions', {id: id})
        };
        $scope.transactionGridOptions = defaultgrid.setupGrid(transactionsUrl, transactionsColumns);

        if ($stateParams.id) {
            $scope.selectEntity($stateParams.id);
        }

    }]);

});