$(document).ready ->
	id = $('#job').data 'id'

	interval = null
	activated = ->
		$('#second').show 'fast'
		check = ->
			$rpc.job.check_active id, (ret) ->
				if ret == 2
					clearInterval interval
					$('#second').hide 'fast'
					start()
		interval = setInterval(check, 5000)

	start = ->
		$('#main').show 'fast'

	$rpc.job.check_active id, (ret) ->
		if ret == 0
			$('#first').show 'fast'
			$('#start').click ->
				$('#first').hide 'fast'
				$rpc.job.set_active id, (ret) ->
					if ret == 2
						start()
					else
						activated()
		else if ret == 1
			activated()
		else
			start()
