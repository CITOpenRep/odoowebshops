odoo.define('website_sale_customisation.customisation_script',function (require) {
'use strict';
	require('web.dom_ready');
	var ajax = require('web.ajax');
	var sAnimations = require('website.content.snippets.animation');
	
	
    sAnimations.registry.form_builder_send.include({
        send: function (){
                var area_data = $.trim(this.$target.find('textarea').val());
                this.$target.find('textarea').val(area_data)
                this._super.apply(this, arguments);
            },
    })
	
	// Bind order not comment in checkout process
	$("button#o_payment_form_pay").bind("click", function (ev) {
		var comment = $('#order_comment').val();
	    ajax.jsonRpc('/order_comment', 'call', {
	        'comment': comment
	    })
	});
	
	/* Call size guide json controller */
	$(document).on('click', '.product_size_guide_json', function(event) {
		event.preventDefault();
		$(".cus_theme_loader_layout").removeClass("d-none");
		var product_size_guide_id = $("#size_guide").val();
     	ajax.jsonRpc("/shop/product/size_guide_json", 'call', {'categ_id': product_size_guide_id}).then(function (data) {
        	$(".div_loading_icon").css("display","none");
        	$("body").css('position','fixed');
        	$("body").append(data);
        	$(".cus_theme_loader_layout").addClass("d-none");
        	$(".button_close_product_size_guide").click(function(){
        		$("body").css('position','relative');
        		$("body").find(".div_whole_class_product_size_guide").remove();
        	});
        	$(document).on( 'keydown', function(e){
				if(e.keyCode === 27){
					$("body").css('position','relative');
					$("body").find(".div_whole_class_product_size_guide").remove();
				}
			});
        });	
        /* Clicking on outside the size guide model popup to close model popup */
        $(document).mouseup(function (e){
        	var container = $(".div_main_class_product_size_guide");
            if (!container.is(e.target) && container.has(e.target).length === 0){
            	$("body").css('position','relative');
    			$("body").find(".div_whole_class_product_size_guide").remove();
            }
        });
	});
	
	// Clear cart function
	$(".clear_shopping_cart").click(function (event) {
		event.preventDefault();
		ajax.jsonRpc("/shop/clear_cart", 'call', {})
			.then(function (data) {
				window.location.reload(true);
		});
	});
	
	// Click outside the cart popover to close(hide) that
	$(document).mouseup(function(e){
	    var container = $(".mycart-popover");
	    if (!container.is(e.target) && container.has(e.target).length === 0){
	        container.find(".te_cross").trigger("click");
	    }
	    var container_qw = $(".product_quick_view_class");
	    if (!container_qw.is(e.target) && container_qw.has(e.target).length === 0){
	    	container_qw.find(".qv_close").trigger("click");
	    }
	});
	//  Esc to hide cart popover
	$(document).on( 'keydown', function(e){
		if(e.keyCode === 27){
			if($(".mycart-popover").find(".te_cross").length != 0){
				$(".mycart-popover").find(".te_cross").trigger("click");
			}
			if($(".t_close.qv_close").length != 0){
				$(".t_close.qv_close").trigger("click");
			}
		}
	});
});

/*odoo.define('website_sale_customisation.product_variant_change', function (require) {
	'use strict';
	
    var core = require('web.core');
    var dom = require('web.dom');
    var ajax = require('web.ajax');
    var config = require('web.config');
    var zoomOdoo = require("website.content.zoomodoo");
    var sAnimations = require('website.content.snippets.animation');
    
    sAnimations.registry.variantChange = sAnimations.Class.extend({
    	selector: '.oe_website_sale',
    	read_events: {
			'change .js_variant_change':'_onJSVariantChange',
		},
		
		_onJSVariantChange : function(ev){
			var $this = $(ev.target);
			if($this.hasClass("c_type")){
				
			}else{
				return false;
			}
		}
    })
    
    /*
    
     Use document ready because it need to override the function 
    $(document).ready(function() {
	     This (is_click_control) variable is use when click on carousel control to change product
	     * set value true if you click on carousel control
	     * set value false when trigger variant change  
	    var is_click_control = false;
	    
	    // Product page variant vise image change
		$(".js_product").find('.product_id').on('change', function (event) {
			$(".cus_theme_loader_layout").removeClass("d-none");
			is_click_control = false;
			changeProductImage();
	    	return;
	    })
	        
	    // Change product slider image when change product variant
	    function changeProductImage(){
	    	var $product_id = $("form .js_product .product_id").val();
	    	$(".carousel-indicators li").each(function () {
	    		if($(this).attr("product_product_id") == $product_id){
	    			$(this).trigger('click');
	    		}
	    	})
	    	removeLoader();
	    }
	    
	     click carousel indicators to change product variat and image 
	    $(".o-carousel-product-ept .carousel-indicators li").on('click', function (event) {
	    	$(".cus_theme_loader_layout").removeClass("d-none");
	    	var product_id = $(this).attr("product_product_id");
	    	if (is_click_control == true) {
	    		if (product_id) {
	    			carouselControlClick(product_id);
		    	}
	    	}
	    	if (event.originalEvent === undefined) {
	    		// Click called by code 
	    		removeLoader();
	    		return;
	    	}
	        else{
	        	// Call when is_click_control varaible set 'true'
		    	if (product_id) {
		    		carouselControlClick(product_id);
		    	}
	        }
	    })
	     Common carousel control for thumbnail image or slider arrows  
	    function carouselControlClick(product_id) {
	    	ajax.jsonRpc('/product/variant/change', 'call' , {'product_id':product_id}).then(function (data) {
	    		var attr_ids = data.attribute_value_ids;
	    		if (attr_ids) {
		    		$("ul.js_add_cart_variants li.variant_attribute").each(function () {
		    			var self = $(this)
		    			// For attribute type radio
		    			if (self.find(".radio_type").length != 0) {
		    				self.find(".radio_type li").each(function () {
		    					var self_radio = $(this);
		    					var crr_val = self_radio.find("input").attr("data-value_id");
		    					if (_.contains(attr_ids, parseInt(crr_val)) == true) {
		    						self_radio.find("input").prop("checked","True");
		    					}else{
		    						self_radio.find("input").removeAttr("checked");
		    					}
		    				})
		    			}// For attribute type color
		    			else if (self.find(".color_type").length != 0) {
		    				self.find(".color_type li").each(function () {
		    					var self_color = $(this);
		    					var crr_val = self_color.find("input").attr("data-value_id");
		    					if (_.contains(attr_ids, parseInt(crr_val)) == true) {
		    						self_color.find("input").prop("checked","True");
		    						self_color.find("input").parent(".css_attribute_color").addClass("active")
		    					}else{
		    						self_color.find("input").removeAttr("checked");
		    						self_color.find("input").parent(".css_attribute_color").removeClass("active")
		    					}
		    				})
		    			}// For attribute type selection
		    			else if(self.find("select").length != 0){
		    				self.find("select option").each(function () {
		    					var optionSelected = $(this);
		    					var crr_val = optionSelected.attr("data-value_id");
		    					if (_.contains(attr_ids, parseInt(crr_val)) == true) {
		    						optionSelected.prop("selected","True");
		    					}else{
		    						optionSelected.removeAttr("selected");
		    					}
		    				})
		    			}
		    		})
	    		}
	    		// update the product id
	    		if (data.product_id) {
	    			var $product_id = $("form .js_product .product_id").val(data.product_id || 0);
	    		}
	    		removeLoader();
	    		is_click_control = false;
	    	})
	    }
	    // carousel control (arrow) to change product
	    $(".o-carousel-product-ept .carousel_controls").on('click', function (event) {
	    	is_click_control = true;
	    	var self = $(this);
	    	var slideIndex = $(".carousel-indicators li.active");
	    	if (self.hasClass("carousel-control-prev")) {
	    		if (slideIndex.prev().length) {
	    			slideIndex.prev().click();
	    		}else{
	    			$(".carousel-indicators li:last").click();
	    		}
	    	}else if(self.hasClass("carousel-control-next")) {
	    		if (slideIndex.next().length) { 
	    			slideIndex.next().click();
	    		}else{
	    			$(".carousel-indicators li:first").click();
	    		}
	    	}else{
	    		return;
	    	}
	    })
	     Remove loading icon when removeLoader() function call 
		function removeLoader(){
			setTimeout(function () {
				$(".cus_theme_loader_layout").addClass("d-none");
			}, 500);
		}
	    
	    
    });
    
     Override _startZoom function for change the product carousel trigger
     * Changed into the _updateProductImage function to stop calling the another carousel 
    sAnimations.registry.WebsiteSale.include({
    	_startZoom: function () {
        // Do not activate image zoom for mobile devices, since it might prevent users from scrolling the page
    		if (!config.device.isMobile) {
	            var autoZoom = $('.ecom-zoomable').data('ecom-zoom-auto') || false,
	            factorZoom = parseFloat($('.ecom-zoomable').data('ecom-zoom-factor')) || 0.5,
	            attach = '#o-carousel-product-ept';
	            _.each($('.ecom-zoomable img[data-zoom]'), function (el) {
	                onImageLoaded(el, function () {
	                    var $img = $(el);
	                    if (!_.str.endsWith(el.src, el.dataset.zoomImage) || // if zoom-img != img
	                        el.naturalWidth >= $(attach).width() * factorZoom || el.naturalHeight >= $(attach).height() * factorZoom) {
	                        $img.zoomOdoo({event: autoZoom ? 'mouseenter' : 'click', attach: attach});
	                        $img.attr('data-zoom', 1); // add cursor (if previously removed)
	                    } else {
	                        $img.removeAttr('data-zoom'); // remove cursor
	                        // remove zooming but keep the attribute because
	                        // it can potentially be set back
	                        $img.attr('data-zoom-image', '');
	                    }
	                });
	            });
	        }
	
	        function onImageLoaded(img, callback) {
	            // On Chrome the load event already happened at this point so we
	            // have to rely on complete. On Firefox it seems that the event is
	            // always triggered after this so we can rely on it.
	            //
	            // However on the "complete" case we still want to keep listening to
	            // the event because if the image is changed later (eg. product
	            // configurator) a new load event will be triggered (both browsers).
	            $(img).on('load', function () {
	                callback();
	            });
	            if (img.complete) {
	                callback();
	            }
	            //attach = '#o-carousel-product-ept';
	        }
	    },
	    _updateProductImage: function ($productContainer, productId, productTemplateId, new_carousel) {
	        var $img;
	        var $carousel = $productContainer.find('#o-carousel-product-ept');
	        if (new_carousel) {
	            // When using the web editor, don't reload this or the images won't
	            // be able to be edited depending on if this is done loading before
	            // or after the editor is ready.
	        }
	        else { // compatibility 12.0
	            var model = productId ? 'product.product' : 'product.template';
	            var modelId = productId || productTemplateId;
	            var imageSrc = '/web/image/{0}/{1}/image'
	                .replace("{0}", model)
	                .replace("{1}", modelId);

	            $img = $productContainer.find('img.js_variant_img');
	            $img.attr("src", imageSrc);
	            $img.parent().attr('data-oe-model', model).attr('data-oe-id', modelId)
	                .data('oe-model', model).data('oe-id', modelId);

	            var $thumbnail = $productContainer.find('img.js_variant_img_small');
	            if ($thumbnail.length !== 0) { // if only one, thumbnails are not displayed
	                $thumbnail.attr("src", "/web/image/{0}/{1}/image/90x90"
	                    .replace('{0}', model)
	                    .replace('{1}', modelId));
	                $('.carousel').carousel(0);
	            }

	            // reset zooming constructs
	            $img.filter('[data-zoom-image]').attr('data-zoom-image', $img.attr('src'));
	            if ($img.data('zoomOdoo') !== undefined) {
	                $img.data('zoomOdoo').isReady = false;
	            }
	        }
	        $carousel.toggleClass('css_not_available', !this.isSelectedVariantAllowed);
	    },
    });*/

