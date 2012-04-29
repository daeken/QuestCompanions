$(document).ready(function() {
    footGlue();
    });

$(window).resize(function() {
    footGlue();
    });

function footGlue()
{
  if (($('.container').outerHeight() + $('.footer').outerHeight() + $('.header').outerHeight()) <
      ($(window).outerHeight() - $('.footer').outerHeight()))
  {
    $('.footer').addClass('stuck');
  } else {
     $('.footer').removeClass('stuck');
  }
}
