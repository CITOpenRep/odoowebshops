odoo.define('theme_clarico.clarico_script',function(require){
'use strict';
var sAnimations = require('website.content.snippets.animation');
	require('web.dom_ready');
	var wish = new sAnimations.registry.ProductWishlist();
	
	/* ---------- top menu hover dropdown  ---------- */
	// Moved this code from theme_ecommerce.js because it was not executing
	$(function(){
		if ($(window).innerWidth() > 1200) {
		    $("#top_menu > .dropdown").hover(            
	            function() {
	                $('> .dropdown-menu', this).stop( true, true ).fadeIn("slow");
	                $(this).toggleClass('open');
	            },
	            function() {
	                $('> .dropdown-menu', this).stop( true, true ).fadeOut("fast");
	                $(this).toggleClass('open');
	            }
		    );
		}
	});
	/* ---------- Header top when transparent header  ---------- */
	$(window).load(function(){
		var header_before_height = $(".t_header_before_overlay").outerHeight();
		if($("body").find(".o_header_overlay").length > 0)
			{
				$("header:not(.o_header_affix)").addClass("transparent_top")
				$(".transparent_top").css("top",header_before_height);
				$(".o_header_affix.affix").removeClass("transparent_top")
			}
	})
	/*  ---------- Category mega menu ---------- */
	// Moved this code from theme_ecommerce.js because it was not executing
     $("#custom_menu li").each(function(){
 		var has_ctg = $(this).find("ul.t_custom_subctg").length > 0
 		if(has_ctg){
 			$(this).append("<span class='ctg_arrow fa fa-angle-right' />")
 			
 			$(".ctg_arrow").click(function(ev){
 				ev.preventDefault();
 				ev.stopPropagation();
 				var self =$(this).siblings("ul.t_custom_subctg");
 				var ul_index=$(self).parents("ul").length;
 				$(self).stop().animate({
 				        width: "100%"
 				        });
 				$(self).css({"display":"block","transition":"0.3s easeout","z-index":ul_index})
 				$(self).parent().parent(".t_custom_subctg").css("overflow-y","hidden");
 				$(self).parent().parent(".t_custom_subctg").scrollTop(0);
 				$(this).parents("#custom_menu").scrollTop(0);
 				$(this).parents("#custom_menu").css("overflow-y","hidden");
 			})
 			$(this).find("ul.t_custom_subctg").children(".t_prent_ctg_heading").click(function(ev){ 
 				ev.preventDefault();
 				ev.stopPropagation();
 				$(this).parent("ul#custom_recursive").stop().animate({
 			        width: "0"
 			        },function() { 
 			           $(this).css("display","none")
 			           $(this).parent().parent(".t_custom_subctg").css("overflow-y","auto");
 			        }
 				);
 			})	   
 		}
 	})
 	$("#custom_menu > li > ul.t_custom_subctg > .t_prent_ctg_heading").click(function(){
 		 $(this).parents("#custom_menu").css("overflow-y","auto");
 	 })
	
	// Compare Script
	$('.o_product_comparison_table > span').text(function(_, txt) {
	  var min_height = $('#read_more').height();
	  var product_name_height = $('.o_product_comparison_table').height();
			 if(txt.length > 22) {
			 	$(this).attr("id","long_width");
			 	var temp_width = $(this).height();
			  	if(temp_width > 25)
			  	{	
				  	$(this).css({'width':'150px','white-space':'nowrap','overflow':'hidden','line-height':'1'});
					$(this).parents('#read_more').after().append("<a id='expand' href='' class='d-inline-block small'>..More</a>");
					$('#read_more > #expand').click(function(){
				  		if($(this).hasClass("less")) {
						  	$(this).parent().find('span').css({'width':'150px','white-space':'nowrap','overflow':'hidden','line-height':'1'});
				        	$(this).removeClass("less");
				            $(this).html('more');
			        } else {
			        	$(this).parent().find('span').css({'white-space':'unset','width':'100%','line-height':'unset','overflow':'unset'})
			        	$('.morecontent').css({'display':'inline-block'});
			            $(this).addClass("less");
			            $(this).html('less');
			        }
			        $(this).parent().prev().toggle();
			        $(this).prev().toggle();
			        return false;

				  	});
			  }
		}
	});
	
	// Portal script
	if($('div').hasClass('o_portal_my_home'))
	{   
		if(!$('a').hasClass('list-group-item') ) 
		{
			$(".page-header").css({'display':'none'})
		}
	}
	//product script
	$('#t_product_tabs li a:not(:first)').addClass('inactive');
	$('.t_product_tab').hide();
	
	$('#t_product_tabs li').each(function(){
		if(!$(this).find("a").hasClass('inactive'))
			{
			 var t = $(this).find("a").attr('id');
			 $('.'+ t + 'C').fadeIn('slow');
			}
	})
	$('#t_product_tabs li a').click(function(){
	    var t = $(this).attr('id');
	  if($(this).hasClass('inactive')){ 
	    $('#t_product_tabs li a').addClass('inactive');           
	    $(this).removeClass('inactive');
	    
	    $('.t_product_tab').hide();
	    $('.'+ t + 'C').fadeIn('slow');
	 }
	});
	// if slider then active first slide
	if($('.recommended_product_slider_main').length){
		$(".theme_carousel_common").each(function(){
			$(this).find(".carousel-item").first().addClass("active");
		})
	}
	// if compare specification is active then active specification tab
	if($('#product_specifications').length){
		$('.specification_li').addClass("active");
	}
	// if rating is active then rating tab is active
	if($('.o_shop_discussion_rating').length){
		$('.rating_review_li').addClass("active");
	}
	// Change in carousel to display two slide
		$('.theme_carousel_common .carousel-item').each(function(){
			var next = $(this).next();
			if (!next.length) {
				next = $(this).siblings(':first');
			}
			next.children(':first-child').clone().appendTo($(this));
		});

	// shop script
	$(window).load(function(){
		$("form.js_attributes input:checked").each(function(){ 
			var self=$(this);
			var val=this.value;
			// For Radio Type
			var radio_attr = self.parent("label").find("span").html();
			var curr_parent=self.parents("ul");
			var target =  curr_parent.parent("li.nav-item").find("a.clear_all_variant");
			target.css("display","block");
			// For Color Only
			var color_attr = self.parent("label").next(".color-name").html();
			var target_color = self.parents("li.nav-item").find("a.clear_all_variant");
			target_color.css("display","block");
			// Show clear all(at top) link when any attribute is selected on load
			if(target.length >= 0 || target_color.length >=0){
				$(".clear_all_form_selection").css("display","block");
				// If any attributes are selected then show 'View Filter Button'
				$(".view_filter_span").css("display","inline-block");
				// Attribute value are display in view filter dropdown 
				if(radio_attr){
					$(".view_all_filter_inner").append("<div class='attribute'>" + radio_attr + "<a data-id='"+val+"' class='clear_attr_a'>x</a></div>");
				}
				if(color_attr){
					$(".view_all_filter_inner").append("<div class='attribute'>" + color_attr + "<a data-id='"+val+"' class='clear_attr_a'>x</a></div>");
				}
			}else{
				$(".clear_all_form_selection").css("display","none");
			}
			
			// Clear particular selected attribute(checkbox only)
			$(".clear_attr_a").click(function(){        			
				var id=$(this).attr("data-id");
				if(id){        				
					$("form.js_attributes input[value="+id+"]").removeAttr("checked");        				
					$("form.js_attributes input").closest("form").submit();        			
				}
			})
			// Change sequence of selected attribute to top
			var first_li = self.closest("ul").find("li").first();
			var selected_li = self.closest("li.nav-item");
			$(first_li).before(selected_li);
			
			// if any attribute are selected then automatically this section is Expand
			if(!curr_parent.hasClass("open_ul")){
				curr_parent.parent("li.nav-item").find('.t_attr_title').click();
			}
		});
		$("form.js_attributes select").each(function(){
			var self=$(this);
			var val = self.find("option:selected").val();
			var select_attr = self.find("option:selected").html();
			var target_select = self.parents("li.nav-item").find("a.clear_all_variant");
			if(val.length >= 1){
				target_select.css("display","block");
				$(".clear_all_form_selection").css("display","block");
				// If any attributes are selected then show 'View Filter Button'
				$(".view_filter_span").css("display","inline-block");
				// Attribute value are display in view filter dropdown 
				if(target_select){
					$(".view_all_filter_inner").append("<div class='attribute'>" + select_attr + "<a data-id='"+val+"' class='clear_attr_a'>x</a></div>");
				}
				self.parents("li.nav-item").find(".t_attr_title").click();
				
			}
			// Clear particular selected attribute(Selectionbox)
			$(".clear_attr_a").click(function(){        			
				var id=$(this).attr("data-id");
				if(id){        				
					$("form.js_attributes option:selected[value="+id+"]").remove();        				
					$("form.js_attributes input").closest("form").submit();        			
				}
			})
		})
		// Active first attribute section
		$(".t_shop_attr_ul > li.nav-item:first-child").each(function(){
			var self=$(this);
			var ul_main = self.find("ul");
			if (ul_main.length == 1){
				if(!ul_main.hasClass("open_ul")){
					self.find('.t_attr_title').click();
				}
			}
		})
		// Click to appear scrollbar to see all attributes  
		$(".view_more_attr").click(function(){
			var self=$(this);
			var clicks = $(this).data('clicks');
			if (clicks) {
				self.prev('li.nav-item').find("ul").css({"overflow":"hidden"});
				self.animate({"opacity": "0"}, 300, function() {
			        $(this).html("Show More  <i class='fa fa-plus'></i>").animate({ opacity: 1 });
			    });
				
			} else {
				self.prev('li.nav-item').find("ul").css({"overflow-y":"auto"});
				self.animate({"opacity": "0"}, 300, function() {
			        $(this).html("Show Less <i class='fa fa-minus'></i>").animate({ opacity: 1 });
			    });
			}
			$(this).data("clicks", !clicks);
		})
	});
	// Clear individual attributes list
	$(".clear_all_variant").click(function(){
		var self=$(this);
		var curent_div = self.parents("li.nav-item");
		$(curent_div).find("input:checked").each(function(){
			$(this).removeAttr("checked");
		});
		$(curent_div).find("option:selected").each(function(){
			$(this).remove();
		})
		$("form.js_attributes input").closest("form").submit();
	});
	// Clear all attributes(form)
	$(".clear_all_form_selection").click(function(){
		$("form.js_attributes .t_shop_attr_ul > li").each(function(){
			var self=$(this);
			self.find("select option:selected").prop('selected', false);
			self.find("input:checked").prop('checked', false);
		})
		$("form.js_attributes").closest("form").submit();
	});
	// Click Filters to toggle div and show selected attribtues list 
	$(".view_filter_span").click(function(){
		$(".view_all_filter_inner").toggle("slow");
	})
	// Click on color name to also check color checkbox
	$(".color-with-name-divmaxW .color-name").click(function(){
		var self=$(this);
		self.parents("li.color-with-name-divmaxW").find("input").click();
	})
	// Collapse - Expand attribute section
	$(".t_attr_title").click(function(){
		var self=$(this);
		var main_li = self.parents("li.nav-item");
		var ul_H = main_li.find("ul").outerHeight();
		// If attribute type is selection box
		if (main_li.find("select").length == 1){
			var main_select = main_li.find("select");
			main_select.toggle('slow');
			var clicks = $(this).data('clicks');
			if (clicks) {
				self.find("i").removeClass('fa-caret-down').addClass('fa-caret-right');
			} else {
				self.find("i").removeClass('fa-caret-right').addClass('fa-caret-down');
			}
			$(this).data("clicks", !clicks);
			return;
		}
		var main_ul = main_li.find("ul");
		// If attribute type is radio or color
		// Toggle attribute section
		if(main_ul.hasClass("open_ul")){
			main_ul.removeClass("open_ul");
			self.find("i").removeClass('fa-caret-down').addClass('fa-caret-right');
			main_ul.toggle('slow');
			// hide view more
			main_li.next('.view_more_attr').removeClass('active');
			main_li.next('.view_more_attr').css("display","none");
		}else{
			main_ul.addClass("open_ul");
			self.find("i").removeClass('fa-caret-right').addClass('fa-caret-down');
			main_ul.toggle('slow');
			// show view more
			if(ul_H >= 125){
				main_li.next('.view_more_attr').addClass('active');
				main_li.next('.view_more_attr').css("display","block");
			}
		}
	})
	// Hover on product item to active cart,quickview, wishlist
	if ($(window).width() > 1200) {
		$(".oe_grid.oe_product").mouseenter(function(){
			var self=$(this);
			var section_H = self.find("section").outerHeight();
			self.find("section").css('height', + section_H);
			self.find(".product_price").addClass("bottom_animation");
			self.find(".oe_product_image").css({"opacity":"0.2","transition":"1s"});
		});
		$(".oe_grid.oe_product").mouseleave(function(){
			var self=$(this);
			self.find(".product_price").removeClass("bottom_animation")
			self.find(".oe_product_image").css("opacity","1");
		});
	}
	else
		{
			$(".product_price").addClass("bottom_animation");
		}
	//Shop filter slide left responsive
	$('.shop_filter_resp').click(function(){
		$("#products_grid_before").toggleClass("t_filter_slide");
		$("#wrapwrap").toggleClass("wrapwrap_trans");
		$('body').css("overflow-x","hidden");
	});
	$('.filter_close').click(function(){
		$("#products_grid_before").removeClass("t_filter_slide")
		$("#wrapwrap").removeClass("wrapwrap_trans");
	});

	//header style
	$(".t_srch_icon").click(function(){
		 $(".t_search_popover").addClass("visible");
		 $(this).css("display","none");
		 $(".t_srch_close").css("display","block");
	});
	$(".t_srch_close").click(function(){
		$(".t_search_popover").removeClass("visible");
		$(this).css("display","none");
		$(".t_srch_icon").css("display","block");
	});
	$(document).click(function(event) {
	 //if you click on anything except the modal itself or the "open modal" link, close the modal
		 if (!$(event.target).closest(".t_search_popover,.t_srch_icon_header").length) {
			$("body").find(".t_search_popover").removeClass("visible");
			$('.t_srch_close').css("display","none");
			$(".t_srch_icon").css("display","block");
			}
	});
	//Search Animation For Header Style 6
	if ($(".header_style_6_main").length){
		$(".header_6_srch_icon").click(function(){
			$(".t_header_before_right").addClass("search_animate");
			if ($(window).width() < 768) {
				$(".t_header_before_left").addClass("search_animate");
			}
			$(".t_header_search input").css("width","100%");
			setTimeout(function(){
				if ($(window).width() > 768) {
					$(".t_header_before_right").css("display","none");
				}else{
					$(".t_header_before_right").css("display","none");
					$(".t_header_before_left").css("display","none");
				}
				$(".t_header_search").css("display","block");
			}, 500);
		})
		$(".t_header_search_close").click(function(){
			$(".t_header_before_right").removeClass("search_animate").css("display","block");
			$(".t_header_before_left").removeClass("search_animate").css("display","block");
			$(".t_header_search").css("display","none");
			$(".t_header_search input").css("width","0%");
		})
	}
	/*expertise progress bar*/ 
	$(window).load(function(){
	$('.progress').each(function(){ 
		    	var area_val = $(this).find('.progress-bar').attr("aria-valuenow")
		    	$(this).find('.progress-bar').css("max-width",area_val+ "%")
		    })
	})
	

	function recently_view_wishlist(){
		wish.willStart()
        $(self.$target).find(".o_add_wishlist").click(function (event) {
        event.stopImmediatePropagation();
        $(this).prop("disabled", true).addClass('disabled');
        var productId = parseInt( $(this).attr('data-product-product-id'), 10);
        $("[data-product-product-id='"+productId+"']").prop("disabled", true).addClass('disabled');
        if (productId && !_.contains(wish.wishlistProductIDs, productId)) {
	    self._rpc({
	        route: '/shop/wishlist/add',
	        params: {
	            	 product_id: productId,
	            	},
		          }).then(function () {
		        	  wish.wishlistProductIDs.push(productId);
		        	  wish._updateWishlistView();
		              wSaleUtils.animateClone($('#my_wish'), $(this).closest('form'), 25, 40);
		          }).fail(function () {
		             $(this).prop("disabled", false).removeClass('disabled');
		             var wproductId = parseInt( $(this).attr('data-product-product-id'), 10);
		             $("[data-product-product-id='"+wproductId+"']").prop("disabled", false).removeClass('disabled');
		          });
             }
        	})
    }

	/* customer carousel snippet */
	$(document).ready(function(){
		$('#carousel_recently_view .carousel-inner').find("div[data-active=True]").remove();
		if(window.innerWidth <= 992) {
			if($('#carousel_recently_view .carousel-inner > div').length <= 4 && $('#carousel_recently_view .carousel-inner >div').length > 2) {
				$('#carousel_recently_view').addClass('carousel slide common_carousel_emp');
				$('#carousel_recently_view .carousel-inner > div').addClass('carousel-item');
				$( "#carousel_recently_view .carousel-inner" ).after( '<a class="carousel-control-prev" role="button" data-slide="prev" data-target="#carousel_recently_view"><i class="fa fa-chevron-left fa-lg text-muted" /></a><a class="carousel-control-next" role="button" data-slide="next" data-target="#carousel_recently_view"><i class="fa fa-chevron-right fa-lg text-muted" /></a>');
			}
		}
		recently_view_wishlist()
		$('.carousel[data-type="multi"]').each(function() {
			$('.carousel_recently_view').find('.carousel-item:first-child').addClass("active");
			if($('#carousel_recently_view .carousel-inner .carousel-item').length <= 4) {
				$('#carousel_recently_view').attr('data-interval','0');
				$('#carousel_recently_view .carousel-control-prev, #carousel_recently_view  .carousel-control-next').remove();
			}
			else{
				$('#carousel_recently_view').attr('data-interval','10000');
			}
			$('#'+this.id).on('slide.bs.carousel', function (e) {
				var carousel_id =this.id;
				var $e = $(e.relatedTarget);
				var idx = $e.index();
				if(window.innerWidth <= 992){
			        var itemsPerSlide = 2;    
			    }
			    else {
			      var itemsPerSlide = 4;
			    }
				var totalItems = $('#'+carousel_id).find('.carousel-item').length;
				if (idx >= totalItems-(itemsPerSlide-1)) {
				var it = itemsPerSlide - (totalItems - idx);
			        for (var i=0; i<it; i++) {
			        	if (e.direction=="left") {
			            	$(this).find('.carousel-item').eq(i).appendTo($(this).find('.carousel-inner'));
			            }
				        else {
				        	$(this).find('.carousel-item').eq(0).appendTo($(this).find('.carousel-inner'));
				        }
					}
				}
			});
			
			/*$('#'+this.id).carousel ({
			  interval: 10000
			})*/
		});
	})
	sAnimations.registry.WebsiteSale.include({
		/**
		* Adds the stock checking to the regular _onChangeCombination method
		* @override
		*/
		_updateProductImage: function (){
			
		this._super.apply(this, arguments);
		if ($(window).width() > 1200) {
			var el =  $("#product_detail").find(".carousel-indicators").length > 0
			if(el)
			{ 
			 var ol_H =  $("#product_detail").find(".carousel-indicators").prop('scrollHeight');
				 if(ol_H > 435) {
					 $(".t_show_more_multi_img").css({'display':'block'});
				 }
				 $(".t_show_more_multi_img").click(function(){
					 var self=$(this);
					 var clicks = $(this).data('clicks');
					 if (clicks) {
						 $(this).siblings("ol.carousel-indicators").css("overflow","hidden");
						 self.animate({"opacity": "0"}, 300, function() {
						 $(this).html("<i class='fa fa-angle-down'></i>").animate({ opacity: 1 });
					 });	
					 } else {
						 $(this).siblings("ol.carousel-indicators").css("overflow-y","auto");
						 self.animate({"opacity": "0"}, 300, function() {
						 $(this).html("<i class='fa fa-angle-up'></i>").animate({ opacity: 1 });
					 });
					 }
					 $(this).data("clicks", !clicks);
				 })
			}
		}
		}
	});
	/* ------------ quantity design in cart lines when promotion app installed -------------*/
	
	$(".t_cart_table .css_quantity > span").siblings("div").css("display","none")
	
	
});
//product carousel multi image show more
$(window).load(function() {  
	if($('#o-carousel-product > .t_show_more_multi_img').length < 1) {
		if ($(window).width() > 1200) {
			var el =  $("#product_detail").find(".carousel-indicators").length > 0
			if(el)
			{ 
			var ol_H =  $("#product_detail").find(".carousel-indicators").prop('scrollHeight');
				if(ol_H > 435) {
					$('#o-carousel-product').append($('<div class="t_show_more_multi_img"><i class="fa fa-angle-down"></i></div>'));
					$(".t_show_more_multi_img").css({'display':'block'});
				}
				$(".t_show_more_multi_img").click(function(){
					var self=$(this);
					var clicks = $(this).data('clicks');
					if (clicks) {
						$(this).siblings("ol.carousel-indicators").css("overflow","hidden");
						self.animate({"opacity": "0"}, 300, function() {
						$(this).html("<i class='fa fa-angle-down'></i>").animate({ opacity: 1 });
					});	
					} else {
						$(this).siblings("ol.carousel-indicators").css("overflow-y","auto");
						self.animate({"opacity": "0"}, 300, function() {
						$(this).html("<i class='fa fa-angle-up'></i>").animate({ opacity: 1 });
					});
					}
					$(this).data("clicks", !clicks);
				})
			}
		}
	}

	if($('#carousel_recently_view .carousel-inner .img_hover').length >= 1) {
		$('.t_product_recent_h2').css('display','block')
	}
})

