$(document).ready(() => {

    let userPreferredTheme = localStorage.getItem("theme");

    if (userPreferredTheme) {
        setTheme(userPreferredTheme);
        setToggleBtnTo(userPreferredTheme);
    } else {
        setTheme("light");
        setToggleBtnTo("light");
    }

})

$("#toggle-theme-btn").on("click", (event) => {
    const current_theme = localStorage.getItem("theme");

    if (current_theme == "light") {
        setTheme("dark");
        setToggleBtnTo("dark");
    } else {
        setTheme("light");
        setToggleBtnTo("light");
    }
});

function setTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem("theme", theme);
}

function setToggleBtnTo(theme) {
    let buttonHtml = "";
    const button = $("#toggle-theme-btn");

    if (theme == "light") {
        buttonHtml = `
        <span class="fa-regular fa-moon"></span>`;
        button.removeClass("btn-light");
        button.addClass("btn-dark");
    } else {
        buttonHtml = `
        <span class="fa-regular fa-sun"></span>`;
        button.removeClass("btn-dark");
        button.addClass("btn-light");
    }
    button.html(buttonHtml);
}