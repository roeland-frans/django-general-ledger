define([
    'backoffice/module',
    'notification'
], function (module, notification) {

    'use strict';

    module.controller('DashboardCtrl', ['$scope', '$http', '$window', function ($scope, $http, $window) {

        $scope.activeUsersSeries = [];
        $scope.dailyNewUsersSeries = [];
        $scope.usersMoneySeries = [];
        $scope.dailyFeesEarnedSeries = [];
        $scope.newTransactionsSeries = [];
        $scope.chartWidth = $window.innerWidth - 280;

        $scope.financialFilterDays = function (item) { return item[1] == 'Days'; };
        $scope.financialFilterMonth = function (item) { return item[1] == 'Month'; };
        $scope.financialFilterYear = function (item) { return item[1] == 'Year'; };

        $http.get($scope.appVariables.baseUrl + "/rest/dashboard/")
            .success(function(data, status, headers, config) {
                $scope.stats = data;
                for (var i = 0; i < $scope.stats.user_sign_ups.length; i++) {
                    $scope.activeUsersSeries.push({value: $scope.stats.user_sign_ups[i][3], date: $scope.stats.user_sign_ups[i][0]});
                    $scope.dailyNewUsersSeries.push({value: $scope.stats.user_sign_ups[i][6], date: $scope.stats.user_sign_ups[i][0]});
                }
                for (var i = 0; i < $scope.stats.liability_balance.length; i++) {
                    $scope.usersMoneySeries.push({value: $scope.stats.liability_balance[i][4], date: $scope.stats.liability_balance[i][0]});
                }
                for (var i = 0; i < $scope.stats.deal_create_metrics.length; i++) {
                    $scope.dailyFeesEarnedSeries.push({value: $scope.stats.deal_create_metrics[i][13], date: $scope.stats.deal_create_metrics[i][0]});
                    $scope.newTransactionsSeries.push({value: $scope.stats.deal_create_metrics[i][11], date: $scope.stats.deal_create_metrics[i][0]});
                }
            })
            .error(function(data, status, headers, config) {
                notification.error(data.message);
            });

    }]);

});