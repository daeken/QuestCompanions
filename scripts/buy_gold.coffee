price = gold = 0
card_number = cvc = expmonth = expyear = null

Stripe.setPublishableKey 'pk_c8kMInhHhfcmjGrhNkm64xI0wpLwG' # test key
#Stripe.setPublishableKey 'pk_0IeXiL6E6MIyU64Ws1FCCFo4YLJg3' # prod key

$(document).ready ->
	$('.amount-choice').click (e) ->
		elem = $ e.currentTarget
		price = elem.data('price')
		gold = elem.data('gold')

		$('#amounts').hide 'fast'
		$('#payment').show 'fast'

	$('#pay-back').click ->
		$('#payment').hide 'fast'    
		$('#amounts').show 'fast'
	$('#pay-next').click ->
		card_number = $('.card-number').val()
		cvc = $('.card-cvc').val()
		expmonth = $('.card-expiry-month').val()
		expyear = $('.card-expiry-year').val()
		return alert 'Invalid card number' if not Stripe.validateCardNumber card_number
		return alert 'Invalid CVC number' if not Stripe.validateCVC cvc
		return alert 'Invalid expiration' if not Stripe.validateExpiry expmonth, expyear

		$('#gold-amount-confirm').text gold
		$('#gold-price-confirm').text price

		$('#card-number-confirm').text card_number.substr(-4, 4)
		$('#cvc-confirm').text cvc
		$('#exp-month-confirm').text expmonth
		$('#exp-year-confirm').text expyear

		$('#payment').hide 'fast'
		$('#confirmation').show 'fast'

	$('#complete-back').click ->
		$('#confirmation').hide 'fast'    
		$('#payment').show 'fast'
	$('#complete').click ->
		Stripe.createToken {
			number: card_number, 
			cvc: cvc, 
			exp_month: expmonth, 
			exp_year: expyear
		}, (status, response) ->
			if response.error?
				errorClear()
				return alert response.error.message
			$rpc.gold.buy response.id, gold, (ret) ->
				[error, gold] = ret
				errorClear()
				if not error?
					$('#gold-total').text gold
					$('#confirmation').hide 'fast'
					$('#completion').show 'fast'
					mixpanel.track("User Purchased Gold", {"Amount": price})
				else
					alert error
