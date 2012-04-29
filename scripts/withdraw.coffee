$(document).ready ->
  $('#next-1').click ->
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
