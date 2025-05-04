

$(document).ready(function(){
    setInterval(function(){
        $.ajax({
            type:"GET",
            url:"/game/check/game",
            success:function(data){
                if(data == "True"){
                    location.reload();
                }
            },
            error:function(){
                location.reload(true);
            }
        })
    },1000)
})