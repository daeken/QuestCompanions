$(document).ready(function() {
 $('input').each(function() {
   if($(this).attr('required'))
   {
    $(this).parent().append('<span class="'+$(this).attr('type')+'post">*required</span>');
   }
   
   $(this).change(function() {
      var type = $(this).attr('type');
      if((type === 'number' || type === 'time') &&
      !$.isNumeric($(this).val()))
      {
        $(this).addClass('error');
        $('.'+$(this).attr('type')+'post')[0].innerHTML = 'Please enter a valid ' + type + ' to continue';
      } else {    
        $('.'+$(this).attr('type')+'post')[0].innerHTML='*required';
        $(this).removeClass('error');
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
        $('.'+$(this).attr('type')+'post')[0].innerHTML = 'Please enter a valid ' + type + ' to continue';
        $(this).addClass('error');
        hasErrors = true;
      }
    });
    if(hasErrors)
    {
      $('h5').remove();
      $('form').prepend('<h5 class="errMessage">Make sure you\'ve entered all the information correctly</h5>');
      return false;
    }
  });
});
