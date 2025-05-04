//checking game reload
$(document).ready(function(){
    setInterval(function(){
        $.ajax({
            type:"GET",
            url:"/game/checkGameReload",
            success:function(data){
                if(data === "True"){
                    //updating game reload to false
                    $.ajax({
                        type:"GET",
                        url:"/game/updateGameReload",
                        success:function(data){
                            console.log("Update Game Reload DOne")
                        },
                        error:function(){
                            location.reload(true);
                        }
                    });
                    location.reload();
                };
            },
            error:function(){
                location.reload(true);
            }
        })
    },1000)
})




function checkSenderFirstNumber(){
    var getSenderFirstNumber = document.getElementById("sender_first_number");
    if(parseInt(getSenderFirstNumber.value) >= 0){
        if(parseInt(getSenderFirstNumber.value) <= 99){
            getSenderFirstNumber.style.border = "10px solid green";
            var getGenerateGold = document.getElementById("generate_gold_check_box");
            getGenerateGold.style.display = "inline";
        }else{
            getSenderFirstNumber.style.border = "10px solid red";
            var getGenerateGold = document.getElementById("generate_gold_check_box");
            getGenerateGold.style.display = "none";
        }
    }else{
            getSenderFirstNumber.style.border = "10px solid red";
            var getGenerateGold = document.getElementById("generate_gold_check_box");
            getGenerateGold.style.display = "none";
    }
}

function checkSenderSecondNumber(){
    var getSenderSecondNumber = document.getElementById("sender_second_number");
    if(parseInt(getSenderSecondNumber.value) >= 0){
        if(parseInt(getSenderSecondNumber.value) <= 99){
            getSenderSecondNumber.style.border = "10px solid green";
            var getGenerateGold = document.getElementById("generate_gold_check_box");
            getGenerateGold.style.display = "inline";
        }else{
            getSenderSecondNumber.style.border = "10px solid red";
            var getGenerateGold = document.getElementById("generate_gold_check_box");
            getGenerateGold.style.display = "none";
        }
    }else{
            getSenderSecondNumber.style.border = "10px solid red";
            var getGenerateGold = document.getElementById("generate_gold_check_box");
            getGenerateGold.style.display = "none";
    }
}

function generateGold(){
    var getSenderFirstNumber = document.getElementById("sender_first_number");
    var getSenderSign = document.getElementById("sender_sign");
    var getSenderSecondNumber = document.getElementById("sender_second_number");
    if(getSenderFirstNumber.value !== "" && getSenderSecondNumber.value !== ""){
        if(Number.isInteger(parseInt(getSenderFirstNumber.value)) && Number.isInteger(parseInt(getSenderSecondNumber.value))){
             if(parseInt(getSenderFirstNumber.value) >= 0 && parseInt(getSenderSecondNumber.value) >= 0 ){
                       if(parseInt(getSenderFirstNumber.value) <= 99 && parseInt(getSenderSecondNumber.value) <= 99 ){
                                if(getSenderSign.value === "Addition"){
                                    var createInput = document.createElement("input");
                                    createInput.className = "sender-button-gtt text-center my-2 bg-warning text-white";
                                    createInput.name = "sender_golden_number";
                                    createInput.value = parseInt(getSenderFirstNumber.value) + parseInt(getSenderSecondNumber.value);
                                    createInput.readOnly = true;
                                    var createGoldenNumber = document.getElementById("golden_number_space").appendChild(createInput);
                                    getSenderFirstNumber.readOnly = true;
                                    getSenderSecondNumber.readOnly = true;
                                    getSenderSign.hidden = true;
                                    var getGenerateGold = document.getElementById("generate_gold_check_box");
                                    getGenerateGold.hidden = true;
                                    var getSenderSubmit = document.getElementById("sender_submit");
                                    getSenderSubmit.style.display = "inline";
                                }
                                else if(getSenderSign.value === "Multiplication"){
                                    var createInput = document.createElement("input");
                                    createInput.className = "sender-button-gtt text-center my-2 bg-warning text-white";
                                    createInput.name = "sender_golden_number";
                                    createInput.value = parseInt(getSenderFirstNumber.value) * parseInt(getSenderSecondNumber.value);
                                    createInput.readOnly = true;
                                    var createGoldenNumber = document.getElementById("golden_number_space").appendChild(createInput);
                                    getSenderFirstNumber.readOnly = true;
                                    getSenderSecondNumber.readOnly = true;
                                    getSenderSign.hidden = true;
                                    var getGenerateGold = document.getElementById("generate_gold_check_box");
                                    getGenerateGold.hidden = true;
                                    var getSenderSubmit = document.getElementById("sender_submit");
                                    getSenderSubmit.style.display = "inline";
                                }
                            }
                                else{
                                    getSenderFirstNumber.value = "";
                                    getSenderFirstNumber.style.border = "10px solid red";
                                    getSenderSecondNumber.value = "";
                                    getSenderSecondNumber.style.border = "10px solid red";
                                }
                       }
                       else{
                                    getSenderFirstNumber.value = "";
                                    getSenderFirstNumber.style.border = "10px solid red";
                                    getSenderSecondNumber.value = "";
                                    getSenderSecondNumber.style.border = "10px solid red";
                        }
             }
             else{
                                    getSenderFirstNumber.value = "";
                                    getSenderFirstNumber.style.border = "10px solid red";
                                    getSenderSecondNumber.value = "";
                                    getSenderSecondNumber.style.border = "10px solid red";
             }
    }
    else{
                                    getSenderFirstNumber.value = "";
                                    getSenderFirstNumber.style.border = "10px solid red";
                                    getSenderSecondNumber.value = "";
                                    getSenderSecondNumber.style.border = "10px solid red";
    }
}

function sendGoldenNumbers(){
    var getSenderRandomNumber = document.getElementById("sender_random_number");
    getSenderRandomNumber.readOnly = true;
    var getSenderSubmit = document.getElementById("sender_submit");
    getSenderSubmit.style.display = "none";
    var getSenderSpinner = document.getElementById("sender_spinner");
    getSenderSpinner.style.display = "inline";
}


//receiver form
function receiverForm(){
    console.log("receiver form called");
    var getAllReceiverFormButton = document.querySelectorAll(".receiver_form_button");
    for(var i in getAllReceiverFormButton){
        console.log(getAllReceiverFormButton[i].readOnly = true);
    }
}


//Finish Round
function finishRound(){
        $.ajax({
            type:"POST",
            url:"/game/finishRound",
            data:{
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },
            success:function(){
                console.log("Finish Round Called");
                location.reload();
            },
            error:function(){
                location.reload()
            }
        });
        var getFinishRoundButton = document.getElementById("finish_round_button");
        var getFinishRoundSpinner = document.getElementById("finish_round_spinner");
        getFinishRoundButton.style.display  = "none";
        getFinishRoundSpinner.style.display = "inline";
}





//End Game
function endGame(){
        $.ajax({
            type:"POST",
            url:"/game/endGame",
            data:{
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },
            success:function(){
                console.log("End Game Called");
                window.location = "/"
            },
            error:function(){
                location.reload()
            }
        })
}


function opponentDelay(){
        $.ajax({
            type:"POST",
            url:"/game/opponentDelayReport",
            data:{
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },
            success:function(){
                alert("Sorry For The Delay,Report Sent Successfully; Please Do Not Report Unnecessarily Or You Will Be Fined!!")
                window.location = "/"
            },
            error:function(){
                location.reload()
            }
        })
}