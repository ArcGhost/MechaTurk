$(document).ready(function() {


    $(":submit").click(function(e) {
        e.preventDefault();
        alert("First, the data is posted to OUR server.");
        console.log('Then, the data is posted to AWS server.');


        /*
        // submit to our server
        $.ajax({
            url: "/",
            type: 'post',
            data: $('form').serialize(),
            success: function(result) {
                // submit to mechanical turk
                $('form').submit();
            }*/


        });
});

