odoo.define('theme_clarico.snippetEpt', function (require) {
	'use strict';
	
	var core = require('web.core');
	var Dialog = require('web.Dialog');
	var Widget = require('web.Widget');
	var summernoteCustomColors = require('web_editor.rte.summernote_custom_colors');
	var weWidgets = require('web_editor.widget');
	var SnippetOption = require('web_editor.snippets.options');
	
	var qweb = core.qweb;
	var _t = core._t;
			
	var registry = {};

	var ept = SnippetOption.Class.include({
		selectClass: function (previewMode, value, $opt) {
	        var $group = $opt && $opt.closest('.dropdown-submenu');
	        if (!$group || !$group.length) {
	            $group = this.$el;
	        }
	        var $lis = $group.find('[data-select-class]').addBack('[data-select-class]');
	        var classes = $lis.map(function () {return $(this).data('selectClass');}).get().join(' ');
	
	        this.$target.removeClass(classes);
	        if (value) {
	        	var data_aos_ept = this.$target.attr('data_aos_ept');
	        	var data_aos = this.$target.attr('data-aos');
	        	
	        	if(data_aos_ept){
		            this.$target.addClass(value);
		            this.$target.attr('data_aos_ept',value);
		        }
		        else if(data_aos){
		        	this.$target.addClass(value);
		            this.$target.attr('data-aos',value);
		        }
		        else{
		            this.$target.addClass(value);
		            this.$target.attr('data_aos_ept',value);
		        }
		    }
	    },
	});
	/*expertise progress bar*/ 
	$(window).load(function(){
	$('.progress').each(function(){ 
		    	var area_val = $(this).find('.progress-bar').attr("aria-valuenow")
		    	$(this).find('.progress-bar').css("max-width",area_val+ "%")
		    })
	})
});