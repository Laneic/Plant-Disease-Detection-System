window.addEventListener('DOMContentLoaded', function() {
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
        document.getElementById('plantName').innerText=result=''
        document.getElementById('diseaseName').innerText=''
        document.getElementById('desc').innerText=''
    });
    const el = document.getElementById('submit');
    if (el) {
      el.addEventListener('click',postImg);
    }  
});

async function postImg(){
    const uploadedImage =document.getElementById('imageUpload').files[0]
    const formData = new FormData();
    formData.append('formIMAGE', uploadedImage);
    
    if (uploadedImage){  
        const response = await fetch("http://127.0.0.1:5000/predict", {     
            method: "POST",
            body: formData
        });
        const result = await response.json();
        document.getElementById('plantName').innerText=`Plant Name: ${result.plantName}`
        document.getElementById('diseaseName').innerText=`Disease Name: ${result.disease}`
        document.getElementById('desc').innerText=`Information :${result.diseaseDesc}`
    }
    else{
        console.log("Image not uploaded")
        return
    }
}
  