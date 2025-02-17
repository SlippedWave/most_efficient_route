$(document).ready(function () {
    // Initialize DataTable
    $('#management_table').dataTable({
        language: {
            url: "https://cdn.datatables.net/plug-ins/2.1.8/i18n/es-MX.json"
        }
    });

    $('button#add-record-btn').on('click', function () {

        var modalBody = $('#addUserModal').find('.modal-dynamic');
        modalBody.html('');

        $.ajax({
            url: '/registrar_usuario',
            type: 'GET',
            dataType: 'html',
            success: function (response) {
                modalBody.html(response);

                var myModal = new bootstrap.Modal(document.getElementById('addUserModal'));
                myModal.show();
            },
            error: function () {
                alert('Error al cargar el formulario de edición');
            }
        });
    });

    $('body').on('click', '.edit-user-btn', function () {
        var userId = $(this).data('id');

        var modalBody = $('#editUserModal').find('.modal-dynamic');
        modalBody.html('');

        $.ajax({
            url: '/editar_usuario/' + userId,
            type: 'GET',
            dataType: 'html',
            success: function (response) {
                modalBody.html(response);

                var myModal = new bootstrap.Modal(document.getElementById('editUserModal'));
                myModal.show();
            },
            error: function () {
                alert('Error al cargar el formulario de edición');
            }
        });
    });
});
