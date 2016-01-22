$(document).ready(function() {

    $(":submit").click(function(e) {
        e.preventDefault();
        // submit to our server 
        //console.log('First, the data is posted to OUR server.');
        $.ajax({
            url: '/hits/{{id}}',
            type: 'POST',
            data: $('form').serialize(),
            success: function(result) { 
                //console.log('Then, the data is posted to AWS server.');
                $('form').submit();// submit to mechanical turk via the external_submit_url on the html template
            }
        });


    });
  });