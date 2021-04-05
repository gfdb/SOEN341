function swapStylesheetlight() {
    document.getElementById("styling").setAttribute("href","/static/light.css")
  $.getJSON('/swap_mode', function('light'){
    alert('light')
  })
}