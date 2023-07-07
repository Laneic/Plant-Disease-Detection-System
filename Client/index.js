window.addEventListener('DOMContentLoaded', function() {
    const imageUpload = document.getElementById('imageUpload');
    const previewImage = document.getElementById('preview');

    imageUpload.addEventListener('change', function() {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();

        reader.addEventListener('load', function() {
          previewImage.src = reader.result;
        });

        reader.readAsDataURL(file);
      }
    });
  });
window.addEventListener("DOMContentLoaded", (event) => {
    const el = document.getElementById('testing');
    console.log(el)
    if (el) {
      el.addEventListener('click',postImg);
}
})
async function postImg(){
    const image2 =document.getElementById('image').files[0]
    if (image2){ 
    const response =fetch("http://127.0.0.1:5000/predict", {     
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: image2,
    });
    }
    if(!image2){
        console.log("Image not uploaded")
        return
    }

    const result = await response.json();
    console.log("Success:", result);

}
  
