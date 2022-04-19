//----------------------------------------------------
// Dynamic Product Slider Snippet
//----------------------------------------------------
odoo.define('clarico_extended.product_slider', function (require) {
    'use strict';

    var ajax = require("web.ajax");
    var rpc = require('web.rpc');
    var wSaleUtils = require('website_sale.utils');
    var sAnimations = require('website.content.snippets.animation');
    var wish = new sAnimations.registry.ProductWishlist();
    var sale = new sAnimations.registry.WebsiteSale();

    sAnimations.registry.js_best_seller = sAnimations.Class.extend({
        selector: ".js_best_seller",
        start: function () {
            this.redrow();
        },
        stop: function () {
            this.clean();
        },
        redrow: function (debug) {
            this.clean(debug);
            this.build(debug);
        },
        clean: function (debug) {
            this.$target.empty();
        },
        build: function (debug) {
            var self = this;
            ajax.jsonRpc('/get_best_seller_data', 'call').then(function (data) {
                $(self.$target).html(data);
                $(self.$target).find(".a-submit").click(function (event) {
                    sale._onClickSubmit(event)
                });
                self.owlCarousel();
                if($('#id_lazyload').length) {
                    $("img.lazyload").lazyload();
                }
            });
        },
        owlCarousel: function() {
            var owl_rtl = false;
            if ($('#wrapwrap').hasClass('o_rtl')) {
                owl_rtl = true;
            }
            $('.best_seller_ept').find('.owl-carousel').owlCarousel({
                loop: true,
                rtl: owl_rtl,
                nav: true,
                dots: false,
                navText : ['<i class="fa fa-chevron-left"></i>','<i class="fa fa-chevron-right"></i>'],
                autoplay: true,
                autoplayTimeout: 4000,
                autoplayHoverPause:true,
                items: 1,
            });
        },
    });
    sAnimations.registry.js_limited_edition = sAnimations.Class.extend({
        selector: ".js_limited_edition",
        start: function () {
            this.redrow();
        },
        stop: function () {
            this.clean();
        },
        redrow: function (debug) {
            this.clean(debug);
            this.build(debug);
        },
        clean: function (debug) {
            this.$target.empty();
        },
        build: function (debug) {
            var self = this;
            ajax.jsonRpc('/get_limited_edition_data', 'call').then(function (data) {
                $(self.$target).html(data);
                $(self.$target).find(".a-submit").click(function (event) {
                    sale._onClickSubmit(event)
                });
                $(self.$target).find(".limited_edition").click(function (event) {
                    event.preventDefault();
                    $('#limitedEditionPopup').modal({backdrop: "static"})
                });
                self.owlCarousel();
                if($('#id_lazyload').length) {
                    $("img.lazyload").lazyload();
                }
            });
        },
        owlCarousel: function() {
            var owl_rtl = false;
            if ($('#wrapwrap').hasClass('o_rtl')) {
                owl_rtl = true;
            }
            $('.limited_edition_ept').find('.owl-carousel').owlCarousel({
                loop: true,
                rtl: owl_rtl,
                nav: true,
                dots: false,
                navText : ['<i class="fa fa-chevron-left"></i>','<i class="fa fa-chevron-right"></i>'],
                autoplay: true,
                autoplayTimeout: 4000,
                autoplayHoverPause:true,
                items: 1,
            });
        },
    });
});
