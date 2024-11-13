$(document).ready(function () {
    // Initialize DataTables
    var packagesTable = $('#manage_packages_table').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.1.8/i18n/es-MX.json',
        }
    });

    var userTable = $('#select_driver_table').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.1.8/i18n/es-MX.json',
        },
        select: true,
    });

    var addressTable = $('#select_address_table').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.1.8/i18n/es-MX.json',
        },
        select: {
            style: 'single'
        },
        drawCallback: function (settings) {
            let api = this.api();
            if (api.rows({ filter: 'applied' }).data().length === 0) {
                $('#select_address_table tbody').html(`
                    <tr>
                        <td colspan="9" class="text-center">
                            No se encontraron registros.
                            <button id="add_new_address_btn" class="btn btn-primary mt-3">Agregar nueva dirección</button>
                        </td>
                    </tr>
                `);

                $('#add_new_address_btn').on('click', function () {
                    addAddressModal.show();
                });
            }
        }
    });

    userTable.on('select', function (e, dt, type, indexes) {
        if (type === 'row') {
            var data = userTable
                .rows(indexes)   
                .data()          
                .pluck(0)[0]; 

            $('input[name="assigned_to_user"]').val(data);
        }
    });

    addressTable.on('select', function (e, dt, type, indexes) {
        if (type === 'row') {
            var data = userTable
                .rows(indexes)  
                .data()           
                .pluck(0)[0]; 

            $('input[name="address"]').val(data);
        }
    });

    var addPackageModal = new bootstrap.Modal(document.getElementById('addPackageModal'));
    var editPackageModal = new bootstrap.Modal(document.getElementById('editPackageModal'));
    var selectUserModal = new bootstrap.Modal(document.getElementById('selectUserModal'));
    var selectAddressModal = new bootstrap.Modal(document.getElementById('selectAddressModal'));
    var addAddressModal = new bootstrap.Modal(document.getElementById('addAddressModal'));

    $('button#add-package-btn').on('click', function () {
        let modalBody = $('#addPackageModal').find('.modal-body');
        modalBody.html('');

        $.ajax({
            url: '/registrar_paquete',
            type: 'GET',
            dataType: 'html',
            success: function (response) {
                modalBody.html(response);  
                addPackageModal.show();    
            },
            error: function () {
                alert('Error al cargar el formulario de registro');
            }
        });
    });

    $('body').on('click', '.edit-package-btn', function () {
        let packageId = $(this).data('id');

        let modalBody = $('#editPackageModal').find('.modal-body');
        modalBody.html(''); 

        $.ajax({
            url: '/editar_paquete/' + packageId,
            type: 'GET',
            dataType: 'html',
            success: function (response) {
                modalBody.html(response);  
                editPackageModal.show();  
            },
            error: function () {
                alert('Error al cargar el formulario de edición');
            }
        });
    });


    $('body').on('click', '#select-driver-btn', function () {
        selectUserModal.show();
    });

    $('body').on('click', '#select-address-btn', function () {
        selectAddressModal.show();
    });

    // Handle form submission for both add and edit package form via AJAX
    $('body').on('submit', '#set_package_info', function (event) {
        event.preventDefault(); // Prevent the default form submission

        let form = $(this);
        let formData = form.serialize();

        let actionUrl = form.attr('action');
        let modalToClose = addPackageModal;

        if ($('#editPackageModal').hasClass('show')) {
            actionUrl = '/registrar_paquete';
            modalToClose = editPackageModal;
        }

        $.ajax({
            url: actionUrl,
            type: form.attr('method'),
            data: formData,
            success: function (response) {
                alert('Paquete guardado exitosamente');
                modalToClose.hide();
                packagesTable.ajax.reload();
            },
            error: function () {
                alert('Error al guardar el paquete');
            }
        });
    });

    $('#closeAddAddressModal').on('click', function () {
        addAddressModal.hide();
    });

    $('#closeSelectAddressModalFooter').on('click', function () {
        selectAddressModal.hide();
    });

    $('#closeSelectUserModalFooter').on('click', function () {
        selectUserModal.hide();
    });

    $('body').on('click', '#closeSelectUserModalFooter', function () {
        selectUserModal.hide();
    });
});
