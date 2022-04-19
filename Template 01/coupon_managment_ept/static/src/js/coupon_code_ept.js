odoo.define('coupon_managment_ept.coupon', function(require) {
    'use strict';

    require('web.dom_ready');
    var ajax = require('web.ajax');

    // To update url
    var urlSearchParams = new URLSearchParams(window.location.search);
    var params = Object.fromEntries(urlSearchParams.entries());
    if(params.hasOwnProperty('code_not_available')) {
        window.history.pushState({}, document.title, document.URL.split('?')[0]);
    }

    // Remove Discount line from sale order
    $("a.js_remove_product_ept").click(function(e) {
        var $input = $(e.currentTarget).closest('div').find('.js_quantity_ept');
        $('.cus_theme_loader_layout').removeClass('d-none')
        ajax.jsonRpc('/shop/cart/update_json', 'call', {
            'line_id':parseInt($input.data('line-id')),
            'product_id': parseInt($input.data('product-id'), 10),
            'set_qty': 0
        }).then(function(data) {
            $( "form[name='coupon_code'] input[name='promo']" ).val('')
            $( "form[name='coupon_code']" ).submit();
        });
    });
});