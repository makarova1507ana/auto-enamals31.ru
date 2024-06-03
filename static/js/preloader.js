document.body.onload = function(){
    setTimeout( function() {
        var preloader = document.getElementById('page-preloader');
        if (!preloader.classList.contains('done'))
        {
            document.getElementById("page-preloader").style.display = "none";
            preloader.classList.add('done');
        }
    }, 200);
}