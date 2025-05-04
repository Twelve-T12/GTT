$.ajaxSetup({ cache: false });
window.focus();





$(document).on("submit","#search_player",function(e){
        e.preventDefault();

        var getSearchButton = document.getElementById("search_button");
        getSearchButton.style.display = "none";
        var getSearchSpinner = document.getElementById("search_spinner");
        getSearchSpinner.style.display = "inline";

        $.ajax({
          type:"post",
          url:"/searchPlayer",
          data:{
              player_name:$("#player_name").val(),
              csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
          },
          success:function(data){
            console.log(data)
            if( data !== "Unavailable"){
                $(".available_players").empty();
                var tem = `<div class="card text-center my-5 bg-white"><div class="card-header"><div class="d-flex justify-content-around"><p class="text text-warning">${data.player_name}</p></div></div><div class="card-body"><h5 class="card-title text text-warning"><i style="font-size:10px">Stake Amount</i> #${data.member_stake_amount}</h5><p class="card-text text text-warning"><i style="font-size:10px">Win Rate</i> ${data.member_win_ratio}%</p><div class="row"><div class="col-6"><a href="${data.member_game_link}" class="btn btn-outline-dark auth challenge-link" onclick='challenge()'>play<i class="fa fa-eye" aria-hidden="true"></i></a></div><div class="col-6"><a href="${data.member_whatsapp_link}" class="btn btn-outline-dark auth">chat  <i class="fa fa-whatsapp" aria-hidden="true"></i></a></div></div><div class="card-footer text-muted"><h1 id="top">GoldenTwelveTransaction<br><b style="font-size:10px">let's play whot...</b></h1></div></div></div>`;
                $(".available_players").append(tem);
            }else{
                alert("Unavailable");
            }
            var getSearchButton = document.getElementById("search_button");
            getSearchButton.style.display = "inline";
            var getSearchSpinner = document.getElementById("search_spinner");
            getSearchSpinner.style.display = "none";
          },
          error:function(){
            console.log("error")
          }
        }),
        document.getElementById("player_name").value = "";
      })








//Check if user has game
$(document).ready(function(){
    setInterval(function(){
        $.ajax({
            type:"GET",
            url:"/check/challenge",
            success:function(data){
                if(data == "True"){
                    $.ajax({
                        type:"GET",
                        url:"/checkGame",
                        success:function(){
                            alert("You have a challenge and you will be redirected now,please wait...")
                            window.location = "/checkGame"
                        },
                        error:function(){
                            alert("Error Connecting Game!!!")
                        }
                    })
                }
                else{
//                    console.log(data);
                    null
                }
            },
            error:function(){
                location.reload();
            }
        })
    },5000)
})



//Challenge Set-Up
    $(document).ready(function(){
      setInterval(function(){
        $.ajax({
          type:"GET",
          url:"/get/challenges/{{username}}",
          cache: false,
          success:function(response){
            if(response){
              for(var i in response.challenges){
                var receive_request = confirm(`${response.challenges[i].challenger} wants to challenge in ""${response.challenges[i].challenge_game_type}"" with you with sum of #${response.challenges[i].amount}. Do you want too accept?`);
                if(receive_request){
                  $.ajax({
                    type:"POST",
                    url:"/accept/challenge",
                    data:{
                        challenge_id:response.challenges[i].id,
                        username:response.challenges[i].challenger,
                        amount:response.challenges[i].amount,
                        game_challenge_type:response.challenges[i].challenge_game_type,
                        csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
                    },
                    success:function(){
//                        console.log("Challenge Accepted");
                        null
                    },
                    error:function(){
                        alert("Unable To Accept");
                        location.reload(true);
                    }
                  })
                }else{
                  $.ajax({
                    type:"POST",
                    url:"/decline/challenge",
                    data:{
                        challenge_id:response.challenges[i].id,
                        username:response.challenges[i].challenger,
                        amount:response.challenges[i].amount,
                        csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
                    },
                    success:function(response){
                        alert(response);
                    },
                    error:function(){
                        alert("Unable to Decline");
                        location.reload(true);
                    }
                  })
                }
              };
            }
          }
        });
      },5000);
    })

function challenge(e){
    var challengeLink = document.querySelectorAll(".challenge-link");
    for(var i in  challengeLink){
         challengeLink[i].hidden = true;
}
}
