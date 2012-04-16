$(document).ready(
    function() {
      $('.alertPop').slideDown('slow');
      $('.errKill').click(
        function() {
          $('.alertPop').slideUp('slow',
            function() {$('.alertPop').remove()}
            );
          }
        );
      }
    );
