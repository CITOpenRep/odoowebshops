odoo.define('theme_clarico.s_editor_js', function (require) {
	'use strict';

	var Dialog = require('web.Dialog');
	var Widget = require('web.Widget');
	var core = require('web.core');
	var rte = require('web_editor.rte');
	var snippetsEditor = require('web_editor.snippet.editor');
	var EditorMenuBar = require("web_editor.editor");
		
    var qweb = core.qweb;
    var ajax = require("web.ajax");

	var _t = core._t;
	var EditorCustomMenuBar = EditorMenuBar.Class.include({
		save: function (reload) {
	        var self = this;
	        var defs = [];
	        $('div,section').removeClass('aos-animate');
	        $("div[data_aos_ept],section[data_aos_ept]").each(function(){
				var data_aos_ept = $(this).attr('data_aos_ept');
				var self = $(this);
				if(data_aos_ept){
	 				$(this).attr('data-aos',data_aos_ept);
					$(this).removeAttr('data_aos_ept');
				}
	    	});
	    
	        this.trigger_up('ready_to_save', {defs: defs});
	        return $.when.apply($, defs).then(function () {
	            self.snippetsMenu.cleanForSave();
	            return self._saveCroppedImages();
	        }).then(function () {
	            return self.rte.save();
	        }).then(function () {
	            if (reload !== false) {
	                return self._reload();
	            }
	        });
	    },
	    
	});
});