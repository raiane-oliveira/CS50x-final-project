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
const formSale = document.querySelectorAll(".click-btn");
const onSale = document.querySelector(".on-sale");
const backgroundSale = document.querySelector(".background-sale");
const closePlanSale = document.querySelectorAll(".material-icons");

// Seleciona o id dos filtros
var id = 0;
var form = document.querySelector(".form-planSale");

document.querySelectorAll("button").forEach(function(button) {

    button.addEventListener("click", function(event) {

        var element = event.target;
        id = element.id;   
        console.log(id)
    });
});

for (var i = 0; i < formSale.length; i++)
{
    formSale[i].addEventListener("submit", function(e) {

        onSale.style.display = "block";
        backgroundSale.style.display = "block";
        e.preventDefault();

        if (id == "selling")
        {
            form.setAttribute("id", "selling");

            // Adiciona o valor id do formulário
            document.querySelector("#id").setAttribute("value", "selling");
        }
        else if (id == "not-started")
        {
            form.setAttribute("id", "not-started");

            document.querySelector("#id").setAttribute("value", "not-started");
        }
        else
        {
            form.setAttribute("id", "sold");

            // Adicionar o valor ao id do formulário
            document.querySelector("#id").setAttribute("value", "sold");
        }
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