function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
}

function setTheme(theme, clickedCard = null) {
    localStorage.setItem("ecoTheme", theme);
    applyTheme(theme);

    document.querySelectorAll(".theme-card").forEach(card => card.classList.remove("selected"));

    if (clickedCard) {
        clickedCard.classList.add("selected");
    }
}
(function () {
    const savedTheme = localStorage.getItem("ecoTheme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);
})();

document.addEventListener("DOMContentLoaded", function () {
    const savedTheme = localStorage.getItem("ecoTheme") || "dark";
    document.querySelectorAll(".theme-card").forEach(card => card.classList.remove("selected"));

    const savedThemeCard = document.querySelector(`[data-theme-val="${savedTheme}"]`);
    if (savedThemeCard) {
        savedThemeCard.classList.add("selected");
    }
});