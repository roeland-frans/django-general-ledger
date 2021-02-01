/**
 * @fileoverview This file defines the defaultgrid service
 * which is used to setup a kendo grid for the defaultgrid module.
 */


define([
    'common/module',
    'notification'
], function (module, notification) {

    'use strict';

    /**
     * Service to setup a kendo grid.
     */
    module.factory('defaultgrid', ['$location', function ($location) {
        /**
         * Sets up a default general datasource.
         * @param baseCrudUrl
         */
        var defaultDataSource = function (baseCrudUrl) {
            return {
                type: "json",
                transport: {
                    read: {
                        url: baseCrudUrl,
                        dataType: "json",
                        contentType: "application/json"
                    },
                    parameterMap: function(data, type) {
                        if (type == "read") {
                            var ordering = undefined;
                            if (data.sort !== undefined && data.sort.length > 0) {
                                ordering = data.sort[0].field;
                                if (data.sort[0].dir == 'desc') {
                                    ordering = '-' + ordering;
                                }
                            }

                            var ret_val = {
                                page_size: data.take,
                                page: data.page,
                                ordering: ordering
                            };

                            if (data.filter) {
                                var date;
                                var year;
                                var month;
                                var day;
                                for (var i = 0; i < data.filter.filters.length; i++) {
                                    if (data.filter.filters[i].operator == 'date_gte') {
                                        date = new Date(data.filter.filters[i].value);
                                        year = '' + date.getFullYear();
                                        month = '' + (date.getMonth() + 1);
                                        if (month.length == 1) {
                                            month = '0' + month;
                                        }
                                        day = '' + date.getDate();
                                        if (day.length == 1) {
                                            day = '0' + day;
                                        }
                                        ret_val['' + data.filter.filters[i].field + '_gte'] = '' + year + '-' + month + '-' + day;
                                    } else if (data.filter.filters[i].operator == 'date_lte') {
                                        date = new Date(data.filter.filters[i].value);
                                        year = '' + date.getFullYear();
                                        month = '' + (date.getMonth() + 1);
                                        if (month.length == 1) {
                                            month = '0' + month;
                                        }
                                        day = '' + date.getDate();
                                        if (day.length == 1) {
                                            day = '0' + day;
                                        }
                                        ret_val['' + data.filter.filters[i].field + '_lte'] = '' + year + '-' + month + '-' + day;
                                    } else {
                                        ret_val['' + data.filter.filters[i].field] = data.filter.filters[i].value;
                                    }
                                }
                            }

                            return ret_val
                        }
                    }
                },
                error: function(e) {
                    notification.error(e.status + ": " + e.xhr.status + " - " + e.xhr.statusText);
                    if (e.xhr.status == 403) {
                        window.location = 'login';
                    }
                },
                schema: {
                    data: "results",
                    total: "count"
                },
                pageSize: 25,
                serverFiltering: true,
                serverPaging: true,
                serverSorting: true
            };
        };

        /**
         * Returns a setup dict for a kendo ui grid.
         * @param baseCrudUrl The base url for the REST API.
         * @param columns The columns of the kendo ui grid.
         * @returns object kendo-ui-grid setup dict.
         */
        var setupGrid = function(baseCrudUrl, columns) {
            return {
                dataSource: defaultDataSource(baseCrudUrl),
                selectable: "multiple",
                sortable: true,
                pageable: {
                    pageSizes: [5, 10, 25, 50, 100]
                },
                scrollable: false,
                filterable: {
                    mode: "row, menu",
                    extra: false,
                    operators: {
                        string: {
                            contains: "Contains"
                        },
                        enums: {
                            eq: "Equal to"
                        },
                        date: {
                            date_gte: "Is after or equal to",
                            date_lte: "Is before or equal to"
                        }
                    }
                },
                columns: columns,
                resizable: true
            };
        };

        return {
            setupGrid: setupGrid,
            defaultDataSource: defaultDataSource
        };

    }]);

});