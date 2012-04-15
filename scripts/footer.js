$(document).ready(function() {
    $('.content').height($('.col').height());
    footGlue();
    });

$(window).resize(function() {
    footGlue();
    });

function footGlue()
{
  if(($('.content').outerHeight() + 40) < ($(window).outerHeight() - $('.footer').outerHeight()))
  {
    $('.footer').addClass('stuck');
  } else {
     $('.footer').removeClass('stuck');
  } 
}
