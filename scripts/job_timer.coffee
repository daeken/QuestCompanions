$(document).ready ->
	id = $('#job').data 'id'

	interval = null
	activated = ->
		$('#second').show 'fast'
		check = ->
			$rpc.job.check_active id, (ret) ->
				[ret, toff] = ret
				if ret == 2
					clearInterval interval
					$('#second').hide 'fast'
					start(toff)
		interval = setInterval(check, 2500)

	start = (toff) ->
		$('#main').show 'fast'
                mixpanel.track "User Started Timer"
		start_time = new Date().valueOf() + toff * 1000
		update = ->
			$('#foo').text((new Date() - start_time) / 1000)
		update()
		timerInterval = setInterval update, 100
		checkComplete = ->
			$rpc.job.check_complete id, (ret) ->
				if ret
					clearInterval timerInterval
					clearInterval checkCompleteInterval
					$('#main').hide 'fast'
					$('#feedback').show 'fast'
		checkCompleteInterval = setInterval checkComplete, 2000
		$('#complete').click ->
			if confirm 'Are you sure you want to complete this job?  This cannot be undone.'
				clearInterval timerInterval
				clearInterval checkCompleteInterval
                                mixpanel.track "User Completed Job"
				$rpc.job.complete id, ->
					$('#main').hide 'fast'
					$('#feedback').show 'fast'


	$rpc.job.check_active id, (ret) ->
		[ret, toff] = ret
		if ret == 0
			$('#first').show 'fast'
			$('#start').click ->
				$('#first').hide 'fast'
				$rpc.job.set_active id, (ret) ->
					[ret, toff] = ret
					if ret == 2
						start(toff)
					else
						activated()
		else if ret == 1
			activated()
		else
			start()
