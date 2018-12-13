function get_colour_name(element_name) {
  return element_name.replace('status_', '')
}

function check_inputs() {
  var colours = []

  $('.custom-switch-input').each(function () {
    if ($(this).is(":checked")) {
      colours.push(get_colour_name(this.name))
    }
  })

  return colours
}

function get_div_class(colours) {
  return 'sky-plots.' + colours.join('.')
}

$(document).ready(function () {
  $('.custom-switch-input').on('click', function (e) {
    var div_to_show = get_div_class(check_inputs())



    console.log(div_to_show)
  })
})
