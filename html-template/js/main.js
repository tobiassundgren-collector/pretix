    


/* HTML document is loaded. DOM is ready. 
-------------------------------------------*/
$(document).ready(function() {

    svg4everybody(); 

      $('.owl-carousel').owlCarousel({
        loop:true,
        margin:20,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
                nav:true,
                loop:false
            },
            600:{
                items:3,
                nav:false,
                loop:false
            },
            1000:{
                items:4,
                nav:true,
                loop:false
            }
        }
    })
    }
);
  