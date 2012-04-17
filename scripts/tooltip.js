$(document).ready(function() {
 $('input, textarea, .charLink').each(function() {
   handler($(this));
  });
});

function handler(obj)
{
  if($(obj).is('input, textarea'))
  {
    $(obj).focus(function() {
      addTip(obj);
      $(obj).mouseover(function() {
        if ($(obj).is($(':focus')))
        {          
          addTip(obj);
        }
      });
    });
  } else {
    $(obj).mouseover( function() {
      addCharTip(obj);
    });
  }
  $(obj).mouseout(function() {
    var oldTip = $('.tip');
      $(oldTip).fadeOut(200, function() {$(oldTip).remove()});
  });
}

function addTip(obj)
{
   $(obj).parent().append('<div class="tip" style="' +
     'left:' + $(obj).offset().left + 'px!important;' +
     'top:' + ($(obj).offset().top + ($(obj).outerHeight(false)) + 5 - $(window).scrollTop()) + 'px;' +
     '">' +
     $(obj).data('hint') +
     '</div>');
}

function addCharTip(obj)
{
  var data = $(obj).data('char');
  $(obj).parent().append( '<div class="charTip tip" style="top: ' + ($(obj).offset().top - 10) + 'px"> ' +
  '<img class="avatar" src="' + data.avatar + '"/> ' +
  '<ul>' +
  '<li class="game">' + data.game +
  '<li class="server">' + data.server +
  '</ul>' +
  '</div>');
}
