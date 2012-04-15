$(document).ready(
    function() {
      $('.errKill').click(
        function() {
          $('.errPop').animate(
            {opacity : 0},
            500,  
            function() {$('.errPop').remove()}
            )
          }
        )
      }
    );
