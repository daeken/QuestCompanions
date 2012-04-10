validateForm = (max_pay) ->
	alert max_pay

$(document).ready ->
	$('.bid-accept').click (e) ->
		elem = $ e.currentTarget
		gold = elem.data 'gold'
		char = elem.data 'char'
		if confirm('Accept bid for ' + gold + ' from ' + char + '?  This cannot be undone.')
			$rpc.job.accept_bid elem.data('id'), ->
				location.reload()
