$("document").ready(function() {

    var DisableValAllItem = function(idArrays, disabled) {
        idArrays.forEach(function(idName) {
            $(idName).attr("disabled", disabled);
       });
    };

    var HideValAllItem = function(idArrays, hide) {
        idArrays.forEach(function(idName) {
            if (true === hide) {
                $(idName).hide();
            } else {
                $(idName).show();
            }
        });
    };

    var UpdateCreateResp = function(resp) {
        $('#create-my-private-key').text(resp.my_private_key);
        for (var key in resp.others_private_key) {
            var elementKey = '<td>' + key + '</td>';
            var elementVal = '<td>' + resp.others_private_key[key] + '</td>';
            $('#create-other-private-keys-table tr:last').after('<tr>' + elementKey + elementVal + '</tr>');
        }
    };

    var allItems = {
        "create": {
            "loading-items": [
                '#create-loading-space',
                '#create-loading-icon'
            ],
            "form-items": [
                '#create-num-sig',
                '#create-raw-data',
                '#create-btn'
            ],
            'result-items': [
                '#create-resp'
            ]
        }
    };
    HideValAllItem(allItems.create['loading-items'], true);
    HideValAllItem(allItems.create['result-items'], true);

    $("#create-form").submit(function(e) {
        e.preventDefault();

        DisableValAllItem(allItems.create['form-items'], true);
        HideValAllItem(allItems.create['loading-items'], false);

        var num_sig = $("#create-num-sig").val();
        var raw_data = $("#create-raw-data").val();

        $.post("will/create", {
            "num_sig": num_sig,
            "raw_data": raw_data
        }).done(function(data) {
            var resp = jQuery.parseJSON(data);
            if (!resp.success) {
                console.log(resp);
                return;
            }
            UpdateCreateResp(resp);
            DisableValAllItem(allItems.create['form-items'], false);
            HideValAllItem(allItems.create['loading-items'], true);
            HideValAllItem(allItems.create['result-items'], false);
        });
    });
});
