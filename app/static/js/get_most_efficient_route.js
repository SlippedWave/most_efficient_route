$(document).ready(function () {
    $('#management_table').dataTable({
        language: {
            url: "https://cdn.datatables.net/plug-ins/2.1.8/i18n/es-MX.json"
        },
        columnDefs: [
            {
                targets: 0, // The index of the column to hide
                visible: false,
                searchable: false
            }
        ],
        order: [[1, 'asc']] // Order by the second column (index 1) in ascending order
    });
});
