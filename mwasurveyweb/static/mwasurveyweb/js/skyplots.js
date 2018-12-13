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

function is_colours_there(colours, name) {
  var success = true
  for (var count = 0; count < colours.length; count++) {
    if (!name.includes(colours[count])) {
      success = false
      break
    }
  }
  return success
}

function only_these_colours(colours, name) {
  return name.replace('.png', '').length === colours.join('_').length
}

function show_image(colours) {

  if (!colours.length) {
    colours = ['blank']
  }

  $('#sky-plots > img').each(function () {

    $(this).attr('hidden', true)

    var name = $(this).attr('src').split('/')
    name = name[name.length - 1]

    if (is_colours_there(colours, name) && only_these_colours(colours, name)) {
      $(this).attr('hidden', false)
    }
  })
}

$(document).ready(function () {
  $('.custom-switch-input').on('click', function () {
    show_image(check_inputs())
  })
})
