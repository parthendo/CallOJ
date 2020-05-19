var count=1
function addTests(){
    console.log("inside add tests");
    var str="";
    str+=`<div class="row">`
    str+=`<div class="col-md-6 mb-3">`;
    str+=`<input type="file" name="uploadedFiles" required>`;
    str+=`<div class="invalid-feedback">file required</div> </div>`;
    str+=`<div class="col-md-6 mb-3">`;
    str+=`<input type="file" name="uploadedFiles" required>`;
    str+=`<div class="invalid-feedback">file required</div> </div>`;
    str+=`</div>`;

    //$('#uploadTests').append(str);
    document.getElementById("uploadTests").innerHTML += str;
    count++;
}
// function addTests(){

// }