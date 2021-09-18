let clicked = false;

document.getElementById("mobi-icon").addEventListener(
  "click",
  () => {
    clicked = !clicked;
    let sidebar = document.getElementById("sidebar");
    if (clicked) {
      sidebar.style.display = "grid";
      sidebar.style.opacity = "100%";
      sidebar.style.top = "0";
      sidebar.style.transition = "0.3s ease-in-out";
    } else {
      sidebar.style.display = "none";
    }
  },
  false
);

document.getElementById("close-btn").addEventListener(
  "click",
  () => {
    clicked = !clicked;
    let sidebar = document.getElementById("sidebar");
    if (!clicked) {
      sidebar.style.display = "none";
    } else {
      sidebar.style.display = "grid";
    }
  },
  false
);
