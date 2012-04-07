function createCover()
{
  $('body').append('<div class="cover"><img class="shield" src="/static/img/logo.png"></div>');
  fade();
}

function fade()
{ 
  var currentOpacity = $('.shield').css('opacity');
  $('.shield').animate({
    opacity : 1 - currentOpacity} ,
    2000,
    function() {fade()}
    );
}

function errorClear()
{
  $('.cover').remove();
}

$(window).load(
    function() {
    $('button').click(
      function() { 
        createCover();
      }    
    )
    }
  );
