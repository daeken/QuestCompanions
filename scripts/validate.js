$(document).ready(function() {
  console.log('prepping');
 $('input').each(function() {
   $(this).change(function() {
      var type = $(this).attr('type');
      if((type === 'number' || type === 'time') &&
      !$.isNumeric($(this).val()))
      {
        $(this).addClass('error');
        $(this).parent().append('<span class="'+type+'Message errMessage">Please enter a valid ' + type + ' to continue</span>')
      } else {
        $(this).removeClass('error');
        $('.'+type+'Message').remove();
        }
    });
  });
  $('form').submit(function(event)
  {
    var hasErrors = false;
    $('input').each(function() {
    var type = $(this).attr('type');
      if((type === 'number' || type === 'time') &&
      !$.isNumeric($(this).val()))
      {
        $(this).addClass('error');
        hasErrors = true;
      }
    });
    if(hasErrors)
    {
      console.log('error');
      $('h5').remove();
      $('form').prepend('<h5 class="errMessage">Make sure you\'ve entered all the information correctly</h5>');
      return false;
    }
  });
});
