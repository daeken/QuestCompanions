/*
 * TODO We need to register a stripe account and get keys.
 * This currently doesn't do anything (and all stripe calls WILL break)
 */

Stripe.setPublishableKey('YOUR_PUBLISHABLE_KEY');

$(document).ready(function() {
  $("#payment-form").submit(function(event) {
    // disable the submit button to prevent repeated clicks
    $('.submit-button').attr("disabled", "disabled");

    Stripe.createToken({
      number: $('.card-number').val(),
      cvc: $('.card-cvc').val(),
      exp_month: $('.card-expiry-month').val(),
      exp_year: $('.card-expiry-year').val()
    }, stripeResponseHandler);
  // prevent the form from submitting with the default action
  return false;
  });
});

function stripeResponseHandler(status, response) {
  if (response.error) {
  /*
   * Logs any stripe error to JS console for now
   */
    console.log(response.error.message);
  }
  
  } else {
    var form$ = $("#payment-form");
    // token contains id, last4, and card type
    var token = response['id'];
    // insert the token into the form so it gets submitted to the server
    form$.append("<input type='hidden' name='stripeToken' value='" + token + "'/>");
    // and submit
    form$.get(0).submit();
  }
}
