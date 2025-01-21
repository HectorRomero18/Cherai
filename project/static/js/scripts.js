// Función para manejar la animación del selector en el navbar
function test() {
    let tabsNewAnim = $("#navbarSupportedContent");
    let activeItemNewAnim = tabsNewAnim.find(".active");
    let activeWidthNewAnimHeight = activeItemNewAnim.innerHeight();
    let activeWidthNewAnimWidth = activeItemNewAnim.innerWidth();
    let itemPosTopNewAnim = activeItemNewAnim.position();
    let itemPosLeftNewAnim = activeItemNewAnim.position();

    $(".hori-selector").css({
        top: itemPosTopNewAnim.top + "px",
        left: itemPosLeftNewAnim.left + "px",
        height: activeWidthNewAnimHeight + "px",
        width: activeWidthNewAnimWidth + "px"
    });

    // Cuando un elemento del navbar es clickeado
    $("#navbarSupportedContent").on("click", "li", function () {
        $("#navbarSupportedContent ul li").removeClass("active");
        $(this).addClass("active");
        let activeWidthNewAnimHeight = $(this).innerHeight();
        let activeWidthNewAnimWidth = $(this).innerWidth();
        let itemPosTopNewAnim = $(this).position();
        let itemPosLeftNewAnim = $(this).position();

        $(".hori-selector").css({
            top: itemPosTopNewAnim.top + "px",
            left: itemPosLeftNewAnim.left + "px",
            height: activeWidthNewAnimHeight + "px",
            width: activeWidthNewAnimWidth + "px"
        });
    });
}

// Inicializa la animación en el navbar
$(document).ready(function () {
    setTimeout(function () {
        test();
    }, 100);  // Usamos un pequeño retraso para asegurarnos de que los elementos estén listos
});

// Añade el efecto hover en los enlaces del navbar
$(document).ready(function () {
    $('#navbarSupportedContent ul li a').hover(
        function () {
            $(this).addClass('hovered');
        },
        function () {
            $(this).removeClass('hovered');
        }
    );
});

// Función para manejar el cierre de sesión
document.getElementById("logout-link").addEventListener("click", function () {
    Swal.fire({
        title: "¿Estás seguro?",
        text: "Se cerrará tu sesión.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, cerrar sesión",
        cancelButtonText: "Cancelar",
    }).then((result) => {
        if (result.isConfirmed) {
            // Limpiar la sesión (puedes usar sessionStorage o localStorage)
            sessionStorage.clear();  // O usa localStorage.clear()

            // Redirigir a la página de login
            window.location.href = "/blog/logout/"; // Cambia la URL de la página de login si es necesario
        }
    });
});

$(document).ready(function() {
    $(".navbar-toggler").click(function() {
      $("#navbarSupportedContent").toggleClass("collapse");
    });
});

// Establece el favicon de la página
let link = document.createElement('link');
link.rel = 'icon';
link.type = 'image/png';
link.href = '{% static "img/logo.png" %}';
document.getElementsByTagName('head')[0].appendChild(link);
