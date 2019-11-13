(function ($) {
	"use strict";
    jQuery(document).ready(function($){
        $(".embed-responsive iframe").addClass("embed-responsive-item");
        $(".carousel-inner .item:first-child").addClass("active");
        $('[data-toggle="tooltip"]').tooltip();
        // service carousel
        $("#pricing-carousel").owlCarousel({
            dots:false,
            nav:true,
            items:3,
            touchDrag: true,
            smartSpeed:1000,
            autoplay:true,
            autoplayTimeout:700000,
            autoplayHoverPause:true,
            loop:true,
            center: true,
            responsive:{
                0:{
                    items:1
                },
                600:{
                    items:2
                },
                1000:{
                    items:3
                }
            },
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"]
        });
        // service carousel

    });
}(jQuery));