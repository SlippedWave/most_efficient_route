$(document).ready(function () {
    // Initialize DataTables
    var packagesTable = $('#management_table').DataTable({
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
        columnDefs: [
            {
                target: 0,
                visible: false,
            },
        ],
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

                $('#add_new_address_btn').off('click');
                $('#add_new_address_btn').on('click', function () {

                    let modalBody = $('#addAddressModal').find('.modal-dynamic');
                    modalBody.html('');

                    $.ajax({
                        url: '/registrar_direccion',
                        type: 'GET',
                        dataType: 'html',
                        success: function (response) {
                            modalBody.html(response);
                            addAddressModal.show();
                        },
                        error: function () {
                            alert('Error al cargar el formulario de registro');
                        }
                    });

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

            $('input[name="PCK_USR_assigned_to"]').val(data);
        }
    });

    addressTable.on('select', function (e, dt, type, indexes) {
        if (type === 'row') {
            var data = addressTable
                .rows(indexes)
                .data()
                .pluck(0)[0];

            $('input[name="PCK_ADD_addressId"]').val(data);
        }
    });

    var addPackageModal = new bootstrap.Modal(document.getElementById('addPackageModal'));
    var editPackageModal = new bootstrap.Modal(document.getElementById('editPackageModal'));
    var selectUserModal = new bootstrap.Modal(document.getElementById('selectUserModal'));
    var selectAddressModal = new bootstrap.Modal(document.getElementById('selectAddressModal'));
    var addAddressModal = new bootstrap.Modal(document.getElementById('addAddressModal'));

    $('button#add-record-btn').on('click', function () {
        let modalBody = $('#addPackageModal').find('.modal-dynamic');
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

        let modalBody = $('#editPackageModal').find('.modal-dynamic');
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
        var assigned_to_user = $('input[name="PCK_USR_assigned_to"]').val();

        if (assigned_to_user) {
            var columnData = userTable.column(0).data();

            var rowIndex = columnData.indexOf(assigned_to_user);

            if (rowIndex !== -1) {
                userTable.row(rowIndex).select();
            }
        }

        selectUserModal.show();
    });


    $('body').on('click', '#select-address-btn', function () {
        var selectedAddressId = $('input[name="PCK_ADD_addressId"]').val();  // Get the selected address ID

        if (selectedAddressId) {
            var columnData = addressTable.column(0).data();

            var rowIndex = columnData.indexOf(selectedAddressId);

            if (rowIndex !== -1) {
                addressTable.row(rowIndex).select();  // Select the row by its index
            }
        }

        selectAddressModal.show();  // Show the modal
    });




    // Handle form submission for both add and edit package form via AJAX
    $('body').on('submit', '#set_package_info', function (event) {
        event.preventDefault(); // Prevent the default form submission

        let form = $(this);
        let formData = form.serialize();

        let actionUrl = form.attr('action');
        let modalToClose = addPackageModal;

        if ($('#editPackageModal').hasClass('show')) {
            modalToClose = editPackageModal;
        }

        $.ajax({
            url: actionUrl,
            type: form.attr('method'),
            data: formData,
            success: function (response) {
                alert('Paquete guardado exitosamente');
                modalToClose.hide();
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
