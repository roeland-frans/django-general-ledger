define(['angular'], function(angular) {

angular.module('templates', []).run(['$templateCache', function($templateCache) {
  $templateCache.put("templates/backoffice/views/accounts.tpl.html",
    "<div id=\"content\">\n" +
    "    <div class=\"container-fluid\">\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"page-header\">\n" +
    "                    <h2>Account <small>{{ account.acc_no }}</small> <a class=\"btn btn-primary pull-right\" href=\"\" ng-click=\"showGrid();\" ng-if=\"selectedAccount\">List Accounts</a></h2>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"!selectedAccount\">\n" +
    "            <div class=\"col=md-12\">\n" +
    "                <kendo-grid options=\"mainGridOptions\" id=\"grid\"></kendo-grid>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"selectedAccount\">\n" +
    "            <tabset class=\"ui-tabs\">\n" +
    "                <tab heading=\"Information\">\n" +
    "                    <div class=\"container-fluid\">\n" +
    "                        <br>\n" +
    "                        <div class=\"col-md-6\">\n" +
    "                            <h4>General Information</h4>\n" +
    "                            <table class=\"table table-striped\">\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Account Number:</strong></td>\n" +
    "                                    <td>{{ account.acc_no }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Account Name:</strong></td>\n" +
    "                                    <td>{{ account.name }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Date Created:</strong></td>\n" +
    "                                    <td>{{ account.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Accounting Type:</strong></td>\n" +
    "                                    <td>{{ account.accounting_type }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>State:</strong></td>\n" +
    "                                    <td><a href=\"\" e-style=\"width: 100%\" onbeforesave=\"updateState($data)\" editable-select=\"account.state\" e-ng-options=\"s.value as s.text for s in states\">{{ account.state }}</a></td>\n" +
    "                                </tr>\n" +
    "                            </table>\n" +
    "                        </div>\n" +
    "\n" +
    "                        <div class=\"col-md-6\">\n" +
    "                            <h4>Balance Information</h4>\n" +
    "                            <table class=\"table table-striped\">\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Available Balance:</strong></td>\n" +
    "                                    <td><strong>{{ account.available_balance }}</strong></td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Current Balance:</strong></td>\n" +
    "                                    <td>{{ account.balance }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Pending Balance:</strong></td>\n" +
    "                                    <td>{{ account.pending_balance }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Total Debit:</strong></td>\n" +
    "                                    <td>{{ account.debit }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Total Credit:</strong></td>\n" +
    "                                    <td>{{ account.credit }}</td>\n" +
    "                                </tr>\n" +
    "                            </table>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                </tab>\n" +
    "                <tab heading=\"Statement\">\n" +
    "                    <div class=\"container-fluid\">\n" +
    "                        <br>\n" +
    "                        <h4>Journal Entry Lines</h4>\n" +
    "                        <kendo-grid options=\"statementGridOptions\" id=\"grid\"></kendo-grid>\n" +
    "                    </div>\n" +
    "                </tab>\n" +
    "            </tabset>\n" +
    "        </div>\n" +
    "\n" +
    "    </div>\n" +
    "</div>");
  $templateCache.put("templates/backoffice/views/auto_recon.tpl.html",
    "<div id=\"content\">\n" +
    "    <div class=\"container-fluid\">\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"page-header\">\n" +
    "                    <h2>Reconciled Lines</h2>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-show=\"gridData.isGridEmpty\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"well\">No statement lines were successfully reconciled.</div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-show=\"gridData.isGridNotEmpty\">\n" +
    "            <div class=\"col=md-12\">\n" +
    "                <kendo-grid options=\"mainGridOptions\" id=\"grid\"></kendo-grid>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "    </div>\n" +
    "</div>");
  $templateCache.put("templates/backoffice/views/base.tpl.html",
    "<!-- Navigation -->\n" +
    "<div ng-include=\"'templates/backoffice/views/partials/navbar.tpl.html'\"></div>\n" +
    "\n" +
    "\n" +
    "<div class=\"container\">\n" +
    "\n" +
    "    <!-- Sidebar -->\n" +
    "    <div class=\"sidebar\">\n" +
    "        <div ng-include=\"'templates/backoffice/views/partials/sidebar.tpl.html'\"></div>\n" +
    "    </div>\n" +
    "\n" +
    "    <!-- Content -->\n" +
    "    <div data-ui-view=\"content\" data-autoscroll=\"false\"></div>\n" +
    "\n" +
    "    <span kendo-notification=\"notf1\" id=\"notf1\"></span>\n" +
    "\n" +
    "</div>");
  $templateCache.put("templates/backoffice/views/dashboard.tpl.html",
    "<div id=\"content\">\n" +
    "    <div class=\"container-fluid\">\n" +
    "\n" +
    "        <br>\n" +
    "\n" +
    "        <!-- Stats bar -->\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-xs-2\">\n" +
    "                <div class=\"panel panel-default\">\n" +
    "                    <div class=\"panel-body text-center\">\n" +
    "                        <h5>TOTAL USERS</h5>\n" +
    "                        <h4><b>{{ stats.total_users }}</b></h4>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "            <div class=\"col-xs-2\">\n" +
    "                <div class=\"panel panel-default\">\n" +
    "                    <div class=\"panel-body text-center\">\n" +
    "                        <h5>ACTIVE USERS</h5>\n" +
    "                        <h4><b>{{ stats.active_users }}</b></h4>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "            <div class=\"col-xs-2\">\n" +
    "                <div class=\"panel panel-default\">\n" +
    "                    <div class=\"panel-body text-center\">\n" +
    "                        <h5>USERS ONLINE</h5>\n" +
    "                        <h4><b>{{ stats.online_users }}</b></h4>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "            <div class=\"col-xs-2\">\n" +
    "                <div class=\"panel panel-default\">\n" +
    "                    <div class=\"panel-body text-center\">\n" +
    "                        <h5>USER MONEY</h5>\n" +
    "                        <h4><b>{{ stats.current_liability }}</b></h4>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "            <div class=\"col-xs-2\">\n" +
    "                <div class=\"panel panel-default\">\n" +
    "                    <div class=\"panel-body text-center\">\n" +
    "                        <h5>TOTAL TRANS</h5>\n" +
    "                        <h4><b>{{ stats.total_deals }}</b></h4>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "            <div class=\"col-xs-2\">\n" +
    "                <div class=\"panel panel-default\">\n" +
    "                    <div class=\"panel-body text-center\">\n" +
    "                        <h5>ACTIVE TRANS</h5>\n" +
    "                        <h4><b>{{ stats.active_deals }}</b></h4>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "        <!-- End stats bar -->\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div role=tabpanel>\n" +
    "                    <!-- Nav tabs -->\n" +
    "                    <ul class=\"nav nav-tabs\" role=\"tablist\">\n" +
    "                        <li role=\"presentation\" class=\"active\"><a href=\"#users\" role=\"tab\" data-toggle=\"tab\">Users</a></li>\n" +
    "                        <li role=\"presentation\"><a href=\"#financial\" role=\"tab\" data-toggle=\"tab\">Financial</a></li>\n" +
    "                        <li role=\"presentation\"><a href=\"#transactions\" role=\"tab\" data-toggle=\"tab\">Transactions</a></li>\n" +
    "                    </ul>\n" +
    "\n" +
    "                    <!-- Tab panes -->\n" +
    "                    <div class=\"tab-content\">\n" +
    "                        <!-- Users tab -->\n" +
    "                        <div role=\"tabpanel\" class=\"tab-pane active\" id=\"users\">\n" +
    "                            <h2>Active Users</h2>\n" +
    "                            <div kendo-chart\n" +
    "                                k-series-defaults=\"{ type: 'line' }\"\n" +
    "                                k-series=\"[{name: 'Active Users', field: 'value', categoryField: 'date'}]\"\n" +
    "                                k-data-source=\"activeUsersSeries\"\n" +
    "                                k-category-axis=\"{majorGridLines: {visible: false} }\"\n" +
    "                                k-legend=\"{visible: false}\"\n" +
    "                                k-chart-area=\"{height: 200, width: chartWidth}\"\n" +
    "                                ></div>\n" +
    "                            <h2>Daily New Users</h2>\n" +
    "                            <div kendo-chart\n" +
    "                                k-series-defaults=\"{ type: 'line' }\"\n" +
    "                                k-series=\"[{name: 'Active Users', field: 'value', categoryField: 'date'}]\"\n" +
    "                                k-data-source=\"dailyNewUsersSeries\"\n" +
    "                                k-category-axis=\"{majorGridLines: {visible: false} }\"\n" +
    "                                k-legend=\"{visible: false}\"\n" +
    "                                k-chart-area=\"{height: 200, width: chartWidth}\"\n" +
    "                                ></div>\n" +
    "                        </div>\n" +
    "\n" +
    "                        <!-- Financial tab -->\n" +
    "                        <div role=\"tabpanel\" class=\"tab-pane\" id=\"financial\">\n" +
    "                            <h2>User Money</h2>\n" +
    "                            <div kendo-chart\n" +
    "                                k-series-defaults=\"{ type: 'line' }\"\n" +
    "                                k-series=\"[{name: 'Active Users', field: 'value', categoryField: 'date'}]\"\n" +
    "                                k-data-source=\"usersMoneySeries\"\n" +
    "                                k-category-axis=\"{majorGridLines: {visible: false} }\"\n" +
    "                                k-legend=\"{visible: false}\"\n" +
    "                                k-chart-area=\"{height: 200, width: chartWidth}\"\n" +
    "                                ></div>\n" +
    "                            <h2>Daily Fees Earned</h2>\n" +
    "                            <div kendo-chart\n" +
    "                                k-series-defaults=\"{ type: 'line' }\"\n" +
    "                                k-series=\"[{name: 'Active Users', field: 'value', categoryField: 'date'}]\"\n" +
    "                                k-data-source=\"dailyFeesEarnedSeries\"\n" +
    "                                k-category-axis=\"{majorGridLines: {visible: false} }\"\n" +
    "                                k-legend=\"{visible: false}\"\n" +
    "                                k-chart-area=\"{height: 200, width: chartWidth}\"\n" +
    "                                ></div>\n" +
    "                            <br>\n" +
    "                            <table class=\"table table-striped table-bordered\">\n" +
    "                                <tr>\n" +
    "                                    <th>Date</th>\n" +
    "                                    <th class=\"text-right\">Transactions</th>\n" +
    "                                    <th class=\"text-right\">Fees Raised</th>\n" +
    "                                    <th class=\"text-right\">Average Fee</th>\n" +
    "                                    <th class=\"text-right\">Fees Received</th>\n" +
    "                                    <th class=\"text-right\">Fees Rate</th>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <th class=\"text-left\">Last {{ stats.display_days }} Days</th>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                </tr>\n" +
    "                                <tr ng-repeat=\"object in stats.deal_create_metrics | filter: financialFilterDays\">\n" +
    "                                    <td style=\"width:30%;\">{{ object[0] }} </td>\n" +
    "                                    <td class=\"text-right\">{{ object[4] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[6] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[15] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[9] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[10] }}%</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <th class=\"text-left\">Last {{ stats.display_months }} Months</th>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                </tr>\n" +
    "                                <tr ng-repeat=\"object in stats.deal_create_metrics | filter: financialFilterMonth\">\n" +
    "                                    <td style=\"width:30%;\">{{ object[0] }} </td>\n" +
    "                                    <td class=\"text-right\">{{ object[4] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[6] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[15] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[9] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[10] }}%</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <th class=\"text-left\">Annually</th>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                </tr>\n" +
    "                                <tr ng-repeat=\"object in stats.deal_create_metrics | filter: financialFilterYear\">\n" +
    "                                    <td style=\"width:30%;\">{{ object[0] }} </td>\n" +
    "                                    <td class=\"text-right\">{{ object[4] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[6] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[15] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[9] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[10] }}%</td>\n" +
    "                                </tr>\n" +
    "                            </table>\n" +
    "                        </div>\n" +
    "\n" +
    "                        <!-- Transactions tab -->\n" +
    "                        <div role=\"tabpanel\" class=\"tab-pane\" id=\"transactions\">\n" +
    "                            <h2>New Transactions</h2>\n" +
    "                            <div kendo-chart\n" +
    "                                k-series-defaults=\"{ type: 'line' }\"\n" +
    "                                k-series=\"[{name: 'Active Users', field: 'value', categoryField: 'date'}]\"\n" +
    "                                k-data-source=\"newTransactionsSeries\"\n" +
    "                                k-category-axis=\"{majorGridLines: {visible: false} }\"\n" +
    "                                k-legend=\"{visible: false}\"\n" +
    "                                k-chart-area=\"{height: 200, width: chartWidth}\"\n" +
    "                                ></div>\n" +
    "                            <br>\n" +
    "                            <table class=\"table table-striped table-bordered\">\n" +
    "                                <tr>\n" +
    "                                    <th>Date</th>\n" +
    "                                    <th class=\"text-right\">Transactions</th>\n" +
    "                                    <th class=\"text-right\">Values</th>\n" +
    "                                    <th class=\"text-right\">Average Value</th>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <th class=\"text-left\">Last {{ stats.display_days }} Days</th>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                </tr>\n" +
    "                                <tr ng-repeat=\"object in stats.deal_create_metrics | filter: financialFilterDays\">\n" +
    "                                    <td style=\"width:30%;\">{{ object[0] }} </td>\n" +
    "                                    <td class=\"text-right\">{{ object[4] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[5] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[14] }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <th class=\"text-left\">Last {{ stats.display_months }} Months</th>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                </tr>\n" +
    "                                <tr ng-repeat=\"object in stats.deal_create_metrics | filter: financialFilterMonth\">\n" +
    "                                    <td style=\"width:30%;\">{{ object[0] }} </td>\n" +
    "                                    <td class=\"text-right\">{{ object[4] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[5] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[14] }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <th class=\"text-left\">Annually</th>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                    <td class=\"text-left\"> </td>\n" +
    "                                </tr>\n" +
    "                                <tr ng-repeat=\"object in stats.deal_create_metrics | filter: financialFilterYear\">\n" +
    "                                    <td style=\"width:30%;\">{{ object[0] }} </td>\n" +
    "                                    <td class=\"text-right\">{{ object[4] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[5] }}</td>\n" +
    "                                    <td class=\"text-right\">{{ object[14] }}</td>\n" +
    "                                </tr>\n" +
    "                            </table>\n" +
    "                            <div class=\"row\">\n" +
    "                                <div class=\"col-sm-6\">\n" +
    "                                    <div class=\"header\">\n" +
    "                                        <h2>Transactions by State</h2>\n" +
    "                                    </div>\n" +
    "                                    <table class=\"table table-striped table-bordered\">\n" +
    "                                        <tr>\n" +
    "                                            <th>Status</th>\n" +
    "                                            <th class=\"text-right\">Transactions</th>\n" +
    "                                        </tr>\n" +
    "                                        <tr ng-repeat=\"object in stats.deal_states\">\n" +
    "                                            <td>{{ object[0] }}</td>\n" +
    "                                            <td class=\"text-right\">{{ object[1] }}</td>\n" +
    "                                        </tr>\n" +
    "                                        <tr>\n" +
    "                                            <th>Total</th>\n" +
    "                                            <th class=\"text-right\">{{ stats.total_deals }}</th>\n" +
    "                                        </tr>\n" +
    "                                    </table>\n" +
    "                                </div>\n" +
    "                                <div class=\"col-sm-6\">\n" +
    "                                    <div class=\"header\">\n" +
    "                                        <h2>Average Transactions</h2>\n" +
    "                                    </div>\n" +
    "                                    <div class=\"panel panel-default\">\n" +
    "                                        <div class=\"panel-body\">\n" +
    "                                            <p>\n" +
    "                                                In the last <b>{{ stats.months_average }}</b> months, <b>{{ stats.avg_trans[0][0] }}</b>\n" +
    "                                                transactions were successfully started. The average value of these\n" +
    "                                                transactions were <b>{{ stats.avg_trans[0][1] }}</b> at an average fee of\n" +
    "                                                <b>{{ stats.avg_trans[0][2] }}</b>.\n" +
    "                                            </p>\n" +
    "                                            <p>\n" +
    "                                                Of these, <b>{{ stats.trans_duration[0][0] }}</b> are already completed and it\n" +
    "                                                took on average <b>{{ stats.trans_duration[0][1] }}</b> days to open the transactions\n" +
    "                                                and after a further <b>{{ stats.trans_duration[0][2] }}</b> days, the transactions\n" +
    "                                                were completed. All in all, the average duration of transactions were\n" +
    "                                                <b>{{ stats.trans_duration[0][3] }}</b> days.\n" +
    "                                            </p>\n" +
    "                                            <p>\n" +
    "                                                These transactions used <b>{{ stats.trans_progress[0][3] }}</b> payments,\n" +
    "                                                <b>{{ stats.trans_progress[0][2] }}</b> refunds and <b>{{ stats.trans_progress[0][1] }}</b>\n" +
    "                                                negotiations. <b>{{ stats.trans_progress[0][13] }}%</b> of the transactions had a\n" +
    "                                                single payment only and <b>{{ stats.trans_progress[0][16] }}%</b> used multiply\n" +
    "                                                payments. The transaction with the most payments used\n" +
    "                                                <b>{{ stats.trans_progress[0][9] }}</b> payments.\n" +
    "                                            </p>\n" +
    "                                        </div>\n" +
    "                                    </div>\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "\n" +
    "                    <br>\n" +
    "\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "    </div>\n" +
    "</div>");
  $templateCache.put("templates/backoffice/views/entities.tpl.html",
    "<div id=\"content\">\n" +
    "    <div class=\"container-fluid\">\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"page-header\">\n" +
    "                    <h2>Entity <small>{{ entity.name }}</small> <a class=\"btn btn-primary pull-right\" href=\"\" ng-click=\"showGrid();\" ng-if=\"selectedEntity\">List Entities</a></h2>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"!selectedEntity\">\n" +
    "            <div class=\"col=md-12\">\n" +
    "                <kendo-grid options=\"mainGridOptions\" id=\"grid\"></kendo-grid>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"selectedEntity\">\n" +
    "            <tabset class=\"ui-tabs\">\n" +
    "                <tab heading=\"Information\">\n" +
    "                    <div class=\"container-fluid\">\n" +
    "                        <br>\n" +
    "                        <div class=\"col-md-6\">\n" +
    "                            <h4>General Information</h4>\n" +
    "                            <table class=\"table table-striped\">\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Entity Number:</strong></td>\n" +
    "                                    <td>{{ entity.entity_no }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Entity Type:</strong></td>\n" +
    "                                    <td>{{ entity.entity_type }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Name:</strong></td>\n" +
    "                                    <td>{{ entity.name }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Telephone:</strong></td>\n" +
    "                                    <td>{{ entity.telephone }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Fax:</strong></td>\n" +
    "                                    <td>{{ entity.fax }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>E-Mail:</strong></td>\n" +
    "                                    <td>{{ entity.email }}</td>\n" +
    "                                </tr>\n" +
    "                            </table>\n" +
    "                        </div>\n" +
    "\n" +
    "                        <div class=\"col-md-6\">\n" +
    "                            <address>\n" +
    "                                <h4>Physical Address:</h4>\n" +
    "                                {{ entity.physical_address.address }}<br>\n" +
    "                                {{ entity.physical_address.suburb }}<br>\n" +
    "                                {{ entity.physical_address.city }}<br>\n" +
    "                                {{ entity.physical_address.province }}<br>\n" +
    "                                {{ entity.physical_address.code }}<br>\n" +
    "                            </address>\n" +
    "                            <address>\n" +
    "                                <h4>Postal Address:</h4>\n" +
    "                                {{ entity.postal_address.address }}<br>\n" +
    "                                {{ entity.postal_address.suburb }}<br>\n" +
    "                                {{ entity.postal_address.city }}<br>\n" +
    "                                {{ entity.postal_address.province }}<br>\n" +
    "                                {{ entity.postal_address.code }}<br>\n" +
    "                            </address>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "\n" +
    "                    <div class=\"row\"  ng-if=\"selectedEntity\">\n" +
    "                        <div class=\"col-md-12\">\n" +
    "                            <div class=\"header\">\n" +
    "                                <h4>Users</h4>\n" +
    "                            </div>\n" +
    "                            <div class=\"content\">\n" +
    "                                <table class=\"table table-striped\">\n" +
    "                                    <thead>\n" +
    "                                        <tr>\n" +
    "                                        <th><strong>User Name</strong></th>\n" +
    "                                        <th><strong>First Name</strong></th>\n" +
    "                                        <th><strong>Last Name</strong></th>\n" +
    "                                        <th><strong>Email</strong></th>\n" +
    "                                        </tr>\n" +
    "                                    </thead>\n" +
    "                                    <tbody>\n" +
    "                                        <tr ng-repeat=\"user in users\">\n" +
    "                                            <td><a href=\"\" ng-click=\"goToUser(user.id)\">{{ user.username }}</a></td>\n" +
    "                                            <td>{{ user.first_name }}</td>\n" +
    "                                            <td>{{ user.last_name }}</td>\n" +
    "                                            <td>{{ user.email }}</td>\n" +
    "                                        </tr>\n" +
    "                                    </tbody>\n" +
    "                                </table>\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                        <div class=\"clear\"></div>\n" +
    "                    </div>\n" +
    "                </tab>\n" +
    "                <tab heading=\"Transactions\">\n" +
    "                    <div class=\"container-fluid\">\n" +
    "                        <br>\n" +
    "                        <h4>Transactions</h4>\n" +
    "                        <kendo-grid  options=\"transactionGridOptions\" id=\"grid2\" name=\"grid2\"></kendo-grid>\n" +
    "                    </div>\n" +
    "                </tab>\n" +
    "            </tabset>\n" +
    "        </div>\n" +
    "    </div>\n" +
    "</div>");
  $templateCache.put("templates/backoffice/views/fnb_pacs.tpl.html",
    "<div id=\"content\">\n" +
    "    <div class=\"container-fluid\">\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"page-header\">\n" +
    "                    <h2>FNB PACS</h2>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div role=tabpanel>\n" +
    "                    <!-- Nav tabs -->\n" +
    "                    <ul class=\"nav nav-tabs\" role=\"tablist\">\n" +
    "                        <li role=\"presentation\" class=\"active\"><a href=\"#accounts\" role=\"tab\" data-toggle=\"tab\">Accounts</a></li>\n" +
    "                        <li role=\"presentation\"><a href=\"#pacs\" role=\"tab\" data-toggle=\"tab\">PACS Files</a></li>\n" +
    "                        <li role=\"presentation\"><a href=\"#statements\" role=\"tab\" data-toggle=\"tab\">Statement Files</a></li>\n" +
    "                    </ul>\n" +
    "\n" +
    "                    <!-- Tab panes -->\n" +
    "                    <div class=\"tab-content\">\n" +
    "                        <!-- Accounts tab -->\n" +
    "                        <div role=\"tabpanel\" class=\"tab-pane active\" id=\"accounts\">\n" +
    "                            <div class=\"header\">\n" +
    "                                <h4>FNB Bank Accounts</h4>\n" +
    "                            </div>\n" +
    "                            <table class=\"table table-striped table-bordered\">\n" +
    "                                <thead>\n" +
    "                                    <tr>\n" +
    "                                        <th><strong>Account No</strong></th>\n" +
    "                                        <th><strong>Branch</strong></th>\n" +
    "                                        <th><strong>Bank</strong></th>\n" +
    "                                        <th><strong>Account Type</strong></th>\n" +
    "                                        <th><strong>Internal Account</strong></th>\n" +
    "                                        <th><strong>Journal</strong></th>\n" +
    "                                    </tr>\n" +
    "                                </thead>\n" +
    "                                <tbody>\n" +
    "                                    <tr ng-repeat=\"account in bank_accounts\">\n" +
    "                                        <td>{{ account.acc_no }}</td>\n" +
    "                                        <td>{{ account.branch }}</td>\n" +
    "                                        <td>{{ account.bank }}</td>\n" +
    "                                        <td>{{ account.account_type }}</td>\n" +
    "                                        <td><a href=\"\">{{ account.account.acc_no }} - {{ account.account.name }} ({{ account.account.balance }})</a></td>\n" +
    "                                        <td>{{ account.journal }}</td>\n" +
    "                                    </tr>\n" +
    "                                </tbody>\n" +
    "                            </table>\n" +
    "\n" +
    "                            <div class=\"header\">\n" +
    "                                <h4>FNB PACS Accounts</h4>\n" +
    "                            </div>\n" +
    "                            <table class=\"table table-striped table-bordered\">\n" +
    "                                <thead>\n" +
    "                                    <tr>\n" +
    "                                        <th><strong>Username</strong></th>\n" +
    "                                        <th><strong>Last Statement Time</strong></th>\n" +
    "                                        <th><strong>Last PACS Time</strong></th>\n" +
    "                                        <th><strong>Statement File No</strong></th>\n" +
    "                                        <th><strong>User Gen No</strong></th>\n" +
    "                                        <th><strong>Hash No</strong></th>\n" +
    "                                        <th><strong>Load Report No</strong></th>\n" +
    "                                        <th><strong>Rejected No</strong></th>\n" +
    "                                        <th><strong>Unpaid No</strong></th>\n" +
    "                                    </tr>\n" +
    "                                </thead>\n" +
    "                                <tbody>\n" +
    "                                    <tr ng-repeat=\"account in pacs_accounts\">\n" +
    "                                        <td>{{ account.username }}</td>\n" +
    "                                        <td>{{ account.last_statement_time | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                                        <td>{{ account.last_pacs_time }}</td>\n" +
    "                                        <td>{{ account.statement_file_no }}</td>\n" +
    "                                        <td>{{ account.user_gen_no }}</td>\n" +
    "                                        <td>{{ account.hash_no }}</td>\n" +
    "                                        <td>{{ account.load_report_no }}</td>\n" +
    "                                        <td>{{ account.rejected_no }}</td>\n" +
    "                                        <td>{{ account.unpaid_no }}</td>\n" +
    "                                    </tr>\n" +
    "                                </tbody>\n" +
    "                            </table>\n" +
    "                        </div>\n" +
    "\n" +
    "                        <!-- Pacs tab -->\n" +
    "                        <div role=\"tabpanel\" class=\"tab-pane\" id=\"pacs\">\n" +
    "                            <kendo-grid options=\"pacsGridOptions\" id=\"grid\"></kendo-grid>\n" +
    "                        </div>\n" +
    "\n" +
    "                        <!-- Statements tab -->\n" +
    "                        <div role=\"tabpanel\" class=\"tab-pane\" id=\"statements\">\n" +
    "                            <kendo-grid options=\"statementGridOptions\" id=\"grid\"></kendo-grid>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "\n" +
    "                    <br>\n" +
    "\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "    </div>\n" +
    "</div>");
  $templateCache.put("templates/backoffice/views/import_statement.tpl.html",
    "<div id=\"content\">\n" +
    "    <div class=\"container-fluid\">\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"page-header\">\n" +
    "                    <h2>Import Statement</h2>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-6\">\n" +
    "                <form novalidate>\n" +
    "                    <div class=\"form-group\">\n" +
    "                        <label>Internal Bank Account:</label>\n" +
    "                        <kendo-drop-down-list style=\"width:100%\" ng-model=\"bank.account\" options=\"bankAccountDropDownOptions\"></kendo-drop-down-list>\n" +
    "                    </div>\n" +
    "                    <div class=\"form-group\">\n" +
    "                        <label>Statement File:</label>\n" +
    "                        <input type=\"file\" fileread=\"statement.upload\" />\n" +
    "                    </div>\n" +
    "                    <button type=\"submit\" ng-click=\"submit();\" ng-disabled=\"!statement.upload\" class=\"btn btn-default pull-right\">Submit</button>\n" +
    "                </form>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "    </div>\n" +
    "</div>");
  $templateCache.put("templates/backoffice/views/journal_entries.tpl.html",
    "<div id=\"content\">\n" +
    "    <div class=\"container-fluid\">\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"page-header\">\n" +
    "                    <h2>Journal Entry <small>{{ entry.ref_no }}</small> <a class=\"btn btn-primary pull-right\" href=\"\" ng-click=\"showGrid();\" ng-if=\"selectedEntry\">List Journal Entries</a></h2>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"!selectedEntry\">\n" +
    "            <div class=\"col=md-12\">\n" +
    "                <kendo-grid options=\"mainGridOptions\" id=\"grid\"></kendo-grid>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"selectedEntry\">\n" +
    "            <div class=\"col-md-6\">\n" +
    "                <h4>Details</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Reference No:</strong></td>\n" +
    "                        <td>{{ entry.ref_no }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Created:</strong></td>\n" +
    "                        <td>{{ entry.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Name:</strong></td>\n" +
    "                        <td>{{ entry.name }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Journal:</strong></td>\n" +
    "                        <td>{{ entry.journal }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>State:</strong></td>\n" +
    "                        <td>{{ entry.state }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\"  ng-if=\"selectedEntry\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"header\">\n" +
    "                    <h4>Journal Entry Lines</h4>\n" +
    "                </div>\n" +
    "                <div class=\"content\">\n" +
    "                    <table class=\"table table-striped\">\n" +
    "                        <thead>\n" +
    "                            <tr>\n" +
    "                                <th><strong>Id</strong></th>\n" +
    "                                <th><strong>Name</strong></th>\n" +
    "                                <th><strong>Date Created</strong></th>\n" +
    "                                <th><strong>Account</strong></th>\n" +
    "                                <th class=\"text-right\"><strong>Debit</strong></th>\n" +
    "                                <th class=\"text-right\"><strong>Credit</strong></th>\n" +
    "                                <th class=\"text-right\"><strong>Account Balance</strong></th>\n" +
    "                                <th><strong>State</strong></th>\n" +
    "                            </tr>\n" +
    "                        </thead>\n" +
    "                        <tbody>\n" +
    "                            <tr ng-repeat=\"line in entryLines\">\n" +
    "                                <td><span data-toggle=\"tooltip\" title=\"Ref No: {{ line.ref_no }}\">{{ line.pk }}</span></td>\n" +
    "                                <td>{{ line.name }}</td>\n" +
    "                                <td>{{ line.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                                <td><a href=\"\" ng-click=\"goToAccount(line.account_number)\">{{ line.account_name }}</a></td>\n" +
    "                                <td class=\"text-right\">{{ line.debit }}</td>\n" +
    "                                <td class=\"text-right\">{{ line.credit }}</td>\n" +
    "                                <td class=\"text-right\">{{ line.account_balance }}</td>\n" +
    "                                <td>{{ line.state }}</td>\n" +
    "                            </tr>\n" +
    "                        </tbody>\n" +
    "                    </table>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "            <div class=\"clear\"></div>\n" +
    "        </div>\n" +
    "\n" +
    "    </div>\n" +
    "</div>");
  $templateCache.put("templates/backoffice/views/partials/navbar.tpl.html",
    "<nav class=\"navbar navbar-inverse navbar-fixed-top topnav\" role=\"navigation\">\n" +
    "\n" +
    "    <div class=\"container-fluid topnav\">\n" +
    "\n" +
    "        <!-- Branding -->\n" +
    "        <div class=\"navbar-header\">\n" +
    "            <button type=\"button\" class=\"navbar-toggle\" data-toggle=\"collapse\" data-target=\".navbar-collapse\">\n" +
    "                <span class=\"sr-only\">Toggle navigation</span>\n" +
    "                <span class=\"icon-bar\"></span>\n" +
    "                <span class=\"icon-bar\"></span>\n" +
    "                <span class=\"icon-bar\"></span>\n" +
    "            </button>\n" +
    "            <a class=\"navbar-brand\" href=\"{{ appVariables.landingRoute }}\">&nbsp;&nbsp;&nbsp;&nbsp;</a>\n" +
    "        </div>\n" +
    "\n" +
    "        <!-- Navbar Items -->\n" +
    "        <div id=\"navbar\" class=\"navbar-collapse collapse\">\n" +
    "            <ul class=\"nav navbar-nav navbar-right\">\n" +
    "                <!-- Username -->\n" +
    "                <li><p class=\"navbar-text\">{{ appVariables.username }}</p></li>\n" +
    "                <li><a href=\"/logout/\">Logout</a></li>\n" +
    "            </ul>\n" +
    "        </div>\n" +
    "\n" +
    "    </div>\n" +
    "\n" +
    "</nav>");
  $templateCache.put("templates/backoffice/views/partials/sidebar.tpl.html",
    "<!-- Sidebar Menu Items - These collapse to the responsive navigation menu on small screens -->\n" +
    "<div class=\"collapse navbar-collapse navbar-ex1-collapse\">\n" +
    "    <ul class=\"nav nav-sidebar\">\n" +
    "\n" +
    "        <!-- Dashboard -->\n" +
    "        <li data-ui-sref-active=\"active\">\n" +
    "            <a data-ui-sref=\"app.dashboard\"><i class=\"fa fa-fw fa-bar-chart-o\"></i> Dashboard</a>\n" +
    "        </li>\n" +
    "\n" +
    "        <!-- Users -->\n" +
    "        <li data-ui-sref-active=\"active\">\n" +
    "            <a data-ui-sref=\"app.users\"><i class=\"fa fa-fw fa-users\"></i> Users</a>\n" +
    "        </li>\n" +
    "\n" +
    "        <!-- Entities -->\n" +
    "        <li data-ui-sref-active=\"active\">\n" +
    "            <a data-ui-sref=\"app.entities\"><i class=\"fa fa-fw fa-building-o\"></i> Entities</a>\n" +
    "        </li>\n" +
    "\n" +
    "        <!-- Transactions -->\n" +
    "        <li data-ui-sref-active=\"active\">\n" +
    "            <a data-ui-sref=\"app.transactions\"><i class=\"fa fa-fw fa-credit-card\"></i> Transactions</a>\n" +
    "        </li>\n" +
    "\n" +
    "        <hr>\n" +
    "\n" +
    "        <h4>Accounts</h4>\n" +
    "\n" +
    "        <!-- All Accounts -->\n" +
    "        <li data-ui-sref-active=\"active\">\n" +
    "            <a data-ui-sref=\"app.accounts\"><i class=\"fa fa-fw fa-table\"></i>  All Accounts</a>\n" +
    "        </li>\n" +
    "\n" +
    "        <!-- Traders Accounts -->\n" +
    "        <li data-ui-sref-active=\"active\">\n" +
    "            <a data-ui-sref=\"app.account_traders\"><i class=\"fa fa-fw fa-table\"></i>  Traders Accounts</a>\n" +
    "        </li>\n" +
    "\n" +
    "        <!-- General Accounts -->\n" +
    "        <li data-ui-sref-active=\"active\">\n" +
    "            <a data-ui-sref=\"app.account_general\"><i class=\"fa fa-fw fa-table\"></i> General Accounts</a>\n" +
    "        </li>\n" +
    "\n" +
    "        <!-- Bank Accounts -->\n" +
    "        <li data-ui-sref-active=\"active\">\n" +
    "            <a data-ui-sref=\"app.account_bank\"><i class=\"fa fa-fw fa-table\"></i> Bank Accounts</a>\n" +
    "        </li>\n" +
    "\n" +
    "        <!-- Journal Entries -->\n" +
    "        <li data-ui-sref-active=\"active\">\n" +
    "            <a data-ui-sref=\"app.journal_entries\"><i class=\"fa fa-fw fa-book\"></i> Journal Entries</a>\n" +
    "        </li>\n" +
    "\n" +
    "        <hr>\n" +
    "\n" +
    "        <h4>Bank</h4>\n" +
    "\n" +
    "        <!-- Payment Batches -->\n" +
    "        <li data-ui-sref-active=\"active\">\n" +
    "            <a data-ui-sref=\"app.payment_batches\"><i class=\"fa fa-fw fa-money\"></i> Payment Batches</a>\n" +
    "        </li>\n" +
    "\n" +
    "        <!-- Payment Lines -->\n" +
    "        <li data-ui-sref-active=\"active\">\n" +
    "            <a data-ui-sref=\"app.payment_lines\"><i class=\"fa fa-fw fa-money\"></i> Payment Lines</a>\n" +
    "        </li>\n" +
    "\n" +
    "        <!-- Statements -->\n" +
    "        <li data-ui-sref-active=\"active\">\n" +
    "            <a data-ui-sref=\"app.statements\"><i class=\"fa fa-fw fa-file-o\"></i> Statements</a>\n" +
    "        </li>\n" +
    "\n" +
    "        <!-- Statement Lines -->\n" +
    "        <li data-ui-sref-active=\"active\">\n" +
    "            <a data-ui-sref=\"app.statement_lines\"><i class=\"fa fa-fw fa-file-o\"></i> Statement Lines</a>\n" +
    "        </li>\n" +
    "\n" +
    "        <!-- FNB PACS -->\n" +
    "        <li data-ui-sref-active=\"active\">\n" +
    "            <a data-ui-sref=\"app.fnb_pacs\"><i class=\"fa fa-fw fa-btc\"></i> FNB PACS</a>\n" +
    "        </li>\n" +
    "\n" +
    "    </ul>\n" +
    "</div>");
  $templateCache.put("templates/backoffice/views/payment_batches.tpl.html",
    "<div id=\"content\">\n" +
    "    <div class=\"container-fluid\">\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"page-header\">\n" +
    "                    <h2>Bank Payment Batches <small>{{ entry.ref_no }}</small> <a class=\"btn btn-primary pull-right\" href=\"\" ng-click=\"showGrid();\" ng-if=\"selectedBatch\">List Payment Batches</a></h2>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"!selectedBatch\">\n" +
    "            <div class=\"col=md-12\">\n" +
    "                <kendo-grid options=\"mainGridOptions\" id=\"grid\"></kendo-grid>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"selectedBatch\">\n" +
    "            <div class=\"col-md-6\">\n" +
    "                <h4>Batch Details</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Reference Number:</strong></td>\n" +
    "                        <td>{{ batch.ref_no }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Created:</strong></td>\n" +
    "                        <td>{{ batch.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Submitted:</strong></td>\n" +
    "                        <td>{{ batch.date_submitted | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Bank Line Type:</strong></td>\n" +
    "                        <td>{{ batch.bank_line_type }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Total Amount:</strong></td>\n" +
    "                        <td>{{ batch.total_amount }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>State:</strong></td>\n" +
    "                        <td>{{ batch.state }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Error Message:</strong></td>\n" +
    "                        <td>{{ batch.error_message || 'None' }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "            </div>\n" +
    "            <div class=\"col-md-6\">\n" +
    "                <h4>Bank Account</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Bank Name:</strong></td>\n" +
    "                        <td>{{ batch.bank_account.bank }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Account Number:</strong></td>\n" +
    "                        <td>{{ batch.bank_account.acc_no }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Branch Code:</strong></td>\n" +
    "                        <td>{{ batch.bank_account.branch }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Journal:</strong></td>\n" +
    "                        <td>{{ batch.bank_account.journal }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Internal Account:</strong></td>\n" +
    "                        <td><a href=\"\" ng-click=\"goToAccount(batch.bank_account.account.acc_no)\">{{ batch.bank_account.account.acc_no }} - {{ batch.bank_account.account.name }} ({{ batch.bank_account.account.available_balance }})</a></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Currency:</strong></td>\n" +
    "                        <td>{{ batch.bank_account.currency.code }} ({{ batch.bank_account.currency.name }}) {{ batch.bank_account.currency.current_rate }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\"  ng-if=\"selectedBatch\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"header\">\n" +
    "                    <h4>Payment Lines</h4>\n" +
    "                </div>\n" +
    "                <div class=\"content\">\n" +
    "                    <table class=\"table table-striped\">\n" +
    "                        <thead>\n" +
    "                            <tr>\n" +
    "                                <th><strong>Bank Ref</strong></th>\n" +
    "                                <th><strong>Date Created</strong></th>\n" +
    "                                <th><strong>Bank Line Type</strong></th>\n" +
    "                                <th><strong>Debit Account</strong></th>\n" +
    "                                <th><strong>Dest Account</strong></th>\n" +
    "                                <th class=\"text-right\"><strong>Amount</strong></th>\n" +
    "                                <th><strong>State</strong></th>\n" +
    "                            </tr>\n" +
    "                        </thead>\n" +
    "                        <tbody>\n" +
    "                            <tr ng-repeat=\"line in paymentLines\">\n" +
    "                                <td><a href=\"\" ng-click=\"goToPaymentLine(line.ref_no)\" data-toggle=\"tooltip\" title=\"{{ line.ref_no }}\">{{ line.bank_ref }}</a></td>\n" +
    "                                <td>{{ line.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                                <td>{{ line.bank_line_type }}</td>\n" +
    "                                <td><a href=\"\" ng-click=\"goToAccount(line.debit_account.acc_no)\">{{ line.debit_account.acc_no }} - {{ line.debit_account.name }} ({{ line.debit_account.available_balance }})</a></td>\n" +
    "                                <td>{{ line.dest_bank_acc_name }}</td>\n" +
    "                                <td class=\"text-right\">{{ line.amount }}</td>\n" +
    "                                <td>{{ line.state }}</td>\n" +
    "                            </tr>\n" +
    "                        </tbody>\n" +
    "                    </table>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "            <div class=\"clear\"></div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\"  ng-if=\"selectedBatch\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"header\">\n" +
    "                    <h4>Journal Entry Lines</h4>\n" +
    "                </div>\n" +
    "                <div class=\"content\">\n" +
    "                    <table class=\"table table-striped\">\n" +
    "                        <thead>\n" +
    "                            <tr>\n" +
    "                                <th><strong>Id</strong></th>\n" +
    "                                <th><strong>Name</strong></th>\n" +
    "                                <th><strong>Date Created</strong></th>\n" +
    "                                <th><strong>Account</strong></th>\n" +
    "                                <th class=\"text-right\"><strong>Debit</strong></th>\n" +
    "                                <th class=\"text-right\"><strong>Credit</strong></th>\n" +
    "                                <th class=\"text-right\"><strong>Account Balance</strong></th>\n" +
    "                                <th><strong>State</strong></th>\n" +
    "                            </tr>\n" +
    "                        </thead>\n" +
    "                        <tbody>\n" +
    "                            <tr ng-repeat=\"line in entryLines\">\n" +
    "                                <td><span data-toggle=\"tooltip\" title=\"Ref No: {{ line.ref_no }}\">{{ line.pk }}</span></td>\n" +
    "                                <td>{{ line.name }}</td>\n" +
    "                                <td>{{ line.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                                <td><a href=\"\" ng-click=\"goToAccount(line.account_number)\">{{ line.account_name }}</a></td>\n" +
    "                                <td class=\"text-right\">{{ line.debit }}</td>\n" +
    "                                <td class=\"text-right\">{{ line.credit }}</td>\n" +
    "                                <td class=\"text-right\">{{ line.account_balance }}</td>\n" +
    "                                <td>{{ line.state }}</td>\n" +
    "                            </tr>\n" +
    "                        </tbody>\n" +
    "                    </table>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "            <div class=\"clear\"></div>\n" +
    "        </div>\n" +
    "\n" +
    "    </div>\n" +
    "</div>");
  $templateCache.put("templates/backoffice/views/payment_lines.tpl.html",
    "<div id=\"content\">\n" +
    "    <div class=\"container-fluid\">\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"page-header\">\n" +
    "                    <h2>Bank Payment Lines <small>{{ line.ref_no }}</small> <a class=\"btn btn-primary pull-right\" href=\"\" ng-click=\"showGrid();\" ng-if=\"selectedLine\">List Payment Lines</a></h2>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"!selectedLine\">\n" +
    "            <div class=\"col=md-12\">\n" +
    "                <kendo-grid options=\"mainGridOptions\" id=\"grid\"></kendo-grid>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"selectedLine\">\n" +
    "            <div class=\"col-md-6\">\n" +
    "                <h4>Payment Details</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Reference Number:</strong></td>\n" +
    "                        <td>{{ line.ref_no }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Created:</strong></td>\n" +
    "                        <td>{{ line.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Submitted:</strong></td>\n" +
    "                        <td>{{ line.date_submitted | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Bank Reference:</strong></td>\n" +
    "                        <td>{{ line.bank_ref }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Bank Line Type:</strong></td>\n" +
    "                        <td>{{ line.bank_line_type }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Amount:</strong></td>\n" +
    "                        <td>{{ line.amount }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Description:</strong></td>\n" +
    "                        <td>{{ line.description }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Journal Entry:</strong></td>\n" +
    "                        <td><a href=\"\" ng-click=\"goToJournalEntry(line.journal_entry.ref_no)\" data-toggle=\"tooltip\" title=\"Ref No: {{ line.journal_entry.ref_no }}\">{{ line.journal_entry.name }}</a></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>State:</strong></td>\n" +
    "                        <td>{{ line.state }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr ng-if=\"isActionDateUpdateable()\">\n" +
    "                        <td><strong>Action Date:</strong></td>\n" +
    "                        <td ng-if=\"!datepickerVisible\">\n" +
    "                            <a href=\"\" ng-click=\"makeDatepickerVisible(true)\">{{ line.action_date | date:appVariables.ngDateFormat }}</a>\n" +
    "                        </td>\n" +
    "                        <td ng-if=\"datepickerVisible\">\n" +
    "                            <input kendo-date-picker ng-model=\"line.action_date\" k-format=\"'yyyy-MM-dd'\" />\n" +
    "                            <button type=\"button\" class=\"btn btn-primary\" ng-click=\"updateActionDate()\"><i class=\"fa fa-check\"></i></button>\n" +
    "                            <button type=\"button\" class=\"btn btn-default\" ng-click=\"makeDatepickerVisible(false)\"><i class=\"fa fa-times\"></i></button>\n" +
    "                        </td>\n" +
    "                    </tr>\n" +
    "                    <tr ng-if=\"!isActionDateUpdateable()\">\n" +
    "                        <td><strong>Action Date:</strong></td>\n" +
    "                        <td>{{ line.action_date | date:appVariables.ngDateFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Error Message:</strong></td>\n" +
    "                        <td>{{ line.error_message || 'None' }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "                <h4 ng-if=\"line.bank_payment_batch\">Bank Payment Batch</h4>\n" +
    "                <table class=\"table table-striped\" ng-if=\"line.bank_payment_batch\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Reference:</strong></td>\n" +
    "                        <td><a href=\"\" ng-click=\"goToPaymentBatch(line.bank_payment_batch.ref_no)\">{{ line.bank_payment_batch.ref_no }}</a></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Created:</strong></td>\n" +
    "                        <td>{{ line.bank_payment_batch.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Submitted:</strong></td>\n" +
    "                        <td>{{ line.bank_payment_batch.date_submitted | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Total Amount:</strong></td>\n" +
    "                        <td>{{ line.bank_payment_batch.total_amount }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>State:</strong></td>\n" +
    "                        <td>{{ line.bank_payment_batch.state }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Error Message:</strong></td>\n" +
    "                        <td>{{ line.bank_payment_batch.error_message || 'None' }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "            </div>\n" +
    "            <div class=\"col-md-6\">\n" +
    "                <h4>Entity</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Entity Number:</strong></td>\n" +
    "                        <td><a href=\"\" ng-click=\"goToEntity(line.dest_bank_acc.entity.id)\">{{ line.dest_bank_acc.entity.entity_no }}</a></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>name:</strong></td>\n" +
    "                        <td>{{ line.dest_bank_acc.entity.name }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "                <h4>Debit Account</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Account Number:</strong></td>\n" +
    "                        <td><a href=\"\" ng-click=\"goToAccount(line.debit_account.acc_no)\">{{ line.debit_account.acc_no }}</a></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Name:</strong></td>\n" +
    "                        <td>{{ line.debit_account.name }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Current Balance:</strong></td>\n" +
    "                        <td>{{ line.debit_account.balance }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Available Balance:</strong></td>\n" +
    "                        <td>{{ line.debit_account.available_balance }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "                <h4>Destination Bank Account</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Account Number:</strong></td>\n" +
    "                        <td>{{ line.dest_bank_acc.acc_no }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>State:</strong></td>\n" +
    "                        <td>{{ line.dest_bank_acc.state }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Bank Name:</strong></td>\n" +
    "                        <td>{{ line.dest_bank_acc.bank.name }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Verified Bank Name:</strong></td>\n" +
    "                        <td>{{ line.dest_bank_acc.bank_name }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Branch:</strong></td>\n" +
    "                        <td>{{ line.dest_bank_acc.bank.eft_branch_code }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                </table>\n" +
    "                <h4 ng-if=\"isReloadable()\">Reload Payment</h4>\n" +
    "                <table class=\"table table-striped\" ng-if=\"isReloadable()\">\n" +
    "                    <tr>\n" +
    "                        <td>Action Date:</td>\n" +
    "                        <td><input kendo-date-picker ng-model=\"line.action_date\" k-format=\"'yyyy-MM-dd'\" /></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td></td>\n" +
    "                        <td><a class=\"btn btn-primary pull-right\" href=\"\" ng-click=\"reloadPayment();\">Reload Payment Line</a></td>\n" +
    "                    </tr>\n" +
    "                    <tr><td></td><td></td></tr>\n" +
    "                </table>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "    </div>\n" +
    "</div>");
  $templateCache.put("templates/backoffice/views/statement_lines.tpl.html",
    "<div id=\"content\">\n" +
    "    <div class=\"container-fluid\">\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"page-header\">\n" +
    "                    <h2>Statement Lines <small>{{ entry.ref_no }}</small>\n" +
    "                        <a class=\"btn btn-primary pull-right\" href=\"\" ng-click=\"showGrid();\" ng-if=\"selectedLine\">List Statement Lines</a>\n" +
    "                        <div class=\"dropdown pull-right\" ng-if=\"!selectedLine\">\n" +
    "                            <button class=\"btn btn-default\" type=\"button\" id=\"dropdownMenu1\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"true\">\n" +
    "                                Actions\n" +
    "                                <span class=\"caret\"></span>\n" +
    "                            </button>\n" +
    "                            <ul class=\"dropdown-menu\" aria-labelledby=\"dropdownMenu1\">\n" +
    "                                <li><a data-ui-sref=\"app.import_statement\">Import Statement</a></li>\n" +
    "                                <li><a data-ui-sref=\"app.auto_recon\">Run Auto Recon</a></li>\n" +
    "                            </ul>\n" +
    "                        </div>\n" +
    "\n" +
    "                    </h2>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"!selectedLine\">\n" +
    "            <div class=\"col=md-12\">\n" +
    "                <kendo-grid options=\"mainGridOptions\" id=\"grid\"></kendo-grid>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"selectedLine\">\n" +
    "            <div class=\"col-md-6\">\n" +
    "                <h4>Details</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Internal Reference:</strong></td>\n" +
    "                        <td>{{ line.uuid }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Hash:</strong></td>\n" +
    "                        <td>{{ line.hash }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Bank Reference:</strong></td>\n" +
    "                        <td>{{ line.ref_no }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Created:</strong></td>\n" +
    "                        <td>{{ line.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Line Type:</strong></td>\n" +
    "                        <td>{{ line.line_type }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Amount:</strong></td>\n" +
    "                        <td>{{ line.amount }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>State:</strong></td>\n" +
    "                        <td>{{ line.state }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Error Message:</strong></td>\n" +
    "                        <td>{{ line.error_message || 'None' }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "            </div>\n" +
    "            <div class=\"col-md-6\">\n" +
    "                <h4>Bank Account</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Bank Name:</strong></td>\n" +
    "                        <td>{{ line.bank_account.bank }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Account Number:</strong></td>\n" +
    "                        <td>{{ line.bank_account.acc_no }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Branch Code:</strong></td>\n" +
    "                        <td>{{ line.bank_account.branch }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Journal:</strong></td>\n" +
    "                        <td>{{ line.bank_account.journal }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Internal Account:</strong></td>\n" +
    "                        <td><a href=\"\" ng-click=\"goToAccount(line.bank_account.account.acc_no)\">{{ line.bank_account.account.acc_no }} - {{ line.bank_account.account.name }} ({{ line.bank_account.account.available_balance }})</a></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Currency:</strong></td>\n" +
    "                        <td>{{ line.bank_account.currency.code }} ({{ line.bank_account.currency.name }}) {{ line.bank_account.currency.current_rate }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "                <h4>Bank Statement</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Reference Number:</strong></td>\n" +
    "                        <td><a href=\"\" ng-click=\"goToStatement(line.bank_statement.ref_no)\">{{ line.bank_statement.ref_no }}</a></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Created:</strong></td>\n" +
    "                        <td>{{ line.bank_statement.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "                <h4 ng-if=\"allowManualRecon()\">Manual Recon</h4>\n" +
    "                <table class=\"table table-striped\" ng-if=\"allowManualRecon()\">\n" +
    "                    <tr>\n" +
    "                        <td>Account Type:</td>\n" +
    "                        <td><kendo-drop-down-list style=\"width:100%\" k-ng-model=\"accountType\" options=\"accountTypeDropDownOptions\"></kendo-drop-down-list></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td>Account:</td>\n" +
    "                        <td><kendo-drop-down-list style=\"width:100%\" k-ng-model=\"recon.account\" options=\"accountDropDownOptions\"></kendo-drop-down-list></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td>Description:</td>\n" +
    "                        <td><input type=\"text\" class=\"form-control\" style=\"width:100%\" ng-model=\"recon.description\" placeholder=\"Description\" /></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td></td>\n" +
    "                        <td><a class=\"btn btn-primary pull-right\" href=\"\" ng-disabled=\"!(recon.account.acc_no && recon.description)\" ng-click=\"doManualRecon();\">Do Manual Recon</a></td>\n" +
    "                    </tr>\n" +
    "                    <tr><td></td><td></td></tr>\n" +
    "                </table>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\"  ng-if=\"selectedLine\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"header\">\n" +
    "                    <h4>Journal Entry Lines</h4>\n" +
    "                </div>\n" +
    "                <div class=\"content\">\n" +
    "                    <table class=\"table table-striped\">\n" +
    "                        <thead>\n" +
    "                            <tr>\n" +
    "                                <th><strong>Id</strong></th>\n" +
    "                                <th><strong>Name</strong></th>\n" +
    "                                <th><strong>Date Created</strong></th>\n" +
    "                                <th><strong>Account</strong></th>\n" +
    "                                <th class=\"text-right\"><strong>Debit</strong></th>\n" +
    "                                <th class=\"text-right\"><strong>Credit</strong></th>\n" +
    "                                <th class=\"text-right\"><strong>Account Balance</strong></th>\n" +
    "                                <th><strong>State</strong></th>\n" +
    "                            </tr>\n" +
    "                        </thead>\n" +
    "                        <tbody>\n" +
    "                            <tr ng-repeat=\"line in journalEntryLines\">\n" +
    "                                <td><span data-toggle=\"tooltip\" title=\"Ref No: {{ line.ref_no }}\">{{ line.pk }}</span></td>\n" +
    "                                <td>{{ line.name }}</td>\n" +
    "                                <td>{{ line.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                                <td><a href=\"\" ng-click=\"goToAccount(line.account_number)\">{{ line.account_name }}</a></td>\n" +
    "                                <td class=\"text-right\">{{ line.debit }}</td>\n" +
    "                                <td class=\"text-right\">{{ line.credit }}</td>\n" +
    "                                <td class=\"text-right\">{{ line.account_balance }}</td>\n" +
    "                                <td>{{ line.state }}</td>\n" +
    "                            </tr>\n" +
    "                        </tbody>\n" +
    "                    </table>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "            <div class=\"clear\"></div>\n" +
    "        </div>\n" +
    "\n" +
    "    </div>\n" +
    "</div>");
  $templateCache.put("templates/backoffice/views/statements.tpl.html",
    "<div id=\"content\">\n" +
    "    <div class=\"container-fluid\">\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"page-header\">\n" +
    "                    <h2>Bank Statements <small>{{ entry.ref_no }}</small> <a class=\"btn btn-primary pull-right\" href=\"\" ng-click=\"showGrid();\" ng-if=\"selectedStatement\">List Statements</a></h2>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"!selectedStatement\">\n" +
    "            <div class=\"col=md-12\">\n" +
    "                <kendo-grid options=\"mainGridOptions\" id=\"grid\"></kendo-grid>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"selectedStatement\">\n" +
    "            <div class=\"col-md-6\">\n" +
    "                <h4>Statement Details</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Reference Number:</strong></td>\n" +
    "                        <td>{{ statement.ref_no }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Created:</strong></td>\n" +
    "                        <td>{{ statement.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "            </div>\n" +
    "            <div class=\"col-md-6\">\n" +
    "                <h4>Bank Account</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Bank Name:</strong></td>\n" +
    "                        <td>{{ statement.bank_account.bank }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Account Number:</strong></td>\n" +
    "                        <td>{{ statement.bank_account.acc_no }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Branch Code:</strong></td>\n" +
    "                        <td>{{ statement.bank_account.branch }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Journal:</strong></td>\n" +
    "                        <td>{{ statement.bank_account.journal }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Internal Account:</strong></td>\n" +
    "                        <td><a href=\"\" ng-click=\"goToAccount(statement.bank_account.account.acc_no)\">{{ statement.bank_account.account.acc_no }} - {{ statement.bank_account.account.name }} ({{ statement.bank_account.account.balance }})</a></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Currency:</strong></td>\n" +
    "                        <td>{{ statement.bank_account.currency.code }} ({{ statement.bank_account.currency.name }}) {{ statement.bank_account.currency.current_rate }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\"  ng-if=\"selectedStatement\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"header\">\n" +
    "                    <h4>Statement Lines</h4>\n" +
    "                </div>\n" +
    "                <div class=\"content\">\n" +
    "                    <table class=\"table table-striped\">\n" +
    "                        <thead>\n" +
    "                            <tr>\n" +
    "                                <th><strong>Internal Ref</strong></th>\n" +
    "                                <th><strong>Ref No</strong></th>\n" +
    "                                <th><strong>Date Created</strong></th>\n" +
    "                                <th><strong>Line Type</strong></th>\n" +
    "                                <th class=\"text-right\"><strong>Amount</strong></th>\n" +
    "                                <th><strong>State</strong></th>\n" +
    "                            </tr>\n" +
    "                        </thead>\n" +
    "                        <tbody>\n" +
    "                            <tr ng-repeat=\"line in statementLines\">\n" +
    "                                <td><a href=\"\" ng-click=\"goToStatementLine(line.uuid)\">{{ line.uuid }}</a></td>\n" +
    "                                <td>{{ line.ref_no }}</td>\n" +
    "                                <td>{{ line.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                                <td>{{ line.line_type}}</td>\n" +
    "                                <td class=\"text-right\">{{ line.amount }}</td>\n" +
    "                                <td>{{ line.state }}</td>\n" +
    "                            </tr>\n" +
    "                        </tbody>\n" +
    "                    </table>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "            <div class=\"clear\"></div>\n" +
    "        </div>\n" +
    "\n" +
    "    </div>\n" +
    "</div>");
  $templateCache.put("templates/backoffice/views/transactions.tpl.html",
    "<div id=\"content\">\n" +
    "    <div class=\"container-fluid\">\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"page-header\">\n" +
    "                    <h2>Transactions <small>{{ transaction.acc_no }}</small> <a class=\"btn btn-primary pull-right\" href=\"\" ng-click=\"showGrid();\" ng-if=\"selectedTransaction\">List Transactions</a></h2>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"!selectedTransaction\">\n" +
    "            <div class=\"col=md-12\">\n" +
    "                <kendo-grid options=\"mainGridOptions\" id=\"grid\"></kendo-grid>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"selectedTransaction\">\n" +
    "            <div class=\"col-md-6\">\n" +
    "                <h4>General Information</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Ref No:</strong></td>\n" +
    "                        <td>{{ transaction.ref_no }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Buyer Ref:</strong></td>\n" +
    "                        <td>{{ transaction.buyer_ref }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Seller Ref:</strong></td>\n" +
    "                        <td>{{ transaction.seller_ref }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Start Date:</strong></td>\n" +
    "                        <td>{{ transaction.start_date | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Last Activity:</strong></td>\n" +
    "                        <td>{{ transaction.last_activity | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>State:</strong></td>\n" +
    "                        <td>{{ transaction.state }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>State Expiry Date:</strong></td>\n" +
    "                        <td>{{ transaction.state_expiry_date | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Name:</strong></td>\n" +
    "                        <td>{{ transaction.name }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Buyer Notes:</strong></td>\n" +
    "                        <td>{{ transaction.buyer_notes }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Seller Notes:</strong></td>\n" +
    "                        <td>{{ transaction.seller_notes }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Value:</strong></td>\n" +
    "                        <td>{{ transaction.value }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Fee:</strong></td>\n" +
    "                        <td>{{ transaction.fee }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Fee Split:</strong></td>\n" +
    "                        <td>{{ transaction.fee_split }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "\n" +
    "                <h4 ng-if=\"transaction.current_settlement\">Current Settlement</h4>\n" +
    "                <table class=\"table table-striped\" ng-if=\"transaction.current_settlement\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Ref No:</strong></td>\n" +
    "                        <td>{{ transaction.current_settlement.ref_no }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Created:</strong></td>\n" +
    "                        <td>{{ transaction.current_settlement.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Closed:</strong></td>\n" +
    "                        <td>{{ transaction.current_settlement.date_closed | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Settlement Type:</strong></td>\n" +
    "                        <td>{{ transaction.current_settlement.settlement_type }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>State:</strong></td>\n" +
    "                        <td>{{ transaction.current_settlement.state }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Payment Amount:</strong></td>\n" +
    "                        <td>{{ transaction.current_settlement.payment_amount }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Refund Amount:</strong></td>\n" +
    "                        <td>{{ transaction.current_settlement.refund_amount }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "\n" +
    "                <h4 ng-if=\"transaction.current_request\">Current Request</h4>\n" +
    "                <table class=\"table table-striped\" ng-if=\"transaction.current_request\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Ref No:</strong></td>\n" +
    "                        <td>{{ transaction.current_request.ref_no }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Created:</strong></td>\n" +
    "                        <td>{{ transaction.current_request.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Closed:</strong></td>\n" +
    "                        <td>{{ transaction.current_request.date_closed | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Request Type:</strong></td>\n" +
    "                        <td>{{ transaction.current_request.request_type }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>State:</strong></td>\n" +
    "                        <td>{{ transaction.current_request.state }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Amount:</strong></td>\n" +
    "                        <td>{{ transaction.current_request.amount }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "            </div>\n" +
    "\n" +
    "            <div class=\"col-md-6\">\n" +
    "                <h4 ng-if=\"transaction.account\">Account</h4>\n" +
    "                <table class=\"table table-striped\" ng-if=\"transaction.account\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Acc No:</strong></td>\n" +
    "                        <td><a href=\"\" ng-click=\"goToAccount(transaction.account.acc_no)\">{{ transaction.account.acc_no }} - {{ transaction.account.name }} ({{ transaction.account.available_balance }})</a></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Name:</strong></td>\n" +
    "                        <td>{{ transaction.account.name }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Accounting Type:</strong></td>\n" +
    "                        <td>{{ transaction.account.accounting_type }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>State:</strong></td>\n" +
    "                        <td>{{ transaction.account.state }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Created:</strong></td>\n" +
    "                        <td>{{ transaction.account.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Last Activity:</strong></td>\n" +
    "                        <td>{{ transaction.account.last_activity | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "\n" +
    "                <h4>Buyer</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Acc No:</strong></td>\n" +
    "                        <td><a href=\"\" ng-click=\"goToAccount(transaction.buyer.acc_no)\">{{ transaction.buyer.acc_no }} - {{ transaction.buyer.name }} ({{ transaction.buyer.available_balance }})</a></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Name:</strong></td>\n" +
    "                        <td>{{ transaction.buyer.name }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Accounting Type:</strong></td>\n" +
    "                        <td>{{ transaction.buyer.accounting_type }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>State:</strong></td>\n" +
    "                        <td>{{ transaction.buyer.state }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Created:</strong></td>\n" +
    "                        <td>{{ transaction.buyer.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Last Activity:</strong></td>\n" +
    "                        <td>{{ transaction.buyer.last_activity | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "\n" +
    "                <h4>Seller</h4>\n" +
    "                <table class=\"table table-striped\">\n" +
    "                    <tr>\n" +
    "                        <td><strong>Acc No:</strong></td>\n" +
    "                        <td><a href=\"\" ng-click=\"goToAccount(transaction.seller.acc_no)\">{{ transaction.seller.acc_no }} - {{ transaction.seller.name }} ({{ transaction.seller.available_balance }})</a></td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Name:</strong></td>\n" +
    "                        <td>{{ transaction.seller.name }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Accounting Type:</strong></td>\n" +
    "                        <td>{{ transaction.seller.accounting_type }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>State:</strong></td>\n" +
    "                        <td>{{ transaction.seller.state }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Date Created:</strong></td>\n" +
    "                        <td>{{ transaction.seller.date_created | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                    <tr>\n" +
    "                        <td><strong>Last Activity:</strong></td>\n" +
    "                        <td>{{ transaction.seller.last_activity | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                    </tr>\n" +
    "                </table>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "    </div>\n" +
    "</div>");
  $templateCache.put("templates/backoffice/views/users.tpl.html",
    "<div id=\"content\">\n" +
    "    <div class=\"container-fluid\">\n" +
    "\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-md-12\">\n" +
    "                <div class=\"page-header\">\n" +
    "                    <h2>User Profile <small>{{ user_auth.username }}</small> <a class=\"btn btn-primary pull-right\" href=\"\" ng-click=\"showGrid();\" ng-if=\"selectedUser\">List Users</a></h2>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"!selectedUser\">\n" +
    "            <div class=\"col=md-12\">\n" +
    "                <kendo-grid options=\"mainGridOptions\" id=\"grid\"></kendo-grid>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"row\" ng-if=\"selectedUser\">\n" +
    "            <tabset class=\"ui-tabs\">\n" +
    "                <tab heading=\"Information\">\n" +
    "                    <div class=\"container-fluid\">\n" +
    "                        <br>\n" +
    "                        <div class=\"col-md-6\">\n" +
    "                            <h4>General Information</h4>\n" +
    "                            <table class=\"table table-striped\">\n" +
    "                                <tr>\n" +
    "                                    <td width=\"40%\"><strong>User Name:</strong></td>\n" +
    "                                    <td width=\"60%\"><a href=\"\" e-style=\"width: 100%\" onbeforesave=\"updateUsername($data)\" editable-text=\"user_auth.username\">{{ user_auth.username || 'empty' }}</a></td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>First Name:</strong></td>\n" +
    "                                    <td>{{ user_auth.first_name }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Last Name:</strong></td>\n" +
    "                                    <td>{{ user_auth.last_name }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>ID Number:</strong></td>\n" +
    "                                    <td><a href=\"\" e-style=\"width: 100%\" onbeforesave=\"updateIdNo($data)\" editable-text=\"user_profile.id_no\">{{ user_profile.id_no || 'empty' }}</a></td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Passport Number:</strong></td>\n" +
    "                                    <td><a href=\"\" e-style=\"width: 100%\" onbeforesave=\"updatePassportNo($data)\" editable-text=\"user_profile.passport_no\">{{ user_profile.passport_no || 'empty' }}</a></td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Passport Country:</strong></td>\n" +
    "                                    <td><a href=\"\" e-style=\"width: 100%\" onbeforesave=\"updatePassportCountry($data)\" editable-text=\"user_profile.passport_country\">{{ user_profile.passport_country || 'empty' }}</a></td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Date of Birth:</strong></td>\n" +
    "                                    <td>{{ user_profile.dob }}</td>\n" +
    "                                </tr>\n" +
    "                            </table>\n" +
    "\n" +
    "                            <h4>Contact Information</h4>\n" +
    "                            <table class=\"table table-striped\">\n" +
    "                                <tr>\n" +
    "                                    <td width=\"40%\"><strong>Mobile:</strong></td>\n" +
    "                                    <td width=\"60%\">{{ user_profile.mobile }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>E-Mail:</strong></td>\n" +
    "                                    <td>{{ user_auth.email }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Email Secondary:</strong></td>\n" +
    "                                    <td>{{ user_profile.email_secondary }}</td>\n" +
    "                                </tr>\n" +
    "                            </table>\n" +
    "                        </div>\n" +
    "\n" +
    "                        <div class=\"col-md-6\">\n" +
    "                            <h4>User Settings</h4>\n" +
    "                            <table class=\"table table-striped\">\n" +
    "                                <tr>\n" +
    "                                    <td width=\"40%\"><strong>Is Staff:</strong></td>\n" +
    "                                    <td width=\"60%\">{{ user_auth.is_staff }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Is Super User:</strong></td>\n" +
    "                                    <td>{{ user_auth.is_superuser }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Is Active:</strong></td>\n" +
    "                                    <td><a href=\"\" onbeforesave=\"updateIsActive($data)\" editable-checkbox=\"user_auth.is_active\" e-title=\"Is Active?\">{{ user_auth.is_active || 'False' }}</a></td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>SMS Login:</strong></td>\n" +
    "                                    <td>{{ user_profile.sms_login }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>E-Mail Login:</strong></td>\n" +
    "                                    <td>{{ user_profile.email_login }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>SMS Critical:</strong></td>\n" +
    "                                    <td>{{  user_profile.sms_critical }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>E-Mail Critical:</strong></td>\n" +
    "                                    <td>{{  user_profile.email_critical }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>SMS Other:</strong></td>\n" +
    "                                    <td>{{  user_profile.sms_other }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>E-Mail Other:</strong></td>\n" +
    "                                    <td>{{  user_profile.email_other }}</td>\n" +
    "                                </tr>\n" +
    "                            </table>\n" +
    "\n" +
    "                            <h4>Meta Information</h4>\n" +
    "                            <table class=\"table table-striped\">\n" +
    "                                <tr>\n" +
    "                                    <td width=\"40%\"><strong>Date Joined:</strong></td>\n" +
    "                                    <td width=\"60%\">{{ user_auth.date_joined | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Last Login:</strong></td>\n" +
    "                                    <td>{{ user_auth.last_login | date: appVariables.ngDatetimeFormat }}</td>\n" +
    "                                </tr>\n" +
    "                                <tr>\n" +
    "                                    <td><strong>Call Count:</strong></td>\n" +
    "                                    <td>{{ user_profile.call_count }}</td>\n" +
    "                                </tr>\n" +
    "                            </table>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "\n" +
    "                    <div class=\"row\"  ng-if=\"selectedUser\">\n" +
    "                        <div class=\"col-md-12\">\n" +
    "                            <div class=\"header\">\n" +
    "                                <h4>Entities</h4>\n" +
    "                            </div>\n" +
    "                            <div class=\"content\">\n" +
    "                                <table class=\"table table-striped\">\n" +
    "                                    <thead>\n" +
    "                                        <tr>\n" +
    "                                            <th><strong>Entity Name</strong></th>\n" +
    "                                            <th><strong>Entity Type</strong></th>\n" +
    "                                            <th><strong>Telephone</strong></th>\n" +
    "                                            <th><strong>Fax</strong></th>\n" +
    "                                            <th><strong>Email</strong></th>\n" +
    "                                        </tr>\n" +
    "                                    </thead>\n" +
    "                                    <tbody>\n" +
    "                                        <tr ng-repeat=\"entity in entities\">\n" +
    "                                            <td><a href=\"\" ng-click=\"goToEntity(entity.id)\">{{ entity.name }}</a></td>\n" +
    "                                            <td>{{ entity.entity_type }}</td>\n" +
    "                                            <td>{{ entity.telephone }}</td>\n" +
    "                                            <td>{{ entity.fax }}</td>\n" +
    "                                            <td>{{ entity.email }}</td>\n" +
    "                                        </tr>\n" +
    "                                    </tbody>\n" +
    "                                </table>\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                        <div class=\"clear\"></div>\n" +
    "                    </div>\n" +
    "                </tab>\n" +
    "                <tab heading=\"Transactions\">\n" +
    "                    <div class=\"container-fluid\">\n" +
    "                        <br>\n" +
    "                        <h4>Transactions</h4>\n" +
    "                        <kendo-grid  options=\"transactionGridOptions\" id=\"grid2\" name=\"grid2\"></kendo-grid>\n" +
    "                    </div>\n" +
    "                </tab>\n" +
    "            </tabset>\n" +
    "        </div>\n" +
    "\n" +
    "    </div>\n" +
    "</div>");
}]);


});
