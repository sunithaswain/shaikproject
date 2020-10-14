function cloneMore(selector, type, num) {
    var total = $('#id_' + type + '_set-TOTAL_FORMS').val();
    if(total < num){
        do {
            var newElement = $(selector).clone(true);

            newElement.find(':input').each(function() {
                if($(this).attr('name')){
                    var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
                } else if ($(this).attr('id')){
                    var name = $(this).attr('id').replace('id_', '');
                } 
                var id = 'id_' + name;
                $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
            });
            newElement.find('label').each(function() {
                var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
                $(this).attr('for', newFor);
            });
            total++;
            $(selector).after(newElement);
        } while (total < num);
        $('#id_' + type + '_set-TOTAL_FORMS').val(total);
    }
    // delete last elems if too many
    if(total > num){
        var i = num;
        do {
            // get target to delete
            $(selector + ':last').remove();
            i++;
        } while (total > i);
        $('#id_' + type + '_set-TOTAL_FORMS').val(num);
    }   
}



function reinitDates(selector){
    $formset = $(selector);
    if($('#id_bookingpassenger_set-0-date_of_birth_container').length){
        $formset.find('[data-form-control="date"]:not(.hide)').each(function () {
            $(this).pickadate('stop');
           // $(this).pickadate('start');
        });
        $formset.find('[data-form-control="date"]:not(.hide)').each(function () {
            $(this).pickadate({
                format: "yyyy-mm-dd",
                formatSubmit: "yyyy-mm-dd",
                selectMonths: true,
                selectYears: 100,
                close: 'OK',
                max: true
             });
        });               
    }
}