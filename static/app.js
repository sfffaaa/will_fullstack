$("document").ready(function() {

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
        },
        "select": {
            "loading-items": [
                '#select-loading-space',
                '#select-loading-icon'
            ],
            "form-items": [
                '#select-private-key',
                '.select-other-keys',
                '#select-add-private-key-btn',
                '#select-del-private-key-btn',
                '#select-btn'
            ],
            'result-items': [
                '#select-resp'
            ]
        }
    };

    var DisableValAllItem = function(idArrays, disabled) {
        idArrays.forEach(function(idName) {
            $(idName).each(function() {
                $(this).attr("disabled", disabled);
            });
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

    HideValAllItem(allItems.create['loading-items'], true);
    HideValAllItem(allItems.create['result-items'], true);
    HideValAllItem(allItems.select['loading-items'], true);

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

    $(document).on('click', '#select-add-private-key-btn', function(e) {
        e.preventDefault();

        var controlForm = $(this).parents('.form-group');
        var currentEntry = $(this).parents('.select-private-entry:first').clone();
        var newEntry = $(currentEntry.clone()).appendTo(controlForm);

        newEntry.find('input').val('');
        controlForm.find('.select-private-entry:not(:last) .btn-add')
            .removeClass('btn-add').addClass('btn-remove')
            .removeClass('btn-success').addClass('btn-danger')
            .attr('id', 'select-del-private-key-btn')
            .html('<div class="fa fa-minus"></div>');

    }).on('click', '#select-del-private-key-btn', function(e) {
        e.preventDefault();
        $(this).parents('.select-private-entry:first').remove();
    });
    var ComposeSelectOtherPrivateKeys = function() {
        var otherPrivateKeysDict = {};
        var idx = 0;
        $(".select-private-entry").each(function() {
            otherPrivateKeysDict[idx] = $(this).find(".form-control").val();
            idx++;
        });
        return otherPrivateKeysDict;
    };

    var UpdateRetrieveResp = function(resp) {
        $('#select-raw-data').text(resp.raw_data);
    };

    $("#select-form").submit(function(e) {
        e.preventDefault();
        DisableValAllItem(allItems.select['form-items'], true);
        HideValAllItem(allItems.select['loading-items'], false);

        var my_private_key = $("#select-private-key").val();
        var others_private_key = ComposeSelectOtherPrivateKeys();

        $.post("will/retrieve", {
            "my_private_key": my_private_key,
            "others_private_key": JSON.stringify(others_private_key)
        }).done(function(data) {
            var resp = jQuery.parseJSON(data);
            if (!resp.success) {
                console.log(resp);
                return;
            }
            UpdateRetrieveResp(resp);
            DisableValAllItem(allItems.select['form-items'], false);
            HideValAllItem(allItems.select['loading-items'], true);
        });
    });
});
