// Menu responsivo
const menuBtn = document.querySelector(".menu-btn");
const menu = document.querySelector(".nav ul");
if (menuBtn && menu) {
  menuBtn.addEventListener("click", () => menu.classList.toggle("open"));
  menu.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => menu.classList.remove("open")));
}

// Ano atual no rodapé
const year = document.getElementById("year");
if (year) year.textContent = new Date().getFullYear();
