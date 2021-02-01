define([
    'backoffice/module',
    'notification'
], function (module, notification) {

    'use strict';

    module.controller('ImportStatementCtrl', ['$scope', '$http', '$state', 'defaultgrid', function ($scope, $http, $state, defaultgrid) {

        var internalBankAccountUrl = $scope.appVariables.baseUrl + "/rest/internal_bank_accounts/";
        var uploadUrl = $scope.appVariables.baseUrl + "/rest/import_statement/";

        $scope.bank = {};
        $scope.statement = {};

        $scope.bankAccountDropDownDataSource = new kendo.data.DataSource(defaultgrid.defaultDataSource(internalBankAccountUrl));
        $scope.bankAccountDropDownOptions = {
            filter: "contains",
            template:"#=acc_no# (#=bank#)",
            valueTemplate:"#=acc_no# (#=bank#)",
            dataTextField: "acc_no",
            dataValueField: "id",
            delay: 0,
            dataSource: $scope.bankAccountDropDownDataSource
        };

        $scope.submit = function () {
            var fd = new FormData();
            fd.append('statement_file', $scope.statement.upload);

            var data ={
                internal_bank_account : $scope.bank.account
            };

            fd.append("internal_bank_account", $scope.bank.account);

            $http.post(uploadUrl, fd, {
                withCredentials: false,
                headers: {
                  'Content-Type': undefined
                },
                transformRequest: angular.identity
            })
            .success(function(data, status, headers, config) {
                $state.go('app.statement_lines')
            })
            .error(function(data, status, headers, config) {
                notification.error(status + " - " + data.message);
            });
        };

    }]);

    module.directive("fileread", [function () {
        return {
            scope: {
                fileread: "="
            },
            link: function (scope, element, attributes) {
                element.bind("change", function (changeEvent) {
                    var reader = new FileReader();
                    reader.onload = function (loadEvent) {
                        scope.$apply(function () {
                            scope.fileread = loadEvent.target.result;
                        });
                    };
                    reader.readAsDataURL(changeEvent.target.files[0]);
                });
            }
        }
    }]);

});