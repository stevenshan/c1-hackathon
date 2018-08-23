$(function(){
    var charities = $(".charity-select");

    function change(self){
        var enum_ = self.attr("enum");

        if (enum_ == undefined) {
            return; 
        }

        enum_ = parseInt(enum_);

        var charity = charityInfo[enum_];

        var name = charity["name"];
        var desc = charity["description"];

        $("#selected-charity-name").html(name);
        $("#selected-charity-desc").html(desc);
    }

    charities.change(function(){
        change($(this));
    });

    var first = $(charities.first());
    change(first);
    first.prop("checked", true);
});