let delForm = document.querySelectorAll(".home_del_form");

// delForm.array.forEach((element) => {
//   element.addEventListener("click", handleClickLoad);
// });
document.addEventListener("DOMContentLoaded", function (event) {
  //the event occurred
  for (let btn of delForm) {
    btn.setAttribute("class", "");
  }
});
window.addEventListener("pageshow", function (event) {
  var historyTraversal =
    event.persisted ||
    (typeof window.performance != "undefined" &&
      window.performance.navigation.type === 2);
  if (historyTraversal) {
    window.location.reload();
  }
});

let coll = document.getElementsByClassName("collapsible");
let i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function () {
    this.classList.toggle("active");
    let content = this.nextElementSibling;
    if (content.style.display === "none") {
      content.style.display = "block";
    } else {
      content.style.display = "none";
    }
  });
}
function handleClickLoad(event) {
  event.preventDefault();
  console.log("DOM NOT loaded");
}
