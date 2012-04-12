$(document).ready(function() {
 $('input').each(function() {
   handler(this);
  })
 $('textarea').each(function() {
   handler($(this));
   })
 });

function handler(obj)
{
 $(obj).focus( function() {
   $('.tip').remove();
   $(obj).parent().append('<div class="tip" style="position:fixed; left:'+$(obj).offset().left + 'px; top: ' + ($(obj).offset().top + ($(obj).outerHeight(false)) ) + 'px; background: rgba(0,0,0,0.8); color: #fff; padding: 10px; border-radius:5px; z-index: 10;">' + $(obj).attr('data-hint') + '</div>');
   
   $(obj).mouseover( function() {
    $(obj).parent().append('<div class="tip" style="position:fixed; left:'+$(obj).offset().left + 'px; top: ' + ($(obj).offset().top + ($(obj).outerHeight(false)) ) + 'px; background: rgba(0,0,0,0.8); color: #fff; padding: 10px; border-radius:5px; z-index: 10;">' + $(obj).attr('data-hint') + '</div>');
    })

   })
 $(obj).mouseout( function() {
   $('.tip').remove();
   })
}
