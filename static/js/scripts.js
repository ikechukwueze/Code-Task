
$(document).ready(function(){
    var url = $("#reservation-url").attr("data-reservations-url")
    var reservations_table = $(".reservations-table-body")
    $.ajax({
        method:'GET',
        url: url,
        success: function(response) {
            $.each(response, function(index, value) {
                reservations_table.append(
                    `<tr>
                        <td>${value.rental}</td>
                        <td>${value.reservation_id}</td>
                        <td>${value.checkin}</td>
                        <td>${value.checkout}</td>
                        <td>${value.previous_reservation}</td>
                    </tr>`
                );
            });
        },
    });
});