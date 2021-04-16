var modal = document.getElementById("myModal");

var modalImg = document.getElementById("modal-img");
var captionText = document.getElementById("caption");

document.addEventListener("click", (e) => {
    const elem = e.target;
    if (elem.id==="myImg") {
      modal.style.display = "block";
      modalImg.src = elem.dataset.biggerSrc || elem.src;
      captionText.innerHTML = elem.alt; 
    }
  })
  
  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];
  
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() { 
    modal.style.display = "none";
  }