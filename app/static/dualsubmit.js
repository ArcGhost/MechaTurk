$(document).ready(function() {

    $(":submit").click(function(e) {
        e.preventDefault();
        // console.log('First, the data is posted to OUR server.');
        // submit to our server
        $.ajax({
            url: window.location.href, //this should be the internal iframe url
            type: 'post',
            data: $('form').serialize(),
            success: function(result) { 
                console.log('Then, the data is posted to AWS server.');
                $('form').submit();// submit to mechanical turk via the external_submit_url on the html template
            }

        });
});

