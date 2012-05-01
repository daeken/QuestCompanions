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

var attrmap = {
  game: 'Game', 
  server: 'Server', 
  name: 'Name', 
  faction: 'Faction', 
  race: 'Race', 
  level: 'Level', 
  charclass: 'Class', 
  item_level: 'Item Level'
};

function addCharTip(obj)
{
  var data = $(obj).data('char');
  var elements = '';
  for(k in attrmap)
    if(data[k])
      elements += '<li class="' + k + '">' + attrmap[k] + ': ' + data[k];
  $(obj).parent().append( '<div class="charTip tip" style="top: ' + ($(obj).offset().top + ($(obj).outerHeight(false)) + 5 ) + 'px"> ' +
  '<img class="avatar" src="' + data.avatar + '"/> ' +
  '<ul>' +
  elements + 
  '</ul>' +
  '<div style="clear:all"></div>'+
  '</div>');
}
