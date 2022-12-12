// Menu responsivo
let show = true;

const header = document.querySelector("header");
const menuToggle = header.querySelector(".menu-toggle");

menuToggle.addEventListener("click", () => {
    document.body.style.overflow = show ? "hidden" : "initial";

    header.classList.toggle("on", show)
    show = !show;
});


// Marca a página atual que o usuário está
// for (var i = 1; i < document.links.length; i++)
// {
//     if (document.links[i].href == document.URL)
//     {
//         document.links[i].className = 'active';
//     }
// }


// Abre o card de formulário para planejar a venda ou edita-la
const buttonSale = document.querySelectorAll(".click-btn");
const editButton = document.querySelectorAll(".form-edit")
const onSale = document.querySelector(".on-sale");
const backgroundSale = document.querySelector(".background-sale");
const closePlanSale = document.querySelectorAll(".material-icons");

// Adiciona um novo card
for (var i = 0; i < buttonSale.length; i++)
{
    buttonSale[i].addEventListener("submit", function(e) {

        onSale.style.display = "block";
        backgroundSale.style.display = "block";
        e.preventDefault();
    });
    
    closePlanSale[i].addEventListener("click", () => {
        
        onSale.style.display = "none";
        backgroundSale.style.display = "none";
    });
}

// Senha visível ou não
eye = document.querySelector(".visibility");
password = document.getElementById("password")
confirm_password = document.getElementById("confirm_password")

eye.addEventListener("click", () => {
    password.type = 'text';
    confirm_password.type = 'text';
});

// // Para que a senha não fique exposta após mover a imagem
eye.addEventListener("mousemove", () => {
    password.type = 'password';
    confirm_password.type = 'password';
});