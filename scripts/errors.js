$(document).ready(
    function() {
      $('.errPop').slideDown('slow')
      $('.errKill').click(
        function() {
          $('.errPop').slideUp('slow', 
            function() {$('.errPop').remove()}
            )
          }
        )
      }
    );
