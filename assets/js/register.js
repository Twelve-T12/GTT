function validateInput(event){
    const inputValue = event.target.value;
    const regex = /^[a-zA-Z]+$/;
    if(!regex.test(inputValue)){
        event.target.value = inputValue.replace(/[^a-zA-Z]/g);
    }
}

//show password function
function showPassword(){
    console.log("SHOW PASS")
    var getPassword = document.getElementById("password");
    var getConfirmPassword = document.getElementById("confirm_password");
    if(getPassword.type === "password" && getConfirmPassword.type === "password"){
            getPassword.type = "text";
            getConfirmPassword.type = "text"
          }
          else{
            getPassword.type = "password";
            getConfirmPassword.type = "password"
          }
}