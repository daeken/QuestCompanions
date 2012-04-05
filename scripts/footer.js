$(document).ready(function() {
    footGlue();
});

$(window).resize(function() {
    footGlue();
    });

function footGlue()
{
  if(($('.content').height() + 40) < ($(window).height() - $('.footer').height()))
  {
    $('.footer').addClass('stuck');
  } else {
     $('.footer').removeClass('stuck');
  } 
}
