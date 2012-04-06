var clock = function()
{
};

clock.prototype = {
seconds: 0,
minutes: 0,
hours: 0,
timer: null,
started: false,
tick: function() {
         this.seconds += 1;
         if (this.seconds === 60)
         {
           this.seconds = 0;
           this.minutes += 1;
         }
         if (this.minutes === 60)
         {
           this.minutes = 0;
           this.hours += 1;
         }
         $('.seconds')[0].innerHTML =
           (this.seconds.toString().length > 1) ?
           this.seconds :
           '0' + this.seconds;

         $('.minutes')[0].innerHTML =
           (this.minutes.toString().length > 1) ?
           this.minutes :
           '0' + this.minutes;

         $('.hours')[0].innerHTML =
           (this.hours.toString().length > 1) ?
           this.hours :
           '0' + this.hours;
       },
stop: function() {
         clearInterval(this.ticker);
         $('.quester > i').attr('class', 'red');
         $('.starter').removeClass('stop');
         $('.starter').addClass('grey');
         $('.starter').off('click');
         $('.starter')[0].innerHTML = 'Finished';
       },
start: function() {
          var t = this;
          if (this.started === false)
          {
            this.started = true;
            this.ticker = setInterval(function() {t.tick();}, 1000);
            $('.starter').addClass('stop');
            $('.starter')[0].innerHTML = 'Stop Timer';
          } else {
            (this.stop)();
            t.started = false;
          }
        }
};
  var c = new clock();
function toggleTimer()
{
  $('.quester > i').attr('class', 'green');
  (c.start)();
}

$(window).load(
  function() {
  $('.starter').click(
      function() {
        toggleTimer();
      }
    );
  }
);

