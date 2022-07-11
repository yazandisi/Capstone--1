allForms = document.querySelectorAll(".form");
let storePics = [];
async function getFavData(val, title, id, len) {
  const res = await axios.post(
    "https://video-game-extract.herokuapp.com/get_fav",
    {
      fav_input: val,
      fav_name: title,
      api_Id: id,
    }
  );
  return res.data;
}
async function deleteFavData(val, title) {
  const res = await axios.post(
    "https://video-game-extract.herokuapp.com/delete_fav",
    {
      fav_input: val,
      fav_name: title,
    }
  );
  return res.data;
}

for (let form of allForms) {
  let input = form.querySelector(".input");
  let title = input.parentElement.parentElement.innerText;
  let apiId = parseInt(
    input.parentElement.parentElement.parentElement.parentElement.parentElement
      .parentElement.id
  );
  let len =
    input.parentElement.parentElement.parentElement.parentElement.parentElement
      .children[2].children;
  form.addEventListener("click", () => {
    if (input.checked == true) {
      console.log("Turned on");
      console.log(len[0]);
      getFavData(input.value, title, apiId, len);
    }
    if (input.checked == false) {
      console.log(input.value);
      console.log(title);
      deleteFavData(input.value, title);
    }
  });
}
