
/*
 * New post buttons
 */
$('#submitPost').click(function() {
    $('#myModal').modal('hide');
});

$('#randomPost').click(function() {
    $('#myModal').modal('hide');
});


/*
 * Infinite scroll
 */
$(window).scroll(function(){
    if($(window).scrollTop() == $(document).height() - $(window).height()) {
        $.ajax({
            TYPE: "GET",
            url: "pagination",
            data: {
                "key": $('.post').get(-1).id
            },
            success: function(data) {
                var data = $.parseJSON(data);
                for (var x = 0; x < data.length; x++) {
                    $('#thePosts').append('<li id="'+data[x]+'" class="post"><a href="https://hackcooper-nocontext.appspot.com/view?key='+data[x]+'&share=1"><img class="postImg" src="/view?key='+data[x]+'"></a><br><ul><li class="fb-share-button" ddata-href="https://hackcooper-nocontext.appspot.com/view?key='+data[x]+'&share=1" data-type="button_count"></li><li class="tweet-link social-buttons"><a href="https://twitter.com/share" class="twitter-share-button" data-url="http://hackcooper-nocontext.appspot.com/view?key='+data[x]+'&share=1" data-via="csherland">Tweet</a></li></ul></li>')
                   }
            }
        });
    }
});

/*
 * Add text to images
 */
function addText(quote,author,imgurl) {
    var fontlist = ['Over the Rainbow','Jolly Lodger','Mystery Quest','Architects Daughter','Happy Monkey','Fascinate','Freckle Face'];
    WebFont.load({
        google: {
            families: fontlist
        },
        active: function(){
            var canvas = document.getElementById("myCanvas");
            var context = canvas.getContext("2d");
            var imageObj = new Image();
            imageObj.onload = function(){
                context.drawImage(imageObj, 0, 0);
                randfont = fontlist[Math.floor((Math.random()*fontlist.length))];
                context.font = "60px " + randfont;
                var quoteheight = (quote.length+1)*60;
                var randheight = Math.floor(Math.random()*(600-quoteheight))+60;
                var y = randheight;
                for (var i in quote){
                    context.fillStyle='black';
                    context.fillText(quote[i],0,y,800);
                    context.fillText(quote[i],0,y+2,800);
                    context.fillText(quote[i],2,y,800);
                    context.fillText(quote[i],2,y+2,800);
                    context.fillStyle='white';
                    context.fillText(quote[i],1,y+1,798);
                    y=y+60;
                }
                var aut_width = context.measureText(author).width;
                var aut_right = 800 - aut_width -1;
                context.fillStyle='black';
                context.fillText(author,aut_right,y,800);
                context.fillText(author,aut_right+2,y+2,800);
                context.fillText(author,aut_right+2,y,800);
                context.fillText(author,aut_right,y+2,800);
                context.fillStyle='white';
                context.fillText(author,aut_right+1,y+1,798);
            }
            imageObj.src = "imgurl"; 
        }
    });
}
