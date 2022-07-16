$(document).ready(function () {
  handleClick();
});

function createImgandAppend(getUrl) {
  const myImg = document.createElement("img");
  myImg.setAttribute("class", "js_img");
  myImg.src = getUrl;
  $("div")[0].append(myImg);
}

// This function gets the URL after the page load event is triggered
async function handleClick() {
  try {
    const searchTerm = document.getElementsByClassName("name");
    const getImage = await getFromApi(searchTerm[0].innerText);

    const getUrl = getImage.data[0].images.original.url;
    createImgandAppend(getUrl);
  } catch {
    return;
  }
}

//This function uses the search term to get the pic data
async function getFromApi(searchTerm) {
  const response = await axios.get(
    `https://api.giphy.com/v1/gifs/search?q=${searchTerm}&api_key=MhAodEJIJxQMxW9XqxKjyXfNYdLoOIym`
  );
  return response.data;
}
