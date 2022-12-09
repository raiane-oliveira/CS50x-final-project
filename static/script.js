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


// Abre o card de formulário para planejar a venda
const buttonSale = document.querySelectorAll(".click-btn");
const onSale = document.querySelector(".on-sale");
const backgroundSale = document.querySelector(".background-sale");
const closePlanSale = document.querySelector(".material-icons");

for (var i = 0; i < buttonSale.length; i++)
{
    buttonSale[i].addEventListener("click", () => {

        onSale.style.display = "block";
        backgroundSale.style.display = "block";
    });
}

closePlanSale.addEventListener("click", () => {
    
    onSale.style.display = "none";
    backgroundSale.style.display = "none";
});