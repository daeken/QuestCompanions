$(document).ready( function() {
    $('.charLink').each( function() {
      $(this).mouseover( function() {
        var data = $(this).data('char');
        $('.charTip').remove();
        $(this).parent().append( '<div class="charTip" style="top: ' + ($(this).offset().top - 10) + 'px"> ' +
          '<img class="avatar" src="' + data.avatar + '"/> ' +
          '<ul>' +
          '<li class="game">' + data.game +
          '<li class="server">' + data.server +
          '</ul>' +
          '</div>');
          });
      $(this).mouseout( function() {
        $('.charTip').remove();
      });
    });
  });
