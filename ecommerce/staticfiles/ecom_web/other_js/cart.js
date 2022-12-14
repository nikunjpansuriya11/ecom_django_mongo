// this is for Ajax CSRF_TOKEN ((((((  DO NOT CHANGE IT/ REMOVE  ))))))

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});

// END AJAX CSRF_TOKEN 



$(document).on('click', '.closed', function () { 
    var element_id = $(this).attr('id');
    
   $('.product_'+element_id).remove();


//    PriceCalculator()

    
  $.ajax({
    url: `/cart/`,
    type: "POST",
    data:{
        'id':element_id,
    },
    success: function(data){
          
        console.log(data);
    }
    });

});
