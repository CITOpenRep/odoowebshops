odoo.define('emipro_theme_lazy_load.lazy_load_image', function(require) {
    'use strict';

    require('web.dom_ready');
    
    // Lazy load images on window load
    $(window).load(function() {
        if($('#id_lazyload').length) {
            $("img.lazyload").lazyload();
        }
    });
   
    $('.li-mega-menu').click(function() {
        if($('#id_lazyload').length) {
            $("img.lazyload").lazyload();
        }
    });
});