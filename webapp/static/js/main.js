$(document).ready(function () {
    $(".page-link").click(get_page);
    $(".mybtn").click(annotate);
    $(".threat_annotate").click(threat_annotate)
});

function get_page() {
    window.location.replace(
        $(this).attr("href") + "?threat_type=" + $("#threat_type").val() + "&relevance=" + $("#relevance").val() + "&annotation=" + $("#annotation").val()
    );
}

function threat_annotate() {
    var card = $(this).parent().parent().parent();

    $.ajax({
      type: "POST",
      url: "/threat_annotate",
      data: {
        id: card.find(".tweet_id").text(),
        annotation: $(this).val()
        },
      success: function (data) {
        }
    });

}

function annotate() {
    $(this).addClass("active");
    var otherb = $(this).siblings();
    for(var i = 0; i < otherb.length; i ++){
        otherb.removeClass("active")
    }
    var card = $(this).parent().parent().parent();


    $.ajax({
      type: "POST",
      url: "/annotate",
      data: {
        id: card.find(".tweet_id").text(),
        annotation: $(this).attr('name')
        },
      success: function (data) {
            var header = card.find(".card-header");
            var color;
            if (data.relevance){
                color = "tweet-green";
                header.removeClass("tweet-red");
                header.addClass(color);
                header.text("Relevant")
            } else {
                color = "tweet-red";
                header.removeClass("tweet-green");
                header.addClass(color);
                header.text("Not Relevant")
            }
        }
    });
}