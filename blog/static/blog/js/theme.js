;(function($){
    "use strict"
	
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


$('.owl-carousel').owlCarousel({
    stagePadding: 50,
    loop:true,
    margin:10,
    nav:false,
    autoplay: true,
    items:2,
    dots:true,
    smartSpeed: 5000,
});



