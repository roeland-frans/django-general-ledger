define([
    'backoffice/module',
    'notification'
], function (module, notification) {

    'use strict';

    module.controller('AutoReconCtrl', ['$scope', '$http', '$state', '$stateParams', '$q', 'defaultgrid', function ($scope, $http, $state, $stateParams, $q, defaultgrid) {

        var url = $scope.appVariables.baseUrl + "/rest/bank_statement_lines/auto_recon/";

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

        $scope.gridData = {};

        $scope.dataSource = new kendo.data.DataSource({
            type: "json",
            transport: {
                read: {
                    url: url,
                    dataType: "json",
                    contentType: "application/json"
                }
            },
            pageSize: 25
        });

        $scope.mainGridOptions = {
            dataSource: $scope.dataSource,
            dataBound: function () {
                $scope.gridData.isGridEmpty = $scope.dataSource.total() == 0;
                $scope.gridData.isGridNotEmpty = !$scope.gridData.isGridEmpty;
                $scope.$apply();
            },
            sortable: true,
            pageable: {
                pageSizes: [5, 10, 25, 50, 100]
            },
            scrollable: false,
            filterable: {
                mode: "row"
            },
            columns: columns,
            resizable: true
        };

    }]);

});