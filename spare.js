allForms = document.querySelectorAll(".form");
let storePics = [];
async function getFavData(val, title, id, len) {
  // for (let i = 0; i < 6; i++) {
  //   if (len[i]) {
  //     len[i] = len[i];
  //   } else {
  //     len[i] = len[0];
  //   }
  // }
  const res = await axios.post("http://127.0.0.1:5000/get_fav", {
    fav_input: val,
    fav_name: title,
    api_Id: id,
  });
  return res.data;
}

async function deleteFavData(val, title) {
  const res = await axios.post("http://127.0.0.1:5000/delete_fav", {
    fav_input: val,
    fav_name: title,
  });
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
  // let img_link = getPics(len);

  form.addEventListener("click", () => {
    if (input.checked == true) {
      console.log("Turned on");
      console.log(len[0]);
      getFavData(input.value, title, apiId, len);
    }
    // img_link

    if (input.checked == false) {
      deleteFavData(input.value, title);
    }
  });
}

// function getPics(len) {
//   for (let l of len) {
//     storePics.push(l.currentSrc);

//     return storePics;
//   }
// }
