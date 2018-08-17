$(function(){
    var charities = $(".charity-select");

    function change(elem){
        var self = elem == undefined ? $(this) : elem;
        console.log(self);
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

    charities.change(change);

    var first = $(charities.first());
    change(first);
    first.prop("checked", true);
});