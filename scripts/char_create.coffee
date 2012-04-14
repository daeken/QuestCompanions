$(document).ready ->
	showgame =  ->
		$('.game-pane').hide 'fast'
		$('#game-' + $('#game').val()).show 'fast'
	showgame()
	$('#game').change showgame
	$('#wow-add').click ->
		$rpc.char.add_wow $('#server').val(), $('#charname').val(), (ret) ->
			if ret == false or ret == undefined
				alert 'Check the server and character name and try again'
				errorClear()
			else
				return_to = $('#return-to').val()
				if return_to
					window.location = return_to
				else
					window.location = ret
