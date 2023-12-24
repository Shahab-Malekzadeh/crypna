$(document).ready(function () {

    show_time();
    price_websocket();


    // Load more posts in the main page
    $('.load-more').click(function () {
        var card_count = $(".card-count").length;
        console.log("card-count : " + card_count);

        $.ajax({
            url: 'load-more',
            method: 'GET',
            data: {
                "card_count": card_count,
            },
            success: function (data) {
                // do something with the return value here if you like
                more_articles = JSON.parse(data);
                console.log("more_articles : ", more_articles);
                serialized_obj = more_articles.serialized_obj;
                console.log("serialized_obj : ", serialized_obj);
                no_more_article = more_articles.no_more_article;
                console.log(no_more_article);

                console.log(window);
                console.log(window.location);

                $(".card-section").empty();
                for (var i = 0; i < serialized_obj.length; i++) {
                    $(".card-section").append("" +
                        "<div class='col-11 col-sm-10 col-md-6 col-lg-4 col-xl-4 mx-auto px-1 py-2'>\n" +
                        "  <a class='link' href='" +
                        window.location.origin + "/article/" + serialized_obj[i].slug + "'>" +
                        "    <div class='card card-count shadow-sm border-0'>\n" +
                        "      <div class='hover-effect'>\n" +
                        "        <img id='img-" + i + "' class='img-responsive mx-auto' src='' alt=''>\n" +
                        "        <div class='overlay'>\n" +
                        "          <h2 class='home-heading h4'>\n" +
                        serialized_obj[i].when_published +
                        "          </h2>\n" +
                        "          <p class='home-text px-2'>\n" +
                        strip_tags(serialized_obj[i].description.split(' ').splice(0, 20).join(' ')) +
                        "          </p>\n" +
                        "        </div>\n" +
                        "      </div>\n" +
                        "      <div class='card-body'>\n" +
                        "        <p class='card-text home-text mb-0 h5'>\n" +
                        serialized_obj[i].title +
                        "        </p>\n" +
                        "      </div>\n" +
                        "      <div class='card-footer border-0 d-flex justify-content-between'>\n" +
                        "        <small class='home-text-small text-muted font-weight-bold'>\n" +
                        "          <i class='fa fa-user'></i>\n" +
                        serialized_obj[i].author_name +
                        "        </small>\n" +
                        "        <small class='home-text-small text-muted font-weight-bold'>\n" +
                        "          <i class='fa fa-calendar'></i>\n" +
                        serialized_obj[i].publish +
                        "        </small>\n" +
                        "      </div>\n" +
                        "    </div>\n" +
                        "  </a>\n" +
                        "</div>"
                    );
                    $('#img-' + i).attr("src", window.location.origin + serialized_obj[i].thumbnail);
                }
                if (no_more_article === true) {
                    $(".load-more").remove();
                }
            },
            error: function (data) {
            }
        });
    });

});

// show the time of now in header
function show_time() {

    d = new Date();
    year = d.getFullYear();
    month = d.getMonth();
    day = d.getDate();
    d_ad = day + "/" + (month + 1) + "/" + year
    H = d.getHours();
    H = (H < 10) ? "0" + H : H;
    m = d.getMinutes();
    m = (m < 10) ? "0" + m : m;
    s = d.getSeconds();
    s = (s < 10) ? "0" + s : s;

    result_time = " <i class='fa fa-clock-o' aria-hidden='true'></i> " + H + ":" + m;
    result_cal = " <i class='fa fa-calendar' aria-hidden='true'></i> " + d_ad;

    document.getElementById('show_time').innerHTML = result_time + result_cal;
    setTimeout("show_time()", 1000);/* 1 sec */
}

// Show the price of cryptocurrencies in the header
function price_websocket() {
    var loc = window.location;
    var wsStart = 'ws://';
    if (loc.protocol == 'https:') {
        wsStart = 'wss://';
    }
    var endpoint = wsStart + loc.host + loc.pathname; //DEVELOPMENT
    // var endpoint = wsStart + loc.host + ":8001/"; // PRODUCTION
    console.log(endpoint);

    //var socket = new WebSocket(endpoint);
    var socket = new ReconnectingWebSocket(endpoint);
    // console.log(socket);

    socket.onmessage = function (e) {
        // when a message coming from the backend
        data = JSON.parse(e.data)
        //console.log(data);
        console.log(e.data);

        $("#price0").html(parseFloat(data.BTCUSDT[0]).toFixed(1) + "<small> $</small>");
        if (parseFloat(data.BTCUSDT[1]) < 0) {
            $("#last-change0").removeClass('text-success');
            $("#last-change0").addClass('text-danger').html(parseFloat(data.BTCUSDT[1]).toFixed(2) + " %");
        } else {
            $("#last-change0").removeClass('text-danger');
            $("#last-change0").addClass('text-success').html("+" + parseFloat(data.BTCUSDT[1]).toFixed(2) + " %");
        }
        $("#price1").html(parseFloat(data.ETHUSDT[0]).toFixed(3) + "<small> $</small>");
        if (parseFloat(data.ETHUSDT[1]) < 0) {
            $("#last-change1").removeClass('text-success');
            $("#last-change1").addClass('text-danger').html(parseFloat(data.ETHUSDT[1]).toFixed(2) + " %");
        } else {
            $("#last-change1").removeClass('text-danger');
            $("#last-change1").addClass('text-success').html("+" + parseFloat(data.ETHUSDT[1]).toFixed(2) + " %");
        }
        $("#price2").html(parseFloat(data.LTCUSDT[0]).toFixed(3) + "<small> $</small>");
        if (parseFloat(data.LTCUSDT[1]) < 0) {
            $("#last-change2").removeClass('text-success');
            $("#last-change2").addClass('text-danger').html(parseFloat(data.LTCUSDT[1]).toFixed(2) + " %");
        } else {
            $("#last-change2").removeClass('text-danger');
            $("#last-change2").addClass('text-success').html("+" + parseFloat(data.LTCUSDT[1]).toFixed(2) + " %");
        }
        $("#price3").html(parseFloat(data.XRPUSDT[0]).toFixed(3) + "<small> $</small>");
        if (parseFloat(data.XRPUSDT[1]) < 0) {
            $("#last-change3").removeClass('text-success');
            $("#last-change3").addClass('text-danger').html(parseFloat(data.XRPUSDT[1]).toFixed(2) + " %");
        } else {
            $("#last-change3").removeClass('text-danger');
            $("#last-change3").addClass('text-success').html("+" + parseFloat(data.XRPUSDT[1]).toFixed(2) + " %");
        }
        $("#price4").html(parseFloat(data.BCHUSDT[0]).toFixed(3) + "<small> $</small>");
        if (parseFloat(data.BCHUSDT[1]) < 0) {
            $("#last-change4").removeClass('text-success');
            $("#last-change4").addClass('text-danger').html(parseFloat(data.BCHUSDT[1]).toFixed(2) + " %");
        } else {
            $("#last-change4").removeClass('text-danger');
            $("#last-change4").addClass('text-success').html("+" + parseFloat(data.BCHUSDT[1]).toFixed(2) + " %");
        }
        $("#price5").html(parseFloat(data.EOSUSDT[0]).toFixed(3) + "<small> $</small>");
        if (parseFloat(data.EOSUSDT[1]) < 0) {
            $("#last-change5").removeClass('text-success');
            $("#last-change5").addClass('text-danger').html(parseFloat(data.EOSUSDT[1]).toFixed(2) + " %");
        } else {
            $("#last-change5").removeClass('text-danger');
            $("#last-change5").addClass('text-success').html("+" + parseFloat(data.EOSUSDT[1]).toFixed(2) + " %");
        }

    };
    socket.onopen = function (event) {
        // when the websocket opens
        console.log("open: ", event);
    };
    socket.onerror = function (event) {
        // When an error happens
        console.log("error: ", event);
    };
    socket.onclose = function (event) {
        // when the websocket closes
        console.log("close: ", event);
    };
}


function strip_tags(input, allowed) {

    // making sure the allowed arg is a string containing only tags in lowercase (<a><b><c>)
    allowed = (((allowed || "") + "").toLowerCase().match(/<[a-z][a-z0-9]*>/g) || []).join('');
    var tags = /<\/?([a-z][a-z0-9]*)\b[^>]*>/gi,
        commentsAndPhpTags = /<!--[\s\S]*?-->|<\?(?:php)?[\s\S]*?\?>/gi;
    return input.replace(commentsAndPhpTags, '').replace(tags, function ($0, $1) {
        return allowed.indexOf('<' + $1.toLowerCase() + '>') > -1 ? $0 : '';
    });
}


// Owl carousel scripts

$(document).ready(function () {
    var owl = $('.owl-carousel');
    owl.owlCarousel({
        loop: true,
        margin: 10,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: true,
        dots: false,
        nav: false,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
            },
            768: {
                items: 2,
            },
            992: {
                items: 3,
            }
        }
    });
});
