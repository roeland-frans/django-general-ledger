define([
    'backoffice/module',
    'notification'
], function (module, notification) {

    'use strict';

    module.controller('UsersCtrl', ['$scope', '$http', '$state', '$stateParams', 'defaultgrid', '$q', function ($scope, $http, $state, $stateParams, defaultgrid, $q) {

        var url = $scope.appVariables.baseUrl + "/rest/users/";

        var columns = [
            {
                field: "username",
                title: "User Name",
                template: '<a href="" ng-click="showGrid(#=id#);">#=username#</a>',
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "first_name",
                title: "First Name",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "last_name",
                title: "Last Name",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            },
            {
                field: "email",
                title: "Email Address",
                filterable: {cell:{showOperators: false, suggestionOperator: "contains"}}
            }
        ];

        $scope.selectedUser = undefined;
        $scope.$on("kendoRendered", function(e) {
            var grid = $('#grid2').data("kendoGrid");
            if (grid && $scope.selectedUser) {
                grid.dataSource.filter({field: "user", operator: "startswith", value: $scope.selectedUser});
            }
        });
        $scope.selectUser = function (id) {
            $scope.selectedUser = id;
            $http.get(url + id + '/')
                .success(function(data, status, headers, config) {
                    $scope.user_auth = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
            $http.get($scope.appVariables.baseUrl + "/rest/user_profiles/" + id + '/')
                .success(function(data, status, headers, config) {
                    $scope.user_profile = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
            $http.get($scope.appVariables.baseUrl + "/rest/entities_for_user/" + id + '/')
                .success(function(data, status, headers, config) {
                    $scope.entities = data;
                })
                .error(function(data, status, headers, config) {
                    notification.error(data.message);
                });
        };
        $scope.showGrid = function(id) {
            $state.go($state.current.name, {id: id})
        };
        $scope.goToEntity = function(id) {
            $state.go('app.entities', {id: id})
        };
        $scope.goToTransaction = function(id) {
            $state.go('app.transactions', {id: id})
        };
        $scope.updateUsername = function(username) {
            var data = {
                username: username,
                is_active: $scope.user_auth.is_active
            };
            var d = $q.defer();
            $http.put(url + $scope.selectedUser + '/', data)
                .success(function(data, status, headers, config) {
                    d.resolve(true)
                })
                .error(function(data, status, headers, config){
                    d.resolve('' + data.username);
                });
            return d.promise;
        };
        $scope.updateIsActive = function(isActive) {
            var data = {
                username: $scope.user_auth.username,
                is_active: isActive
            };
            var d = $q.defer();
            $http.put(url + $scope.selectedUser + '/', data)
                .success(function(data, status, headers, config) {
                    d.resolve(true)
                })
                .error(function(data, status, headers, config){
                    d.resolve('' + data.is_active);
                });
            return d.promise;
        };
        $scope.updateIdNo = function(idNo) {
            var data = {
                id_no: idNo,
                passport_no: $scope.user_profile.passport_no,
                passport_country: $scope.user_profile.passport_country
            };
            var d = $q.defer();
            $http.put($scope.appVariables.baseUrl + "/rest/user_profiles/" + $scope.selectedUser + '/', data)
                .success(function(data, status, headers, config) {
                    d.resolve(true)
                })
                .error(function(data, status, headers, config){
                    d.resolve('' + data.id_no);
                });
            return d.promise;
        };
        $scope.updatePassportNo = function(passportNo) {
            var data = {
                id_no: $scope.user_profile.id_no,
                passport_no: passportNo,
                passport_country: $scope.user_profile.passport_country
            };
            var d = $q.defer();
            $http.put($scope.appVariables.baseUrl + "/rest/user_profiles/" + $scope.selectedUser + '/', data)
                .success(function(data, status, headers, config) {
                    d.resolve(true)
                })
                .error(function(data, status, headers, config){
                    d.resolve('' + data.passport_no);
                });
            return d.promise;
        };
        $scope.updatePassportCountry = function(passportCountry) {
            var data = {
                id_no: $scope.user_profile.id_no,
                passport_no: $scope.user_profile.passport_no,
                passport_country: passportCountry
            };
            var d = $q.defer();
            $http.put($scope.appVariables.baseUrl + "/rest/user_profiles/" + $scope.selectedUser + '/', data)
                .success(function(data, status, headers, config) {
                    d.resolve(true)
                })
                .error(function(data, status, headers, config){
                    d.resolve('' + data.passport_country);
                });
            return d.promise;
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
        $scope.transactionGridOptions = defaultgrid.setupGrid(transactionsUrl, transactionsColumns);

        if ($stateParams.id) {
            $scope.selectUser($stateParams.id);
        }

    }]);

});