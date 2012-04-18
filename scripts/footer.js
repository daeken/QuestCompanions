$(document).ready(function() {
   /* if ($('.col').length > 0)
    {
    if ($(window).width() > 980)
    {
      $('.content').height($('.col').height());
    } else {
      $('.content').height($('.col').height() + $('.col').next().height());
      }
      }*/
    footGlue();
    });

$(window).resize(function() {
    footGlue();
    });

function footGlue()
{
  if (($('.content').outerHeight() + 40) <
      ($(window).outerHeight() - $('.footer').outerHeight()))
  {
    $('.footer').addClass('stuck');
  } else {
     $('.footer').removeClass('stuck');
  }
}
