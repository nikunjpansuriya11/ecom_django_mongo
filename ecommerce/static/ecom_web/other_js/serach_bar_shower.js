// search_bar_div

var pathname = window.location.pathname;
console.log(pathname);
$(".hdr").removeClass("active");

if (pathname == "/home/"){
    $('.search_bar_div').hide();
    $('.home_hdr').addClass("active");
}
else if(pathname == "/product/"){
    $('.search_bar_div').show();
    $('.all_product_hdr').addClass("active");
}
else if(pathname == "/new_arrivals/"){
    $('.search_bar_div').show();
    $('.new_arrivals_hdr').addClass("active");
}
else if(pathname == "/men/"){
    $('.search_bar_div').show();
    $('.men_hdr').addClass("active");
}
else if(pathname == "/women/"){
    $('.search_bar_div').show();
    $('.women_hdr').addClass("active");
}
else if(pathname == "/kids/"){
    $('.search_bar_div').show();
    $('.kids_hdr').addClass("active");
}
else if(pathname == "/sport/"){
    $('.search_bar_div').show();
    $('.sport_hdr').addClass("active");
}
else if(pathname == "/outlet/"){
    $('.search_bar_div').show();
    $('.outlet_hdr').addClass("active");
}