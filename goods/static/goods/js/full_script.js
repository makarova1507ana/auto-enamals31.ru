$('#img-card-div').on('click', function() {
    document.getElementById("info-card").style.display = "none";
    document.getElementById("footer").style.display = "none";
    document.getElementById("img-full-none").style.display = "block";
    document.getElementById("mainNav").style.display = "none";
});

$('#button-close').on('click', function() {
    document.getElementById("mainNav").style.display = "block";
    document.getElementById("info-card").style.display = "block";
    document.getElementById("footer").style.display = "block";
    document.getElementById("img-full-none").style.display = "none";
});



