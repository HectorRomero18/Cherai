    // Función para abrir el modal con la imagen
    function openModal(imageUrl) {
      var modal = document.getElementById("imageModal");
      var modalImage = document.getElementById("modalImage");
      
      // Asigna la URL de la imagen al src del modal
      modalImage.src = imageUrl;
      
      // Muestra el modal
      modal.style.display = "flex";
  }

  // Función para cerrar el modal
  function closeModal() {
      var modal = document.getElementById("imageModal");
      modal.style.display = "none";
  }

  // Cierra el modal si se hace clic fuera de la imagen
  window.onclick = function(event) {
      var modal = document.getElementById("imageModal");
      if (event.target == modal) {
          closeModal();
      }
  }