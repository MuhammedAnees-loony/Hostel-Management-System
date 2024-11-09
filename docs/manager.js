// manager.js

document.addEventListener("DOMContentLoaded", () => {
    const dashboardItems = document.querySelectorAll(".dashboard-item");

    dashboardItems.forEach(item => {
        item.addEventListener("click", () => {
            const destination = item.querySelector("a").getAttribute("href");
            window.location.href = destination;
        });

        item.addEventListener("mouseover", () => {
            item.style.backgroundColor = "#45a049";
        });

        item.addEventListener("mouseleave", () => {
            item.style.backgroundColor = "#4CAF50";
        });
    });
});
