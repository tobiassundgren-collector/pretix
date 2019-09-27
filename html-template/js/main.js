    
/* Mobile Navigation
    -----------------------------------------------
$(window).scroll(function() {
    if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
});
*/


/* HTML document is loaded. DOM is ready. 
-------------------------------------------*/
$(document).ready(function() {

    svg4everybody(); 
    /* Hide mobile menu after clicking on a link
      -----------------------------------------------*/
      $('.navbar-collapse a').click(function(){
          $(".navbar-collapse").collapse('hide');
      });
    }
);
  