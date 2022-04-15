odoo.define('theme_canna.canna', function (require) {
'use strict';
    var sAnimations = require('website.content.snippets.animation');

    sAnimations.registry.limitedEdition = sAnimations.Class.extend({
        selector: '#wrapwrap',
        read_events: {
            'click .limited_edition': '_onClickAddToCart'
        },
         _onClickAddToCart: function (e){
            $('#limitedEditionPopup').modal({backdrop: "static"})
        },
    });
});