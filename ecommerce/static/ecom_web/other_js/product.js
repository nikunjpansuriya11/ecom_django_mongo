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



$(document).on('click', '.filter_by', function () { 

    let url = window.location.search;
    let param_s = new URLSearchParams(url);
    const params = new URLSearchParams(window.location.search)
    for (const param of params) {
        if("search" in param){
            key = encodeURIComponent(param[0]);
            value = encodeURIComponent(param[0]);
            param_s.append(key, value);
        }
    }

    param_s.delete('price_sort')
    param_s.delete('name_sort')

    var filter_id = $(this).attr('id');
    if(filter_id == "price_asc" || filter_id == "price_desc" || filter_id == "name_asc" || filter_id == "name_desc"){
        
        if(filter_id == "price_asc"){
            key = encodeURIComponent("price_sort");
            value = encodeURIComponent("asc");
            param_s.append(key, value);

        }
        else if(filter_id == "price_desc"){
            key = encodeURIComponent("price_sort");
            value = encodeURIComponent("desc");
            param_s.append(key, value);
        }
        else if(filter_id == "name_asc"){
            key = encodeURIComponent("name_sort");
            value = encodeURIComponent("asc");
            param_s.append(key, value);
        }
        else{
            key = encodeURIComponent("name_sort");
            value = encodeURIComponent("desc");
            param_s.append(key, value);

        }
    }
    else{
        console.log("error")
        
    }
    
    document.location.search = param_s;
});



$(document).on('click', '.submit-search', function () { 

    let url = window.location.href;
    let param_s = new URLSearchParams(url.search);
    const params = new URLSearchParams(window.location.search)
    for (const param of params) {
        key = encodeURIComponent(param[0]);
        value = encodeURIComponent(param[1]);
        param_s.append(key, value);
        
    }
    param_s.delete('search')


    var search = $('.search').val();
    console.log(search)
    key = encodeURIComponent("search");
    value = encodeURIComponent(search);
    param_s.append(key, value);
    
    
    document.location.search = param_s;
});


$(document).on('click', '#btn_prev', function () { 

    
    let url = window.location.href;
    let param_s = new URLSearchParams(url.search);

    var current_page = 1;
    const params = new URLSearchParams(window.location.search)
    for (const param of params) {
        if( param[0] == "page"){

            var current_page = parseInt(param[1]);
        }
        else{
            var current_page = 1;
        }

        key = encodeURIComponent(param[0]);
        value = encodeURIComponent(param[1]);
        param_s.append(key, value);
        
    }
    param_s.delete('page')


    if (current_page > 1) {
        current_page--;
    }


    key = encodeURIComponent("page");
    value = encodeURIComponent(current_page);
    param_s.append(key, value);
    
    
    document.location.search = param_s;



});


$(document).on('click', '#btn_next', function () { 

    
    let url = window.location.href;
    let param_s = new URLSearchParams(url.search);

    var current_page = 1;
    const params = new URLSearchParams(window.location.search)
    for (const param of params) {
        if( param[0] == "page"){

            var current_page = parseInt(param[1]);
        }
        else{
            var current_page = 1;
        }

        key = encodeURIComponent(param[0]);
        value = encodeURIComponent(param[1]);
        param_s.append(key, value);
        
    }
    param_s.delete('page')

    total_page = $(".total_page").attr("id");
    if (current_page < total_page) {
        current_page++;
    }


    key = encodeURIComponent("page");
    value = encodeURIComponent(current_page);
    param_s.append(key, value);
    
    
    document.location.search = param_s;


});


$(document).on('click', '.add_cart', function () { 
    var element_id = $(this).attr('id');
    
    
  $.ajax({
    url: `/product/`,
    type: "POST",
    data:{
        'id':element_id,
    },
    success: function(data){
          
        console.log(data);
    }
    });

});