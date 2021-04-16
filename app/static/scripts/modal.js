var modal = document.getElementById("myModal");

var modalImg = document.getElementById("modal-img");


document.addEventListener("click", (e) => {
    const elem = e.target;
    if (elem.id==="myImg") {
      modal.style.display = "block";
      modalImg.src = elem.dataset.biggerSrc || elem.src;
      captionText.innerHTML = elem.alt; 
    }
  })
  

  
  // When the user clicks on modal image, close the modal
  modal.onclick = function() { 
    modal.style.display = "none";
  }