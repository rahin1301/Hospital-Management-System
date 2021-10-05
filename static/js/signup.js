$(function() {
    $('#subm').click(function() {
 
        $.ajax({
            url: '/signup',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                // window.location.href = "/userHome";
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});