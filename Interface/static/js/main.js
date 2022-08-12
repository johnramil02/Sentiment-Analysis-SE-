$(document).ready(function(){
  $("#sentimentArea").emojioneArea(
    {
      pickerPosition : "bottom"
    }
  );
})

$('.interactive-menu-button a').click(function() {
  $(this).toggleClass('active');
});

var scroll = new SmoothScroll('a[href*="#"]');




$('.more-btn').click(function() {
  $('#hiden-gallery').toggleClass('hide');
  $('#hiden-gallery').toggleClass('open');
  if ( $('#hiden-gallery').is( ".open" ) ) {
    $(".more-btn-inside").text("Show Less.");
  }else {
    $(".more-btn-inside").text("Show More.");
  }
});



function slickify(){
  $('.blog-slider').slick({
      autoplay: true,
      slidesToShow: 3,
      slidesToScroll: 3,
      responsive: [
        {
            breakpoint: 991,
            settings: "unslick"
        }
      ] 
  });
  $(".slick-next").text("");
  $(".slick-next").addClass("icofont-long-arrow-right");
  $(".slick-prev").text("");
  $(".slick-prev").addClass("icofont-long-arrow-left");
}

slickify();
$(window).resize(function(){
  var $windowWidth = $(window).width();
  if ($windowWidth > 991) {
      slickify(); 
      $('#blog-btn').addClass('hide-me');  
  }else if($windowWidth < 991) {
    $('#blog-btn').removeClass('hide-me');
  }
});

$('#blog-btn').click(function() {
  $('.hiden-blog').toggleClass('hide-blog');
  $('.hiden-blog').toggleClass('open-blog');
  if ( $('.hiden-blog').is( ".open-blog" ) ) {
    $("#blog-btn").text("Show Less Stories.");
  }else {
    $("#blog-btn").text("Show More Stories.");
  }
});



// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    //modal.style.display = "none";
  }
}


// SCRIPT FIRST FOR LOADING BUTTONS 

let showDownload = window.localStorage.getItem('show');


//document.getElementById("loading").style.display = "none";

// get the eshow value to flag if downoad button will show up
let show = document.getElementById('show-value').innerHTML

let sentiment_with_emoji_chart = document.getElementById('sentiment-with-emoji-chart').innerHTML 
let show_sentiment_chart = document.getElementById('show-sentiment-chart').innerHTML
let show_with_emoji_chart = document.getElementById('show-with-emoji-chart').innerHTML
let show_sentiment_without_emoji_chart = document.getElementById('show-sentiment-without-emoji-chart').innerHTML

console.log(sentiment_with_emoji_chart)
console.log(show_sentiment_chart)
console.log(show_with_emoji_chart)
console.log(show_sentiment_without_emoji_chart)

if(sentiment_with_emoji_chart != "False"){
    document.getElementById('sentiment-with-emoji-chart-html').style.display = "none";
}

if(show_sentiment_chart != "False"){
    document.getElementById('sentiment-chart-html').style.display = "none";
}

if(show_with_emoji_chart != "False"){
    document.getElementById('with-emoji-chart-html').style.display = "none";
}

if(show_sentiment_without_emoji_chart != "False"){
    document.getElementById('sentiment-without-emoji-chart-html').style.display = "none";
}


//showDownload !='1'  &&  
if(show == "False"){
    
    alert("Invalid File Input")

    window.localStorage.removeItem("show");
    document.getElementById("download").style.display = "none";
    document.getElementById("myBtn").style.display = "none";
    $(".loader-wrapper").css("display","none")


//showDownload !='1'
}else if(show == "Empty"){
    alert("Empty File Input")
    window.localStorage.removeItem("show");
    document.getElementById("download").style.display = "none";
    document.getElementById("myBtn").style.display = "none";
    $(".loader-wrapper").css("display","none")

}else if(show == "True"){
    document.getElementById("download").style.display = "block";
    document.getElementById("myBtn").style.display = "block";

    $(".loader-wrapper").css("display","none")

}else{
    document.getElementById("download").style.display = "none";
    document.getElementById("myBtn").style.display = "none";
    $(".loader-wrapper").css("display","none")
}



// to show and hide download button
  function removeDisable(){

    window.localStorage.setItem("show", "1");

}