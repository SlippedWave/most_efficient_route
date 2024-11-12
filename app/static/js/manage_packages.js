$(document).ready(function () {
    // Initialize DataTable
    $('#manage_packages_table').dataTable();

    $('button#add-package-btn').on('click', function () {

        var modalBody = $('#addPackageModal').find('.modal-body');
        modalBody.html(''); 

        $.ajax({
            url: '/registrar_paquete',
            type: 'GET',
            dataType: 'html',
            success: function (response) {
                modalBody.html(response);

                var myModal = new bootstrap.Modal(document.getElementById('addPackageModal'));
                myModal.show(); 
            },
            error: function () {
                alert('Error al cargar el formulario de edición');
            }
        });
    });

    $('body').on('click', '.edit-package-btn', function () {
        var package_id = $(this).data('id'); 

        var modalBody = $('#editPackageModal').find('.modal-body');
        modalBody.html(''); 

        $.ajax({
            url: '/editar_paquete/' + package_id,
            type: 'GET',
            dataType: 'html',
            success: function (response) {
                modalBody.html(response);

                var myModal = new bootstrap.Modal(document.getElementById('editPackageModal'));
                myModal.show(); 
            },
            error: function () {
                alert('Error al cargar el formulario de edición');
            }
        });
    });
});
