/**
 * @fileoverview This file defines our notification module used to
 * show popup notifications.
 */


define([
    'jquery'
], function($) {

    'use strict';

    var popupNotification = null;

    var showNotification = function(message, type) {
        if (!popupNotification) {
            popupNotification = $("#notf1").kendoNotification({
                // See http://docs.telerik.com/kendo-ui/api/javascript/ui/notification for list of settings.
                width: "50em",
                autoHideAfter: 10000
            }).data("kendoNotification");
        }
        popupNotification.show(message, type);
    };

    return {
        info: function(message) {
            showNotification(message, 'info');
        },
        success: function(message) {
            showNotification(message, 'success');
        },
        warning: function(message) {
            showNotification(message, 'warning');
        },
        error: function(message) {
            showNotification(message, 'error');
        }
    }
});