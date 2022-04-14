odoo.define('category_carousel.editor', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');
var rpc = require('web.rpc');
var weContext = require('web_editor.context');
var web_editor = require('web_editor.editor');
var options = require('web_editor.snippets.options');
var wUtils = require('website.utils');
var _t = core._t;

var snippets_category_carousel = options.Class.extend({
    popup_template_id: "product_category_limit",
    popup_title: _t("Add Category"),
    select_snippet_list: function (previewMode, value) {
        var self = this;
        var def = wUtils.prompt({
            'id': this.popup_template_id,
            'window_title': this.popup_title,
            'select': _t("Limit"),
            'init': function (field) {
                var $group = this.$dialog.find('select');
               // $group.removeClass('mb0');

                var $add = "<option value='10'>10</option><option value='15'>15</option><option value='20'>20</option>"
                $group.append($add);  
            },
        });
        def.then(function (product_list_id) {
        self.$target.attr("data-list-id", product_list_id);

	});
        return def;
    },	
    onBuilt: function () {
        var self = this;
        this._super();
        this.select_snippet_list('click').fail(function () {
            self.getParent()._onRemoveClick($.Event( "click" ));
        });
    },
});
options.registry.category_limit = snippets_category_carousel.extend({
    cleanForSave: function () {
        this.$target.addClass("hidden");
    },
});
});
