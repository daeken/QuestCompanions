$(document).ready(function() {
 $('input, textarea, .charLink').each(function() {
   handler($(this));
  });
});

function handler(obj)
{
  if($(obj).is('input, textarea'))
  {
    if($(obj).data('hint'))
    {
    $(obj).focus(function() {
      addTip(obj);
      $('.tip').slideDown('fast');
      $(obj).mouseover(function() {
        if ($(obj).is($(':focus')))
        {          
          addTip(obj);
          $('.tip').slideDown('fast'); 
        }
      });
    });
    }
  } else {
    $(obj).mouseover( function() {
      addCharTip(obj);
      $('.tip').slideDown('fast');
    });
  }
  $(obj).mouseout(function() {
    var oldTip = $('.tip');
      $(oldTip).slideUp('fast', function() {$(oldTip).remove()});
  });
  $(obj).blur(function() {
      var oldTip = $('.tip');
      $(oldTip).slideUp('fast', function() {$(oldTip).remove()});
      } );
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
  $(obj).parent().append( '<div class="charTip tip" style="top: ' + ($(obj).offset().top + ($(obj).outerHeight(false)) + 5 ) + 'px"> ' +
  '<img class="avatar" src="' + data.avatar + '"/> ' +
  '<ul>' +
  '<li class="game">Game: ' + data.game +
  '<li class="server">Server: ' + data.server +
  '<li class="name">Name: ' + data.name +
  '<li class="faction">Faction: ' + data.faction +
  '<li class="race">Race: ' + data.race +
  '<li class="level">Level: ' + data.level +
  '<li class="charclass">Class: ' + data.charclass +
  '<li class="item_level">Equipment Level: ' + data.item_level +
  '</ul>' +
  '<div style="clear:all"></div>'+
  '</div>');
}
