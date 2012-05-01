$(document).ready ->
	$('#next-1').click ->
		if ~~$('#amount').val() < 10
				alert('Minimum amount for withdrawal is 10 gold')
				return false
		$('#first').hide 'fast'
		$('#second').show 'fast'
		false
	$('#next-2').click ->
		$('#amount-confirm').text ~~$('#amount').val()
		$('#name-confirm').text $('#name').val()
		$('#address-confirm').text $('#address').val()

		$('#second').hide 'fast'
		$('#third').show 'fast'
		false
