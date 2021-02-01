define([
    'backoffice/module',
    'notification'
], function (module, notification) {

    'use strict';

    module.controller('JournalEntryCtrl', ['$scope', '$http', '$state', '$stateParams', 'defaultgrid', function ($scope, $http, $state, $stateParams, defaultgrid) {

        var url = $scope.appVariables.baseUrl + "/rest/journal_entries/";

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
                field: "name",
                title: "Name",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "journal__name",
                title: "Journal",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "state",
                title: "State",
                values: [
                    { text: 'POSTED', value: 'POSTED' },
                    { text: 'UNPOSTED', value: 'UNPOSTED' },
                    { text: 'RECONCILED', value: 'RECONCILED' }
                ],
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            }
        ];

        $scope.selectedEntry = undefined;
        $scope.selectEntry = function (id) {
            $scope.selectedEntry = id;
            $http.get(url + id + '/')
                .success(function(data, status, headers, config) {
                    $scope.entry = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
            $http.get(url + id + '/entry_lines/')
                .success(function(data, status, headers, config) {
                    $scope.entryLines = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
        };
        $scope.showGrid = function(id) {
            $state.go($state.current.name, {id: id})
        };
        $scope.goToAccount = function(id) {
            $state.go('app.accounts', {id: id})
        };
        $scope.mainGridOptions = defaultgrid.setupGrid(url, columns);

        if ($stateParams.id) {
            $scope.selectEntry($stateParams.id);
        }

    }]);

});