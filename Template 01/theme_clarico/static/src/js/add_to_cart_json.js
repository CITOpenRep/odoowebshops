odoo.define('theme_clarico.add_to_cart_json', function (require) {
'use strict';

var sAnimations = require('website.content.snippets.animation');

sAnimations.registry.ajaxAddToCart = sAnimations.Class.extend({
    selector: '.oe_website_sale',
    read_events: {
        'click .add_to_cart_json': '_onModalSubmit',
    },

    init: function (){
        this._super.apply(this, arguments);
    },

    _onModalSubmit: function (e){
        $('.cus_theme_loader_layout').removeClass('d-none');
        debugger
        var product_id = $('#quick_view_model_shop:visible').length ? parseInt($('#quick_view_model_shop .js_product .product_id').val()) : parseInt($('#product_details .js_product .product_id').val())
        product_id = !product_id ? parseInt($(e.currentTarget).prev().val()) : product_id
        var product_qty = $('#quick_view_model_shop:visible').length ? 1 : parseInt($('.js_product .quantity').val())
        this._rpc({
            route: "/shop/cart/update_json",
            params: {
                product_id: product_id,
                add_qty: product_qty,
                display: false,
            },
        }).then(function (resp) {
            $('.cus_theme_loader_layout').addClass('d-none');
            if (resp.warning) {
                if (! $('#data_warning').length) {
                    $('.wishlist-section').prepend('<div class="mt16 alert alert-danger alert-dismissable" role="alert" id="data_warning"></div>');
                }
                var cart_alert = $('.wishlist-section').parent().find('#data_warning');
                cart_alert.html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + resp.warning);
            }
            var product_name = $('#quick_view_model_shop:visible').length ? $('.t_product_name').html().trim() : $('.te_product_name').html().trim()
            $('.my_cart_quantity').html(resp.cart_quantity || '<i class="fa fa-warning" /> ');
            if($('.my_cart_quantity').hasClass('badge-primary')) {
                $('.my_cart_quantity').toggleClass('badge-primary badge-success')
            }
            if($('#quick_view_model_shop').length){
                $('.quick_close').click()
            }
            $(".popup_product_name").html(product_name)
            //$('.te_cart_icon_head').after('<div class="modal fade" id="conformCart" tabindex="-1" role="dialog"><div class="modal-dialog modal-sm modal-dialog-centered" role="document"><div class="modal-content text-center"><div class="modal-header"><h5 class="modal-title">'+product_name+'</h5></div><div class="modal-body"><p>You added <b>'+product_name+'</b> to your shopping cart..</p></div><div class="p-3"><button type="button" class="btn btn-primary w-100" data-dismiss="modal">Continue Shopping</button><button type="button" class="btn btn-primary w-100 mt8" onclick="location.href='+"'/shop/cart'"+'">Process Checkout <span class="fa fa-chevron-right ml-2"></span></button></div></div></div></div>')
            $('#conformCart').modal({backdrop: "static"})
            $('#conformCart').on('hidden.bs.modal', function (e) {
               // $('#conformCart').modal('dispose')
                $('#conformCart').hide()
            })
        });
    },

});



});
