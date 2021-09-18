let list = document.querySelectorAll(".nav-item");
for (let i = 0; i < list.length; i++) {
  list[i].onclick = function () {
    let j = 0;
    while (j < list.length) {
      list[j++].className = "nav-item";
    }
    list[i].className = "nav-item active2";
  };
}
