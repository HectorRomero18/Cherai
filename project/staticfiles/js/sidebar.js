document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.querySelector(".sidebar");
    const menuToggle = document.querySelector("#menu-toggle");
    const overlay = document.querySelector("#overlay");

    // Función para alternar la visibilidad de la barra lateral
    menuToggle.addEventListener("click", function() {
        sidebar.classList.toggle("open"); // Abre o cierra la barra lateral

        // Si la barra lateral está abierta, ocultar el ícono de las tres líneas
        if (sidebar.classList.contains("open")) {
            menuToggle.style.display = "none"; // Ocultar el ícono
        } else {
            menuToggle.style.display = "block"; // Mostrar el ícono
        }
    });

    // Cerrar la barra lateral si se hace clic fuera de ella (en el overlay)
    overlay.addEventListener("click", function() {
        sidebar.classList.remove("open"); // Cerrar la barra lateral
        menuToggle.style.display = "block"; // Mostrar el ícono de las tres líneas
    });
});
