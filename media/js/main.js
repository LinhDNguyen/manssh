$(document).ready(function() {
    // table row color
    $('table.table-list tbody tr:even').addClass("even");
    $('table.table-list tbody tr:odd').addClass("odd");

    $('.form-table tbody tr').each(function(index, element){
        if($(this).children().length == 2) {
            $(this).children().each(function(idx, ele){
                if(idx == 0) {
                    $(this).css("text-align", "right");
                }
            });
        } else {
            $(this).css("text-align", "center");
        }
    });
});

function form_fill(id, type, key) {
    var txtId = $('form[name=frmKey] input:text[name=txtId]');
    var txtType = $('form[name=frmKey] input:text[name=txtType]');
    var txtKey = $('form[name=frmKey] textarea[name=txtKey]');
    txtId.val(id);
    txtType.val(type);
    txtKey.val(key);
}

function add_key() {
    $('form[name=frmKey] input:hidden[name=actionType]').val('');
    form_fill('', 'ssh-rsa', '');
    $('form[name=frmKey] table caption').text('Add new key');
    $('form[name=frmKey] input:text[name=txtType]').parent().parent().hide();
    $('form[name=frmKey] input:text[name=txtId]').parent().parent().hide();
    $('.edit-area').show("slow");

}

function edit_key(idx) {
    $('form[name=frmKey] input:hidden[name=actionType]').val(idx);
    $('form[name=frmKey] table caption').text('Edit key');
    $('form[name=frmKey] input:text[name=txtType]').parent().parent().show();
    $('form[name=frmKey] input:text[name=txtId]').parent().parent().show();
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "manssh/getKeyByIndex",
        async: false,
        data: { keyIdx: idx },
        success: function(key) {
            if (!key) {
                form_fill('', '', '');
            } else {
                form_fill(key.id, key.type, key.key);
            }
            $('.edit-area').show("slow");
            $('.error-msg').hide();
        },
        error: function(key) {
            $('.error-msg').html('Could not get key has index ' + idx + '.');
            $('.error-msg').show("slow");
        }
    });
}

function save_key() {
    var txtId = $('form[name=frmKey] input:text[name=txtId]');
    var txtType = $('form[name=frmKey] input:text[name=txtType]');
    var txtKey = $('form[name=frmKey] textarea[name=txtKey]');
    var txtAction = $('form[name=frmKey] input:hidden[name=actionType]');

    $.ajax({
        type: "GET",
        dataType: "text",
        url: "manssh/saveKey",
        async: false,
        data: { curId: txtId.val(), curType: txtType.val(), curKey: txtKey.val(), actionType: txtAction.val() },
        success: function(resStr) {
            if(resStr.length > 0){
                // error
                $('.error-msg').html(resStr);
                $('.error-msg').show("slow");
            } else {
                $('.edit-area').hide("slow");
                $('.error-msg').hide();
                update_keys();
            }
        },
        error: function(resStr) {
            $('.error-msg').html('Could not save the SSH key. Please try again.');
            $('.error-msg').show("slow");
        }
    });
}

function update_keys() {
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "manssh/getKeys",
        async: false,
        data: { },
        success: function(objs) {
            $('.error-msg').hide();
            // delete all row of ssh list
            var new_str = '';
            var media_url = '/media/';
            $.each(objs, function(key, value) {
                new_str += '<tr><td>' + value['id'] + '</td>';
                new_str += '<td>' + value['type'] + '</td>';
                new_str += '<td>' + value['skey'] + '</td>';
                new_str += '<td class=\'last-column\'>';
                new_str += "<a href='javascript:edit_key(" + value['idx'] + ")'><img src='"+value['media_url']+"img/edit.png' /></a>";
                new_str += "<a href='javascript:delete_key(" + value['idx'] + ")'><img src='"+value['media_url']+"img/delete.png' /></a>";
                new_str += "</td></tr>";
                media_url = value['media_url'];
            });
            new_str += "<tr><td colspan='4' class='lastrow'><a href='javascript:add_key()'><img src='"+media_url+"img/add.png' /></a></td></tr>";

            $('table.table-list tbody').html(new_str);

            $('table.table-list tbody tr:even').addClass("even");
            $('table.table-list tbody tr:odd').addClass("odd");
        },
        error: function(objs) {
            $('.error-msg').html('Could not update the list of SSH keys. Please try again.');
            $('.error-msg').show("slow");
        }
    });
}

function delete_key(idx) {
    var c = confirm("Do you really want to delete this key?");
    if(c == true) {
        $.ajax({
            type: "GET",
            dataType: "text",
            url: "manssh/deleteKey",
            async: false,
            data: { keyIdx: idx },
            success: function(resStr) {
                if(resStr.length > 0){
                    // error
                    $('.error-msg').html(resStr);
                    $('.error-msg').show("slow");
                } else {
                    $('.error-msg').hide();
                    update_keys();
                }
            },
            error: function(resStr) {
                $('.error-msg').html('Could not delete the SSH key. Please try again.');
                $('.error-msg').show("slow");
            }
        });
    }
}

function cancel_key() {
    $('.edit-area').hide("slow");
    $('.error-msg').html('');
    $('.error-msg').hide("slow");
}