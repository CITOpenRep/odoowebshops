odoo.define('clarico_extended.clarico_extended_scripts', function(require) {
    "use strict";
    var sAnimations = require('website.content.snippets.animation');
    var dom = require('web.dom');
    var ajax = require('web.ajax');
    var core = require('web.core');

    sAnimations.registry.themeHeaderSearch = sAnimations.Class.extend({
        selector: '#wrapwrap',
        read_events: {
            'click .te_srch_icon': '_onSearchClickToOpen',
            'click .te_srch_close': '_onSearchClickToClose',
        },
         _onSearchClickToOpen: function(ev) {
            var self = ev.currentTarget;
            //style8
            if ($(".te_header_8_right").length) {
                if ( !$('header.o_affix_enabled.te_header_canna').hasClass('start-sticky') ) {
                    $('header.o_affix_enabled.te_header_canna').addClass('start-sticky');
                }
                if ($(window).width() < 768) {
                    $(".te_search_popover").css('width', $(window).width() + 'px');
                }
                if ($(window).width() < 992) {
                    if ( $('.navbar-light .navbar-toggler-icon').hasClass('open') ) {
                        $("header.te_header_canna .navbar .navbar-collapse").css('z-index', '1');
                    }
                    else {
                        $("header.te_header_canna .navbar .navbar-collapse").css('z-index', '99');
                    }
                }
                $(".te_search_popover").addClass("visible");
                $(self).css("display", "none");
                $(".te_srch_close").css("display", "inline-block");
                setTimeout(function(){
                    $('.te_search_popover input[name="search"]').focus();
                });
            }
         },

         _onSearchClickToClose: function(ev) {
            var self = ev.currentTarget;
            //style8
            if ($(".te_header_8_right").length) {
                if ( $('header.o_affix_enabled.te_header_canna').hasClass('header_not_scrolled') ) {
                    if ( !$('.navbar-light .navbar-toggler-icon').hasClass('open') ) {
                        $('header.o_affix_enabled.te_header_canna').removeClass('start-sticky');
                    }
                }
                $(".te_search_popover").removeClass("visible");
                $(self).css("display", "none");
                $(".te_srch_icon").css("display", "inline-block");
            }
         },

    });

    /* Added specific sizeClass while extra menu added */
    sAnimations.registry.autohideMenu.include({
         start: function () {
            var self = this;
            dom.initAutoMoreMenu(self.$el, {unfoldable: '.divider, .divider ~ li', sizeClass: 'MD'});
         },
    });

    /* Canna FR News Model Popup */
    sAnimations.registry.claricoExtended = sAnimations.Class.extend({
        selector: "#wrapwrap",
        read_events: {
            'click .te_event_popup': '_onClickEvent',
            'click .department_img': '_onClickDepartment',
            'click .dept_team_name': '_onClickTeam',
            'click #partnership_form .o_website_form_send' : '_onClickPartnership',
            'click #canna_signup_form .community_form_submit_btn' : '_onClickSignUp',
        },
        start: function () {
            self = this;
            self.newsPopup();
        },
        newsPopup: function() {
            $('.te_news_popup').on('click', function() {
                 var news_id = $(this).attr('data-id');
                 ajax.jsonRpc('/news_item', 'call',{'news_id':news_id}).then(function(data) {
                    $("#news_model .modal-body").html(data);
                     $("#news_model").modal({keyboard: true});
                 });
            });
        },
        _onClickEvent: function(ev) {
            ev.preventDefault();
             var event_id = $(ev.currentTarget).attr('data-id');
             ajax.jsonRpc('/event_item', 'call',{'event_id':event_id}).then(function(data) {
                $("#news_model .modal-body").html(data);
                $("#news_model").modal({keyboard: true});
             });
        },
        _onClickDepartment: function(ev) {
            self = $(ev.currentTarget)
            var department_id = self.attr('dep-id') || false;
            if (department_id) {
                ajax.jsonRpc('/get_department_team', 'call', {'department_id': department_id}).then(function (data) {
                    $("#dept_teams_model .modal-body").html(data);
                    $("#dept_teams_model").modal({keyboard: true});
                });
            }
        },
        _onClickTeam: function(ev) {
            self = $(ev.currentTarget)
            var team_id = self.attr('team-id') || false;
            if (team_id) {
                ajax.jsonRpc('/get_department_team_data', 'call', {'team_id': team_id}).then(function (data) {
                    $("#dept_teams_model .modal-body").html(data);
                    $("#dept_teams_model").modal({keyboard: true});
                });
            }
        },
        _onClickPartnership: function(ev) {
            self = $(ev.currentTarget)
            var name = $("#partner_name").val();
            var email = $("#partner_email").val();
            var description = $("#partner_description").val();
            if (name == "" || email=="" || description == ""){
                $(".partner_form_error").css({"display": "block"});

            }
            else{
                var is_become_partner = $("#is_become_partner:checked").val();
                if (is_become_partner){
                    is_become_partner = 1
                }
                var is_organize_event = $("#is_organize_event:checked").val();
                if (is_organize_event){
                    is_organize_event = 1
                }
                var is_other = $("#is_other:checked").val();
                if (is_other){
                    is_other = 1
                }
                ajax.jsonRpc('/create_partnership_data', 'call', {'name': name,'email':email, 'description':description, 'is_become_partner':is_become_partner, 'is_organize_event':is_organize_event, 'is_other': is_other}).then(function (data) {
                    $(".partnership_form_msg").css({"display": "block"});
                    $(".partner_form_error").css({"display": "none"});
                    $('#partnership_form')[0].reset();
                });
            }

        },
        _onClickSignUp: function(ev) {
            self = $(ev.currentTarget)
            var t_n_c_checkbox = $("#canna_t_n_c:checked").val();
            var news_later_checkbox = $("#canna_news_latter:checked").val();
            if (t_n_c_checkbox && news_later_checkbox){
                    $( "#canna_signup_form").submit();
            }
            else{
                $("#canna_signup_form .community_form_submit p").text( "News later and terms & condition checkbox is necessary");
                $("#canna_signup_form .community_form_checkbox .mark").css({"border": "1px solid red"});
            }
        },
    });

    /* Canna new header sticky */
    $(window).load(function() {
        if ($('header.o_affix_enabled.te_header_canna').length) {
            var headerHeight = $('header.o_affix_enabled.te_header_canna').height();
            $('header.o_affix_enabled.te_header_canna').addClass('header_not_scrolled');
            $(window).scroll(function () {
                var st = $(this).scrollTop();
                if (st > headerHeight) {
                    $('body').addClass('fixed-canna-header-bar');
                    $('header.o_affix_enabled.te_header_canna').addClass('header_scrolled start-sticky').removeClass('header_not_scrolled');
                } else {
                    $('body').removeClass('fixed-canna-header-bar');
                    $('header.o_affix_enabled.te_header_canna').removeClass('header_scrolled start-sticky').addClass('header_not_scrolled');
                }
            });
        }

        $("button.navbar-toggler").click(function(e) {
            if ($(window).width() < 992) {
                $('.te_header_canna.start-sticky nav.te_header_navbar, .te_header_canna.start-sticky, header.te_header_canna .navbar .navbar-collapse').css('transition','none');
                $('header.header_not_scrolled').toggleClass('start-sticky');
                $('span.navbar-toggler-icon').toggleClass('open');
            }
        });
        $(window).scroll(function () {
           if ($(window).width() < 992) {
                $('.te_header_canna.start-sticky nav.te_header_navbar, .te_header_canna.start-sticky, header.te_header_canna .navbar .navbar-collapse').css({'transition': 'all .2s;'});
           }
        });
    });

    $(document).ready(function($) {
        var owl_rtl = false;
        if ($('#wrapwrap').hasClass('o_rtl')) {
            owl_rtl = true;
        }
        $('#owl_homepage_news_block, #owl_events_block').owlCarousel({
            rtl: owl_rtl,
            items: 1,
            dots: true,
        });
        var items = $('#owl-department').attr('data-items') || false;
        $('#owl-department').owlCarousel({
            rtl: owl_rtl,
            items: 3,
            loop: items > 3 ? true : false,
            margin: 20,
            lazyLoad:true,
            autoplay: true,
            autoplayTimeout: 4000,
            items: 3,
            responsive:{
                0: {
                    items: 1,
                    loop: items > 1 ? true : false,
                },
                576: {
                    items: 2,
                    loop: items > 2 ? true : false,
                },
                992: {
                    items: 3,
                    loop: items > 3 ? true : false,
                },
                1300: {
                    items: 3,
                    loop: items > 3 ? true : false,
                }
            }
        });
    });
});