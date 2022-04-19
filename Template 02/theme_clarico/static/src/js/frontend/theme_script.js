/**************************************************
		01. Header Menu
		02. Search in Header
		03.	Page Scroll up
		04. Theme Wishlist
		05. Shop Events
		06. cart Popover
		07. Product Offer Timer
		08. Price Filter 
		09. Theme layout
		10. Multi Item Carousel
**************************************************/
odoo.define('theme_emipro.theme_script', function(require) {
    'use strict';
 
    var sAnimations = require('website.content.snippets.animation');
    var Widget = require('web.Widget');
    var core = require('web.core');
    var _t = core._t
    var ProductConfiguratorMixin = require('sale.ProductConfiguratorMixin');  
    var ajax = require('web.ajax');
    var wish = new sAnimations.registry.ProductWishlist();
    var wSaleUtils = require('website_sale.utils');
    
    
    $('.te_canna_offer_header').fadeOut('fast');





    //Quick View Script
    function quickview(){
          $("a.quick-view-a").click(function(ev) {
                ev.preventDefault()
                self = this;
                var element = ev.currentTarget;
                var product_id = $(element).attr('data-id');
                $('.cus_theme_loader_layout').removeClass('d-none');
                ajax.jsonRpc('/productdata', 'call',{'product_id':product_id}).then(function(data) {
                var sale = new sAnimations.registry.WebsiteSale();
                $('.cus_theme_loader_layout').addClass('d-none');
                if($("#wrap").hasClass('js_sale')) {
                $("#quick_view_model_shop .modal-body").html(data);
                $("#quick_view_model_shop").modal({keyboard: true});
                } else {
                $("#quick_view_model .modal-body").html(data);
                $("#quick_view_model").modal({keyboard: true});
                }
                var WebsiteSale = new sAnimations.registry.WebsiteSale();
                WebsiteSale.init();
                $("[data-attribute_exclusions]").on('change', function(event) {
                    WebsiteSale.onChangeVariant(event)
                })
                $("[data-attribute_exclusions]").trigger('change')
                if ($(window).width() > 767) {
                if($('.carousel .vertical .carousel-item').length > 5) {
                $('.carousel .vertical .carousel-item').each(function(){
                var next = $(this).next();

                if (!next.length) {
                next = $(this).siblings(':first');
                }
                next.children(':first-child').clone().appendTo($(this));

                for (var i=1;i<4;i++) {
                next=next.next();
                if (!next.length) {
                next = $(this).siblings(':first');
                }
                next.children(':first-child').clone().appendTo($(this));
                }
                });
                } else {
                $('.carousel .vertical .carousel-item').each(function(){
                $(this).addClass("active");
                })
                $(".carousel-control-up, .carousel-control-down").addClass("d-none");
                }
                } else {
                $("#carousel-pager .vertical").addClass("carousel-indicators");
                }

                $(".css_attribute_color input").click(function(event){
                sale._onChangeColorAttribute(event)
                })
                $('.variant_attribute .list-inline-item').first().addClass('active_li');
                $(".variant_attribute li").each(function() {
                if($(this).find('.css_attribute_color').hasClass('active')) {
                $(this).parent('.list-inline-item').addClass('active_li');
                }
                });

                $( ".list-inline-item .css_attribute_color" ).change(function() {
                $('.list-inline-item').removeClass('active_li');
                $(this).parent('.list-inline-item').addClass('active_li');
                });

              });
           });
    	};
    //------------------------------------------
    // 01. Header Menu
    //------------------------------------------
    sAnimations.registry.themeMenu = sAnimations.Class.extend({
        selector: '#top_menu',
        read_events: {
            'mouseenter .cat-column': '_onMouseColEnter',
            'mouseleave .cat-column': '_onMouseColLeave',
        },
        _onMouseColEnter: function(ev) {
            var self = ev.currentTarget;
            $(self).addClass('opacity-full');
            var button_cat = $(self).find('a#btn_categary');
            button_cat.addClass('menu-cate-hover');
            $('.cat-column').addClass('opacity');
        },
        _onMouseColLeave: function(ev) {
            var self = ev.currentTarget;
            var button_cat = $(self).find('a#btn_categary');
            button_cat.removeClass('menu-cate-hover');
            $('.cat-column').removeClass('opacity');
            $(self).removeClass('opacity-full');
        },
    });
    //------------------------------------------
    // 02. Search in Header
    //------------------------------------------
    sAnimations.registry.themeSearch = sAnimations.Class.extend({
        selector: '#wrapwrap',
        read_events: {
            'click .te_srch_icon': '_onSearchClickOpen',
            'click .te_srch_close': '_onSearchClickClose',
            'click .te_offer_close': '_onOfferClose',
        },
        _onOfferClose: function(ev) {
            $('.te_canna_offer_header').addClass("d-none");
        },
        _onSearchClickOpen: function(ev) {
            var self = ev.currentTarget;
            //style1
            if ($(".te_header_1_right").length) {
                $(".te_search_popover").addClass("visible");
                $(self).css("display", "none");
                $(".te_srch_close").css("display", "block");
            }
            //style 2 3 and 4 resp view
            if ($(window).width() < 768) {
                if ($(".te_header_style_2_right").length || $(".te_header_3_search").length || $(".te_header_style_4_inner_first").length) {
                    $(".te_search_popover").addClass("visible");
                    $(self).css("display", "none");
                    $(".te_srch_close").css("display", "block");
                }
            }
            //style5
            if ($(".te_header_5_search").length) {
                $(".te_search_5_form").addClass("open_search");
                var $h_menu = $("#oe_main_menu_navbar").height();
                $(".te_search_5_form").css({
                    top: $h_menu + 0
                });
            }
            //style6
            if ($(".te_header_6_srch_icon").length) {  	
            	$(".te_header_before_right").addClass("search_animate");
    			if ($(window).width() < 768) {
    				$(".te_header_before_left").addClass("search_animate");
    			}
    			$(".te_header_search input").css("width","100%");
    			setTimeout(function(){
    				if ($(window).width() > 768) {
    					$(".te_header_before_right").css("display","none");
    				}else{
    					$(".te_header_before_right").css("display","none");
    					$(".te_header_before_left").css("display","none");
    				}
    				$(".te_header_search").css("display","block");
    			}, 500);
            }
            //style7
            if ($(".te_searchform__popup").length) {
                $(".te_searchform__popup").addClass("open");
                $(".te_srch_close").css("display", "block");
            }
        },
        _onSearchClickClose: function(ev) {
            var self = ev.currentTarget;
            //style1
            if ($(".te_header_1_right").length) {
                $(".te_search_popover").removeClass("visible");
                $(self).css("display", "none");
                $(".te_srch_icon").css("display", "block");
            }
            //style 2 and 3 resp view
            if ($(window).width() < 768) {
                if ($(".te_header_style_2_right").length || $(".te_header_3_search").length || $(".te_header_style_4_inner_first").length) {
                    $(".te_search_popover").removeClass("visible");
                    $(self).css("display", "none");
                    $(".te_srch_icon").css("display", "block");
                }
            }
            //style5
            if ($(".te_header_5_search").length) {
                $(".te_search_5_form").removeClass("open_search");
                $(".te_search_icon_5").css("display", "inline-block");
            }
            //style6
            if ($(".te_header_6_srch_icon").length) {
                $(".te_header_before_right").removeClass("search_animate").css("display", "block");
                $(".te_header_search").css("display", "none");
                $(".te_header_search input").css("width", "0%");
                $(".te_srch_icon").css("display", "inline-block")
            }
            //style7
            if ($(".te_searchform__popup").length) {
                $(".te_searchform__popup").removeClass("open");
                $(".te_srch_icon").css("display", "block");
            }
        },
    });
    //------------------------------------------
    // 03. Page Scroll up
    //------------------------------------------
    sAnimations.registry.themeLayout = sAnimations.Class.extend({
        selector: '.o_footer',
        read_events: {
            'click .scrollup-div': '_onClickAnimate',
        },
        _onClickAnimate: function(ev) {
            $("html, body").animate({
                scrollTop: 0
            }, 1000);
        },
    });
    //------------------------------------------
    // 04. Theme Wishlist
    //------------------------------------------
    sAnimations.registry.themeWishlist = sAnimations.Class.extend({
        selector: '#o_comparelist_table',
        read_events: {
            'click .o_wish_rm': '_onRemoveClick',
        },
        _onRemoveClick: function(ev) {
            var ajax = require('web.ajax');
            var tr = $(ev.currentTarget).parents('tr');
            var wish = tr.data('wish-id');
            var route = '/shop/wishlist/remove/' + wish;
            ajax.jsonRpc(route, 'call', {
                'wish': wish
            }).then(function(data) {
                $(tr).hide();
                if ($('.t_wish_table tr:visible').length == 0) {
                    window.location.href = '/shop';
                }
                if (data) {
                    $('.my_wish_quantity').text(data);
                }
            })
        },

    });
    //------------------------------------------
    // 05. Shop Events
    //------------------------------------------
    sAnimations.registry.themeEvent = sAnimations.Class.extend({
        selector: '.oe_website_sale',
        read_events: {
//            'mouseenter .oe_grid.oe_product': '_onMouseEnter',
//            'mouseleave .oe_grid.oe_product': '_onMouseLeave',
//            'click .oe_product':'_onIcons',
            'click .te_clear_attr_a': '_onClearAttribInd',
            'click .te_clear_all_form_selection': '_onClearAttribAll',
            'click .te_clear_all_variant': '_onClearAttribDiv',
            'click .te_attr_title': '_onAttribSection',
            'click .te_view_more_attr': '_onViewMore',
            'click .te_view_filter_span': '_onFilterToogle',
            'click .te_shop_filter_resp': '_onRespFilter',
            'click .te_filter_close': '_onFilterClose',
            'click .te_color-name':'_oncolorattr',
           
        },

   
        /*_onMouseEnter: function(ev) {
            var self = ev.currentTarget;
            var height = $(self).find("section").outerHeight();
            if ($(window).width() > 1200) {
            	$(self).find("section").css('height', +height);
            	$(self).find(".product_price").addClass("bottom_animation");
            }	
        },
        _onMouseLeave: function(ev) {
            var self = ev.currentTarget;
            if ($(window).width() > 1200) {
                $(self).find(".product_price").removeClass("bottom_animation");
            }
        },
        _onIcons: function(ev){
            var self = ev.currentTarget;
            if ($(window).width() > 1200) {
            $(self).find(".product_price").removeClass("bottom_animation")
            $(self).find(".oe_product_image").css("opacity", "1");
            }
        },*/
        _onClearAttribInd: function(ev) {
            var self = ev.currentTarget;
            var id = $(self).attr("data-id");
            if (id) {
                $("form.js_attributes option:selected[value=" + id + "]").remove();
                $("form.js_attributes").find("input[value=" + id + "]").removeAttr("checked");
            }
            ajaxorformload(ev);
        },
        _onClearAttribAll: function(ev) {
            $("form.js_attributes select").val('');
            $("form.js_attributes").find("input:checked").removeAttr("checked");
            $(".te_reset").trigger('click')
            ajaxorformload(ev);
        },
        _onClearAttribDiv: function(ev) {
            var self = ev.currentTarget;
            var curent_div = $(self).parents("li.nav-item");
            var curr_divinput = $(curent_div).find("input:checked");
            var curr_divselect = $(curent_div).find("option:selected");
            _.each(curr_divselect, function(ev) {
                $(curr_divselect).remove();
            });
            _.each(curr_divinput, function(ev) {
                $(curr_divinput).removeAttr("checked");
            });
            ajaxorformload(ev);
        },
        _onAttribSection: function(ev) {
            var self = ev.currentTarget;
            var main_li = $(self).parents("li.nav-item");
            var ul_H = main_li.find("ul").outerHeight();

            if (main_li.find("select").length == 1) {
                var main_select = main_li.find("select");
                main_select.toggle('slow');
                var clicks = $(this).data('clicks');
                if (clicks) {
                    $(self).find("i").removeClass('fa-caret-down').addClass('fa-caret-right');
                } else {
                    $(self).find("i").removeClass('fa-caret-right').addClass('fa-caret-down');
                }
                $(this).data("clicks", !clicks);
                return;
            }
            var main_ul = main_li.find("ul");

            if (main_ul.hasClass("open_ul")) {
                main_ul.removeClass("open_ul");
                $(self).find("i").removeClass('fa-caret-down').addClass('fa-caret-right');
                main_ul.toggle('slow');

                main_li.find('.te_view_more_attr').removeClass('active');
                main_li.find('.te_view_more_attr').css("display", "none");
            } else {
                main_ul.addClass("open_ul");
                $(self).find("i").removeClass('fa-caret-right').addClass('fa-caret-down');
                main_ul.toggle('slow');

                if (ul_H >= 125) {
                    main_li.find('.te_view_more_attr').addClass('active');
                    main_li.find('.te_view_more_attr').css("display", "block");
                }
            }
        },
        _onViewMore: function(ev) {
            var self = ev.currentTarget;
            var clicks = $(self).data('clicks');
            if (clicks) {
                $(self).parent('li.nav-item').find("ul").css({
                    "overflow": "hidden"
                });
                $(self).animate({
                    "opacity": "0"
                }, 300, function() {
                    $(this).html("Show More  <i class='fa fa-plus'></i>").animate({
                        opacity: 1
                    });
                });

            } else {
                $(self).parent('li.nav-item').find("ul").css({
                    "overflow-y": "auto"
                });
                $(self).animate({
                    "opacity": "0"
                }, 300, function() {
                    $(this).html("Show Less <i class='fa fa-minus'></i>").animate({
                        opacity: 1
                    });
                });
            }
            $(self).data("clicks", !clicks);
        },
        _onFilterToogle: function(ev) {
            $(".te_view_all_filter_inner").toggle("slow");
        },
        _onRespFilter: function(ev) {
            $("#products_grid_before").toggleClass("te_filter_slide");
            $("#wrapwrap").toggleClass("wrapwrap_trans");
            $('body').css("overflow-x", "hidden");
        },
        _onFilterClose: function(ev) {
            $("#products_grid_before").removeClass("te_filter_slide")
            $("#wrapwrap").removeClass("wrapwrap_trans");
        },
        _oncolorattr: function(ev){
			var self=ev.currentTarget;
			 $(self).parents("li.color-with-name-divmaxW").find("input").click();
		},
    });
    /*---- Shop Functions ------*/
    //function for ajax form load
    function ajaxorformload(ev) {
        var ajax_load = $(".ajax_loading").val();
        if (ajax_load == 'True') {
            ajaxform(ev);
        } else {
            $("form.js_attributes input,form.js_attributes select").closest("form").submit();
        }
    }
    //function for ajax form submission
    function ajaxform(ev) {
        $('.cus_theme_loader_layout').removeClass('d-none');
        var url = window.location.pathname;
        var frm = $('.js_attributes')
        url = url + "?" + frm.serialize();
        window.history.pushState({}, "", url);
        var ajax = require('web.ajax');
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                var data_replace = null;
                data_replace = $(data).find('.row.mt-3');
                $(".row.mt-3").replaceWith(data_replace);
                data_replace = $(data).find('.products_pager:first');
                $(".products_pager:first").replaceWith(data_replace);
                data_replace = $(data).find('.products_pager:last');
                $(".products_pager:last").replaceWith(data_replace);
                data_replace = $(data).find('.shop_filter_resp');
                $(".shop_filter_resp").replaceWith(data_replace);
                onShowClearVariant();
                quickfilter();
                priceFilter();
                quickview();
                $('.cus_theme_loader_layout').addClass('d-none');
                $('.cus_theme_loader_layout').addClass('hidden')

            },
            error: function(data) {
                console.log('An error occurred.');
            },
        });
    }
    sAnimations.registry.WebsiteSale.include({
		/**
		* Adds the stock checking to the regular _onChangeCombination method
		* @override
		*/
		_updateProductImage: function (){
			
		this._super.apply(this, arguments);
		if ($(window).width() > 768) {
			if($('.carousel .vertical .carousel-item').length > 4)
				{
					$('.carousel .vertical .carousel-item').each(function(){
						  var next = $(this).next();
					
						  if (!next.length) {
						    next = $(this).siblings(':first');
						  }
						  next.children(':first-child').clone().appendTo($(this));
						  
						  for (var i=1;i<3;i++) {
						    next=next.next();
						    if (!next.length) {
						    	next = $(this).siblings(':first');
						  	}					    
						    next.children(':first-child').clone().appendTo($(this));
						  }							
					});
				}
			else
				{
					$('.carousel .vertical .carousel-item').each(function(){
						$(this).addClass("active");
					})
					$(".carousel-control-up, .carousel-control-down").addClass("d-none");
				}

			}
		else
			{
				$("#carousel-pager .vertical").addClass("carousel-indicators");
			}
		}, 	
    	
    	_onChangeAttribute: function(ev) {
            if (!ev.isDefaultPrevented()) {
                ev.preventDefault();
                var ajax_load = $(".ajax_loading").val();
                if (ajax_load == 'True') {
                    ajaxform(ev);
                    this._delegateEvents();
                } else {
                    $(ev.currentTarget).closest("form").submit();
                }
            }
        },
    });
    function onShowClearVariant(ev) {
        $("form.js_attributes input:checked, form.js_attributes select,form.js_attributes input#price_default_slider_min").each(function() {
            var self = $(this);
            var type = ($(self).context);
            var type_value;
            var attr_value;
            var target_select;
            var curr_parent;
            var target_select = self.parents("li.nav-item").find("a.te_clear_all_variant");
            if ($(type).is("input:checked")) {
                type_value = this.value;
                attr_value = self.parent("label").find("span").html();
                curr_parent = self.parents("ul");
                target_select = curr_parent.parent("li.nav-item").find("a.te_clear_all_variant");
                if (self.parent("label").hasClass("css_attribute_color")) {
                    attr_value = self.parent("label").next(".te_color-name").html();
                }
                var first_li = self.closest("ul").find("li").first();
                var selected_li = self.closest("li.nav-item");
                $(first_li).before(selected_li);
                if (!curr_parent.hasClass("open_ul")) {
                    curr_parent.parent("li.nav-item").find('.te_attr_title').click();
                }
            } else if ($(type).is("select")) {
                type_value = self.find("option:selected").val();
                attr_value = self.find("option:selected").html();
                target_select = self.parents("li.nav-item").find("a.te_clear_all_variant");
            }
            else if ($(type).is("input") && $(type).attr('id') == 'price_default_slider_min') {
                var get_min_val = parseInt($('input#price_default_slider_min').val());
                var get_max_val = parseInt($('input#price_default_slider_max').val());
                var current_min_val = parseInt($('input#price_range_min_value').val());
                var current_max_val = parseInt($('input#price_range_max_value').val());
                if(current_min_val != get_min_val || current_max_val != get_max_val) {
                $(".te_view_filter_span").css("display", "inline-block");
                        $(".te_view_all_filter_inner").append("<div class='attribute'>" + " "+current_min_val+' - '+current_max_val+"<a data-id='" + type_value + "' class='te_clear_attr_a te_reset'>x</a></div>");

                }
            }
            if (type_value) {
                target_select.css("display", "inline-block");
                $(".te_clear_all_form_selection").css("display", "block");
                $(".te_view_filter_span").css("display", "inline-block");
                if (target_select) {
                    $(".te_view_all_filter_inner").append("<div class='attribute'>" + attr_value + "<a data-id='" + type_value + "' class='te_clear_attr_a'>x</a></div>");
                }
            }
        });
    }

    function showDropdown() {
        $(".te_custom_submenu").parent("li.nav-item").addClass("dropdown");
        $(".te_custom_submenu").siblings("a.nav-link").addClass("dropdown-toggle").attr("data-toggle", "dropdown");
        $(".static_menu").parent("li.nav-item").css("position", "static");

       //Scroll up 
        $(window).scroll(function() {
            if ($(this).scrollTop() > 300) {
                $('.scrollup-div').fadeIn();
            } else {
                $('.scrollup-div').fadeOut();
            }
        });
        $('.dropdown').on('show.bs.dropdown', function() {
            $(this).find('.dropdown-menu').first().stop(true, true).slideDown(150);
        });
        $('.dropdown').on('hide.bs.dropdown', function() {
            $(this).find('.dropdown-menu').first().stop(true, true).slideUp(150);
        });
    }

    function quickfilter() {
        $(".te_quick_filter_dropdown_menu form ul > li").each(function() {
            var filter_height = $(this).outerHeight();
            if (filter_height >= 220) {
                $(this).next('.te_view_more_attr').css("display", "inline-block");
            }
        });
        if ($(window).width() > 991.98) {
            $(".te_quick_filter_dropdown").click(function() {
                $(".te_quick_filter_dropdown_menu").slideToggle(500);
                $(".te_quick_filter_dropdown_menu li").each(function() {

                    var filter_height = $(this).find(".open_ul").outerHeight();
                    if (filter_height >= 180) {
                        $(this).find('.te_view_more_attr').css("display", "block");
                    }
                })
            })
            /* When attributes are not in quick filter */
            function isEmpty(el) {
                return !$.trim(el.html())
            }
            if (!isEmpty($('.te_quick_filter_ul'))) {
                $(".te_quick_filter_dropdown").css("display", "block");
            }
        } else {
            $(".te_quick_filter_res").click(function() {
                $(".te_quick_filter_dropdown_menu").addClass("te_open");
                $("#products_grid_before").scrollTop(0);
                $(".te_quick_filter_dropdown_menu li").each(function() {
                    var filter_height = $(this).find(".open_ul").outerHeight();
                    if (filter_height >= 180) {
                        $(this).find('.te_view_more_attr').css("display", "block");
                    }
                })
            })
            $('.te_filter_btn_close').click(function() {
                $(".te_quick_filter_dropdown_menu").removeClass("te_open");
            });

            /* When attributes are not in responsive quick filter */
            function isEmpty(el) {
                return !$.trim(el.html())
            }
            if (isEmpty($('.te_quick_filter_ul'))) {
                $(".te_quick_filter_res").css("display", "none");
            }
        }
    }
    $(window).load(function() {
        onShowClearVariant();
        quickfilter();
        priceFilter();
        quickview();
        showDropdown();
        productDiscountTimer();
    });
    
    //------------------------------------------
    // 06. cart Popover
    //------------------------------------------
    var timeout;
    sAnimations.registry.websiteSaleCartLink = sAnimations.Class.extend({
        selector: ' a#my_cart[href$="/shop/cart"]',
        read_events: {
            'click': '_onClickCart',
        },
        start: function() {
            var def = this._super.apply(this, arguments);
            //var def
            if (this.editableMode) {
                return def;
            }
            this.$el.popover({
                trigger: 'manual',
                animation: true,
                html: true,
                title: function() {
                    return _t("My Cart");
                },
                container: 'body',
                placement: 'right',
                template: '<div class="popover mycart-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="te_cross">X</div><div class="popover-body"></div></div>'
            });
            return def;
        },
        _onClickCart: function(ev) {
            if ($(window).width() > 1000) {
                ev.preventDefault();
                var self = this;
                clearTimeout(timeout);
                $(this.selector).not(ev.currentTarget).popover('hide');
                timeout = setTimeout(function() {
                    if ($('.mycart-popover:visible').length) {
                        return;
                    }
                    ajax.jsonRpc('/shop/cart/popover', 'call').then(function (data) {
                    	self.$el.data("bs.popover").config.content = data;
                        self.$el.popover("show");
                        $(".mycart-popover").addClass("te_open");
                        $("#wrapwrap").addClass("te_overlay");
                        $(".te_cross").click(function() {
                            self.$el.popover("hide");
                            $(".mycart-popover").removeClass("te_open");
                            $("#wrapwrap").removeClass("te_overlay");
                        });
                    })
                }, 100);
            }
        },
    });
    //------------------------------------------
    // 07. Product Offer Timer
    //------------------------------------------
    function productDiscountTimer(ev) {
    var start_date = $(".te_product_start_date").text();
    var count_start_date = new Date(start_date).getTime();

    var enddate = $(".te_product_end_date").text();
    var count_end_date = new Date(enddate).getTime();
    var product_offer;

    var p = setInterval(function() {
        var current_date = new Date().getTime();

        if (count_start_date <= current_date && count_end_date >= current_date) {
            var duration = count_end_date - current_date;
            product_offer = true;
        } else {
            product_offer = false;
        }
        if (duration > 0) {
            var days = Math.floor(duration / (1000 * 60 * 60 * 24));
            var hours = Math.floor((duration % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((duration % (1000 * 60)) / 1000);

            if ((seconds + '').length == 1) {
                seconds = "0" + seconds;
            }
            if ((days + '').length == 1) {
                days = "0" + days;
            }
            if ((hours + '').length == 1) {
                hours = "0" + hours;
            }
            if ((minutes + '').length == 1) {
                minutes = "0" + minutes;
            }
        }
        // If the count down is over, write some text
        if (duration <= 0) {
            clearInterval(p);
            seconds = "00";
            days = "00";
            minutes = "00";
            hours = "00";
            $('.te_display_end_date').empty();
        }
        if (product_offer == true) {
            $(".te_offer_timer_prod").css("display", "block");
            $(".product_offer_timer").remove();
            var append_date = "<div class='product_offer_timer'><span class='text-center d-inline-block'><div class='rounded_digit_product'><span id='days' class='d-block  te_days_hr_min_sec'>" + days + "</span><span id='time_lbl' class='d-block'>Days</span></div></span><span class='text-center d-inline-block'><div class='rounded_digit_product'><span id='hours' class='d-block  te_days_hr_min_sec'>" + hours + "</span><span id='time_lbl' class='d-block'>Hrs</span></div></span><span class='text-center d-inline-block'><div class='rounded_digit_product'><span id='minutes' class='d-block te_days_hr_min_sec'>" + minutes + "</span><span id='time_lbl' class=' d-block'>Mins</span></div></span><span class='text-center d-inline-block'><div class='rounded_digit_product'><span id='seconds' class='d-block te_days_hr_min_sec'>" + seconds + "</span><span id='time_lbl' class='d-block'>Secs</span></div></span></div>";
            $(".te_display_end_date").append(append_date);
        }
    }, 1000);
    }
    // 08. Price Filter
    //--------------------------------------------------------------------------
    //min and max values
    function priceFilter(ev) {
        if ($(".price_filter_main_div").length) {
            var get_min_val = $('input#price_default_slider_min').val();
            var get_max_val = $('input#price_default_slider_max').val();
            $("span.min-amount").html(parseInt(get_min_val));
            $("span.max-amount").html(parseInt(get_max_val));
            var current_min_val = $('input#price_range_min_value').val();
            var current_max_val = $('input#price_range_max_value').val();

            // Prevent Form From Getting Submit on change event of attributes
            $('input#priceRangeLower, input#price_range_min_value').change(function(ev) {
                ev.preventDefault();
                return false;
            })
            $('input#priceRangeUpper, input#price_range_max_value').change(function(ev) {
                ev.preventDefault();
                return false;
            })
            /* Allow only numbers and "." in calculator input fields */
            $.fn.inputFilter = function(inputFilter) {
                return this.on("input keydown keyup mousedown mouseup select contextmenu drop", function() {
                    if (inputFilter(this.value)) {
                        this.oldValue = this.value;
                        this.oldSelectionStart = this.selectionStart;
                        this.oldSelectionEnd = this.selectionEnd;
                    } else if (this.hasOwnProperty("oldValue")) {
                        this.value = this.oldValue;
                        this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
                    }
                });
            };
            $(".filter-price input#price_range_min_value, .filter-price input#price_range_max_value").inputFilter(function(value) {
                return /^-?\d*[0-9]?\d*$/.test(value);
            });
            //validations
            $("#price_slider_form").click(function() {
                $('span#submit-error').removeClass("price_error_message");
                $('span#submit-error').html("");
                $('#price_range_min_value').css({
                    'border-color': 'inherit',
                    'background': '#ffffff'
                });
                $('#price_range_max_value').css({
                    'border-color': 'inherit',
                    'background': '#ffffff'
                });

                if ($("#price_range_min_value").val() == "" || $("#price_range_min_value").val() < parseInt(get_min_val) || $("#price_range_min_value").val() > parseInt(get_max_val)) {
                    $('#price_range_min_value').css({
                        'border-color': 'red',
                        'background': '#f2dede'
                    });
                    $('span#submit-error').addClass("price_error_message");
                    $('span#submit-error').html("Invalid Input");
                    return false
                }

                if ($("#price_range_max_value").val() == "" || $("#price_range_max_value").val() < parseInt(get_min_val) || $("#price_range_max_value").val() > parseInt(get_max_val)) {
                    $('#price_range_max_value').css({
                        'border-color': 'red',
                        'background': '#f2dede'
                    });
                    $('span#submit-error').addClass("price_error_message");
                    $('span#submit-error').html("Invalid Input");
                    return false
                }

                if (parseFloat($("#price_range_max_value").val()) <= parseFloat($("#price_range_min_value").val())) {
                    $('span#submit-error').addClass("price_error_message");
                    $('span#submit-error').html("Minimum amount can't be more or equal to maximum amount");
                    return false
                } else {
                    ajaxorformload(ev);
                }
            })
            /* Change price range slider to change into the input box
             * Also change the value if price result is active */
            var lowerSlider = document.querySelector('#priceRangeLower');
            var upperSlider = document.querySelector('#priceRangeUpper');

            document.querySelector('#price_range_max_value').value = parseInt(upperSlider.value);
            document.querySelector('#price_range_min_value').value = parseInt(lowerSlider.value);

            var lowerVal = parseInt(current_min_val);
            var upperVal = parseInt(current_max_val);
            upperSlider.oninput = function() {
                lowerVal = parseInt(lowerSlider.value);
                upperVal = parseInt(upperSlider.value);
                if (upperVal < lowerVal + 4) {
                    lowerSlider.value = upperVal - 4;
                    if (lowerVal == lowerSlider.min) {
                        upperSlider.value = 4;
                    }
                }
                if (parseInt(this.value) <= lowerVal) {
                    $('span#submit-error').addClass("price_error_message");
                    $('span#submit-error').html("Maximum amount can't be less or equal to minimum amount");
                    document.querySelector('#price_range_max_value').value = lowerVal
                } else {
                    $('span#submit-error').removeClass("price_error_message").html('');
                    document.querySelector('#price_range_max_value').value = parseInt(this.value)
                }
            };

            lowerSlider.oninput = function() {
                lowerVal = parseInt(lowerSlider.value);
                upperVal = parseInt(upperSlider.value);
                if (lowerVal > upperVal - 4) {
                    upperSlider.value = lowerVal + 4;
                    if (upperVal == upperSlider.max) {
                        lowerSlider.value = parseInt(upperSlider.max) - 4;
                    }
                }
                if (parseInt(this.value) >= upperVal) {
                    $('span#submit-error').addClass("price_error_message");
                    $('span#submit-error').html("Minimum amount can't be more or equal to maximum amount");
                    document.querySelector('#price_range_min_value').value = upperVal
                } else {
                    $('span#submit-error').removeClass("price_error_message").html('');
                    document.querySelector('#price_range_min_value').value = parseInt(this.value)
                }
            };

            lowerSlider.value = lowerVal;
            upperSlider.value = upperVal;

            /* Reset button */
                if(current_min_val != get_min_val || current_max_val != get_max_val) {
                    $(".price_filter_head").find(".te_reset").css("display","block");

                    $(".te_reset").click(function(){
                        $('input#price_range_min_value').val(get_min_val);
                        $('input#price_range_max_value').val(get_max_val);
                        //$("form.js_attributes").submit();
                        ajaxorformload(ev);
                    })
                }
        }
    }
        
        //slider main event
        /*$("#Slider1").slider({
            from:10,
            to:75,
            step: 1,
            smooth: true,
            round: 0,
            dimension: " $",
            skin: "round",
            onstatechange: function(value){
            var set_val=value.split(";");
                $('input#price_range_min_value').val(set_val[0])
                $('input#price_range_max_value').val(set_val[1])
        }}); */
       
       //$("#Slider1").slider('value',parseInt($('input#price_range_min_value').val()),parseInt($('input#price_range_max_value').val()))
      
    // }

    //------------------------------------------
    // 09. Theme layout
    //------------------------------------------
    $(window).load(function() {
        //Top menu hover dropdown
        if ($(window).innerWidth() > 1200) {
            $("#top_menu > .dropdown").each(function() {
                if (!$(this).closest(".o_extra_menu_items").length) {
                    $(this).closest("a").click(function() {
                        return false;
                    });
                    $(this).hover(
                        function() {
                            $('> .dropdown-menu', this).stop(true, true).fadeIn("slow");
                            $(this).toggleClass('open');
                        },
                        function() {
                            $('> .dropdown-menu', this).stop(true, true).fadeOut("fast");
                            $(this).toggleClass('open');
                        }
                    );
                }
            })
        }
        //shop icon responsive
        else
        {
			$(".product_price").addClass("bottom_animation");
		}
        //extra menu dropdown
        $('.o_extra_menu_items .dropdown-menu').css("display", "none")
        $('li.o_extra_menu_items .dropdown').click(function(event) {
            event.stopImmediatePropagation();
            $(this).find(".dropdown-menu").slideToggle();
        });
        //Header top when transparent header
        var header_before_height = $(".te_header_before_overlay").outerHeight();
        if ($("body").find(".o_header_overlay").length > 0) {
            $("header:not(.o_header_affix)").addClass("transparent_top")
            $(".transparent_top").css("top", header_before_height);
            $(".o_header_affix.affix").removeClass("transparent_top")
        }
        //Category mega menu
        $("#custom_menu li").each(function() {
            var has_ctg = $(this).find("ul.t_custom_subctg").length > 0
            if (has_ctg) {
                $(this).append("<span class='ctg_arrow fa fa-angle-right' />")
                $(".ctg_arrow").click(function(ev) {
                    ev.preventDefault();
                    ev.stopPropagation();
                    var self = $(this).siblings("ul.t_custom_subctg");
                    var ul_index = $(self).parents("ul").length;
                    $(self).stop().animate({
                        width: "100%"
                    });
                    $(self).css({
                        "display": "block",
                        "transition": "0.3s easeout",
                        "z-index": ul_index
                    })
                    $(self).parent().parent(".t_custom_subctg").css("overflow-y", "hidden");
                    $(self).parent().parent(".t_custom_subctg").scrollTop(0);
                    $(this).parents("#custom_menu").scrollTop(0);
                    $(this).parents("#custom_menu").css("overflow-y", "hidden");
                })
                $(this).find("ul.t_custom_subctg").children(".te_prent_ctg_heading").click(function(ev) {
                    ev.preventDefault();
                    ev.stopPropagation();
                    $(this).parent("ul#custom_recursive").stop().animate({
                        width: "0"
                    }, function() {
                        $(this).css("display", "none")
                        $(this).parent().parent(".t_custom_subctg").css("overflow-y", "auto");
                    });
                })
            }
        })
        $("#custom_menu > li > ul.t_custom_subctg > .te_prent_ctg_heading").click(function() {
            $(this).parents("#custom_menu").css("overflow-y", "auto");
        })
        //Changed search form action in theme's search when website search is installed
        if ($("body").find(".website_search_form_main").length > 0) {
            $(".te_header_search,.te_searchform__popup").each(function() {
                $(this).find("form").attr("action", "/search-result");
            })
            $(".website_search_form_main").html("");
        }
        //Recently viewed title
        if ($('#carousel_recently_view .carousel-inner .img_hover').length >= 1) {
            $('.te_product_recent_h2').css('display', 'block')
        }
        //expertise progress bar
        $('.progress').each(function() {
            var area_val = $(this).find('.progress-bar').attr("aria-valuenow")
            $(this).find('.progress-bar').css("max-width", area_val + "%")
        })
        //Remove images in extra menu
        $("li.o_extra_menu_items").find("img").removeAttr("src alt");

            //product script
    $('#te_product_tabs li a:not(:first)').addClass('inactive');
    $('.te_product_tab').hide();

    $('#te_product_tabs li').each(function() {
        if (!$(this).find("a").hasClass('inactive')) {
            var t = $(this).find("a").attr('id');
            $('.' + t + 'C').fadeIn('slow');
        }
    })
    $('#te_product_tabs li a').click(function() {
        var t = $(this).attr('id');
        if ($(this).hasClass('inactive')) {
            $('#te_product_tabs li a').addClass('inactive');
            $(this).removeClass('inactive');

            $('.te_product_tab').hide();
            $('.' + t + 'C').fadeIn('slow');
        }
    });
    if ($('#product_specifications').length) {
        $('.specification_li').addClass("active");
    }
    if ($('.o_shop_discussion_rating').length) {
        $('.rating_review_li').addClass("active");
    }
    // if slider then active first slide
    if ($('.recommended_product_slider_main').length) {
        $(".theme_carousel_common").each(function() {
            $(this).find(".carousel-item").first().addClass("active");
        })
    }
    // Change in carousel to display two slide
    $('.theme_carousel_common .carousel-item').each(function() {
        var next = $(this).next();
        if (!next.length) {
            next = $(this).siblings(':first');
        }
        next.children(':first-child').clone().appendTo($(this));
        quickview()
    });
    // quantity design in cart lines when promotion app installed
    $(".te_cart_table .css_quantity > span").siblings("div").css("display", "none")
    // Portal script
    if ($('div').hasClass('o_portal_my_home')) {
        if (!$('a').hasClass('list-group-item')) {
            $(".page-header").css({
                'display': 'none'
            })
        }
    }
    var owl_rtl = false;
    if ($('#wrapwrap').hasClass('o_rtl')) {
        owl_rtl = true;
    }
    var myCarousel_acce_prod = $('.alternative_product_main .owl-carousel').owlCarousel({
        loop: false,
        rewind: true,
        rtl: owl_rtl,
        margin: 10,
        nav: true,
        dots: false,
        autoplay: true,
        autoplayTimeout: 4000,
        navText : ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
        autoplayHoverPause:true,
        items: 4,
        responsive: {
            0: {
                items: 1,
            },
            576: {
                items: 2,
            },
            991: {
                items: 3,
            },
            1200: {
                items: 4,
            }
        }
    });

    /*OWL carousel for recently viewed products*/
    var myCarousel_recently_view_prod = $('#carousel_recently_view .owl-carousel').owlCarousel({
        loop: false,
        rewind: true,
        rtl: owl_rtl,
        margin: 10,
        nav: true,
        dots: false,
        autoplay: true,
        autoplayTimeout: 4000,
        navText : ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
        autoplayHoverPause:true,
        items: 4,
        responsive: {
            0: {
                items: 1,
            },
            576: {
                items: 2,
            },
            991: {
                items: 3,
            },
            1200: {
                items: 4,
            }
        }
    });

    })

    function recently_view_wishlist(){
		wish.willStart()
        $(".o_add_wishlist").click(function (event) {
        event.stopImmediatePropagation();
        $(this).prop("disabled", true).addClass('disabled');
        var productId = parseInt( $(this).attr('data-product-product-id'), 10);
        $("[data-product-product-id='"+productId+"']").prop("disabled", true).addClass('disabled');
        if (productId && !_.contains(wish.wishlistProductIDs, productId)) {
	    ajax.jsonRpc('/shop/wishlist/add', 'call',{product_id: productId}).then(function () {
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
    
    //------------------------------------------
    // 10. Multi Item Carousel
    //------------------------------------------
    $(document).ready(function() {
        $('#carousel_recently_view .carousel-inner').find("div[data-active=True]").remove();

        if (window.innerWidth <= 992) {
            if ($('#carousel_recently_view .carousel-inner > div').length <= 4 && $('#carousel_recently_view .carousel-inner >div').length > 2) {
                $('#carousel_recently_view').addClass('carousel slide common_carousel_emp');
                $('#carousel_recently_view .carousel-inner > div').addClass('carousel-item');
                $("#carousel_recently_view .carousel-inner").after('<a class="carousel-control-prev" role="button" data-slide="prev" data-target="#carousel_recently_view"><i class="fa fa-chevron-left fa-lg text-muted" /></a><a class="carousel-control-next" role="button" data-slide="next" data-target="#carousel_recently_view"><i class="fa fa-chevron-right fa-lg text-muted" /></a>');
            }
        }
        recently_view_wishlist()
        $('.carousel[data-type="multi"]').each(function() {
            $('.carousel_recently_view').find('.carousel-item:first-child').addClass("active");
            if ($('#carousel_recently_view .carousel-inner .carousel-item').length <= 4) {
                $('#carousel_recently_view').attr('data-interval', '0');
                $('#carousel_recently_view .carousel-control-prev, #carousel_recently_view  .carousel-control-next').remove();
            } else {
                $('#carousel_recently_view').attr('data-interval', '10000');
            }
            $('#' + this.id).on('slide.bs.carousel', function(e) {
                var carousel_id = this.id;
                var $e = $(e.relatedTarget);
                var idx = $e.index();
                if (window.innerWidth <= 992) {
                    var itemsPerSlide = 2;
                } else {
                    var itemsPerSlide = 4;
                }
                var totalItems = $('#' + carousel_id).find('.carousel-item').length;
                if (idx >= totalItems - (itemsPerSlide - 1)) {
                    var it = itemsPerSlide - (totalItems - idx);
                    for (var i = 0; i < it; i++) {
                        if (e.direction == "left") {
                            $(this).find('.carousel-item').eq(i).appendTo($(this).find('.carousel-inner'));
                        } else {
                            $(this).find('.carousel-item').eq(0).appendTo($(this).find('.carousel-inner'));
                        }
                    }
                }
            });
        });
    })
});
