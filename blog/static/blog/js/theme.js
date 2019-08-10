(function($){
    "use strict";

    function text_slider(){
        if ( $('.blog_text_slider').length ){
            $('.blog_text_slider').owlCarousel({
                loop:true,
                margin: 20,
                items: 1,
                nav: false,
                autoplay: true,
                smartSpeed: 3000,
                dots:false,
				navContainer: '.blog_text_slider',
                navText: ['<i class="fas fa-arrow-left text-dark"></i>','<i class="fas fa-arrow-right text-dark"></i>'],
            })
        }
    }
    text_slider();
})(jQuery);


(function ($){
    'use strict';
        $('.post-category-slider').owlCarousel({
            items: 1,
            margin: 10,
            loop: true,
            dots: false,
            autoplay: true,
            autoplayTimeout: 3500, // Autoplay Timeout 1s = 1000ms
            smartSpeed: 2000,
            autoHeight:true,
        });
    })(jQuery);