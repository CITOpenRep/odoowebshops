odoo.define('theme_clarico.ecommerce', function(require) {
    'use strict';

    require('web.dom_ready');
    var core = require('web.core');
    var sAnimations = require('website.content.snippets.animation');
    var utils = require('web.utils');
    var ajax = require('web.ajax');
    var dom = require('web.dom');
    var sAnimation = require('website.content.snippets.animation');
    var ProductConfiguratorMixin = require('sale.ProductConfiguratorMixin');
    var sale = new sAnimation.registry.WebsiteSale();
    var _t = core._t;

    // Quick view js script
    $("a.quick-view-a").click(function() {
        var pid = $(this).attr('data-id');
        pid = pid;
        $('.cus_theme_loader_layout').removeClass('d-none');
        ajax.jsonRpc('/productdata', 'call', {'product_id':pid}).then(function(data) 
        	{
        	$('.cus_theme_loader_layout').addClass('d-none');
            $(".mask_cover").append(data) 
            $(".mask").fadeIn();
            sale.init();
            $('.cus_theme_loader_layout').addClass('hidden');
            $(".mask_cover").css("display", "block");
            $("[data-attribute_exclusions]").on('change', function(event) {
                sale.onChangeVariant(event)
            })
            $("[data-attribute_exclusions]").trigger('change')
           $(".css_attribute_color input").click(function(event){ 	
					sale._onChangeColorAttribute(event)
				})
            $(".a-submit").click(function(event) {
                sale._onClickSubmit(event)
            }) 
            $(".qv_close").click(function() {
                $('.mask_cover').empty(data);
            });
        });
    });

  

	$(".t_custom_submenu").parent("li.nav-item").addClass("dropdown");
	$(".t_custom_submenu").siblings("a.nav-link").addClass("dropdown-toggle").attr("data-toggle","dropdown");
	$(".static_menu").parent("li.nav-item").css("position","static");

	sAnimation.registry.affixMenu = sAnimation.Class.extend({
	    selector: 'header.o_affix_enabled',

	    /**
	     * @override
	     */
	    start: function () {
	        var def = this._super.apply(this, arguments);
	        if (this.editableMode) {
	            return def;
	        }
	        
	        var self = this;
	        this.$headerClone = this.$target.clone().addClass('o_header_affix affix').removeClass('o_affix_enabled');
	        this.$headerClone.insertAfter(this.$target);
	        this.$headers = this.$target.add(this.$headerClone);
	        this.$dropdowns = this.$headers.find('.dropdown');
	        this.$navbarCollapses = this.$headers.find('.navbar-collapse');

	        // Handle events for the collapse menus
	        _.each(this.$headerClone.find('[data-toggle="collapse"]'), function (el) {
	            var $source = $(el);
	            var targetIDSelector = $source.attr('data-target');
	            var $target = self.$headerClone.find(targetIDSelector);
	            $source.attr('data-target', targetIDSelector + '_clone');
	            $target.attr('id', targetIDSelector.substr(1) + '_clone');
	        });

	        // Window Handlers
	        $(window).on('resize.affixMenu scroll.affixMenu', _.throttle(this._onWindowUpdate.bind(this), 200));
	        setTimeout(this._onWindowUpdate.bind(this), 0); // setTimeout to allow override with advanced stuff... see themes
	        
	      
			/*------------- static mega menu snippets --------------*/
			$(".cat-column").mouseenter(function(){
				var self = $(this);
				self.addClass('opacity-full');
				var button_cat = $(self).find('a#btn_categary');
				button_cat.addClass('menu-cate-hover');
				$('.cat-column').addClass('opacity');
			});
			
			$(".cat-column").mouseleave(function(){
				var self = $(this);
				var button_cat = $(self).find('a#btn_categary');
				button_cat.removeClass('menu-cate-hover');
				$('.cat-column').removeClass('opacity');
				self.removeClass('opacity-full');
			});
	        return def;
	    },
	    /**
	     * @override
	     */
	    destroy: function () {
	        if (this.$headerClone) {
	            this.$headerClone.remove();
	            $(window).off('.affixMenu');
	        }
	        this._super.apply(this, arguments);
	    },

	    //--------------------------------------------------------------------------
	    // Handlers
	    //--------------------------------------------------------------------------

	    /**
	     * Called when the window is resized or scrolled -> updates affix status and
	     * automatically closes submenus.
	     *
	     * @private
	     */
	    _onWindowUpdate: function () {
	        var wOffset = $(window).scrollTop();
	        var hOffset = this.$target.scrollTop();
	        this.$headerClone.toggleClass('affixed', wOffset > (hOffset + 300));

	        // Reset opened menus
	        this.$dropdowns.removeClass('show');
	        this.$navbarCollapses.removeClass('show').attr('aria-expanded', false);
	    },
	});
	//Scroll up 
	$(window).scroll(function(){
		if ($(this).scrollTop() > 300) {
			$('.scrollup-div').fadeIn();
		} else {
			$('.scrollup-div').fadeOut();
		}
	}); 
	
	$('.scrollup-div').click(function(){
		$("html, body").animate({ scrollTop: 0 }, 1000);
	});
	//dropdown menu slidedown
	
	  $( '.dropdown' ).on( 'show.bs.dropdown', function() {
		    $( this ).find( '.dropdown-menu' ).first().stop( true, true ).slideDown( 150 );
		  });
		  $('.dropdown').on( 'hide.bs.dropdown', function(){
		    $( this ).find( '.dropdown-menu' ).first().stop( true, true ).slideUp( 150 );
		  });
	
	// Price filter
		/*	$('form.js_attributes .price_filter_main input').unbind();

		    

			$("#price_range_min_value,#price_range_max_value").on('change', function () {

			 

			  var min_price_range = parseFloat($("#price_range_min_value").val());

			  var max_price_range = parseFloat($("#price_range_max_value").val());

			  if (min_price_range > max_price_range) {
				$('#price_range_max_value').val(min_price_range);
			  }

			  $("#slider-range").slider({
				values: [min_price_range, max_price_range]
			  });
			  
			});


			$("#price_range_min_value,#price_range_max_value").on("paste keyup", function () {                                        

			  $('#price-range-submit').show();

			  var min_price_range = parseFloat($("#price_range_min_value").val());

			  var max_price_range = parseFloat($("#price_range_max_value").val());
			  
			  if(min_price_range == max_price_range){

					max_price_range = min_price_range + 1;
					
					$("#price_range_min_value").val(min_price_range);		
					$("#price_range_max_value").val(max_price_range);
			  }

			  $("#slider-range").slider({
				values: [min_price_range, max_price_range]
			  });

			});

			 var min_pricee = parseFloat($("#price_range_min_value").val());
			  var max_pricee =parseFloat($("#price_range_max_value").val());
			$(function () {
			  $("#slider-range").slider({
				range: true,
				orientation: "horizontal",
				  min: min_pricee,
				  max: max_pricee,
				  values: [min_pricee, max_pricee],
				  step: 1,

				slide: function (event, ui) {
				  if (ui.values[0] == ui.values[1]) {
					  return false;
				  }
				  
				  $("#price_range_min_value").val(ui.values[0]);
				  $("#price_range_max_value").val(ui.values[1]);
				}
			  });

			  $("#price_range_min_value").val($("#slider-range").slider("values", 0));
			  $("#price_range_max_value").val($("#slider-range").slider("values", 1));

			});

			$("#slider-range,#price-range-submit").click(function () {
				$('form.js_attributes').submit()	
			  var min_price = $('#price_range_min_value').val();
			  var max_price = $('#price_range_max_value').val();

			  $("#searchResults").text("Here List of products will be shown which are cost between " + min_price  +" "+ "and" + " "+ max_price + ".");
			});
*/
});
