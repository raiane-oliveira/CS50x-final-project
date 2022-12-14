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
for (var i = 1; i < document.links.length; i++)
{
    if (document.links[i].href == document.URL)
    {
        document.links[i].className = 'active';
    }
}

// Seleciona o formulário de planejar a venda 
const formSale = document.querySelectorAll(".click-btn");
const onSale = document.querySelector(".on-sale");
const backgroundSale = document.querySelector(".background-sale");
const closePlanSale = document.querySelectorAll(".material-icons");

// Seleciona o id dos filtros
var id = 0;
var formOnSale = document.querySelector(".form-planSale");

document.querySelectorAll("button").forEach(function(button) {

    button.addEventListener("click", function(event) {

        var element = event.target;
        id = element.id;   
    });
});

// Abre o card do formulário e adiciona um filtro pra cada um deles
formSale.forEach(function(form) {

    form.addEventListener("submit", function(e) {

        onSale.style.display = "block";
        backgroundSale.style.display = "block";
        e.preventDefault();

        if (id == "selling")
        {
            formOnSale.setAttribute("id", "selling");

            // Adiciona o id do formulário
            document.querySelector("#id").setAttribute("value", "selling");
        }
        else if (id == "not-started")
        {
            formOnSale.setAttribute("id", "not-started");

            // Adiciona o id do formulário
            document.querySelector("#id").setAttribute("value", "not-started");
        }
        else
        {
            formOnSale.setAttribute("id", "sold");

            // Adicionar o id do formulário
            document.querySelector("#id").setAttribute("value", "sold");
        }
    });

    closePlanSale.forEach(function(close) {

        close.addEventListener("click", () => {

            onSale.style.display = "none";
            backgroundSale.style.display = "none";
        });
    });
        
});

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
