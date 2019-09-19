$(function($){
    "use strict";
            $('.blog_text_slider').owlCarousel({
                loop:true,
                margin: 20,
                items: 1,
                nav: false,
                autoplay: true,
                autoplayTimeout: 15000,
                smartSpeed: 3000,
                dots:false,
				navContainer: '.blog_text_slider',
                navText: ['<i class="fas fa-arrow-left text-dark"></i>','<i class="fas fa-arrow-right text-dark"></i>'],
            })
});


$(function ($){
    'use strict';
        $('.post-category-slider').owlCarousel({
            items: 1,
            margin: 0,
            loop: true,
            dots: false,
            autoplay: true,
            autoplayTimeout: 15000,
            smartSpeed: 2000,
            nav: true,
            navText: ['<i class="fas fa-arrow-circle-left"></i>', '<i class="fas fa-arrow-circle-right"></i>']
        });
    });

$(function ($) {
    'use strict';
    $('.cycle_slider').owlCarousel({
    loop:true,
    margin:10,
    responsiveClass:true,
    responsive:{
        0:{
            items:1,
            nav:true
        },
        1000:{
            items:2,
            loop:false,
        }
    }
})
});
