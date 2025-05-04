function updateAllowReload(){
        $.ajax({
            type:"POST",
            url:"/game/opponentDelayReport",
            data:{
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },
            success:function(){
                alert("Sorry For The Delay,Report Sent Successfully; Please Do Not Report Unnecessarily Or You Will Be Banned!!")
                window.location = "/"
            },
            error:function(){
                location.reload()
            }
        })
}

function submitCard(id,card_shape,card_number,player){
    if(player === "player_one"){
        var getAllPlayerOneCards = document.querySelectorAll(".player-one-cards");
        for(var i in getAllPlayerOneCards){
            console.log(getAllPlayerOneCards[i].disabled = true);
        }
    }
    else{
        var getAllPlayerTwoCards = document.querySelectorAll(".player-two-cards");
        for(var i in getAllPlayerTwoCards){
            console.log(getAllPlayerTwoCards[i].disabled = true);
        }
    }
    $.ajax({
        type:"POST",
        url:"/gttWhott/gttWhot/collectCard/"+id+"/"+card_shape+"/"+card_number,
        data:{
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },
        success:function(r){
            location.reload();
        },
        error:function(){
            location.reload();
        }
    })
}


function generalMarket(){
    var getGeneralMarket = document.querySelector(".general-market");
    getGeneralMarket.disabled = true;
    $.ajax({
        type:"POST",
        url:"/gttWhott/gttWhot/generalMarket",
        data:{
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },
        success:function(){
            location.reload();
        },
        error:function(){
            location.reload();
        }
    })
}


//Count Cards
function countCards(){
    $.ajax({
        type:"POST",
        url:"/gttWhott/gttWhot/countCards",
        data:{
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },
        success:function(){
            location.reload();
        },
        error:function(){
            location.reload();
        }
    })
}

//checking game reload
//$(document).ready(function(){
//    setInterval(function(){
//        $.ajax({
//            type:"GET",
//            url:"/gttWhott/gttWhot/check/gameReload",
//            success:function(data){
//                if(data === "True"){
//                    location.reload();
//                    $.ajax({
//                        type:"GET",
//                        url:"/gttWhott/gttWhot/update/gameReload",
//                        success:function(data){
//                            location.reload();
//                        },
//                        error:function(){
//                            location.reload(true);
//                        }
//                    });
//                };
//            },
//            error:function(){
//                location.reload(true);
//            }
//        })
//    },1000)
//})


//End Game
function endGame(){
    $.ajax({
        type:"POST",
        url:"/gttWhott/gttWhot/endGame",
        data:{
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },
        success:function(){
            location.reload();
        },
        error:function(){
            location.reload();
        }
    })
}

//Finish
function finishGame(){
    $.ajax({
        type:"POST",
        url:"/gttWhott/gttWhot/finishGame",
        data:{
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },
        success:function(){
            location.reload();
        },
        error:function(){
            location.reload();
        }
    })
}






