price = gold = 0
card_number = cvc = expmonth = expyear = null

Stripe.setPublishableKey 'pk_c8kMInhHhfcmjGrhNkm64xI0wpLwG' # test key

$(document).ready ->
  $('.amount-choice').click (e) ->
    elem = $ e.currentTarget
    price = elem.data('price')
    gold = elem.data('gold')

    $('#amounts').hide 'fast'
    $('#payment').show 'fast'

  $('#pay-next').click ->
    card_number = $('.card-number').val()
    cvc = $('.card-cvc').val()
    expmonth = $('.card-expiry-month').val()
    expyear = $('.card-expiry-year').val()
    return alert 'Invalid card number' if not Stripe.validateCardNumber card_number
    return alert 'Invalid CVC number' if not Stripe.validateCVC cvc
    return alert 'Invalid expiration' if not Stripe.validateExpiry expmonth, expyear

    $('#gold-amount').text gold
    $('#gold-price').text price

    $('#card-number').text card_number
    $('#cvs').text cvc
    $('#exp-month').text expmonth
    $('#exp-year').text expyear

    $('#payment').hide 'fast'
    $('#confirmation').show 'fast'

  $('#complete').click ->
    Stripe.createToken {
      number: card_number, 
      cvc: cvc, 
      exp_month: expmonth, 
      exp_year: expyear
    }, (status, response) ->
      if response.error?
        return alert response.error
      $rpc.gold.buy response.id, gold, (ret) ->
        [error, gold] = ret
        if not error?
          $('#gold-total').text gold
          $('#confirmation').hide 'fast'
          $('#completion').show 'fast'
        else
          alert error
