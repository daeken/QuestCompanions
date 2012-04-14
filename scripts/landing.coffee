enlist = () ->
	if enlisted
		return
	email = $('#email').val()
	if email.indexOf('@') == -1
		alert('Please enter a proper email before enlisting!')
		return
	enlisted = true
	$rpc.auth.enlist $('#email').val(), (ret) ->
		if ret == true
			$('#email').val('You have enlisted!').attr('disabled', true)
		else
			$('#email').val('You have already enlisted!').attr('disabled', true)
		$('#enlist').attr('disabled', true)


$(document).ready ->
	$('#enlist').click -> enlist()
