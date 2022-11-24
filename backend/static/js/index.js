window.addEventListener("DOMContentLoaded", () => {
  const translateItem = document.getElementById("translate");
  const uploadBtn = document.getElementById("uploadBtn");
  const fileDialog = document.querySelector(".file-dialog");
  const imageArea = document.querySelector(".image-area");
  const letterArea = document.querySelector(".letter-area");

  let file =
    //FILE UPLOAD HANDLING
    uploadBtn.addEventListener("click", () => fileDialog.click());

  fileDialog.addEventListener("change", () => {
    file = fileDialog.files[0];
    console.log(URL.createObjectURL(file), file);
    imageArea.innerHTML =
      '<img class="uploaded-image" src="' + URL.createObjectURL(file) + '"">';
  });

  translateItem.addEventListener("click", async () => {
    let data = new FormData();
    data.append("file", file);

    console.log("calling post API");
    fetch("/translate", {
      method: "POST",
      body: data,
    })
      .then((response) => response.json())
      .then((response) => {
        console.log("return data", response);
        const { text } = response;
        letterArea.innerHTML = "<div class='output-letter'>" + text + "</div>";
      });
  });
});
