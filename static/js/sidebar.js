window.addEventListener('DOMContentLoaded', () => {
    const arrows = document.querySelectorAll(".arrow");
    const sidebar = document.querySelector(".sidebar");
    const sidebarBtn = document.querySelector(".bx-menu");
    
    arrows.forEach(arrow => {
        arrow.addEventListener("click", (e) => {
            const arrowParent = e.target.parentElement.parentElement;
            arrowParent.classList.toggle("showMenu");
        });
    })
    
    sidebarBtn.addEventListener("click", () => {
        sidebar.classList.toggle("close");
    });
})