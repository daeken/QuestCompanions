$(document).ready ->
	if $('#job-title').data('accepted') == 'no'
		setTimeout (-> location.reload()), 30000

	$('#bid-form').submit ->
		max_pay = ~~$('#bid-form').data 'maxpay'
		amount = ~~$('input[name="amount"]').val()
		if amount < 5
			alert('Minimum amount is 5 gold')
			return false
		else if amount > max_pay
			alert('Amount is over maximum')
			return false
		return true

	$('.bid-accept').click (e) ->
		elem = $ e.currentTarget
		gold = elem.data 'gold'
		char = elem.data 'char'
		if confirm('Accept bid for ' + gold + ' from ' + char + '?  This cannot be undone.')
			$rpc.job.accept_bid elem.data('id'), ->
				location.reload()

	$('#cancel-job').click ->
		if confirm('Are you sure you want to cancel this job?  This cannot be undone.')
			$rpc.job.cancel $('#job-title').data('id'), ->
				location.reload()
