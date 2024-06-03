$('#container-none').on('change', 'input[data-check-none]', function() {
  console.log('радио изменен');
  document.getElementById("id_delivery_address").style.display = "none";
  document.getElementById("id_delivery_address").required = false;
  const button_send_code = document.querySelector('#id_delivery_address');
});

$('#container').on('change', 'input[data-check]', function() {
  console.log('радио');
  document.getElementById("id_delivery_address").style.display = "inline-block";
  const button_send_code = document.querySelector('#id_delivery_address');
});
